param(
  [ValidateSet('inventory','backup','plan','apply','audit')]
  [string]$Action = 'inventory',
  [ValidateSet('single','global','all')]
  [string]$Scope = 'all',
  [ValidateSet('codex','claude','gemini','gh','vscode','windsurf')]
  [string]$Program = 'codex',
  [string]$SharedRoot = 'C:\Dev\AI_UNIFIED',
  [string]$ProjectRoot = 'C:\Dev'
)

$base = Split-Path -Parent $MyInvocation.MyCommand.Path
switch ($Action) {
  'inventory' { pwsh -File (Join-Path $base 'inventory.ps1') -SharedRoot $SharedRoot }
  'backup'    { pwsh -File (Join-Path $base 'backup.ps1') -Scope $Scope -Program $Program -SharedRoot $SharedRoot }
  'plan'      { pwsh -File (Join-Path $base 'apply-path-unify.ps1') -Scope $Scope -Program $Program -SharedRoot $SharedRoot -ProjectRoot $ProjectRoot }
  'apply'     { pwsh -File (Join-Path $base 'apply-path-unify.ps1') -Scope $Scope -Program $Program -SharedRoot $SharedRoot -ProjectRoot $ProjectRoot -Apply }
  'audit'     { pwsh -File (Join-Path $base 'audit-drift.ps1') -SharedRoot $SharedRoot }
}
