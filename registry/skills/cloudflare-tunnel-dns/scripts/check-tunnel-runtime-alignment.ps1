param(
    [string]$AuthoringRoot = "Q:\Projects\tb2-claude-subagent-workflow",
    [string]$ProdConfigPath = "Q:\Services\tb2-prod\ops\cloudflared.tb2.yml",
    [string]$StagingConfigPath = "Q:\Services\tb2-staging\ops\cloudflared.tb2.yml",
    [string]$ProdReleaseInfoPath = "Q:\Services\tb2-prod\release-info.json",
    [string]$ReleaseTargetsPath = "Q:\Projects\tb2-claude-subagent-workflow\ops\release-targets.json",
    [string]$InventoryJsonPath,
    [string]$MarkdownOutputPath,
    [string]$JsonOutputPath
)

$ErrorActionPreference = "Stop"

function Read-TextFile {
    param([string]$Path)

    if (-not (Test-Path -LiteralPath $Path)) {
        return $null
    }

    return Get-Content -LiteralPath $Path -Raw
}

function Parse-CloudflaredConfig {
    param([string]$Path)

    $text = Read-TextFile -Path $Path
    if (-not $text) {
        return $null
    }

    $tunnelMatch = [Regex]::Match($text, '(?m)^tunnel:\s*(.+)$')
    $credentialsMatch = [Regex]::Match($text, '(?m)^credentials-file:\s*(.+)$')
    $ingressMatches = [Regex]::Matches($text, '(?ms)-\s+hostname:\s*(?<hostname>[^\r\n]+)\s+service:\s*(?<service>[^\r\n]+)')

    $ingress = @()
    foreach ($match in $ingressMatches) {
        $ingress += [ordered]@{
            hostname = $match.Groups["hostname"].Value.Trim()
            service = $match.Groups["service"].Value.Trim()
        }
    }

    return [ordered]@{
        path = $Path
        tunnel = if ($tunnelMatch.Success) { $tunnelMatch.Groups[1].Value.Trim() } else { $null }
        credentialsFile = if ($credentialsMatch.Success) { $credentialsMatch.Groups[1].Value.Trim() } else { $null }
        ingress = $ingress
        rawText = $text
    }
}

function Resolve-StageCloudflaredSourceFile {
    param(
        [string]$RootDir,
        [string]$StageName
    )

    $stageSpecific = Join-Path $RootDir ("ops\cloudflared.tb2.{0}.yml" -f $StageName)
    if (Test-Path -LiteralPath $stageSpecific) {
        return $stageSpecific
    }

    return (Join-Path $RootDir "ops\cloudflared.tb2.yml")
}

function Normalize-IngressSignature {
    param([object[]]$Ingress)

    if (-not $Ingress) {
        return @()
    }

    return @($Ingress | ForEach-Object { "{0}->{1}" -f $_.hostname, $_.service } | Sort-Object)
}

function Get-InventoryMapping {
    param([string]$InventoryJsonPath)

    if (-not $InventoryJsonPath -or -not (Test-Path -LiteralPath $InventoryJsonPath)) {
        return $null
    }

    $json = Get-Content -LiteralPath $InventoryJsonPath -Raw | ConvertFrom-Json -Depth 12
    $tunnelNameById = @{}
    foreach ($item in @($json.tunnels.items)) {
        if ($item.id) {
            $tunnelNameById[$item.id] = $item.name
        }
    }

    $dns = @()
    foreach ($record in @($json.dnsRecords.items)) {
        if ($record.type -eq "CNAME" -and $record.content -match '^(?<id>[0-9a-f-]+)\.cfargotunnel\.com$') {
            $tunnelId = $matches["id"]
            $dns += [ordered]@{
                hostname = $record.name
                tunnelId = $tunnelId
                tunnelName = $tunnelNameById[$tunnelId]
                proxied = $record.proxied
            }
        }
    }

    return [ordered]@{
        raw = $json
        tunnelNameById = $tunnelNameById
        dnsTunnelRecords = $dns
    }
}

