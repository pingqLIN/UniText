param(
  [string]$Root = ".",
  [switch]$AsJson
)

$ErrorActionPreference = "Stop"

function Resolve-PythonInvocation {
  $candidates = @()

  if (-not [string]::IsNullOrWhiteSpace($env:ProgramFiles)) {
    $candidates += @{ Path = (Join-Path $env:ProgramFiles "Python311\python.exe"); Args = @() }
  }
  if (-not [string]::IsNullOrWhiteSpace($env:WINDIR)) {
    $candidates += @{ Path = (Join-Path $env:WINDIR "py.exe"); Args = @("-3") }
  }
  $candidates += @{ Path = (Get-Command python -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source -ErrorAction SilentlyContinue); Args = @() }
  $candidates += @{ Path = (Get-Command py -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source -ErrorAction SilentlyContinue); Args = @("-3") }
  if (-not [string]::IsNullOrWhiteSpace($env:LOCALAPPDATA)) {
    $candidates += @{ Path = (Join-Path $env:LOCALAPPDATA "Microsoft\WindowsApps\python.exe"); Args = @() }
    $candidates += @{ Path = (Join-Path $env:LOCALAPPDATA "Microsoft\WindowsApps\py.exe"); Args = @("-3") }
  }

  foreach ($candidate in $candidates) {
    $path = $candidate.Path
    if (-not [string]::IsNullOrWhiteSpace($path) -and (Test-Path -LiteralPath $path)) {
      return ,@($path) + $candidate.Args
    }
  }

  throw "Python interpreter not found for catalog generation."
}

function Test-SkillHasMinimumMetadata {
  param(
    [string]$SkillFile
  )

  if (-not (Test-Path -LiteralPath $SkillFile)) {
    return $false
  }

  $content = Get-Content -LiteralPath $SkillFile -Raw -ErrorAction SilentlyContinue
  if ([string]::IsNullOrWhiteSpace($content)) {
    return $false
  }

  return $content -match '^(?:\uFEFF)?---' -and $content -match '(?m)^name:\s*\S+' -and $content -match '(?m)^description:\s*\S+'
}

$repo = (Resolve-Path $Root).Path
$skillsRoot = Join-Path $repo "registry\skills"
$scriptRepo = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$validator = Join-Path $repo "registry\skills\skill-creator\scripts\quick_validate.py"
$fallbackValidator = Join-Path $scriptRepo "registry\skills\skill-creator\scripts\quick_validate.py"
$catalogExclusionsPath = Join-Path $repo "registry\catalog-exclusions.json"

if (-not (Test-Path -LiteralPath $skillsRoot)) {
  throw "registry/skills not found under root: $repo"
}
if (-not (Test-Path -LiteralPath $validator)) {
  if (Test-Path -LiteralPath $fallbackValidator) {
    $validator = $fallbackValidator
  } else {
    throw "quick_validate.py not found under root: $repo"
  }
}

$catalogExclusions = @{}
if (Test-Path -LiteralPath $catalogExclusionsPath) {
  $catalogExclusions = Get-Content -LiteralPath $catalogExclusionsPath -Raw | ConvertFrom-Json
}
$excludedSkills = @{}
if ($catalogExclusions -and $catalogExclusions.PSObject.Properties["skills"]) {
  foreach ($entry in $catalogExclusions.skills.PSObject.Properties) {
    $excludedSkills[$entry.Name] = $entry.Value
  }
}

$pythonArgs = Resolve-PythonInvocation

$validatorArgs = @()
if ($pythonArgs.Count -gt 1) {
  $validatorArgs += $pythonArgs[1..($pythonArgs.Count - 1)]
}

$entries = @()
foreach ($skill in Get-ChildItem -LiteralPath $skillsRoot -Directory | Sort-Object Name) {
  if ($excludedSkills.ContainsKey($skill.Name)) {
    continue
  }

  $skillFile = Join-Path $skill.FullName "SKILL.md"
  $isValid = $false

  $result = & $pythonArgs[0] @($validatorArgs + @($validator, $skill.FullName, "--json")) 2>$null
  if ($LASTEXITCODE -eq 0 -or $LASTEXITCODE -eq 1) {
    try {
      $parsed = $result | ConvertFrom-Json
      $isValid = [bool]$parsed.ok
    } catch {
      $isValid = $false
    }
  }

  if (-not $isValid) {
    $isValid = Test-SkillHasMinimumMetadata -SkillFile $skillFile
  }

  if (-not $isValid) {
    continue
  }

  $entries += [pscustomobject]@{
    id = $skill.Name
    type = "skills"
    canonical_location = "/registry/skills/$($skill.Name)"
    status = "active"
    source_of_truth = "/registry/skills/$($skill.Name)/SKILL.md"
    supported_clis = "claude, codex, gemini"
    delivery_guidance = "Use the skills adapter; resolved mode depends on CLI capabilities and local environment."
  }
}

if ($AsJson) {
  ConvertTo-Json -InputObject @($entries) -Depth 4
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
