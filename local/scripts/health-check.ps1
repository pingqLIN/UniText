$ErrorActionPreference = "Stop"
$skillsRoot = "registry\\skills"
$required = @(
  "README.md",
  "INDEX.md",
  "VISION.md",
  "RESOURCE_SPEC.md",
  "OPERATIONS.md",
  "PROJECT_MODES.md",
  "MILESTONES.md",
  "EXTERNAL_REVIEW_PACKAGE.md",
  "EXTERNAL_REVIEW_COVER_NOTE.md",
  "EXTERNAL_REVIEW_HIGHLIGHTS.md",
  "local\\scripts\\sync-skills.ps1",
  "local\\scripts\\scan-skills.ps1",
  "local\\scripts\\verify-delivery.ps1",
  "local\\scripts\\batch-adopt-skills.ps1",
  "local\\scripts\\generate-index-entries.ps1",
  "local\\scripts\\rollback-skills.ps1",
  "local\\scripts\\export-review-package.ps1",
  "local\\docs\\ADOPTION_CHECKLIST.md",
  "local\\docs\\ENVIRONMENT.md",
  "local\\docs\\authoring\\README.md",
  "registry\\agents\\registry-curator\\AGENT.md",
  "registry\\mcp\\claude-project-mcp-seed\\definition.json",
  "registry\\workflow\\claude-plans\\WORKFLOW.md"
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
