[CmdletBinding()]
param(
    [string]$SkillRoot,

    [string]$ScratchRoot,

    [int]$LiveTimeoutSeconds = 30,

    [switch]$SkipLive
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($SkillRoot)) {
    $SkillRoot = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
}

$resolvedSkillRoot = (Resolve-Path -LiteralPath $SkillRoot).Path

if ([string]::IsNullOrWhiteSpace($ScratchRoot)) {
    $ScratchRoot = Join-Path -Path ([System.IO.Path]::GetTempPath()) -ChildPath ("external-audit-doctor-" + (Get-Date -Format "yyyyMMdd-HHmmss"))
}

$resolvedScratchRoot = [System.IO.Path]::GetFullPath($ScratchRoot)
New-Item -ItemType Directory -Force -Path $resolvedScratchRoot | Out-Null

$results = [System.Collections.Generic.List[object]]::new()

function Add-Result {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name,

        [Parameter(Mandatory = $true)]
        [ValidateSet("pass", "warn", "fail", "skip")]
        [string]$Status,

        [string]$Detail = "",

        [string]$Evidence = ""
    )

    $script:results.Add([pscustomobject]@{
        name = $Name
        status = $Status
        detail = $Detail
        evidence = $Evidence
    })
}

function Test-RequiredPath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$RelativePath
    )

    $path = Join-Path -Path $resolvedSkillRoot -ChildPath $RelativePath
    if (Test-Path -LiteralPath $path) {
        Add-Result -Name "path:$RelativePath" -Status "pass" -Detail "found" -Evidence $path
        return
    }

    Add-Result -Name "path:$RelativePath" -Status "fail" -Detail "missing" -Evidence $path
}

function Invoke-Step {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name,

        [Parameter(Mandatory = $true)]
        [scriptblock]$Script
    )

    try {
        $output = & $Script 2>&1
        Add-Result -Name $Name -Status "pass" -Detail "completed" -Evidence (($output | Out-String).Trim())
    }
    catch {
        Add-Result -Name $Name -Status "fail" -Detail $_.Exception.Message -Evidence (($_ | Out-String).Trim())
    }
}

function Get-FirstCommandPath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$CommandName
    )

    $application = Get-Command -Name $CommandName -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($application) {
        return $application.Source
    }

    $command = Get-Command -Name $CommandName -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($command -and $command.Source) {
        return $command.Source
    }

    return $null
}

function Invoke-ExternalWithTimeout {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name,

        [Parameter(Mandatory = $true)]
        [string]$FilePath,

        [Parameter(Mandatory = $true)]
        [string[]]$ArgumentList,

        [int]$TimeoutSeconds = 30
    )

    $safeName = ($Name -replace '[\\/:*?"<>|]', '_')
    $stdoutPath = Join-Path -Path $resolvedScratchRoot -ChildPath "$safeName.stdout.txt"
    $stderrPath = Join-Path -Path $resolvedScratchRoot -ChildPath "$safeName.stderr.txt"

    try {
        $process = Start-Process -FilePath $FilePath -ArgumentList $ArgumentList -NoNewWindow -PassThru -RedirectStandardOutput $stdoutPath -RedirectStandardError $stderrPath
        $completed = $process.WaitForExit($TimeoutSeconds * 1000)

        if (-not $completed) {
            try {
                $process.Kill($true)
            }
            catch {
                try { Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue } catch {}
            }

            $stdout = if (Test-Path -LiteralPath $stdoutPath) { Get-Content -LiteralPath $stdoutPath -Raw } else { "" }
            $stderr = if (Test-Path -LiteralPath $stderrPath) { Get-Content -LiteralPath $stderrPath -Raw } else { "" }
            Add-Result -Name $Name -Status "warn" -Detail "timed out after ${TimeoutSeconds}s" -Evidence (($stdout + "`n" + $stderr).Trim())
            return
        }

        $stdoutText = if (Test-Path -LiteralPath $stdoutPath) { Get-Content -LiteralPath $stdoutPath -Raw } else { "" }
        $stderrText = if (Test-Path -LiteralPath $stderrPath) { Get-Content -LiteralPath $stderrPath -Raw } else { "" }
        $status = if ($process.ExitCode -eq 0) { "pass" } else { "fail" }
        Add-Result -Name $Name -Status $status -Detail "exit_code=$($process.ExitCode)" -Evidence (($stdoutText + "`n" + $stderrText).Trim())
    }
    catch {
        Add-Result -Name $Name -Status "fail" -Detail $_.Exception.Message -Evidence (($_ | Out-String).Trim())
    }
}

