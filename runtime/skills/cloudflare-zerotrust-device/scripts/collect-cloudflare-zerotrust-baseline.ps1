param(
    [string]$AccountId,
    [string]$JsonOutputPath,
    [string]$MarkdownOutputPath,
    [switch]$SkipNetworkProbes
)

$ErrorActionPreference = "Stop"

function Invoke-CommandCapture {
    param(
        [string]$FilePath,
        [string[]]$Arguments
    )

    try {
        $output = & $FilePath @Arguments 2>&1
        return @{
            success = $true
            text = (($output | ForEach-Object { "$_" }) -join [Environment]::NewLine).Trim()
        }
    } catch {
        return @{
            success = $false
            text = $_.Exception.Message
        }
    }
}

function Find-LineValue {
    param(
        [string]$Text,
        [string]$Label
    )

    if (-not $Text) {
        return $null
    }

    $pattern = "(?m)^\s*$([Regex]::Escape($Label)):\s*(.+)$"
    $match = [Regex]::Match($Text, $pattern)
    if ($match.Success) {
        return $match.Groups[1].Value.Trim()
    }

    return $null
}

function Find-FirstLineValue {
    param(
        [string]$Text,
        [string[]]$Labels
    )

    foreach ($label in $Labels) {
        $value = Find-LineValue -Text $Text -Label $label
        if ($null -ne $value -and -not [string]::IsNullOrWhiteSpace($value)) {
            return $value
        }
    }

    return $null
}

function Convert-TraceText {
    param([string]$Text)

    $result = @{}
    if (-not $Text) {
        return $result
    }

    foreach ($line in ($Text -split "`r?`n")) {
        if ($line -match "^(?<key>[^=]+)=(?<value>.*)$") {
            $result[$matches.key] = $matches.value
        }
    }

    return $result
}

function Add-ProbeError {
    param(
        [System.Collections.Generic.List[string]]$Errors,
        [string]$Name,
        [hashtable]$Capture
    )

    if (-not $Capture.success -or [string]::IsNullOrWhiteSpace($Capture.text)) {
        $Errors.Add("$Name failed")
        return
    }

    if ($Capture.text -match "failed|unreachable|could not|error|not recognized") {
        $Errors.Add("$Name returned: $($Capture.text)")
    }
}

$probeErrors = [System.Collections.Generic.List[string]]::new()
$newLine = [Environment]::NewLine

$warpPath = (Get-Command warp-cli.exe -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source -ErrorAction SilentlyContinue)
$cloudflaredPath = (Get-Command cloudflared.exe -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source -ErrorAction SilentlyContinue)
$wslPath = (Get-Command wsl.exe -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source -ErrorAction SilentlyContinue)

$warpStatus = if ($warpPath) { Invoke-CommandCapture -FilePath $warpPath -Arguments @("status") } else { @{ success = $false; text = $null } }
$warpSettings = if ($warpPath) { Invoke-CommandCapture -FilePath $warpPath -Arguments @("settings") } else { @{ success = $false; text = $null } }
$warpRegistration = if ($warpPath) { Invoke-CommandCapture -FilePath $warpPath -Arguments @("registration", "show") } else { @{ success = $false; text = $null } }
$warpTunnelDump = if ($warpPath) { Invoke-CommandCapture -FilePath $warpPath -Arguments @("tunnel", "dump") } else { @{ success = $false; text = $null } }
$windowsRoute = Invoke-CommandCapture -FilePath "route.exe" -Arguments @("print", "-4")
$wslList = if ($wslPath) { Invoke-CommandCapture -FilePath $wslPath -Arguments @("-l", "-v") } else { @{ success = $false; text = $null } }

$ubuntuAvailable = $false
if ($wslList.success -and $wslList.text -match "Ubuntu") {
    $ubuntuAvailable = $true
}

$wslRoute = if ($ubuntuAvailable) {
    Invoke-CommandCapture -FilePath $wslPath -Arguments @("-d", "Ubuntu", "--exec", "bash", "-lc", "ip -4 addr; echo '---'; ip route")
} else {
    @{ success = $false; text = $null }
}

$windowsTrace = @{ success = $false; text = $null }
$wslTrace = @{ success = $false; text = $null }
if (-not $SkipNetworkProbes) {
    $windowsTrace = Invoke-CommandCapture -FilePath "curl.exe" -Arguments @("-s", "https://www.cloudflare.com/cdn-cgi/trace")
    if ($ubuntuAvailable) {
        $wslTrace = Invoke-CommandCapture -FilePath $wslPath -Arguments @("-d", "Ubuntu", "--exec", "bash", "-lc", "curl -s https://www.cloudflare.com/cdn-cgi/trace")
    }
}

if (-not $windowsRoute.success) { Add-ProbeError -Errors $probeErrors -Name "windows-route" -Capture $windowsRoute }
if ($ubuntuAvailable -and -not $wslRoute.success) { Add-ProbeError -Errors $probeErrors -Name "wsl-route" -Capture $wslRoute }
if (-not $SkipNetworkProbes) {
    Add-ProbeError -Errors $probeErrors -Name "windows-trace" -Capture $windowsTrace
    if ($ubuntuAvailable) { Add-ProbeError -Errors $probeErrors -Name "wsl-trace" -Capture $wslTrace }
}

