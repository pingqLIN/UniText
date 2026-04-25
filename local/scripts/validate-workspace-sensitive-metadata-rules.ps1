param()

$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path
$libPath = Join-Path $PSScriptRoot "lib\\workspace-sensitive-metadata.ps1"
. $libPath

$rules = Get-WorkspaceSensitiveMetadataRules -RootPath $root
$result = Test-WorkspaceSensitiveMetadataRules -Rules $rules -RootPath $root -RequireScopeExists
$missingScopeEntries = @($result.errors | Where-Object { $_ -like "shared_surface_scope entry is missing from root:*" } | ForEach-Object {
  $_.Substring("shared_surface_scope entry is missing from root: ".Length)
})

[pscustomobject]@{
  rules_path = Join-Path $root "WORKSPACE_SENSITIVE_METADATA_RULES.json"
  shared_surface_scope_count = @($rules.shared_surface_scope).Count
  path_rule_count = @($rules.path_rules).Count
  content_pattern_count = @($rules.content_patterns).Count
  self_test_case_count = @($rules.self_test_cases).Count
  missing_shared_surface_scope = $missingScopeEntries
  errors = @($result.errors)
  ok = [bool]$result.ok
}
