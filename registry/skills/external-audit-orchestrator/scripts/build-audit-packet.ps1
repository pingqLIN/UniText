[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectPath,

    [ValidateSet("WorkingTree", "Staged", "CommitRange", "Path", "Manual")]
    [string]$ScopeType = "WorkingTree",

    [string]$ScopeValue,

    [string]$Summary = "",

    [string[]]$Question = @(),

    [string[]]$Check = @(),

    [string[]]$Reference = @(),

    [string]$OutputPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Test-GitRepository {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    & git -C $Path rev-parse --show-toplevel *> $null
    return ($LASTEXITCODE -eq 0)
}

function Get-GitStatusText {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    try {
        return (git -C $Path status --short --branch) -join [Environment]::NewLine
    }
    catch {
        return "git status unavailable"
    }
}

function Get-GitDiffText {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,

        [Parameter(Mandatory = $true)]
        [string]$Mode,

        [string]$Value
    )

    try {
        switch ($Mode) {
            "WorkingTree" { return (git -C $Path diff -- .) -join [Environment]::NewLine }
            "Staged" { return (git -C $Path diff --staged -- .) -join [Environment]::NewLine }
            "CommitRange" {
                if ([string]::IsNullOrWhiteSpace($Value)) {
                    return "commit range missing"
                }

                return (git -C $Path diff $Value -- .) -join [Environment]::NewLine
            }
            "Path" {
                if ([string]::IsNullOrWhiteSpace($Value)) {
                    return "path scope missing"
                }

                return (git -C $Path diff -- $Value) -join [Environment]::NewLine
            }
            default { return "manual scope; no git diff captured" }
        }
    }
    catch {
        return "git diff unavailable"
    }
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

    $kind = $parts[0].Trim()
    $target = $parts[1].Trim()
    $reason = $parts[2].Trim()
    return "- ${kind}: ${target} - $reason"
}

$resolvedProjectPath = (Resolve-Path -LiteralPath $ProjectPath).Path
$projectName = Split-Path -Path $resolvedProjectPath -Leaf
$isGitRepo = Test-GitRepository -Path $resolvedProjectPath
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

$statusText = if ($isGitRepo) {
    Get-GitStatusText -Path $resolvedProjectPath
}
else {
    "not a git repository"
}

$diffText = if ($isGitRepo) {
    Get-GitDiffText -Path $resolvedProjectPath -Mode $ScopeType -Value $ScopeValue
}
else {
    "git diff unavailable because the path is not a git repository"
}

if ([string]::IsNullOrWhiteSpace($OutputPath)) {
    $slug = Get-Date -Format "yyyyMMdd-HHmmss"
    $OutputPath = Join-Path -Path $resolvedProjectPath -ChildPath "audit-packet-$slug.md"
}

$referenceLines = if ($Reference.Count -gt 0) {
    $Reference | ForEach-Object { Convert-ReferenceEntry -Entry $_ }
}
else {
    @("- none")
}

$questionLines = if ($Question.Count -gt 0) {
    $Question | ForEach-Object { "- $_" }
}
else {
    @("- Are there blocking bugs, regressions, or security concerns?")
}

$checkLines = if ($Check.Count -gt 0) {
    $Check | ForEach-Object { "- $_" }
}
else {
    @("- none recorded")
}

$summaryText = if ([string]::IsNullOrWhiteSpace($Summary)) {
    "External audit requested for $projectName."
}
else {
    $Summary
}

$generatedAt = Get-Date -Format s
$packetText = @"
# Audit Packet

## Audit Goal

$summaryText

## Scope

- project: $resolvedProjectPath
- scope: $scopeLabel
- git_repo: $isGitRepo

## Project Context

- project_name: $projectName
- generated_at: $generatedAt
- builder: build-audit-packet.ps1

## Change Evidence

### Git Status

~~~text
$statusText
~~~

### Diff Or Scope Evidence

~~~diff
$diffText
~~~

## Checks Already Run

$($checkLines -join [Environment]::NewLine)

## Questions For Reviewer

$($questionLines -join [Environment]::NewLine)

## Reference Inputs

$($referenceLines -join [Environment]::NewLine)

## Expected Output Format

- Critical
- Warning
- Suggestion
- Assumptions
- Reference Inputs Used
"@

[System.IO.File]::WriteAllText($OutputPath, $packetText, [System.Text.Encoding]::UTF8)
Write-Output $OutputPath
