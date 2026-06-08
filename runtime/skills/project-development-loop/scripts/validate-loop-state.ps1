param(
    [string]$ProjectRoot = (Get-Location).Path,
    [string]$StateRoot = "Q:\UniText\ops\project-development-loop",
    [string]$StateFile,
    [string]$StartupScript = "runtime/skills/project-development-loop/scripts/startup-briefing-countdown.ps1",
    [int]$CountdownWindowSeconds = 30,
    [int]$MaxStateAgeHours = 3,
    [switch]$OutputJson = $false,
    [switch]$Strict = $false
)

$resolvedProjectRoot = (Resolve-Path $ProjectRoot).Path
$startupPath = Join-Path $resolvedProjectRoot $StartupScript
$stateRootResolved = if ([string]::IsNullOrWhiteSpace($StateRoot)) {
    Join-Path $resolvedProjectRoot "ops\project-development-loop"
} else {
    $StateRoot
}

if (-not (Test-Path -LiteralPath $stateRootResolved)) {
    throw "StateRoot not found: $stateRootResolved"
}

$currentBranch = 'unknown'
try {
    $currentBranch = (& git -C $resolvedProjectRoot rev-parse --abbrev-ref HEAD) 2>$null
} catch {
    $currentBranch = 'unknown'
}

$resolvedStateFile = if ([string]::IsNullOrWhiteSpace($StateFile)) {
    $files = Get-ChildItem -Path $stateRootResolved -Filter "active-*.json" -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending
    if (-not $files) {
        throw "No active state file found under $stateRootResolved"
    }
    $files[0].FullName
} else {
    if (-not (Test-Path -LiteralPath $StateFile)) {
        throw "StateFile not found: $StateFile"
    }
    (Resolve-Path $StateFile).Path
}

$stateRaw = $null
$loadError = $null
$stateObj = @{}
try {
    $stateRaw = Get-Content -Raw -LiteralPath $resolvedStateFile
    $stateObj = $stateRaw | ConvertFrom-Json -ErrorAction Stop
} catch {
    $loadError = $_.Exception.Message
}

$requiredFields = @('mode','budget','deadline','branch','active_batch','next_intended_action')
$missingFields = @()
if ($stateObj -and $stateObj.PSObject.TypeNames -contains 'System.Management.Automation.PSCustomObject') {
    foreach ($field in $requiredFields) {
        if (-not ($stateObj.PSObject.Properties.Name -contains $field)) {
            $missingFields += $field
        }
    }
}

$stateDeadline = $null
if ($stateObj.deadline) {
    try {
        $stateDeadline = [datetime]::Parse($stateObj.deadline)
    } catch {
        if (-not $loadError) { $loadError = $_.Exception.Message }
    }
}

$now = Get-Date
$deadlineUnix = if ($stateDeadline) { [Math]::Max(0, [int][Math]::Floor(($stateDeadline - $now).TotalSeconds)) } else { $null }
$stateAge = if ($stateObj.started_at) {
    try { [int][Math]::Floor(($now - [datetime]::Parse($stateObj.started_at)).TotalHours) } catch { $null }
} else { $null }

$branchMatch = $false
if ($stateObj.branch -and $currentBranch) {
    $branchMatch = ($stateObj.branch -eq $currentBranch)
}

$timeAlive = if ($stateObj.started_at) {
    try { [int][Math]::Floor(($now - [datetime]::Parse($stateObj.started_at)).TotalSeconds) } catch { $null }
} else { $null }

$orchestration = [ordered]@{
    schema_version = 1
    timestamp = $now.ToString('o')
    project_root = $resolvedProjectRoot
    active_state_file = $resolvedStateFile
    current_branch = $currentBranch
    state_loaded = ($loadError -eq $null)
    load_error = $loadError
    missing_fields = $missingFields
    deadline = if ($stateDeadline) { $stateDeadline.ToString('o') } else { $null }
    seconds_to_deadline = $deadlineUnix
    state_age_hours = $stateAge
    branch_expected = if ($stateObj.branch) { $stateObj.branch } else { $null }
    branch_match = $branchMatch
    active_batch = if ($stateObj.active_batch) { $stateObj.active_batch } else { $null }
    next_intended_action = if ($stateObj.next_intended_action) { $stateObj.next_intended_action } else { $null }
    state_file_age_hours = $stateAge
    max_state_age_hours = $MaxStateAgeHours
    can_resume = $false
    recommendations = @()
}

