param(
  [string]$OutputRoot = "ops/review-package",
  [string]$Name = "",
  [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$root = (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$folder = if ($Name) { $Name } else { "review_$stamp" }
$package = Join-Path (Join-Path $root $OutputRoot) $folder
$coreSkills = @(
  "pdf",
  "docx",
  "xlsx",
  "pptx",
  "mcp-builder",
  "skill-creator",
  "webapp-testing",
  "doc-coauthoring"
)
$expansionSkills = @(
  "frontend-design",
  "web-artifacts-builder",
  "internal-comms",
  "theme-factory"
)
$items = @(
  [pscustomobject]@{ kind = "file"; path = "EXTERNAL_REVIEW_COVER_NOTE.md" },
  [pscustomobject]@{ kind = "file"; path = "EXTERNAL_REVIEW_HIGHLIGHTS.md" },
  [pscustomobject]@{ kind = "file"; path = "README.md" },
  [pscustomobject]@{ kind = "file"; path = "INDEX.md" },
  [pscustomobject]@{ kind = "file"; path = "VISION.md" },
  [pscustomobject]@{ kind = "file"; path = "RESOURCE_SPEC.md" },
  [pscustomobject]@{ kind = "file"; path = "OPERATIONS.md" },
  [pscustomobject]@{ kind = "file"; path = "SECRET_HANDLING_GUIDELINES.md" },
  [pscustomobject]@{ kind = "file"; path = "PROJECT_MODES.md" },
  [pscustomobject]@{ kind = "file"; path = "MILESTONES.md" },
  [pscustomobject]@{ kind = "file"; path = "PROJECT_STATUS_REPORT_2026-03-23.md" },
  [pscustomobject]@{ kind = "file"; path = "ESSENTIAL_SKILLS_SHORTLIST.md" },
  [pscustomobject]@{ kind = "file"; path = "EXTERNAL_REVIEW_PACKAGE.md" },
  [pscustomobject]@{ kind = "file"; path = "local\\docs\\ADOPTION_CHECKLIST.md" },
  [pscustomobject]@{ kind = "file"; path = "local\\docs\\CLI_COMPAT_MATRIX.md" },
  [pscustomobject]@{ kind = "file"; path = "local\\scripts\\README.md" },
  [pscustomobject]@{ kind = "file"; path = "local\\scripts\\bootstrap.py" },
  [pscustomobject]@{ kind = "file"; path = "local\\scripts\\verify-bootstrap.py" },
  [pscustomobject]@{ kind = "file"; path = "local\\scripts\\create-git-bundle.py" },
  [pscustomobject]@{ kind = "file"; path = "local\\scripts\\scan-skills.ps1" },
  [pscustomobject]@{ kind = "file"; path = "local\\scripts\\sync-skills.ps1" },
  [pscustomobject]@{ kind = "file"; path = "local\\scripts\\verify-delivery.ps1" },
  [pscustomobject]@{ kind = "file"; path = "local\\scripts\\health-check.ps1" },
  [pscustomobject]@{ kind = "file"; path = "local\\scripts\\batch-adopt-skills.ps1" },
  [pscustomobject]@{ kind = "file"; path = "local\\scripts\\generate-index-entries.ps1" },
  [pscustomobject]@{ kind = "file"; path = "local\\scripts\\rollback-skills.ps1" },
  [pscustomobject]@{ kind = "file"; path = "local\\scripts\\export-review-package.ps1" },
  [pscustomobject]@{ kind = "dir"; path = "registry\\agents\\registry-curator" },
  [pscustomobject]@{ kind = "dir"; path = "registry\\mcp\\claude-project-mcp-seed" },
  [pscustomobject]@{ kind = "dir"; path = "registry\\workflow\\claude-plans" }
)

$items += $coreSkills | ForEach-Object {
  [pscustomobject]@{
    kind = "dir"
    path = "registry\\skills\\$_"
  }
}

$items += $expansionSkills | ForEach-Object {
  [pscustomobject]@{
    kind = "dir"
    path = "registry\\skills\\$_"
  }
}

$missing = $items | Where-Object {
  -not (Test-Path (Join-Path $root $_.path))
}

if ($missing.Count -gt 0) {
  throw "Missing review package sources: $($missing.path -join ', ')"
}

if ($DryRun) {
  [pscustomobject]@{
    package_path = $package
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
  source_root = $root
  package_path = $package
  phase_target = "external-review-ready"
  item_count = $items.Count
  excluded = @(
    "backup/",
    "recovered_*/",
    ".bak_*/",
    "ops/history/",
    "local/docs/authoring/",
    "untracked experiments"
  )
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
