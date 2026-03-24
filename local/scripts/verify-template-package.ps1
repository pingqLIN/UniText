param(
  [string]$Path
)

$ErrorActionPreference = "Stop"

if (-not $Path) {
  throw "Path is required."
}

$required = @(
  ".gitignore",
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
  "registry\\skills\\example-skill\\SKILL.md",
  "registry\\agents\\example-agent\\AGENT.md",
  "registry\\mcp\\example-mcp\\definition.json",
  "registry\\workflow\\example-workflow\\WORKFLOW.md",
  "local\\README.md",
  "local\\docs\\PATH_MAP.md",
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

$missing = $required | Where-Object {
  -not (Test-Path (Join-Path $Path $_))
}

$presentForbidden = $forbidden | Where-Object {
  Test-Path (Join-Path $Path $_)
}

[pscustomobject]@{
  package_path = $Path
  missing = $missing
  forbidden_present = $presentForbidden
  ok = ($missing.Count -eq 0) -and ($presentForbidden.Count -eq 0)
}
