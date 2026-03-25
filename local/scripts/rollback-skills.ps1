param(
  [string]$RunDir = "",
  [string]$Id = "",
  [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$repo = (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path
$history = Join-Path $repo "ops\history"
. (Join-Path $PSScriptRoot "lib\path-safety.ps1")

if (-not $RunDir) {
  $runs = @(Get-ChildItem $history -Directory | Where-Object { $_.Name -like "adopt_*" } | Sort-Object Name -Descending)
  if ($runs.Count -eq 0) {
    Write-Output "no adopt backups found"
    return
  }

  $runs
  return
}

$safeRunDir = Resolve-SafeRepoPath -RepoRoot $repo -BaseRelativePath "ops\history" -UserPath $RunDir -AllowBasePath -RequireExisting
if ((Split-Path $safeRunDir -Leaf) -notlike "adopt_*") {
  throw "RunDir must point to an adopt_* backup directory under ops/history."
}

if (-not $Id) {
  Get-ChildItem -LiteralPath $safeRunDir -Directory
  return
}

$safeId = Assert-SafeSimpleName -Value $Id -Label "Id" -Pattern '^[a-z0-9][a-z0-9-]{0,63}$'
$skillsRoot = Join-Path $repo "registry\skills"
$source = Resolve-SafeRepoPath -RepoRoot $safeRunDir -BaseRelativePath "." -UserPath $safeId -RequireExisting
$target = Resolve-SafeRepoPath -RepoRoot $repo -BaseRelativePath "registry\skills" -UserPath $safeId
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$rollbackRunDir = Join-Path $history "rollback_$stamp"
$backup = Join-Path $rollbackRunDir $safeId

if (Test-ContainsReparsePoint -Path $source) {
  throw "backup source contains a symlink or reparse point: $source"
}

if (-not (Test-Path -LiteralPath $source)) {
  throw "backup source not found: $source"
}

if ($DryRun) {
  [pscustomobject]@{
    action = "restore"
    source = $source
    target = $target
    existing_target = (Test-Path -LiteralPath $target)
    backup_path = if (Test-Path -LiteralPath $target) { $backup } else { $null }
  }
  return
}

if (Test-Path -LiteralPath $target) {
  if (Test-ContainsReparsePoint -Path $target) {
    throw "target contains a symlink or reparse point: $target"
  }

  New-Item -ItemType Directory -Force -Path $rollbackRunDir | Out-Null
  Copy-Item -LiteralPath $target -Destination $backup -Recurse -Force
  Remove-Item -LiteralPath $target -Recurse -Force
}

Copy-Item -LiteralPath $source -Destination $target -Recurse -Force

$summary = [ordered]@{
  action = "restore"
  restored_id = $safeId
  source = $source
  target = $target
  backup_path = if (Test-Path -LiteralPath $backup) { $backup } else { $null }
  generated_at = (Get-Date).ToString("s")
}

if (-not (Test-Path -LiteralPath $rollbackRunDir)) {
  New-Item -ItemType Directory -Force -Path $rollbackRunDir | Out-Null
}

$summary | ConvertTo-Json -Depth 4 | Set-Content (Join-Path $rollbackRunDir "summary.json")
[pscustomobject]$summary
