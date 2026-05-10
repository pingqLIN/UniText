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

    [ValidateSet("auto", "accept", "fix-and-rerun", "escalate-to-human", "archive-only")]
    [string]$Disposition = "auto",

    [string]$NextAction = "",

    [string]$OutputPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$allowedSeverities = @("Critical", "Warning", "Suggestion")
$allowedVerdicts = @("accept", "fix-and-rerun", "escalate-to-human", "archive-only")
$allowedStatuses = @("completed", "timeout", "invalid", "failed")

function Test-Property {
    param(
        [Parameter(Mandatory = $true)]
        [object]$Object,

        [Parameter(Mandatory = $true)]
        [string]$Name
    )

    return ($Object.PSObject.Properties.Name -contains $Name)
}

function Get-PropertyValue {
    param(
        [Parameter(Mandatory = $true)]
        [object]$Object,

        [Parameter(Mandatory = $true)]
        [string]$Name,

        [object]$Default = $null
    )

    if (Test-Property -Object $Object -Name $Name) {
        return $Object.$Name
    }

    return $Default
}

function Convert-ToArray {
    param(
        [AllowNull()]
        [object]$Value
    )

    if ($null -eq $Value) {
        return @()
    }

    return @($Value)
}

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

function Convert-ReferenceInput {
    param(
        [Parameter(Mandatory = $true)]
        [object]$ReferenceInput
    )

    if ($ReferenceInput -is [string]) {
        return "- $ReferenceInput"
    }

    $kind = [string](Get-PropertyValue -Object $ReferenceInput -Name "kind" -Default "unclassified")
    $target = [string](Get-PropertyValue -Object $ReferenceInput -Name "target" -Default "")
    $reason = [string](Get-PropertyValue -Object $ReferenceInput -Name "reason" -Default "")
    return "- ${kind}: ${target} - $reason"
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

function Test-ReviewerResult {
    param(
        [Parameter(Mandatory = $true)]
        [object]$Result
    )

    $required = @(
        "reviewer_id",
        "verdict",
        "findings",
        "assumptions",
        "reference_inputs_used",
        "confidence",
        "requires_rerun"
    )

    $missing = @($required | Where-Object { -not (Test-Property -Object $Result -Name $_) })
    if ($missing.Count -gt 0) {
        return "missing required field(s): $($missing -join ', ')"
    }

    $verdict = [string](Get-PropertyValue -Object $Result -Name "verdict")
    if ($allowedVerdicts -notcontains $verdict) {
        return "invalid verdict: $verdict"
    }

    $confidence = Get-PropertyValue -Object $Result -Name "confidence"
    if (-not ($confidence -is [int] -or $confidence -is [double] -or $confidence -is [decimal])) {
        return "confidence must be numeric"
    }

    if ([double]$confidence -lt 0 -or [double]$confidence -gt 1) {
        return "confidence must be between 0 and 1"
    }

    $requiresRerun = Get-PropertyValue -Object $Result -Name "requires_rerun"
    if (-not ($requiresRerun -is [bool])) {
        return "requires_rerun must be boolean"
    }

    foreach ($finding in (Convert-ToArray -Value (Get-PropertyValue -Object $Result -Name "findings"))) {
        foreach ($field in @("severity", "title", "location", "risk", "recommended_action")) {
            if (-not (Test-Property -Object $finding -Name $field)) {
                return "finding missing required field: $field"
            }
        }

        $severity = [string](Get-PropertyValue -Object $finding -Name "severity")
        if ($allowedSeverities -notcontains $severity) {
            return "invalid finding severity: $severity"
        }
    }

    return $null
}

function New-InvalidWrapper {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ReviewerId,

        [Parameter(Mandatory = $true)]
        [string]$ErrorMessage,

        [string]$RawResultPath = ""
    )

    return [pscustomobject]@{
        reviewer_id = $ReviewerId
        status = "invalid"
        result = $null
        error = $ErrorMessage
        timed_out = $false
        raw_result_path = $RawResultPath
        validated_at = (Get-Date).ToUniversalTime().ToString("o")
    }
}

