[CmdletBinding()]
param(
    [Parameter()]
    [string]$TargetPath = (Get-Location).Path,

    [Parameter()]
    [string]$EditorExecutable = "code",

    [Parameter()]
    [string[]]$EditorArguments = @("--reuse-window"),

    [Parameter()]
    [int]$MonitorIndex = -1,

    [Parameter()]
    [ValidateRange(0, 8)]
    [int]$SeamOverlapPx = 1
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName UIAutomationClient

function Resolve-TargetPath {
    param([string]$PathValue)
    $resolved = Resolve-Path -LiteralPath $PathValue -ErrorAction Stop
    return [System.IO.Path]::GetFullPath($resolved.Path).TrimEnd("\")
}

function Get-WindowRectangleFromProcess {
    param([System.Diagnostics.Process]$Process)
    if ($null -eq $Process -or $Process.MainWindowHandle -eq 0) {
        return $null
    }

    try {
        $element = [System.Windows.Automation.AutomationElement]::FromHandle([IntPtr]$Process.MainWindowHandle)
        return $element.Current.BoundingRectangle
    } catch {
        return $null
    }
}

function Get-ScreenWorkAreaFromProcess {
    param([System.Diagnostics.Process]$Process)
    $rect = Get-WindowRectangleFromProcess -Process $Process
    if ($null -eq $rect) {
        throw "Process does not have a usable top-level window."
    }

    $centerX = [int][Math]::Round($rect.Left + ($rect.Width / 2))
    $centerY = [int][Math]::Round($rect.Top + ($rect.Height / 2))
    $point = [System.Drawing.Point]::new($centerX, $centerY)
    return [System.Windows.Forms.Screen]::FromPoint($point).WorkingArea
}

function Set-WindowBoundsByAutomation {
    param(
        [System.Diagnostics.Process]$Process,
        [int]$X,
        [int]$Y,
        [int]$Width,
        [int]$Height
    )

    if ($null -eq $Process -or $Process.MainWindowHandle -eq 0) {
        return $false
    }

    return Set-WindowBoundsByHandleAutomation -Handle ([IntPtr]$Process.MainWindowHandle) -X $X -Y $Y -Width $Width -Height $Height
}

function Set-WindowBoundsByHandleAutomation {
    param(
        [IntPtr]$Handle,
        [int]$X,
        [int]$Y,
        [int]$Width,
        [int]$Height
    )

    if ($Handle -eq [IntPtr]::Zero) {
        return $false
    }

    try {
        $element = [System.Windows.Automation.AutomationElement]::FromHandle($Handle)

        $windowPatternObj = $element.GetCurrentPattern([System.Windows.Automation.WindowPatternIdentifiers]::Pattern)
        if ($null -ne $windowPatternObj) {
            $windowPattern = [System.Windows.Automation.WindowPattern]$windowPatternObj
            $windowPattern.SetWindowVisualState([System.Windows.Automation.WindowVisualState]::Normal)
        }

        $transformPatternObj = $element.GetCurrentPattern([System.Windows.Automation.TransformPatternIdentifiers]::Pattern)
        if ($null -eq $transformPatternObj) {
            return $false
        }

        $transformPattern = [System.Windows.Automation.TransformPattern]$transformPatternObj
        if (-not $transformPattern.Current.CanMove -or -not $transformPattern.Current.CanResize) {
            return $false
        }

        $transformPattern.Move($X, $Y)
        Start-Sleep -Milliseconds 120
        $transformPattern.Resize($Width, $Height)
        return $true
    } catch {
        return $false
    }
}

function Set-WindowBoundsByAutomationAligned {
    param(
        [System.Diagnostics.Process]$Process,
        [int]$X,
        [int]$Y,
        [int]$Width,
        [int]$Height,
        [object]$AlignLeft = $null,
        [object]$AlignTop = $null,
        [object]$AlignWidth = $null,
        [object]$AlignHeight = $null
    )

    $moved = Set-WindowBoundsByAutomation -Process $Process -X $X -Y $Y -Width $Width -Height $Height
    if (-not $moved) {
        return $false
    }

    if ($null -eq $AlignLeft -or $null -eq $AlignTop -or $null -eq $AlignWidth -or $null -eq $AlignHeight) {
        return $true
    }

    $adjustedX = $X
    $adjustedY = $Y
    $adjustedWidth = $Width
    $adjustedHeight = $Height

    for ($i = 0; $i -lt 4; $i++) {
        Start-Sleep -Milliseconds 120
        $rect = Get-WindowRectangleFromProcess -Process $Process
        if ($null -eq $rect) {
            break
        }

        $leftDiff = [int][Math]::Round(([double]$AlignLeft) - $rect.Left)
        $topDiff = [int][Math]::Round(([double]$AlignTop) - $rect.Top)
        $widthDiff = [int][Math]::Round(([double]$AlignWidth) - $rect.Width)
        $heightDiff = [int][Math]::Round(([double]$AlignHeight) - $rect.Height)

        if (
            [Math]::Abs($leftDiff) -le 1 -and
            [Math]::Abs($topDiff) -le 1 -and
            [Math]::Abs($widthDiff) -le 1 -and
            [Math]::Abs($heightDiff) -le 1
        ) {
            return $true
        }

        $adjustedX += $leftDiff
        $adjustedY += $topDiff
        $adjustedWidth = [Math]::Max(100, $adjustedWidth + $widthDiff)
        $adjustedHeight = [Math]::Max(100, $adjustedHeight + $heightDiff)

        $moved = Set-WindowBoundsByAutomation -Process $Process -X $adjustedX -Y $adjustedY -Width $adjustedWidth -Height $adjustedHeight
        if (-not $moved) {
            return $false
        }
    }

    return $true
}

function Get-InvokerTerminalProcess {
    $terminalNames = @("WindowsTerminal", "pwsh", "powershell", "cmd", "ConEmu", "ConEmu64", "mintty")
    $visited = New-Object 'System.Collections.Generic.HashSet[int]'
    $cursorPid = $PID

    while ($cursorPid -gt 0 -and -not $visited.Contains($cursorPid)) {
        [void]$visited.Add($cursorPid)
        $node = Get-CimInstance Win32_Process -Filter "ProcessId = $cursorPid" -ErrorAction SilentlyContinue
        if ($null -eq $node) {
            break
        }

        $parentPid = [int]$node.ParentProcessId
        if ($parentPid -le 0) {
            break
        }

        $parentProc = Get-Process -Id $parentPid -ErrorAction SilentlyContinue
        if ($null -ne $parentProc -and $parentProc.MainWindowHandle -ne 0 -and ($terminalNames -icontains $parentProc.ProcessName)) {
            return $parentProc
        }

        $cursorPid = $parentPid
    }

    return $null
}

function Get-FocusedTerminalProcess {
    $terminalNames = @("WindowsTerminal", "pwsh", "powershell", "cmd", "ConEmu", "ConEmu64", "mintty")
    try {
        $focused = [System.Windows.Automation.AutomationElement]::FocusedElement
        if ($null -eq $focused) { return $null }

        $pid = [int]$focused.Current.ProcessId
        if ($pid -le 0) { return $null }

        $proc = Get-Process -Id $pid -ErrorAction SilentlyContinue
        if ($null -eq $proc) { return $null }
        if (-not ($terminalNames -icontains $proc.ProcessName)) { return $null }

        if ($proc.MainWindowHandle -ne 0) { return $proc }

        return Get-Process -Name $proc.ProcessName -ErrorAction SilentlyContinue |
            Where-Object { $_.MainWindowHandle -ne 0 } |
            Sort-Object StartTime -Descending |
            Select-Object -First 1
    } catch {
        return $null
    }
}

function Get-LatestTerminalProcess {
    $terminalNames = @("WindowsTerminal", "pwsh", "powershell", "cmd", "ConEmu", "ConEmu64", "mintty")
    return Get-Process -ErrorAction SilentlyContinue |
        Where-Object { $_.MainWindowHandle -ne 0 -and ($terminalNames -icontains $_.ProcessName) } |
        Sort-Object StartTime -Descending |
        Select-Object -First 1
}

function Get-TerminalProcess {
    $proc = Get-InvokerTerminalProcess
    if ($null -ne $proc) { return $proc }
    $proc = Get-FocusedTerminalProcess
    if ($null -ne $proc) { return $proc }
    return Get-LatestTerminalProcess
}

function Get-WorkArea {
    param(
        [System.Diagnostics.Process]$TerminalProcess,
        [int]$TargetMonitorIndex
    )

    $screens = [System.Windows.Forms.Screen]::AllScreens
    if ($TargetMonitorIndex -ge 0) {
        if ($TargetMonitorIndex -ge $screens.Length) {
            throw "MonitorIndex $TargetMonitorIndex is out of range. Available monitors: 0..$($screens.Length - 1)."
        }
        return $screens[$TargetMonitorIndex].WorkingArea
    }

    return Get-ScreenWorkAreaFromProcess -Process $TerminalProcess
}

function Wait-ExplorerWindowByPath {
    param(
        [string]$PathValue,
        [bool]$VisibleOnly = $true,
        [int]$TimeoutMs = 5000
    )

    $deadline = (Get-Date).AddMilliseconds($TimeoutMs)
    $shellApp = New-Object -ComObject Shell.Application
    try {
        do {
            foreach ($window in @($shellApp.Windows())) {
                try {
                    $windowPath = [string]$window.Document.Folder.Self.Path
                    if ([string]::IsNullOrWhiteSpace($windowPath)) { continue }
                    $normalized = [System.IO.Path]::GetFullPath($windowPath).TrimEnd("\")
                    if ($normalized -ieq $PathValue.TrimEnd("\")) {
                        if ($VisibleOnly -and -not [bool]$window.Visible) { continue }
                        return $window
                    }
                } catch {
                    continue
                }
            }
            Start-Sleep -Milliseconds 200
        } while ((Get-Date) -lt $deadline)
    } finally {
        if ($null -ne $shellApp) {
            [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($shellApp)
        }
    }
    return $null
}

function Wait-AnyVisibleExplorerWindow {
    param([int]$TimeoutMs = 5000)

    $deadline = (Get-Date).AddMilliseconds($TimeoutMs)
    $shellApp = New-Object -ComObject Shell.Application
    try {
        do {
            foreach ($window in @($shellApp.Windows())) {
                try {
                    if ([bool]$window.Visible -and ([int64]$window.HWND) -ne 0) {
                        return $window
                    }
                } catch {
                    continue
                }
            }
            Start-Sleep -Milliseconds 200
        } while ((Get-Date) -lt $deadline)
    } finally {
        if ($null -ne $shellApp) {
            [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($shellApp)
        }
    }
    return $null
}

function Set-ExplorerBounds {
    param(
        [System.__ComObject]$Window,
        [int]$X,
        [int]$Y,
        [int]$Width,
        [int]$Height
    )

    $handle = [IntPtr][int64]$Window.HWND
    $moved = Set-WindowBoundsByHandleAutomation -Handle $handle -X $X -Y $Y -Width $Width -Height $Height
    if ($moved) {
        return
    }

    $Window.Visible = $true
    $Window.FullScreen = $false
    $Window.Left = $X
    $Window.Top = $Y
    $Window.Width = $Width
    $Window.Height = $Height
}

function Get-EditorProcessNames {
    param([string]$Executable)
    $base = [System.IO.Path]::GetFileNameWithoutExtension($Executable)
    $names = @("Code", "Cursor", "VSCodium")
    if (-not [string]::IsNullOrWhiteSpace($base)) { $names += $base }
    return ($names | Select-Object -Unique)
}

function Get-ExistingEditorProcess {
    param([string[]]$ProcessNames)
    return Get-Process -ErrorAction SilentlyContinue |
        Where-Object { $_.MainWindowHandle -ne 0 -and ($ProcessNames -icontains $_.ProcessName) } |
        Sort-Object StartTime -Descending |
        Select-Object -First 1
}

function Resolve-EditorExecutablePath {
    param([string]$RequestedExecutable)

    $cmd = Get-Command $RequestedExecutable -ErrorAction SilentlyContinue
    if ($null -ne $cmd) {
        return @{
            FilePath = $RequestedExecutable
            Arguments = $EditorArguments + @($path)
            Label = $RequestedExecutable
        }
    }

    $fallbackCandidates = @(
        "C:\Users\ADMIN_miles\AppData\Local\Programs\Microsoft VS Code\Code.exe",
        "C:\Program Files\Microsoft VS Code\Code.exe",
        "C:\Users\ADMIN_miles\AppData\Local\Programs\Cursor\Cursor.exe",
        "C:\Program Files\Cursor\Cursor.exe",
        "C:\Users\ADMIN_miles\AppData\Local\Programs\VSCodium\VSCodium.exe",
        "C:\Program Files\VSCodium\VSCodium.exe"
    )

    foreach ($candidate in $fallbackCandidates) {
        if (Test-Path $candidate) {
            return @{
                FilePath = $candidate
                Arguments = $EditorArguments + @($path)
                Label = $candidate
            }
        }
    }

    return @{
        FilePath = "notepad.exe"
        Arguments = @()
        Label = "notepad.exe"
    }
}

function Wait-EditorProcess {
    param(
        [string[]]$ProcessNames,
        [int[]]$KnownPids,
        [int]$TimeoutMs = 10000
    )

    $deadline = (Get-Date).AddMilliseconds($TimeoutMs)
    do {
        $newProc = Get-Process -ErrorAction SilentlyContinue |
            Where-Object { $_.MainWindowHandle -ne 0 -and ($ProcessNames -icontains $_.ProcessName) -and ($KnownPids -notcontains $_.Id) } |
            Sort-Object StartTime -Descending |
            Select-Object -First 1
        if ($null -ne $newProc) {
            return $newProc
        }

        $latestProc = Get-Process -ErrorAction SilentlyContinue |
            Where-Object { $_.MainWindowHandle -ne 0 -and ($ProcessNames -icontains $_.ProcessName) } |
            Sort-Object StartTime -Descending |
            Select-Object -First 1
        if ($null -ne $latestProc) {
            return $latestProc
        }

        Start-Sleep -Milliseconds 200
    } while ((Get-Date) -lt $deadline)

    return $null
}

$path = Resolve-TargetPath -PathValue $TargetPath

$terminalProc = Get-TerminalProcess
if ($null -eq $terminalProc) {
    throw "Cannot find terminal window to arrange."
}

$workArea = Get-WorkArea -TerminalProcess $terminalProc -TargetMonitorIndex $MonitorIndex
$leftWidth = [int][Math]::Round($workArea.Width * 0.25)
$centerWidth = [int][Math]::Round($workArea.Width * 0.50)
$rightWidth = $workArea.Width - $leftWidth - $centerWidth

$explorerWindow = Wait-ExplorerWindowByPath -PathValue $path -VisibleOnly $true -TimeoutMs 800
if ($null -eq $explorerWindow) {
    Start-Process explorer.exe -ArgumentList @($path) | Out-Null
    $explorerWindow = Wait-ExplorerWindowByPath -PathValue $path -VisibleOnly $true -TimeoutMs 5000
}
if ($null -eq $explorerWindow) {
    $explorerWindow = Wait-AnyVisibleExplorerWindow -TimeoutMs 5000
}
if ($null -eq $explorerWindow) {
    throw "Cannot find Explorer window to arrange."
}

$editorNames = Get-EditorProcessNames -Executable $EditorExecutable
$editorProc = $null
$editorLaunch = Resolve-EditorExecutablePath -RequestedExecutable $EditorExecutable

if ($editorLaunch.FilePath -ne "notepad.exe" -or (Get-Command notepad.exe -ErrorAction SilentlyContinue)) {
    $knownEditorPids = @(Get-Process -ErrorAction SilentlyContinue |
        Where-Object { $editorNames -icontains $_.ProcessName } |
        Select-Object -ExpandProperty Id)

    if ($editorLaunch.Arguments.Count -gt 0) {
        Start-Process -FilePath $editorLaunch.FilePath -ArgumentList $editorLaunch.Arguments | Out-Null
    } else {
        Start-Process -FilePath $editorLaunch.FilePath | Out-Null
    }
    if ($editorLaunch.FilePath -eq "notepad.exe") {
        $editorNames = @("notepad")
    }
    $editorProc = Wait-EditorProcess -ProcessNames $editorNames -KnownPids $knownEditorPids -TimeoutMs 10000
} else {
    $editorProc = Get-ExistingEditorProcess -ProcessNames $editorNames
}

if ($null -eq $editorProc) {
    throw "Cannot find an editor window. Requested executable '$EditorExecutable' and fallbacks are unavailable."
}

Set-ExplorerBounds -Window $explorerWindow -X $workArea.X -Y $workArea.Y -Width $leftWidth -Height $workArea.Height

$overlap = $SeamOverlapPx
$editorTargetX = $workArea.X + $leftWidth - $overlap
$editorTargetY = $workArea.Y
$editorTargetWidth = $centerWidth + (2 * $overlap)
$editorTargetHeight = $workArea.Height

$editorMoved = Set-WindowBoundsByAutomationAligned `
    -Process $editorProc `
    -X $editorTargetX `
    -Y $editorTargetY `
    -Width $editorTargetWidth `
    -Height $editorTargetHeight `
    -AlignLeft $editorTargetX `
    -AlignTop $editorTargetY `
    -AlignWidth $editorTargetWidth `
    -AlignHeight $editorTargetHeight
if (-not $editorMoved) {
    throw "Cannot move editor window using automation."
}

$terminalTargetX = $workArea.X + $leftWidth + $centerWidth - $overlap
$terminalTargetY = $workArea.Y
$terminalTargetWidth = $rightWidth + $overlap
$terminalTargetHeight = $workArea.Height
$terminalMoved = Set-WindowBoundsByAutomationAligned `
    -Process $terminalProc `
    -X $terminalTargetX `
    -Y $terminalTargetY `
    -Width $terminalTargetWidth `
    -Height $terminalTargetHeight `
    -AlignLeft $terminalTargetX `
    -AlignTop $terminalTargetY `
    -AlignWidth $terminalTargetWidth `
    -AlignHeight $terminalTargetHeight
if (-not $terminalMoved) {
    throw "Cannot move terminal window using automation."
}

Write-Host "Three-pane layout applied."
Write-Host "Path: $path"
Write-Host "Editor: $($editorLaunch.Label)"
if ($MonitorIndex -ge 0) {
    Write-Host "MonitorIndex: $MonitorIndex"
}
Write-Host "SeamOverlapPx: $SeamOverlapPx"
