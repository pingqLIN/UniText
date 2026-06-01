param(
  [ValidateSet('enable','disable')]
  [string]$Mode = 'enable',
  [string]$TaskName = 'AI-Runtime-Governance-DriftAudit',
  [string]$SharedRoot = 'C:\Dev\AI_UNIFIED'
)

$script = "C:\Dev\AI_UNIFIED\skills\ai-runtime-governance\scripts\audit-drift.ps1"
if ($Mode -eq 'disable') {
  if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Write-Output "task_removed=$TaskName"
  } else {
    Write-Output "task_not_found=$TaskName"
  }
  exit 0
}

$action = New-ScheduledTaskAction -Execute 'pwsh.exe' -Argument "-NoProfile -ExecutionPolicy Bypass -File \"$script\" -SharedRoot \"$SharedRoot\""
$trigger = New-ScheduledTaskTrigger -Daily -At 3:00am
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited

if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
  Set-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Principal $principal
  Write-Output "task_updated=$TaskName"
} else {
  Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Principal $principal | Out-Null
  Write-Output "task_created=$TaskName"
}
