param(
  [string]$Topic = "document",
  [string]$CandidatePath,
  [switch]$CanonicalSharedTruth,
  [switch]$DescribesSingleWorkspace,
  [switch]$GeneratedState,
  [switch]$DraftOrReviewNote,
  [ValidateSet("root-doc", "registry-reference", "registry-workflow")]
  [string]$SharedForm = "root-doc"
)

$ErrorActionPreference = "Stop"

function Convert-ToKebabCase {
  param([string]$Value)

  $normalized = ($Value -replace '[^A-Za-z0-9]+', '-').Trim('-').ToLowerInvariant()
  if ([string]::IsNullOrWhiteSpace($normalized)) {
    return "document"
  }

  return $normalized
}

function Convert-ToUpperSnakeCase {
  param([string]$Value)

  $normalized = ($Value -replace '[^A-Za-z0-9]+', '_').Trim('_').ToUpperInvariant()
  if ([string]::IsNullOrWhiteSpace($normalized)) {
    return "DOCUMENT"
  }

  return $normalized
}

function Normalize-RepoPath {
  param([string]$Path)

  if ([string]::IsNullOrWhiteSpace($Path)) {
    return $null
  }

  return ($Path -replace '\\', '/').TrimStart('./')
}

function New-Recommendation {
  param(
    [string]$Classification,
    [string]$RecommendedLocation,
    [bool]$Tracked,
    [bool]$ShareSafe,
    [string]$Rationale,
    [string[]]$Notes
  )

  $normalizedCandidate = Normalize-RepoPath -Path $CandidatePath
  $matchesCandidate = $null

  if ($normalizedCandidate) {
    $prefix = Normalize-RepoPath -Path $RecommendedLocation
    $matchesCandidate = $normalizedCandidate.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)
  }

  [pscustomobject]@{
    topic = $Topic
    authorship_window_is_primary_rule = $false
    classification = $Classification
    shared_form = if ($Classification -eq "shared-canonical") { $SharedForm } else { $null }
    recommended_location = $RecommendedLocation
    tracked = $Tracked
    share_safe = $ShareSafe
    candidate_path = $normalizedCandidate
    candidate_path_matches_recommendation = $matchesCandidate
    rationale = $Rationale
    notes = @($Notes)
  }
}

$classificationCount = @(
  [bool]$CanonicalSharedTruth
  [bool]$DescribesSingleWorkspace
  [bool]$GeneratedState
) | Where-Object { $_ } | Measure-Object | Select-Object -ExpandProperty Count

if ($classificationCount -ne 1) {
  throw "Choose exactly one primary classification: -CanonicalSharedTruth, -DescribesSingleWorkspace, or -GeneratedState."
}

if ($DraftOrReviewNote -and -not $DescribesSingleWorkspace) {
  throw "-DraftOrReviewNote requires -DescribesSingleWorkspace."
}

$topicKebab = Convert-ToKebabCase -Value $Topic
$topicUpperSnake = Convert-ToUpperSnakeCase -Value $Topic
$commonNotes = @(
  "Classify by document role and audience, not by the window where the file was edited.",
  "If you need both shared sanitized guidance and live local state, create a pair instead of mixing them into one file."
)

if ($GeneratedState) {
  return (New-Recommendation `
    -Classification "generated-state" `
    -RecommendedLocation ("ops/{0}/" -f $topicKebab) `
    -Tracked $false `
    -ShareSafe $false `
    -Rationale "Generated audit trails, drift reports, export outputs, and other stateful artifacts belong under ops/. They are evidence, not canonical source." `
    -Notes $commonNotes)
}

if ($DescribesSingleWorkspace) {
  if ($DraftOrReviewNote) {
    return (New-Recommendation `
      -Classification "authoring-draft" `
      -RecommendedLocation ("local/docs/authoring/{0}.md" -f $topicKebab) `
      -Tracked $false `
      -ShareSafe $false `
      -Rationale "Drafts, review notes, and authoring workboards stay in ignored local authoring space even when the topic is governance or architecture." `
      -Notes $commonNotes)
  }

  return (New-Recommendation `
    -Classification "single-workspace-live" `
    -RecommendedLocation ("local/docs/{0}_WORKSPACE_BASELINE.md" -f $topicUpperSnake) `
    -Tracked $false `
    -ShareSafe $false `
    -Rationale "If the document describes the current state of one authoring workspace or machine-local wiring, keep it in local/docs/ rather than the tracked shared layer." `
    -Notes @(
      $commonNotes
      "Use *_LIVE.md for active operational checklists and *_WORKSPACE_BASELINE.md for baseline snapshots."
    ))
}

$sharedLocation = switch ($SharedForm) {
  "registry-reference" { "registry/.../references/{0}.md" -f $topicKebab }
  "registry-workflow" { "registry/workflow/{0}/WORKFLOW.md" -f $topicKebab }
  default { "{0}.md" -f $topicKebab }
}

return (New-Recommendation `
  -Classification "shared-canonical" `
  -RecommendedLocation $sharedLocation `
  -Tracked $true `
  -ShareSafe $true `
  -Rationale "Canonical shared truth should live in the tracked shared layer and remain template-safe. The fact that it was authored inside UniText does not make it local-only." `
  -Notes @(
    $commonNotes
    "Use root docs for repo-wide policy/spec, registry references for sanitized domain references, and registry workflow for shared runbooks."
    "Tracked shared placement still does not imply publish permission."
  ))
