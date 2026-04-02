param()

$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path
$boundaryScript = Join-Path $PSScriptRoot "verify-workspace-boundaries.ps1"

if (-not (Test-Path -LiteralPath $boundaryScript)) {
  throw "Boundary verification script not found: $boundaryScript"
}

$branch = (& git -C $root branch --show-current).Trim()
$unstaged = @((& git -C $root diff --name-only) | Where-Object { $_ })
$staged = @((& git -C $root diff --cached --name-only) | Where-Object { $_ })
$untracked = @((& git -C $root ls-files --others --exclude-standard) | Where-Object { $_ })
$changed = @($unstaged + $staged + $untracked | Sort-Object -Unique)
$boundary = & $boundaryScript

$localOnlyChanges = @($changed | Where-Object {
  $_ -match '^local/docs/authoring/' -or
  $_ -match '^local/docs/.+_LIVE\.md$' -or
  $_ -match '^local/docs/.+_WORKSPACE_BASELINE\.md$'
})

$opsChanges = @($changed | Where-Object { $_ -match '^ops/' })
$sharedChanges = @($changed | Where-Object {
  $_ -notmatch '^ops/' -and
  $_ -notmatch '^local/docs/authoring/' -and
  $_ -notmatch '^local/docs/.+_LIVE\.md$' -and
  $_ -notmatch '^local/docs/.+_WORKSPACE_BASELINE\.md$'
})

[pscustomobject]@{
  branch = $branch
  no_publish_permission_required = $true
  working_tree_clean = ($changed.Count -eq 0)
  changed_paths = $changed
  local_only_changes = $localOnlyChanges
  ops_changes = $opsChanges
  shared_surface_changes = $sharedChanges
  boundary_ok = [bool]$boundary.ok
  boundary_path_violations = @($boundary.path_violations)
  boundary_content_violations = @($boundary.content_violations)
  structurally_publishable_if_permission_is_granted = [bool]$boundary.ok -and ($changed.Count -eq 0) -and ($localOnlyChanges.Count -eq 0) -and ($opsChanges.Count -eq 0)
}