$requiredPaths = @(
    "SKILL.md",
    "references\audit-packet-format.md",
    "references\mode-codex-exec.md",
    "references\mode-gemini-cli.md",
    "references\mode-same-provider.md",
    "references\mode-tb2.md",
    "references\report-format.md",
    "references\source-attribution-policy.md",
    "assets\codex\audit-report.schema.json",
    "assets\gemini\plan-architect.md",
    "assets\gemini\plan-critic.md",
    "assets\gemini\plan-critic.schema.json",
    "assets\gemini\design-critic.md",
    "assets\gemini\design-critic.schema.json",
    "assets\tb2\tb2-audit-request.template.json",
    "assets\claude\code-reviewer.md",
    "assets\report\external-audit-report.template.md",
    "scripts\build-audit-packet.ps1",
    "scripts\export-codex-exec-request.ps1",
    "scripts\export-gemini-reviewer-bundle.ps1",
    "scripts\export-tb2-audit-request.ps1",
    "scripts\normalize-audit-report.ps1",
    "scripts\run-external-audit-flow.ps1"
)

$requiredPaths | ForEach-Object { Test-RequiredPath -RelativePath $_ }

$packetPath = Join-Path -Path $resolvedScratchRoot -ChildPath "audit-packet.md"
$targetProject = $resolvedScratchRoot
$buildScript = Join-Path -Path $resolvedSkillRoot -ChildPath "scripts\build-audit-packet.ps1"
$codexExportScript = Join-Path -Path $resolvedSkillRoot -ChildPath "scripts\export-codex-exec-request.ps1"
$geminiExportScript = Join-Path -Path $resolvedSkillRoot -ChildPath "scripts\export-gemini-reviewer-bundle.ps1"
$tb2ExportScript = Join-Path -Path $resolvedSkillRoot -ChildPath "scripts\export-tb2-audit-request.ps1"

Invoke-Step -Name "build-audit-packet:dry-run" -Script {
    & $buildScript `
        -ProjectPath $targetProject `
        -ScopeType Manual `
        -ScopeValue "doctor smoke" `
        -Summary "Doctor smoke packet." `
        -Question @("Does packet generation work?") `
        -Check @("doctor smoke") `
        -Reference @("local-skill|$resolvedSkillRoot|doctor smoke") `
        -OutputPath $packetPath
}

Invoke-Step -Name "export-codex-exec-request:dry-run" -Script {
    & $codexExportScript `
        -SkillRoot $resolvedSkillRoot `
        -TargetProject $targetProject `
        -AuditPacketPath $packetPath `
        -OutputDirectory (Join-Path -Path $resolvedScratchRoot -ChildPath "codex-export")
}

Invoke-Step -Name "export-gemini-reviewer-bundle:dry-run" -Script {
    & $geminiExportScript `
        -SkillRoot $resolvedSkillRoot `
        -TargetProject $targetProject `
        -AuditPacketPath $packetPath `
        -OutputDirectory (Join-Path -Path $resolvedScratchRoot -ChildPath "gemini-export")
}

Invoke-Step -Name "export-tb2-audit-request:dry-run" -Script {
    & $tb2ExportScript `
        -SkillRoot $resolvedSkillRoot `
        -TargetProject $targetProject `
        -AuditPacketPath $packetPath `
        -OutputPath (Join-Path -Path $resolvedScratchRoot -ChildPath "tb2-request.json")
}

$codexPath = Get-FirstCommandPath -CommandName "codex"
if ($codexPath) {
    Add-Result -Name "cli:codex:path" -Status "pass" -Detail "found" -Evidence $codexPath
    Invoke-ExternalWithTimeout -Name "cli:codex:version" -FilePath $codexPath -ArgumentList @("--version") -TimeoutSeconds 10
}
else {
    Add-Result -Name "cli:codex:path" -Status "warn" -Detail "not found"
}

