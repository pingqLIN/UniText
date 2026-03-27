Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$registry = Join-Path $root "registry\skills"
$importDate = "2026-03-27"
$patchCacheRoot = Join-Path $root ".tmp\local-skill-patches"

$preservedPatchFiles = @{
    "skill-creator" = @("scripts/quick_validate.py")
    "webapp-testing" = @("scripts/with_server.py")
}

function Quote-Yaml {
    param(
        [Parameter(Mandatory = $true)]
        [AllowEmptyString()]
        [string]$Value
    )

    $escaped = $Value.Replace("\", "\\").Replace('"', '\"')
    return '"' + $escaped + '"'
}

function Set-FileContentWithRetry {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,
        [Parameter(Mandatory = $true)]
        [string]$Content
    )

    for ($attempt = 1; $attempt -le 5; $attempt++) {
        try {
            Set-Content -Path $Path -Value $Content
            return
        }
        catch {
            if ($attempt -eq 5) {
                throw
            }
            Start-Sleep -Milliseconds (200 * $attempt)
        }
    }
}

function Copy-SkillDirectory {
    param(
        [Parameter(Mandatory = $true)]
        [string]$SourcePath,
        [Parameter(Mandatory = $true)]
        [string]$DestinationPath
    )

    if (Test-Path $DestinationPath) {
        Remove-Item $DestinationPath -Recurse -Force
    }

    Copy-Item $SourcePath $DestinationPath -Recurse -Force
}

function Backup-PreservedPatchFiles {
    param(
        [Parameter(Mandatory = $true)]
        [string]$SkillName,
        [Parameter(Mandatory = $true)]
        [string]$SkillDirectory
    )

    $relativeFiles = $preservedPatchFiles[$SkillName]
    if (-not $relativeFiles) {
        return
    }

    foreach ($relativeFile in $relativeFiles) {
        $sourceFile = Join-Path $SkillDirectory $relativeFile
        if (-not (Test-Path $sourceFile)) {
            continue
        }

        $cacheFile = Join-Path $patchCacheRoot (Join-Path $SkillName $relativeFile)
        $cacheParent = Split-Path $cacheFile -Parent
        New-Item -ItemType Directory -Path $cacheParent -Force | Out-Null
        Copy-Item $sourceFile $cacheFile -Force
    }
}

function Restore-PreservedPatchFiles {
    param(
        [Parameter(Mandatory = $true)]
        [string]$SkillName,
        [Parameter(Mandatory = $true)]
        [string]$SkillDirectory
    )

    $relativeFiles = $preservedPatchFiles[$SkillName]
    if (-not $relativeFiles) {
        return
    }

    foreach ($relativeFile in $relativeFiles) {
        $cacheFile = Join-Path $patchCacheRoot (Join-Path $SkillName $relativeFile)
        if (-not (Test-Path $cacheFile)) {
            continue
        }

        $targetFile = Join-Path $SkillDirectory $relativeFile
        $targetParent = Split-Path $targetFile -Parent
        New-Item -ItemType Directory -Path $targetParent -Force | Out-Null
        Copy-Item $cacheFile $targetFile -Force
    }
}

function Find-GitRoot {
    param(
        [Parameter(Mandatory = $true)]
        [string]$StartPath
    )

    $resolvedPath = (Resolve-Path $StartPath).Path
    $current = [System.IO.DirectoryInfo]$resolvedPath
    while ($null -ne $current) {
        if (Test-Path (Join-Path $current.FullName ".git")) {
            return $current.FullName
        }
        $current = $current.Parent
    }

    return $null
}

function Get-GitRevision {
    param(
        [Parameter(Mandatory = $true)]
        [string]$StartPath
    )

    $gitRoot = Find-GitRoot -StartPath $StartPath
    if (-not $gitRoot) {
        return ""
    }

    return (git -C $gitRoot rev-parse HEAD).Trim()
}

