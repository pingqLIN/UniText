Set-StrictMode -Version Latest

function Get-NormalizedFullPath {
  param(
    [Parameter(Mandatory)][string]$BasePath,
    [Parameter(Mandatory)][string]$CandidatePath
  )

  $base = [System.IO.Path]::GetFullPath($BasePath)
  $combined = if ([System.IO.Path]::IsPathRooted($CandidatePath)) {
    $CandidatePath
  } else {
    [System.IO.Path]::Combine($base, $CandidatePath)
  }

  return [System.IO.Path]::GetFullPath($combined)
}

function Resolve-PortablePath {
  param(
    [Parameter(Mandatory)][string]$Path
  )

  if ([string]::IsNullOrWhiteSpace($Path)) {
    throw "Path cannot be empty or whitespace."
  }

  $candidate = $Path.Trim()

  if (Test-Path -LiteralPath $candidate) {
    return (Resolve-Path -LiteralPath $candidate).Path
  }

  if ($candidate.StartsWith('/')) {
    $wsl = Get-Command wsl.exe -ErrorAction SilentlyContinue
    if ($null -ne $wsl) {
      $translated = & wsl.exe wslpath -w -- $candidate 2>$null
      if ($LASTEXITCODE -eq 0 -and -not [string]::IsNullOrWhiteSpace($translated)) {
        return [System.IO.Path]::GetFullPath($translated.Trim())
      }
    }
  }

  return [System.IO.Path]::GetFullPath($candidate)
}

function Test-IsUnderPath {
  param(
    [Parameter(Mandatory)][string]$RootPath,
    [Parameter(Mandatory)][string]$CandidatePath
  )

  $root = [System.IO.Path]::GetFullPath($RootPath).TrimEnd('\', '/')
  $candidate = [System.IO.Path]::GetFullPath($CandidatePath).TrimEnd('\', '/')

  if ($candidate -eq $root) {
    return $true
  }

  $prefix = $root + [System.IO.Path]::DirectorySeparatorChar
  return $candidate.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)
}

function Test-ContainsReparsePoint {
  param(
    [Parameter(Mandatory)][string]$Path
  )

  if (-not (Test-Path -LiteralPath $Path)) {
    return $false
  }

  $item = Get-Item -LiteralPath $Path -Force
  if (($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
    return $true
  }

  if (-not $item.PSIsContainer) {
    return $false
  }

  foreach ($child in Get-ChildItem -LiteralPath $Path -Force -Recurse) {
    if (($child.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
      return $true
    }
  }

  return $false
}

function Assert-SafeSimpleName {
  param(
    [Parameter(Mandatory)][string]$Value,
    [string]$Label = "name",
    [string]$Pattern = '^[a-z0-9][a-z0-9_-]{0,127}$'
  )

  if ([string]::IsNullOrWhiteSpace($Value)) {
    throw "$Label cannot be empty or whitespace."
  }

  $trimmed = $Value.Trim()
  if ($trimmed -ne $Value) {
    throw "$Label cannot start or end with whitespace."
  }

  if ($trimmed -match '[/\\:]') {
    throw "$Label cannot contain path separators or colons."
  }

  if ($trimmed -match '\.\.') {
    throw "$Label cannot contain traversal sequences."
  }

  if ($trimmed -match '[\x00-\x1f]') {
    throw "$Label cannot contain control characters."
  }

  if ($trimmed -match '[\.\s]$') {
    throw "$Label cannot end with a dot or space."
  }

  $reserved = @(
    'CON', 'PRN', 'AUX', 'NUL',
    'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
    'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
  )
  $baseName = [System.IO.Path]::GetFileNameWithoutExtension($trimmed)
  if ($reserved -contains $baseName.ToUpperInvariant()) {
    throw "$Label cannot use a Windows reserved device name."
  }

  if ($trimmed -notmatch $Pattern) {
    throw "$Label is invalid: $trimmed"
  }

  return $trimmed
}

function Resolve-SafeRepoPath {
  param(
    [Parameter(Mandatory)][string]$RepoRoot,
    [Parameter(Mandatory)][string]$BaseRelativePath,
    [Parameter(Mandatory)][string]$UserPath,
    [switch]$AllowBasePath,
    [switch]$RequireExisting
  )

  if ([string]::IsNullOrWhiteSpace($UserPath)) {
    throw "Path cannot be empty or whitespace."
  }

  $base = Get-NormalizedFullPath -BasePath $RepoRoot -CandidatePath $BaseRelativePath
  $candidate = Get-NormalizedFullPath -BasePath $RepoRoot -CandidatePath $UserPath

  if (-not $AllowBasePath -and $candidate -eq $base) {
    throw "Resolved path cannot be the base directory itself."
  }

  if (-not (Test-IsUnderPath -RootPath $base -CandidatePath $candidate)) {
    throw "Resolved path escapes allowed boundary: $candidate"
  }

  if ($RequireExisting -and -not (Test-Path -LiteralPath $candidate)) {
    throw "Resolved path does not exist: $candidate"
  }

  return $candidate
}
