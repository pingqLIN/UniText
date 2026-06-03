param(
    [string]$ApiToken,
    [string]$GlobalApiKey,
    [string]$CloudflareEmail,
    [string]$AccountId,
    [string]$CloudflaredPath,
    [switch]$SkipTunnelList
)

$ErrorActionPreference = "Stop"

function Get-ScopedEnvValue {
    param([string[]]$Names)

    foreach ($name in $Names) {
        $processValue = [Environment]::GetEnvironmentVariable($name, "Process")
        if ($processValue) {
            return @{ Name = $name; Scope = "Process"; Value = $processValue }
        }

        $userValue = [Environment]::GetEnvironmentVariable($name, "User")
        if ($userValue) {
            return @{ Name = $name; Scope = "User"; Value = $userValue }
        }

        $machineValue = [Environment]::GetEnvironmentVariable($name, "Machine")
        if ($machineValue) {
            return @{ Name = $name; Scope = "Machine"; Value = $machineValue }
        }
    }

    return $null
}

function Write-CloudflareError {
    param([System.Exception]$Exception)

    if ($Exception.Response) {
        $reader = New-Object System.IO.StreamReader($Exception.Response.GetResponseStream())
        $body = $reader.ReadToEnd()
        Write-Host $body
        return
    }

    Write-Host $Exception.Message
}

function Invoke-CloudflareHttpJson {
    param(
        [string]$Uri,
        [hashtable]$Headers
    )

    $curlPath = (Get-Command curl.exe -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source -ErrorAction SilentlyContinue)
    if ($curlPath) {
        $arguments = @("-sS", "-D", "-", $Uri)
        foreach ($key in $Headers.Keys) {
            $arguments = @("-H", ("{0}: {1}" -f $key, $Headers[$key])) + $arguments
        }

        $raw = & $curlPath @arguments 2>&1
        $text = (($raw | ForEach-Object { "$_" }) -join [Environment]::NewLine)
        if ($LASTEXITCODE -eq 0 -and $text -match "\r?\n\r?\n") {
            $parts = $text -split "\r?\n\r?\n", 2
            $body = $parts[1]
            return @{
                success = $true
                body = $body
                parsed = ($body | ConvertFrom-Json -Depth 8)
                transport = "curl"
            }
        }
    }

    $pythonPath = (Get-Command python -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source -ErrorAction SilentlyContinue)
    if ($pythonPath) {
        $env:CODEX_CF_URI = $Uri
        $env:CODEX_CF_HEADERS_JSON = ($Headers | ConvertTo-Json -Compress)
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
                return @{
                    success = $true
                    body = $pythonResult.body
                    parsed = ($pythonResult.body | ConvertFrom-Json -Depth 8)
                    transport = "python-urllib"
                }
            }

            return @{
                success = $false
                body = $pythonResult.body
                parsed = $null
                transport = "python-urllib"
            }
        } catch {
            return @{
                success = $false
                body = $_.Exception.Message
                parsed = $null
                transport = "python-urllib"
            }
        } finally {
            Remove-Item Env:CODEX_CF_URI -ErrorAction SilentlyContinue
            Remove-Item Env:CODEX_CF_HEADERS_JSON -ErrorAction SilentlyContinue
        }
    }

    try {
        $response = Invoke-RestMethod -Method Get -Uri $Uri -Headers $Headers -TimeoutSec 20
        return @{
            success = $true
            body = ($response | ConvertTo-Json -Depth 8)
            parsed = $response
            transport = "Invoke-RestMethod"
        }
    } catch {
        $errorText = $_.Exception.Message
        if ($_.ErrorDetails.Message) {
            $errorText = $_.ErrorDetails.Message
        }

        return @{
            success = $false
            body = $errorText
            parsed = $null
            transport = "Invoke-RestMethod"
        }
    }
}

function Test-CloudflaredTunnelList {
    param([string]$Executable)

    $candidate = $Executable
    if (-not $candidate) {
        $command = Get-Command cloudflared.exe -ErrorAction SilentlyContinue
        if ($command) {
            $candidate = $command.Source
        }
    }

    if (-not $candidate) {
        return @{ success = $false; text = "cloudflared.exe not found" }
    }

    try {
        $output = & $candidate tunnel list 2>&1
        $text = (($output | ForEach-Object { "$_" }) -join [Environment]::NewLine).Trim()
        $looksUnauthorized = $text -match "unauthorized|authentication error|forbidden|permission denied|not logged in"
        return @{
            success = (-not $looksUnauthorized)
            text = $text
        }
    } catch {
        return @{
            success = $false
            text = $_.Exception.Message
        }
    }
}

$tokenSource = "parameter"
if (-not $ApiToken) {
    $tokenEnv = Get-ScopedEnvValue @("CF_API_TOKEN", "CLOUDFLARE_API_TOKEN")
    if ($tokenEnv) {
        $ApiToken = $tokenEnv.Value
        $tokenSource = "$($tokenEnv.Name) [$($tokenEnv.Scope)]"
    }
}

