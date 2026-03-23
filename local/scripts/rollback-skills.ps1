param(
  [string]$RunDir = "",
  [string]$Id = "",
  [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$repo = Resolve-Path (Join-Path $PSScriptRoot "..\\..")
$history = Join-Path $repo "ops\history"

if (-not $RunDir) {
  $runs = Get-ChildItem $history -Directory | Where-Object { $_.Name -like "adopt_*" } | Sort-Object Name -Descending
  if ($runs.Count -eq 0) {
    Write-Output "no adopt backups found"
    return
  }

  $runs
  return
}

$source = Join-Path $RunDir $Id
$target = Join-Path $repo ("registry\skills\" + $Id)

if (-not $Id) {
  Get-ChildItem $RunDir -Directory
  return
}

if (-not (Test-Path $source)) {
  throw "backup source not found: $source"
}

if ($DryRun) {
  Write-Output "would restore $source -> $target"
  return
}

if (Test-Path $target) {
  Remove-Item $target -Recurse -Force
}

Copy-Item $source $target -Recurse
Write-Output "restored $Id"
