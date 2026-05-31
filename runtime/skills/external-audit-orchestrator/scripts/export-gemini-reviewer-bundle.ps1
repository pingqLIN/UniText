[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$SkillRoot,

    [Parameter(Mandatory = $true)]
    [string]$TargetProject,

    [string]$AuditPacketPath,

    [string]$OutputDirectory,

    [string]$GeminiCommand = "gemini",

    [string]$ArchitectModel = "gemini-3.1-flash",

    [string]$CriticModel = "gemini-3.1-pro",

    [string]$DesignCriticModel = "gemini-3.1-pro",

    [int]$MaxReviewRounds = 3,

    [switch]$Apply
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function ConvertTo-PowerShellSingleQuotedLiteral {
    param(
        [AllowEmptyString()]
        [string]$Value
    )

    return "'" + $Value.Replace("'", "''") + "'"
}

function Set-AgentFrontmatterValue {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Text,

        [Parameter(Mandatory = $true)]
        [string]$Key,

        [Parameter(Mandatory = $true)]
        [string]$Value
    )

    $escapedKey = [regex]::Escape($Key)
    if ($Text -match "(?m)^$escapedKey`:") {
        return [regex]::Replace($Text, "(?m)^$escapedKey`:.*$", "${Key}: $Value")
    }

    return $Text
}

$resolvedSkillRoot = (Resolve-Path -LiteralPath $SkillRoot).Path
$resolvedTargetProject = (Resolve-Path -LiteralPath $TargetProject).Path

$sourceAgentsDirectory = Join-Path -Path $resolvedSkillRoot -ChildPath "assets\gemini"
$sourceArchitect = Join-Path -Path $sourceAgentsDirectory -ChildPath "plan-architect.md"
$sourceCritic = Join-Path -Path $sourceAgentsDirectory -ChildPath "plan-critic.md"
$sourceDesignCritic = Join-Path -Path $sourceAgentsDirectory -ChildPath "design-critic.md"
$sourceSchema = Join-Path -Path $sourceAgentsDirectory -ChildPath "plan-critic.schema.json"
$sourceDesignSchema = Join-Path -Path $sourceAgentsDirectory -ChildPath "design-critic.schema.json"

foreach ($requiredPath in @($sourceArchitect, $sourceCritic, $sourceDesignCritic, $sourceSchema, $sourceDesignSchema)) {
    if (-not (Test-Path -LiteralPath $requiredPath)) {
        throw "Missing Gemini reviewer asset: $requiredPath"
    }
}

if ([string]::IsNullOrWhiteSpace($OutputDirectory)) {
    $OutputDirectory = Join-Path -Path $resolvedTargetProject -ChildPath ".audit\gemini-cli"
}

$resolvedOutputDirectory = if (Test-Path -LiteralPath $OutputDirectory) {
    (Resolve-Path -LiteralPath $OutputDirectory).Path
}
else {
    [System.IO.Path]::GetFullPath($OutputDirectory)
}

$targetGeminiDirectory = Join-Path -Path $resolvedTargetProject -ChildPath ".gemini"
$targetAgentsDirectory = Join-Path -Path $targetGeminiDirectory -ChildPath "agents"
$targetArchitect = Join-Path -Path $targetAgentsDirectory -ChildPath "external-plan-architect.md"
$targetCritic = Join-Path -Path $targetAgentsDirectory -ChildPath "external-plan-critic.md"
$targetDesignCritic = Join-Path -Path $targetAgentsDirectory -ChildPath "external-design-critic.md"
$targetSchema = Join-Path -Path $resolvedOutputDirectory -ChildPath "plan-critic.schema.json"
$targetDesignSchema = Join-Path -Path $resolvedOutputDirectory -ChildPath "design-critic.schema.json"
$runnerPath = Join-Path -Path $resolvedOutputDirectory -ChildPath "run-gemini-plan-review.ps1"
$rawArchitectPath = Join-Path -Path $resolvedOutputDirectory -ChildPath "plan-architect.raw.txt"
$rawCriticPath = Join-Path -Path $resolvedOutputDirectory -ChildPath "plan-critic.raw.json"
$finalPlanPath = Join-Path -Path $resolvedOutputDirectory -ChildPath "final-plan.md"

$resolvedAuditPacketPath = ""
if (-not [string]::IsNullOrWhiteSpace($AuditPacketPath)) {
    $resolvedAuditPacketPath = (Resolve-Path -LiteralPath $AuditPacketPath).Path
}