if (-not $GlobalApiKey) {
    $keyEnv = Get-ScopedEnvValue @("CF_API_KEY", "CLOUDFLARE_API_KEY")
    if ($keyEnv) {
        $GlobalApiKey = $keyEnv.Value
    }
}

if (-not $CloudflareEmail) {
    $emailEnv = Get-ScopedEnvValue @("CLOUDFLARE_EMAIL", "CF_EMAIL")
    if ($emailEnv) {
        $CloudflareEmail = $emailEnv.Value
    }
}

if ($ApiToken) {
    try {
        Write-Host "Auth mode: API token"
        Write-Host "Token source: $tokenSource"
        $tokenResponse = Invoke-CloudflareHttpJson -Uri "https://api.cloudflare.com/client/v4/user/tokens/verify" -Headers @{ Authorization = "Bearer $($ApiToken.Trim())" }
        if (-not $tokenResponse.success) {
            throw $tokenResponse.body
        }
        Write-Host "Token verification: SUCCESS"
        $capabilityClass = "account-auth"
        if ($tokenResponse.parsed.result) {
            Write-Host ("HTTP transport: " + $tokenResponse.transport)
            Write-Host ("Status: " + $tokenResponse.parsed.result.status)
            Write-Host ("Token ID: " + $tokenResponse.parsed.result.id)
            Write-Host ("Not before: " + $tokenResponse.parsed.result.not_before)
            Write-Host ("Expires on: " + $tokenResponse.parsed.result.expires_on)
        }

        if ($AccountId -and -not $SkipTunnelList) {
            $tunnelResponse = Invoke-CloudflareHttpJson -Uri "https://api.cloudflare.com/client/v4/accounts/$AccountId/cfd_tunnel" -Headers @{ Authorization = "Bearer $($ApiToken.Trim())" }
            if (-not $tunnelResponse.success) {
                throw $tunnelResponse.body
            }
            Write-Host "Tunnel API access: SUCCESS"
            Write-Host ("Tunnel count: " + $tunnelResponse.parsed.result.Count)
            $tunnelResponse.parsed.result | Select-Object -First 5 id, name, created_at | Format-Table -AutoSize
            $capabilityClass = "tunnel-api"
        }

        Write-Host ("Capability class: " + $capabilityClass)

        exit 0
    } catch {
        Write-Host "Token verification: FAILED"
        Write-CloudflareError $_.Exception
        exit 2
    }
}

if ($GlobalApiKey -and $CloudflareEmail) {
    try {
        Write-Host "Auth mode: Global API Key"
        $headers = @{
            "X-Auth-Key" = $GlobalApiKey.Trim()
            "X-Auth-Email" = $CloudflareEmail.Trim()
        }
        $userResponse = Invoke-CloudflareHttpJson -Uri "https://api.cloudflare.com/client/v4/user" -Headers $headers
        if (-not $userResponse.success) {
            throw $userResponse.body
        }
        Write-Host "Global API Key verification: SUCCESS"
        $capabilityClass = "account-auth"
        if ($userResponse.parsed.result) {
            Write-Host ("HTTP transport: " + $userResponse.transport)
            Write-Host ("User ID: " + $userResponse.parsed.result.id)
            Write-Host ("Email: " + $userResponse.parsed.result.email)
        }

        if ($AccountId -and -not $SkipTunnelList) {
            $tunnelResponse = Invoke-CloudflareHttpJson -Uri "https://api.cloudflare.com/client/v4/accounts/$AccountId/cfd_tunnel" -Headers $headers
            if (-not $tunnelResponse.success) {
                throw $tunnelResponse.body
            }
            Write-Host "Tunnel API access: SUCCESS"
            Write-Host ("Tunnel count: " + $tunnelResponse.parsed.result.Count)
            $tunnelResponse.parsed.result | Select-Object -First 5 id, name, created_at | Format-Table -AutoSize
            $capabilityClass = "tunnel-api"
        }

        Write-Host ("Capability class: " + $capabilityClass)

        exit 0
    } catch {
        Write-Host "Global API Key verification: FAILED"
        Write-CloudflareError $_.Exception
        exit 3
    }
}

$cloudflaredProbe = Test-CloudflaredTunnelList -Executable $CloudflaredPath
if ($cloudflaredProbe.success) {
    Write-Host "Auth mode: cloudflared cert"
    Write-Host "Tunnel list access via cloudflared: SUCCESS"
    Write-Host "Capability class: tunnel-cert-only"
    Write-Host $cloudflaredProbe.text
    exit 0
}

Write-Host "No Cloudflare API credential found."
Write-Host "Expected one of:"
Write-Host "- CF_API_TOKEN or CLOUDFLARE_API_TOKEN"
Write-Host "- CF_API_KEY or CLOUDFLARE_API_KEY plus CLOUDFLARE_EMAIL or CF_EMAIL"
Write-Host "- Or a valid cloudflared cert for tunnel-only operations"
if ($CloudflaredPath -or $cloudflaredProbe.text) {
    Write-Host ("cloudflared probe: " + $cloudflaredProbe.text)
}
exit 1
