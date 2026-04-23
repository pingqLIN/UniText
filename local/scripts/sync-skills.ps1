param(
  [switch]$DryRun,
  [switch]$Force,
  [switch]$SkipBackup
)

$ErrorActionPreference = "Stop"
$repo = Resolve-Path (Join-Path $PSScriptRoot "..\\..")
$source = Join-Path $repo "runtime\skills"
$targets = @(
  "$HOME\.claude\skills",
  "$HOME\.gemini\skills",
  "$HOME\.agents\skills"
)

if (-not (Test-Path $source)) {
  throw "skills source not found: $source"
}

function Get-CanonicalAliasEntries {
  param(
    [string]$SourcePath,
    [string]$TargetPath
  )

  if (-not (Test-Path -LiteralPath $TargetPath)) {
    return @()
  }

  $canonicalByKey = @{}
  Get-ChildItem -LiteralPath $SourcePath -Force | ForEach-Object {
    $canonicalByKey[$_.Name.ToLowerInvariant()] = $_.Name
  }

  $aliases = @()
  Get-ChildItem -LiteralPath $TargetPath -Force | ForEach-Object {
    $canonicalName = $canonicalByKey[$_.Name.ToLowerInvariant()]
    if ($canonicalName -and $_.Name -cne $canonicalName) {
      $aliases += [pscustomobject]@{
        path = $_.FullName
        canonical_name = $canonicalName
      }
    }
  }

  return $aliases
}

$runId = Get-Date -Format "yyyyMMdd_HHmmss"
$runDir = Join-Path $repo "ops\history\sync_$runId"
$summary = @()

if (-not $DryRun) {
  New-Item -ItemType Directory -Force -Path $runDir | Out-Null
}

foreach ($target in $targets) {
  $item = if (Test-Path $target) { Get-Item $target -Force } else { $null }
  $isLink = [bool]($item -and $item.LinkType)
  $linkTarget = if ($isLink) { $item.Target } else { $null }
  $aliasEntries = if ((Test-Path -LiteralPath $target) -and -not $isLink) {
    @(Get-CanonicalAliasEntries -SourcePath $source -TargetPath $target)
  } else {
    @()
  }

  if ($isLink -and $linkTarget -like "*runtime\skills") {
    $summary += [pscustomobject]@{
      target = $target
      mode = "symlink"
      action = "skip"
      reason = "already points to runtime source"
    }
    continue
  }

  if ($DryRun) {
    $summary += [pscustomobject]@{
      target = $target
      mode = if ($isLink) { "symlink" } else { "mirror" }
      action = "dry-run"
      reason = if ($isLink) { "link target mismatch - review required" } else { "would backup and sync" }
      alias_prune_candidates = $aliasEntries
    }
    continue
  }

  if ($isLink) {
    throw "target requires review before sync: $target -> $linkTarget"
  }

  if (-not $Force) {
    throw "non-dry-run sync requires -Force"
  }

  New-Item -ItemType Directory -Force -Path $target | Out-Null

  if ((Test-Path $target) -and -not $SkipBackup) {
    $backupTarget = Join-Path $runDir ([IO.Path]::GetFileName($target))
    Copy-Item $target $backupTarget -Recurse
  }

  foreach ($aliasEntry in $aliasEntries) {
    Remove-Item -LiteralPath $aliasEntry.path -Recurse -Force
  }

  $log = Join-Path $runDir ("sync-" + ([IO.Path]::GetFileName($target)) + ".log")
  $output = & robocopy $source $target /E /R:1 /W:1 /NFL /NDL /NJH /NJS /NP 2>&1
  $output | Tee-Object -FilePath $log | Out-Host
  $exit = $LASTEXITCODE

  if ($exit -gt 7) {
    throw "robocopy failed for $target with exit code $exit"
  }

  $summary += [pscustomobject]@{
    target = $target
    mode = "mirror"
    action = "synced"
    reason = "robocopy /E completed"
    log = $log
    exit_code = $exit
    pruned_alias_entries = $aliasEntries
  }
}

$summaryPath = Join-Path $runDir "summary.json"
if (-not $DryRun) {
  $summary | ConvertTo-Json -Depth 4 | Set-Content $summaryPath
}
$summary
