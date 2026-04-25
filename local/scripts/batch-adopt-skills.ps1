param(
  [string]$Source = ".bak_20260315_00\skills.bak.20260228_215107",
  [string]$Destination = "registry\skills",
  [string[]]$Ids = @("frontend-design", "pdf", "docx", "xlsx", "mcp-builder"),
  [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$repo = (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path
. (Join-Path $PSScriptRoot "lib\path-safety.ps1")
$safeIds = @(
  foreach ($id in $Ids) {
    Assert-SafeSimpleName -Value $id -Label "Id" -Pattern '^[a-z0-9][a-z0-9-]{0,63}$'
  }
)

$srcPath = Resolve-Path $Source -ErrorAction SilentlyContinue
if (-not $srcPath) {
  throw "Source root not found: $Source"
}

$srcRoot = $srcPath.Path
$skillsRoot = Get-NormalizedFullPath -BasePath $repo -CandidatePath "registry\skills"
$dstRoot = Get-NormalizedFullPath -BasePath $repo -CandidatePath $Destination
if (-not (Test-IsUnderPath -RootPath $skillsRoot -CandidatePath $dstRoot)) {
  throw "Destination must remain under registry/skills: $dstRoot"
}
$runId = Get-Date -Format "yyyyMMdd_HHmmss"
$runDir = Join-Path $repo "ops\history\adopt_$runId"

if (Test-ContainsReparsePoint -Path $srcRoot) {
  throw "Source root contains a symlink or reparse point: $srcRoot"
}

if (-not $DryRun) {
  New-Item -ItemType Directory -Force -Path $dstRoot | Out-Null
}

if (-not $DryRun) {
  New-Item -ItemType Directory -Force -Path $runDir | Out-Null
}

foreach ($safeId in $safeIds) {
  $src = Get-NormalizedFullPath -BasePath $srcRoot -CandidatePath $safeId
  $dst = Get-NormalizedFullPath -BasePath $dstRoot -CandidatePath $safeId

  if (-not (Test-IsUnderPath -RootPath $srcRoot -CandidatePath $src)) {
    throw "Resolved source escapes source root: $src"
  }

  if (-not (Test-IsUnderPath -RootPath $dstRoot -CandidatePath $dst)) {
    throw "Resolved destination escapes destination root: $dst"
  }

  if (-not (Test-Path -LiteralPath $src)) {
    Write-Warning "missing source: $safeId"
    continue
  }

  if (Test-ContainsReparsePoint -Path $src) {
    throw "source contains a symlink or reparse point: $src"
  }

  if ($DryRun) {
    [pscustomobject]@{
      action = "adopt"
      id = $safeId
      source = $src
      destination = $dst
      existing_destination = (Test-Path -LiteralPath $dst)
    }
    continue
  }

  if (Test-Path -LiteralPath $dst) {
    if (Test-ContainsReparsePoint -Path $dst) {
      throw "destination contains a symlink or reparse point: $dst"
    }

    $backup = Join-Path $runDir $safeId
    Copy-Item -LiteralPath $dst -Destination $backup -Recurse -Force
    Remove-Item -LiteralPath $dst -Recurse -Force
  }

  Copy-Item -LiteralPath $src -Destination $dst -Recurse -Force
  Write-Output "adopted $safeId"
}
