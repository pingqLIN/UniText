param(
  [ValidateSet('single','global','all')]
  [string]$Scope = 'all',
  [ValidateSet('codex','claude','gemini','gh','vscode','windsurf')]
  [string]$Program = 'codex',
  [string]$SharedRoot = 'C:\Dev\AI_UNIFIED',
  [string]$ProjectRoot = 'C:\Dev',
  [switch]$Apply
)

$ErrorActionPreference = 'Stop'
$ts = Get-Date -Format 'yyyyMMdd_HHmmss'
$opsRoot = Join-Path $SharedRoot 'ops'
$runDir = Join-Path (Join-Path $opsRoot 'history') ("unify_$ts")
New-Item -ItemType Directory -Force -Path $runDir, $opsRoot | Out-Null

$sharedSkills = Join-Path $SharedRoot 'skills'
$sharedMcp = Join-Path $SharedRoot 'mcp'
$sharedWorkflow = Join-Path $SharedRoot 'workflow'
$sharedClaudePlans = Join-Path $sharedWorkflow 'claude-plans'
$canonMcpFile = Join-Path $sharedMcp 'claude.mcp.json'

$userHome = $HOME
$codexSkills = Join-Path $userHome '.codex\skills'
$claudeSkills = Join-Path $userHome '.claude\skills'
$geminiSkills = Join-Path $userHome '.gemini\skills'
$agentsSkills = Join-Path $userHome '.agents\skills'
$claudePlans = Join-Path $userHome '.claude\plans'
$projectMcp = Join-Path $ProjectRoot '.mcp.json'
$codexConfig = Join-Path $userHome '.codex\config.toml'

function Ensure-Dir([string]$path) {
  if (-not (Test-Path $path)) { New-Item -ItemType Directory -Force -Path $path | Out-Null }
}

function Parse-CodexSkillsPath([string]$cfgPath) {
  if (-not (Test-Path $cfgPath)) { return $null }
  $m = Select-String -Path $cfgPath -Pattern '^skills_path\s*=\s*"([^"]+)"' -AllMatches | Select-Object -First 1
  if (-not $m) { return $null }
  return $m.Matches[0].Groups[1].Value
}

function Is-JunctionTarget([string]$link, [string]$target) {
  if (-not (Test-Path $link)) { return $false }
  $i = Get-Item $link -Force
  if (-not ($i.Attributes -band [IO.FileAttributes]::ReparsePoint)) { return $false }
  $actual = [string]$i.Target
  return ($actual.TrimEnd('\\') -ieq $target.TrimEnd('\\'))
}

function Is-HardlinkPair([string]$a, [string]$b) {
  if (-not (Test-Path $a) -or -not (Test-Path $b)) { return $false }
  $out = cmd /c "fsutil hardlink list \"$a\"" 2>$null
  if (-not $out) { return $false }
  foreach ($line in $out) {
    if ($line.Trim().ToLower() -eq $b.ToLower()) { return $true }
  }
  return $false
}

function Backup-Path([string]$path) {
  if (-not (Test-Path $path)) { return $null }
  $bak = "$path.bak.$ts"
  Rename-Item $path $bak -Force
  return $bak
}

function Create-Junction([string]$link, [string]$target) {
  $parent = Split-Path $link -Parent
  Ensure-Dir $parent
  Ensure-Dir $target
  cmd /c "mklink /J \"$link\" \"$target\"" | Out-Null
}

function Create-Hardlink([string]$link, [string]$target) {
  $parent = Split-Path $link -Parent
  Ensure-Dir $parent
  if (-not (Test-Path $target)) { '{"mcpServers":{}}' | Set-Content -Path $target -Encoding UTF8 }
  cmd /c "mklink /H \"$link\" \"$target\"" | Out-Null
}

Ensure-Dir $sharedMcp
Ensure-Dir $sharedWorkflow
Ensure-Dir $sharedClaudePlans
if (-not (Test-Path $canonMcpFile)) { '{"mcpServers":{}}' | Set-Content -Path $canonMcpFile -Encoding UTF8 }

$cfgSkillsPath = Parse-CodexSkillsPath $codexConfig
$ops = @()

$includeCodex = ($Scope -eq 'all' -or $Scope -eq 'global' -or ($Scope -eq 'single' -and $Program -eq 'codex'))
$includeClaude = ($Scope -eq 'all' -or $Scope -eq 'global' -or ($Scope -eq 'single' -and $Program -eq 'claude'))
$includeGemini = ($Scope -eq 'all' -or $Scope -eq 'global' -or ($Scope -eq 'single' -and $Program -eq 'gemini'))
$includeMcp = ($Scope -eq 'all' -or $Scope -eq 'global' -or ($Scope -eq 'single' -and $Program -in @('claude','gh','vscode','windsurf')))

