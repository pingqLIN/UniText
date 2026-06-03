param()

$ErrorActionPreference = "Stop"
$script = Join-Path $PSScriptRoot "validate-workspace-sensitive-metadata-rules.py"
$raw = (& python $script --format json | Out-String).Trim()

if ([string]::IsNullOrWhiteSpace($raw)) {
  throw "validate-workspace-sensitive-metadata-rules.py returned empty output"
}

$raw | ConvertFrom-Json
