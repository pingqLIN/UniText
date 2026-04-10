param(
  [int]$SampleSize = 40
)

$ErrorActionPreference = "Stop"
$scriptPath = Join-Path $PSScriptRoot "preview-renormalize.py"
$pythonCommand = Get-Command python -ErrorAction SilentlyContinue

if ($pythonCommand) {
  $output = @((& $pythonCommand.Source $scriptPath "--sample-size" $SampleSize 2>&1))
} else {
  $pyCommand = Get-Command py -ErrorAction SilentlyContinue
  if (-not $pyCommand) {
    throw "Python interpreter not found. Expected 'python' or 'py'."
  }
  $output = @((& $pyCommand.Source -3 $scriptPath "--sample-size" $SampleSize 2>&1))
}

if ($LASTEXITCODE -ne 0) {
  throw "preview-renormalize.py failed: $($output -join [Environment]::NewLine)"
}

$output -join [Environment]::NewLine | ConvertFrom-Json
