param(
  [string]$Source = ".bak_20260315_00\\skills.bak.20260228_215107",
  [string]$Destination = "registry\\skills",
  [string[]]$Ids = @("frontend-design", "pdf", "docx", "xlsx", "mcp-builder"),
  [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$srcRoot = Resolve-Path $Source
$dstRoot = Join-Path (Resolve-Path ".") $Destination
New-Item -ItemType Directory -Force -Path $dstRoot | Out-Null

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
    Remove-Item $dst -Recurse -Force
  }

  Copy-Item $src $dst -Recurse
  Write-Output "adopted $id"
}
