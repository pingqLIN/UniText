param(
  [string]$OutputRoot = "ops/template-package",
  [string]$Name = "",
  [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$root = (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$folder = if ($Name) { $Name } else { "template_$stamp" }
$outputBase = if ([IO.Path]::IsPathRooted($OutputRoot)) { $OutputRoot } else { (Join-Path $root $OutputRoot) }
$package = Join-Path $outputBase $folder
$items = @(
  [pscustomobject]@{ kind = "file"; source = ".gitignore"; target = ".gitignore" },
  [pscustomobject]@{ kind = "file"; source = ".mcp.json"; target = ".mcp.json" },
  [pscustomobject]@{ kind = "file"; source = "README.md"; target = "README.md" },
  [pscustomobject]@{ kind = "file"; source = "INDEX.md"; target = "INDEX.md" },
  [pscustomobject]@{ kind = "file"; source = "VISION.md"; target = "VISION.md" },
  [pscustomobject]@{ kind = "file"; source = "RESOURCE_SPEC.md"; target = "RESOURCE_SPEC.md" },
  [pscustomobject]@{ kind = "file"; source = "OPERATIONS.md"; target = "OPERATIONS.md" },
  [pscustomobject]@{ kind = "file"; source = "PROJECT_MODES.md"; target = "PROJECT_MODES.md" },
  [pscustomobject]@{ kind = "file"; source = "SECRET_HANDLING_GUIDELINES.md"; target = "SECRET_HANDLING_GUIDELINES.md" },
  [pscustomobject]@{ kind = "file"; source = "MILESTONES.md"; target = "MILESTONES.md" },
  [pscustomobject]@{ kind = "file"; source = "TEMPLATE_RELEASE_PACKAGE.md"; target = "TEMPLATE_RELEASE_PACKAGE.md" },
  [pscustomobject]@{ kind = "file"; source = "TEMPLATE_RELEASE_CHECKLIST.md"; target = "TEMPLATE_RELEASE_CHECKLIST.md" },
  [pscustomobject]@{ kind = "file"; source = ".claude\\settings.json"; target = ".claude\\settings.json" },
  [pscustomobject]@{ kind = "file"; source = "template\\examples\\local\\README.md"; target = "local\\README.md" },
  [pscustomobject]@{ kind = "file"; source = "template\\examples\\local\\docs\\PATH_MAP.template.md"; target = "local\\docs\\PATH_MAP.md" },
  [pscustomobject]@{ kind = "file"; source = "local\\scripts\\bootstrap.py"; target = "local\\scripts\\bootstrap.py" },
  [pscustomobject]@{ kind = "file"; source = "local\\scripts\\verify-bootstrap.py"; target = "local\\scripts\\verify-bootstrap.py" },
  [pscustomobject]@{ kind = "file"; source = "local\\scripts\\create-git-bundle.py"; target = "local\\scripts\\create-git-bundle.py" },
  [pscustomobject]@{ kind = "file"; source = "local\\scripts\\sync-skills.ps1"; target = "local\\scripts\\sync-skills.ps1" },
  [pscustomobject]@{ kind = "dir"; source = "template\\examples\\skills\\example-skill"; target = "registry\\skills\\example-skill" },
  [pscustomobject]@{ kind = "dir"; source = "template\\examples\\agents\\example-agent"; target = "registry\\agents\\example-agent" },
  [pscustomobject]@{ kind = "dir"; source = "registry\\mcp\\claude-project-mcp-seed"; target = "registry\\mcp\\claude-project-mcp-seed" },
  [pscustomobject]@{ kind = "dir"; source = "template\\examples\\mcp\\example-mcp"; target = "registry\\mcp\\example-mcp" },
  [pscustomobject]@{ kind = "dir"; source = "template\\examples\\workflow\\example-workflow"; target = "registry\\workflow\\example-workflow" }
)

$missing = $items | Where-Object {
  -not (Test-Path (Join-Path $root $_.source))
}

if ($missing.Count -gt 0) {
  throw "Missing template package sources: $($missing.source -join ', ')"
}

if ($DryRun) {
  [pscustomobject]@{
    package_path = $package
    item_count = $items.Count
    items = $items
    excluded = @(
      "backup/",
      "recovered_*/",
      ".bak_*/",
      "ops/history/",
      "ops/review-package/",
      "local/docs/authoring/",
      "review-only docs",
      "machine-local runtime state"
    )
  }
  return
}

if (Test-Path $package) {
  throw "Target package path already exists: $package"
}

New-Item -ItemType Directory -Path $package -Force | Out-Null

foreach ($item in $items) {
  $source = Join-Path $root $item.source
  $target = Join-Path $package $item.target
  $parent = Split-Path $target -Parent

  if (-not (Test-Path $parent)) {
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
  }

  if ($item.kind -eq "file") {
    Copy-Item -LiteralPath $source -Destination $target -Force
    continue
  }

  Copy-Item -LiteralPath $source -Destination $target -Recurse -Force
}

$manifest = [ordered]@{
  generated_at = (Get-Date).ToString("s")
  source_root = $root
  package_path = $package
  phase_target = "template-release-cleanup"
  release_channel = "candidate"
  release_version = "$((Get-Date).ToString('yyyy.MM.dd'))-template-candidate"
  item_count = $items.Count
  excluded = @(
    "backup/",
    "recovered_*/",
    ".bak_*/",
    "ops/history/",
    "ops/review-package/",
    "local/docs/authoring/",
    "review-only docs",
    "machine-local runtime state"
  )
  items = $items
}

$manifest | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $package "manifest.json")
$manifest | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $package "release.json")

[pscustomobject]@{
  package_path = $package
  item_count = $items.Count
  manifest = "manifest.json"
}
