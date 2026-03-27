$ErrorActionPreference = "Stop"

$root = (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path
$gitignorePath = Join-Path $root ".gitignore"
$gitignore = if (Test-Path $gitignorePath) { Get-Content $gitignorePath } else { @() }

$requiredIgnorePatterns = @(
  "backup/",
  "recovered_*/",
  ".bak_*/",
  ".tmp/",
  "ops/history/*",
  "ops/review-package/",
  "ops/template-package/",
  "ops/rebuild-project/",
  "ops/git-bundles/",
  "local/docs/PATH_MAP.md",
  "local/docs/authoring/",
  "local/docs/reviews/"
)

$missingIgnorePatterns = $requiredIgnorePatterns | Where-Object { $_ -notin $gitignore }

$forbiddenTrackedPrefixes = @(
  "backup/",
  "recovered_",
  ".bak_",
  ".tmp/",
  "ops/history/",
  "ops/review-package/",
  "ops/template-package/",
  "ops/rebuild-project/",
  "ops/git-bundles/",
  "local/docs/authoring/",
  "local/docs/reviews/"
)

$trackedFiles = @(git ls-files)
$trackedViolations = @()

foreach ($prefix in $forbiddenTrackedPrefixes) {
  $trackedViolations += $trackedFiles | Where-Object { $_.StartsWith($prefix) }
}

$trackedViolations = $trackedViolations | Sort-Object -Unique

$configFiles = @(
  ".mcp.json",
  ".claude/settings.json"
)

$absolutePathPatterns = @(
  "C:\\Users\\",
  "C:\\dev\\UniText",
  "/Users/",
  "/home/"
)

$absolutePathHits = @()

foreach ($path in $configFiles) {
  $fullPath = Join-Path $root $path
  if (-not (Test-Path $fullPath)) {
    continue
  }

  $raw = Get-Content $fullPath -Raw
  foreach ($pattern in $absolutePathPatterns) {
    if ($raw -like "*$pattern*") {
      $absolutePathHits += [pscustomobject]@{
        path = $path
        pattern = $pattern
      }
    }
  }
}

[pscustomobject]@{
  required_ignore_patterns = $requiredIgnorePatterns
  missing_ignore_patterns = $missingIgnorePatterns
  tracked_violations = $trackedViolations
  absolute_path_hits = $absolutePathHits
  ok = ($missingIgnorePatterns.Count -eq 0) -and ($trackedViolations.Count -eq 0) -and ($absolutePathHits.Count -eq 0)
}
