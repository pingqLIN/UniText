$ErrorActionPreference = "Stop"
$skillsRoot = "registry\\skills"
$required = @(
  ".mcp.json",
  ".claude\\settings.json",
  "README.md",
  "INDEX.md",
  "VISION.md",
  "RESOURCE_SPEC.md",
  "OPERATIONS.md",
  "PROJECT_MODES.md",
  "DOCUMENT_PLACEMENT_POLICY.md",
  "SECRET_HANDLING_GUIDELINES.md",
  "MILESTONES.md",
  "BOUNDARY_INCIDENT_REVIEW_TEMPLATE.md",
  "EXTERNAL_REVIEW_PACKAGE.md",
  "EXTERNAL_REVIEW_COVER_NOTE.md",
  "EXTERNAL_REVIEW_HIGHLIGHTS.md",
  "TEMPLATE_RELEASE_PACKAGE.md",
  "TEMPLATE_RELEASE_CHECKLIST.md",
  "local\\scripts\\sync-skills.ps1",
  "local\\scripts\\bootstrap.py",
  "local\\scripts\\verify-bootstrap.py",
  "local\\scripts\\create-git-bundle.py",
  "local\\scripts\\scan-skills.ps1",
  "local\\scripts\\verify-delivery.ps1",
  "local\\scripts\\batch-adopt-skills.ps1",
  "local\\scripts\\generate-index-entries.ps1",
  "local\\scripts\\rollback-skills.ps1",
  "local\\scripts\\export-review-package.ps1",
  "local\\scripts\\export-template-package.ps1",
  "local\\scripts\\verify-template-package.ps1",
  "local\\scripts\\verify-workspace-boundaries.ps1",
  "local\\scripts\\get-publishability-report.ps1",
  "local\\docs\\ADOPTION_CHECKLIST.md",
  "local\\docs\\CLI_COMPAT_MATRIX.md",
  "registry\\agents\\registry-curator\\AGENT.md",
  "registry\\mcp\\claude-project-mcp-seed\\definition.json",
  "registry\\mcp\\claude-project-mcp-seed\\server.py",
  "registry\\workflow\\claude-plans\\WORKFLOW.md",
  "template\\examples\\skills\\example-skill\\SKILL.md",
  "template\\examples\\agents\\example-agent\\AGENT.md",
  "template\\examples\\mcp\\example-mcp\\definition.json",
  "template\\examples\\workflow\\example-workflow\\WORKFLOW.md",
  "template\\examples\\local\\README.md",
  "template\\examples\\local\\docs\\PATH_MAP.template.md",
  "template\\examples\\local\\scripts\\sync-skills.template.ps1"
)

$missing = $required | Where-Object { -not (Test-Path $_) }
$skills = if (Test-Path $skillsRoot) { Get-ChildItem $skillsRoot -Directory } else { @() }
$invalid = @()

foreach ($skill in $skills) {
  $path = Join-Path $skill.FullName "SKILL.md"
  if (-not (Test-Path $path)) {
    $invalid += $skill.Name
    continue
  }

  $body = Get-Content $path -Raw
  if (-not $body.StartsWith("---")) {
    $invalid += $skill.Name
  }
}

[pscustomobject]@{
  missing_files = $missing
  adopted_skills = $skills.Count
  invalid_skills = $invalid
  agent_seed = Test-Path "registry\\agents\\registry-curator\\AGENT.md"
  mcp_seed = Test-Path "registry\\mcp\\claude-project-mcp-seed\\definition.json"
  workflow_seed = Test-Path "registry\\workflow\\claude-plans\\WORKFLOW.md"
  ok = ($missing.Count -eq 0) -and ($invalid.Count -eq 0) -and ($skills.Count -ge 1)
}
