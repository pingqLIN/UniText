param(
  [string]$Path
)

$ErrorActionPreference = "Stop"

if (-not $Path) {
  throw "Path is required."
}

$resolvedPath = (Resolve-Path -LiteralPath $Path).Path

$verifyTemplateScript = Join-Path $PSScriptRoot "verify-template-package.ps1"
$templateResult = & $verifyTemplateScript -Path $resolvedPath
$required = @(
  "REBUILD_AS_NEW_PROJECT.md"
)

$missing = @($required | Where-Object {
  -not (Test-Path (Join-Path $resolvedPath $_))
})

[pscustomobject]@{
  package_path = $resolvedPath
  template_ok = [bool]$templateResult.ok
  missing = $missing
  forbidden_present = $templateResult.forbidden_present
  ok = [bool]$templateResult.ok -and ($missing.Count -eq 0)
}
