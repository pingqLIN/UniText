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
  $result = & $pythonArgs[0] @($validatorArgs + @($validator, $skill.FullName, "--metadata-json")) 2>$null
  $parsed = if ($LASTEXITCODE -eq 0 -or $LASTEXITCODE -eq 1) { $result | ConvertFrom-Json } else { [pscustomobject]@{ ok = $false; message = "validator execution failed" } }
  $frontmatter = $parsed.frontmatter
  $name = if ($frontmatter -and $frontmatter.name) { $frontmatter.name } else { $null }
  $description = if ($frontmatter -and $frontmatter.description) { $frontmatter.description } else { $null }
  $license = if ($frontmatter -and $frontmatter.license) { $frontmatter.license } else { $null }
  $source = if ($frontmatter -and $frontmatter.source) { $frontmatter.source } else { $null }
  $category = if ($frontmatter -and $frontmatter.category) { $frontmatter.category } else { $null }
  $tags = if ($frontmatter -and $frontmatter.tags) { $frontmatter.tags } else { $null }
  $risk = if ($frontmatter -and $frontmatter.risk) { $frontmatter.risk } else { $null }
  $dateAdded = if ($frontmatter -and $frontmatter.date_added) { $frontmatter.date_added } else { $null }

  [pscustomobject]@{
    id = $skill.Name
    has_skill_md = [bool]$parsed.skill_md_exists
    has_frontmatter = [bool]$parsed.has_frontmatter
    name = $name
    description = $description
    has_description = [bool]$description
    license = $license
    source = $source
    category = $category
    tags = $tags
    risk = $risk
    date_added = $dateAdded
    validation_ok = [bool]$parsed.ok
    validation_message = $parsed.message
    canonical_location = "/registry/skills/$($skill.Name)"
    adoption_ready = [bool]$parsed.ok
  }
} | Sort-Object id
