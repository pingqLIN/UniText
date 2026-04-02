param(
  [int]$SampleSize = 40
)

$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path
$output = @((& git -C $root add -n --renormalize . 2>&1))
if ($LASTEXITCODE -ne 0) {
  throw "git add --renormalize preview failed: $($output -join [Environment]::NewLine)"
}

$lines = @($output | Where-Object { $_ -match "^add '" })
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
