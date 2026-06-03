param(
    [string]$InventoryJsonPath,
    [string]$AuthoringRoot = ".",
    [string]$ReleaseTargetsPath = "ops\release-targets.json",
    [string]$Stage = "staging",
    [string]$TunnelName = "tb2-public-prod-20260330",
    [string]$JsonOutputPath,
    [string]$MarkdownOutputPath
)

$ErrorActionPreference = "Stop"

function ConvertFrom-JsonCompat {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Text,
        [int]$Depth = 12
    )

    $command = Get-Command ConvertFrom-Json
    if ($command.Parameters.ContainsKey("Depth")) {
        return ($Text | ConvertFrom-Json -Depth $Depth)
    }

    return ($Text | ConvertFrom-Json)
}

function Resolve-OptionalPath {
    param(
        [string]$Path,
        [string]$BasePath
    )

    if ([string]::IsNullOrWhiteSpace($Path)) {
        return $null
    }

    if ([IO.Path]::IsPathRooted($Path)) {
        return $Path
    }

    if ([string]::IsNullOrWhiteSpace($BasePath)) {
        return $Path
    }

    return (Join-Path $BasePath $Path)
}

function Read-JsonFile {
    param([string]$Path)

    if ([string]::IsNullOrWhiteSpace($Path) -or -not (Test-Path -LiteralPath $Path)) {
        throw "Missing required JSON file: $Path"
    }

    return (ConvertFrom-JsonCompat -Text (Get-Content -LiteralPath $Path -Raw) -Depth 12)
}

function Select-StageTarget {
    param(
        [object]$ReleaseTargets,
        [string]$StageName
    )

    $stageConfig = $ReleaseTargets.stages.$StageName
    if (-not $stageConfig) {
        throw "Stage '$StageName' not found in release targets."
    }

    if (-not $stageConfig.public_health_host) {
        throw "Stage '$StageName' does not declare public_health_host."
    }

    return $stageConfig
}

function Get-InventoryItems {
    param(
        [object]$Container
    )

    if (-not $Container) {
        return @()
    }

    if ($Container -is [System.Collections.IEnumerable] -and -not ($Container -is [string])) {
        return @($Container)
    }

    return @($Container)
}

$resolvedAuthoringRoot = Resolve-OptionalPath -Path $AuthoringRoot -BasePath (Get-Location).Path
$resolvedInventoryJsonPath = Resolve-OptionalPath -Path $InventoryJsonPath -BasePath (Get-Location).Path
$resolvedReleaseTargetsPath = Resolve-OptionalPath -Path $ReleaseTargetsPath -BasePath $resolvedAuthoringRoot

$inventory = Read-JsonFile -Path $resolvedInventoryJsonPath
$releaseTargets = Read-JsonFile -Path $resolvedReleaseTargetsPath
$stageConfig = Select-StageTarget -ReleaseTargets $releaseTargets -StageName $Stage
$targetHost = $stageConfig.public_health_host
$prodHealthHost = $releaseTargets.stages.prod.public_health_host

$dnsItems = @(Get-InventoryItems -Container $inventory.dnsRecords.items)
$accessItems = @(Get-InventoryItems -Container $inventory.accessApps.items)
$tunnelItems = @(Get-InventoryItems -Container $inventory.tunnels.items)

$resolvedTunnel = $tunnelItems | Where-Object { $_.name -eq $TunnelName } | Select-Object -First 1
$targetDns = $dnsItems | Where-Object { $_.name -eq $targetHost } | Select-Object -First 1
$prodDns = $dnsItems | Where-Object { $_.name -eq $prodHealthHost } | Select-Object -First 1
$targetAccessApp = $accessItems | Where-Object { $_.domain -eq $targetHost } | Select-Object -First 1
$prodAccessApp = $accessItems | Where-Object { $_.domain -eq $prodHealthHost } | Select-Object -First 1
$stagePublicApps = @($accessItems | Where-Object {
    $_.domain -and $_.domain -like "*-staging.colorgeek.co"
})

$recommendedDnsContent = if ($resolvedTunnel) {
    "{0}.cfargotunnel.com" -f $resolvedTunnel.id
} else {
    $null
}

$dnsAction = "none"
if (-not $resolvedTunnel) {
    $dnsAction = "blocked-missing-tunnel"
} elseif (-not $targetDns) {
    $dnsAction = "create"
} elseif ($recommendedDnsContent -and $targetDns.content -ne $recommendedDnsContent) {
    $dnsAction = "update-target"
}

$accessAction = if ($targetAccessApp) {
    "already-present"
} elseif ($prodAccessApp) {
    "consider-cloning-prod-pattern"
} elseif ($stagePublicApps.Count -gt 0) {
    "review-needed-no-prod-health-analogue"
} else {
    "no-visible-signal"
}

$notes = @(
    "This script is read-only and does not mutate Cloudflare resources."
)
if ($resolvedTunnel) {
    $notes += "DNS can be planned directly because the target tunnel is visible."
} else {
    $notes += "The target tunnel was not visible in inventory, so confirm the tunnel target before planning DNS activation."
}
if (-not $prodAccessApp) {
    $notes += "No prod health Access app was visible, so Access creation for the staging health host should remain a policy decision."
}