function Get-RelativePath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$BasePath,
        [Parameter(Mandatory = $true)]
        [string]$TargetPath
    )

    $baseFull = (Resolve-Path $BasePath).Path.TrimEnd('\')
    $targetFull = (Resolve-Path $TargetPath).Path
    $baseUri = [Uri]::new(($baseFull + '\'))
    $targetUri = [Uri]::new($targetFull)

    return [Uri]::UnescapeDataString($baseUri.MakeRelativeUri($targetUri).ToString().Replace('/', '\'))
}

function Get-LicenseEvidence {
    param(
        [Parameter(Mandatory = $true)]
        [string]$SkillDirectory
    )

    $sourceRoot = Find-GitRoot -StartPath $SkillDirectory
    if (-not $sourceRoot) {
        return @{
            Path = ""
            Scope = "not-found"
            Note = "No git root discovered for license evidence; repo-level license relied upon."
        }
    }

    $skillMatches = Get-ChildItem -Path $SkillDirectory -Recurse -File | Where-Object {
        $_.Name -match "^(LICENSE|COPYING|COPYRIGHT)(\..*)?$"
    } | Sort-Object @{ Expression = { $_.FullName.Length } }, FullName

    $selected = $skillMatches | Select-Object -First 1
    if ($selected) {
        $relativePath = Get-RelativePath -BasePath $sourceRoot -TargetPath $selected.FullName
        $selectedParent = Split-Path $selected.FullName -Parent
        $scope = if ((Resolve-Path $sourceRoot).Path -eq $selectedParent) {
            "repository-root"
        }
        else {
            "skill-subtree"
        }

        return @{
            Path = $relativePath
            Scope = $scope
            Note = "License evidence discovered at $relativePath; scope recorded as $scope."
        }
    }

    $rootMatches = Get-ChildItem -Path $sourceRoot -File | Where-Object {
        $_.Name -match "^(LICENSE|COPYING|COPYRIGHT)(\..*)?$"
    } | Sort-Object @{ Expression = { $_.FullName.Length } }, FullName

    $rootSelected = $rootMatches | Select-Object -First 1
    if ($rootSelected) {
        $relativePath = Get-RelativePath -BasePath $sourceRoot -TargetPath $rootSelected.FullName
        return @{
            Path = $relativePath
            Scope = "repository-root"
            Note = "Repository-root license evidence discovered at $relativePath; no closer subtree license file found."
        }
    }

    return @{
        Path = ""
        Scope = "not-found"
        Note = "No LICENSE/COPYING/COPYRIGHT file discovered in source clone; repo-level license relied upon."
    }
}

function Set-SkillFrontmatter {
    param(
        [Parameter(Mandatory = $true)]
        [string]$SkillDirectory,
        [Parameter(Mandatory = $true)]
        [string]$SkillName,
        [Parameter(Mandatory = $true)]
        [string]$Description,
        [Parameter(Mandatory = $true)]
        [string]$License
    )

    $skillFile = Join-Path $SkillDirectory "SKILL.md"
    $raw = Get-Content $skillFile -Raw

    if ($raw.StartsWith("---")) {
        $match = [regex]::Match($raw, "(?s)^---\r?\n(.*?)\r?\n---\r?\n?(.*)$")
        if (-not $match.Success) {
            throw "Invalid frontmatter in $skillFile"
        }

        $otherLines = @()
        foreach ($line in ($match.Groups[1].Value -split "\r?\n")) {
            if ($line -match "^\s*name\s*:") {
                continue
            }
            if ($line -match "^\s*description\s*:") {
                continue
            }
            if ($line -match "^\s*license\s*:") {
                continue
            }
            $otherLines += $line
        }

        $frontmatterLines = @(
            "---"
            "name: $SkillName"
            "description: $(Quote-Yaml $Description)"
            "license: $(Quote-Yaml $License)"
        ) + $otherLines + @(
            "---"
            ""
        )

        Set-FileContentWithRetry -Path $skillFile -Content (($frontmatterLines -join "`n") + $match.Groups[2].Value)
        return
    }

    $headerLines = @(
        "---"
        "name: $SkillName"
        "description: $(Quote-Yaml $Description)"
        "license: $(Quote-Yaml $License)"
        "---"
        ""
    )

    Set-FileContentWithRetry -Path $skillFile -Content (($headerLines -join "`n") + $raw)
}

function Write-SourceYaml {
    param(
        [Parameter(Mandatory = $true)]
        [string]$SkillDirectory,
        [Parameter(Mandatory = $true)]
        [hashtable]$Info
    )

    $lines = @(
        "registry_name: $($Info.RegistryName)"
        "source_type: $(Quote-Yaml $Info.SourceType)"
        "source_repo: $(Quote-Yaml $Info.SourceRepo)"
        "source_url: $(Quote-Yaml $Info.SourceUrl)"
        "source_path: $(Quote-Yaml $Info.SourcePath)"
        "source_license: $(Quote-Yaml $Info.SourceLicense)"
        "imported_at: $(Quote-Yaml $Info.ImportedAt)"
        "source_revision: $(Quote-Yaml $Info.SourceRevision)"
        "license_evidence_path: $(Quote-Yaml $Info.LicenseEvidencePath)"
        "license_evidence_scope: $(Quote-Yaml $Info.LicenseEvidenceScope)"
        "license_scope_note: $(Quote-Yaml $Info.LicenseScopeNote)"
        "provenance_confidence: $(Quote-Yaml $Info.ProvenanceConfidence)"
        "import_method: $(Quote-Yaml $Info.ImportMethod)"
        "notes: $(Quote-Yaml $Info.Notes)"
    )

    Set-FileContentWithRetry -Path (Join-Path $SkillDirectory "SOURCE.yaml") -Content ($lines -join "`n")
}

function Read-SourceValue {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Lines,
        [Parameter(Mandatory = $true)]
        [string]$Key
    )

    $line = $Lines | Where-Object { $_ -like "${Key}:*" } | Select-Object -First 1
    if (-not $line) {
        return ""
    }

    return $line.Split(":", 2)[1].Trim().Trim('"')
}

$removedSkills = @(
    "doc-coauthoring",
    "docx",
    "pdf",
    "pptx",
    "xlsx"
)

$retainedSkills = @()

$imports = @(
    @{ RegistryName = "frontend-design"; SourcePath = ".tmp/sources/sickn33-antigravity-awesome-skills/skills/frontend-design"; SourceRepo = "sickn33/antigravity-awesome-skills"; SourceUrl = "https://github.com/sickn33/antigravity-awesome-skills"; SourceSkillPath = "skills/frontend-design"; SourceLicense = "Apache-2.0"; Description = "Use when building distinctive, production-grade frontend interfaces with a strong visual point of view."; Notes = "Imported from a public Apache-2.0 skill set, replacing the former local registry copy."; },
    @{ RegistryName = "internal-comms"; SourcePath = ".tmp/sources/sickn33-antigravity-awesome-skills/skills/internal-comms"; SourceRepo = "sickn33/antigravity-awesome-skills"; SourceUrl = "https://github.com/sickn33/antigravity-awesome-skills"; SourceSkillPath = "skills/internal-comms"; SourceLicense = "Apache-2.0"; Description = "Use when writing internal communications such as status reports, updates, FAQs, newsletters, and incident notes."; Notes = "Imported from a public Apache-2.0 skill set, replacing the former local registry copy."; },
    @{ RegistryName = "mcp-builder"; SourcePath = ".tmp/sources/sickn33-antigravity-awesome-skills/skills/mcp-builder"; SourceRepo = "sickn33/antigravity-awesome-skills"; SourceUrl = "https://github.com/sickn33/antigravity-awesome-skills"; SourceSkillPath = "skills/mcp-builder"; SourceLicense = "Apache-2.0"; Description = "Use when creating MCP servers that expose high-quality tools and resources for LLM workflows."; Notes = "Imported from a public Apache-2.0 skill set, replacing the former local registry copy."; },
    @{ RegistryName = "skill-creator"; SourcePath = ".tmp/sources/sickn33-antigravity-awesome-skills/skills/skill-creator"; SourceRepo = "sickn33/antigravity-awesome-skills"; SourceUrl = "https://github.com/sickn33/antigravity-awesome-skills"; SourceSkillPath = "skills/skill-creator"; SourceLicense = "Apache-2.0"; Description = "Use when creating or updating reusable CLI skills with progressive disclosure, validation, and installation guidance."; Notes = "Imported from a public Apache-2.0 skill set, replacing the former local registry copy."; },
    @{ RegistryName = "theme-factory"; SourcePath = ".tmp/sources/sickn33-antigravity-awesome-skills/skills/theme-factory"; SourceRepo = "sickn33/antigravity-awesome-skills"; SourceUrl = "https://github.com/sickn33/antigravity-awesome-skills"; SourceSkillPath = "skills/theme-factory"; SourceLicense = "Apache-2.0"; Description = "Use when applying cohesive font and color themes to slides, docs, landing pages, and other artifacts."; Notes = "Imported from a public Apache-2.0 skill set, replacing the former local registry copy."; },
    @{ RegistryName = "web-artifacts-builder"; SourcePath = ".tmp/sources/sickn33-antigravity-awesome-skills/skills/web-artifacts-builder"; SourceRepo = "sickn33/antigravity-awesome-skills"; SourceUrl = "https://github.com/sickn33/antigravity-awesome-skills"; SourceSkillPath = "skills/web-artifacts-builder"; SourceLicense = "Apache-2.0"; Description = "Use when building rich frontend artifacts with React, TypeScript, Tailwind, and bundled single-file outputs."; Notes = "Imported from a public Apache-2.0 skill set, replacing the former local registry copy."; },
    @{ RegistryName = "webapp-testing"; SourcePath = ".tmp/sources/sickn33-antigravity-awesome-skills/skills/webapp-testing"; SourceRepo = "sickn33/antigravity-awesome-skills"; SourceUrl = "https://github.com/sickn33/antigravity-awesome-skills"; SourceSkillPath = "skills/webapp-testing"; SourceLicense = "Apache-2.0"; Description = "Use when testing local web applications with Playwright-based scripts and managed server lifecycles."; Notes = "Imported from a public Apache-2.0 skill set, replacing the former local registry copy."; },

    @{ RegistryName = "superpowers-brainstorming"; SourcePath = ".tmp/sources/obra-superpowers/skills/brainstorming"; SourceRepo = "obra/superpowers"; SourceUrl = "https://github.com/obra/superpowers"; SourceSkillPath = "skills/brainstorming"; SourceLicense = "MIT"; Description = "Use for structured ideation, option generation, and exploratory planning before committing to an implementation."; Notes = "Imported from a public MIT repository."; },
    @{ RegistryName = "superpowers-dispatching-parallel-agents"; SourcePath = ".tmp/sources/obra-superpowers/skills/dispatching-parallel-agents"; SourceRepo = "obra/superpowers"; SourceUrl = "https://github.com/obra/superpowers"; SourceSkillPath = "skills/dispatching-parallel-agents"; SourceLicense = "MIT"; Description = "Use when independent subtasks can be delegated in parallel without overlapping ownership."; Notes = "Imported from a public MIT repository."; },
    @{ RegistryName = "superpowers-executing-plans"; SourcePath = ".tmp/sources/obra-superpowers/skills/executing-plans"; SourceRepo = "obra/superpowers"; SourceUrl = "https://github.com/obra/superpowers"; SourceSkillPath = "skills/executing-plans"; SourceLicense = "MIT"; Description = "Use when following an approved implementation plan and keeping work aligned to explicit checkpoints."; Notes = "Imported from a public MIT repository."; },
    @{ RegistryName = "superpowers-finishing-a-development-branch"; SourcePath = ".tmp/sources/obra-superpowers/skills/finishing-a-development-branch"; SourceRepo = "obra/superpowers"; SourceUrl = "https://github.com/obra/superpowers"; SourceSkillPath = "skills/finishing-a-development-branch"; SourceLicense = "MIT"; Description = "Use when finalizing branch work, verifying readiness, and preparing a branch for handoff."; Notes = "Imported from a public MIT repository."; },
    @{ RegistryName = "superpowers-receiving-code-review"; SourcePath = ".tmp/sources/obra-superpowers/skills/receiving-code-review"; SourceRepo = "obra/superpowers"; SourceUrl = "https://github.com/obra/superpowers"; SourceSkillPath = "skills/receiving-code-review"; SourceLicense = "MIT"; Description = "Use when processing review feedback and converting comments into concrete follow-up actions."; Notes = "Imported from a public MIT repository."; },
    @{ RegistryName = "superpowers-requesting-code-review"; SourcePath = ".tmp/sources/obra-superpowers/skills/requesting-code-review"; SourceRepo = "obra/superpowers"; SourceUrl = "https://github.com/obra/superpowers"; SourceSkillPath = "skills/requesting-code-review"; SourceLicense = "MIT"; Description = "Use when preparing code for review and asking another agent or reviewer for a focused pass."; Notes = "Imported from a public MIT repository."; },
    @{ RegistryName = "superpowers-subagent-driven-development"; SourcePath = ".tmp/sources/obra-superpowers/skills/subagent-driven-development"; SourceRepo = "obra/superpowers"; SourceUrl = "https://github.com/obra/superpowers"; SourceSkillPath = "skills/subagent-driven-development"; SourceLicense = "MIT"; Description = "Use when coordinating multi-agent implementation with explicit ownership and integration boundaries."; Notes = "Imported from a public MIT repository."; },
    @{ RegistryName = "superpowers-systematic-debugging"; SourcePath = ".tmp/sources/obra-superpowers/skills/systematic-debugging"; SourceRepo = "obra/superpowers"; SourceUrl = "https://github.com/obra/superpowers"; SourceSkillPath = "skills/systematic-debugging"; SourceLicense = "MIT"; Description = "Use when debugging failures and you need root-cause analysis before proposing fixes."; Notes = "Imported from a public MIT repository."; },
    @{ RegistryName = "superpowers-test-driven-development"; SourcePath = ".tmp/sources/obra-superpowers/skills/test-driven-development"; SourceRepo = "obra/superpowers"; SourceUrl = "https://github.com/obra/superpowers"; SourceSkillPath = "skills/test-driven-development"; SourceLicense = "MIT"; Description = "Use when implementing behavior through a test-first workflow with tight verification loops."; Notes = "Imported from a public MIT repository."; },
    @{ RegistryName = "superpowers-using-git-worktrees"; SourcePath = ".tmp/sources/obra-superpowers/skills/using-git-worktrees"; SourceRepo = "obra/superpowers"; SourceUrl = "https://github.com/obra/superpowers"; SourceSkillPath = "skills/using-git-worktrees"; SourceLicense = "MIT"; Description = "Use when coordinating multiple branches or agent workspaces via git worktrees."; Notes = "Imported from a public MIT repository."; },
    @{ RegistryName = "superpowers-using-superpowers"; SourcePath = ".tmp/sources/obra-superpowers/skills/using-superpowers"; SourceRepo = "obra/superpowers"; SourceUrl = "https://github.com/obra/superpowers"; SourceSkillPath = "skills/using-superpowers"; SourceLicense = "MIT"; Description = "Use as an overview for the obra superpowers workflow and associated companion skills."; Notes = "Imported from a public MIT repository."; },
    @{ RegistryName = "superpowers-verification-before-completion"; SourcePath = ".tmp/sources/obra-superpowers/skills/verification-before-completion"; SourceRepo = "obra/superpowers"; SourceUrl = "https://github.com/obra/superpowers"; SourceSkillPath = "skills/verification-before-completion"; SourceLicense = "MIT"; Description = "Use before claiming work is complete; requires fresh verification evidence before success statements."; Notes = "Imported from a public MIT repository."; },
    @{ RegistryName = "superpowers-writing-plans"; SourcePath = ".tmp/sources/obra-superpowers/skills/writing-plans"; SourceRepo = "obra/superpowers"; SourceUrl = "https://github.com/obra/superpowers"; SourceSkillPath = "skills/writing-plans"; SourceLicense = "MIT"; Description = "Use when turning goals into implementation plans, checkpoints, and execution-ready task breakdowns."; Notes = "Imported from a public MIT repository."; },
    @{ RegistryName = "superpowers-writing-skills"; SourcePath = ".tmp/sources/obra-superpowers/skills/writing-skills"; SourceRepo = "obra/superpowers"; SourceUrl = "https://github.com/obra/superpowers"; SourceSkillPath = "skills/writing-skills"; SourceLicense = "MIT"; Description = "Use when authoring or refining reusable agent skills with concise triggering metadata and guidance."; Notes = "Imported from a public MIT repository."; },

    @{ RegistryName = "affaan-browser-qa"; SourcePath = ".tmp/sources/affaan-everything-claude-code/skills/browser-qa"; SourceRepo = "affaan-m/everything-claude-code"; SourceUrl = "https://github.com/affaan-m/everything-claude-code"; SourceSkillPath = "skills/browser-qa"; SourceLicense = "MIT"; Description = "Use for automated browser smoke tests, UI interaction checks, and visual QA on preview or live pages."; Notes = "Imported from a public MIT repository and wrapped with UniText frontmatter."; },
    @{ RegistryName = "affaan-coding-standards"; SourcePath = ".tmp/sources/affaan-everything-claude-code/skills/coding-standards"; SourceRepo = "affaan-m/everything-claude-code"; SourceUrl = "https://github.com/affaan-m/everything-claude-code"; SourceSkillPath = "skills/coding-standards"; SourceLicense = "MIT"; Description = "Use for cross-project coding standards, naming conventions, maintainability checks, and quality baselines."; Notes = "Imported from a public MIT repository and wrapped with UniText frontmatter."; },
    @{ RegistryName = "affaan-design-system"; SourcePath = ".tmp/sources/affaan-everything-claude-code/skills/design-system"; SourceRepo = "affaan-m/everything-claude-code"; SourceUrl = "https://github.com/affaan-m/everything-claude-code"; SourceSkillPath = "skills/design-system"; SourceLicense = "MIT"; Description = "Use when generating or auditing a design system, extracting tokens, and reviewing visual consistency."; Notes = "Imported from a public MIT repository and wrapped with UniText frontmatter."; },
    @{ RegistryName = "affaan-mcp-server-patterns"; SourcePath = ".tmp/sources/affaan-everything-claude-code/skills/mcp-server-patterns"; SourceRepo = "affaan-m/everything-claude-code"; SourceUrl = "https://github.com/affaan-m/everything-claude-code"; SourceSkillPath = "skills/mcp-server-patterns"; SourceLicense = "MIT"; Description = "Use when building MCP servers with Node or TypeScript, including tools, resources, prompts, and transport choices."; Notes = "Imported from a public MIT repository and wrapped with UniText frontmatter."; },

    @{ RegistryName = "copilot-cli-mastery"; SourcePath = ".tmp/sources/github-awesome-copilot/skills/cli-mastery"; SourceRepo = "github/awesome-copilot"; SourceUrl = "https://github.com/github/awesome-copilot"; SourceSkillPath = "skills/cli-mastery"; SourceLicense = "MIT"; Description = "Use for GitHub Copilot CLI training, command discovery, and operator reference workflows."; Notes = "Imported from a public MIT repository."; },
    @{ RegistryName = "copilot-create-agentsmd"; SourcePath = ".tmp/sources/github-awesome-copilot/skills/create-agentsmd"; SourceRepo = "github/awesome-copilot"; SourceUrl = "https://github.com/github/awesome-copilot"; SourceSkillPath = "skills/create-agentsmd"; SourceLicense = "MIT"; Description = "Use when generating or revising a repository AGENTS.md file grounded in the agents.md format."; Notes = "Imported from a public MIT repository."; },
    @{ RegistryName = "copilot-documentation-writer"; SourcePath = ".tmp/sources/github-awesome-copilot/skills/documentation-writer"; SourceRepo = "github/awesome-copilot"; SourceUrl = "https://github.com/github/awesome-copilot"; SourceSkillPath = "skills/documentation-writer"; SourceLicense = "MIT"; Description = "Use when writing software documentation with a Diataxis-oriented structure and reader-focused separation of doc types."; Notes = "Imported from a public MIT repository."; },
    @{ RegistryName = "copilot-quality-playbook"; SourcePath = ".tmp/sources/github-awesome-copilot/skills/quality-playbook"; SourceRepo = "github/awesome-copilot"; SourceUrl = "https://github.com/github/awesome-copilot"; SourceSkillPath = "skills/quality-playbook"; SourceLicense = "MIT"; Description = "Use for codebase quality baselines, specification-grounded audits, testing protocols, and repeatable quality systems."; Notes = "Imported from a public MIT repository."; },
    @{ RegistryName = "copilot-web-design-reviewer"; SourcePath = ".tmp/sources/github-awesome-copilot/skills/web-design-reviewer"; SourceRepo = "github/awesome-copilot"; SourceUrl = "https://github.com/github/awesome-copilot"; SourceSkillPath = "skills/web-design-reviewer"; SourceLicense = "MIT"; Description = "Use when visually reviewing or fixing website layout, responsive behavior, accessibility, and design consistency."; Notes = "Imported from a public MIT repository."; },

    @{ RegistryName = "nlb-banner-design"; SourcePath = ".tmp/sources/nextlevelbuilder-ui-ux-pro-max-skill/.claude/skills/banner-design"; SourceRepo = "nextlevelbuilder/ui-ux-pro-max-skill"; SourceUrl = "https://github.com/nextlevelbuilder/ui-ux-pro-max-skill"; SourceSkillPath = ".claude/skills/banner-design"; SourceLicense = "MIT"; Description = "Use when creating banners, hero art, and visual marketing surfaces with deliberate design systems."; Notes = "Imported from a public MIT repository."; },
    @{ RegistryName = "nlb-design"; SourcePath = ".tmp/sources/nextlevelbuilder-ui-ux-pro-max-skill/.claude/skills/design"; SourceRepo = "nextlevelbuilder/ui-ux-pro-max-skill"; SourceUrl = "https://github.com/nextlevelbuilder/ui-ux-pro-max-skill"; SourceSkillPath = ".claude/skills/design"; SourceLicense = "MIT"; Description = "Use for broad product design work covering UI structure, visual direction, and interaction decisions."; Notes = "Imported from a public MIT repository."; },
    @{ RegistryName = "nlb-ui-styling"; SourcePath = ".tmp/sources/nextlevelbuilder-ui-ux-pro-max-skill/.claude/skills/ui-styling"; SourceRepo = "nextlevelbuilder/ui-ux-pro-max-skill"; SourceUrl = "https://github.com/nextlevelbuilder/ui-ux-pro-max-skill"; SourceSkillPath = ".claude/skills/ui-styling"; SourceLicense = "MIT"; Description = "Use when styling interfaces with shadcn/ui, Tailwind, accessible components, and theme systems."; Notes = "Imported from a public MIT repository."; },
    @{ RegistryName = "nlb-ui-ux-pro-max"; SourcePath = ".tmp/sources/nextlevelbuilder-ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max"; SourceRepo = "nextlevelbuilder/ui-ux-pro-max-skill"; SourceUrl = "https://github.com/nextlevelbuilder/ui-ux-pro-max-skill"; SourceSkillPath = ".claude/skills/ui-ux-pro-max"; SourceLicense = "MIT"; Description = "Use for high-coverage UI and UX guidance across web and mobile stacks, layouts, components, and visual systems."; Notes = "Imported from a public MIT repository."; },

    @{ RegistryName = "antigravity-algorithmic-art"; SourcePath = ".tmp/sources/sickn33-antigravity-awesome-skills/skills/algorithmic-art"; SourceRepo = "sickn33/antigravity-awesome-skills"; SourceUrl = "https://github.com/sickn33/antigravity-awesome-skills"; SourceSkillPath = "skills/algorithmic-art"; SourceLicense = "Apache-2.0"; Description = "Use when creating algorithmic art concepts and expressing them as generative p5.js outputs."; Notes = "Imported from a public Apache-2.0 skill set."; },
    @{ RegistryName = "antigravity-canvas-design"; SourcePath = ".tmp/sources/sickn33-antigravity-awesome-skills/skills/canvas-design"; SourceRepo = "sickn33/antigravity-awesome-skills"; SourceUrl = "https://github.com/sickn33/antigravity-awesome-skills"; SourceSkillPath = "skills/canvas-design"; SourceLicense = "Apache-2.0"; Description = "Use when producing design philosophies and expressing them as canvas-based PNG or PDF artifacts."; Notes = "Imported from a public Apache-2.0 skill set."; }
)

    $catalogOnlySources = @(
    @{
        Repo = "VoltAgent/awesome-openclaw-skills"
        Url = "https://github.com/VoltAgent/awesome-openclaw-skills"
        License = "MIT"
        Notes = "Catalog-only source. No native SKILL.md directories were found in the cloned repository on 2026-03-27."
    }
)

foreach ($skillName in $removedSkills) {
    $skillDirectory = Join-Path $registry $skillName
    if (Test-Path $skillDirectory) {
        Remove-Item $skillDirectory -Recurse -Force
    }
}

foreach ($info in $retainedSkills) {
    $skillDirectory = Join-Path $registry $info.RegistryName
    if (-not (Test-Path $skillDirectory)) {
        throw "Retained skill missing: $($info.RegistryName)"
    }

    Write-SourceYaml -SkillDirectory $skillDirectory -Info $info
}

foreach ($info in $imports) {
    $sourceDirectory = Join-Path $root $info.SourcePath
    $targetDirectory = Join-Path $registry $info.RegistryName

    if (-not (Test-Path $sourceDirectory)) {
        throw "Source skill missing: $sourceDirectory"
    }

    if (Test-Path $targetDirectory) {
        Backup-PreservedPatchFiles -SkillName $info.RegistryName -SkillDirectory $targetDirectory
    }

    Copy-SkillDirectory -SourcePath $sourceDirectory -DestinationPath $targetDirectory
    Restore-PreservedPatchFiles -SkillName $info.RegistryName -SkillDirectory $targetDirectory
    Set-SkillFrontmatter -SkillDirectory $targetDirectory -SkillName $info.RegistryName -Description $info.Description -License $info.SourceLicense
    $sourceRevision = Get-GitRevision -StartPath $sourceDirectory
    if (-not $sourceRevision) {
        $sourceRevision = "unrecorded-import-snapshot-$importDate"
    }
    $licenseEvidence = Get-LicenseEvidence -SkillDirectory $sourceDirectory

    Write-SourceYaml -SkillDirectory $targetDirectory -Info @{
        RegistryName = $info.RegistryName
        SourceType = "github-import"
        SourceRepo = $info.SourceRepo
        SourceUrl = $info.SourceUrl
        SourcePath = $info.SourceSkillPath
        SourceLicense = $info.SourceLicense
        ImportedAt = $importDate
        SourceRevision = $sourceRevision
        LicenseEvidencePath = $licenseEvidence.Path
        LicenseEvidenceScope = $licenseEvidence.Scope
        LicenseScopeNote = "$($licenseEvidence.Note) source_path and source_revision recorded from the local source clone."
        ProvenanceConfidence = if ($licenseEvidence.Path) { "path-level-evidence-available" } else { "repo-license-relied-upon" }
        ImportMethod = "curated-copy"
        Notes = $info.Notes
    }
}

$catalogLines = @(
    "# Skill Sources",
    "",
    "This index records the active skills in registry/skills and their source metadata.",
    "",
    "## Active Skills",
    "",
    "| Skill | Source Type | Source Repo | License | Source Data |",
    "|---|---|---|---|---|"
)

$activeRows = @()
foreach ($skillDirectory in (Get-ChildItem $registry -Directory | Sort-Object Name)) {
    $sourceFile = Join-Path $skillDirectory.FullName "SOURCE.yaml"
    if (-not (Test-Path $sourceFile)) {
        continue
    }

    $sourceLines = Get-Content $sourceFile
    $sourceType = Read-SourceValue -Lines $sourceLines -Key "source_type"
    $sourceRepo = Read-SourceValue -Lines $sourceLines -Key "source_repo"
    $sourceLicense = Read-SourceValue -Lines $sourceLines -Key "source_license"
    $activeRows += "| [$($skillDirectory.Name)]($($skillDirectory.Name)/SKILL.md) | $sourceType | $sourceRepo | $sourceLicense | [$($skillDirectory.Name)/SOURCE.yaml]($($skillDirectory.Name)/SOURCE.yaml) |"
}

$catalogLines += $activeRows
$catalogLines += @(
    "",
    "## Catalog-Only Source Repositories",
    "",
    "| Repository | License | Notes |",
    "|---|---|---|"
)

foreach ($catalog in $catalogOnlySources) {
    $catalogLines += "| [$($catalog.Repo)]($($catalog.Url)) | $($catalog.License) | $($catalog.Notes) |"
}

$catalogLines += @(
    "",
    "## Removed During 2026-03-27 Cleanup",
    ""
)

foreach ($skillName in $removedSkills) {
    $catalogLines += "- ``$skillName``"
}

Set-FileContentWithRetry -Path (Join-Path $registry "SOURCES.md") -Content ($catalogLines -join "`n")
