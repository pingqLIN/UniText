[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$EvidencePath,

    [string]$OutputPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Assert-Property {
    param(
        [Parameter(Mandatory = $true)]
        [object]$Object,

        [Parameter(Mandatory = $true)]
        [string]$Name
    )

    if ($null -eq $Object.PSObject.Properties[$Name]) {
        throw "TB2 execution evidence is missing required property: $Name"
    }
}

function ConvertTo-ReferenceEntry {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Target,

        [Parameter(Mandatory = $true)]
        [string]$Reason
    )

    return "local-project|$Target|$Reason"
}

$resolvedEvidencePath = (Resolve-Path -LiteralPath $EvidencePath).ProviderPath
$evidence = Get-Content -LiteralPath $resolvedEvidencePath -Raw | ConvertFrom-Json

foreach ($name in @("export_type", "normalized_audit_report", "boundary", "workstream", "messages", "audit_events", "audit")) {
    Assert-Property -Object $evidence -Name $name
}

if ($evidence.export_type -ne "tb2_execution_evidence") {
    throw "Unsupported TB2 evidence export_type: $($evidence.export_type)"
}

if ($evidence.normalized_audit_report -ne $false) {
    throw "TB2 evidence must not claim to be a normalized audit report."
}

$workstream = $evidence.workstream
foreach ($name in @("workstream_id", "bridge_id", "room_id", "state", "health", "topology", "dependency")) {
    Assert-Property -Object $workstream -Name $name
}

$messages = @($evidence.messages)
$auditEvents = @($evidence.audit_events)
$request = $messages | Where-Object { $_.kind -eq "review_request" } | Select-Object -First 1
if ($null -eq $request) {
    throw "TB2 evidence does not include a review_request message."
}

$health = $workstream.health
$audit = $evidence.audit
$referenceReason = "TB2 execution evidence contract sample; confirms TB2 supplies transport evidence only"
$reference = ConvertTo-ReferenceEntry -Target $resolvedEvidencePath -Reason $referenceReason
$scopeValue = "tb2 execution evidence: $($workstream.workstream_id)/$($workstream.room_id)"
$summary = "Adapt TB2 execution evidence for external-audit-orchestrator without importing orchestrator packet logic into TB2."
$checks = @(
    "TB2 sample export_type is tb2_execution_evidence.",
    "TB2 sample normalized_audit_report is false.",
    "TB2 boundary states: $($evidence.boundary)",
    "Workstream $($workstream.workstream_id) is $($workstream.state) with health $($health.state).",
    "Topology room_present=$($workstream.topology.room_present), bridge_present=$($workstream.topology.bridge_present), orphaned=$($workstream.topology.orphaned).",
    "Dependency child_count=$($workstream.dependency.child_count), blocked=$($workstream.dependency.blocked).",
    "Review request message $($request.event_id) came from $($request.author) with trusted=$($request.trusted).",
    "Audit event count is $($auditEvents.Count).",
    "Audit redaction stores_raw_text=$($audit.redaction.stores_raw_text), stores_masked_placeholders=$($audit.redaction.stores_masked_placeholders)."
)
$questions = @(
    "Can external-audit-orchestrator turn this TB2 execution evidence into an internal evidence input?",
    "Does the orchestrator, not TB2, still produce the reviewer request JSON, expected schema, and normalized report?"
)
$rawReviewMarkdown = @"
Critical
- none

Warning
- none

Suggestion
- Keep TB2 limited to execution evidence and keep reviewer request JSON, expected schema, and normalized reports in external-audit-orchestrator.

Assumptions
- This sample is contract evidence, not a live reviewer transcript.

Reference Inputs Used
- local-project: $resolvedEvidencePath - $referenceReason
"@

$adapted = [ordered]@{
    contract_type = "orchestrator_evidence_input"
    source = [ordered]@{
        kind = "local-project"
        target = $resolvedEvidencePath
        reason = $referenceReason
    }
    scope_type = "Manual"
    scope_value = $scopeValue
    summary = $summary
    questions = $questions
    checks = $checks
    references = @($reference)
    raw_review_markdown = $rawReviewMarkdown
    artifacts = [ordered]@{
        reviewer_request_json = "orchestrator-owned"
        expected_schema = "orchestrator-owned"
        normalized_report = "orchestrator-owned"
    }
}

$json = $adapted | ConvertTo-Json -Depth 8
if ([string]::IsNullOrWhiteSpace($OutputPath)) {
    Write-Output $json
    return
}

$outputDirectory = Split-Path -Path $OutputPath -Parent
if (-not [string]::IsNullOrWhiteSpace($outputDirectory)) {
    New-Item -ItemType Directory -Force -Path $outputDirectory | Out-Null
}

[System.IO.File]::WriteAllText($OutputPath, $json + [Environment]::NewLine, [System.Text.Encoding]::UTF8)
Write-Output $OutputPath
