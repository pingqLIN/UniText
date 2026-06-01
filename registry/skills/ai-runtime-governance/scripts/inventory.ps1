param(
  [string]$SharedRoot = 'C:\Dev\AI_UNIFIED'
)

$ErrorActionPreference = 'Stop'
$ts = Get-Date -Format 'yyyyMMdd_HHmmss'
$opsRoot = Join-Path $SharedRoot 'ops'
$histRoot = Join-Path $opsRoot 'history'
$invDir = Join-Path $histRoot ("inventory_$ts")
New-Item -ItemType Directory -Force -Path $invDir, $opsRoot | Out-Null

function Get-CmdInfo([string]$name) {
  $c = Get-Command $name -ErrorAction SilentlyContinue | Select-Object -First 1
  if (-not $c) {
    return [pscustomobject]@{ name = $name; found = $false; source = $null; version = $null }
  }
  $runner = if ([string]::IsNullOrWhiteSpace([string]$c.Source)) { $name } else { [string]$c.Source }
  $ver = $null
  try {
    $ver = (& $runner --version 2>$null | Select-Object -First 1)
  } catch {}
  [pscustomobject]@{ name = $name; found = $true; source = $runner; version = $ver }
}

function Get-PathInfo([string]$path) {
  if (-not (Test-Path $path)) {
    return [pscustomobject]@{ path = $path; exists = $false; kind = $null; attrs = $null; target = $null }
  }
  $i = Get-Item $path -Force
  $kind = if ($i.PSIsContainer) { 'dir' } else { 'file' }
  $target = $null
  if ($i.Attributes -band [IO.FileAttributes]::ReparsePoint) {
    $target = $i.Target
  }
  [pscustomobject]@{ path = $path; exists = $true; kind = $kind; attrs = "$($i.Attributes)"; target = $target }
}

$cliNames = @('codex','gemini','claude','gh','code','windsurf','chatgpt','ollama','python','node','npm','uv','docker','wsl','git')
$pathList = @(
  "$HOME/.codex/config.toml",
  "$HOME/.codex/skills",
  "$HOME/.claude/settings.json",
  "$HOME/.claude.json",
  "$HOME/.claude/skills",
  "$HOME/.claude/plans",
  "$HOME/.gemini/settings.json",
  "$HOME/.gemini/skills",
  "$HOME/.agents/skills",
  "$env:APPDATA/GitHub CLI/config.yml",
  "$env:APPDATA/Code/User/settings.json",
  "$env:LOCALAPPDATA/Programs/Windsurf",
  "$env:LOCALAPPDATA/Programs/Microsoft VS Code",
  "$HOME/.cache/huggingface",
  "$HOME/.ollama/models",
  "C:\Dev\.mcp.json",
  "C:\Dev\AI_UNIFIED\mcp\claude.mcp.json",
  "C:\Dev\AI_UNIFIED\skills",
  "C:\Dev\AI_UNIFIED\workflow"
)

$settingsExtract = @{}
$codexCfg = "$HOME/.codex/config.toml"
if (Test-Path $codexCfg) {
  $line = (Select-String -Path $codexCfg -Pattern '^skills_path\s*=\s*".*"' -SimpleMatch:$false | Select-Object -First 1).Line
  $settingsExtract['codex.skills_path'] = $line
}
$claudeSettings = "$HOME/.claude/settings.json"
if (Test-Path $claudeSettings) {
  try {
    $j = Get-Content $claudeSettings -Raw | ConvertFrom-Json
    $settingsExtract['claude.autoUpdatesChannel'] = $j.autoUpdatesChannel
    $settingsExtract['claude.plansDirectory'] = $j.plansDirectory
  } catch {}
}
$geminiSettings = "$HOME/.gemini/settings.json"
if (Test-Path $geminiSettings) {
  try {
    $j = Get-Content $geminiSettings -Raw | ConvertFrom-Json
    $settingsExtract['gemini.general.enableAutoUpdate'] = $j.general.enableAutoUpdate
    $settingsExtract['gemini.general.disableAutoUpdate'] = $j.general.disableAutoUpdate
  } catch {}
}

$report = [pscustomobject]@{
  generated_at = (Get-Date).ToString('s')
  shared_root = $SharedRoot
  cli = @($cliNames | ForEach-Object { Get-CmdInfo $_ })
  paths = @($pathList | ForEach-Object { Get-PathInfo $_ })
  settings = $settingsExtract
}

$jsonPath = Join-Path $invDir 'inventory.json'
$latestJson = Join-Path $opsRoot 'inventory.latest.json'
$report | ConvertTo-Json -Depth 8 | Set-Content -Path $jsonPath -Encoding UTF8
$report | ConvertTo-Json -Depth 8 | Set-Content -Path $latestJson -Encoding UTF8

Write-Output "inventory_json=$jsonPath"
Write-Output "inventory_latest=$latestJson"
