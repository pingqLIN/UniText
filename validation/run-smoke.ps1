[CmdletBinding()]
param(
    [switch]$SkipCodexMirror,
    [switch]$KeepArtifacts
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path -LiteralPath (Join-Path -Path $PSScriptRoot -ChildPath "..")).Path
$registrySkillRoot = Join-Path -Path $repoRoot -ChildPath "registry\skills\external-audit-orchestrator"
$runtimeSkillRoot = Join-Path -Path $repoRoot -ChildPath "runtime\skills\external-audit-orchestrator"
$scratchRoot = Join-Path -Path ([System.IO.Path]::GetTempPath()) -ChildPath ("external-audit-orchestrator-smoke-" + [guid]::NewGuid().ToString("N"))
$runtimeDryRun = Join-Path -Path $repoRoot -ChildPath "runtime\.runtime-dryrun-external-audit-smoke"

function Assert-Condition {
    param(
        [Parameter(Mandatory = $true)]
        [bool]$Condition,

        [Parameter(Mandatory = $true)]
        [string]$Message
    )

    if (-not $Condition) {
        throw $Message
    }
}

function Invoke-Step {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name,

        [Parameter(Mandatory = $true)]
        [scriptblock]$Body
    )

    Write-Output "== $Name =="
    & $Body
    Write-Output "PASS $Name"
}

function Test-PowerShellParser {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ScriptDirectory
    )

    $scripts = Get-ChildItem -LiteralPath $ScriptDirectory -Filter "*.ps1"
    foreach ($script in $scripts) {
        $tokens = $null
        $errors = $null
        $null = [System.Management.Automation.Language.Parser]::ParseFile($script.FullName, [ref]$tokens, [ref]$errors)
        if ($errors -and $errors.Count -gt 0) {
            $messages = ($errors | ForEach-Object { $_.Message }) -join [Environment]::NewLine
            throw "Parser errors in $($script.FullName):$([Environment]::NewLine)$messages"
        }
    }
}

function Test-PwshParserWhenAvailable {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ScriptDirectory
    )

    $pwsh = Get-Command pwsh -ErrorAction SilentlyContinue
    if ($null -eq $pwsh) {
        Write-Output "pwsh unavailable; skipped PowerShell 7 parser check."
        return
    }

    $parserScript = Join-Path -Path $scratchRoot -ChildPath "pwsh-parser-check.ps1"
    [System.IO.File]::WriteAllText(
        $parserScript,
        @'
param(
    [Parameter(Mandatory = $true)]
    [string]$ScriptDirectory
)

$ErrorActionPreference = "Stop"
$scripts = Get-ChildItem -LiteralPath $ScriptDirectory -Filter "*.ps1"
foreach ($script in $scripts) {
    $tokens = $null
    $errors = $null
    $null = [System.Management.Automation.Language.Parser]::ParseFile($script.FullName, [ref]$tokens, [ref]$errors)
    if ($errors -and $errors.Count -gt 0) {
        $messages = ($errors | ForEach-Object { $_.Message }) -join [Environment]::NewLine
        throw "Parser errors in $($script.FullName):$([Environment]::NewLine)$messages"
    }
}
'@,
        [System.Text.Encoding]::UTF8
    )

    & $pwsh.Source -NoProfile -File $parserScript -ScriptDirectory $ScriptDirectory
    if ($LASTEXITCODE -ne 0) {
        throw "PowerShell 7 parser check failed for $ScriptDirectory."
    }
}

function New-SmokeProject {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ParentDirectory,

        [string]$ProjectName = "target-project"
    )

    $project = Join-Path -Path $ParentDirectory -ChildPath $ProjectName
    New-Item -ItemType Directory -Force -Path $project | Out-Null
    [System.IO.File]::WriteAllText((Join-Path -Path $project -ChildPath "README.md"), "# Fixture`n", [System.Text.Encoding]::UTF8)
    git -C $project init | Out-Null
    git -C $project config user.email "codex@example.test"
    git -C $project config user.name "Codex Test"
    git -C $project add README.md
    git -C $project commit -m "initial fixture" | Out-Null
    [System.IO.File]::WriteAllText((Join-Path -Path $project -ChildPath "README.md"), "# Fixture`n`nChanged working tree.`n", [System.Text.Encoding]::UTF8)
    return $project
}

