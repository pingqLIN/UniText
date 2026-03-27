$ErrorActionPreference = "Stop"
$skillsRoot = "registry\\skills"
$required = @(
  ".github\\workflows\\ci.yml",
  ".mcp.json",
  ".claude\\settings.json",
  "README.md",
  "INDEX.md",
  "requirements.txt",
  "requirements-tooling.txt",
  "requirements-skill-local.txt",
  "requirements-dev.txt",
  "VISION.md",
  "LICENSE",
  "THIRD_PARTY_LICENSES.md",
  "docs\\reviews\\README.md",
  "docs\\reviews\\SECURITY_REVIEW_ADVISORY.md",
  "docs\\reviews\\SECURITY_ATTACK_INPUT_RESPONSE_REPORT.md",
  "docs\\reviews\\DEVILS_ADVOCATE_REVIEW_COMBINED_REVIEW_2026-03-27.md",
  "docs\\reviews\\DEVILS_ADVOCATE_REVIEW_CLOSURE_NOTE_2026-03-27.md",
  "docs\\reviews\\DEVILS_ADVOCATE_REVIEW_2026-03-27.md",
  "docs\\reviews\\REVIEW_FINDINGS_REMEDIATION_PLAN_2026-03-27.md",
  "docs\\reviews\\SECOND_ROUND_REMEDIATION_ADDENDUM_2026-03-27.md",
  "docs\\reviews\\ACT_06_REGRESSION_DISPOSITION_2026-03-27.md",
  "docs\\reviews\\ACT_11_I18N_SPOT_CHECK_2026-03-27.md",
  "docs\\reviews\\ACT_12_DOCS_SCALE_BASELINE_2026-03-27.md",
  "docs\\reviews\\ACT_13_SKILLS_PROVENANCE_AUDIT_2026-03-27.md",
  "docs\\reviews\\ACT_14_HOSTED_CI_EVIDENCE_2026-03-27.md",
  "RESOURCE_SPEC.md",
  "OPERATIONS.md",
  "PROJECT_MODES.md",
  "SECRET_HANDLING_GUIDELINES.md",
  "WORKSPACE_BOUNDARY.md",
  "MILESTONES.md",
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
  "local\\scripts\\verify-workspace-hygiene.ps1",
  "local\\scripts\\batch-adopt-skills.ps1",
  "local\\scripts\\generate-index-entries.ps1",
  "local\\scripts\\rollback-skills.ps1",
  "local\\scripts\\export-review-package.ps1",
  "local\\scripts\\export-template-package.ps1",
  "local\\scripts\\verify-template-package.ps1",
  "local\\docs\\ADOPTION_CHECKLIST.md",
  "local\\docs\\CLI_COMPAT_MATRIX.md",
  "local\\docs\\SUPPORT_PROOF_MATRIX.md",
  "local\\docs\\DOCS_GOVERNANCE_RULES.md",
  "local\\docs\\INDEPENDENT_VALIDATION_RUNBOOK.md",
  "local\\docs\\INDEPENDENT_VALIDATION_REPORT_TEMPLATE.md",
  "registry\\skills\\SOURCE_SCHEMA.md",
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
