param()

$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path
$boundaryScript = Join-Path $PSScriptRoot "verify-workspace-boundaries.ps1"
$placementScript = Join-Path $PSScriptRoot "get-document-placement-recommendation.ps1"

if (-not (Test-Path -LiteralPath $boundaryScript)) {
  throw "Boundary verification script not found: $boundaryScript"
}

if (-not (Test-Path -LiteralPath $placementScript)) {
  throw "Document placement helper not found: $placementScript"
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

$documentPlacementObservations = @(
  $changed |
    Where-Object { $_ -match '\.md$' } |
    ForEach-Object { & $placementScript -CandidatePath $_ -InferFromCandidatePath }
)

$documentPlacementManualReview = @(
  $documentPlacementObservations |
    Where-Object { $_.classification -eq "manual-review" }
)

$documentPlacementMismatches = @(
  $documentPlacementObservations |
    Where-Object { $_.candidate_path_matches_recommendation -eq $false }
)

[pscustomobject]@{
  branch = $branch
  no_publish_permission_required = $true
  working_tree_clean = ($changed.Count -eq 0)
  changed_paths = $changed
  local_only_changes = $localOnlyChanges
  ops_changes = $opsChanges
  shared_surface_changes = $sharedChanges
  document_placement_observations = $documentPlacementObservations
  document_placement_manual_review = $documentPlacementManualReview
  document_placement_mismatches = $documentPlacementMismatches
  boundary_ok = [bool]$boundary.ok
  boundary_rules_ok = [bool]$boundary.rules_ok
  boundary_rule_errors = @($boundary.rules_errors)
  boundary_path_violations = @($boundary.path_violations)
  boundary_content_violations = @($boundary.content_violations)
  structurally_publishable_if_permission_is_granted = [bool]$boundary.ok -and ($changed.Count -eq 0) -and ($localOnlyChanges.Count -eq 0) -and ($opsChanges.Count -eq 0)
}