$localAccountId = Find-LineValue -Text $warpRegistration.text -Label "Account ID"
$localOrganization = Find-LineValue -Text $warpRegistration.text -Label "Organization"
$modeLine = Find-FirstLineValue -Text $warpSettings.text -Labels @(
    "(override)	Mode",
    "(network policy)	Mode",
    "(derived)	Mode",
    "Mode"
)
$allowModeSwitch = Find-FirstLineValue -Text $warpSettings.text -Labels @(
    "(override)	Allow Mode Switch",
    "(network policy)	Allow Mode Switch",
    "(derived)	Allow Mode Switch",
    "Allow Mode Switch"
)
$alwaysOn = Find-FirstLineValue -Text $warpSettings.text -Labels @(
    "(override)	Always On",
    "(network policy)	Always On",
    "(derived)	Always On",
    "Always On"
)
$includeModeDetected = [bool]($warpSettings.text -match "Include mode")
$excludeModeDetected = [bool]($warpSettings.text -match "Exclude mode")
$routingMode = $null
if ($includeModeDetected) {
    $routingMode = "include"
} elseif ($excludeModeDetected) {
    $routingMode = "exclude"
}

$baseline = [ordered]@{
    collectedAt = (Get-Date).ToString("o")
    computerName = $env:COMPUTERNAME
    accountIdHint = $AccountId
    tools = [ordered]@{
        warpCliAvailable = [bool]$warpPath
        wslAvailable = [bool]$wslPath
        cloudflaredAvailable = [bool]$cloudflaredPath
    }
    warp = [ordered]@{
        statusText = $warpStatus.text
        settingsText = $warpSettings.text
        registrationText = $warpRegistration.text
        tunnelDumpText = $warpTunnelDump.text
        summary = [ordered]@{
            organization = $localOrganization
            accountId = $localAccountId
            mode = $modeLine
            allowModeSwitch = $allowModeSwitch
            alwaysOn = $alwaysOn
            routingMode = $routingMode
            includeModeDetected = $includeModeDetected
            excludeModeDetected = $excludeModeDetected
            policyLocked = [bool]($allowModeSwitch -eq "false")
        }
    }
    windows = [ordered]@{
        routeText = $windowsRoute.text
    }
    wsl = [ordered]@{
        distrosText = $wslList.text
        ubuntuAvailable = $ubuntuAvailable
        routeText = $wslRoute.text
    }
    correlation = [ordered]@{
        localAccountId = $localAccountId
        localOrganization = $localOrganization
        accountIdHint = $AccountId
        accountIdMatches = [bool]($AccountId -and $localAccountId -and ($AccountId -eq $localAccountId))
    }
    networkProbes = [ordered]@{
        windowsTraceText = $windowsTrace.text
        windowsTrace = Convert-TraceText -Text $windowsTrace.text
        wslTraceText = $wslTrace.text
        wslTrace = Convert-TraceText -Text $wslTrace.text
        errors = @($probeErrors)
    }
}

$markdown = @(
    "# Cloudflare Zero Trust Baseline"
    ""
    "- Collected at: $($baseline.collectedAt)"
    "- Computer: $($baseline.computerName)"
    "- WARP org: $($baseline.correlation.localOrganization)"
    "- Local account ID: $($baseline.correlation.localAccountId)"
    "- Account hint: $($baseline.accountIdHint)"
    "- Account match: $($baseline.correlation.accountIdMatches)"
    "- WARP mode: $($baseline.warp.summary.mode)"
    "- Allow Mode Switch: $($baseline.warp.summary.allowModeSwitch)"
    "- Always On: $($baseline.warp.summary.alwaysOn)"
    "- Routing mode: $($baseline.warp.summary.routingMode)"
    "- Include mode detected: $($baseline.warp.summary.includeModeDetected)"
    "- Exclude mode detected: $($baseline.warp.summary.excludeModeDetected)"
    "- Policy locked: $($baseline.warp.summary.policyLocked)"
    "- Ubuntu available: $($baseline.wsl.ubuntuAvailable)"
    "- Windows trace warp: $($baseline.networkProbes.windowsTrace.warp)"
    "- Windows trace gateway: $($baseline.networkProbes.windowsTrace.gateway)"
    "- WSL trace warp: $($baseline.networkProbes.wslTrace.warp)"
    "- WSL trace gateway: $($baseline.networkProbes.wslTrace.gateway)"
    ""
    "## Notes"
    ""
    "- Baseline script is evidence collection only; it does not change policy."
)

if ($baseline.networkProbes.errors.Count -gt 0) {
    $markdown += ""
    $markdown += "## Probe Errors"
    $markdown += ""
    foreach ($errorText in $baseline.networkProbes.errors) {
        $markdown += "- $errorText"
    }
}

if (-not $baseline.wsl.ubuntuAvailable -and $baseline.wsl.distrosText) {
    $markdown += ""
    $markdown += "## WSL Notes"
    $markdown += ""
    $markdown += "- WSL probe did not find a usable Ubuntu distro in this session."
    $markdown += "- Raw WSL output: ``$($baseline.wsl.distrosText)``"
} elseif ($baseline.wsl.ubuntuAvailable -and -not $wslRoute.success -and $baseline.wsl.routeText) {
    $markdown += ""
    $markdown += "## WSL Notes"
    $markdown += ""
    $markdown += "- Ubuntu was detected but route collection failed."
    $markdown += "- Raw WSL route output: ``$($baseline.wsl.routeText)``"
}

$jsonText = $baseline | ConvertTo-Json -Depth 8
$markdownText = $markdown -join $newLine

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