$blockers = @()
if (-not $resolvedTunnel) {
    $blockers += "Resolved tunnel '$TunnelName' was not visible in inventory."
}

$plan = [ordered]@{
    collectedAt = (Get-Date).ToString("o")
    stage = $Stage
    targetHost = $targetHost
    prodHealthHost = $prodHealthHost
    tunnel = [ordered]@{
        requestedName = $TunnelName
        resolved = if ($resolvedTunnel) {
            [ordered]@{
                id = $resolvedTunnel.id
                name = $resolvedTunnel.name
            }
        } else {
            $null
        }
    }
    dns = [ordered]@{
        action = $dnsAction
        existingRecord = if ($targetDns) {
            [ordered]@{
                id = $targetDns.id
                type = $targetDns.type
                name = $targetDns.name
                content = $targetDns.content
                proxied = $targetDns.proxied
            }
        } else {
            $null
        }
        prodReference = if ($prodDns) {
            [ordered]@{
                id = $prodDns.id
                name = $prodDns.name
                content = $prodDns.content
                proxied = $prodDns.proxied
            }
        } else {
            $null
        }
        recommendedRecord = if ($recommendedDnsContent) {
            [ordered]@{
                type = "CNAME"
                name = $targetHost
                content = $recommendedDnsContent
                proxied = $true
            }
        } else {
            $null
        }
    }
    access = [ordered]@{
        action = $accessAction
        existingApp = if ($targetAccessApp) {
            [ordered]@{
                id = $targetAccessApp.id
                name = $targetAccessApp.name
                domain = $targetAccessApp.domain
                type = $targetAccessApp.type
            }
        } else {
            $null
        }
        prodReference = if ($prodAccessApp) {
            [ordered]@{
                id = $prodAccessApp.id
                name = $prodAccessApp.name
                domain = $prodAccessApp.domain
                type = $prodAccessApp.type
            }
        } else {
            $null
        }
        visibleStagePublicApps = @($stagePublicApps | Select-Object id, name, domain, type)
    }
    blockers = $blockers
    notes = $notes
}

$markdown = @(
    "# Staging Public Host Activation Plan",
    "",
    "- Collected at: $($plan.collectedAt)",
    "- Stage: $($plan.stage)",
    "- Target host: $($plan.targetHost)",
    "- Prod health host: $($plan.prodHealthHost)",
    "- Resolved tunnel: $(if ($plan.tunnel.resolved) { '{0} [{1}]' -f $plan.tunnel.resolved.name, $plan.tunnel.resolved.id } else { 'missing' })",
    "- DNS action: $($plan.dns.action)",
    "- Access action: $($plan.access.action)",
    "",
    "## DNS",
    ""
)

if ($plan.dns.existingRecord) {
    $markdown += "- Existing staging DNS: $($plan.dns.existingRecord.name) -> $($plan.dns.existingRecord.content) proxied=$($plan.dns.existingRecord.proxied)"
} else {
    $markdown += "- Existing staging DNS: missing"
}

if ($plan.dns.prodReference) {
    $markdown += "- Prod reference DNS: $($plan.dns.prodReference.name) -> $($plan.dns.prodReference.content) proxied=$($plan.dns.prodReference.proxied)"
}

if ($plan.dns.recommendedRecord) {
    $markdown += "- Recommended DNS record: $($plan.dns.recommendedRecord.name) -> $($plan.dns.recommendedRecord.content) proxied=$($plan.dns.recommendedRecord.proxied)"
}

$markdown += ""
$markdown += "## Access"
$markdown += ""

if ($plan.access.existingApp) {
    $markdown += "- Existing staging Access app: $($plan.access.existingApp.name) -> $($plan.access.existingApp.domain)"
} else {
    $markdown += "- Existing staging Access app: missing"
}

if ($plan.access.prodReference) {
    $markdown += "- Prod reference Access app: $($plan.access.prodReference.name) -> $($plan.access.prodReference.domain)"
} else {
    $markdown += "- Prod reference Access app: none visible for $($plan.prodHealthHost)"
}

if ($plan.access.visibleStagePublicApps.Count -gt 0) {
    $markdown += "- Other visible staging public Access apps:"
    foreach ($app in $plan.access.visibleStagePublicApps) {
        $markdown += "  - $($app.name) -> $($app.domain)"
    }
}

if ($plan.blockers.Count -gt 0) {
    $markdown += ""
    $markdown += "## Blockers"
    $markdown += ""
    foreach ($blocker in $plan.blockers) {
        $markdown += "- $blocker"
    }
}

if ($plan.notes.Count -gt 0) {
    $markdown += ""
    $markdown += "## Notes"
    $markdown += ""
    foreach ($note in $plan.notes) {
        $markdown += "- $note"
    }
}

$jsonText = $plan | ConvertTo-Json -Depth 8
$markdownText = $markdown -join [Environment]::NewLine

if ($JsonOutputPath) {
    Set-Content -LiteralPath $JsonOutputPath -Value $jsonText
}

if ($MarkdownOutputPath) {
    Set-Content -LiteralPath $MarkdownOutputPath -Value $markdownText
}

Write-Host $markdownText
Write-Host ""
Write-Host "## JSON"
Write-Host $jsonText
