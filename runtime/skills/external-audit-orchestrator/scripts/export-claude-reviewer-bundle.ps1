[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$SkillRoot,

    [Parameter(Mandatory = $true)]
    [string]$TargetProject,

    [switch]$Apply
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Read-JsonObject {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    if (-not (Test-Path -LiteralPath $Path)) {
        return @{}
    }

    $raw = Get-Content -LiteralPath $Path -Raw
    if ([string]::IsNullOrWhiteSpace($raw)) {
        return @{}
    }

    $parsed = $raw | ConvertFrom-Json
    return ConvertTo-Hashtable -InputObject $parsed
}

function ConvertTo-Hashtable {
    param(
        [Parameter(Mandatory = $true)]
        [object]$InputObject
    )

    if ($null -eq $InputObject) {
        return $null
    }

    if ($InputObject -is [System.Collections.IDictionary]) {
        $result = @{}
        foreach ($key in $InputObject.Keys) {
            $result[$key] = ConvertTo-Hashtable -InputObject $InputObject[$key]
        }
        return $result
    }

    if ($InputObject -is [System.Collections.IEnumerable] -and -not ($InputObject -is [string])) {
        $items = @()
        foreach ($item in $InputObject) {
            $items += ,(ConvertTo-Hashtable -InputObject $item)
        }
        return $items
    }

    if ($InputObject -is [string] -or
        $InputObject -is [char] -or
        $InputObject -is [bool] -or
        $InputObject -is [int] -or
        $InputObject -is [long] -or
        $InputObject -is [double] -or
        $InputObject -is [decimal] -or
        $InputObject -is [datetime]) {
        return $InputObject
    }

    $properties = @()
    if ($InputObject.PSObject) {
        $properties = @($InputObject.PSObject.Properties)
    }

    if ($properties.Count -gt 0) {
        $result = @{}
        foreach ($property in $properties) {
            $result[$property.Name] = ConvertTo-Hashtable -InputObject $property.Value
        }
        return $result
    }

    return $InputObject
}

function Merge-HookArray {
    param(
        [object[]]$Existing,
        [object[]]$Incoming
    )

    $merged = @()
    if ($Existing) {
        $merged += $Existing
    }

    foreach ($item in ($Incoming | Where-Object { $_ -ne $null })) {
        $matcher = $item["matcher"]
        if ([string]::IsNullOrWhiteSpace([string]$matcher)) {
            $merged += $item
            continue
        }

        $alreadyExists = $false
        foreach ($existingItem in $merged) {
            if ($existingItem -is [hashtable] -and $existingItem.ContainsKey("matcher") -and $existingItem["matcher"] -eq $matcher) {
                $alreadyExists = $true
                break
            }
        }

        if (-not $alreadyExists) {
            $merged += $item
        }
    }

    return ,$merged
}

$resolvedSkillRoot = (Resolve-Path -LiteralPath $SkillRoot).Path
$resolvedTargetProject = (Resolve-Path -LiteralPath $TargetProject).Path

$sourceReviewer = Join-Path -Path $resolvedSkillRoot -ChildPath "assets\claude\code-reviewer.md"
$sourceSettings = Join-Path -Path $resolvedSkillRoot -ChildPath "assets\claude\settings.audit.json"

$targetClaudeDir = Join-Path -Path $resolvedTargetProject -ChildPath ".claude"
$targetAgentsDir = Join-Path -Path $targetClaudeDir -ChildPath "agents"
$targetReviewer = Join-Path -Path $targetAgentsDir -ChildPath "code-reviewer.md"
$targetSettings = Join-Path -Path $targetClaudeDir -ChildPath "settings.json"

if (-not (Test-Path -LiteralPath $sourceReviewer)) {
    throw "Missing reviewer asset: $sourceReviewer"
}

if (-not (Test-Path -LiteralPath $sourceSettings)) {
    throw "Missing settings asset: $sourceSettings"
}

$incomingSettings = Read-JsonObject -Path $sourceSettings
$existingSettings = Read-JsonObject -Path $targetSettings

if (-not $existingSettings.ContainsKey("hooks")) {
    $existingSettings["hooks"] = @{}
}

if (-not $incomingSettings.ContainsKey("hooks")) {
    $incomingSettings["hooks"] = @{}
}

$existingSubagentStop = @()
if ($existingSettings["hooks"].ContainsKey("SubagentStop")) {
    $existingSubagentStop = @($existingSettings["hooks"]["SubagentStop"])
}

$incomingSubagentStop = @()
if ($incomingSettings["hooks"].ContainsKey("SubagentStop")) {
    $incomingSubagentStop = @($incomingSettings["hooks"]["SubagentStop"])
}

$existingSettings["hooks"]["SubagentStop"] = Merge-HookArray -Existing $existingSubagentStop -Incoming $incomingSubagentStop
$mergedSettingsJson = $existingSettings | ConvertTo-Json -Depth 20

$modeLabel = if ($Apply) { "apply" } else { "dry-run" }
$plan = @(
    "Claude reviewer bundle plan",
    "- target_project: $resolvedTargetProject",
    "- target_reviewer: $targetReviewer",
    "- target_settings: $targetSettings",
    "- mode: $modeLabel",
    "- action: copy reviewer asset",
    "- action: merge hooks.SubagentStop into settings.json"
)

Write-Output ($plan -join [Environment]::NewLine)

if (-not $Apply) {
    Write-Output ""
    Write-Output "Dry-run only. Re-run with -Apply to write files."
    return
}

New-Item -ItemType Directory -Force -Path $targetAgentsDir | Out-Null
Copy-Item -LiteralPath $sourceReviewer -Destination $targetReviewer -Force
[System.IO.File]::WriteAllText($targetSettings, $mergedSettingsJson + [Environment]::NewLine, [System.Text.Encoding]::UTF8)

Write-Output ""
Write-Output "Applied reviewer bundle."
