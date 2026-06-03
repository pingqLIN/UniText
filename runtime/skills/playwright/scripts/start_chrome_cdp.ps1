param(
  [string]$Url = 'https://chatgpt.com',
  [int]$Port = 9222,
  [string]$UserDataDir = "$env:USERPROFILE\.codex\plugins\cache\openai-bundled\browser-use\0.1.0-alpha1\skills\browser\profile-01",
  [string]$ProfileDirectory = 'Default',
  [ValidateSet('Chrome', 'Edge')]
  [string]$Browser = 'Chrome'
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Get-CdpVersion {
  param([Parameter(Mandatory)][int]$Port)

  foreach ($endpoint in "http://127.0.0.1:$Port", "http://[::1]:$Port") {
    try {
      $version = Invoke-RestMethod -Uri "$endpoint/json/version" -TimeoutSec 2
      return [pscustomobject]@{
        Endpoint = $endpoint
        Version = $version
      }
    } catch {
      continue
    }
  }

  return $null
}

function Get-BrowserPath {
  param([Parameter(Mandatory)][string]$Browser)

  $candidates = if ($Browser -eq 'Chrome') {
    @(
      "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
      "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
      "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
    )
  } else {
    @(
      "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe",
      "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
      "$env:LOCALAPPDATA\Microsoft\Edge\Application\msedge.exe"
    )
  }

  foreach ($candidate in $candidates) {
    if (Test-Path -LiteralPath $candidate) {
      return $candidate
    }
  }

  throw "$Browser executable was not found."
}

function Get-ProfileSourceCandidates {
  @(
    "$env:USERPROFILE\.codex\plugins\cache\openai-bundled\browser-use\0.1.0-alpha1\skills\browser\profile-02",
    "$env:LOCALAPPDATA\Temp\falcon-headed-ubol-profile2",
    "Q:\BrowserProfiles\chrome-postinstall-closed-20260506-080159"
  )
}

function Restore-UserDataDir {
  param([Parameter(Mandatory)][string]$Target)

  if (Test-Path -LiteralPath $Target) {
    return 'existing'
  }

  foreach ($candidate in Get-ProfileSourceCandidates) {
    if (-not (Test-Path -LiteralPath $candidate)) {
      continue
    }

    $parent = Split-Path -Parent $Target
    New-Item -ItemType Directory -Force -Path $parent | Out-Null
    robocopy $candidate $Target /E /COPY:DAT /DCOPY:DAT /R:1 /W:1 /XJ | Out-Null
    if ($LASTEXITCODE -le 7) {
      return "restored-from:$candidate"
    }

    throw "Failed to restore Chrome profile from $candidate to $Target. robocopy exit code: $LASTEXITCODE"
  }

  New-Item -ItemType Directory -Force -Path $Target | Out-Null
  return 'created-empty-fallback'
}

$existing = Get-CdpVersion -Port $Port
if ($existing) {
  [pscustomobject]@{
    Status = 'already-running'
    Browser = $existing.Version.Browser
    WebSocketDebuggerUrl = $existing.Version.webSocketDebuggerUrl
    Endpoint = $existing.Endpoint
    UserDataDir = $UserDataDir
    ProfileDirectory = $ProfileDirectory
  } | Format-List -Force
  exit 0
}

$browserPath = Get-BrowserPath -Browser $Browser
$profileStatus = Restore-UserDataDir -Target $UserDataDir

$arguments = @(
  "--remote-debugging-port=$Port",
  "--user-data-dir=$UserDataDir",
  "--profile-directory=$ProfileDirectory",
  '--no-first-run',
  '--no-default-browser-check',
  $Url
)

Start-Process -FilePath $browserPath -ArgumentList $arguments

$started = $null
foreach ($attempt in 1..15) {
  Start-Sleep -Seconds 1
  $started = Get-CdpVersion -Port $Port
  if ($started) {
    break
  }
}

if (-not $started) {
  throw "Started $Browser, but CDP endpoint did not respond on 127.0.0.1 or ::1 port $Port."
}

[pscustomobject]@{
  Status = 'started'
  Browser = $started.Version.Browser
  WebSocketDebuggerUrl = $started.Version.webSocketDebuggerUrl
  Endpoint = $started.Endpoint
  UserDataDir = $UserDataDir
  ProfileStatus = $profileStatus
  ProfileDirectory = $ProfileDirectory
} | Format-List -Force
