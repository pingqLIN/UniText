param(
  [string]$Source = ".bak_20260315_00\skills.bak.20260228_215107",
  [string]$Destination = "registry\skills",
  [string[]]$Ids = @("frontend-design", "pdf", "docx", "xlsx", "mcp-builder"),
  [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$repo = Resolve-Path (Join-Path $PSScriptRoot "..\\..")
$srcRoot = Resolve-Path $Source
$dstRoot = Join-Path $repo $Destination
$runId = Get-Date -Format "yyyyMMdd_HHmmss"
$runDir = Join-Path $repo "ops\history\adopt_$runId"
New-Item -ItemType Directory -Force -Path $dstRoot | Out-Null

if (-not $DryRun) {
  New-Item -ItemType Directory -Force -Path $runDir | Out-Null
}

foreach ($id in $Ids) {
  $src = Join-Path $srcRoot $id
  $dst = Join-Path $dstRoot $id
  if (-not (Test-Path $src)) {
    Write-Warning "missing source: $id"
    continue
  }

  if ($DryRun) {
    Write-Output "would adopt $id -> $dst"
    continue
  }

  if (Test-Path $dst) {
    $backup = Join-Path $runDir $id
    Copy-Item $dst $backup -Recurse
    Remove-Item $dst -Recurse -Force
  }

  Copy-Item $src $dst -Recurse
  Write-Output "adopted $id"
}
