param(
  [string]$Path
)

$ErrorActionPreference = "Stop"
$libPath = Join-Path $PSScriptRoot "lib\\workspace-sensitive-metadata.ps1"
. $libPath

if (-not $Path) {
  throw "Path is required."
}

$resolvedPath = (Resolve-Path -LiteralPath $Path).Path
$rules = Get-WorkspaceSensitiveMetadataRules -RootPath $resolvedPath
$rulesCheck = Test-WorkspaceSensitiveMetadataRules -Rules $rules

$required = @(
  ".gitattributes",
  ".gitignore",
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
  "BOUNDARY_INCIDENT_REVIEW_TEMPLATE.md",
  "MILESTONES.md",
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
  "local\\scripts\\preview-renormalize.py",
  "local\\scripts\\preview-renormalize.ps1",
  "local\\scripts\\run-renormalize.ps1",
  "local\\scripts\\run-renormalize.py",
  "local\\scripts\\sync-skills.ps1",
  "local\\scripts\\lib\\renormalize_core.py",
  "local\\scripts\\validate-workspace-sensitive-metadata-rules.ps1",
  "local\\scripts\\lib\\workspace-sensitive-metadata.ps1",
  "local\\scripts\\verify-workspace-boundaries.ps1",
  "local\\scripts\\get-publishability-report.ps1"
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

$contentPatterns = @(
  @($rules.content_patterns | Where-Object {
    $_.label -in @(
      "machine-specific Windows path",
      "live workspace hostname",
      "live connector redirect URI"
    )
  })
)

$contentFiles = Get-ChildItem -LiteralPath $resolvedPath -Recurse -File | Where-Object {
  $_.Extension -in @(".md", ".json", ".jsonc", ".txt", ".ps1", ".py", ".toml", ".yml", ".yaml")
}

$missing = $required | Where-Object {
  -not (Test-Path (Join-Path $resolvedPath $_))
}

$presentForbidden = $forbidden | Where-Object {
  Test-Path (Join-Path $resolvedPath $_)
}

$relativeContentFiles = @($contentFiles | ForEach-Object {
  $_.FullName.Substring($resolvedPath.Length).TrimStart('\', '/')
})
$rawViolations = @(Find-WorkspaceSensitiveContentViolations -RootPath $resolvedPath -Files $relativeContentFiles -ContentPatterns $contentPatterns)
$contentViolations = @($rawViolations | ForEach-Object {
  [pscustomobject]@{
    path = $_.path
    label = $_.label
    line = $_.line
    text = $_.text
  }
})

[pscustomobject]@{
  package_path = $resolvedPath
  rules_ok = [bool]$rulesCheck.ok
  rules_errors = @($rulesCheck.errors)
  missing = $missing
  forbidden_present = $presentForbidden
  content_violations = @($contentViolations)
  ok = [bool]$rulesCheck.ok -and ($missing.Count -eq 0) -and ($presentForbidden.Count -eq 0) -and (@($contentViolations).Count -eq 0)
}
