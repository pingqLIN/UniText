param(
    [string]$RepoRoot = (Get-Location).Path,
    [int]$TimeoutSeconds = 60,
    [int]$BarWidth = 28,
    [int]$RefreshMilliseconds = 125,
    [string]$StateRoot = ''
)

$null = $RepoRoot
$null = $TimeoutSeconds
$null = $BarWidth
$null = $RefreshMilliseconds
$null = $StateRoot

Write-Output 'continue'