if (-not $stateObj -or $loadError) {
    $orchestration.can_resume = $false
    $orchestration.recommendations += 'fix state file load error first'
}
if ($missingFields.Count -gt 0) {
    $orchestration.can_resume = $false
    $orchestration.recommendations += 'state file missing required fields; perform audit before resume'
}
if (-not $branchMatch) {
    $orchestration.can_resume = $false
    $orchestration.recommendations += 'branch changed; restart batch with reset and log checkpoint'
}
if ($stateDeadline -and ($now -gt $stateDeadline)) {
    $orchestration.can_resume = $false
    $orchestration.recommendations += 'batch deadline reached; start next reviewed batch'
}
if ($stateAge -ne $null -and $stateAge -gt $MaxStateAgeHours) {
    $orchestration.can_resume = $false
    $orchestration.recommendations += 'state is older than allowed max age; prefer fresh run'
}

if ($orchestration.recommendations.Count -eq 0) {
    $orchestration.can_resume = $true
    $orchestration.recommendations += 'resume conditions satisfied'
}

$startupCheck = $null
try {
    $startupOutputRaw = & powershell -NoProfile -ExecutionPolicy Bypass -File $startupPath -RepoRoot $resolvedProjectRoot -TimeoutSeconds $CountdownWindowSeconds -Reset -OutputJson
    $startupCheck = $startupOutputRaw | ConvertFrom-Json -ErrorAction Stop
} catch {
    $orchestration.can_resume = $false
    $startupCheck = [ordered]@{
        decision = 'error'
        decision_reason = $_.Exception.Message
    }
    $orchestration.recommendations = @('startup script failed to return a valid JSON health check') + @($orchestration.recommendations | Where-Object { $_ -ne 'resume conditions satisfied' })
}
$orchestration.startup_check = $startupCheck

if ($startupCheck.decision -eq 'stop') {
    $orchestration.recommendations = @('startup countdown window reached stop; extend CountdownWindowSeconds if needed') + @($orchestration.recommendations | Where-Object { $_ -ne 'resume conditions satisfied' })
}

if ($startupCheck.state_file_written -eq $false) {
    $orchestration.can_resume = $false
    $orchestration.recommendations = @('startup state file write failed; verify writable state path') + @($orchestration.recommendations | Where-Object { $_ -ne 'resume conditions satisfied' })
}

if (-not $stateObj -and -not $strict) {
    $orchestration.can_resume = $false
}

if ($strict -and -not $orchestration.can_resume) {
    if ($OutputJson) {
        Write-Output ($orchestration | ConvertTo-Json -Depth 5)
    } else {
        Write-Output "resume denied: $($orchestration.recommendations -join '; ')"
    }
    exit 1
}

if ($OutputJson) {
    Write-Output ($orchestration | ConvertTo-Json -Depth 5)
} else {
    $status = if ($orchestration.can_resume) { 'CAN RESUME' } else { 'REVIEW REQUIRED' }
    Write-Output "Loop state: $status"
    Write-Output "State file: $resolvedStateFile"
    if ($stateDeadline) { Write-Output "Deadline: $($orchestration.deadline) (in ${deadlineUnix}s)" }
    Write-Output "Branch match: $branchMatch"
    Write-Output "Startup decision: $($startupCheck.decision) / $($startupCheck.decision_reason)"
    if ($orchestration.recommendations.Count -gt 0) {
        Write-Output "Recommendations:"
        $orchestration.recommendations | ForEach-Object { Write-Output "- $_" }
    }
}
