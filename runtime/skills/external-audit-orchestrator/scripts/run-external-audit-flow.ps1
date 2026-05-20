[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$SkillRoot,

    [Parameter(Mandatory = $true)]
    [string]$TargetProject,

    [ValidateSet("same-provider-subagent", "external-web", "external-cli-mcp", "codex-exec", "tb2-template")]
    [string]$Mode = "same-provider-subagent",

    [ValidateSet("WorkingTree", "Staged", "CommitRange", "Path", "Manual")]
    [string]$ScopeType = "WorkingTree",

    [string]$ScopeValue,

    [string]$Summary = "",

    [string[]]$Question = @(),

    [string[]]$Check = @(),

    [string[]]$Reference = @(),

    [string]$PacketPath,

    [string]$RawReviewPath,

    [string]$ReportPath,

    [ValidateSet("", "Y", "N", "O")]
    [string]$StartupGateAnswer = "",

    [ValidateSet("accept", "fix-and-rerun", "escalate-to-human", "archive-only")]
    [string]$Disposition = "fix-and-rerun",

    [string]$NextAction = "Review the findings, apply required fixes, and rerun the audit if any warning or higher issue was accepted.",

    [switch]$Apply
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$resolvedSkillRoot = (Resolve-Path -LiteralPath $SkillRoot).Path
$resolvedTargetProject = (Resolve-Path -LiteralPath $TargetProject).Path

$buildScript = Join-Path -Path $resolvedSkillRoot -ChildPath "scripts\build-audit-packet.ps1"
$normalizeScript = Join-Path -Path $resolvedSkillRoot -ChildPath "scripts\normalize-audit-report.ps1"
$claudeExportScript = Join-Path -Path $resolvedSkillRoot -ChildPath "scripts\export-claude-reviewer-bundle.ps1"
$codexExecExportScript = Join-Path -Path $resolvedSkillRoot -ChildPath "scripts\export-codex-exec-request.ps1"
$tb2ExportScript = Join-Path -Path $resolvedSkillRoot -ChildPath "scripts\export-tb2-audit-request.ps1"

foreach ($requiredScript in @($buildScript, $normalizeScript, $claudeExportScript, $codexExecExportScript, $tb2ExportScript)) {
    if (-not (Test-Path -LiteralPath $requiredScript)) {
        throw "Missing required script: $requiredScript"
    }
}

if ([string]::IsNullOrWhiteSpace($PacketPath)) {
    $packetDirectory = Join-Path -Path $resolvedTargetProject -ChildPath ".audit\packets"
    New-Item -ItemType Directory -Force -Path $packetDirectory | Out-Null
    $packetPath = Join-Path -Path $packetDirectory -ChildPath ("audit-packet-" + (Get-Date -Format "yyyyMMdd-HHmmss") + ".md")
}
else {
    $packetPath = (Resolve-Path -LiteralPath (Split-Path -Path $PacketPath -Parent)).Path + "\" + (Split-Path -Path $PacketPath -Leaf)
}

$buildSplat = @{
    ProjectPath = $resolvedTargetProject
    ScopeType = $ScopeType
    Summary = $Summary
    Question = $Question
    Check = $Check
    Reference = $Reference
    OutputPath = $packetPath
}

if (-not [string]::IsNullOrWhiteSpace($ScopeValue)) {
    $buildSplat["ScopeValue"] = $ScopeValue
}

$builtPacketPath = & $buildScript @buildSplat
$packetPath = [string]$builtPacketPath

$flowSummary = @(
    "External audit flow summary",
    "- mode: $Mode",
    "- target_project: $resolvedTargetProject",
    "- packet_path: $packetPath",
    "- apply: $Apply"
)

switch ($Mode) {
    "same-provider-subagent" {
        $exportSplat = @{
            SkillRoot = $resolvedSkillRoot
            TargetProject = $resolvedTargetProject
        }

        if ($Apply) {
            $exportSplat["Apply"] = $true
        }

        $exportOutput = & $claudeExportScript @exportSplat
        $flowSummary += "- export: claude reviewer bundle"
        $flowSummary += ($exportOutput | ForEach-Object { "  $_" })
    }
    "tb2-template" {
        $exportSplat = @{
            SkillRoot = $resolvedSkillRoot
            TargetProject = $resolvedTargetProject
            AuditPacketPath = $packetPath
        }

        if ($Apply) {
            $exportSplat["Apply"] = $true
        }

        $exportOutput = & $tb2ExportScript @exportSplat
        $flowSummary += "- export: tb2 request template"
        $flowSummary += ($exportOutput | ForEach-Object { "  $_" })
    }
    "codex-exec" {
        $exportSplat = @{
            SkillRoot = $resolvedSkillRoot
            TargetProject = $resolvedTargetProject
            AuditPacketPath = $packetPath
            StartupGateAnswer = $StartupGateAnswer
        }

        if ($Apply) {
            $exportSplat["Apply"] = $true
        }

        $exportOutput = & $codexExecExportScript @exportSplat
        $flowSummary += "- export: codex exec request"
        $flowSummary += ($exportOutput | ForEach-Object { "  $_" })
    }
    "external-web" {
        $flowSummary += "- export: none"
        $flowSummary += "- operator_step: paste the packet into the chosen visible web reviewer"
        $flowSummary += "- operator_step: save raw reviewer output to a file and rerun this flow with -RawReviewPath"
    }
    "external-cli-mcp" {
        $flowSummary += "- export: none"
        $flowSummary += "- operator_step: send the packet to the chosen CLI or MCP reviewer"
        $flowSummary += "- operator_step: save raw reviewer output to a file and rerun this flow with -RawReviewPath"
    }
}

if (-not [string]::IsNullOrWhiteSpace($RawReviewPath)) {
    $resolvedRawReviewPath = (Resolve-Path -LiteralPath $RawReviewPath).Path
    $scopeLabel = switch ($ScopeType) {
        "CommitRange" { "commit-range: $ScopeValue" }
        "Path" { "path: $ScopeValue" }
        "Manual" {
            if ([string]::IsNullOrWhiteSpace($ScopeValue)) {
                "manual-question"
            }
            else {
                "manual-question: $ScopeValue"
            }
        }
        "Staged" { "staged" }
        default { "working-tree" }
    }

    $normalizeSplat = @{
        RawReviewPath = $resolvedRawReviewPath
        AuditMode = $Mode
        ProjectPath = $resolvedTargetProject
        Scope = $scopeLabel
        Reference = $Reference
        Disposition = $Disposition
        NextAction = $NextAction
    }

    if (-not [string]::IsNullOrWhiteSpace($ReportPath)) {
        $normalizeSplat["OutputPath"] = $ReportPath
    }

    $reportOutput = & $normalizeScript @normalizeSplat
    $flowSummary += "- normalized_report: $reportOutput"
}
else {
    $flowSummary += "- normalized_report: skipped"
}

Write-Output ($flowSummary -join [Environment]::NewLine)
