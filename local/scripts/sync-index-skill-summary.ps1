param(
  [string]$Root = ".",
  [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$repo = (Resolve-Path $Root).Path
$indexPath = Join-Path $repo "INDEX.md"
$skillsRoot = Join-Path $repo "registry\skills"

if (-not (Test-Path -LiteralPath $indexPath)) {
  throw "INDEX.md not found under root: $repo"
}

if (-not (Test-Path -LiteralPath $skillsRoot)) {
  throw "registry/skills not found under root: $repo"
}

$skillCount = (Get-ChildItem -LiteralPath $skillsRoot -Directory | Where-Object { -not $_.Name.StartsWith(".") }).Count
$today = Get-Date -Format "yyyy-MM-dd"

$content = Get-Content -LiteralPath $indexPath -Raw

# Match the one-line skills summary by stable tokens instead of locale-specific text.
$summaryPattern = '(?m)^(?<prefix>.*?`)(?<date>\d{4}-\d{2}-\d{2})(?<middle>`.*?`registry/skills/`.*?`)(?<count>\d+)(?<suffix>`.*review-facing catalog excerpt.*)$'
$match = [regex]::Match($content, $summaryPattern)

if (-not $match.Success) {
  throw "Could not locate INDEX.md skills summary line."
}

$summaryLine = $match.Value
$updatedLine = "$($match.Groups['prefix'].Value)$today$($match.Groups['middle'].Value)$skillCount$($match.Groups['suffix'].Value)"
$updated = $content.Replace($summaryLine, $updatedLine)

$changed = $updated -ne $content
$result = [pscustomobject]@{
  index = $indexPath
  date = $today
  skill_count = $skillCount
  changed = $changed
  dry_run = [bool]$DryRun
}

if ($changed -and -not $DryRun) {
  Set-Content -LiteralPath $indexPath -Value $updated -Encoding utf8NoBOM
}

$result | ConvertTo-Json -Depth 3
