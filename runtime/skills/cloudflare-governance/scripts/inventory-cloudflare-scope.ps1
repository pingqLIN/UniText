param(
    [string]$ApiToken,
    [string]$GlobalApiKey,
    [string]$CloudflareEmail,
    [string]$AccountId,
    [string]$ZoneId,
    [string]$ZoneName,
    [int]$MaxItems = 20,
    [string]$JsonOutputPath,
    [string]$MarkdownOutputPath
)

$ErrorActionPreference = "Stop"

function Get-ScopedEnvValue {
    param([string[]]$Names)

    foreach ($name in $Names) {
        foreach ($scope in @("Process", "User", "Machine")) {
            $value = [Environment]::GetEnvironmentVariable($name, $scope)
            if ($value) {
                return @{
                    Name = $name
                    Scope = $scope
                    Value = $value
                }
            }
        }
    }

    return $null
}

function New-AuthHeaders {
    if ($script:ResolvedApiToken) {
        return @{ Authorization = "Bearer $($script:ResolvedApiToken.Trim())" }
    }

    if ($script:ResolvedGlobalApiKey -and $script:ResolvedCloudflareEmail) {
        return @{
            "X-Auth-Key" = $script:ResolvedGlobalApiKey.Trim()
            "X-Auth-Email" = $script:ResolvedCloudflareEmail.Trim()
        }
    }

    throw "No Cloudflare credential available."
}

function Invoke-CloudflareApi {
    param(
        [string]$Path,
        [hashtable]$Query = @{}
    )

    $queryPairs = @()
    foreach ($key in $Query.Keys) {
        if ($null -ne $Query[$key] -and "$($Query[$key])" -ne "") {
            $queryPairs += ("{0}={1}" -f [Uri]::EscapeDataString($key), [Uri]::EscapeDataString("$($Query[$key])"))
        }
    }

    $uri = "https://api.cloudflare.com/client/v4$Path"
    if ($queryPairs.Count -gt 0) {
        $uri = "{0}?{1}" -f $uri, ($queryPairs -join "&")
    }

    $headers = New-AuthHeaders
    $curlPath = (Get-Command curl.exe -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source -ErrorAction SilentlyContinue)
    if ($curlPath) {
        $arguments = @("-sS", "-D", "-", $uri)
        foreach ($key in $headers.Keys) {
            $arguments = @("-H", ("{0}: {1}" -f $key, $headers[$key])) + $arguments
        }

        $raw = & $curlPath @arguments 2>&1
        $text = (($raw | ForEach-Object { "$_" }) -join [Environment]::NewLine)
        if ($LASTEXITCODE -eq 0 -and $text -match "\r?\n\r?\n") {
            $parts = $text -split "\r?\n\r?\n", 2
            $body = $parts[1]
            return @{
                success = $true
                errors = @()
                result = ((($body | ConvertFrom-Json -Depth 12)).result)
                resultInfo = ((($body | ConvertFrom-Json -Depth 12)).result_info)
                messages = ((($body | ConvertFrom-Json -Depth 12)).messages)
            }
        }
    }

    $pythonPath = (Get-Command python -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source -ErrorAction SilentlyContinue)
    if ($pythonPath) {
        $env:CODEX_CF_URI = $uri
        $env:CODEX_CF_HEADERS_JSON = ($headers | ConvertTo-Json -Compress)
        $pythonSource = @'
import json
import os
from urllib.request import Request, urlopen
from urllib.error import HTTPError

uri = os.environ["CODEX_CF_URI"]
headers = json.loads(os.environ["CODEX_CF_HEADERS_JSON"])
req = Request(uri, headers=headers)

try:
    with urlopen(req, timeout=30) as resp:
        body = resp.read().decode("utf-8", "replace")
        print(json.dumps({"success": True, "body": body}))
except HTTPError as exc:
    body = exc.read().decode("utf-8", "replace")
    print(json.dumps({"success": False, "body": body}))
except Exception as exc:
    print(json.dumps({"success": False, "body": str(exc)}))
'@

        try {
            $pythonOutput = & $pythonPath -c $pythonSource 2>&1
            $pythonText = (($pythonOutput | ForEach-Object { "$_" }) -join [Environment]::NewLine).Trim()
            $pythonResult = $pythonText | ConvertFrom-Json -Depth 8
            if ($pythonResult.success) {
                $parsed = $pythonResult.body | ConvertFrom-Json -Depth 12
                return @{
                    success = $true
                    errors = @()
                    result = $parsed.result
                    resultInfo = $parsed.result_info
                    messages = $parsed.messages
                }
            }

            return @{
                success = $false
                errors = @($pythonResult.body)
                result = $null
                resultInfo = $null
                messages = @()
            }
        } catch {
            return @{
                success = $false
                errors = @($_.Exception.Message)
                result = $null
                resultInfo = $null
                messages = @()
            }
        } finally {
            Remove-Item Env:CODEX_CF_URI -ErrorAction SilentlyContinue
            Remove-Item Env:CODEX_CF_HEADERS_JSON -ErrorAction SilentlyContinue
        }
    }

    try {
        $response = Invoke-RestMethod -Method Get -Uri $uri -Headers $headers -TimeoutSec 30
        return @{
            success = $true
            errors = @()
            result = $response.result
            resultInfo = $response.result_info
            messages = $response.messages
        }
    } catch {
        $errorText = $_.Exception.Message
        if ($_.ErrorDetails.Message) {
            $errorText = $_.ErrorDetails.Message
        } elseif ($_.Exception.Response) {
            try {
                $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
                $body = $reader.ReadToEnd()
                if (-not [string]::IsNullOrWhiteSpace($body)) {
                    $errorText = $body
                }
            } catch {
            }
        }

        return @{
            success = $false
            errors = @($errorText)
            result = $null
            resultInfo = $null
            messages = @()
        }
    }
}

