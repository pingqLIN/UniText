param(
  [string]$Output
)

$ErrorActionPreference = "Stop"
$script = Join-Path $PSScriptRoot "generate-push-suitability-report.py"
$args = @($script)

if (-not [string]::IsNullOrWhiteSpace($Output)) {
  $args += @("--output", $Output)
}

& python @args
