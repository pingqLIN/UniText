param(
  [string[]]$Scope
)

$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path
$libPath = Join-Path $PSScriptRoot "lib\\workspace-sensitive-metadata.ps1"
. $libPath
$rules = Get-WorkspaceSensitiveMetadataRules -RootPath $root
$effectiveScope = if ($Scope -and $Scope.Count -gt 0) { $Scope } else { @($rules.shared_surface_scope) }
$tracked = & git -C $root ls-files -- $effectiveScope

if ($LASTEXITCODE -ne 0) {
  throw "git ls-files failed while resolving tracked files for boundary verification."
}

$trackedFiles = @($tracked | Where-Object { $_ })
$pathRules = @($rules.path_rules)
$contentPatterns = @($rules.content_patterns)

$contentFiles = $trackedFiles | Where-Object {
  [IO.Path]::GetExtension($_) -in @(".md", ".json", ".jsonc", ".txt", ".ps1", ".py", ".toml", ".yml", ".yaml")
}

$pathViolations = @(Find-WorkspaceSensitivePathViolations -TrackedFiles $trackedFiles -PathRules $pathRules)
$contentViolations = @(Find-WorkspaceSensitiveContentViolations -RootPath $root -Files $contentFiles -ContentPatterns $contentPatterns)

[pscustomobject]@{
  scanned_scope = $effectiveScope
  scanned_file_count = $trackedFiles.Count
  path_violations = @($pathViolations)
  content_violations = @($contentViolations)
  ok = (@($pathViolations).Count -eq 0) -and (@($contentViolations).Count -eq 0)
}
