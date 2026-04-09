# EdTech Research Wiki — 주간 자동 수집 스케줄 등록
# PowerShell 관리자 권한으로 실행: .\schedule_setup.ps1

$TaskName   = "EdTechWikiCollect"
$ScriptPath = "D:\OneDrive\Documents\Obsidian Vault\03-Resources\edtech-research\scripts\collect_all.py"
$WorkDir    = "D:\OneDrive\Documents\Obsidian Vault\03-Resources\edtech-research"
$Python     = (Get-Command python).Source

# 매주 월요일 오전 7시 실행
$Trigger  = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At "07:00"
$Action   = New-ScheduledTaskAction `
    -Execute $Python `
    -Argument "`"$ScriptPath`"" `
    -WorkingDirectory $WorkDir
$Settings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Hours 1) `
    -RunOnlyIfNetworkAvailable `
    -StartWhenAvailable

Register-ScheduledTask `
    -TaskName $TaskName `
    -Trigger  $Trigger `
    -Action   $Action `
    -Settings $Settings `
    -RunLevel Limited `
    -Force

Write-Host "등록 완료: $TaskName (매주 월요일 07:00)"
Write-Host "확인: Get-ScheduledTask -TaskName '$TaskName'"
Write-Host "수동 실행: Start-ScheduledTask -TaskName '$TaskName'"
Write-Host "삭제: Unregister-ScheduledTask -TaskName '$TaskName' -Confirm:`$false"