function New-RawReview {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ParentDirectory
    )

    $rawReview = Join-Path -Path $ParentDirectory -ChildPath "raw-review.md"
    [System.IO.File]::WriteAllText(
        $rawReview,
        @"
Critical
- none

Warning
- title: sample warning
  location: fixture
  risk: demonstrates normalization
  recommended action: inspect report

Suggestion
- none

Assumptions
- temp fixture only
"@,
        [System.Text.Encoding]::UTF8
    )
    return $rawReview
}

function Test-SkillFlow {
    param(
        [Parameter(Mandatory = $true)]
        [string]$SkillRoot,

        [Parameter(Mandatory = $true)]
        [string]$ProjectPath,

        [Parameter(Mandatory = $true)]
        [string]$RawReviewPath,

        [Parameter(Mandatory = $true)]
        [string]$Label
    )

    $packetPath = Join-Path -Path $scratchRoot -ChildPath "$Label-working-packet.md"
    & (Join-Path -Path $SkillRoot -ChildPath "scripts\build-audit-packet.ps1") `
        -ProjectPath $ProjectPath `
        -ScopeType WorkingTree `
        -Summary "$Label working tree smoke" `
        -Question "Check fixture" `
        -Reference "local-project|$repoRoot|smoke fixture" `
        -OutputPath $packetPath | Out-Null
    Assert-Condition -Condition (Test-Path -LiteralPath $packetPath) -Message "Missing packet for $Label."
    Assert-Condition -Condition ((Get-Content -LiteralPath $packetPath -Raw) -match "Reference Inputs") -Message "Packet missing Reference Inputs for $Label."

    $reportPath = Join-Path -Path $scratchRoot -ChildPath "$Label-report.md"
    & (Join-Path -Path $SkillRoot -ChildPath "scripts\normalize-audit-report.ps1") `
        -RawReviewPath $RawReviewPath `
        -AuditMode same-provider-subagent `
        -ProjectPath $ProjectPath `
        -Scope "working-tree" `
        -Reference "local-project|$repoRoot|smoke fixture" `
        -OutputPath $reportPath | Out-Null
    Assert-Condition -Condition ((Get-Content -LiteralPath $reportPath -Raw) -match "sample warning") -Message "Normalized report missing warning for $Label."

    & (Join-Path -Path $SkillRoot -ChildPath "scripts\export-claude-reviewer-bundle.ps1") `
        -SkillRoot $SkillRoot `
        -TargetProject $ProjectPath | Out-Null
    & (Join-Path -Path $SkillRoot -ChildPath "scripts\export-claude-reviewer-bundle.ps1") `
        -SkillRoot $SkillRoot `
        -TargetProject $ProjectPath `
        -Apply | Out-Null
    Assert-Condition -Condition (Test-Path -LiteralPath (Join-Path -Path $ProjectPath -ChildPath ".claude\agents\code-reviewer.md")) -Message "Claude reviewer was not exported for $Label."

    $tb2Directory = Join-Path -Path $scratchRoot -ChildPath "$Label-tb2-requests"
    & (Join-Path -Path $SkillRoot -ChildPath "scripts\export-tb2-audit-request.ps1") `
        -SkillRoot $SkillRoot `
        -TargetProject $ProjectPath `
        -AuditPacketPath $packetPath `
        -OutputPath $tb2Directory `
        -Apply | Out-Null
    $tb2RequestFiles = @(Get-ChildItem -LiteralPath $tb2Directory -Filter "*.request.json")
    Assert-Condition -Condition ($tb2RequestFiles.Count -eq 3) -Message "TB2 export did not write three reviewer requests for $Label."
    foreach ($tb2RequestFile in $tb2RequestFiles) {
        $tb2Json = Get-Content -LiteralPath $tb2RequestFile.FullName -Raw | ConvertFrom-Json
        Assert-Condition -Condition ($tb2Json.prompt -match "packet_path") -Message "TB2 request prompt did not reference packet_path for $Label."
        Assert-Condition -Condition ($tb2Json.packet_transport -eq "path-reference") -Message "TB2 request should default to path-reference for $Label."
        Assert-Condition -Condition (-not [string]::IsNullOrWhiteSpace($tb2Json.packet_sha256)) -Message "TB2 request missing packet hash for $Label."
        Assert-Condition -Condition ($null -eq $tb2Json.packet_inline) -Message "TB2 request should not inline packet by default for $Label."
    }
    $tb2Manifest = Get-Content -LiteralPath (Join-Path -Path $tb2Directory -ChildPath "manifest.json") -Raw | ConvertFrom-Json
    Assert-Condition -Condition ($tb2Manifest.requests.Count -eq 3) -Message "TB2 manifest did not record three reviewer requests for $Label."

    foreach ($mode in @("same-provider-subagent", "tb2-template", "external-web", "external-cli-mcp")) {
        $flowOutput = & (Join-Path -Path $SkillRoot -ChildPath "scripts\run-external-audit-flow.ps1") `
            -SkillRoot $SkillRoot `
            -TargetProject $ProjectPath `
            -Mode $mode `
            -ScopeType Manual `
            -ScopeValue "$Label-$mode" `
            -Summary "$Label $mode smoke" `
            -Question "Smoke?" `
            -Reference "local-project|$repoRoot|smoke fixture"
        Assert-Condition -Condition (($flowOutput -join "`n") -match "mode: $mode") -Message "Unified flow output missing mode $mode for $Label."
    }

    $flowReport = Join-Path -Path $scratchRoot -ChildPath "$Label-flow-report.md"
    & (Join-Path -Path $SkillRoot -ChildPath "scripts\run-external-audit-flow.ps1") `
        -SkillRoot $SkillRoot `
        -TargetProject $ProjectPath `
        -Mode external-web `
        -ScopeType Manual `
        -ScopeValue "$Label-reviewed" `
        -Summary "$Label reviewed smoke" `
        -RawReviewPath $RawReviewPath `
        -ReportPath $flowReport `
        -Reference "local-project|$repoRoot|smoke fixture" | Out-Null
    Assert-Condition -Condition (Test-Path -LiteralPath $flowReport) -Message "Unified flow did not write normalized report for $Label."
}

function Test-ScopeVariants {
    param(
        [Parameter(Mandatory = $true)]
        [string]$SkillRoot,

        [Parameter(Mandatory = $true)]
        [string]$ParentDirectory
    )

    $project = Join-Path -Path $ParentDirectory -ChildPath "scope-project"
    New-Item -ItemType Directory -Force -Path $project | Out-Null
    [System.IO.File]::WriteAllText((Join-Path -Path $project -ChildPath "README.md"), "# Fixture`n", [System.Text.Encoding]::UTF8)
    git -C $project init | Out-Null
    git -C $project config user.email "codex@example.test"
    git -C $project config user.name "Codex Test"
    git -C $project add README.md
    git -C $project commit -m "initial fixture" | Out-Null
    $base = (git -C $project rev-parse HEAD).Trim()
    [System.IO.File]::WriteAllText((Join-Path -Path $project -ChildPath "README.md"), "# Fixture`n`nSecond commit.`n", [System.Text.Encoding]::UTF8)
    git -C $project add README.md
    git -C $project commit -m "second fixture" | Out-Null
    $head = (git -C $project rev-parse HEAD).Trim()
    [System.IO.File]::WriteAllText((Join-Path -Path $project -ChildPath "README.md"), "# Fixture`n`nSecond commit.`n`nPath diff.`n", [System.Text.Encoding]::UTF8)
    [System.IO.File]::WriteAllText((Join-Path -Path $project -ChildPath "staged.txt"), "staged`n", [System.Text.Encoding]::UTF8)
    git -C $project add staged.txt

    $cases = @(
        @{ Name = "staged"; ScopeType = "Staged"; ScopeValue = $null; Expect = "staged.txt" },
        @{ Name = "commit"; ScopeType = "CommitRange"; ScopeValue = "$base..$head"; Expect = "Second commit" },
        @{ Name = "path"; ScopeType = "Path"; ScopeValue = "README.md"; Expect = "Path diff" },
        @{ Name = "manual"; ScopeType = "Manual"; ScopeValue = "operator question"; Expect = "manual scope" }
    )

    foreach ($case in $cases) {
        $outputPath = Join-Path -Path $ParentDirectory -ChildPath ("packet-" + $case.Name + ".md")
        $splat = @{
            ProjectPath = $project
            ScopeType = $case.ScopeType
            Summary = "scope smoke"
            OutputPath = $outputPath
        }
        if ($case.ScopeValue) {
            $splat["ScopeValue"] = $case.ScopeValue
        }

        & (Join-Path -Path $SkillRoot -ChildPath "scripts\build-audit-packet.ps1") @splat | Out-Null
        $packetText = Get-Content -LiteralPath $outputPath -Raw
        Assert-Condition -Condition ($packetText -match [regex]::Escape($case.Expect)) -Message "Scope $($case.Name) missing expected evidence."
    }
}

