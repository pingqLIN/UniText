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
try {
  $actualRelative = Convert-ToRepoRelativePath -RepoRoot $root -Path $resolvedPath
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

  if ($document.expectedType -and $document.value.document_type -ne $document.expectedType) {
    $metadataIssues += "$($document.label).document_type must be $($document.expectedType)."
  }
  if ($document.value.release_target -ne $ExpectedReleaseTarget) {
    $metadataIssues += "$($document.label).release_target must be $ExpectedReleaseTarget."
  }
  if ($document.value.generation_state -ne "complete") {
    $metadataIssues += "$($document.label).generation_state must be complete."
  }
  if ($actualRelative -and $document.value.package_path -ne $actualRelative) {
    $metadataIssues += "$($document.label).package_path does not match the actual package path."
  }
}

if ($manifest -and $manifest.output_root -ne (Convert-ToRepoRelativePath -RepoRoot $root -Path (Split-Path -Path $resolvedPath -Parent))) {
  $metadataIssues += "manifest.output_root does not match the package parent."
}

if ($release -and $release.output_root -ne (Convert-ToRepoRelativePath -RepoRoot $root -Path (Split-Path -Path $resolvedPath -Parent))) {
  $metadataIssues += "release.output_root does not match the package parent."
}

if ($release -and $release.verify_script -ne $ExpectedVerifyScript) {
  $metadataIssues += "release.verify_script does not match the expected verifier."
}

foreach ($pathField in @(
    [pscustomobject]@{ label = "manifest.package_path"; value = if ($manifest) { $manifest.package_path } else { $null } },
    [pscustomobject]@{ label = "manifest.output_root"; value = if ($manifest) { $manifest.output_root } else { $null } },
    [pscustomobject]@{ label = "manifest.source_root"; value = if ($manifest) { $manifest.source_root } else { $null } },
    [pscustomobject]@{ label = "release.package_path"; value = if ($release) { $release.package_path } else { $null } },
    [pscustomobject]@{ label = "release.output_root"; value = if ($release) { $release.output_root } else { $null } },
    [pscustomobject]@{ label = "state.package_path"; value = if ($state) { $state.package_path } else { $null } },
    [pscustomobject]@{ label = "state.output_root"; value = if ($state) { $state.output_root } else { $null } },
    [pscustomobject]@{ label = "state.source_root"; value = if ($state) { $state.source_root } else { $null } }
  )) {
  if (Test-AbsoluteLikePathString -Value $pathField.value) {
    $metadataIssues += "$($pathField.label) must remain repo-relative."
  }
}

if ($manifest -and $manifest.item_count -ne @($manifest.items).Count) {
  $metadataIssues += "manifest.item_count does not match manifest.items."
}

if ($release -and $manifest -and $release.item_count -ne $manifest.item_count) {
  $metadataIssues += "release.item_count does not match manifest.item_count."
}

[pscustomobject]@{
  package_path = $resolvedPath
  release_target = $ExpectedReleaseTarget
  missing = $missing
  forbidden_present = $presentForbidden
  metadata_issues = $metadataIssues
  ok = ($missing.Count -eq 0) -and ($presentForbidden.Count -eq 0) -and ($metadataIssues.Count -eq 0)
}