$authoringProd = Parse-CloudflaredConfig -Path (Resolve-StageCloudflaredSourceFile -RootDir $AuthoringRoot -StageName "prod")
$authoringStaging = Parse-CloudflaredConfig -Path (Resolve-StageCloudflaredSourceFile -RootDir $AuthoringRoot -StageName "staging")
$prod = Parse-CloudflaredConfig -Path $ProdConfigPath
$staging = Parse-CloudflaredConfig -Path $StagingConfigPath
$prodReleaseInfo = if (Test-Path -LiteralPath $ProdReleaseInfoPath) {
    Get-Content -LiteralPath $ProdReleaseInfoPath -Raw | ConvertFrom-Json -Depth 8
} else {
    $null
}
$releaseTargets = if (Test-Path -LiteralPath $ReleaseTargetsPath) {
    Get-Content -LiteralPath $ReleaseTargetsPath -Raw | ConvertFrom-Json -Depth 8
} else {
    $null
}
$inventory = Get-InventoryMapping -InventoryJsonPath $InventoryJsonPath

$authoringProdIngressSignature = @(Normalize-IngressSignature -Ingress $authoringProd.ingress)
$authoringStagingIngressSignature = @(Normalize-IngressSignature -Ingress $authoringStaging.ingress)
$prodIngressSignature = @(Normalize-IngressSignature -Ingress $prod.ingress)
$stagingIngressSignature = @(Normalize-IngressSignature -Ingress $staging.ingress)

$localTunnelIds = @(
    $authoringProd.tunnel
    $authoringStaging.tunnel
    $prod.tunnel
    $staging.tunnel
) | Where-Object { $_ } | Select-Object -Unique
$localTunnelIds = @($localTunnelIds)

$runtimeFindings = [ordered]@{
    tunnelIdAligned = [bool]($localTunnelIds.Count -eq 1)
    credentialsAligned = [bool]($authoringProd.credentialsFile -and $authoringProd.credentialsFile -eq $authoringStaging.credentialsFile -and $authoringStaging.credentialsFile -eq $prod.credentialsFile -and $prod.credentialsFile -eq $staging.credentialsFile)
    prodIngressAligned = [bool](
        ($authoringProdIngressSignature.Count -eq $prodIngressSignature.Count) -and
        (@(Compare-Object $authoringProdIngressSignature $prodIngressSignature).Count -eq 0)
    )
    stagingIngressAligned = [bool](
        ($authoringStagingIngressSignature.Count -eq $stagingIngressSignature.Count) -and
        (@(Compare-Object $authoringStagingIngressSignature $stagingIngressSignature).Count -eq 0)
    )
}

$prodHealthHost = if ($prodReleaseInfo) { $prodReleaseInfo.public_health_host } else { $null }
$prodExpectedHealthHost = if ($releaseTargets) { $releaseTargets.stages.prod.public_health_host } else { $null }
$stagingExpectedHealthHost = if ($releaseTargets) { $releaseTargets.stages.staging.public_health_host } else { $null }
$prodIngressHosts = @($prod.ingress | ForEach-Object { $_.hostname })
$stagingIngressHosts = @($staging.ingress | ForEach-Object { $_.hostname })

$inventoryFindings = [ordered]@{
    inventoryLoaded = [bool]$inventory
    dnsMatchesLocalTunnel = $null
    dnsTunnelHostnames = @()
}

if ($inventory) {
    $localTunnelId = if ($runtimeFindings.tunnelIdAligned) { $localTunnelIds[0] } else { $null }
    $inventoryFindings.dnsTunnelHostnames = @($inventory.dnsTunnelRecords)
    if ($localTunnelId) {
        $inventoryFindings.dnsMatchesLocalTunnel = [bool](
            @($inventory.dnsTunnelRecords | Where-Object { $_.hostname -in @("mcp.colorgeek.co", "tb2-health.colorgeek.co") -and $_.tunnelId -eq $localTunnelId }).Count -eq 2
        )
    }
}

