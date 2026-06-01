[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$RawReviewPath,

    [Parameter(Mandatory = $true)]
    [string]$AuditMode,

    [Parameter(Mandatory = $true)]
    [string]$ProjectPath,

    [Parameter(Mandatory = $true)]
    [string]$Scope,

    [ValidateSet("passed", "failed", "partial", "unavailable")]
    [string]$AuditGate = "failed",

    [string]$ReviewerId = "",

    [string]$CommandOrRoute = "",

    [string]$RawStdoutPath = "",

    [string]$RawStderrPath = "",

    [string]$ExitCodeOrTimeout = "",

    [string]$UnavailableReason = "",

    [ValidateSet("yes", "no", "unknown")]
    [string]$SubstantiveFindingsCaptured = "unknown",

    [string[]]$Reference = @(),

    [ValidateSet("accept", "fix-and-rerun", "escalate-to-human", "archive-only")]
    [string]$Disposition = "fix-and-rerun",

    [string]$NextAction = "Review the findings, apply required fixes, and rerun the audit if any warning or higher issue was accepted.",

    [string]$OutputPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Convert-ReferenceEntry {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Entry
    )

    $parts = $Entry.Split("|", 3)
    if ($parts.Count -lt 3) {
        return "- unclassified: $Entry"
    }

    return "- $($parts[0].Trim()): $($parts[1].Trim()) - $($parts[2].Trim())"
}

function Convert-ReportValue {
    param(
        [AllowEmptyString()]
        [string]$Value
    )

    if ([string]::IsNullOrWhiteSpace($Value)) {
        return "none"
    }

    return $Value
}

function Resolve-OptionalPathValue {
    param(
        [AllowEmptyString()]
        [string]$PathValue
    )

    if ([string]::IsNullOrWhiteSpace($PathValue)) {
        return ""
    }

    if (Test-Path -LiteralPath $PathValue) {
        return (Resolve-Path -LiteralPath $PathValue).Path
    }

    return $PathValue
}

function Get-JsonPropertyValue {
    param(
        [Parameter(Mandatory = $true)]
        [object]$Object,

        [Parameter(Mandatory = $true)]
        [string]$Name
    )

    $property = $Object.PSObject.Properties[$Name]
    if ($null -eq $property) {
        return $null
    }

    return $property.Value
}

function Convert-FindingArrayToMarkdown {
    param(
        [AllowNull()]
        [object]$Findings
    )

    if ($null -eq $Findings) {
        return "- none"
    }

    $items = @($Findings)
    if ($items.Count -eq 0) {
        return "- none"
    }

    $lines = foreach ($finding in $items) {
        if ($finding -is [string]) {
            "- $finding"
            continue
        }

        $title = [string](Get-JsonPropertyValue -Object $finding -Name "title")
        $location = [string](Get-JsonPropertyValue -Object $finding -Name "location")
        $risk = [string](Get-JsonPropertyValue -Object $finding -Name "risk")
        $recommendedAction = [string](Get-JsonPropertyValue -Object $finding -Name "recommended_action")

        if ([string]::IsNullOrWhiteSpace($title)) {
            $title = "untitled finding"
        }

        "- $title | location: $(Convert-ReportValue -Value $location) | risk: $(Convert-ReportValue -Value $risk) | recommended_action: $(Convert-ReportValue -Value $recommendedAction)"
    }

    return ($lines -join [Environment]::NewLine)
}

function Convert-StringArrayToMarkdown {
    param(
        [AllowNull()]
        [object]$Items
    )

    if ($null -eq $Items) {
        return "- none"
    }

    $values = @(@($Items) | ForEach-Object { [string]$_ } | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
    if ($values.Count -eq 0) {
        return "- none"
    }

    return (($values | ForEach-Object { "- $_" }) -join [Environment]::NewLine)
}

function Convert-JsonReferencesToLines {
    param(
        [AllowNull()]
        [object]$References
    )

    if ($null -eq $References) {
        return @("- none")
    }

    $items = @($References)
    if ($items.Count -eq 0) {
        return @("- none")
    }

    $lines = foreach ($reference in $items) {
        if ($reference -is [string]) {
            "- unclassified: $reference"
            continue
        }

        $kind = [string](Get-JsonPropertyValue -Object $reference -Name "kind")
        $target = [string](Get-JsonPropertyValue -Object $reference -Name "target")
        $reason = [string](Get-JsonPropertyValue -Object $reference -Name "reason")
        "- $(Convert-ReportValue -Value $kind): $(Convert-ReportValue -Value $target) - $(Convert-ReportValue -Value $reason)"
    }

    return @($lines)
}

function Test-JsonHasSubstantiveVerdict {
    param(
        [Parameter(Mandatory = $true)]
        [object]$Review
    )

    foreach ($name in @("critical", "warning", "suggestion")) {
        if ($null -ne (Get-JsonPropertyValue -Object $Review -Name $name)) {
            return $true
        }
    }

    foreach ($name in @("disposition", "summary", "next_action")) {
        $value = [string](Get-JsonPropertyValue -Object $Review -Name $name)
        if (-not [string]::IsNullOrWhiteSpace($value)) {
            return $true
        }
    }

    return $false
}

function Test-MarkdownHasSubstantiveVerdict {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Text
    )

    $hasFindingSection = [regex]::IsMatch($Text, "(?im)^\s*(#+\s*)?(Critical|Warnings?|Suggestions?)\s*:?\s*$")
    if ($hasFindingSection) {
        return $true
    }

    $hasExplicitNoFindings = [regex]::IsMatch($Text, "(?im)\b(no findings|no issues|no blocking findings|nothing to report)\b")
    if ($hasExplicitNoFindings) {
        return $true
    }

    return $false
}

