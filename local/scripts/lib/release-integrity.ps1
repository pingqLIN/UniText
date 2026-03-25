Set-StrictMode -Version Latest

function Get-TemplatePackageItems {
  return @(
    [pscustomobject]@{ kind = "file"; source = ".gitignore"; target = ".gitignore" },
    [pscustomobject]@{ kind = "file"; source = ".mcp.json"; target = ".mcp.json" },
    [pscustomobject]@{ kind = "file"; source = "README.md"; target = "README.md" },
    [pscustomobject]@{ kind = "file"; source = "INDEX.md"; target = "INDEX.md" },
    [pscustomobject]@{ kind = "file"; source = "VISION.md"; target = "VISION.md" },
    [pscustomobject]@{ kind = "file"; source = "RESOURCE_SPEC.md"; target = "RESOURCE_SPEC.md" },
    [pscustomobject]@{ kind = "file"; source = "OPERATIONS.md"; target = "OPERATIONS.md" },
    [pscustomobject]@{ kind = "file"; source = "PROJECT_MODES.md"; target = "PROJECT_MODES.md" },
    [pscustomobject]@{ kind = "file"; source = "SECRET_HANDLING_GUIDELINES.md"; target = "SECRET_HANDLING_GUIDELINES.md" },
    [pscustomobject]@{ kind = "file"; source = "MILESTONES.md"; target = "MILESTONES.md" },
    [pscustomobject]@{ kind = "file"; source = "TEMPLATE_RELEASE_PACKAGE.md"; target = "TEMPLATE_RELEASE_PACKAGE.md" },
    [pscustomobject]@{ kind = "file"; source = "TEMPLATE_RELEASE_CHECKLIST.md"; target = "TEMPLATE_RELEASE_CHECKLIST.md" },
    [pscustomobject]@{ kind = "file"; source = ".claude\\settings.json"; target = ".claude\\settings.json" },
    [pscustomobject]@{ kind = "file"; source = "template\\examples\\local\\README.md"; target = "local\\README.md" },
    [pscustomobject]@{ kind = "file"; source = "template\\examples\\local\\docs\\PATH_MAP.template.md"; target = "local\\docs\\PATH_MAP.md" },
    [pscustomobject]@{ kind = "file"; source = "local\\scripts\\bootstrap.py"; target = "local\\scripts\\bootstrap.py" },
    [pscustomobject]@{ kind = "file"; source = "local\\scripts\\verify-bootstrap.py"; target = "local\\scripts\\verify-bootstrap.py" },
    [pscustomobject]@{ kind = "file"; source = "local\\scripts\\create-git-bundle.py"; target = "local\\scripts\\create-git-bundle.py" },
    [pscustomobject]@{ kind = "file"; source = "local\\scripts\\sync-skills.ps1"; target = "local\\scripts\\sync-skills.ps1" },
    [pscustomobject]@{ kind = "dir"; source = "template\\examples\\skills\\example-skill"; target = "registry\\skills\\example-skill" },
    [pscustomobject]@{ kind = "dir"; source = "template\\examples\\agents\\example-agent"; target = "registry\\agents\\example-agent" },
    [pscustomobject]@{ kind = "dir"; source = "registry\\mcp\\claude-project-mcp-seed"; target = "registry\\mcp\\claude-project-mcp-seed" },
    [pscustomobject]@{ kind = "dir"; source = "template\\examples\\mcp\\example-mcp"; target = "registry\\mcp\\example-mcp" },
    [pscustomobject]@{ kind = "dir"; source = "template\\examples\\workflow\\example-workflow"; target = "registry\\workflow\\example-workflow" }
  )
}

function Get-ReleaseExclusions {
  return @(
    "backup/",
    "recovered_*/",
    ".bak_*/",
    "ops/history/",
    "ops/review-package/",
    "local/docs/authoring/",
    "review-only docs",
    "machine-local runtime state"
  )
}

function Write-Utf8TextAtomic {
  param(
    [Parameter(Mandatory)][string]$Path,
    [Parameter(Mandatory)][string]$Content
  )

  $parent = Split-Path -Path $Path -Parent
  if ($parent -and -not (Test-Path -LiteralPath $parent)) {
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
  }

  $tempPath = Join-Path $parent ".$([System.IO.Path]::GetFileName($Path)).$([guid]::NewGuid().ToString('N')).tmp"
  $utf8NoBom = [System.Text.UTF8Encoding]::new($false)

  $backupPath = $null

  try {
    [System.IO.File]::WriteAllText($tempPath, $Content, $utf8NoBom)
    if (Test-Path -LiteralPath $Path) {
      $backupPath = Join-Path $parent ".$([System.IO.Path]::GetFileName($Path)).$([guid]::NewGuid().ToString('N')).bak"
      [System.IO.File]::Replace($tempPath, $Path, $backupPath, $false)
      if (Test-Path -LiteralPath $backupPath) {
        Remove-Item -LiteralPath $backupPath -Force -ErrorAction SilentlyContinue
      }
    } else {
      [System.IO.File]::Move($tempPath, $Path)
    }
  } catch {
    if (Test-Path -LiteralPath $tempPath) {
      Remove-Item -LiteralPath $tempPath -Force -ErrorAction SilentlyContinue
    }
    if ($backupPath -and (Test-Path -LiteralPath $backupPath)) {
      Remove-Item -LiteralPath $backupPath -Force -ErrorAction SilentlyContinue
    }
    throw
  }
}

