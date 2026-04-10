param(
  [ValidateSet("repo", "root", "registry", "i18n", "local", "template")]
  [string[]]$Scope = @("repo"),
  [int]$SampleSize = 40,
  [int]$MaxFiles = 200,
  [switch]$Apply,
  [switch]$Force
)

$ErrorActionPreference = "Stop"
$scriptPath = Join-Path $PSScriptRoot "run-renormalize.py"
$args = @($scriptPath)

foreach ($item in $Scope) {
  $args += @("--scope", $item)
}

$args += @("--sample-size", $SampleSize, "--max-files", $MaxFiles)

if ($Apply) {
  $args += "--apply"
}

if ($Force) {
  $args += "--force"
}

$pythonCommand = Get-Command python -ErrorAction SilentlyContinue

if ($pythonCommand) {
  $output = @((& $pythonCommand.Source @args 2>&1))
} else {
  $pyCommand = Get-Command py -ErrorAction SilentlyContinue
  if (-not $pyCommand) {
    throw "Python interpreter not found. Expected 'python' or 'py'."
  }
  $output = @((& $pyCommand.Source -3 @args 2>&1))
}

if ($LASTEXITCODE -ne 0) {
  throw "run-renormalize.py failed: $($output -join [Environment]::NewLine)"
}

$output -join [Environment]::NewLine | ConvertFrom-Json
