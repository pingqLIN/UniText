param(
  [string]$Source = ""
)

$ErrorActionPreference = "Stop"
$root = Resolve-Path (Join-Path $PSScriptRoot "..\\..")
$resolvedSource = if ($Source) { (Resolve-Path $Source).Path } else { (Join-Path $root "registry\skills") }
$expectedSuffix = [IO.Path]::Combine("registry", "skills")
$targets = @(
  "$HOME\\.claude\\skills",
  "$HOME\\.gemini\\skills",
  "$HOME\\.agents\\skills"
)

$report = @()
$report += [pscustomobject]@{
  path = $resolvedSource
  kind = "source"
  exists = Test-Path $resolvedSource
  attrs = if (Test-Path $resolvedSource) { (Get-Item $resolvedSource).Attributes.ToString() } else { $null }
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
    expected_target = $expectedSuffix
    matches_expected = if ($item -and $item.LinkType) { $item.Target -like "*$expectedSuffix" } else { $null }
  }
}

$report
