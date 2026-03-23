param(
  [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$repo = Resolve-Path (Join-Path $PSScriptRoot "..\\..")
$source = Join-Path $repo "registry\\skills"
$targets = @(
  "$HOME\.claude\skills",
  "$HOME\.gemini\skills",
  "$HOME\.agents\skills"
)

if (-not (Test-Path $source)) {
  throw "skills source not found: $source"
}

foreach($t in $targets){
  New-Item -ItemType Directory -Force -Path $t | Out-Null
  $mode = if ($DryRun) { "/L" } else { $null }
  robocopy $source $t /MIR /R:1 /W:1 /NFL /NDL /NJH /NJS /NP $mode | Out-Null
}
Write-Output ($(if ($DryRun) { "skills sync dry-run complete" } else { "skills synced" }))
