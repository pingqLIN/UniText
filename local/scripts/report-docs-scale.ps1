param(
  [string]$Root = ".",
  [switch]$AsJson
)

$ErrorActionPreference = "Stop"

$resolvedRoot = (Resolve-Path $Root).Path

function Get-RepoRelativePath {
  param(
    [string]$RepoRoot,
    [string]$FullName
  )

  $normalizedRoot = $RepoRoot.TrimEnd("\")

  if ($FullName.StartsWith("$normalizedRoot\")) {
    return $FullName.Substring($normalizedRoot.Length + 1).Replace("\", "/")
  }

  return $FullName.Replace("\", "/")
}

function Get-TopLevelBucket {
  param(
    [string]$RepoRoot,
    [string]$FullName
  )

  $relative = Get-RepoRelativePath -RepoRoot $RepoRoot -FullName $FullName

  if ($relative -notmatch "/") {
    return "root"
  }

  return ($relative -split "/")[0]
}

$markdownFiles = Get-ChildItem $resolvedRoot -Recurse -File -Filter "*.md"
$groupedCounts = $markdownFiles |
  Group-Object {
    Get-TopLevelBucket -RepoRoot $resolvedRoot -FullName $_.FullName
  } |
  Sort-Object Count -Descending

$areaCounts = @(
  $groupedCounts | ForEach-Object {
    [pscustomobject]@{
      area = $_.Name
      count = $_.Count
    }
  }
)

$report = [pscustomobject]@{
  repository_root = $resolvedRoot
  markdown_file_count = $markdownFiles.Count
  canonical_docs_count = @(
    $markdownFiles | Where-Object {
      $relative = Get-RepoRelativePath -RepoRoot $resolvedRoot -FullName $_.FullName
      ($relative -notmatch "/") -or
      $relative.StartsWith("local/docs/") -or
      $relative.StartsWith("template/")
    }
  ).Count
  review_archive_count = @(
    $markdownFiles | Where-Object {
      (Get-RepoRelativePath -RepoRoot $resolvedRoot -FullName $_.FullName).StartsWith("docs/reviews/")
    }
  ).Count
  i18n_count = @(
    $markdownFiles | Where-Object {
      (Get-RepoRelativePath -RepoRoot $resolvedRoot -FullName $_.FullName).StartsWith("i18n/")
    }
  ).Count
  area_counts = $areaCounts
}

if ($AsJson) {
  $report | ConvertTo-Json -Depth 6
  exit 0
}

$report
