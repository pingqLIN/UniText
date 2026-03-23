param(
  [string]$Source = ".bak_20260315_00\\skills.bak.20260228_215107"
)

$ErrorActionPreference = "Stop"
$root = Resolve-Path $Source

Get-ChildItem $root -Directory | Where-Object {
  $_.Name -notlike ".*" -and $_.Name -notlike "_*" -and $_.Name -notlike "*Copy*"
} | ForEach-Object {
  $skill = $_
  $file = Join-Path $skill.FullName "SKILL.md"
  $body = if (Test-Path $file) { Get-Content $file -Raw } else { "" }
  $hasFrontmatter = $body.StartsWith("---")
  $name = if ($body -match "(?m)^name:\s*(.+)$") { $Matches[1].Trim("`r", '"', ' ') } else { $null }
  $description = if ($body -match "(?m)^description:\s*(.+)$") { $Matches[1].Trim("`r", '"', ' ') } else { $null }

  [pscustomobject]@{
    id = $skill.Name
    has_skill_md = Test-Path $file
    has_frontmatter = $hasFrontmatter
    name = $name
    has_description = [bool]$description
    canonical_location = "/registry/skills/$($skill.Name)"
    adoption_ready = (Test-Path $file) -and $hasFrontmatter -and [bool]$name -and [bool]$description
  }
} | Sort-Object id
