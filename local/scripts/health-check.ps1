$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path
$skillsRoot = "registry\\skills"
$required = @(
  ".gitattributes",
  ".github\\pull_request_template.md",
  ".mcp.json",
  ".claude\\settings.json",
  "README.md",
  "INDEX.md",
  "VISION.md",
  "RESOURCE_SPEC.md",
  "OPERATIONS.md",
  "PROJECT_MODES.md",
  "WORKSPACE_SENSITIVE_METADATA_RULES.json",
  "WORKSPACE_SENSITIVE_METADATA_RULES.md",
  "DOCUMENT_PLACEMENT_POLICY.md",
  "SECRET_HANDLING_GUIDELINES.md",
  "MILESTONES.md",
  "BOUNDARY_INCIDENT_REVIEW_TEMPLATE.md",
  "docs/reviews/EXTERNAL_REVIEW_PACKAGE.md",
  "docs/reviews/EXTERNAL_REVIEW_COVER_NOTE.md",
  "docs/reviews/EXTERNAL_REVIEW_HIGHLIGHTS.md",
  "TEMPLATE_RELEASE_PACKAGE.md",
  "TEMPLATE_RELEASE_CHECKLIST.md",
  "local\\scripts\\sync-skills.ps1",
  "local\\scripts\\bootstrap.py",
  "local\\scripts\\verify-bootstrap.py",
  "local\\scripts\\create-git-bundle.py",
  "local\\scripts\\preview-renormalize.py",
  "local\\scripts\\preview-renormalize.ps1",
  "local\\scripts\\run-renormalize.ps1",
  "local\\scripts\\run-renormalize.py",
  "local\\scripts\\scan-skills.ps1",
  "local\\scripts\\verify-delivery.ps1",
  "local\\scripts\\batch-adopt-skills.ps1",
  "local\\scripts\\generate-index-entries.ps1",
  "local\\scripts\\rollback-skills.ps1",
  "local\\scripts\\export-review-package.ps1",
  "local\\scripts\\export-template-package.ps1",
  "local\\scripts\\lib\\renormalize_core.py",
  "local\\scripts\\validate-workspace-sensitive-metadata-rules.ps1",
  "local\\scripts\\lib\\workspace-sensitive-metadata.ps1",
  "local\\scripts\\verify-template-package.ps1",
  "local\\scripts\\verify-workspace-boundaries.ps1",
  "local\\scripts\\get-publishability-report.ps1",
  "local\\scripts\\get-document-placement-recommendation.ps1",
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

$missing = $required | Where-Object { -not (Test-Path (Join-Path $root $_)) }
$trackedSkillFiles = @((& git -C $root ls-files "$skillsRoot/*/SKILL.md") | Where-Object { $_ })
$skills = @($trackedSkillFiles | ForEach-Object { Split-Path $_ -Parent } | Sort-Object -Unique)
$invalid = @()
$rulesScript = Join-Path $root "local\\scripts\\validate-workspace-sensitive-metadata-rules.ps1"
$i18nAuditScript = Join-Path $root "local\\scripts\\audit-i18n-drift.py"

foreach ($skill in $skills) {
  $path = Join-Path $root (Join-Path $skill "SKILL.md")
  if (-not (Test-Path $path)) {
    $invalid += (Split-Path $skill -Leaf)
    continue
  }

  $body = Get-Content $path -Raw
  if (-not $body.StartsWith("---")) {
    $invalid += (Split-Path $skill -Leaf)
  }
}

$rulesCheck = & $rulesScript
$rulesOk = [bool]$rulesCheck.ok
$i18nSummary = $null
$i18nError = $null

try {
  $i18nRaw = (& python $i18nAuditScript --format json --sample-size 0 --exit-zero | Out-String).Trim()
  if ($LASTEXITCODE -ne 0) {
    $i18nError = "audit-i18n-drift.py exited with code $LASTEXITCODE"
  } elseif ([string]::IsNullOrWhiteSpace($i18nRaw)) {
    $i18nError = "audit-i18n-drift.py returned empty output"
  } else {
    $i18nSummary = $i18nRaw | ConvertFrom-Json
  }
} catch {
  $i18nError = $_.Exception.Message
}

$i18nCollected = $null -ne $i18nSummary
$i18nMissing = $null
$i18nStale = $null
$i18nUntracked = $null
$i18nSourceMissing = $null

if ($i18nCollected) {
  $byLocale = @($i18nSummary.by_locale.PSObject.Properties.Value)
  $i18nMissing = ($byLocale | Measure-Object -Property missing -Sum).Sum
  $i18nStale = ($byLocale | Measure-Object -Property stale -Sum).Sum
  $i18nUntracked = ($byLocale | Measure-Object -Property untracked -Sum).Sum
  $i18nSourceMissing = ($byLocale | Measure-Object -Property source_missing -Sum).Sum
}

[pscustomobject]@{
  missing_files = $missing
  adopted_skills = $skills.Count
  invalid_skills = $invalid
  agent_seed = Test-Path "registry\\agents\\registry-curator\\AGENT.md"
  mcp_seed = Test-Path "registry\\mcp\\claude-project-mcp-seed\\definition.json"
  workflow_seed = Test-Path "registry\\workflow\\claude-plans\\WORKFLOW.md"
  boundary_rules_ok = $rulesOk
  boundary_rule_errors = @($rulesCheck.errors)
  i18n_drift_collected = $i18nCollected
  i18n_drift_ok = if ($i18nCollected) { [bool]$i18nSummary.ok } else { $null }
  i18n_issues_found = if ($i18nCollected) { [int]$i18nSummary.issues_found } else { $null }
  i18n_missing = $i18nMissing
  i18n_stale = $i18nStale
  i18n_untracked = $i18nUntracked
  i18n_source_missing = $i18nSourceMissing
  i18n_drift_error = $i18nError
  ok = ($missing.Count -eq 0) -and ($invalid.Count -eq 0) -and ($skills.Count -ge 1) -and $rulesOk
}
