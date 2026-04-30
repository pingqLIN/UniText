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
  "local\\config\\integration-surfaces.json",
  "README.md",
  "README.zh-TW.md",
  "LICENSE",
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
  "local\\scripts\\build-runtime-layer.py",
  "local\\scripts\\create-git-bundle.py",
  "local\\scripts\\preview-renormalize.py",
  "local\\scripts\\preview-renormalize.ps1",
  "local\\scripts\\run-renormalize.ps1",
  "local\\scripts\\run-renormalize.py",
  "local\\scripts\\sync-skills.ps1",
  "local\\scripts\\lib\\integration_surfaces.py",
  "local\\scripts\\lib\\renormalize_core.py",
  "local\\scripts\\validate-workspace-sensitive-metadata-rules.ps1",
  "local\\scripts\\validate-workspace-sensitive-metadata-rules.py",
  "local\\scripts\\lib\\workspace-sensitive-metadata.ps1",
  "local\\scripts\\lib\\workspace_sensitive_metadata.py",
  "local\\scripts\\lib\\workspace_boundaries.py",
  "local\\scripts\\verify-workspace-boundaries.ps1",
  "local\\scripts\\verify-workspace-boundaries.py",
  "local\\scripts\\get-publishability-report.ps1",
  "local\\scripts\\get-publishability-report.py",
  "local\\scripts\\get-document-placement-recommendation.ps1",
  "local\\scripts\\build-project-map.py",
  "local\\scripts\\project-map-runtime.js",
  "local\\scripts\\project-map-template.html",
  "web\\project-map-ui\\README.md",
  "web\\project-map-ui\\build-project-map.py",
  "web\\project-map-ui\\project-map-runtime.js",
  "web\\project-map-ui\\project-map-template.html"
)

$forbidden = @(
  "backup",
  "recovered_20260318_165117",
  ".bak_20260315_00",
  "ops\\history",
  "docs/reviews/EXTERNAL_REVIEW_PACKAGE.md",
  "docs/reviews/EXTERNAL_REVIEW_COVER_NOTE.md",
  "docs/reviews/EXTERNAL_REVIEW_HIGHLIGHTS.md",
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
  missing = @($missing)
  forbidden_present = @($presentForbidden)
  content_violations = @($contentViolations)
  ok = [bool]$rulesCheck.ok -and ($missing.Count -eq 0) -and ($presentForbidden.Count -eq 0) -and (@($contentViolations).Count -eq 0)
}
