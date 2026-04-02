param(
  [string[]]$Scope = @(
    "AGENTS.md",
    "README.md",
    "INDEX.md",
    "VISION.md",
    "RESOURCE_SPEC.md",
    "OPERATIONS.md",
    "PROJECT_MODES.md",
    "SECRET_HANDLING_GUIDELINES.md",
    "TEMPLATE_RELEASE_PACKAGE.md",
    "TEMPLATE_RELEASE_CHECKLIST.md",
    "REBUILD_AS_NEW_PROJECT.md",
    "MILESTONES.md",
    "NO_PUBLISH_POLICY.md",
    "DOCUMENT_PLACEMENT_POLICY.md",
    "BOUNDARY_INCIDENT_REVIEW_TEMPLATE.md",
    "COPILOT_CLI_ADAPTER_NOTE.md",
    "SKILL0_COLLABORATION_VISION.md",
    "ESSENTIAL_SKILLS_SHORTLIST.md",
    "EXTERNAL_REVIEW_PACKAGE.md",
    "EXTERNAL_REVIEW_COVER_NOTE.md",
    "EXTERNAL_REVIEW_HIGHLIGHTS.md",
    ".mcp.json",
    ".claude/settings.json",
    "local/scripts/bootstrap.py",
    "local/scripts/git-startup.ps1",
    "local/scripts/health-check.ps1",
    "local/scripts/export-template-package.ps1",
    "local/scripts/verify-template-package.ps1",
    "local/scripts/export-rebuild-project.ps1",
    "local/scripts/verify-rebuild-project.ps1",
    "local/scripts/verify-workspace-boundaries.ps1",
    "local/scripts/get-publishability-report.ps1",
    "registry"
  )
)

$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path
$tracked = & git -C $root ls-files -- $Scope

if ($LASTEXITCODE -ne 0) {
  throw "git ls-files failed while resolving tracked files for boundary verification."
}

$trackedFiles = @($tracked | Where-Object { $_ })
$pathRules = @(
  [pscustomobject]@{ label = "tracked authoring doc"; regex = '^local/docs/authoring/' },
  [pscustomobject]@{ label = "tracked live local doc"; regex = '^local/docs/.+_LIVE\.md$' },
  [pscustomobject]@{ label = "tracked workspace baseline doc"; regex = '^local/docs/.+_WORKSPACE_BASELINE\.md$' },
  [pscustomobject]@{ label = "tracked operations state"; regex = '^ops/' }
)

$contentPatterns = @(
  [pscustomobject]@{ label = "machine-specific Windows path"; regex = '(?i)\b[A-Z]:\\(Users|Services|Projects)\\' },
  [pscustomobject]@{ label = "live workspace hostname"; regex = '(?i)\b(?:zone hostname|ingress|hostnames?|domain|redirect uris?)\b[^\r\n]*\b(?!workspace\.example\.com\b)(?!example\.com\b)(?:[a-z0-9-]+\.)+[a-z]{2,}\b' },
  [pscustomobject]@{ label = "live connector redirect URI"; regex = '(?i)https://chatgpt\.com/connector/oauth/' },
  [pscustomobject]@{ label = "live Cloudflare account or zone identifier"; regex = '(?i)\b(?:Account ID|Zone ID)\b[^\r\n]*\b[a-f0-9]{32}\b' },
  [pscustomobject]@{ label = "live Cloudflare tunnel or access app identifier"; regex = '(?i)\b(?:Tunnel ID|Access app ID)\b[^\r\n]*\b[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\b' }
)

$contentFiles = $trackedFiles | Where-Object {
  [IO.Path]::GetExtension($_) -in @(".md", ".json", ".jsonc", ".txt", ".ps1", ".py", ".toml", ".yml", ".yaml")
}

$pathViolations = foreach ($file in $trackedFiles) {
  foreach ($rule in $pathRules) {
    if ($file -match $rule.regex) {
      [pscustomobject]@{
        path = $file
        label = $rule.label
      }
    }
  }
}

$contentViolations = foreach ($file in $contentFiles) {
  $absolutePath = Join-Path $root $file
  foreach ($pattern in $contentPatterns) {
    $matches = Select-String -LiteralPath $absolutePath -Pattern $pattern.regex -AllMatches
    foreach ($match in $matches) {
      if ($file -match '\.(ps1|py)$' -and $match.Line -match '(?i)\b(regex|pattern|contentpatterns?)\b') {
        continue
      }
      [pscustomobject]@{
        path = $file
        label = $pattern.label
        line = $match.LineNumber
        text = $match.Line.Trim()
      }
    }
  }
}

[pscustomobject]@{
  scanned_scope = $Scope
  scanned_file_count = $trackedFiles.Count
  path_violations = @($pathViolations)
  content_violations = @($contentViolations)
  ok = (@($pathViolations).Count -eq 0) -and (@($contentViolations).Count -eq 0)
}