function Convert-ToResultWrapper {
    param(
        [Parameter(Mandatory = $true)]
        [object]$Item,

        [string]$RawResultPath = ""
    )

    if ((Test-Property -Object $Item -Name "status") -and (Test-Property -Object $Item -Name "result")) {
        $status = [string](Get-PropertyValue -Object $Item -Name "status")
        $reviewerId = [string](Get-PropertyValue -Object $Item -Name "reviewer_id" -Default "unknown-reviewer")
        if ($allowedStatuses -notcontains $status) {
            return New-InvalidWrapper -ReviewerId $reviewerId -ErrorMessage "invalid wrapper status: $status" -RawResultPath $RawResultPath
        }

        $result = Get-PropertyValue -Object $Item -Name "result"
        if ($status -eq "completed") {
            if ($null -eq $result) {
                return New-InvalidWrapper -ReviewerId $reviewerId -ErrorMessage "completed wrapper has null result" -RawResultPath $RawResultPath
            }

            $validationError = Test-ReviewerResult -Result $result
            if ($validationError) {
                return New-InvalidWrapper -ReviewerId $reviewerId -ErrorMessage $validationError -RawResultPath $RawResultPath
            }
        }

        return [pscustomobject]@{
            reviewer_id = $reviewerId
            status = $status
            result = $result
            error = Get-PropertyValue -Object $Item -Name "error" -Default $null
            timed_out = [bool](Get-PropertyValue -Object $Item -Name "timed_out" -Default ($status -eq "timeout"))
            raw_result_path = [string](Get-PropertyValue -Object $Item -Name "raw_result_path" -Default $RawResultPath)
            validated_at = [string](Get-PropertyValue -Object $Item -Name "validated_at" -Default (Get-Date).ToUniversalTime().ToString("o"))
        }
    }

    $reviewerId = [string](Get-PropertyValue -Object $Item -Name "reviewer_id" -Default "unknown-reviewer")
    $validationError = Test-ReviewerResult -Result $Item
    if ($validationError) {
        return New-InvalidWrapper -ReviewerId $reviewerId -ErrorMessage $validationError -RawResultPath $RawResultPath
    }

    return [pscustomobject]@{
        reviewer_id = $reviewerId
        status = "completed"
        result = $Item
        error = $null
        timed_out = $false
        raw_result_path = $RawResultPath
        validated_at = (Get-Date).ToUniversalTime().ToString("o")
    }
}

function Read-JsonWrappersFromFile {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    $rawText = Get-Content -LiteralPath $Path -Raw
    try {
        $json = $rawText | ConvertFrom-Json
    }
    catch {
        return @((New-InvalidWrapper -ReviewerId (Split-Path -Path $Path -LeafBase) -ErrorMessage "invalid JSON: $($_.Exception.Message)" -RawResultPath $Path))
    }

    return @(Convert-ToArray -Value $json | ForEach-Object { Convert-ToResultWrapper -Item $_ -RawResultPath $Path })
}

