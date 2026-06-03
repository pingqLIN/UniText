param(
    [ValidateSet("Desktop", "Window")]
    [string]$Mode = "Desktop",

    [string]$OutputPath,
    [string]$WindowTitle,
    [string]$ProcessName,
    [switch]$AllScreens,
    [int]$DelayMs = 250
)

$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.Windows.Forms

if (-not ("CodexScreenshot.NativeMethods" -as [type])) {
    Add-Type -TypeDefinition @"
using System;
using System.Text;
using System.Runtime.InteropServices;

namespace CodexScreenshot {
    public static class NativeMethods {
        public delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr lParam);

        [DllImport("user32.dll")]
        public static extern bool EnumWindows(EnumWindowsProc enumProc, IntPtr lParam);

        [DllImport("user32.dll")]
        public static extern bool IsWindowVisible(IntPtr hWnd);

        [DllImport("user32.dll")]
        public static extern int GetWindowTextLength(IntPtr hWnd);

        [DllImport("user32.dll", CharSet = CharSet.Unicode)]
        public static extern int GetWindowText(IntPtr hWnd, StringBuilder text, int count);

        [DllImport("user32.dll")]
        public static extern bool GetWindowRect(IntPtr hWnd, out RECT rect);

        [DllImport("user32.dll")]
        public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint processId);

        [StructLayout(LayoutKind.Sequential)]
        public struct RECT {
            public int Left;
            public int Top;
            public int Right;
            public int Bottom;
        }
    }
}
"@
}

function New-DefaultOutputPath {
    $directory = Join-Path $env:TEMP "codex-screenshots"
    New-Item -ItemType Directory -Force -Path $directory | Out-Null
    $stamp = Get-Date -Format "yyyyMMdd-HHmmss-fff"
    return Join-Path $directory "screenshot-$stamp.png"
}

function Save-BoundsScreenshot {
    param(
        [System.Drawing.Rectangle]$Bounds,
        [string]$Path
    )

    if ($Bounds.Width -le 0 -or $Bounds.Height -le 0) {
        throw "Cannot capture an empty region: $($Bounds.Width)x$($Bounds.Height)."
    }

    $parent = Split-Path -Parent $Path
    if ($parent) {
        New-Item -ItemType Directory -Force -Path $parent | Out-Null
    }

    $bitmap = New-Object System.Drawing.Bitmap $Bounds.Width, $Bounds.Height
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    try {
        $graphics.CopyFromScreen($Bounds.Location, [System.Drawing.Point]::Empty, $Bounds.Size)
        $bitmap.Save($Path, [System.Drawing.Imaging.ImageFormat]::Png)
    }
    finally {
        $graphics.Dispose()
        $bitmap.Dispose()
    }
}

function Get-DesktopBounds {
    if (-not $AllScreens) {
        return [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
    }

    $bounds = [System.Drawing.Rectangle]::Empty
    foreach ($screen in [System.Windows.Forms.Screen]::AllScreens) {
        $bounds = [System.Drawing.Rectangle]::Union($bounds, $screen.Bounds)
    }
    return $bounds
}

function Get-VisibleWindows {
    $windows = New-Object System.Collections.Generic.List[object]
    $callback = [CodexScreenshot.NativeMethods+EnumWindowsProc]{
        param([IntPtr]$handle, [IntPtr]$param)

        if (-not [CodexScreenshot.NativeMethods]::IsWindowVisible($handle)) {
            return $true
        }

        $length = [CodexScreenshot.NativeMethods]::GetWindowTextLength($handle)
        if ($length -le 0) {
            return $true
        }

        $builder = New-Object System.Text.StringBuilder ($length + 1)
        [void][CodexScreenshot.NativeMethods]::GetWindowText($handle, $builder, $builder.Capacity)
        $title = $builder.ToString()

        $processId = 0
        [void][CodexScreenshot.NativeMethods]::GetWindowThreadProcessId($handle, [ref]$processId)
        $process = $null
        try {
            $process = Get-Process -Id $processId -ErrorAction Stop
        }
        catch {
            $process = $null
        }

        $rect = New-Object CodexScreenshot.NativeMethods+RECT
        if (-not [CodexScreenshot.NativeMethods]::GetWindowRect($handle, [ref]$rect)) {
            return $true
        }

        $width = $rect.Right - $rect.Left
        $height = $rect.Bottom - $rect.Top
        if ($width -le 0 -or $height -le 0) {
            return $true
        }

        $windows.Add([pscustomobject]@{
            Handle = $handle
            Title = $title
            ProcessId = [int]$processId
            ProcessName = if ($process) { $process.ProcessName } else { $null }
            Bounds = [System.Drawing.Rectangle]::FromLTRB($rect.Left, $rect.Top, $rect.Right, $rect.Bottom)
        })

        return $true
    }

    [void][CodexScreenshot.NativeMethods]::EnumWindows($callback, [IntPtr]::Zero)
    return $windows
}

function Select-Window {
    $matches = Get-VisibleWindows

    if ($WindowTitle) {
        $matches = $matches | Where-Object { $_.Title -like "*$WindowTitle*" }
    }

    if ($ProcessName) {
        $normalized = [System.IO.Path]::GetFileNameWithoutExtension($ProcessName)
        $matches = $matches | Where-Object { $_.ProcessName -ieq $normalized }
    }

    $selected = $matches | Sort-Object @{ Expression = { $_.Bounds.Width * $_.Bounds.Height }; Descending = $true } | Select-Object -First 1
    if (-not $selected) {
        throw "No visible window matched WindowTitle='$WindowTitle' ProcessName='$ProcessName'."
    }

    return $selected
}

if (-not $OutputPath) {
    $OutputPath = New-DefaultOutputPath
}

Start-Sleep -Milliseconds $DelayMs

if ($Mode -eq "Desktop") {
    $bounds = Get-DesktopBounds
    Save-BoundsScreenshot -Bounds $bounds -Path $OutputPath
    [pscustomobject]@{
        outputPath = (Resolve-Path -LiteralPath $OutputPath).Path
        mode = "Desktop"
        allScreens = [bool]$AllScreens
        width = $bounds.Width
        height = $bounds.Height
        left = $bounds.Left
        top = $bounds.Top
    } | ConvertTo-Json -Depth 4
    exit 0
}

$window = Select-Window
Save-BoundsScreenshot -Bounds $window.Bounds -Path $OutputPath
[pscustomobject]@{
    outputPath = (Resolve-Path -LiteralPath $OutputPath).Path
    mode = "Window"
    title = $window.Title
    processId = $window.ProcessId
    processName = $window.ProcessName
    width = $window.Bounds.Width
    height = $window.Bounds.Height
    left = $window.Bounds.Left
    top = $window.Bounds.Top
} | ConvertTo-Json -Depth 4

