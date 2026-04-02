function Get-WorkspaceSensitiveMetadataRules {
  param(
    [string]$RootPath
  )

  $rulesPath = Join-Path $RootPath "WORKSPACE_SENSITIVE_METADATA_RULES.json"
  if (-not (Test-Path -LiteralPath $rulesPath)) {
    throw "Workspace-sensitive metadata rules file not found: $rulesPath"
  }

  $rules = Get-Content -LiteralPath $rulesPath -Raw | ConvertFrom-Json
  if (-not $rules.shared_surface_scope) {
    throw "Rules file is missing shared_surface_scope."
  }

  if (-not $rules.path_rules) {
    throw "Rules file is missing path_rules."
  }

  if (-not $rules.content_patterns) {
    throw "Rules file is missing content_patterns."
  }

  return $rules
}

function Find-WorkspaceSensitivePathViolations {
  param(
    [string[]]$TrackedFiles,
    [object[]]$PathRules
  )

  foreach ($file in $TrackedFiles) {
    foreach ($rule in $PathRules) {
      if ($file -match $rule.regex) {
        [pscustomobject]@{
          path = $file
          label = $rule.label
        }
      }
    }
  }
}

function Find-WorkspaceSensitiveContentViolations {
  param(
    [string]$RootPath,
    [string[]]$Files,
    [object[]]$ContentPatterns
  )

  foreach ($file in $Files) {
    $absolutePath = Join-Path $RootPath $file
    foreach ($pattern in $ContentPatterns) {
      $matches = Select-String -LiteralPath $absolutePath -Pattern $pattern.regex -AllMatches
      foreach ($match in $matches) {
        if ($pattern.skip_script_pattern_lines -and $file -match '\.(ps1|py)$' -and $match.Line -match '(?i)\b(regex|pattern|contentpatterns?)\b') {
          continue
        }

        [pscustomobject]@{
          path = $file
          label = $pattern.label
          line = $match.LineNumber
          text = $match.Line.Trim()
        }
      }
    }
  }
}
