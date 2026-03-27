param(
  [string]$Root = ""
)

$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "lib\path-safety.ps1")

$root = if ($Root) {
  Resolve-PortablePath -Path $Root
} else {
  Resolve-PortablePath -Path (Join-Path $PSScriptRoot "..\\..")
}
$skills = Get-ChildItem (Join-Path $root "registry\skills") -Directory | Sort-Object Name

foreach ($skill in $skills) {
  $file = Join-Path $skill.FullName "SKILL.md"
  if (-not (Test-Path $file)) {
    continue
  }

  @(
    "| Field | Value |"
    "|---|---|"
    "| ``id`` | ``$($skill.Name)`` |"
    "| ``type`` | ``skills`` |"
    "| ``canonical_location`` | ``/registry/skills/$($skill.Name)`` |"
    "| ``status`` | ``active`` |"
    "| ``source_of_truth`` | ``/registry/skills/$($skill.Name)/SKILL.md`` |"
    "| ``supported_clis`` | ``claude, codex, gemini`` |"
    "| ``delivery_guidance`` | ``Use the skills adapter; resolved mode depends on CLI capabilities and local environment.`` |"
    ""
  )
}
