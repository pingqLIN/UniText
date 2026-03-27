param(
  [string]$Path
)

$ErrorActionPreference = "Stop"

if (-not $Path) {
  throw "Path is required."
}

$verifyTemplateScript = Join-Path $PSScriptRoot "verify-template-package.ps1"
$templateResult = & $verifyTemplateScript -Path $Path
$required = @(
  "REBUILD_AS_NEW_PROJECT.md"
)

$missing = @($required | Where-Object {
  -not (Test-Path (Join-Path $Path $_))
})

[pscustomobject]@{
  package_path = $Path
  template_ok = [bool]$templateResult.ok
  missing = $missing
  forbidden_present = $templateResult.forbidden_present
  ok = [bool]$templateResult.ok -and ($missing.Count -eq 0)
}
