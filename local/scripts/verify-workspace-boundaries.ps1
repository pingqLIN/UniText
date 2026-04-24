param(
  [string[]]$Scope
)

$ErrorActionPreference = "Stop"
$script = Join-Path $PSScriptRoot "verify-workspace-boundaries.py"
$args = @($script, "--format", "json")

foreach ($entry in @($Scope | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })) {
  $args += @("--scope", $entry)
}

$raw = (& python @args | Out-String).Trim()

if ([string]::IsNullOrWhiteSpace($raw)) {
  throw "verify-workspace-boundaries.py returned empty output"
}

$raw | ConvertFrom-Json
