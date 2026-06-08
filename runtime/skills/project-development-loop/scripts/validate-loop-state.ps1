param(
    [string]$ProjectRoot = (Get-Location).Path,
    [string]$StateRoot = '',
    [string]$StateFile,
    [string]$StartupScript = "runtime/skills/project-development-loop/scripts/startup-briefing-countdown.ps1",
    [string]$CounterpartStartupScript = "registry/skills/project-development-loop/scripts/startup-briefing-countdown.ps1",
    [string[]]$ScriptFileNames = @(
        'startup-briefing-countdown.ps1',
        'validate-loop-state.ps1'
    ),
    [int]$CountdownWindowSeconds = 30,
    [int]$MaxStateAgeHours = 3,
    [int]$FutureToleranceSeconds = 120,
    [switch]$DryRun = $false,
    [switch]$CheckCounterpart = $true,
    [switch]$CheckScriptParity = $true,
    [switch]$OutputJson = $false,
    [switch]$Strict = $false
)

function Get-CanonicalScriptHash {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,
        [string]$FileName
    )

    $raw = Get-Content -Raw -LiteralPath $Path -Encoding UTF8
    $normalized = $raw -replace "`r`n", "`n"
    if ($FileName -eq 'validate-loop-state.ps1') {
        $normalized = [regex]::Replace(
            $normalized,
            '(\[string\]\$CounterpartStartupScript\s*=\s*")[^"]+(")',
            '${1}<counterpart-startup-script-placeholder>${2}'
        )
    }

    $sha256 = [System.Security.Cryptography.SHA256]::Create()
    try {
        $bytes = [System.Text.Encoding]::UTF8.GetBytes($normalized)
        return [BitConverter]::ToString($sha256.ComputeHash($bytes)).Replace('-', '')
    } finally {
        $sha256.Dispose()
    }
}

function Get-StartupHealthChecks {
    param(
        [Parameter(Mandatory = $true)]
        [PSCustomObject]$StartupCheck
    )

    [string[]]$issues = @()
    if (-not $StartupCheck.schema_version) {
        $issues += 'startup schema version missing'
    } elseif ([int]$StartupCheck.schema_version -lt 2) {
        $issues += "unsupported startup schema version: $($StartupCheck.schema_version)"
    }

    if ($null -ne $StartupCheck.branch_match -and $StartupCheck.branch_match -eq $false) {
        $issues += 'branch mismatch for startup state'
    }

    if ($null -ne $StartupCheck.state_load_error -and $StartupCheck.state_load_error) {
        $issues += "startup state load error: $($StartupCheck.state_load_error)"
    }

    if (($null -ne $StartupCheck.state_age_seconds) -and ($null -ne $StartupCheck.max_state_age_seconds)) {
        $stateAgeSeconds = [int]$StartupCheck.state_age_seconds
        $maxAgeSeconds = [int]$StartupCheck.max_state_age_seconds
        if ($maxAgeSeconds -gt 0 -and $stateAgeSeconds -gt $maxAgeSeconds) {
            $issues += "startup state age (${stateAgeSeconds}s) exceeds max age (${maxAgeSeconds}s)"
        }
    }

    return ([string[]]@($issues))
}

$resolvedProjectRoot = (Resolve-Path $ProjectRoot).Path
$startupPath = Join-Path $resolvedProjectRoot $StartupScript
$counterpartStartupPath = if ([string]::IsNullOrWhiteSpace($CounterpartStartupScript)) {
    $null
} else {
    Join-Path $resolvedProjectRoot $CounterpartStartupScript
}
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
$stateStartedAt = $null
if ($stateObj.started_at) {
    try {
        $stateStartedAt = [datetime]::Parse($stateObj.started_at)
    } catch {
        if (-not $loadError) { $loadError = $_.Exception.Message }
    }
}

$now = Get-Date
$deadlineUnix = if ($stateDeadline) { [Math]::Max(0, [int][Math]::Floor(($stateDeadline - $now).TotalSeconds)) } else { $null }
$stateAge = if ($stateStartedAt) { [int][Math]::Floor(($now - $stateStartedAt).TotalHours) } else { $null }

