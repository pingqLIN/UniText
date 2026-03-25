param(
  [string]$Source = ".bak_20260315_00\\skills.bak.20260228_215107"
)

$ErrorActionPreference = "Stop"

$root = (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path
$skillsRoot = (Resolve-Path $Source).Path
$validator = Join-Path $root "registry\skills\skill-creator\scripts\quick_validate.py"

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
  $py = Get-Command py -ErrorAction SilentlyContinue
  if (-not $py) {
    throw "Python interpreter not found for skill validation."
  }
  $pythonArgs = @($py.Path, "-3")
} else {
  $pythonArgs = @($python.Path)
}

$validatorArgs = @()
if ($pythonArgs.Count -gt 1) {
  $validatorArgs += $pythonArgs[1..($pythonArgs.Count - 1)]
}

Get-ChildItem -LiteralPath $skillsRoot -Directory | Where-Object {
  $_.Name -notlike ".*" -and $_.Name -notlike "_*" -and $_.Name -notlike "*Copy*"
} | ForEach-Object {
  $skill = $_
  $file = Join-Path $skill.FullName "SKILL.md"
  $body = if (Test-Path -LiteralPath $file) { Get-Content -LiteralPath $file -Raw } else { "" }
  $hasFrontmatter = $body.StartsWith("---")
  $name = if ($body -match "(?m)^name:\s*(.+)$") { $Matches[1].Trim("`r", '"', ' ') } else { $null }
  $description = if ($body -match "(?m)^description:\s*(.+)$") { $Matches[1].Trim("`r", '"', ' ') } else { $null }

  $result = & $pythonArgs[0] @($validatorArgs + @($validator, $skill.FullName, "--json")) 2>$null
  $parsed = if ($LASTEXITCODE -eq 0 -or $LASTEXITCODE -eq 1) { $result | ConvertFrom-Json } else { [pscustomobject]@{ ok = $false; message = "validator execution failed" } }

  [pscustomobject]@{
    id = $skill.Name
    has_skill_md = Test-Path -LiteralPath $file
    has_frontmatter = $hasFrontmatter
    name = $name
    has_description = [bool]$description
    validation_ok = [bool]$parsed.ok
    validation_message = $parsed.message
    canonical_location = "/registry/skills/$($skill.Name)"
    adoption_ready = [bool]$parsed.ok
  }
} | Sort-Object id
