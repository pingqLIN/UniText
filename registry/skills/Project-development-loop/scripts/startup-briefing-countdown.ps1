param(
    [string]$RepoRoot = (Get-Location).Path,
    [int]$TimeoutSeconds = 60,
    [int]$BarWidth = 28,
    [int]$RefreshMilliseconds = 125,
    [string]$StateRoot = "$env:LOCALAPPDATA\Codex\project-development-loop\startup-briefing"
)

if ($TimeoutSeconds -lt 1) {
    throw "TimeoutSeconds must be at least 1."
}

if ($BarWidth -lt 10) {
    throw "BarWidth must be at least 10."
}

function Get-NormalizedRepoRoot {
    param([string]$Path)

    try {
        return (Resolve-Path -LiteralPath $Path -ErrorAction Stop).Path
    } catch {
        return $Path
    }
}

function Get-ParentLineageSignature {
    $segments = New-Object System.Collections.Generic.List[string]

    try {
        $currentProcess = Get-CimInstance Win32_Process -Filter "ProcessId = $PID" -ErrorAction Stop
        $ancestorId = [int]$currentProcess.ParentProcessId

        for ($depth = 0; $depth -lt 6 -and $ancestorId -gt 0; $depth++) {
            $ancestor = Get-CimInstance Win32_Process -Filter "ProcessId = $ancestorId" -ErrorAction Stop
            $segments.Add(('{0}:{1}' -f $ancestor.Name, $ancestor.ProcessId))
            $ancestorId = [int]$ancestor.ParentProcessId
        }
    } catch {
        $segments.Add('unknown-parent-lineage')
    }

    if ($segments.Count -eq 0) {
        $segments.Add('no-parent-lineage')
    }

    return ($segments -join '>')
}

function Get-HashHex {
    param([string]$Value)

    $sha256 = [System.Security.Cryptography.SHA256]::Create()

    try {
        $bytes = [System.Text.Encoding]::UTF8.GetBytes($Value)
        $hash = $sha256.ComputeHash($bytes)
        return ([System.BitConverter]::ToString($hash)).Replace('-', '').ToLowerInvariant()
    } finally {
        $sha256.Dispose()
    }
}

$normalizedRepoRoot = Get-NormalizedRepoRoot -Path $RepoRoot
$lineageSignature = Get-ParentLineageSignature
$markerKey = Get-HashHex -Value ($normalizedRepoRoot + '|' + $lineageSignature)
$markerDir = Get-NormalizedRepoRoot -Path $StateRoot
$markerPath = Join-Path $markerDir ($markerKey + '.json')

function Save-Marker {
    param([string]$Status)

    if (-not (Test-Path -LiteralPath $markerDir)) {
        New-Item -ItemType Directory -Path $markerDir -Force | Out-Null
    }

    $payload = [ordered]@{
        repoRoot = $normalizedRepoRoot
        lineageSignature = $lineageSignature
        status = $Status
        recordedAt = (Get-Date).ToString('o')
    } | ConvertTo-Json -Depth 3

    Set-Content -LiteralPath $markerPath -Value $payload -Encoding UTF8
}

if (Test-Path -LiteralPath $markerPath) {
    Write-Output 'skip'
    exit 0
}

$consoleReady = $true

try {
    $null = [Console]::KeyAvailable
    $null = [Console]::CursorVisible
} catch {
    $consoleReady = $false
}

if (-not $consoleReady -or [Console]::IsInputRedirected -or [Console]::IsOutputRedirected) {
    Save-Marker -Status 'noninteractive'
    Write-Output 'noninteractive'
    exit 0
}

$prompt = 'Do you want a project progress briefing? Y/N'
$frames = @('[=   ]', '[==  ]', '[=== ]', '[ ===]', '[  ==]', '[   =]')
$startTime = Get-Date
$frameIndex = 0
$originalCursorVisible = $true
$cursorCaptured = $false
$anchorTop = 0

function Write-FixedConsoleLine {
    param(
        [int]$Top,
        [string]$Text,
        [ConsoleColor]$Color = [ConsoleColor]::Gray
    )

    $width = [Math]::Max(20, [Console]::BufferWidth)
    $safeWidth = [Math]::Max(1, $width - 1)
    $clippedText = if ($Text.Length -gt $safeWidth) {
        $Text.Substring(0, $safeWidth)
    } else {
        $Text
    }

    $previousColor = [Console]::ForegroundColor
    [Console]::SetCursorPosition(0, $Top)
    [Console]::ForegroundColor = $Color
    [Console]::Write($clippedText.PadRight($safeWidth))
    [Console]::ForegroundColor = $previousColor
}

try {
    $originalCursorVisible = [Console]::CursorVisible
    $cursorCaptured = $true
    [Console]::CursorVisible = $false
    $anchorTop = [Console]::CursorTop

    Write-Host ''
    Write-Host ''

    while ($true) {
        while ([Console]::KeyAvailable) {
            $key = [Console]::ReadKey($true)
            $choice = [string]$key.KeyChar

            if ($choice.Equals('Y', [System.StringComparison]::OrdinalIgnoreCase)) {
                Save-Marker -Status 'brief'
                Write-Host ''
                Write-Output 'brief'
                exit 0
            }

            if ($choice.Equals('N', [System.StringComparison]::OrdinalIgnoreCase)) {
                Save-Marker -Status 'continue'
                Write-Host ''
                Write-Output 'continue'
                exit 0
            }
        }

        $elapsed = (Get-Date) - $startTime
        $elapsedSeconds = [Math]::Min($TimeoutSeconds, [int][Math]::Floor($elapsed.TotalSeconds))
        $remainingSeconds = [Math]::Max(0, $TimeoutSeconds - $elapsedSeconds)
        $filledWidth = [Math]::Min($BarWidth, [int][Math]::Floor(($elapsed.TotalSeconds / $TimeoutSeconds) * $BarWidth))
        $emptyWidth = $BarWidth - $filledWidth
        $bar = ('#' * $filledWidth) + ('.' * $emptyWidth)
        $frame = $frames[$frameIndex % $frames.Count]
        $statusLine = "$frame [$bar] $remainingSeconds" + 's'

        Write-FixedConsoleLine -Top $anchorTop -Text 'Project-development-loop startup gate' -Color Cyan
        Write-FixedConsoleLine -Top ($anchorTop + 1) -Text $prompt -Color Yellow
        Write-FixedConsoleLine -Top ($anchorTop + 2) -Text ''
        Write-FixedConsoleLine -Top ($anchorTop + 3) -Text $statusLine -Color Green

        if ($elapsed.TotalSeconds -ge $TimeoutSeconds) {
            Save-Marker -Status 'timeout'
            [Console]::SetCursorPosition(0, $anchorTop + 4)
            Write-Host ''
            Write-Output 'timeout'
            exit 0
        }

        Start-Sleep -Milliseconds $RefreshMilliseconds
        $frameIndex++
    }
} finally {
    if ($cursorCaptured) {
        [Console]::SetCursorPosition(0, $anchorTop + 4)
        [Console]::CursorVisible = $originalCursorVisible
    }
}
