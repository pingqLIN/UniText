param(
  [string[]]$Scope = @(
    "README.md",
    "INDEX.md",
    "OPERATIONS.md",
    "PROJECT_MODES.md",
    "SECRET_HANDLING_GUIDELINES.md",
    "TEMPLATE_RELEASE_PACKAGE.md",
    "TEMPLATE_RELEASE_CHECKLIST.md",
    "REBUILD_AS_NEW_PROJECT.md",
    "NO_PUBLISH_POLICY.md",
    "DOCUMENT_PLACEMENT_POLICY.md",
    "BOUNDARY_INCIDENT_REVIEW_TEMPLATE.md",
    ".mcp.json",
    ".claude/settings.json",
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
  [pscustomobject]@{ label = "live workspace hostname"; regex = '(?i)\b(?:[\w-]+\.)?colorgeek\.co\b' },
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
