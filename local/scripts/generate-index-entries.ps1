param(
  [string]$Root = ".",
  [switch]$AsJson
)

$ErrorActionPreference = "Stop"

$repo = (Resolve-Path $Root).Path
$skillsRoot = Join-Path $repo "registry\skills"
$validator = Join-Path $repo "registry\skills\skill-creator\scripts\quick_validate.py"
$catalogExclusionsPath = Join-Path $repo "registry\catalog-exclusions.json"

if (-not (Test-Path -LiteralPath $skillsRoot)) {
  throw "registry/skills not found under root: $repo"
}
if (-not (Test-Path -LiteralPath $validator)) {
  throw "quick_validate.py not found under root: $repo"
}

$catalogExclusions = @{}
if (Test-Path -LiteralPath $catalogExclusionsPath) {
  $catalogExclusions = Get-Content -LiteralPath $catalogExclusionsPath -Raw | ConvertFrom-Json -AsHashtable
}
$excludedSkills = @{}
if ($catalogExclusions.ContainsKey("skills") -and $catalogExclusions.skills -is [hashtable]) {
  $excludedSkills = $catalogExclusions.skills
}

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
  $py = Get-Command py -ErrorAction SilentlyContinue
  if (-not $py) {
    throw "Python interpreter not found for catalog generation."
  }
  $pythonArgs = @($py.Path, "-3")
} else {
  $pythonArgs = @($python.Path)
}

$validatorArgs = @()
if ($pythonArgs.Count -gt 1) {
  $validatorArgs += $pythonArgs[1..($pythonArgs.Count - 1)]
}

$entries = @()
foreach ($skill in Get-ChildItem -LiteralPath $skillsRoot -Directory | Sort-Object Name) {
  if ($excludedSkills.ContainsKey($skill.Name)) {
    continue
  }

  $result = & $pythonArgs[0] @($validatorArgs + @($validator, $skill.FullName, "--json")) 2>$null
  if (-not ($LASTEXITCODE -eq 0 -or $LASTEXITCODE -eq 1)) {
    continue
  }
  $parsed = $result | ConvertFrom-Json
  if (-not $parsed.has_skill_md -or -not $parsed.ok) {
    continue
  }

  $entries += [pscustomobject]@{
    id = if ($parsed.id) { $parsed.id } else { $skill.Name }
    type = "skills"
    canonical_location = if ($parsed.canonical_location) { $parsed.canonical_location } else { "/registry/skills/$($skill.Name)" }
    status = "active"
    source_of_truth = "/registry/skills/$($skill.Name)/SKILL.md"
    supported_clis = "claude, codex, gemini"
    delivery_guidance = "Use the skills adapter; resolved mode depends on CLI capabilities and local environment."
  }
}

if ($AsJson) {
  $entries | ConvertTo-Json -Depth 4
  return
}

foreach ($entry in $entries) {
  @(
    "| Field | Value |"
    "|---|---|"
    "| ``id`` | ``$($entry.id)`` |"
    "| ``type`` | ``$($entry.type)`` |"
    "| ``canonical_location`` | ``$($entry.canonical_location)`` |"
    "| ``status`` | ``$($entry.status)`` |"
    "| ``source_of_truth`` | ``$($entry.source_of_truth)`` |"
    "| ``supported_clis`` | ``$($entry.supported_clis)`` |"
    "| ``delivery_guidance`` | ``$($entry.delivery_guidance)`` |"
    ""
  )
}
