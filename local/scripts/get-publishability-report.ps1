param()

$ErrorActionPreference = "Stop"
$script = Join-Path $PSScriptRoot "get-publishability-report.py"
$raw = (& python $script --format json | Out-String).Trim()

if ([string]::IsNullOrWhiteSpace($raw)) {
  throw "get-publishability-report.py returned empty output"
}

$raw | ConvertFrom-Json
