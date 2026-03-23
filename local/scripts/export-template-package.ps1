param(
  [string]$OutputRoot = "ops/template-package",
  [string]$Name = "",
  [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$root = (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$folder = if ($Name) { $Name } else { "template_$stamp" }
$package = Join-Path (Join-Path $root $OutputRoot) $folder
$items = @(
  [pscustomobject]@{ kind = "file"; source = ".gitignore"; target = ".gitignore" },
  [pscustomobject]@{ kind = "file"; source = "README.md"; target = "README.md" },
  [pscustomobject]@{ kind = "file"; source = "INDEX.md"; target = "INDEX.md" },
  [pscustomobject]@{ kind = "file"; source = "VISION.md"; target = "VISION.md" },
  [pscustomobject]@{ kind = "file"; source = "RESOURCE_SPEC.md"; target = "RESOURCE_SPEC.md" },
  [pscustomobject]@{ kind = "file"; source = "OPERATIONS.md"; target = "OPERATIONS.md" },
  [pscustomobject]@{ kind = "file"; source = "PROJECT_MODES.md"; target = "PROJECT_MODES.md" },
  [pscustomobject]@{ kind = "file"; source = "MILESTONES.md"; target = "MILESTONES.md" },
  [pscustomobject]@{ kind = "file"; source = "TEMPLATE_RELEASE_PACKAGE.md"; target = "TEMPLATE_RELEASE_PACKAGE.md" },
  [pscustomobject]@{ kind = "file"; source = "TEMPLATE_RELEASE_CHECKLIST.md"; target = "TEMPLATE_RELEASE_CHECKLIST.md" },
  [pscustomobject]@{ kind = "dir"; source = "template\\examples\\skills\\example-skill"; target = "registry\\skills\\example-skill" },
  [pscustomobject]@{ kind = "dir"; source = "template\\examples\\agents\\example-agent"; target = "registry\\agents\\example-agent" },
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
      "review-only docs"
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
  item_count = $items.Count
  excluded = @(
    "backup/",
    "recovered_*/",
    ".bak_*/",
    "ops/history/",
    "ops/review-package/",
    "local/docs/authoring/",
    "review-only docs"
  )
  items = $items
}

$manifest | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $package "manifest.json")

[pscustomobject]@{
  package_path = $package
  item_count = $items.Count
  manifest = "manifest.json"
}
