[CmdletBinding()]
param(
    [Parameter()]
    [string]$TargetPath = (Get-Location).Path
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName UIAutomationClient

function Resolve-TargetPath {
    param([string]$PathValue)
    $resolved = Resolve-Path -LiteralPath $PathValue -ErrorAction Stop
    return [System.IO.Path]::GetFullPath($resolved.Path)
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
        if ($null -ne $parentProc -and $parentProc.MainWindowHandle -ne 0) {
            if ($terminalNames -icontains $parentProc.ProcessName) {
                return $parentProc
            }
        }

        $cursorPid = $parentPid
    }

    return $null
}

function Get-FocusedTerminalProcess {
    $terminalNames = @("WindowsTerminal", "pwsh", "powershell", "cmd", "ConEmu", "ConEmu64", "mintty")
    try {
        $focused = [System.Windows.Automation.AutomationElement]::FocusedElement
        if ($null -eq $focused) {
            return $null
        }

        $pid = [int]$focused.Current.ProcessId
        if ($pid -le 0) {
            return $null
        }

        $proc = Get-Process -Id $pid -ErrorAction SilentlyContinue
        if ($null -eq $proc) {
            return $null
        }

        if (-not ($terminalNames -icontains $proc.ProcessName)) {
            return $null
        }

        if ($proc.MainWindowHandle -ne 0) {
            return $proc
        }

        $procByName = Get-Process -Name $proc.ProcessName -ErrorAction SilentlyContinue |
            Where-Object { $_.MainWindowHandle -ne 0 } |
            Sort-Object StartTime -Descending |
            Select-Object -First 1
        return $procByName
    } catch {
        return $null
    }
}