$branchMatch = $false
if ($stateObj.branch -and $currentBranch) {
    $branchMatch = ($stateObj.branch -eq $currentBranch)
}

$timeAlive = if ($stateObj.started_at) {
    try { [int][Math]::Floor(($now - $stateStartedAt).TotalSeconds) } catch { $null }
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
if ($stateObj) {
    $blankableFields = @('mode', 'budget', 'branch', 'active_batch', 'next_intended_action')
    foreach ($field in $blankableFields) {
        if (-not [string]::IsNullOrWhiteSpace([string]$stateObj.$field)) {
            continue
        }
        $orchestration.can_resume = $false
        $orchestration.recommendations += "state field requires non-empty value: $field"
    }
}
if ($stateStartedAt -and $stateStartedAt -gt $now.AddSeconds($FutureToleranceSeconds)) {
    $orchestration.can_resume = $false
    $orchestration.recommendations += "state started_at is in the future: $($stateObj.started_at)"
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

$scriptParityChecks = @()
if ($CheckScriptParity) {
    $scriptRootRuntime = Join-Path $resolvedProjectRoot "runtime/skills/project-development-loop/scripts"
    $scriptRootRegistry = Join-Path $resolvedProjectRoot "registry/skills/project-development-loop/scripts"
    foreach ($file in $ScriptFileNames) {
        $runtimeFile = Join-Path $scriptRootRuntime $file
        $registryFile = Join-Path $scriptRootRegistry $file
        $entry = [ordered]@{
            file = $file
            runtime_exists = $false
            registry_exists = $false
            runtime_hash = $null
            registry_hash = $null
            hashes_match = $false
            check_error = $null
        }

        if (Test-Path -LiteralPath $runtimeFile) {
            $entry.runtime_exists = $true
        } else {
            $entry.check_error = "missing runtime script: $runtimeFile"
            $orchestration.can_resume = $false
            $orchestration.recommendations = @("runtime script missing: $runtimeFile") + @($orchestration.recommendations | Where-Object { $_ -ne 'resume conditions satisfied' })
        }

        if (Test-Path -LiteralPath $registryFile) {
            $entry.registry_exists = $true
        } else {
            $entry.check_error = if ($entry.check_error) { $entry.check_error + '; ' } else { '' } + "missing registry script: $registryFile"
            $orchestration.can_resume = $false
            $orchestration.recommendations = @("registry script missing: $registryFile") + @($orchestration.recommendations | Where-Object { $_ -ne 'resume conditions satisfied' })
        }

        if ($entry.runtime_exists -and $entry.registry_exists) {
            try {
                $entry.runtime_hash = Get-CanonicalScriptHash -Path $runtimeFile -FileName $file
                $entry.registry_hash = Get-CanonicalScriptHash -Path $registryFile -FileName $file
                $entry.hashes_match = ($entry.runtime_hash -eq $entry.registry_hash)
                if (-not $entry.hashes_match) {
                    $orchestration.can_resume = $false
                    $orchestration.recommendations = @("parity mismatch: $file") + @($orchestration.recommendations | Where-Object { $_ -ne 'resume conditions satisfied' })
                }
            } catch {
                $entry.check_error = $_.Exception.Message
                $orchestration.can_resume = $false
                $orchestration.recommendations = @("script parity check failed for ${file}: $($_.Exception.Message)") + @($orchestration.recommendations | Where-Object { $_ -ne 'resume conditions satisfied' })
            }
        }

        $scriptParityChecks += $entry
    }
    $orchestration.script_parity_checks = $scriptParityChecks
}

$startupCheck = $null
try {
    $startupArgs = @(
        '-NoProfile',
        '-ExecutionPolicy',
        'Bypass',
        '-File',
        $startupPath,
        '-RepoRoot',
        $resolvedProjectRoot,
        '-TimeoutSeconds',
        $CountdownWindowSeconds,
        '-Reset',
        '-OutputJson'
    )
    if ($DryRun) {
        $startupArgs += '-DryRun'
    }
    $startupOutputRaw = & powershell @startupArgs
    $startupCheck = $startupOutputRaw | ConvertFrom-Json -ErrorAction Stop
} catch {
    $orchestration.can_resume = $false
    $startupCheck = [ordered]@{
        decision = 'error'
        decision_reason = $_.Exception.Message
    }
    $orchestration.recommendations = @('startup script failed to return a valid JSON health check') + @($orchestration.recommendations | Where-Object { $_ -ne 'resume conditions satisfied' })
}
$startupHealthChecks = if ($startupCheck -and $startupCheck.PSObject) {
    Get-StartupHealthChecks -StartupCheck $startupCheck
} else {
    @()
}
if ($startupHealthChecks -eq $null) {
    $startupHealthChecks = @()
}
$orchestration.startup_health_checks = $startupHealthChecks
if ($startupHealthChecks.Count -gt 0) {
    $orchestration.can_resume = $false
    $orchestration.recommendations = @("startup health issues: $($startupHealthChecks -join '; ')") + @($orchestration.recommendations | Where-Object { $_ -ne 'resume conditions satisfied' })
}
$orchestration.startup_check = $startupCheck

if ($startupCheck.decision -eq 'stop') {
    $orchestration.recommendations = @('startup countdown window reached stop; extend CountdownWindowSeconds if needed') + @($orchestration.recommendations | Where-Object { $_ -ne 'resume conditions satisfied' })
}

if (-not $DryRun -and $startupCheck.state_file_written -eq $false) {
    $orchestration.can_resume = $false
    $orchestration.recommendations = @('startup state file write failed; verify writable state path') + @($orchestration.recommendations | Where-Object { $_ -ne 'resume conditions satisfied' })
}

if ($CheckCounterpart -and $counterpartStartupPath -and (Test-Path -LiteralPath $counterpartStartupPath)) {
    $counterpartArgs = @(
        '-NoProfile',
        '-ExecutionPolicy',
        'Bypass',
        '-File',
        $counterpartStartupPath,
        '-RepoRoot',
        $resolvedProjectRoot,
        '-TimeoutSeconds',
        $CountdownWindowSeconds,
        '-Reset',
        '-OutputJson'
    )
    if ($DryRun) {
        $counterpartArgs += '-DryRun'
    }

    $counterpartCheck = $null
    try {
        $counterpartRaw = & powershell @counterpartArgs
        $counterpartCheck = $counterpartRaw | ConvertFrom-Json -ErrorAction Stop
    } catch {
        $counterpartCheck = [ordered]@{
            decision = 'error'
            decision_reason = $_.Exception.Message
        }
    }
    $orchestration.counterpart_startup_check = $counterpartCheck
    $counterpartHealthChecks = if ($counterpartCheck -and $counterpartCheck.PSObject) {
        Get-StartupHealthChecks -StartupCheck $counterpartCheck
    } else {
        @()
    }
    if ($counterpartHealthChecks -eq $null) {
        $counterpartHealthChecks = @()
    }
    $orchestration.counterpart_health_checks = $counterpartHealthChecks
    if ($counterpartHealthChecks.Count -gt 0) {
        $orchestration.can_resume = $false
        $orchestration.recommendations = @("counterpart startup health issues: $($counterpartHealthChecks -join '; ')") + @($orchestration.recommendations | Where-Object { $_ -ne 'resume conditions satisfied' })
    }

    $parityMismatch = @()
    $compareFields = @('decision', 'decision_reason', 'state_file_written', 'state_file_error', 'schema_version', 'progress_state')
    foreach ($field in $compareFields) {
        if (($startupCheck[$field] -ne $counterpartCheck[$field])) {
            $parityMismatch += "field_mismatch:$field|${startupCheck[$field]}<>${counterpartCheck[$field]}"
        }
    }
    if ($parityMismatch.Count -gt 0) {
        $orchestration.can_resume = $false
        $orchestration.recommendations = @('startup runtime/registry parity mismatch: ' + ($parityMismatch -join '; ')) + @($orchestration.recommendations | Where-Object { $_ -ne 'resume conditions satisfied' })
    }
} elseif ($CheckCounterpart) {
    $orchestration.counterpart_startup_check = $null
    $orchestration.can_resume = $false
    $orchestration.recommendations = @("counterpart startup script not found: $CounterpartStartupScript") + @($orchestration.recommendations | Where-Object { $_ -ne 'resume conditions satisfied' })
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
