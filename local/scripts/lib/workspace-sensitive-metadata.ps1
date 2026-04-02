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

  if (-not $rules.self_test_cases) {
    throw "Rules file is missing self_test_cases."
  }

  return $rules
}

function Test-WorkspaceSensitiveMetadataRules {
  param(
    [object]$Rules
  )

  $errors = [System.Collections.Generic.List[string]]::new()

  if (@($Rules.shared_surface_scope).Count -eq 0) {
    $errors.Add("shared_surface_scope must not be empty.")
  }

  $pathLabels = @($Rules.path_rules | ForEach-Object { $_.label })
  if (($pathLabels | Sort-Object | Get-Unique).Count -ne $pathLabels.Count) {
    $errors.Add("path_rules labels must be unique.")
  }

  $contentLabels = @($Rules.content_patterns | ForEach-Object { $_.label })
  if (($contentLabels | Sort-Object | Get-Unique).Count -ne $contentLabels.Count) {
    $errors.Add("content_patterns labels must be unique.")
  }

  foreach ($rule in @($Rules.path_rules)) {
    try {
      [void][regex]::new($rule.regex)
    } catch {
      $errors.Add("Invalid path rule regex for '$($rule.label)': $($rule.regex)")
    }
  }

  foreach ($pattern in @($Rules.content_patterns)) {
    try {
      [void][regex]::new($pattern.regex)
    } catch {
      $errors.Add("Invalid content pattern regex for '$($pattern.label)': $($pattern.regex)")
    }

    if ($null -eq $pattern.skip_script_pattern_lines) {
      $errors.Add("content pattern '$($pattern.label)' must define skip_script_pattern_lines.")
    }
  }

  foreach ($case in @($Rules.self_test_cases)) {
    $expected = @($case.expected_labels)
    $actual = @($Rules.content_patterns | Where-Object {
      $case.sample -match $_.regex
    } | ForEach-Object { $_.label } | Sort-Object -Unique)
    $expectedSorted = @($expected | Sort-Object -Unique)

    if (@(Compare-Object -ReferenceObject $expectedSorted -DifferenceObject $actual).Count -gt 0) {
      $errors.Add("self_test_case '$($case.label)' mismatch. expected=[$($expectedSorted -join ', ')] actual=[$($actual -join ', ')]")
    }
  }

  return [pscustomobject]@{
    ok = ($errors.Count -eq 0)
    errors = @($errors)
  }
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
        if ($file -match 'WORKSPACE_SENSITIVE_METADATA_RULES\.json$' -and $match.Line -match '(?i)"sample"\s*:') {
          continue
        }

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