function Test-CodexMirror {
    $mirrorRoot = "C:\Users\miles\.codex\skills\external-audit-orchestrator"
    $requiredPaths = @(
        "SKILL.md",
        "scripts\build-audit-packet.ps1",
        "scripts\run-external-audit-flow.ps1",
        "assets\tb2\tb2-audit-request.template.json",
        "assets\claude\settings.audit.json"
    )

    foreach ($relativePath in $requiredPaths) {
        $fullPath = Join-Path -Path $mirrorRoot -ChildPath $relativePath
        Assert-Condition -Condition (Test-Path -LiteralPath $fullPath) -Message "Codex mirror missing $relativePath."
    }
}

try {
    New-Item -ItemType Directory -Force -Path $scratchRoot | Out-Null

    Invoke-Step -Name "projection unit tests" -Body {
        python -m unittest tests.test_runtime_support_projection
    }

    Invoke-Step -Name "runtime dry-run parity" -Body {
        $dryRunOutput = python local\scripts\build-runtime-layer.py --output-dir runtime\.runtime-dryrun-external-audit-smoke
        if ($LASTEXITCODE -ne 0) {
            throw "Runtime dry-run failed."
        }

        $dryRunSummary = ($dryRunOutput -join [Environment]::NewLine) | ConvertFrom-Json
        Assert-Condition -Condition ($dryRunSummary.diff_summary.status -eq "clean") -Message "Runtime dry-run drift status was $($dryRunSummary.diff_summary.status)."
        Assert-Condition -Condition ($dryRunSummary.diff_summary.write_gate.routine_write_allowed -eq $true) -Message "Runtime dry-run write gate requires review."
        $dryRunOutput
    }

    Invoke-Step -Name "PowerShell parser checks" -Body {
        Test-PowerShellParser -ScriptDirectory (Join-Path -Path $registrySkillRoot -ChildPath "scripts")
        Test-PowerShellParser -ScriptDirectory (Join-Path -Path $runtimeSkillRoot -ChildPath "scripts")
        Test-PwshParserWhenAvailable -ScriptDirectory (Join-Path -Path $registrySkillRoot -ChildPath "scripts")
        Test-PwshParserWhenAvailable -ScriptDirectory (Join-Path -Path $runtimeSkillRoot -ChildPath "scripts")
    }

    $rawReviewPath = New-RawReview -ParentDirectory $scratchRoot

    Invoke-Step -Name "registry skill flow" -Body {
        $registryProjectPath = New-SmokeProject -ParentDirectory $scratchRoot -ProjectName "registry-project"
        Test-SkillFlow -SkillRoot $registrySkillRoot -ProjectPath $registryProjectPath -RawReviewPath $rawReviewPath -Label "registry"
    }

    Invoke-Step -Name "runtime skill flow" -Body {
        $runtimeProjectPath = New-SmokeProject -ParentDirectory $scratchRoot -ProjectName "runtime-project"
        Test-SkillFlow -SkillRoot $runtimeSkillRoot -ProjectPath $runtimeProjectPath -RawReviewPath $rawReviewPath -Label "runtime"
    }

    Invoke-Step -Name "packet scope variants" -Body {
        Test-ScopeVariants -SkillRoot $runtimeSkillRoot -ParentDirectory $scratchRoot
    }

    if (-not $SkipCodexMirror) {
        Invoke-Step -Name "Codex mirror support files" -Body {
            Test-CodexMirror
        }
    }

    Write-Output "All external-audit-orchestrator smoke checks passed."
}
finally {
    if (-not $KeepArtifacts) {
        if (Test-Path -LiteralPath $scratchRoot) {
            Remove-Item -LiteralPath $scratchRoot -Recurse -Force
        }
        if (Test-Path -LiteralPath $runtimeDryRun) {
            Remove-Item -LiteralPath $runtimeDryRun -Recurse -Force
        }
    }
    else {
        Write-Output "Kept smoke artifacts:"
        Write-Output "- $scratchRoot"
        Write-Output "- $runtimeDryRun"
    }
}

