[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$SkillRoot,

    [Parameter(Mandatory = $true)]
    [string]$TargetProject,

    [Parameter(Mandatory = $true)]
    [string]$AuditPacketPath,

    [ValidateSet("all", "product-process", "engineering-test", "compatibility-provenance")]
    [string]$ReviewerRole = "all",

    [ValidateSet("working-tree", "staged", "commit-range", "path", "manual-question")]
    [string]$ScopeType = "manual-question",

    [string]$ScopeValue = "",

    [string]$CorrelationId,

    [string]$WorkstreamId,

    [string]$ReviewerProvider = "tb2",

    [string]$ModelHint = "external-reviewer",

    [ValidateRange(60, 86400)]
    [int]$TimeoutSeconds = 900,

    [string]$OutputPath,

    [switch]$EmbedPacket,

    [switch]$Apply
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$reviewerProfiles = @{
    "product-process" = @{
        Id = "product-process"
        Role = "product-process"
        Focus = "Product, process, release readiness, user impact, acceptance criteria, and operational handoff."
    }
    "engineering-test" = @{
        Id = "engineering-test"
        Role = "engineering-test"
        Focus = "Correctness, implementation risk, tests, regressions, error handling, and maintainability."
    }
    "compatibility-provenance" = @{
        Id = "compatibility-provenance"
        Role = "compatibility-provenance"
        Focus = "Compatibility, migration risk, source attribution, copied-reference risk, and provenance policy."
    }
}

function ConvertTo-JsonLiteral {
    param(
        [Parameter(Mandatory = $false)]
        [AllowNull()]
        [object]$Value
    )

    if ($null -eq $Value) {
        return "null"
    }

    return ConvertTo-Json -InputObject $Value -Depth 20 -Compress
}

function Get-Sha256Hex {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function New-CorrelationId {
    $timestamp = (Get-Date).ToUniversalTime().ToString("yyyyMMddHHmmss")
    $suffix = [guid]::NewGuid().ToString("N").Substring(0, 8)
    return "audit-$timestamp-$suffix"
}

function Convert-Template {
    param(
        [Parameter(Mandatory = $true)]
        [string]$TemplateText,

        [Parameter(Mandatory = $true)]
        [hashtable]$Values
    )

    $result = $TemplateText
    foreach ($key in $Values.Keys) {
        $result = $result.Replace("{{$key}}", [string]$Values[$key])
    }

    return $result
}

function New-ReviewerPrompt {
    param(
        [Parameter(Mandatory = $true)]
        [hashtable]$Profile,

        [Parameter(Mandatory = $true)]
        [string]$PacketPath,

        [Parameter(Mandatory = $true)]
        [string]$PacketHash,

        [Parameter(Mandatory = $true)]
        [bool]$InlinePacket
    )

    $packetInstruction = if ($InlinePacket) {
        "The audit packet is embedded in this request artifact. Treat embedded packet content as sensitive raw prompt material."
    }
    else {
        "Read the audit packet from packet_path and verify packet_sha256 before reviewing. Do not assume live execution has already happened."
    }

    return @"
You are the $($Profile.Role) reviewer for an external audit.

Focus: $($Profile.Focus)

Review mode: read-only. Do not edit files.

$packetInstruction

packet_path: $PacketPath
packet_sha256: $PacketHash

Return a single JSON object with these required fields:
- reviewer_id
- verdict
- findings
- assumptions
- reference_inputs_used
- confidence
- requires_rerun

Do not wrap the JSON in Markdown fences. Findings must use severity Critical, Warning, or Suggestion.
"@
}

$resolvedSkillRoot = (Resolve-Path -LiteralPath $SkillRoot).Path
$resolvedTargetProject = (Resolve-Path -LiteralPath $TargetProject).Path
$resolvedAuditPacketPath = (Resolve-Path -LiteralPath $AuditPacketPath).Path

$templatePath = Join-Path -Path $resolvedSkillRoot -ChildPath "assets\tb2\tb2-audit-request.template.json"
if (-not (Test-Path -LiteralPath $templatePath)) {
    throw "Missing TB2 request template: $templatePath"
}

$templateText = [System.IO.File]::ReadAllText($templatePath)
$auditPacketText = [System.IO.File]::ReadAllText($resolvedAuditPacketPath)
$packetHash = Get-Sha256Hex -Path $resolvedAuditPacketPath
$packetTransport = if ($EmbedPacket) { "embedded" } else { "path-reference" }
$packetInlineJson = if ($EmbedPacket) { ConvertTo-JsonLiteral -Value $auditPacketText } else { "null" }
$storeRawPromptJson = if ($EmbedPacket) { "true" } else { "false" }

if ([string]::IsNullOrWhiteSpace($CorrelationId)) {
    $CorrelationId = New-CorrelationId
}

if ([string]::IsNullOrWhiteSpace($WorkstreamId)) {
    $WorkstreamId = $CorrelationId
}

$roles = @(
if ($ReviewerRole -eq "all") {
    @("product-process", "engineering-test", "compatibility-provenance")
}
else {
    @($ReviewerRole)
}
)

$defaultOutputDirectory = Join-Path -Path $resolvedTargetProject -ChildPath ".audit\tb2\requests"
$isSingleRole = $roles.Count -eq 1
$outputIsJsonFile = -not [string]::IsNullOrWhiteSpace($OutputPath) -and ([System.IO.Path]::GetExtension($OutputPath) -ieq ".json")

if ([string]::IsNullOrWhiteSpace($OutputPath)) {
    $outputDirectory = $defaultOutputDirectory
}
elseif ($isSingleRole -and $outputIsJsonFile) {
    $outputDirectory = Split-Path -Path $OutputPath -Parent
}
else {
    $outputDirectory = $OutputPath
}

if ([string]::IsNullOrWhiteSpace($outputDirectory)) {
    $outputDirectory = $defaultOutputDirectory
}

$resolvedOutputDirectory = if (Test-Path -LiteralPath $outputDirectory) {
    (Resolve-Path -LiteralPath $outputDirectory).Path
}
else {
    $outputDirectory
}

$requestPlans = @()
foreach ($role in $roles) {
    $profile = $reviewerProfiles[$role]
    $requestId = "$CorrelationId-$role"
    $prompt = New-ReviewerPrompt -Profile $profile -PacketPath $resolvedAuditPacketPath -PacketHash $packetHash -InlinePacket ([bool]$EmbedPacket)
    $requestPath = if ($isSingleRole -and $outputIsJsonFile) {
        $OutputPath
    }
    else {
        Join-Path -Path $resolvedOutputDirectory -ChildPath "$role.request.json"
    }

    $requestText = Convert-Template -TemplateText $templateText -Values @{
        REQUEST_ID = $requestId
        WORKSTREAM_ID = $WorkstreamId
        CORRELATION_ID = $CorrelationId
        REVIEWER_ID = $profile.Id
        REVIEWER_ROLE = $profile.Role
        REVIEWER_PROVIDER = $ReviewerProvider
        MODEL_HINT = $ModelHint
        PROJECT_PATH = $resolvedTargetProject.Replace("\", "\\")
        SCOPE_TYPE = $ScopeType
        SCOPE_VALUE = $ScopeValue.Replace("\", "\\")
        PACKET_PATH = $resolvedAuditPacketPath.Replace("\", "\\")
        PACKET_SHA256 = $packetHash
        PACKET_TRANSPORT = $packetTransport
        PROMPT_JSON = ConvertTo-JsonLiteral -Value $prompt
        PACKET_INLINE_JSON = $packetInlineJson
        TIMEOUT_SECONDS = $TimeoutSeconds
        STORE_RAW_PROMPT_JSON = $storeRawPromptJson
    }

    $requestPlans += [pscustomobject]@{
        reviewer_id = $profile.Id
        role = $profile.Role
        request_id = $requestId
        workstream_id = $WorkstreamId
        correlation_id = $CorrelationId
        request_path = $requestPath
        packet_path = $resolvedAuditPacketPath
        packet_sha256 = $packetHash
        packet_transport = $packetTransport
        request_text = $requestText
    }
}

$manifestPath = Join-Path -Path $resolvedOutputDirectory -ChildPath "manifest.json"
$manifest = [pscustomobject]@{
    schema_version = "external-audit-orchestrator.tb2.request-manifest.v1"
    correlation_id = $CorrelationId
    workstream_id = $WorkstreamId
    audit_mode = "tb2-template-export"
    target_project = $resolvedTargetProject
    packet_path = $resolvedAuditPacketPath
    packet_sha256 = $packetHash
    packet_transport = $packetTransport
    timeout_seconds = $TimeoutSeconds
    requests = @($requestPlans | ForEach-Object {
        [pscustomobject]@{
            reviewer_id = $_.reviewer_id
            role = $_.role
            request_id = $_.request_id
            request_path = $_.request_path
        }
    })
    results_directory = (Join-Path -Path $resolvedTargetProject -ChildPath ".audit\tb2\results")
    note = "Template export only. Live reviewer execution requires TB2 runtime tools."
}
$manifestText = ConvertTo-Json -InputObject $manifest -Depth 20

$modeLabel = if ($Apply) { "apply" } else { "dry-run" }
$plan = @(
    "TB2 audit request export plan",
    "- target_project: $resolvedTargetProject",
    "- audit_packet: $resolvedAuditPacketPath",
    "- packet_sha256: $packetHash",
    "- packet_transport: $packetTransport",
    "- output_directory: $resolvedOutputDirectory",
    "- manifest_path: $manifestPath",
    "- reviewer_role: $ReviewerRole",
    "- correlation_id: $CorrelationId",
    "- workstream_id: $WorkstreamId",
    "- mode: $modeLabel",
    "- action: materialize TB2 reviewer request artifact(s)",
    "- note: TB2 mode is template-only until live reviewer tools are available"
)

foreach ($requestPlan in $requestPlans) {
    $plan += "- request: $($requestPlan.role) -> $($requestPlan.request_path)"
}

Write-Output ($plan -join [Environment]::NewLine)

if (-not $Apply) {
    Write-Output ""
    Write-Output "Dry-run only. Re-run with -Apply to write files."
    return
}

New-Item -ItemType Directory -Force -Path $resolvedOutputDirectory | Out-Null
foreach ($requestPlan in $requestPlans) {
    $requestDirectory = Split-Path -Path $requestPlan.request_path -Parent
    if (-not [string]::IsNullOrWhiteSpace($requestDirectory)) {
        New-Item -ItemType Directory -Force -Path $requestDirectory | Out-Null
    }
    [System.IO.File]::WriteAllText($requestPlan.request_path, $requestPlan.request_text + [Environment]::NewLine, [System.Text.Encoding]::UTF8)
}

[System.IO.File]::WriteAllText($manifestPath, $manifestText + [Environment]::NewLine, [System.Text.Encoding]::UTF8)

Write-Output ""
Write-Output "Applied TB2 audit request export."