$geminiCommandLiteral = ConvertTo-PowerShellSingleQuotedLiteral -Value $GeminiCommand
$targetProjectLiteral = ConvertTo-PowerShellSingleQuotedLiteral -Value $resolvedTargetProject
$auditPacketLiteral = ConvertTo-PowerShellSingleQuotedLiteral -Value $resolvedAuditPacketPath
$maxReviewRoundsLiteral = [string]$MaxReviewRounds

$runnerText = @'
[CmdletBinding()]
param(
    [string]$GeminiCommand = __GEMINI_COMMAND_LITERAL__,
    [string]$AuditPacketPath = __AUDIT_PACKET_LITERAL__,
    [int]$MaxReviewRounds = __MAX_REVIEW_ROUNDS_LITERAL__
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$targetProject = __TARGET_PROJECT_LITERAL__
$outputDirectory = $PSScriptRoot
$architectOutputPath = Join-Path -Path $outputDirectory -ChildPath "plan-architect.raw.txt"
$criticOutputPath = Join-Path -Path $outputDirectory -ChildPath "plan-critic.raw.json"
$finalPlanPath = Join-Path -Path $outputDirectory -ChildPath "final-plan.md"

if (-not (Test-Path -LiteralPath $targetProject)) {
    throw "Missing target project: $targetProject"
}

if ([string]::IsNullOrWhiteSpace($AuditPacketPath)) {
    $AuditPacketPath = Join-Path -Path $outputDirectory -ChildPath "audit-packet.md"
}

if (-not (Test-Path -LiteralPath $AuditPacketPath)) {
    throw "Missing audit packet: $AuditPacketPath"
}

$geminiExecutable = if (Test-Path -LiteralPath $GeminiCommand -PathType Leaf) {
    (Resolve-Path -LiteralPath $GeminiCommand).Path
}
else {
    $application = Get-Command -Name $GeminiCommand -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
    if (-not $application) {
        throw "Gemini executable not found for command: $GeminiCommand"
    }

    $application.Source
}

$auditPacket = Get-Content -LiteralPath $AuditPacketPath -Raw
$revisionPrompt = ""
$lastPlan = ""

for ($round = 1; $round -le $MaxReviewRounds; $round++) {
    $architectPrompt = @"
@external_plan_architect

Draft or revise a software implementation plan for this audit packet.

Round: $round of $MaxReviewRounds

Reviewer revision request:
$revisionPrompt

# Audit Packet

$auditPacket
"@

    Push-Location -LiteralPath $targetProject
    try {
        $lastPlan = & $geminiExecutable -p $architectPrompt
    }
    finally {
        Pop-Location
    }

    if ($LASTEXITCODE -ne 0) {
        throw "Gemini architect step failed with exit code $LASTEXITCODE"
    }

    [System.IO.File]::WriteAllText($architectOutputPath, $lastPlan + [Environment]::NewLine, [System.Text.Encoding]::UTF8)

    $criticPrompt = @"
@external_plan_critic

Review the plan below. Return only the strict JSON object.

# Plan

$lastPlan
"@

    Push-Location -LiteralPath $targetProject
    try {
        $criticRaw = & $geminiExecutable -p $criticPrompt --output-format json
    }
    finally {
        Pop-Location
    }

    if ($LASTEXITCODE -ne 0) {
        throw "Gemini critic step failed with exit code $LASTEXITCODE"
    }

    [System.IO.File]::WriteAllText($criticOutputPath, ($criticRaw | Out-String).Trim() + [Environment]::NewLine, [System.Text.Encoding]::UTF8)

    $outerJson = ($criticRaw | Out-String).Trim() | ConvertFrom-Json
    $criticText = if ($outerJson.PSObject.Properties.Name -contains "response") {
        [string]$outerJson.response
    }
    else {
        ($criticRaw | Out-String).Trim()
    }

    $review = $criticText | ConvertFrom-Json
    if ($review.status -eq "pass") {
        [System.IO.File]::WriteAllText($finalPlanPath, $lastPlan + [Environment]::NewLine, [System.Text.Encoding]::UTF8)
        Write-Output "Gemini actor-critic review passed on round $round."
        Write-Output "Final plan: $finalPlanPath"
        Write-Output "Raw critic output: $criticOutputPath"
        exit 0
    }

    if ($review.status -ne "revise") {
        throw "Gemini critic returned unsupported status: $($review.status)"
    }

    $revisionPrompt = [string]$review.improvement_prompt
    if ([string]::IsNullOrWhiteSpace($revisionPrompt)) {
        throw "Gemini critic requested revise but did not provide improvement_prompt."
    }
}

[System.IO.File]::WriteAllText($finalPlanPath, $lastPlan + [Environment]::NewLine, [System.Text.Encoding]::UTF8)
throw "Gemini actor-critic review did not pass within $MaxReviewRounds rounds. Last plan: $finalPlanPath. Last critic output: $criticOutputPath"
'@

$runnerText = $runnerText.Replace("__GEMINI_COMMAND_LITERAL__", $geminiCommandLiteral)
$runnerText = $runnerText.Replace("__TARGET_PROJECT_LITERAL__", $targetProjectLiteral)
$runnerText = $runnerText.Replace("__AUDIT_PACKET_LITERAL__", $auditPacketLiteral)
$runnerText = $runnerText.Replace("__MAX_REVIEW_ROUNDS_LITERAL__", $maxReviewRoundsLiteral)

$modeLabel = if ($Apply) { "apply" } else { "dry-run" }
$plan = @(
    "Gemini reviewer bundle plan",
    "- target_project: $resolvedTargetProject",
    "- target_agents_directory: $targetAgentsDirectory",
    "- target_architect: $targetArchitect",
    "- target_critic: $targetCritic",
    "- target_design_critic: $targetDesignCritic",
    "- output_directory: $resolvedOutputDirectory",
    "- schema_path: $targetSchema",
    "- design_schema_path: $targetDesignSchema",
    "- runner_path: $runnerPath",
    "- raw_architect: $rawArchitectPath",
    "- raw_critic: $rawCriticPath",
    "- final_plan: $finalPlanPath",
    "- audit_packet: $resolvedAuditPacketPath",
"- gemini_command: $GeminiCommand",
"- architect_model: $ArchitectModel",
"- critic_model: $CriticModel",
"- design_critic_model: $DesignCriticModel",
"- max_review_rounds: $MaxReviewRounds",
    "- mode: $modeLabel",
    "- operator_step: run /agents reload and /agents list in Gemini CLI to confirm discovery",
    "- operator_step: run the generated runner to execute the headless actor-critic loop"
)

Write-Output ($plan -join [Environment]::NewLine)

if (-not $Apply) {
    Write-Output ""
    Write-Output "Dry-run only. Re-run with -Apply to write files."
    return
}

New-Item -ItemType Directory -Force -Path $targetAgentsDirectory | Out-Null
New-Item -ItemType Directory -Force -Path $resolvedOutputDirectory | Out-Null
$architectText = Get-Content -LiteralPath $sourceArchitect -Raw
$criticText = Get-Content -LiteralPath $sourceCritic -Raw
$designCriticText = Get-Content -LiteralPath $sourceDesignCritic -Raw
$architectText = Set-AgentFrontmatterValue -Text $architectText -Key "model" -Value $ArchitectModel
$criticText = Set-AgentFrontmatterValue -Text $criticText -Key "model" -Value $CriticModel
$designCriticText = Set-AgentFrontmatterValue -Text $designCriticText -Key "model" -Value $DesignCriticModel
[System.IO.File]::WriteAllText($targetArchitect, $architectText, [System.Text.Encoding]::UTF8)
[System.IO.File]::WriteAllText($targetCritic, $criticText, [System.Text.Encoding]::UTF8)
[System.IO.File]::WriteAllText($targetDesignCritic, $designCriticText, [System.Text.Encoding]::UTF8)
Copy-Item -LiteralPath $sourceSchema -Destination $targetSchema -Force
Copy-Item -LiteralPath $sourceDesignSchema -Destination $targetDesignSchema -Force
if (-not [string]::IsNullOrWhiteSpace($resolvedAuditPacketPath)) {
    Copy-Item -LiteralPath $resolvedAuditPacketPath -Destination (Join-Path -Path $resolvedOutputDirectory -ChildPath "audit-packet.md") -Force
}
[System.IO.File]::WriteAllText($runnerPath, $runnerText + [Environment]::NewLine, [System.Text.Encoding]::UTF8)

Write-Output ""
Write-Output "Applied Gemini reviewer bundle."
