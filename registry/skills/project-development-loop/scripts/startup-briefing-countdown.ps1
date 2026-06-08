param(
    [string]$RepoRoot = (Get-Location).Path,
    [int]$TimeoutSeconds = 60,
    [int]$BarWidth = 28,
    [int]$RefreshMilliseconds = 125,
    [string]$StateRoot = '',
    [switch]$DryRun = $false,
    [switch]$OutputJson = $false,
    [switch]$Reset = $false,
    [int]$MaxStateAgeSeconds = 10800,
    [int]$StateWriteRetryMs = 75
)

function Write-StateFileWithRetry {
    param(
        [Parameter(Mandatory = $true)] [string]$Path,
        [Parameter(Mandatory = $true)] [string]$Content,
        [int]$MaxRetries = 5,
        [int]$RetryDelayMs = 75
    )

    for ($i = 0; $i -lt $MaxRetries; $i++) {
        try {
            Set-Content -Path $Path -Value $Content -Encoding UTF8 -ErrorAction Stop
            return [ordered]@{ ok = $true; error = $null }
        } catch {
            if ($i -eq ($MaxRetries - 1)) {
                return [ordered]@{ ok = $false; error = $_.Exception.Message }
            }
            Start-Sleep -Milliseconds ([Math]::Max(0, $RetryDelayMs * [Math]::Pow(2, $i)))
        }
    }

    return [ordered]@{ ok = $false; error = 'unknown write failure' }
}

$normalizedRepoRoot = (Resolve-Path $RepoRoot).Path
$safeStateName = [IO.Path]::GetFileName($normalizedRepoRoot).Replace(':','_')
$defaultStateRoot = [IO.Path]::GetTempPath()
$stateDirectory = if ([string]::IsNullOrWhiteSpace($StateRoot)) {
    Join-Path $defaultStateRoot 'project-development-loop'
} else {
    $StateRoot
}

if (-not (Test-Path -LiteralPath $stateDirectory)) {
    New-Item -ItemType Directory -Path $stateDirectory -Force | Out-Null
}

$stateFile = Join-Path $stateDirectory ("startup-briefing-${safeStateName}.json")
$state = @{}
$stateLoadError = $null
$hasState = $false
if (Test-Path -LiteralPath $stateFile) {
    $hasState = $true
    try {
        $state = Get-Content -Raw -LiteralPath $stateFile | ConvertFrom-Json -ErrorAction Stop
    } catch {
        $stateLoadError = $_.Exception.Message
        $state = @{}
    }
}

$gitBranch = 'unknown'
try {
    $gitBranch = (& git -C $normalizedRepoRoot rev-parse --abbrev-ref HEAD) 2>$null
} catch {
    $gitBranch = 'unknown'
}

$stateBranch = if ($state.branch) { $state.branch } else { $null }
$branchMismatch = $false
$stateHasTimestamp = [bool]($state.started_at)
$stateAgeSeconds = $null
$resumed = $false
$resumeReason = @()

if ($Reset) {
    $resumeReason += 'reset-requested'
}

$startedAt = Get-Date
if (-not $Reset -and $stateHasTimestamp -and [string]::IsNullOrEmpty($stateLoadError)) {
    try {
        $parsedStartedAt = [datetime]::Parse($state.started_at)
        if ($stateBranch -and $stateBranch -ne $gitBranch) {
            $branchMismatch = $true
            $resumeReason += "branch_mismatch:$stateBranch->$gitBranch"
        } else {
            $now = Get-Date
            $stateAgeSeconds = [Math]::Round(($now - $parsedStartedAt).TotalSeconds)
            if ($stateAgeSeconds -gt $MaxStateAgeSeconds) {
                $resumeReason += "state_too_old:${stateAgeSeconds}s>=$MaxStateAgeSeconds"
            } else {
                $resumed = $true
                $startedAt = $parsedStartedAt
                $resumeReason += 'state_resumed'
            }
        }
    } catch {
        $stateLoadError = $_.Exception.Message
        $resumeReason += 'state_started_at_parse_failed'
    }
}

if (-not $resumed) {
    $startedAt = Get-Date
    $resumeReason += 'state_start_reset'
}

if ($stateAgeSeconds -eq $null) {
    $now = Get-Date
    $stateAgeSeconds = [int][Math]::Round(($now - $startedAt).TotalSeconds)
}

$now = Get-Date
$elapsedSeconds = [Math]::Max([double]0, ($now - $startedAt).TotalSeconds)
$remainingSeconds = [Math]::Max([double]0, [double]$TimeoutSeconds - $elapsedSeconds)
$decision = if ($remainingSeconds -gt 0) { 'continue' } else { 'stop' }
$decisionReason = if ($decision -eq 'stop') {
    if ($resumed -and $remainingSeconds -le 0) {
        'deadline_reached'
    } else {
        'manual_reset_or_expired'
    }
} else {
    'within_window'
}
$elapsedRounded = [int][Math]::Round($elapsedSeconds)
$remainingRounded = [int][Math]::Ceiling($remainingSeconds)

$ratio = [Math]::Min(1, [Math]::Max([double]0, $elapsedSeconds / [Math]::Max([double]1, [double]$TimeoutSeconds)))
$filled = [int][Math]::Round($ratio * $BarWidth)
$empty = [Math]::Max([int]0, $BarWidth - $filled)

$stateFileContent = [ordered]@{
    schema_version = 2
    repo_root = $normalizedRepoRoot
    branch = $gitBranch
    started_at = $startedAt.ToString('o')
    timeout_seconds = $TimeoutSeconds
    bar_width = $BarWidth
    refresh_milliseconds = $RefreshMilliseconds
    last_checked_at = $now.ToString('o')
    elapsed_seconds = $elapsedRounded
    remaining_seconds = $remainingRounded
    deadline = $startedAt.AddSeconds($TimeoutSeconds).ToString('o')
    progress_bar = if ($decision -eq 'continue' -or $DryRun) {
        ("#" * $filled) + ('-' * $empty)
    } else {
        "#" * $BarWidth
    }
    decision = $decision
    decision_reason = $decisionReason
    progress_state = if ($resumed) { 'resumed' } else { 'fresh' }
    state_file = $stateFile
    state_age_seconds = [int]$stateAgeSeconds
    previous_state_present = $hasState
    branch_match = (-not $branchMismatch)
    state_load_error = $stateLoadError
    resume_reason = $resumeReason
    max_state_age_seconds = $MaxStateAgeSeconds
    state_file_written = $false
    state_file_error = $null
}

$stateFileContentJson = $stateFileContent | ConvertTo-Json -Depth 5
$writeResult = Write-StateFileWithRetry -Path $stateFile -Content $stateFileContentJson -RetryDelayMs $StateWriteRetryMs
$stateFileContent.state_file_written = $writeResult.ok
$stateFileContent.state_file_error = $writeResult.error
$stateFileContentJson = $stateFileContent | ConvertTo-Json -Depth 5

if ($OutputJson) {
    Write-Output $stateFileContentJson
} else {
    Write-Output $decision
}