if ($includeCodex) {
  $ops += [pscustomobject]@{ kind='junction'; link=$sharedSkills; target=$codexSkills; note='shared skills root follows codex skills'; enabled=$true }
  if ($cfgSkillsPath -and ($cfgSkillsPath.TrimEnd('\\') -ine $codexSkills.TrimEnd('\\'))) {
    $ops += [pscustomobject]@{ kind='junction'; link=$cfgSkillsPath; target=$sharedSkills; note='bridge codex configured skills_path without editing config'; enabled=$true }
  }
}
if ($includeClaude) {
  $ops += [pscustomobject]@{ kind='junction'; link=$claudeSkills; target=$sharedSkills; note='claude skills -> shared'; enabled=$true }
  $ops += [pscustomobject]@{ kind='junction'; link=$claudePlans; target=$sharedClaudePlans; note='claude plans -> shared workflow'; enabled=$true }
}
if ($includeGemini) {
  $ops += [pscustomobject]@{ kind='junction'; link=$geminiSkills; target=$sharedSkills; note='gemini skills -> shared'; enabled=$true }
  $ops += [pscustomobject]@{ kind='junction'; link=$agentsSkills; target=$sharedSkills; note='agents skills alias -> shared'; enabled=$true }
}
if ($includeMcp) {
  $ops += [pscustomobject]@{ kind='hardlink'; link=$projectMcp; target=$canonMcpFile; note='project mcp file -> canonical mcp file'; enabled=$true }
}

$plan = @()
foreach ($op in $ops) {
  if ($op.kind -eq 'junction') {
    $already = Is-JunctionTarget $op.link $op.target
    $plan += [pscustomobject]@{ kind=$op.kind; link=$op.link; target=$op.target; note=$op.note; action=($(if($already){'skip'}else{'apply'})) }
  } elseif ($op.kind -eq 'hardlink') {
    $already = Is-HardlinkPair $op.link $op.target
    $plan += [pscustomobject]@{ kind=$op.kind; link=$op.link; target=$op.target; note=$op.note; action=($(if($already){'skip'}else{'apply'})) }
  }
}

$planPath = Join-Path $runDir 'plan.json'
$plan | ConvertTo-Json -Depth 6 | Set-Content -Path $planPath -Encoding UTF8

if (-not $Apply) {
  Write-Output "mode=DRY_RUN"
  Write-Output "plan=$planPath"
  $plan | Format-Table -AutoSize | Out-String | Write-Output
  exit 0
}

$results = @()
foreach ($op in $plan) {
  if ($op.action -eq 'skip') {
    $results += [pscustomobject]@{ kind=$op.kind; link=$op.link; target=$op.target; result='SKIP_ALREADY_MATCHED'; backup=$null }
    continue
  }
  try {
    $bak = Backup-Path $op.link
    if ($op.kind -eq 'junction') {
      Create-Junction $op.link $op.target
    } else {
      Create-Hardlink $op.link $op.target
    }
    $results += [pscustomobject]@{ kind=$op.kind; link=$op.link; target=$op.target; result='APPLIED'; backup=$bak }
  } catch {
    $results += [pscustomobject]@{ kind=$op.kind; link=$op.link; target=$op.target; result=("FAILED: " + $_.Exception.Message); backup=$bak }
  }
}

$resultPath = Join-Path $runDir 'result.json'
$results | ConvertTo-Json -Depth 6 | Set-Content -Path $resultPath -Encoding UTF8

# Baseline file hashes for drift audit
$baselineTargets = @(
  $codexConfig,
  "$userHome/.claude/settings.json",
  "$userHome/.claude.json",
  "$userHome/.gemini/settings.json",
  "$env:APPDATA/GitHub CLI/config.yml",
  "$env:APPDATA/Code/User/settings.json",
  $projectMcp,
  $canonMcpFile
) | Select-Object -Unique

$hashes = @()
foreach ($f in $baselineTargets) {
  if (Test-Path $f -PathType Leaf) {
    $h = Get-FileHash $f -Algorithm SHA256
    $hashes += [pscustomobject]@{ path=$f; sha256=$h.Hash }
  }
}
$baseline = [pscustomobject]@{ generated_at=(Get-Date).ToString('s'); run_dir=$runDir; files=$hashes }
$baselinePath = Join-Path $opsRoot 'baseline.json'
$baseline | ConvertTo-Json -Depth 6 | Set-Content -Path $baselinePath -Encoding UTF8

Write-Output "mode=APPLY"
Write-Output "plan=$planPath"
Write-Output "result=$resultPath"
Write-Output "baseline=$baselinePath"
