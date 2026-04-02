param(
  [ValidateSet("repo", "root", "registry", "i18n", "local", "template")]
  [string[]]$Scope = @("repo"),
  [int]$SampleSize = 40,
  [int]$MaxFiles = 200,
  [switch]$Apply,
  [switch]$Force
)

$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path

$scopeMap = [ordered]@{
  repo = @(".")
  root = @(
    ".gitattributes",
    ".gitignore",
    ".mcp.json",
    ".claude",
    "README.md",
    "INDEX.md",
    "VISION.md",
    "RESOURCE_SPEC.md",
    "OPERATIONS.md",
    "PROJECT_MODES.md",
    "WORKSPACE_SENSITIVE_METADATA_RULES.json",
    "WORKSPACE_SENSITIVE_METADATA_RULES.md",
    "DOCUMENT_PLACEMENT_POLICY.md",
    "SECRET_HANDLING_GUIDELINES.md",
    "MILESTONES.md",
    "BOUNDARY_INCIDENT_REVIEW_TEMPLATE.md",
    "TEMPLATE_RELEASE_PACKAGE.md",
    "TEMPLATE_RELEASE_CHECKLIST.md",
    "REBUILD_AS_NEW_PROJECT.md",
    "NO_PUBLISH_POLICY.md",
    "COPILOT_CLI_ADAPTER_NOTE.md"
  )
  registry = @("registry")
  i18n = @("i18n")
  local = @("local")
  template = @("template")
}

$selectedScopes = @($Scope | Select-Object -Unique)
$targets = @($selectedScopes | ForEach-Object {
  if (-not $scopeMap.Contains($_)) {
    throw "Unsupported scope: $_"
  }
  $scopeMap[$_]
} | Select-Object -Unique)

$previewArgs = @("-C", $root, "add", "-n", "--renormalize", "--") + $targets
$previewOutput = @((& git @previewArgs 2>&1))
if ($LASTEXITCODE -ne 0) {
  throw "git add --renormalize preview failed: $($previewOutput -join [Environment]::NewLine)"
}

$previewLines = @($previewOutput | Where-Object { $_ -match "^add '" })
$paths = @($previewLines | ForEach-Object {
  if ($_ -match "^add '(.+)'$") {
    $Matches[1]
  }
})

if ($Apply -and $paths.Count -gt $MaxFiles -and -not $Force) {
  throw "Renormalize would touch $($paths.Count) files, which exceeds MaxFiles=$MaxFiles. Re-run with -Force or narrow -Scope."
}

$stagedPaths = @()
if ($Apply -and $paths.Count -gt 0) {
  $applyArgs = @("-C", $root, "add", "--renormalize", "--") + $targets
  $applyOutput = @((& git @applyArgs 2>&1))
  if ($LASTEXITCODE -ne 0) {
    throw "git add --renormalize apply failed: $($applyOutput -join [Environment]::NewLine)"
  }
  $stagedPaths = @((& git -C $root diff --cached --name-only -- @targets) | Where-Object { $_ })
}

[pscustomobject]@{
  repo_root = $root
  scope = $selectedScopes
  target_paths = $targets
  line_ending_policy_present = Test-Path (Join-Path $root ".gitattributes")
  apply_mode = [bool]$Apply
  forced = [bool]$Force
  max_files_guard = $MaxFiles
  renormalize_candidate_count = $paths.Count
  sample_paths = @($paths | Select-Object -First $SampleSize)
  staged_paths = $stagedPaths
  ok = $true
}
