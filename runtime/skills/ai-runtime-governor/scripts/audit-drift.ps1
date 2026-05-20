param(
  [string]$SharedRoot = 'C:\Dev\AI_UNIFIED',
  [switch]$UpdateBaseline
)

$ErrorActionPreference = 'Stop'
$opsRoot = Join-Path $SharedRoot 'ops'
$baselinePath = Join-Path $opsRoot 'baseline.json'
$ts = Get-Date -Format 'yyyyMMdd_HHmmss'
$outDir = Join-Path (Join-Path $opsRoot 'history') ("drift_$ts")
New-Item -ItemType Directory -Force -Path $outDir, $opsRoot | Out-Null

if (-not (Test-Path $baselinePath)) {
  if (-not $UpdateBaseline) {
    Write-Output "baseline_missing=$baselinePath"
    exit 2
  }

  $seed = @(
    "$HOME/.codex/config.toml",
    "$HOME/.claude/settings.json",
    "$HOME/.claude.json",
    "$HOME/.gemini/settings.json",
    "$env:APPDATA/GitHub CLI/config.yml",
    "$env:APPDATA/Code/User/settings.json",
    "C:\Dev\.mcp.json",
    "C:\Dev\AI_UNIFIED\mcp\claude.mcp.json"
  ) | Select-Object -Unique

  $seedHashes = @()
  foreach ($f in $seed) {
    if (Test-Path $f -PathType Leaf) {
      $h = Get-FileHash $f -Algorithm SHA256
      $seedHashes += [pscustomobject]@{ path=$f; sha256=$h.Hash }
    }
  }
  $seedBase = [pscustomobject]@{ generated_at=(Get-Date).ToString('s'); run_dir=$outDir; files=$seedHashes }
  $seedBase | ConvertTo-Json -Depth 6 | Set-Content -Path $baselinePath -Encoding UTF8
  Write-Output "baseline_created=$baselinePath"
  exit 0
}

$baseline = Get-Content $baselinePath -Raw | ConvertFrom-Json
$report = @()

foreach ($entry in $baseline.files) {
  $p = [string]$entry.path
  $old = [string]$entry.sha256
  if (-not (Test-Path $p -PathType Leaf)) {
    $report += [pscustomobject]@{ path=$p; status='MISSING'; old_sha256=$old; new_sha256=$null }
    continue
  }
  $new = (Get-FileHash $p -Algorithm SHA256).Hash
  if ($new -eq $old) {
    $report += [pscustomobject]@{ path=$p; status='UNCHANGED'; old_sha256=$old; new_sha256=$new }
  } else {
    $report += [pscustomobject]@{ path=$p; status='DRIFT'; old_sha256=$old; new_sha256=$new }
  }
}

$reportPath = Join-Path $outDir 'drift.json'
$report | ConvertTo-Json -Depth 6 | Set-Content -Path $reportPath -Encoding UTF8

if ($UpdateBaseline) {
  $newBase = @()
  foreach ($r in $report) {
    if ($r.status -ne 'MISSING') {
      $newBase += [pscustomobject]@{ path=$r.path; sha256=$r.new_sha256 }
    }
  }
  $obj = [pscustomobject]@{ generated_at=(Get-Date).ToString('s'); run_dir=$outDir; files=$newBase }
  $obj | ConvertTo-Json -Depth 6 | Set-Content -Path $baselinePath -Encoding UTF8
}

$driftCount = @($report | Where-Object { $_.status -eq 'DRIFT' }).Count
$missingCount = @($report | Where-Object { $_.status -eq 'MISSING' }).Count
Write-Output "drift_report=$reportPath"
Write-Output "drift_count=$driftCount"
Write-Output "missing_count=$missingCount"