$result = [ordered]@{
    collectedAt = (Get-Date).ToString("o")
    local = [ordered]@{
        authoringProd = $authoringProd
        authoringStaging = $authoringStaging
        prod = $prod
        staging = $staging
    }
    runtimeMetadata = [ordered]@{
        prodReleaseInfo = $prodReleaseInfo
        releaseTargets = $releaseTargets
    }
    findings = [ordered]@{
    runtime = $runtimeFindings
    prodHealthHostMatchesReleaseTarget = [bool]($prodHealthHost -and $prodExpectedHealthHost -and $prodHealthHost -eq $prodExpectedHealthHost)
    prodIngressContainsExpectedHealthHost = [bool]($prodExpectedHealthHost -and $prodIngressHosts -contains $prodExpectedHealthHost)
    stagingIngressContainsExpectedHealthHost = [bool]($stagingExpectedHealthHost -and $stagingIngressHosts -contains $stagingExpectedHealthHost)
    stagingIngressContainsProdHealthHost = [bool]($prodExpectedHealthHost -and $stagingIngressHosts -contains $prodExpectedHealthHost)
    stagingExpectedHealthHost = $stagingExpectedHealthHost
    inventory = $inventoryFindings
  }
}

$markdown = @(
    "# Cloudflare Tunnel Runtime Alignment",
    "",
    "- Collected at: $($result.collectedAt)",
    "- Local tunnel IDs aligned: $($result.findings.runtime.tunnelIdAligned)",
    "- Credentials path aligned: $($result.findings.runtime.credentialsAligned)",
    "- Prod ingress aligned with authoring source: $($result.findings.runtime.prodIngressAligned)",
    "- Staging ingress aligned with authoring source: $($result.findings.runtime.stagingIngressAligned)",
    "- Prod health host matches release target: $($result.findings.prodHealthHostMatchesReleaseTarget)",
    "- Prod ingress contains expected health host: $($result.findings.prodIngressContainsExpectedHealthHost)",
    "- Staging ingress contains expected health host: $($result.findings.stagingIngressContainsExpectedHealthHost)",
    "- Staging ingress still contains prod health host: $($result.findings.stagingIngressContainsProdHealthHost)",
    "- Staging expected health host: $($result.findings.stagingExpectedHealthHost)",
    "- Inventory loaded: $($result.findings.inventory.inventoryLoaded)",
    "- DNS matches local tunnel for prod hosts: $($result.findings.inventory.dnsMatchesLocalTunnel)",
    "",
    "## Local Config",
    "",
    "- Authoring prod tunnel: $($authoringProd.tunnel)",
    "- Authoring staging tunnel: $($authoringStaging.tunnel)",
    "- Prod tunnel: $($prod.tunnel)",
    "- Staging tunnel: $($staging.tunnel)",
    "- Credentials file: $($prod.credentialsFile)",
    ""
)

if ($authoringProd.ingress) {
    $markdown += "## Prod Ingress Source"
    $markdown += ""
    foreach ($item in $authoringProd.ingress) {
        $markdown += "- $($item.hostname) -> $($item.service)"
    }
}

if ($authoringStaging.ingress) {
    $markdown += ""
    $markdown += "## Staging Ingress Source"
    $markdown += ""
    foreach ($item in $authoringStaging.ingress) {
        $markdown += "- $($item.hostname) -> $($item.service)"
    }
}

if ($inventory -and $inventory.dnsTunnelRecords.Count -gt 0) {
    $markdown += ""
    $markdown += "## DNS Tunnel Records"
    $markdown += ""
    foreach ($record in $inventory.dnsTunnelRecords) {
        $markdown += "- $($record.hostname) -> $($record.tunnelId) ($($record.tunnelName)) proxied=$($record.proxied)"
    }
}

$jsonText = $result | ConvertTo-Json -Depth 10
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