function Get-SectionContent {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Text,

        [Parameter(Mandatory = $true)]
        [string[]]$SectionNames
    )

    $joinedNames = ($SectionNames | ForEach-Object { [regex]::Escape($_) }) -join "|"
    $boundaryNames = "Critical|Warning|Warnings|Suggestion|Suggestions|Assumptions|Reference Inputs Used"
    $pattern = "(?ms)^[#\-\*\s]*?(?:$joinedNames)\s*:?\s*$\r?\n(.*?)(?=^[#\-\*\s]*?(?:$boundaryNames)\s*:?\s*$|\z)"
    $match = [regex]::Match($Text, $pattern)
    if ($match.Success) {
        $value = $match.Groups[1].Value.Trim()
        if (-not [string]::IsNullOrWhiteSpace($value)) {
            return $value
        }
    }

    return "- none"
}

$resolvedRawReviewPath = (Resolve-Path -LiteralPath $RawReviewPath).Path
$resolvedProjectPath = (Resolve-Path -LiteralPath $ProjectPath).Path
$rawText = Get-Content -LiteralPath $resolvedRawReviewPath -Raw
$projectName = Split-Path -Path $resolvedProjectPath -Leaf

if ($AuditGate -ne "passed" -and $Disposition -eq "accept") {
    throw "Disposition 'accept' is only valid when AuditGate is 'passed'."
}

$resolvedRawStdoutPath = Resolve-OptionalPathValue -PathValue $RawStdoutPath
$resolvedRawStderrPath = Resolve-OptionalPathValue -PathValue $RawStderrPath
$reviewerIdValue = if ([string]::IsNullOrWhiteSpace($ReviewerId)) { $AuditMode } else { $ReviewerId }

$jsonReview = $null
try {
    $jsonReview = $rawText | ConvertFrom-Json -ErrorAction Stop
}
catch {
    $jsonReview = $null
}

$hasSubstantiveVerdict = if ($null -ne $jsonReview) {
    Test-JsonHasSubstantiveVerdict -Review $jsonReview
}
else {
    Test-MarkdownHasSubstantiveVerdict -Text $rawText
}

if ($AuditGate -eq "passed" -and -not $hasSubstantiveVerdict) {
    throw "AuditGate 'passed' requires raw reviewer output with findings or an explicit no-findings verdict."
}

if ($SubstantiveFindingsCaptured -eq "unknown") {
    $SubstantiveFindingsCaptured = if ($AuditGate -in @("passed", "partial")) { "yes" } else { "no" }
}

$criticalBlock = if ($null -ne $jsonReview) {
    Convert-FindingArrayToMarkdown -Findings (Get-JsonPropertyValue -Object $jsonReview -Name "critical")
}
else {
    Get-SectionContent -Text $rawText -SectionNames @("Critical")
}

$warningBlock = if ($null -ne $jsonReview) {
    Convert-FindingArrayToMarkdown -Findings (Get-JsonPropertyValue -Object $jsonReview -Name "warning")
}
else {
    Get-SectionContent -Text $rawText -SectionNames @("Warning", "Warnings")
}

$suggestionBlock = if ($null -ne $jsonReview) {
    Convert-FindingArrayToMarkdown -Findings (Get-JsonPropertyValue -Object $jsonReview -Name "suggestion")
}
else {
    Get-SectionContent -Text $rawText -SectionNames @("Suggestion", "Suggestions")
}

$assumptionBlock = if ($null -ne $jsonReview) {
    Convert-StringArrayToMarkdown -Items (Get-JsonPropertyValue -Object $jsonReview -Name "assumptions")
}
else {
    Get-SectionContent -Text $rawText -SectionNames @("Assumptions")
}

$referenceLines = if ($Reference.Count -gt 0) {
    $Reference | ForEach-Object { Convert-ReferenceEntry -Entry $_ }
}
elseif ($null -ne $jsonReview) {
    Convert-JsonReferencesToLines -References (Get-JsonPropertyValue -Object $jsonReview -Name "reference_inputs_used")
}
else {
    @("- none")
}

if ([string]::IsNullOrWhiteSpace($OutputPath)) {
    $slug = Get-Date -Format "yyyyMMdd-HHmmss"
    $OutputPath = Join-Path -Path $resolvedProjectPath -ChildPath "audit-report-$slug.md"
}

$reviewedAt = Get-Date -Format s
$reportText = @"
# Audit Report

## Audit Mode

$AuditMode

## Audit Gate

- classification: $AuditGate
- reviewer_id: $(Convert-ReportValue -Value $reviewerIdValue)
- command_or_route: $(Convert-ReportValue -Value $CommandOrRoute)
- raw_review: $resolvedRawReviewPath
- raw_stdout: $(Convert-ReportValue -Value $resolvedRawStdoutPath)
- raw_stderr: $(Convert-ReportValue -Value $resolvedRawStderrPath)
- exit_code_or_timeout: $(Convert-ReportValue -Value $ExitCodeOrTimeout)
- unavailable_reason: $(Convert-ReportValue -Value $UnavailableReason)
- substantive_findings_captured: $SubstantiveFindingsCaptured

## Scope

- project: $projectName
- path: $resolvedProjectPath
- scope: $Scope
- reviewed_at: $reviewedAt
- raw_review: $resolvedRawReviewPath

## Reference Inputs

$($referenceLines -join [Environment]::NewLine)

## Findings

### Critical

$criticalBlock

### Warning

$warningBlock

### Suggestion

$suggestionBlock

## Assumptions

$assumptionBlock

## Disposition

$Disposition

## Next Action

$NextAction
"@

[System.IO.File]::WriteAllText($OutputPath, $reportText, [System.Text.Encoding]::UTF8)
Write-Output $OutputPath
