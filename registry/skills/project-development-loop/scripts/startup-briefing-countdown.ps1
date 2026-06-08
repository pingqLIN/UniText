param(
    [string]$RepoRoot = (Get-Location).Path,
    [int]$TimeoutSeconds = 60,
    [int]$BarWidth = 28,
    [int]$RefreshMilliseconds = 125,
    [string]$StateRoot = '',
    [switch]$DryRun = $false,
    [switch]$OutputJson = $false,
    [switch]$Reset = $false
)

$normalizedRepoRoot = (Resolve-Path $RepoRoot).Path
$safeStateName = [IO.Path]::GetFileName($normalizedRepoRoot).Replace(':','_')
$defaultStateRoot = [IO.Path]::GetTempPath()
$stateDirectory = if ([string]::IsNullOrWhiteSpace($StateRoot)) {
    Join-Path $defaultStateRoot 'project-development-loop'
} else {
    $StateRoot
}

if (-not (Test-Path -LiteralPath $stateDirectory)) {
    New-Item -ItemType Directory -Path $stateDirectory -Force | Out-Null
}

$stateFile = Join-Path $stateDirectory ("startup-briefing-${safeStateName}.json")
$state = @{}
if (Test-Path -LiteralPath $stateFile) {
    try {
        $state = Get-Content -Raw -LiteralPath $stateFile | ConvertFrom-Json -ErrorAction Stop
    } catch {
        $state = @{}
    }
}

$startedAt = if (($state.started_at) -and -not $Reset) {
    try {
        [datetime]::Parse($state.started_at)
    } catch {
        Get-Date
    }
} else {
    Get-Date
}

$gitBranch = 'unknown'
try {
    $gitBranch = (& git -C $normalizedRepoRoot rev-parse --abbrev-ref HEAD) 2>$null
} catch {
    $gitBranch = 'unknown'
}

$now = Get-Date
$elapsedSeconds = [Math]::Max([double]0, ($now - $startedAt).TotalSeconds)
$remainingSeconds = [Math]::Max([double]0, [double]$TimeoutSeconds - $elapsedSeconds)
$decision = if ($remainingSeconds -gt 0) { 'continue' } else { 'stop' }
$elapsedRounded = [int][Math]::Round($elapsedSeconds)
$remainingRounded = [int][Math]::Ceiling($remainingSeconds)

$ratio = [Math]::Min(1, [Math]::Max([double]0, $elapsedSeconds / [Math]::Max([double]1, [double]$TimeoutSeconds)))
$filled = [int][Math]::Round($ratio * $BarWidth)
$empty = [Math]::Max([int]0, $BarWidth - $filled)

$stateFileContent = [ordered]@{
    schema_version = 1
    repo_root = $normalizedRepoRoot
    branch = $gitBranch
    started_at = $startedAt.ToString('o')
    timeout_seconds = $TimeoutSeconds
    bar_width = $BarWidth
    refresh_milliseconds = $RefreshMilliseconds
    last_checked_at = $now.ToString('o')
    elapsed_seconds = $elapsedRounded
    remaining_seconds = $remainingRounded
    deadline = $startedAt.AddSeconds($TimeoutSeconds).ToString('o')
    progress_bar = if ($decision -eq 'continue' -or $DryRun) {
        ("#" * $filled) + ('-' * $empty)
    } else {
        "#" * $BarWidth
    }
    decision = $decision
}

$stateFileContentJson = $stateFileContent | ConvertTo-Json -Depth 4
Set-Content -Path $stateFile -Value $stateFileContentJson -Encoding UTF8

if ($OutputJson) {
    Write-Output $stateFileContentJson
} else {
    Write-Output $decision
}
