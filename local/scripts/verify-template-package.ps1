param(
  [string]$Path,
  [string]$ExpectedReleaseTarget = "template-package",
  [string]$ExpectedVerifyScript = "local/scripts/verify-template-package.ps1"
)

$ErrorActionPreference = "Stop"

if (-not $Path) {
  throw "Path is required."
}

$root = (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path
. (Join-Path $PSScriptRoot "lib\path-safety.ps1")
. (Join-Path $PSScriptRoot "lib\release-integrity.ps1")

function Get-OptionalPropertyValue {
  param(
    $Value,
    [Parameter(Mandatory)][string]$Name
  )

  if ($null -eq $Value) {
    return $null
  }

  $property = $Value.PSObject.Properties[$Name]
  if ($null -eq $property) {
    return $null
  }

  return $property.Value
}

$resolvedPath = Get-NormalizedFullPath -BasePath $root -CandidatePath $Path
$required = @(
  ".gitignore",
  ".mcp.json",
  ".claude\\settings.json",
  "README.md",
  "INDEX.md",
  "VISION.md",
  "RESOURCE_SPEC.md",
  "OPERATIONS.md",
  "PROJECT_MODES.md",
  "SECRET_HANDLING_GUIDELINES.md",
  "MILESTONES.md",
  "TEMPLATE_RELEASE_PACKAGE.md",
  "TEMPLATE_RELEASE_CHECKLIST.md",
  "manifest.json",
  "release.json",
  "generation-state.json",
  ".unitext-release-complete",
  "registry\\skills\\example-skill\\SKILL.md",
  "registry\\agents\\example-agent\\AGENT.md",
  "registry\\mcp\\claude-project-mcp-seed\\server.py",
  "registry\\mcp\\claude-project-mcp-seed\\definition.json",
  "registry\\mcp\\example-mcp\\definition.json",
  "registry\\workflow\\example-workflow\\WORKFLOW.md",
  "local\\README.md",
  "local\\docs\\PATH_MAP.md",
  "local\\scripts\\bootstrap.py",
  "local\\scripts\\verify-bootstrap.py",
  "local\\scripts\\create-git-bundle.py",
  "local\\scripts\\sync-skills.ps1"
)

$forbidden = @(
  "backup",
  "recovered_20260318_165117",
  ".bak_20260315_00",
  "ops\\history",
  "EXTERNAL_REVIEW_PACKAGE.md",
  "EXTERNAL_REVIEW_COVER_NOTE.md",
  "EXTERNAL_REVIEW_HIGHLIGHTS.md",
  "PROJECT_STATUS_REPORT_2026-03-23.md"
)

$missing = @($required | Where-Object {
  -not (Test-Path -LiteralPath (Join-Path $resolvedPath $_))
})

$presentForbidden = @($forbidden | Where-Object {
  Test-Path -LiteralPath (Join-Path $resolvedPath $_)
})

$metadataIssues = @()
$leaf = Split-Path -Path $resolvedPath -Leaf
if ($leaf.StartsWith(".")) {
  $metadataIssues += "Package path appears to be a staging or hidden directory."
}

$manifest = $null
$release = $null
$state = $null

try {
  $manifest = Read-JsonFile -Path (Join-Path $resolvedPath "manifest.json")
} catch {
  $metadataIssues += "manifest.json is missing or invalid JSON."
}

try {
  $release = Read-JsonFile -Path (Join-Path $resolvedPath "release.json")
} catch {
  $metadataIssues += "release.json is missing or invalid JSON."
}

try {
  $state = Read-JsonFile -Path (Join-Path $resolvedPath "generation-state.json")
} catch {
  $metadataIssues += "generation-state.json is missing or invalid JSON."
}

$actualRelative = $null
$packageParentRelative = $null
try {
  $actualRelative = Convert-ToRepoRelativePath -RepoRoot $root -Path $resolvedPath
  $packageParentRelative = Convert-ToRepoRelativePath -RepoRoot $root -Path (Split-Path -Path $resolvedPath -Parent)
} catch {
  $metadataIssues += "Package path is outside the repo root."
}

foreach ($document in @(
    [pscustomobject]@{ label = "manifest"; value = $manifest; expectedType = "manifest" },
    [pscustomobject]@{ label = "release"; value = $release; expectedType = "release" },
    [pscustomobject]@{ label = "state"; value = $state; expectedType = $null }
  )) {
  if ($null -eq $document.value) {
    continue
  }

  $documentType = Get-OptionalPropertyValue -Value $document.value -Name "document_type"
  $releaseTarget = Get-OptionalPropertyValue -Value $document.value -Name "release_target"
  $generationState = Get-OptionalPropertyValue -Value $document.value -Name "generation_state"
  $packagePath = Get-OptionalPropertyValue -Value $document.value -Name "package_path"

  if ($document.expectedType -and $documentType -ne $document.expectedType) {
    $metadataIssues += "$($document.label).document_type must be $($document.expectedType)."
  }
  if ($releaseTarget -ne $ExpectedReleaseTarget) {
    $metadataIssues += "$($document.label).release_target must be $ExpectedReleaseTarget."
  }
  if ($generationState -ne "complete") {
    $metadataIssues += "$($document.label).generation_state must be complete."
  }
  if ($actualRelative -and $packagePath -ne $actualRelative) {
    $metadataIssues += "$($document.label).package_path does not match the actual package path."
  }
}

if ($manifest) {
  $manifestOutputRoot = Get-OptionalPropertyValue -Value $manifest -Name "output_root"
  if ($packageParentRelative -and $manifestOutputRoot -ne $packageParentRelative) {
    $metadataIssues += "manifest.output_root does not match the package parent."
  }
}

if ($release) {
  $releaseOutputRoot = Get-OptionalPropertyValue -Value $release -Name "output_root"
  if ($packageParentRelative -and $releaseOutputRoot -ne $packageParentRelative) {
    $metadataIssues += "release.output_root does not match the package parent."
  }
}

if ($release) {
  $verifyScript = Get-OptionalPropertyValue -Value $release -Name "verify_script"
  if ($verifyScript -ne $ExpectedVerifyScript) {
    $metadataIssues += "release.verify_script does not match the expected verifier."
  }
}

if ($manifest) {
  $manifestItemCount = Get-OptionalPropertyValue -Value $manifest -Name "item_count"
  $manifestItems = Get-OptionalPropertyValue -Value $manifest -Name "items"
  if ($manifestItemCount -ne @($manifestItems).Count) {
    $metadataIssues += "manifest.item_count does not match manifest.items."
  }
}

if ($release -and $manifest) {
  $releaseItemCount = Get-OptionalPropertyValue -Value $release -Name "item_count"
  $manifestItemCount = Get-OptionalPropertyValue -Value $manifest -Name "item_count"
  if ($releaseItemCount -ne $manifestItemCount) {
    $metadataIssues += "release.item_count does not match manifest.item_count."
  }
}

foreach ($pathField in @(
    [pscustomobject]@{ label = "manifest.package_path"; value = if ($manifest) { Get-OptionalPropertyValue -Value $manifest -Name "package_path" } else { $null } },
    [pscustomobject]@{ label = "manifest.output_root"; value = if ($manifest) { Get-OptionalPropertyValue -Value $manifest -Name "output_root" } else { $null } },
    [pscustomobject]@{ label = "manifest.source_root"; value = if ($manifest) { Get-OptionalPropertyValue -Value $manifest -Name "source_root" } else { $null } },
    [pscustomobject]@{ label = "release.package_path"; value = if ($release) { Get-OptionalPropertyValue -Value $release -Name "package_path" } else { $null } },
    [pscustomobject]@{ label = "release.output_root"; value = if ($release) { Get-OptionalPropertyValue -Value $release -Name "output_root" } else { $null } },
    [pscustomobject]@{ label = "state.package_path"; value = if ($state) { Get-OptionalPropertyValue -Value $state -Name "package_path" } else { $null } },
    [pscustomobject]@{ label = "state.output_root"; value = if ($state) { Get-OptionalPropertyValue -Value $state -Name "output_root" } else { $null } },
    [pscustomobject]@{ label = "state.source_root"; value = if ($state) { Get-OptionalPropertyValue -Value $state -Name "source_root" } else { $null } }
  )) {
  if (Test-AbsoluteLikePathString -Value $pathField.value) {
    $metadataIssues += "$($pathField.label) must remain repo-relative."
  }
}

[pscustomobject]@{
  package_path = $resolvedPath
  release_target = $ExpectedReleaseTarget
  missing = $missing
  forbidden_present = $presentForbidden
  metadata_issues = $metadataIssues
  ok = ($missing.Count -eq 0) -and ($presentForbidden.Count -eq 0) -and ($metadataIssues.Count -eq 0)
} | ConvertTo-Json -Depth 8