function Write-JsonFileAtomic {
  param(
    [Parameter(Mandatory)][string]$Path,
    [Parameter(Mandatory)]$Value,
    [int]$Depth = 10
  )

  $json = $Value | ConvertTo-Json -Depth $Depth
  Write-Utf8TextAtomic -Path $Path -Content ($json + "`n")
}

function Convert-ToRepoRelativePath {
  param(
    [Parameter(Mandatory)][string]$RepoRoot,
    [Parameter(Mandatory)][string]$Path
  )

  $repo = [System.IO.Path]::GetFullPath($RepoRoot)
  $candidate = [System.IO.Path]::GetFullPath($Path)

  if ($candidate -eq $repo) {
    return "."
  }

  if (-not (Test-IsUnderPath -RootPath $repo -CandidatePath $candidate)) {
    throw "Path is outside repo root: $candidate"
  }

  return $candidate.Substring($repo.Length).TrimStart('\', '/').Replace('\', '/')
}

function Get-GitEvidence {
  param(
    [Parameter(Mandatory)][string]$RepoRoot
  )

  $commit = $null
  $workspaceDirty = $null

  try {
    $commitOutput = & git -C $RepoRoot rev-parse HEAD 2>$null
    if ($LASTEXITCODE -eq 0) {
      $commit = ($commitOutput | Select-Object -First 1).Trim()
    }
  } catch {
  }

  try {
    & git -C $RepoRoot diff --quiet --ignore-submodules HEAD -- 2>$null
    $workspaceDirty = ($LASTEXITCODE -ne 0)
  } catch {
  }

  return [ordered]@{
    source_commit = $commit
    workspace_dirty = $workspaceDirty
  }
}

function Finalize-StagedDirectory {
  param(
    [Parameter(Mandatory)][string]$StagingPath,
    [Parameter(Mandatory)][string]$FinalPath
  )

  if (Test-Path -LiteralPath $FinalPath) {
    throw "Final path already exists: $FinalPath"
  }

  [System.IO.Directory]::Move($StagingPath, $FinalPath)
}

function Test-AbsoluteLikePathString {
  param(
    [AllowNull()][string]$Value
  )

  if ([string]::IsNullOrWhiteSpace($Value)) {
    return $false
  }

  return $Value -match '^(?:[A-Za-z]:[\\/]|/|\\\\)'
}

function Read-JsonFile {
  param(
    [Parameter(Mandatory)][string]$Path
  )

  return Get-Content -LiteralPath $Path -Raw | ConvertFrom-Json
}

function Test-ReleasePackageMetadata {
  param(
    [Parameter(Mandatory)][string]$PackagePath,
    [Parameter(Mandatory)][string]$ExpectedReleaseTarget,
    [Parameter(Mandatory)][string]$ExpectedPhaseTarget,
    [Parameter(Mandatory)][string]$ExpectedReleaseChannel,
    [string]$ExpectedGenerationState = "complete"
  )

  $issues = @()
  $resolvedPath = [System.IO.Path]::GetFullPath($PackagePath)
  $manifest = $null
  $release = $null
  $state = $null

  foreach ($entry in @(
      [pscustomobject]@{ label = "manifest"; path = (Join-Path $resolvedPath "manifest.json") },
      [pscustomobject]@{ label = "release"; path = (Join-Path $resolvedPath "release.json") },
      [pscustomobject]@{ label = "state"; path = (Join-Path $resolvedPath "generation-state.json") }
    )) {
    try {
      $body = Read-JsonFile -Path $entry.path
      switch ($entry.label) {
        "manifest" { $manifest = $body }
        "release" { $release = $body }
        "state" { $state = $body }
      }
    } catch {
      $issues += "$($entry.label).json is missing or invalid."
    }
  }

  foreach ($document in @(
      [pscustomobject]@{ label = "manifest"; value = $manifest },
      [pscustomobject]@{ label = "release"; value = $release },
      [pscustomobject]@{ label = "state"; value = $state }
    )) {
    if ($null -eq $document.value) {
      continue
    }

    if ($document.value.release_target -ne $ExpectedReleaseTarget) {
      $issues += "$($document.label).release_target must be $ExpectedReleaseTarget."
    }
    if ($document.value.phase_target -ne $ExpectedPhaseTarget) {
      $issues += "$($document.label).phase_target must be $ExpectedPhaseTarget."
    }
    if ($document.value.release_channel -ne $ExpectedReleaseChannel) {
      $issues += "$($document.label).release_channel must be $ExpectedReleaseChannel."
    }
    if ($document.value.generation_state -ne $ExpectedGenerationState) {
      $issues += "$($document.label).generation_state must be $ExpectedGenerationState."
    }
  }

  return [pscustomobject]@{
    package_path = $resolvedPath
    ok = ($issues.Count -eq 0)
    issues = $issues
  }
}
