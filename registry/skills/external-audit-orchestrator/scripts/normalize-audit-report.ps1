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

$criticalBlock = Get-SectionContent -Text $rawText -SectionNames @("Critical")
$warningBlock = Get-SectionContent -Text $rawText -SectionNames @("Warning", "Warnings")
$suggestionBlock = Get-SectionContent -Text $rawText -SectionNames @("Suggestion", "Suggestions")
$assumptionBlock = Get-SectionContent -Text $rawText -SectionNames @("Assumptions")

$referenceLines = if ($Reference.Count -gt 0) {
    $Reference | ForEach-Object { Convert-ReferenceEntry -Entry $_ }
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
