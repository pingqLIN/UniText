param(
  [string]$BaseBranch = "",
  [string]$FeatureBranch = "feature/new-task",
  [switch]$DryRun
)

$ErrorActionPreference = "Stop"

function Invoke-Git {
  param(
    [Parameter(Mandatory = $true)]
    [string[]]$Args
  )

  $hadNativePreference = Test-Path Variable:\PSNativeCommandUseErrorActionPreference
  $nativePreference = $null
  if ($hadNativePreference) {
    $nativePreference = $PSNativeCommandUseErrorActionPreference
    $PSNativeCommandUseErrorActionPreference = $false
  }

  $output = & git @Args 2>&1

  if ($hadNativePreference) {
    $PSNativeCommandUseErrorActionPreference = $nativePreference
  }

  if ($LASTEXITCODE -ne 0) {
    $text = ($output | Out-String).Trim()
    throw "git $($Args -join ' ') failed: $text"
  }

  $output
}

function Test-GitRef {
  param(
    [Parameter(Mandatory = $true)]
    [string]$Ref
  )

  & git show-ref --verify --quiet $Ref
  $LASTEXITCODE -eq 0
}

function Get-RemoteHeadBranch {
  $ref = & git symbolic-ref --quiet refs/remotes/origin/HEAD 2>$null
  if ($LASTEXITCODE -eq 0 -and $ref) {
    return ($ref -replace '^refs/remotes/origin/', '')
  }

  $remote = & git remote show origin 2>$null
  if ($LASTEXITCODE -ne 0) {
    return $null
  }

  $line = $remote | Where-Object { $_ -match 'HEAD branch:\s+(.+)$' } | Select-Object -First 1
  if (-not $line) {
    return $null
  }

  $match = [regex]::Match($line, 'HEAD branch:\s+(.+)$')
  if (-not $match.Success) {
    return $null
  }

  $match.Groups[1].Value.Trim()
}

function Get-CanonicalBaseBranch {
  param(
    [string]$RequestedBranch
  )

  if ($RequestedBranch) {
    return [pscustomobject]@{
      branch = $RequestedBranch
      source = "explicit"
    }
  }

  $remoteHead = Get-RemoteHeadBranch
  if ($remoteHead) {
    return [pscustomobject]@{
      branch = $remoteHead
      source = "origin-head"
    }
  }

  if (Test-GitRef "refs/heads/main") {
    return [pscustomobject]@{
      branch = "main"
      source = "local-main"
    }
  }

  if (Test-GitRef "refs/heads/master") {
    return [pscustomobject]@{
      branch = "master"
      source = "local-master"
    }
  }

  throw "Cannot resolve a canonical base branch. Pass -BaseBranch explicitly."
}

$repoRoot = (Invoke-Git -Args @("rev-parse", "--show-toplevel") | Select-Object -Last 1).Trim()
$status = Invoke-Git -Args @("status", "--short")
if ($status) {
  throw "Working tree is not clean. Resolve or stash changes before startup."
}

$hasOrigin = (& git remote get-url origin 2>$null)
$base = $null
if ($hasOrigin -and $LASTEXITCODE -eq 0) {
  Invoke-Git -Args @("fetch", "origin", "--prune") | Out-Null
}

$base = Get-CanonicalBaseBranch -RequestedBranch $BaseBranch
$baseBranch = $base.branch
$baseSource = $base.source
$remoteBaseRef = "refs/remotes/origin/$baseBranch"
$localBaseRef = "refs/heads/$baseBranch"
$hasRemoteBase = Test-GitRef $remoteBaseRef
$hasLocalBase = Test-GitRef $localBaseRef

if (-not $hasLocalBase -and $hasRemoteBase) {
  if ($DryRun) {
    $hasLocalBase = $true
  } else {
    Invoke-Git -Args @("branch", "--track", $baseBranch, "origin/$baseBranch") | Out-Null
    $hasLocalBase = $true
  }
}

if (-not $hasLocalBase) {
  throw "Base branch '$baseBranch' does not exist locally or on origin."
}

$featureLocalRef = "refs/heads/$FeatureBranch"
$featureRemoteRef = "refs/remotes/origin/$FeatureBranch"
$featureExistsLocal = Test-GitRef $featureLocalRef
$featureExistsRemote = Test-GitRef $featureRemoteRef
if ($featureExistsLocal -or $featureExistsRemote) {
  $scope = if ($featureExistsLocal -and $featureExistsRemote) {
    "local and remote"
  } elseif ($featureExistsLocal) {
    "local"
  } else {
    "remote"
  }

  throw "Feature branch '$FeatureBranch' already exists on $scope."
}

if ($DryRun) {
  [pscustomobject]@{
    repo_root = $repoRoot
    base_branch = $baseBranch
    base_branch_source = $baseSource
    has_remote_base = $hasRemoteBase
    feature_branch = $FeatureBranch
    dry_run = $true
    actions = @(
      "git fetch origin --prune",
      "git switch $baseBranch",
      $(if ($hasRemoteBase) { "git pull --ff-only origin $baseBranch" } else { "skip pull (no remote base branch)" }),
      "git switch -c $FeatureBranch"
    )
  }
  return
}

Invoke-Git -Args @("switch", $baseBranch) | Out-Null
if ($hasRemoteBase) {
  Invoke-Git -Args @("pull", "--ff-only", "origin", $baseBranch) | Out-Null
}

$postStatus = Invoke-Git -Args @("status", "--short")
if ($postStatus) {
  throw "Base branch '$baseBranch' is not clean after update."
}

Invoke-Git -Args @("switch", "-c", $FeatureBranch) | Out-Null

[pscustomobject]@{
  repo_root = $repoRoot
  base_branch = $baseBranch
  base_branch_source = $baseSource
  has_remote_base = $hasRemoteBase
  feature_branch = $FeatureBranch
  dry_run = $false
}
