param(
  [string]$Path
)

$ErrorActionPreference = "Stop"

if (-not $Path) {
  throw "Path is required."
}

$required = @(
  ".github\\workflows\\ci.yml",
  ".gitignore",
  ".mcp.json",
  "LICENSE",
  "THIRD_PARTY_LICENSES.md",
  "requirements.txt",
  "requirements-tooling.txt",
  "requirements-skill-local.txt",
  "requirements-dev.txt",
  ".claude\\settings.json",
  "README.md",
  "INDEX.md",
  "VISION.md",
  "RESOURCE_SPEC.md",
  "OPERATIONS.md",
  "PROJECT_MODES.md",
  "SECRET_HANDLING_GUIDELINES.md",
  "WORKSPACE_BOUNDARY.md",
  "MILESTONES.md",
  "SKILLS_PUBLIC_RELEASE_POLICY.md",
  "TEMPLATE_RELEASE_PACKAGE.md",
  "TEMPLATE_RELEASE_CHECKLIST.md",
  "manifest.json",
  "release.json",
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
  "local\\scripts\\sync-skills.ps1",
  "local\\scripts\\verify-workspace-hygiene.ps1"
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

$missing = New-Object System.Collections.Generic.List[string]
foreach ($item in $required) {
  if (-not (Test-Path (Join-Path $Path $item))) {
    [void]$missing.Add($item)
  }
}

$presentForbidden = New-Object System.Collections.Generic.List[string]
foreach ($item in $forbidden) {
  if (Test-Path (Join-Path $Path $item)) {
    [void]$presentForbidden.Add($item)
  }
}

[pscustomobject]@{
  package_path = $Path
  missing = $missing
  forbidden_present = $presentForbidden
  ok = ($missing.Count -eq 0) -and ($presentForbidden.Count -eq 0)
}