function Read-ReviewWrappers {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    $item = Get-Item -LiteralPath $Path
    if ($item.PSIsContainer) {
        $files = @(Get-ChildItem -LiteralPath $item.FullName -Filter "*.result.json" -File | Sort-Object Name)
        if ($files.Count -eq 0) {
            return @((New-InvalidWrapper -ReviewerId "results-directory" -ErrorMessage "no *.result.json files found" -RawResultPath $item.FullName))
        }

        return @($files | ForEach-Object { Read-JsonWrappersFromFile -Path $_.FullName })
    }

    if ($item.Extension -ieq ".json") {
        return Read-JsonWrappersFromFile -Path $item.FullName
    }

    $rawText = Get-Content -LiteralPath $item.FullName -Raw
    $legacyResult = [pscustomobject]@{
        reviewer_id = "legacy-markdown"
        verdict = "fix-and-rerun"
        findings = @()
        assumptions = @()
        reference_inputs_used = @()
        confidence = 0.5
        requires_rerun = $true
    }

    foreach ($severity in $allowedSeverities) {
        $sectionNames = if ($severity -eq "Warning") { @("Warning", "Warnings") } elseif ($severity -eq "Suggestion") { @("Suggestion", "Suggestions") } else { @("Critical") }
        $block = Get-SectionContent -Text $rawText -SectionNames $sectionNames
        if ($block -ne "- none") {
            $legacyResult.findings += [pscustomobject]@{
                severity = $severity
                title = "Legacy Markdown $severity finding"
                location = "raw review"
                risk = $block
                recommended_action = "Inspect the legacy Markdown reviewer output."
            }
        }
    }

    $assumptionBlock = Get-SectionContent -Text $rawText -SectionNames @("Assumptions")
    if ($assumptionBlock -ne "- none") {
        $legacyResult.assumptions = @($assumptionBlock)
    }

    return @((Convert-ToResultWrapper -Item $legacyResult -RawResultPath $item.FullName))
}

function Format-Findings {
    param(
        [Parameter(Mandatory = $true)]
        [object[]]$Wrappers,

        [Parameter(Mandatory = $true)]
        [string]$Severity
    )

    $lines = @()
    foreach ($wrapper in $Wrappers) {
        if ($wrapper.status -ne "completed" -or $null -eq $wrapper.result) {
            continue
        }

        foreach ($finding in (Convert-ToArray -Value (Get-PropertyValue -Object $wrapper.result -Name "findings"))) {
            if ([string](Get-PropertyValue -Object $finding -Name "severity") -ne $Severity) {
                continue
            }

            $title = [string](Get-PropertyValue -Object $finding -Name "title")
            $location = [string](Get-PropertyValue -Object $finding -Name "location")
            $risk = [string](Get-PropertyValue -Object $finding -Name "risk")
            $action = [string](Get-PropertyValue -Object $finding -Name "recommended_action")
            $lines += "- [$($wrapper.reviewer_id)] $title"
            $lines += "  - location: $location"
            $lines += "  - risk: $risk"
            $lines += "  - recommended action: $action"
        }
    }

    if ($lines.Count -eq 0) {
        return "- none"
    }

    return ($lines -join [Environment]::NewLine)
}

function Get-ReviewerStatusBlock {
    param(
        [Parameter(Mandatory = $true)]
        [object[]]$Wrappers
    )

    return (($Wrappers | ForEach-Object {
        $errorText = if ([string]::IsNullOrWhiteSpace([string]$_.error)) { "none" } else { [string]$_.error }
        "- $($_.reviewer_id): status=$($_.status); timed_out=$($_.timed_out); raw_result=$($_.raw_result_path); error=$errorText"
    }) -join [Environment]::NewLine)
}

function Get-AssumptionBlock {
    param(
        [Parameter(Mandatory = $true)]
        [object[]]$Wrappers
    )

    $lines = @()
    foreach ($wrapper in $Wrappers) {
        if ($wrapper.status -ne "completed" -or $null -eq $wrapper.result) {
            continue
        }

        foreach ($assumption in (Convert-ToArray -Value (Get-PropertyValue -Object $wrapper.result -Name "assumptions"))) {
            $lines += "- [$($wrapper.reviewer_id)] $assumption"
        }
    }

    if ($lines.Count -eq 0) {
        return "- none"
    }

    return ($lines -join [Environment]::NewLine)
}

function Get-ReferenceBlock {
    param(
        [Parameter(Mandatory = $true)]
        [object[]]$Wrappers,

        [string[]]$ExplicitReferences
    )

    $lines = @()
    if ($ExplicitReferences.Count -gt 0) {
        $lines += ($ExplicitReferences | ForEach-Object { Convert-ReferenceEntry -Entry $_ })
    }

    foreach ($wrapper in $Wrappers) {
        if ($wrapper.status -ne "completed" -or $null -eq $wrapper.result) {
            continue
        }

        foreach ($referenceInput in (Convert-ToArray -Value (Get-PropertyValue -Object $wrapper.result -Name "reference_inputs_used"))) {
            $lines += Convert-ReferenceInput -ReferenceInput $referenceInput
        }
    }

    if ($lines.Count -eq 0) {
        return "- none"
    }

    return (($lines | Select-Object -Unique) -join [Environment]::NewLine)
}