function Select-CompactFields {
    param(
        [object[]]$Items,
        [string[]]$Fields
    )

    if (-not $Items) {
        return @()
    }

    return @($Items | Select-Object -First $MaxItems -Property $Fields)
}

$tokenSource = "parameter"
$globalKeyProvided = -not [string]::IsNullOrWhiteSpace($GlobalApiKey)
$emailProvided = -not [string]::IsNullOrWhiteSpace($CloudflareEmail)
$apiTokenProvided = -not [string]::IsNullOrWhiteSpace($ApiToken)

$script:ResolvedApiToken = $ApiToken
$script:ResolvedGlobalApiKey = $GlobalApiKey
$script:ResolvedCloudflareEmail = $CloudflareEmail

if (-not $apiTokenProvided -and -not ($globalKeyProvided -and $emailProvided)) {
    $tokenEnv = Get-ScopedEnvValue @("CF_API_TOKEN", "CLOUDFLARE_API_TOKEN")
    if ($tokenEnv) {
        $script:ResolvedApiToken = $tokenEnv.Value
        $tokenSource = "$($tokenEnv.Name) [$($tokenEnv.Scope)]"
    }
}

if (-not $globalKeyProvided) {
    $keyEnv = Get-ScopedEnvValue @("CF_API_KEY", "CLOUDFLARE_API_KEY")
    if ($keyEnv) {
        $script:ResolvedGlobalApiKey = $keyEnv.Value
    }
}

if (-not $emailProvided) {
    $emailEnv = Get-ScopedEnvValue @("CLOUDFLARE_EMAIL", "CF_EMAIL")
    if ($emailEnv) {
        $script:ResolvedCloudflareEmail = $emailEnv.Value
    }
}

if (-not $script:ResolvedApiToken -and -not ($script:ResolvedGlobalApiKey -and $script:ResolvedCloudflareEmail)) {
    throw "Provide CF_API_TOKEN/CLOUDFLARE_API_TOKEN or CF_API_KEY/CLOUDFLARE_API_KEY plus CLOUDFLARE_EMAIL/CF_EMAIL."
}

$authMode = if ($script:ResolvedApiToken) { "api-token" } else { "global-api-key" }
$accountsResponse = Invoke-CloudflareApi -Path "/accounts" -Query @{ per_page = $MaxItems }
$zonesPath = "/zones"
$zonesQuery = @{ per_page = $MaxItems }

if ($AccountId) {
    $zonesQuery["account.id"] = $AccountId
}
if ($ZoneName) {
    $zonesQuery["name"] = $ZoneName
}

$zonesResponse = Invoke-CloudflareApi -Path $zonesPath -Query $zonesQuery

$resolvedAccountId = $AccountId
if (-not $resolvedAccountId -and $accountsResponse.success -and $accountsResponse.result.Count -eq 1) {
    $resolvedAccountId = $accountsResponse.result[0].id
}

$resolvedZoneId = $ZoneId
if (-not $resolvedZoneId -and $zonesResponse.success -and $zonesResponse.result.Count -eq 1) {
    $resolvedZoneId = $zonesResponse.result[0].id
}

$userResponse = Invoke-CloudflareApi -Path "/user"
$tunnelsResponse = if ($resolvedAccountId) {
    Invoke-CloudflareApi -Path "/accounts/$resolvedAccountId/cfd_tunnel" -Query @{ per_page = $MaxItems }
} else {
    @{ success = $false; errors = @("AccountId not provided or not uniquely resolved."); result = @(); resultInfo = $null; messages = @() }
}

$accessAppsResponse = if ($resolvedAccountId) {
    Invoke-CloudflareApi -Path "/accounts/$resolvedAccountId/access/apps" -Query @{ per_page = $MaxItems }
} else {
    @{ success = $false; errors = @("AccountId not provided or not uniquely resolved."); result = @(); resultInfo = $null; messages = @() }
}

