param(
  [string]$OutputRoot = "ops/rebuild-project",
  [string]$Name = "",
  [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$root = (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$folder = if ($Name) { $Name } else { "rebuild_$stamp" }
$exportScript = Join-Path $PSScriptRoot "export-template-package.ps1"
$verifyScript = Join-Path $PSScriptRoot "verify-template-package.ps1"
$rebuildGuide = Join-Path $root "REBUILD_AS_NEW_PROJECT.md"
$stagingRoot = "ops/template-package"

if (-not (Test-Path -LiteralPath $exportScript)) {
  throw "Template export script not found: $exportScript"
}

if (-not (Test-Path -LiteralPath $rebuildGuide)) {
  throw "Rebuild guide not found: $rebuildGuide"
}

$template = & $exportScript -OutputRoot $stagingRoot -Name $folder -DryRun:$DryRun
$finalOutputRoot = Join-Path $root $OutputRoot
$finalPackage = Join-Path $finalOutputRoot $folder

if ($DryRun) {
  [pscustomobject]@{
    package_path = $finalPackage
    output_root = $finalOutputRoot
    item_count = $template.item_count
    mode = "rebuild-project"
    includes_rebuild_guide = $true
    source_flow = "export-template-package.ps1"
  }
  return
}

$templatePackage = $template.package_path
if (-not (Test-Path -LiteralPath $finalOutputRoot)) {
  New-Item -ItemType Directory -Force -Path $finalOutputRoot | Out-Null
}

if (Test-Path -LiteralPath $finalPackage) {
  throw "Rebuild package path already exists: $finalPackage"
}

Move-Item -LiteralPath $templatePackage -Destination $finalPackage
$package = $finalPackage
Copy-Item -LiteralPath $rebuildGuide -Destination (Join-Path $package "REBUILD_AS_NEW_PROJECT.md") -Force

$manifestPath = Join-Path $package "manifest.json"
$releasePath = Join-Path $package "release.json"
$manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
$release = Get-Content -LiteralPath $releasePath -Raw | ConvertFrom-Json

$manifest.package_path = "."
$manifest | Add-Member -NotePropertyName package_name -NotePropertyValue $folder -Force
$manifest | Add-Member -NotePropertyName rebuild_mode -NotePropertyValue "fresh-project" -Force
$manifest | Add-Member -NotePropertyName rebuild_guide -NotePropertyValue "REBUILD_AS_NEW_PROJECT.md" -Force
$manifest | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $manifestPath

$release.package_path = "."
$release | Add-Member -NotePropertyName package_name -NotePropertyValue $folder -Force
$release | Add-Member -NotePropertyName release_channel -NotePropertyValue "rebuild-project" -Force
$release | Add-Member -NotePropertyName rebuild_guide -NotePropertyValue "REBUILD_AS_NEW_PROJECT.md" -Force
$release | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $releasePath

[pscustomobject]@{
  package_path = $package
  output_root = Split-Path $package -Parent
  item_count = $template.item_count + 1
  manifest = "manifest.json"
  release = "release.json"
  verify_script = $verifyScript
  rebuild_guide = "REBUILD_AS_NEW_PROJECT.md"
}
