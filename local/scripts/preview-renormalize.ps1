param(
  [int]$SampleSize = 40
)

$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path
$lines = @((& git -C $root add -n --renormalize .) | Where-Object { $_ -match "^add '" })
$paths = @($lines | ForEach-Object {
  if ($_ -match "^add '(.+)'$") {
    $Matches[1]
  }
})
$groups = @($paths | Group-Object {
  if ($_ -match "^[^/\\]+") {
    $Matches[0]
    return
  }
  "."
} | Sort-Object Count -Descending | ForEach-Object {
  [pscustomobject]@{
    scope = $_.Name
    count = $_.Count
  }
})

[pscustomobject]@{
  repo_root = $root
  line_ending_policy_present = Test-Path (Join-Path $root ".gitattributes")
  renormalize_candidate_count = $paths.Count
  top_level_scopes = $groups
  sample_paths = @($paths | Select-Object -First $SampleSize)
  ok = $true
}
