param(
  [ValidateSet('single','global','all')]
  [string]$Scope = 'all',
  [ValidateSet('codex','claude','gemini','gh','vscode','windsurf')]
  [string]$Program = 'codex',
  [string]$SharedRoot = 'C:\Dev\AI_UNIFIED'
)

$ErrorActionPreference = 'Stop'
$ts = Get-Date -Format 'yyyyMMdd_HHmmss'
$dst = Join-Path (Join-Path $SharedRoot 'ops\history') ("backup_$ts")
New-Item -ItemType Directory -Force -Path $dst | Out-Null

$map = @{
  codex = @("$HOME/.codex/config.toml","$HOME/.codex/skills")
  claude = @("$HOME/.claude/settings.json","$HOME/.claude.json","$HOME/.claude/skills","$HOME/.claude/plans","C:\Dev\.mcp.json")
  gemini = @("$HOME/.gemini/settings.json","$HOME/.gemini/skills","$HOME/.agents/skills")
  gh = @("$env:APPDATA/GitHub CLI/config.yml","$env:APPDATA/GitHub CLI/hosts.yml")
  vscode = @("$env:APPDATA/Code/User/settings.json")
  windsurf = @("$env:APPDATA/Windsurf/User/settings.json","$env:LOCALAPPDATA/Programs/Windsurf")
  global = @("C:\Dev\AI_UNIFIED\skills","C:\Dev\AI_UNIFIED\mcp","C:\Dev\AI_UNIFIED\workflow")
}

$targets = @()
if ($Scope -eq 'single') {
  $targets += $map[$Program]
} elseif ($Scope -eq 'global') {
  $targets += $map['global']
} else {
  foreach ($k in $map.Keys) { $targets += $map[$k] }
}

$manifest = @()
foreach ($t in ($targets | Select-Object -Unique)) {
  if (-not (Test-Path $t)) {
    $manifest += [pscustomobject]@{ path = $t; status = 'missing'; backup = $null }
    continue
  }

  $leaf = ($t -replace '[:\\/ ]','_')
  $out = Join-Path $dst $leaf
  $item = Get-Item $t -Force

  if ($item.PSIsContainer) {
    New-Item -ItemType Directory -Force -Path $out | Out-Null
    robocopy $t $out /E /R:1 /W:1 /NFL /NDL /NJH /NJS /NP | Out-Null
    $manifest += [pscustomobject]@{ path = $t; status = 'backed_up_dir'; backup = $out }
  } else {
    Copy-Item $t $out -Force
    $manifest += [pscustomobject]@{ path = $t; status = 'backed_up_file'; backup = $out }
  }
}

$manifestPath = Join-Path $dst 'manifest.json'
$manifest | ConvertTo-Json -Depth 6 | Set-Content -Path $manifestPath -Encoding UTF8
Write-Output "backup_dir=$dst"
Write-Output "manifest=$manifestPath"