function Resolve-Disposition {
    param(
        [Parameter(Mandatory = $true)]
        [object[]]$Wrappers,

        [Parameter(Mandatory = $true)]
        [string]$RequestedDisposition
    )

    if ($RequestedDisposition -ne "auto") {
        return $RequestedDisposition
    }

    if (@($Wrappers | Where-Object { $_.status -ne "completed" }).Count -gt 0) {
        return "fix-and-rerun"
    }

    foreach ($wrapper in $Wrappers) {
        $result = $wrapper.result
        if ([string](Get-PropertyValue -Object $result -Name "verdict") -eq "escalate-to-human") {
            return "escalate-to-human"
        }

        if ([bool](Get-PropertyValue -Object $result -Name "requires_rerun")) {
            return "fix-and-rerun"
        }

        foreach ($finding in (Convert-ToArray -Value (Get-PropertyValue -Object $result -Name "findings"))) {
            $severity = [string](Get-PropertyValue -Object $finding -Name "severity")
            if ($severity -eq "Critical" -or $severity -eq "Warning") {
                return "fix-and-rerun"
            }
        }
    }

    return "accept"
}

function Resolve-NextAction {
    param(
        [Parameter(Mandatory = $true)]
        [string]$FinalDisposition,

        [string]$RequestedNextAction
    )

    if (-not [string]::IsNullOrWhiteSpace($RequestedNextAction)) {
        return $RequestedNextAction
    }

    switch ($FinalDisposition) {
        "accept" { return "Archive the audit artifacts and proceed with acceptance." }
        "escalate-to-human" { return "Escalate the audit report to a human reviewer before accepting or rerunning." }
        "archive-only" { return "Archive the audit artifacts without taking implementation action." }
        default { return "Review the findings, apply required fixes, and rerun the audit if any warning or higher issue was accepted." }
    }
}

$resolvedRawReviewPath = (Resolve-Path -LiteralPath $RawReviewPath).Path
$resolvedProjectPath = (Resolve-Path -LiteralPath $ProjectPath).Path
$projectName = Split-Path -Path $resolvedProjectPath -Leaf
$wrappers = @(Read-ReviewWrappers -Path $resolvedRawReviewPath)

if ([string]::IsNullOrWhiteSpace($OutputPath)) {
    $slug = Get-Date -Format "yyyyMMdd-HHmmss"
    $OutputPath = Join-Path -Path $resolvedProjectPath -ChildPath "audit-report-$slug.md"
}

$criticalBlock = Format-Findings -Wrappers $wrappers -Severity "Critical"
$warningBlock = Format-Findings -Wrappers $wrappers -Severity "Warning"
$suggestionBlock = Format-Findings -Wrappers $wrappers -Severity "Suggestion"
$reviewerStatusBlock = Get-ReviewerStatusBlock -Wrappers $wrappers
$referenceBlock = Get-ReferenceBlock -Wrappers $wrappers -ExplicitReferences $Reference
$assumptionBlock = Get-AssumptionBlock -Wrappers $wrappers
$finalDisposition = Resolve-Disposition -Wrappers $wrappers -RequestedDisposition $Disposition
$finalNextAction = Resolve-NextAction -FinalDisposition $finalDisposition -RequestedNextAction $NextAction

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

## Reviewer Status

$reviewerStatusBlock

## Reference Inputs

$referenceBlock

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

$finalDisposition

## Next Action

$finalNextAction
"@

[System.IO.File]::WriteAllText($OutputPath, $reportText, [System.Text.Encoding]::UTF8)
Write-Output $OutputPath
