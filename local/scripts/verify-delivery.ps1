param(
  [string]$Source = "Q:\\UniText\\registry\\skills"
)

$ErrorActionPreference = "Stop"
$targets = @(
  "$HOME\\.claude\\skills",
  "$HOME\\.gemini\\skills",
  "$HOME\\.agents\\skills"
)

$report = @()
$report += [pscustomobject]@{
  path = $Source
  kind = "source"
  exists = Test-Path $Source
  attrs = if (Test-Path $Source) { (Get-Item $Source).Attributes.ToString() } else { $null }
  target = $null
}

$report += [pscustomobject]@{
  path = "$HOME\\.codex\\config.toml"
  kind = "codex-config"
  exists = Test-Path "$HOME\\.codex\\config.toml"
  attrs = if (Test-Path "$HOME\\.codex\\config.toml") { (Get-Item "$HOME\\.codex\\config.toml").Attributes.ToString() } else { $null }
  target = $null
}

foreach ($path in $targets) {
  $exists = Test-Path $path
  $item = if ($exists) { Get-Item $path -Force } else { $null }
  $report += [pscustomobject]@{
    path = $path
    kind = "target"
    exists = $exists
    attrs = if ($item) { $item.Attributes.ToString() } else { $null }
    target = if ($item -and $item.LinkType) { $item.Target } else { $null }
    expected_target = $Source
    matches_expected = if ($item -and $item.LinkType) { $item.Target -eq $Source } else { $null }
  }
}

$report
