param(
  [string]$OutputRoot = "ops/template-package",
  [string]$Name = "",
  [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$root = (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path
. (Join-Path $PSScriptRoot "lib\path-safety.ps1")
. (Join-Path $PSScriptRoot "lib\release-integrity.ps1")

$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$folder = if ($Name) {
  Assert-SafeSimpleName -Value $Name -Label "Name" -Pattern '^[a-z0-9][a-z0-9_-]{0,127}$'
} else {
  "template_$stamp"
}

$allowedOutputBase = Get-NormalizedFullPath -BasePath $root -CandidatePath "ops/template-package"
$outputBase = Get-NormalizedFullPath -BasePath $root -CandidatePath $OutputRoot
if (-not (Test-IsUnderPath -RootPath $allowedOutputBase -CandidatePath $outputBase)) {
  throw "OutputRoot must remain under ops/template-package: $outputBase"
}

$package = Join-Path $outputBase $folder
$stagingPackage = Join-Path $outputBase ".$folder.staging_$stamp"
$items = Get-TemplatePackageItems
$excluded = Get-ReleaseExclusions
$evidence = Get-GitEvidence -RepoRoot $root
$packageRelative = Convert-ToRepoRelativePath -RepoRoot $root -Path $package
$outputRootRelative = Convert-ToRepoRelativePath -RepoRoot $root -Path $outputBase

$missing = @($items | Where-Object {
  -not (Test-Path -LiteralPath (Join-Path $root $_.source))
})

if ($missing.Count -gt 0) {
  throw "Missing template package sources: $($missing.source -join ', ')"
}

if ($DryRun) {
  [pscustomobject]@{
    package_path = $package
    package_path_relative = $packageRelative
    output_root = $outputBase
    output_root_relative = $outputRootRelative
    staging_path = $stagingPackage
    release_target = "template-package"
    generation_state = "dry_run"
    item_count = $items.Count
    items = $items
    excluded = $excluded
  }
  return
}

if (Test-Path -LiteralPath $package) {
  throw "Target package path already exists: $package"
}

if (Test-Path -LiteralPath $stagingPackage) {
  throw "Staging package path already exists: $stagingPackage"
}

if (-not (Test-Path -LiteralPath $outputBase)) {
  New-Item -ItemType Directory -Path $outputBase -Force | Out-Null
}

New-Item -ItemType Directory -Path $stagingPackage -Force | Out-Null

$generatedAt = (Get-Date).ToString("s")
$statePath = Join-Path $stagingPackage "generation-state.json"
$markerName = ".unitext-release-complete"
$state = [ordered]@{
  schema_version = 1
  release_target = "template-package"
  generation_state = "in_progress"
  generated_at = $generatedAt
  completed_at = $null
  package_path = $packageRelative
  output_root = $outputRootRelative
  staging_path = (Convert-ToRepoRelativePath -RepoRoot $root -Path $stagingPackage)
  source_root = "."
  phase_target = "template-release-cleanup"
  release_channel = "candidate"
  release_version = "$((Get-Date).ToString('yyyy.MM.dd'))-template-candidate"
  completion_marker = $markerName
  source_commit = $evidence.source_commit
  workspace_dirty = $evidence.workspace_dirty
  item_count = $items.Count
  excluded = $excluded
  items = $items
}
Write-JsonFileAtomic -Path $statePath -Value $state

try {
  foreach ($item in $items) {
    $source = Join-Path $root $item.source
    $target = Join-Path $stagingPackage $item.target
    $parent = Split-Path -Path $target -Parent

    if (-not (Test-Path -LiteralPath $parent)) {
      New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }

    if ($item.kind -eq "file") {
      Copy-Item -LiteralPath $source -Destination $target -Force
      continue
    }

    Copy-Item -LiteralPath $source -Destination $target -Recurse -Force
  }

  $completedAt = (Get-Date).ToString("s")
  $manifest = [ordered]@{
    document_type = "manifest"
    schema_version = 1
    release_target = "template-package"
    generation_state = "complete"
    generated_at = $generatedAt
    completed_at = $completedAt
    package_path = $packageRelative
    output_root = $outputRootRelative
    source_root = "."
    phase_target = "template-release-cleanup"
    release_channel = "candidate"
    release_version = "$((Get-Date).ToString('yyyy.MM.dd'))-template-candidate"
    completion_marker = $markerName
    source_commit = $evidence.source_commit
    workspace_dirty = $evidence.workspace_dirty
    item_count = $items.Count
    excluded = $excluded
    items = $items
  }
  $release = [ordered]@{
    document_type = "release"
    schema_version = 1
    release_target = "template-package"
    generation_state = "complete"
    generated_at = $generatedAt
    completed_at = $completedAt
    package_path = $packageRelative
    output_root = $outputRootRelative
    phase_target = "template-release-cleanup"
    release_channel = "candidate"
    release_version = "$((Get-Date).ToString('yyyy.MM.dd'))-template-candidate"
    completion_marker = $markerName
    verify_script = "local/scripts/verify-template-package.ps1"
    source_commit = $evidence.source_commit
    workspace_dirty = $evidence.workspace_dirty
    item_count = $items.Count
  }
  $state.generation_state = "complete"
  $state.completed_at = $completedAt

  Write-JsonFileAtomic -Path (Join-Path $stagingPackage "manifest.json") -Value $manifest
  Write-JsonFileAtomic -Path (Join-Path $stagingPackage "release.json") -Value $release
  Write-JsonFileAtomic -Path $statePath -Value $state
  Write-Utf8TextAtomic -Path (Join-Path $stagingPackage $markerName) -Content ($completedAt + "`n")

  Finalize-StagedDirectory -StagingPath $stagingPackage -FinalPath $package
} catch {
  try {
    $state.generation_state = "failed"
    $state.failure_message = $_.Exception.Message
    Write-JsonFileAtomic -Path $statePath -Value $state
  } catch {
  }
  throw
}

[pscustomobject]@{
  package_path = $package
  package_path_relative = $packageRelative
  item_count = $items.Count
  manifest = "manifest.json"
  release = "release.json"
  state = "generation-state.json"
  marker = $markerName
}
