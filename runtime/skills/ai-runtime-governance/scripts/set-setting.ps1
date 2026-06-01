param(
  [ValidateSet('codex','claude','gemini','vscode','windsurf')]
  [string]$Program,
  [Parameter(Mandatory = $true)]
  [string]$Key,
  [Parameter(Mandatory = $true)]
  [string]$Value,
  [string]$SharedRoot = 'C:\Dev\AI_UNIFIED',
  [switch]$Apply
)

$ErrorActionPreference = 'Stop'
$ts = Get-Date -Format 'yyyyMMdd_HHmmss'
$runDir = Join-Path (Join-Path $SharedRoot 'ops\history') ("set_setting_$ts")
New-Item -ItemType Directory -Force -Path $runDir | Out-Null

function Split-KeyPath([string]$k) { return $k.Split('.') }

function Set-NestedJsonValue([object]$obj, [string[]]$segments, [object]$val) {
  $cur = $obj
  for ($i = 0; $i -lt $segments.Length - 1; $i++) {
    $seg = $segments[$i]
    if ($null -eq $cur.$seg) {
      $cur | Add-Member -NotePropertyName $seg -NotePropertyValue ([pscustomobject]@{}) -Force
    }
    $cur = $cur.$seg
  }
  $last = $segments[$segments.Length - 1]
  $cur | Add-Member -NotePropertyName $last -NotePropertyValue $val -Force
}

function Parse-TypedValue([string]$v) {
  if ($v -match '^(true|false)$') { return [bool]::Parse($v) }
  if ($v -match '^-?\d+$') { return [int]$v }
  if ($v -match '^-?\d+\.\d+$') { return [double]$v }
  return $v
}

$cfg = switch ($Program) {
  'codex' { "$HOME/.codex/config.toml" }
  'claude' { "$HOME/.claude/settings.json" }
  'gemini' { "$HOME/.gemini/settings.json" }
  'vscode' { "$env:APPDATA/Code/User/settings.json" }
  'windsurf' { "$env:APPDATA/Windsurf/User/settings.json" }
}

if (-not (Test-Path $cfg)) {
  Write-Output "config_missing=$cfg"
  exit 2
}

$typed = Parse-TypedValue $Value
$preview = [pscustomobject]@{ program=$Program; config=$cfg; key=$Key; new_value=$typed; mode=$(if($Apply){'APPLY'}else{'DRY_RUN'}) }
$previewPath = Join-Path $runDir 'preview.json'
$preview | ConvertTo-Json -Depth 6 | Set-Content -Path $previewPath -Encoding UTF8

if (-not $Apply) {
  Write-Output "mode=DRY_RUN"
  Write-Output "preview=$previewPath"
  exit 0
}

$bak = "$cfg.bak.$ts"
Copy-Item $cfg $bak -Force

if ($Program -eq 'codex') {
  $raw = Get-Content $cfg -Raw
  $escapedKey = [regex]::Escape($Key)
  $valueToml = if ($typed -is [bool]) { $typed.ToString().ToLower() } elseif ($typed -is [int] -or $typed -is [double]) { "$typed" } else { '"' + (($typed -replace '"','\"')) + '"' }
  $pattern = "(?m)^$escapedKey\s*=\s*.*$"
  if ($raw -match $pattern) {
    $raw = [regex]::Replace($raw, $pattern, "$Key = $valueToml")
  } else {
    $raw = "$Key = $valueToml`r`n" + $raw
  }
  Set-Content -Path $cfg -Value $raw -Encoding UTF8
} else {
  $json = Get-Content $cfg -Raw | ConvertFrom-Json
  Set-NestedJsonValue -obj $json -segments (Split-KeyPath $Key) -val $typed
  $json | ConvertTo-Json -Depth 40 | Set-Content -Path $cfg -Encoding UTF8
}

$result = [pscustomobject]@{ program=$Program; config=$cfg; key=$Key; new_value=$typed; backup=$bak; status='APPLIED' }
$resultPath = Join-Path $runDir 'result.json'
$result | ConvertTo-Json -Depth 6 | Set-Content -Path $resultPath -Encoding UTF8

Write-Output "mode=APPLY"
Write-Output "result=$resultPath"
Write-Output "backup=$bak"