$dnsResponse = if ($resolvedZoneId) {
    Invoke-CloudflareApi -Path "/zones/$resolvedZoneId/dns_records" -Query @{ per_page = $MaxItems }
} else {
    @{ success = $false; errors = @("ZoneId not provided or not uniquely resolved."); result = @(); resultInfo = $null; messages = @() }
}

$inventory = [ordered]@{
    collectedAt = (Get-Date).ToString("o")
    auth = [ordered]@{
        mode = $authMode
        tokenSource = if ($authMode -eq "api-token") { $tokenSource } else { $null }
        emailPresent = [bool]$script:ResolvedCloudflareEmail
    }
    selection = [ordered]@{
        requestedAccountId = $AccountId
        resolvedAccountId = $resolvedAccountId
        requestedZoneId = $ZoneId
        requestedZoneName = $ZoneName
        resolvedZoneId = $resolvedZoneId
    }
    user = [ordered]@{
        success = $userResponse.success
        errors = $userResponse.errors
        summary = if ($userResponse.success -and $userResponse.result) {
            [ordered]@{
                id = $userResponse.result.id
                email = $userResponse.result.email
                username = $userResponse.result.username
            }
        } else {
            $null
        }
    }
    accounts = [ordered]@{
        success = $accountsResponse.success
        errors = $accountsResponse.errors
        count = if ($accountsResponse.result) { @($accountsResponse.result).Count } else { 0 }
        items = if ($accountsResponse.success) {
            Select-CompactFields -Items $accountsResponse.result -Fields @("id", "name")
        } else {
            @()
        }
    }
    zones = [ordered]@{
        success = $zonesResponse.success
        errors = $zonesResponse.errors
        count = if ($zonesResponse.result) { @($zonesResponse.result).Count } else { 0 }
        items = if ($zonesResponse.success) {
            Select-CompactFields -Items $zonesResponse.result -Fields @("id", "name", "status", "type")
        } else {
            @()
        }
    }
    tunnels = [ordered]@{
        success = $tunnelsResponse.success
        errors = $tunnelsResponse.errors
        count = if ($tunnelsResponse.result) { @($tunnelsResponse.result).Count } else { 0 }
        items = if ($tunnelsResponse.success) {
            Select-CompactFields -Items $tunnelsResponse.result -Fields @("id", "name", "created_at", "deleted_at")
        } else {
            @()
        }
    }
    accessApps = [ordered]@{
        success = $accessAppsResponse.success
        errors = $accessAppsResponse.errors
        count = if ($accessAppsResponse.result) { @($accessAppsResponse.result).Count } else { 0 }
        items = if ($accessAppsResponse.success) {
            Select-CompactFields -Items $accessAppsResponse.result -Fields @("id", "name", "domain", "type")
        } else {
            @()
        }
    }
    dnsRecords = [ordered]@{
        success = $dnsResponse.success
        errors = $dnsResponse.errors
        count = if ($dnsResponse.result) { @($dnsResponse.result).Count } else { 0 }
        items = if ($dnsResponse.success) {
            Select-CompactFields -Items $dnsResponse.result -Fields @("id", "type", "name", "content", "proxied")
        } else {
            @()
        }
    }
}

$markdown = @(
    "# Cloudflare Scope Inventory",
    "",
    "- Collected at: $($inventory.collectedAt)",
    "- Auth mode: $($inventory.auth.mode)",
    "- Resolved account ID: $($inventory.selection.resolvedAccountId)",
    "- Resolved zone ID: $($inventory.selection.resolvedZoneId)",
    "- Accounts visible: $($inventory.accounts.count)",
    "- Zones visible: $($inventory.zones.count)",
    "- Tunnels visible: $($inventory.tunnels.count)",
    "- Access apps visible: $($inventory.accessApps.count)",
    "- DNS records visible: $($inventory.dnsRecords.count)",
    "",
    "## Notes",
    "",
    "- This script is read-only inventory.",
    "- Counts reflect visible resources for the active credential and selected scope."
)

$sections = @(
    @{ Name = "Accounts"; Key = "accounts" },
    @{ Name = "Zones"; Key = "zones" },
    @{ Name = "Tunnels"; Key = "tunnels" },
    @{ Name = "Access Apps"; Key = "accessApps" },
    @{ Name = "DNS Records"; Key = "dnsRecords" }
)

foreach ($section in $sections) {
    $data = $inventory[$section.Key]
    if ($data.success -and $data.items.Count -gt 0) {
        $markdown += ""
        $markdown += "## $($section.Name)"
        $markdown += ""
        foreach ($item in $data.items) {
            $pairs = @()
            foreach ($property in $item.PSObject.Properties) {
                $pairs += ("{0}: {1}" -f $property.Name, $property.Value)
            }
            $markdown += "- " + ($pairs -join " | ")
        }
    } elseif (-not $data.success) {
        $markdown += ""
        $markdown += "## $($section.Name) Errors"
        $markdown += ""
        foreach ($errorText in $data.errors) {
            $markdown += "- $errorText"
        }
    }
}

$jsonText = $inventory | ConvertTo-Json -Depth 8
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
