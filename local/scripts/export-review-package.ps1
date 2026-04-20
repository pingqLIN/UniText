param(
  [string]$OutputRoot = "ops/review-package",
  [string]$Name = "",
  [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$root = (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path
. (Join-Path $PSScriptRoot "lib\path-safety.ps1")
$contractPath = Join-Path $root "docs/reviews/external-review-bundle.contract.json"
$contract = Get-Content $contractPath -Raw | ConvertFrom-Json
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$folder = if ($Name) {
  Assert-SafeSimpleName -Value $Name -Label "Name" -Pattern '^[a-z0-9][a-z0-9_-]{0,127}$'
} else {
  "review_$stamp"
}
$allowedOutputBase = Get-NormalizedFullPath -BasePath $root -CandidatePath "ops/review-package"
$outputBase = Get-NormalizedFullPath -BasePath $root -CandidatePath $OutputRoot
if (-not (Test-IsUnderPath -RootPath $allowedOutputBase -CandidatePath $outputBase)) {
  throw "OutputRoot must remain under ops/review-package: $outputBase"
}
$package = Join-Path $outputBase $folder
$coreSkills = @($contract.skills.core)
$expansionSkills = @($contract.skills.expansion)
$items = @()

$items += @($contract.files) | ForEach-Object {
  [pscustomobject]@{
    kind = "file"
    path = [string]$_
  }
}

$items += @($contract.directories) | ForEach-Object {
  [pscustomobject]@{
    kind = "dir"
    path = [string]$_
  }
}

$items += $coreSkills | ForEach-Object {
  [pscustomobject]@{
    kind = "dir"
    path = "registry/skills/$_"
  }
}

$items += $expansionSkills | ForEach-Object {
  [pscustomobject]@{
    kind = "dir"
    path = "registry/skills/$_"
  }
}

$missing = @($items | Where-Object {
  -not (Test-Path (Join-Path $root $_.path))
})

if ($missing.Count -gt 0) {
  throw "Missing review package sources: $($missing.path -join ', ')"
}

if ($DryRun) {
  [pscustomobject]@{
    package_path = $package
    output_root = $outputBase
    item_count = $items.Count
    skills_core = $coreSkills
    skills_expansion = $expansionSkills
    items = $items
  }
  return
}

if (Test-Path $package) {
  throw "Target package path already exists: $package"
}

New-Item -ItemType Directory -Path $package -Force | Out-Null

foreach ($item in $items) {
  $source = Join-Path $root $item.path
  $target = Join-Path $package $item.path
  $parent = Split-Path $target -Parent

  if (-not (Test-Path $parent)) {
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
  }

  if ($item.kind -eq "file") {
    Copy-Item -LiteralPath $source -Destination $target -Force
    continue
  }

  Copy-Item -LiteralPath $source -Destination $parent -Recurse -Force
}

$manifest = [ordered]@{
  generated_at = (Get-Date).ToString("s")
  source_root = "."
  package_path = $package
  phase_target = [string]$contract.phase_target
  contract_path = "docs/reviews/external-review-bundle.contract.json"
  reading_order = @($contract.reading_order)
  item_count = $items.Count
  excluded = @($contract.excluded)
  skills_core = $coreSkills
  skills_expansion = $expansionSkills
  items = $items
}

$manifest | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $package "manifest.json")

[pscustomobject]@{
  package_path = $package
  item_count = $items.Count
  manifest = "manifest.json"
}
