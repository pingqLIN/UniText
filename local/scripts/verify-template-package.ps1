param(
  [string]$Path
)

$ErrorActionPreference = "Stop"

if (-not $Path) {
  throw "Path is required."
}

$resolvedPath = (Resolve-Path -LiteralPath $Path).Path

$required = @(
  ".gitignore",
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
  "local\\scripts\\sync-skills.ps1",
  "local\\scripts\\verify-workspace-boundaries.ps1"
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
  [pscustomobject]@{ label = "machine-specific Windows path"; regex = '(?i)\b[A-Z]:\\(Users|Services|Projects)\\' },
  [pscustomobject]@{ label = "live workspace hostname"; regex = '(?i)\b(?:[\w-]+\.)?colorgeek\.co\b' },
  [pscustomobject]@{ label = "live connector redirect URI"; regex = '(?i)https://chatgpt\.com/connector/oauth/' }
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

$contentViolations = foreach ($file in $contentFiles) {
  $relativePath = $file.FullName.Substring($resolvedPath.Length).TrimStart('\', '/')
  foreach ($pattern in $contentPatterns) {
    $matches = Select-String -LiteralPath $file.FullName -Pattern $pattern.regex -AllMatches
    foreach ($match in $matches) {
      [pscustomobject]@{
        path = $relativePath
        label = $pattern.label
        line = $match.LineNumber
        text = $match.Line.Trim()
      }
    }
  }
}

[pscustomobject]@{
  package_path = $resolvedPath
  missing = $missing
  forbidden_present = $presentForbidden
  content_violations = @($contentViolations)
  ok = ($missing.Count -eq 0) -and ($presentForbidden.Count -eq 0) -and (@($contentViolations).Count -eq 0)
}
