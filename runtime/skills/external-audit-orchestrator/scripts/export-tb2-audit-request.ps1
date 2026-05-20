[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$SkillRoot,

    [Parameter(Mandatory = $true)]
    [string]$TargetProject,

    [Parameter(Mandatory = $true)]
    [string]$AuditPacketPath,

    [string]$OutputPath,

    [switch]$Apply
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$resolvedSkillRoot = (Resolve-Path -LiteralPath $SkillRoot).Path
$resolvedTargetProject = (Resolve-Path -LiteralPath $TargetProject).Path
$resolvedAuditPacketPath = (Resolve-Path -LiteralPath $AuditPacketPath).Path

$templatePath = Join-Path -Path $resolvedSkillRoot -ChildPath "assets\tb2\tb2-audit-request.template.json"
if (-not (Test-Path -LiteralPath $templatePath)) {
    throw "Missing TB2 request template: $templatePath"
}

if ([string]::IsNullOrWhiteSpace($OutputPath)) {
    $OutputPath = Join-Path -Path $resolvedTargetProject -ChildPath ".audit\tb2\request.json"
}

$templateText = [System.IO.File]::ReadAllText($templatePath)
$auditPacketText = [System.IO.File]::ReadAllText($resolvedAuditPacketPath)
$escapedPacketJson = ConvertTo-Json -InputObject $auditPacketText -Compress
$escapedPacketJsonValue = $escapedPacketJson.Substring(1, $escapedPacketJson.Length - 2)
$requestText = $templateText.Replace("{{AUDIT_PACKET}}", $escapedPacketJsonValue)

$modeLabel = if ($Apply) { "apply" } else { "dry-run" }
$plan = @(
    "TB2 audit request export plan",
    "- target_project: $resolvedTargetProject",
    "- audit_packet: $resolvedAuditPacketPath",
    "- output_path: $OutputPath",
    "- mode: $modeLabel",
    "- action: materialize TB2 request template with embedded audit packet",
    "- note: TB2 mode is template-only in v0.1.x until reviewer profile validation is complete"
)

Write-Output ($plan -join [Environment]::NewLine)

if (-not $Apply) {
    Write-Output ""
    Write-Output "Dry-run only. Re-run with -Apply to write files."
    return
}

$outputDirectory = Split-Path -Path $OutputPath -Parent
New-Item -ItemType Directory -Force -Path $outputDirectory | Out-Null
[System.IO.File]::WriteAllText($OutputPath, $requestText + [Environment]::NewLine, [System.Text.Encoding]::UTF8)

Write-Output ""
Write-Output "Applied TB2 audit request export."
