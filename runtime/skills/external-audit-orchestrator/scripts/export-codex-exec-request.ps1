[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$SkillRoot,

    [Parameter(Mandatory = $true)]
    [string]$TargetProject,

    [Parameter(Mandatory = $true)]
    [string]$AuditPacketPath,

    [string]$OutputDirectory,

    [string]$CodexCommand = "codex",

    [ValidateSet("", "Y", "N", "O")]
    [string]$StartupGateAnswer = "",

    [ValidateSet("read-only", "workspace-write", "danger-full-access")]
    [string]$Sandbox = "read-only",

    [switch]$Apply
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function ConvertTo-PowerShellSingleQuotedLiteral {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Value
    )

    return "'" + $Value.Replace("'", "''") + "'"
}

$resolvedSkillRoot = (Resolve-Path -LiteralPath $SkillRoot).Path
$resolvedTargetProject = (Resolve-Path -LiteralPath $TargetProject).Path
$resolvedAuditPacketPath = (Resolve-Path -LiteralPath $AuditPacketPath).Path

$schemaAssetPath = Join-Path -Path $resolvedSkillRoot -ChildPath "assets\codex\audit-report.schema.json"
if (-not (Test-Path -LiteralPath $schemaAssetPath)) {
    throw "Missing Codex exec schema asset: $schemaAssetPath"
}

if ([string]::IsNullOrWhiteSpace($OutputDirectory)) {
    $OutputDirectory = Join-Path -Path $resolvedTargetProject -ChildPath ".audit\codex-exec"
}

$resolvedOutputDirectory = if (Test-Path -LiteralPath $OutputDirectory) {
    (Resolve-Path -LiteralPath $OutputDirectory).Path
}
else {
    [System.IO.Path]::GetFullPath($OutputDirectory)
}

$promptPath = Join-Path -Path $resolvedOutputDirectory -ChildPath "prompt.md"
$schemaPath = Join-Path -Path $resolvedOutputDirectory -ChildPath "audit-report.schema.json"
$runnerPath = Join-Path -Path $resolvedOutputDirectory -ChildPath "run-codex-exec-audit.ps1"
$rawReviewPath = Join-Path -Path $resolvedOutputDirectory -ChildPath "raw-review.json"

$auditPacketText = [System.IO.File]::ReadAllText($resolvedAuditPacketPath)
$startupGateText = if ([string]::IsNullOrWhiteSpace($StartupGateAnswer)) {
    "If active project instructions require a first-turn startup gate and no operator answer is supplied, stop and report that the gate blocks the non-interactive audit."
}
else {
    "Operator startup gate answer: $StartupGateAnswer. Use it only when permitted by active instruction priority; if higher-priority instructions still require a live answer, stop and report the blocker."
}

$promptText = @"
Read-only engineering audit. Review the audit packet below.

Return only the final JSON object that conforms to audit-report.schema.json.
Order findings by severity and preserve explicit Reference Inputs Used when any local project, official documentation, public repository, article, or obvious reference shaped the audit.

$startupGateText

# Audit Packet

$auditPacketText
"@

$codexCommandLiteral = ConvertTo-PowerShellSingleQuotedLiteral -Value $CodexCommand
$sandboxLiteral = ConvertTo-PowerShellSingleQuotedLiteral -Value $Sandbox
$targetProjectLiteral = ConvertTo-PowerShellSingleQuotedLiteral -Value $resolvedTargetProject
$runnerText = @'
[CmdletBinding()]
param(
    [string]$CodexCommand = __CODEX_COMMAND_LITERAL__,
    [ValidateSet("read-only", "workspace-write", "danger-full-access")]
    [string]$Sandbox = __SANDBOX_LITERAL__,
    [switch]$IgnoreUserConfig
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$targetProject = __TARGET_PROJECT_LITERAL__
$promptPath = Join-Path -Path $PSScriptRoot -ChildPath "prompt.md"
$schemaPath = Join-Path -Path $PSScriptRoot -ChildPath "audit-report.schema.json"
$rawReviewPath = Join-Path -Path $PSScriptRoot -ChildPath "raw-review.json"

foreach ($requiredPath in @($promptPath, $schemaPath, $targetProject)) {
    if (-not (Test-Path -LiteralPath $requiredPath)) {
        throw "Missing required path: $requiredPath"
    }
}

$prompt = Get-Content -LiteralPath $promptPath -Raw

$codexExecutable = if (Test-Path -LiteralPath $CodexCommand -PathType Leaf) {
    (Resolve-Path -LiteralPath $CodexCommand).Path
}
else {
    $application = Get-Command -Name $CodexCommand -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
    if (-not $application) {
        throw "Codex executable not found for command: $CodexCommand"
    }

    $application.Source
}

$codexArgs = @(
    "exec",
    "--cd", $targetProject,
    "--sandbox", $Sandbox,
    "--ignore-rules",
    "--output-schema", $schemaPath,
    "--output-last-message", $rawReviewPath
)

if ($IgnoreUserConfig) {
    $codexArgs += "--ignore-user-config"
}

$codexArgs += "-"

$prompt | & $codexExecutable @codexArgs

if ($LASTEXITCODE -ne 0) {
    throw "codex exec failed with exit code $LASTEXITCODE"
}

Write-Output "Codex exec audit completed."
Write-Output "Raw review: $rawReviewPath"
'@

$runnerText = $runnerText.Replace("__CODEX_COMMAND_LITERAL__", $codexCommandLiteral)
$runnerText = $runnerText.Replace("__SANDBOX_LITERAL__", $sandboxLiteral)
$runnerText = $runnerText.Replace("__TARGET_PROJECT_LITERAL__", $targetProjectLiteral)

$modeLabel = if ($Apply) { "apply" } else { "dry-run" }
$plan = @(
    "Codex exec audit export plan",
    "- target_project: $resolvedTargetProject",
    "- audit_packet: $resolvedAuditPacketPath",
    "- output_directory: $resolvedOutputDirectory",
    "- prompt_path: $promptPath",
    "- schema_path: $schemaPath",
    "- runner_path: $runnerPath",
    "- raw_review: $rawReviewPath",
    "- codex_command: $CodexCommand",
    "- startup_gate_answer: $StartupGateAnswer",
    "- sandbox: $Sandbox",
    "- mode: $modeLabel",
    "- action: materialize Codex non-interactive audit prompt, schema, and runner"
)

Write-Output ($plan -join [Environment]::NewLine)

if (-not $Apply) {
    Write-Output ""
    Write-Output "Dry-run only. Re-run with -Apply to write files."
    return
}

New-Item -ItemType Directory -Force -Path $resolvedOutputDirectory | Out-Null
[System.IO.File]::WriteAllText($promptPath, $promptText + [Environment]::NewLine, [System.Text.Encoding]::UTF8)
Copy-Item -LiteralPath $schemaAssetPath -Destination $schemaPath -Force
[System.IO.File]::WriteAllText($runnerPath, $runnerText + [Environment]::NewLine, [System.Text.Encoding]::UTF8)

Write-Output ""
Write-Output "Applied Codex exec audit export."