function Get-LatestTerminalProcess {
    $terminalNames = @("WindowsTerminal", "pwsh", "powershell", "cmd", "ConEmu", "ConEmu64", "mintty")
    $process = Get-Process -ErrorAction SilentlyContinue |
        Where-Object { $_.MainWindowHandle -ne 0 -and ($terminalNames -icontains $_.ProcessName) } |
        Sort-Object StartTime -Descending |
        Select-Object -First 1
    return $process
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

function Get-BestVisibleTerminalProcess {
    $terminalNames = @("WindowsTerminal", "pwsh", "powershell", "cmd", "ConEmu", "ConEmu64", "mintty")
    $preferredScreen = [System.Windows.Forms.Screen]::FromPoint([System.Windows.Forms.Cursor]::Position)

    $candidates = Get-Process -ErrorAction SilentlyContinue |
        Where-Object { $_.MainWindowHandle -ne 0 -and ($terminalNames -icontains $_.ProcessName) }

    if ($null -eq $candidates -or $candidates.Count -eq 0) {
        return $null
    }

    $onPreferredScreen = @()
    foreach ($candidate in $candidates) {
        $rect = Get-WindowRectangleFromProcess -Process $candidate
        if ($null -eq $rect) {
            continue
        }

        $centerX = [int][Math]::Round($rect.Left + ($rect.Width / 2))
        $centerY = [int][Math]::Round($rect.Top + ($rect.Height / 2))
        $screen = [System.Windows.Forms.Screen]::FromPoint([System.Drawing.Point]::new($centerX, $centerY))
        if ($screen.DeviceName -eq $preferredScreen.DeviceName) {
            $onPreferredScreen += $candidate
        }
    }

    if ($onPreferredScreen.Count -gt 0) {
        return $onPreferredScreen | Sort-Object StartTime -Descending | Select-Object -First 1
    }

    return $candidates | Sort-Object StartTime -Descending | Select-Object -First 1
}

function Activate-Window {
    param(
        [System.__ComObject]$Shell,
        [int]$ProcessId = 0,
        [string]$Title = "",
        [string]$Name
    )

    if ($ProcessId -gt 0 -and $Shell.AppActivate($ProcessId)) {
        return
    }

    if (-not [string]::IsNullOrWhiteSpace($Title) -and $Shell.AppActivate($Title)) {
        return
    }
    throw "Cannot activate $Name window."
}

function Send-SnapKey {
    param(
        [System.__ComObject]$Shell,
        [ValidateSet("LEFT", "RIGHT")]
        [string]$Direction
    )

    Start-Sleep -Milliseconds 200
    $Shell.SendKeys("#{$Direction}")
    Start-Sleep -Milliseconds 300
}

function Wait-ExplorerWindowByPath {
    param(
        [string]$PathValue,
        [bool]$VisibleOnly = $true,
        [int]$TimeoutMs = 8000
    )

    $deadline = (Get-Date).AddMilliseconds($TimeoutMs)
    $shellApp = New-Object -ComObject Shell.Application
    try {
        do {
            foreach ($window in @($shellApp.Windows())) {
                try {
                    $windowPath = [string]$window.Document.Folder.Self.Path
                    if ([string]::IsNullOrWhiteSpace($windowPath)) {
                        continue
                    }

                    $normalized = [System.IO.Path]::GetFullPath($windowPath).TrimEnd("\")
                    if ($normalized -ieq $PathValue.TrimEnd("\")) {
                        if ($VisibleOnly -and -not [bool]$window.Visible) {
                            continue
                        }
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

function Get-ScreenWorkAreaFromProcess {
    param([System.Diagnostics.Process]$Process)

    if ($null -eq $Process -or $Process.MainWindowHandle -eq 0) {
        throw "Process does not have a top-level window handle."
    }

    $element = [System.Windows.Automation.AutomationElement]::FromHandle([IntPtr]$Process.MainWindowHandle)
    $rect = $element.Current.BoundingRectangle
    $centerX = [int][Math]::Round($rect.Left + ($rect.Width / 2))
    $centerY = [int][Math]::Round($rect.Top + ($rect.Height / 2))
    $point = [System.Drawing.Point]::new($centerX, $centerY)
    return [System.Windows.Forms.Screen]::FromPoint($point).WorkingArea
}

function Set-ExplorerBounds {
    param(
        [System.__ComObject]$Window,
        [int]$X,
        [int]$Y,
        [int]$Width,
        [int]$Height
    )

    $Window.Visible = $true
    $Window.FullScreen = $false
    $Window.Left = $X
    $Window.Top = $Y
    $Window.Width = $Width
    $Window.Height = $Height
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

    try {
        $element = [System.Windows.Automation.AutomationElement]::FromHandle([IntPtr]$Process.MainWindowHandle)
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

$path = Resolve-TargetPath -PathValue $TargetPath
$shell = New-Object -ComObject WScript.Shell

$terminalProc = Get-FocusedTerminalProcess
if ($null -eq $terminalProc) {
    $terminalProc = Get-InvokerTerminalProcess
}
if ($null -eq $terminalProc) {
    $terminalProc = Get-LatestTerminalProcess
}
if ($null -eq $terminalProc) {
    $terminalProc = Get-BestVisibleTerminalProcess
}
if ($null -eq $terminalProc) {
    throw "Cannot find a terminal window to arrange."
}

$workArea = Get-ScreenWorkAreaFromProcess -Process $terminalProc
$leftWidth = [int][Math]::Floor($workArea.Width / 2)
$rightWidth = $workArea.Width - $leftWidth

$explorerWindow = Wait-ExplorerWindowByPath -PathValue $path -VisibleOnly $true -TimeoutMs 800
if ($null -eq $explorerWindow) {
    Start-Process explorer.exe -ArgumentList @($path) | Out-Null
    try {
        $explorerWindow = Wait-ExplorerWindowByPath -PathValue $path -VisibleOnly $true -TimeoutMs 5000
    } catch {
        $explorerWindow = Wait-AnyVisibleExplorerWindow -TimeoutMs 5000
    }
}

if ($null -eq $explorerWindow) {
    throw "Cannot locate an Explorer window to arrange."
}

Set-ExplorerBounds -Window $explorerWindow -X $workArea.X -Y $workArea.Y -Width $leftWidth -Height $workArea.Height

$terminalSized = Set-WindowBoundsByAutomation -Process $terminalProc -X ($workArea.X + $leftWidth) -Y $workArea.Y -Width $rightWidth -Height $workArea.Height
if (-not $terminalSized) {
    Activate-Window -Shell $shell -ProcessId $terminalProc.Id -Title $terminalProc.MainWindowTitle -Name "Terminal"
    Send-SnapKey -Shell $shell -Direction "RIGHT"
}

Write-Host "Dual-pane layout applied."
Write-Host "Path: $path"