$claudePath = Get-FirstCommandPath -CommandName "claude"
if ($claudePath) {
    Add-Result -Name "cli:claude:path" -Status "pass" -Detail "found" -Evidence $claudePath
    Invoke-ExternalWithTimeout -Name "cli:claude:version" -FilePath $claudePath -ArgumentList @("--version") -TimeoutSeconds 10
}
else {
    Add-Result -Name "cli:claude:path" -Status "warn" -Detail "not found"
}

$geminiPath = Get-FirstCommandPath -CommandName "gemini"
if ($geminiPath) {
    Add-Result -Name "cli:gemini:path" -Status "pass" -Detail "found" -Evidence $geminiPath
    Invoke-ExternalWithTimeout -Name "cli:gemini:version" -FilePath $geminiPath -ArgumentList @("--version") -TimeoutSeconds 10
}
else {
    Add-Result -Name "cli:gemini:path" -Status "warn" -Detail "not found"
}

if ($SkipLive) {
    Add-Result -Name "live:codex-exec:minimal" -Status "skip" -Detail "SkipLive set"
    Add-Result -Name "live:claude-print:minimal" -Status "skip" -Detail "SkipLive set"
    Add-Result -Name "live:gemini-headless:minimal" -Status "skip" -Detail "SkipLive set"
}
else {
    if ($codexPath) {
        $codexLastMessage = Join-Path -Path $resolvedScratchRoot -ChildPath "codex-last-message.txt"
        Invoke-ExternalWithTimeout `
            -Name "live:codex-exec:minimal" `
            -FilePath $codexPath `
            -ArgumentList @("exec", "--ephemeral", "--ignore-user-config", "--ignore-rules", "--output-last-message", $codexLastMessage, "OK") `
            -TimeoutSeconds $LiveTimeoutSeconds
    }
    else {
        Add-Result -Name "live:codex-exec:minimal" -Status "skip" -Detail "codex not found"
    }

    if ($claudePath) {
        Invoke-ExternalWithTimeout `
            -Name "live:claude-print:minimal" `
            -FilePath $claudePath `
            -ArgumentList @("--print", "--no-session-persistence", "--output-format", "text", "--permission-mode", "dontAsk", "OK") `
            -TimeoutSeconds $LiveTimeoutSeconds
    }
    else {
        Add-Result -Name "live:claude-print:minimal" -Status "skip" -Detail "claude not found"
    }

    if ($geminiPath) {
        Invoke-ExternalWithTimeout `
            -Name "live:gemini-headless:minimal" `
            -FilePath $geminiPath `
            -ArgumentList @("-p", "OK", "--output-format", "json") `
            -TimeoutSeconds $LiveTimeoutSeconds
    }
    else {
        Add-Result -Name "live:gemini-headless:minimal" -Status "skip" -Detail "gemini not found"
    }
}

$failCount = @($results | Where-Object { $_.status -eq "fail" }).Count
$nonLiveFailCount = @($results | Where-Object { $_.status -eq "fail" -and $_.name -notlike "live:*" }).Count
$warnCount = @($results | Where-Object { $_.status -eq "warn" }).Count
$liveBlocked = @($results | Where-Object { $_.name -like "live:*" -and $_.status -in @("warn", "fail") }).Count -gt 0

$overall = if ($nonLiveFailCount -gt 0) {
    "missing-assets-or-export-failed"
}
elseif ($liveBlocked) {
    "export-ok-live-review-blocked"
}
elseif ($warnCount -gt 0) {
    "skill-ok-with-warnings"
}
else {
    "skill-ok"
}

$report = [pscustomobject]@{
    skill = "external-audit-orchestrator"
    overall = $overall
    skill_root = $resolvedSkillRoot
    scratch_root = $resolvedScratchRoot
    live_timeout_seconds = $LiveTimeoutSeconds
    skip_live = [bool]$SkipLive
    summary = [pscustomobject]@{
        pass = @($results | Where-Object { $_.status -eq "pass" }).Count
        warn = $warnCount
        fail = $failCount
        skip = @($results | Where-Object { $_.status -eq "skip" }).Count
    }
    results = @($results)
}

$report | ConvertTo-Json -Depth 6
