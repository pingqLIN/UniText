param(
  [string]$Source = "registry\\skills",
  [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$targets = @(
  "$HOME\\.claude\\skills",
  "$HOME\\.gemini\\skills"
)

foreach ($target in $targets) {
  [pscustomobject]@{
    source = $Source
    target = $target
    dry_run = $DryRun.IsPresent
    note = "Replace this starter script with the delivery mode and safety checks you need."
  }
}
