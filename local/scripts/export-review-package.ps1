param(
  [string]$OutputRoot = "ops/review-package",
  [string]$Name = "",
  [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$root = (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path
. (Join-Path $PSScriptRoot "lib\path-safety.ps1")
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$folder = if ($Name) {
  Assert-SafeSimpleName -Value $Name -Label "Name" -Pattern '^[a-z0-9][a-z0-9_-]{0,127}$'
} else {
  "review_$stamp"
}
$allowedOutputBase = Get-NormalizedFullPath -BasePath $root -CandidatePath "ops/review-package"
$outputBase = Get-NormalizedFullPath -BasePath $root -CandidatePath $OutputRoot
if (-not (Test-IsUnderPath -RootPath $allowedOutputBase -CandidatePath $outputBase)) {
  throw "OutputRoot must remain under ops/review-package: $outputBase"
}
$package = Join-Path $outputBase $folder
$publicSkillsCore = @(
  "mcp-builder",
  "skill-creator",
  "webapp-testing"
)
$publicSkillsExpansion = @(
  "frontend-design",
  "web-artifacts-builder",
  "internal-comms",
  "theme-factory"
)
$restrictedSkillsHoldback = @(
  "pdf",
  "docx",
  "xlsx",
  "pptx",
  "doc-coauthoring"
)
$publicSkillExamples = @(
  "template\\examples\\skills\\example-skill"
)
$items = @(
  [pscustomobject]@{ kind = "file"; path = ".github\\workflows\\ci.yml" },
  [pscustomobject]@{ kind = "file"; path = "EXTERNAL_REVIEW_COVER_NOTE.md" },
  [pscustomobject]@{ kind = "file"; path = "EXTERNAL_REVIEW_HIGHLIGHTS.md" },
  [pscustomobject]@{ kind = "file"; path = "LICENSE" },
  [pscustomobject]@{ kind = "file"; path = "THIRD_PARTY_LICENSES.md" },
  [pscustomobject]@{ kind = "file"; path = "docs\\reviews\\README.md" },
  [pscustomobject]@{ kind = "file"; path = "docs\\reviews\\DEVILS_ADVOCATE_REVIEW_2026-03-26.md" },
  [pscustomobject]@{ kind = "file"; path = "docs\\reviews\\DEVILS_ADVOCATE_REVIEW_RESPONSE_2026-03-26.md" },
  [pscustomobject]@{ kind = "file"; path = "docs\\reviews\\DEVILS_ADVOCATE_REVIEW_COMBINED_REVIEW_2026-03-27.md" },
  [pscustomobject]@{ kind = "file"; path = "docs\\reviews\\DEVILS_ADVOCATE_REVIEW_CLOSURE_NOTE_2026-03-27.md" },
  [pscustomobject]@{ kind = "file"; path = "docs\\reviews\\DEVILS_ADVOCATE_REVIEW_2026-03-27.md" },
  [pscustomobject]@{ kind = "file"; path = "docs\\reviews\\REVIEW_FINDINGS_REMEDIATION_PLAN_2026-03-27.md" },
  [pscustomobject]@{ kind = "file"; path = "docs\\reviews\\SECOND_ROUND_REMEDIATION_ADDENDUM_2026-03-27.md" },
  [pscustomobject]@{ kind = "file"; path = "docs\\reviews\\PRE_PUSH_AUDIT_2026-03-26.md" },
  [pscustomobject]@{ kind = "file"; path = "docs\\reviews\\SECURITY_ATTACK_INPUT_CHECKLIST.md" },
  [pscustomobject]@{ kind = "file"; path = "docs\\reviews\\SECURITY_REVIEW_ADVISORY.md" },
  [pscustomobject]@{ kind = "file"; path = "docs\\reviews\\SECURITY_ATTACK_INPUT_RESPONSE_REPORT.md" },
  [pscustomobject]@{ kind = "file"; path = "docs\\reviews\\ACT_06_REGRESSION_DISPOSITION_2026-03-27.md" },
  [pscustomobject]@{ kind = "file"; path = "docs\\reviews\\ACT_11_I18N_SPOT_CHECK_2026-03-27.md" },
  [pscustomobject]@{ kind = "file"; path = "docs\\reviews\\ACT_12_DOCS_SCALE_BASELINE_2026-03-27.md" },
  [pscustomobject]@{ kind = "file"; path = "docs\\reviews\\ACT_13_SKILLS_PROVENANCE_AUDIT_2026-03-27.md" },
  [pscustomobject]@{ kind = "file"; path = "docs\\reviews\\ACT_14_HOSTED_CI_EVIDENCE_2026-03-27.md" },
  [pscustomobject]@{ kind = "file"; path = "requirements.txt" },
  [pscustomobject]@{ kind = "file"; path = "requirements-tooling.txt" },
  [pscustomobject]@{ kind = "file"; path = "requirements-skill-local.txt" },
  [pscustomobject]@{ kind = "file"; path = "requirements-dev.txt" },
  [pscustomobject]@{ kind = "file"; path = "README.md" },
  [pscustomobject]@{ kind = "file"; path = "INDEX.md" },
  [pscustomobject]@{ kind = "file"; path = "VISION.md" },
  [pscustomobject]@{ kind = "file"; path = "RESOURCE_SPEC.md" },
  [pscustomobject]@{ kind = "file"; path = "OPERATIONS.md" },
  [pscustomobject]@{ kind = "file"; path = "SECRET_HANDLING_GUIDELINES.md" },
  [pscustomobject]@{ kind = "file"; path = "SKILLS_PUBLIC_RELEASE_POLICY.md" },
  [pscustomobject]@{ kind = "file"; path = "WORKSPACE_BOUNDARY.md" },
  [pscustomobject]@{ kind = "file"; path = "PROJECT_MODES.md" },
  [pscustomobject]@{ kind = "file"; path = "MILESTONES.md" },
  [pscustomobject]@{ kind = "file"; path = "PROJECT_STATUS_REPORT_2026-03-23.md" },
  [pscustomobject]@{ kind = "file"; path = "ESSENTIAL_SKILLS_SHORTLIST.md" },
  [pscustomobject]@{ kind = "file"; path = "EXTERNAL_REVIEW_PACKAGE.md" },
  [pscustomobject]@{ kind = "file"; path = "registry\\skills\\SOURCES.md" },
  [pscustomobject]@{ kind = "file"; path = "local\\docs\\ADOPTION_CHECKLIST.md" },
  [pscustomobject]@{ kind = "file"; path = "local\\docs\\CLI_COMPAT_MATRIX.md" },
  [pscustomobject]@{ kind = "file"; path = "local\\docs\\SUPPORT_PROOF_MATRIX.md" },
  [pscustomobject]@{ kind = "file"; path = "local\\docs\\DOCS_GOVERNANCE_RULES.md" },
  [pscustomobject]@{ kind = "file"; path = "local\\docs\\INDEPENDENT_VALIDATION_RUNBOOK.md" },
  [pscustomobject]@{ kind = "file"; path = "local\\docs\\INDEPENDENT_VALIDATION_REPORT_TEMPLATE.md" },
  [pscustomobject]@{ kind = "file"; path = "registry\\skills\\SOURCE_SCHEMA.md" },
  [pscustomobject]@{ kind = "file"; path = "local\\scripts\\README.md" },
  [pscustomobject]@{ kind = "file"; path = "local\\scripts\\bootstrap.py" },
  [pscustomobject]@{ kind = "file"; path = "local\\scripts\\verify-bootstrap.py" },
  [pscustomobject]@{ kind = "file"; path = "local\\scripts\\create-git-bundle.py" },
  [pscustomobject]@{ kind = "file"; path = "local\\scripts\\scan-skills.ps1" },
  [pscustomobject]@{ kind = "file"; path = "local\\scripts\\sync-skills.ps1" },
  [pscustomobject]@{ kind = "file"; path = "local\\scripts\\verify-delivery.ps1" },
  [pscustomobject]@{ kind = "file"; path = "local\\scripts\\verify-workspace-hygiene.ps1" },
  [pscustomobject]@{ kind = "file"; path = "local\\scripts\\health-check.ps1" },
  [pscustomobject]@{ kind = "file"; path = "local\\scripts\\batch-adopt-skills.ps1" },
  [pscustomobject]@{ kind = "file"; path = "local\\scripts\\generate-index-entries.ps1" },
  [pscustomobject]@{ kind = "file"; path = "local\\scripts\\rollback-skills.ps1" },
  [pscustomobject]@{ kind = "file"; path = "local\\scripts\\export-review-package.ps1" },
  [pscustomobject]@{ kind = "file"; path = "local\\scripts\\lib\\path-safety.ps1" },
  [pscustomobject]@{ kind = "dir"; path = "template\\examples\\skills\\example-skill"; target = "registry\\skills\\example-skill" },
  [pscustomobject]@{ kind = "dir"; path = "registry\\agents\\registry-curator" },
  [pscustomobject]@{ kind = "dir"; path = "registry\\mcp\\claude-project-mcp-seed" },
  [pscustomobject]@{ kind = "dir"; path = "registry\\workflow\\claude-plans" }
)

$items += $publicSkillsCore | ForEach-Object {
  [pscustomobject]@{
    kind = "dir"
    path = "registry\\skills\\$_"
  }
}

$items += $publicSkillsExpansion | ForEach-Object {
  [pscustomobject]@{
    kind = "dir"
    path = "registry\\skills\\$_"
  }
}

$missing = @($items | Where-Object {
  -not (Test-Path (Join-Path $root $_.path))
})

if ($missing.Count -gt 0) {
  throw "Missing review package sources: $($missing.path -join ', ')"
}

if ($DryRun) {
  [pscustomobject]@{
    package_path = $package
    output_root = $outputBase
    item_count = $items.Count
    public_skill_examples = $publicSkillExamples
    public_skill_source_model = "github-backed"
    public_skills_core = $publicSkillsCore
    public_skills_expansion = $publicSkillsExpansion
    restricted_skills_holdback = $restrictedSkillsHoldback
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
  $targetPath = if ($item.PSObject.Properties.Name -contains "target") { $item.target } else { $item.path }
  $target = Join-Path $package $targetPath
  $parent = Split-Path $target -Parent

  if (-not (Test-Path $parent)) {
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
  }

  if ($item.kind -eq "file") {
    Copy-Item -LiteralPath $source -Destination $target -Force
    continue
  }

  if ($item.PSObject.Properties.Name -contains "target") {
    Copy-Item -LiteralPath $source -Destination $target -Recurse -Force
    continue
  }

  Copy-Item -LiteralPath $source -Destination $parent -Recurse -Force
}

$manifest = [ordered]@{
  generated_at = (Get-Date).ToString("s")
  source_root = "."
  package_path = $package
  phase_target = "external-review-ready"
  item_count = $items.Count
  excluded = @(
    "backup/",
    "recovered_*/",
    ".bak_*/",
    "ops/history/",
    "local/docs/authoring/",
    "untracked experiments",
    "local-only validation skills",
    "restricted-license skills"
  )
  public_skill_examples = $publicSkillExamples
  public_skill_source_model = "github-backed"
  public_skills_core = $publicSkillsCore
  public_skills_expansion = $publicSkillsExpansion
  restricted_skills_holdback = $restrictedSkillsHoldback
  items = $items
}

$manifest | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $package "manifest.json")

[pscustomobject]@{
  package_path = $package
  item_count = $items.Count
  manifest = "manifest.json"
}
