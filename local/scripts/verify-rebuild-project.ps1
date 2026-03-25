param(
  [string]$Path
)

$ErrorActionPreference = "Stop"

if (-not $Path) {
  throw "Path is required."
}

$verifyTemplateScript = Join-Path $PSScriptRoot "verify-template-package.ps1"
$templateResult = & $verifyTemplateScript `
  -Path $Path `
  -ExpectedReleaseTarget "rebuild-project" `
  -ExpectedVerifyScript "local/scripts/verify-rebuild-project.ps1"

$required = @(
  "REBUILD_AS_NEW_PROJECT.md"
)

$metadataIssues = @($templateResult.metadata_issues)
$resolvedPath = $templateResult.package_path
$missing = @($required | Where-Object {
  -not (Test-Path -LiteralPath (Join-Path $resolvedPath $_))
})

try {
  $manifest = Get-Content -LiteralPath (Join-Path $resolvedPath "manifest.json") -Raw | ConvertFrom-Json
  $release = Get-Content -LiteralPath (Join-Path $resolvedPath "release.json") -Raw | ConvertFrom-Json
  if ($manifest.rebuild_mode -ne "fresh-project") {
    $metadataIssues += "manifest.rebuild_mode must be fresh-project."
  }
  if ($manifest.rebuild_guide -ne "REBUILD_AS_NEW_PROJECT.md") {
    $metadataIssues += "manifest.rebuild_guide must be REBUILD_AS_NEW_PROJECT.md."
  }
  if ($release.rebuild_mode -ne "fresh-project") {
    $metadataIssues += "release.rebuild_mode must be fresh-project."
  }
  if ($release.rebuild_guide -ne "REBUILD_AS_NEW_PROJECT.md") {
    $metadataIssues += "release.rebuild_guide must be REBUILD_AS_NEW_PROJECT.md."
  }
} catch {
  $metadataIssues += "Rebuild manifest or release metadata is invalid."
}

[pscustomobject]@{
  package_path = $resolvedPath
  template_ok = [bool]$templateResult.ok
  missing = $missing
  forbidden_present = $templateResult.forbidden_present
  metadata_issues = $metadataIssues
  ok = [bool]$templateResult.ok -and ($missing.Count -eq 0) -and ($metadataIssues.Count -eq 0)
}
