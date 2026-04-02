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
  $_ -match '^registry/' -or
  $_ -match '^README\.md$' -or
  $_ -match '^INDEX\.md$' -or
  $_ -match '^OPERATIONS\.md$' -or
  $_ -match '^PROJECT_MODES\.md$' -or
  $_ -match '^SECRET_HANDLING_GUIDELINES\.md$' -or
  $_ -match '^TEMPLATE_RELEASE_PACKAGE\.md$' -or
  $_ -match '^TEMPLATE_RELEASE_CHECKLIST\.md$' -or
  $_ -match '^REBUILD_AS_NEW_PROJECT\.md$' -or
  $_ -match '^DOCUMENT_PLACEMENT_POLICY\.md$' -or
  $_ -match '^BOUNDARY_INCIDENT_REVIEW_TEMPLATE\.md$' -or
  $_ -match '^NO_PUBLISH_POLICY\.md$'
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
  structurally_publishable_if_permission_is_granted = [bool]$boundary.ok -and ($localOnlyChanges.Count -eq 0) -and ($opsChanges.Count -eq 0)
}
