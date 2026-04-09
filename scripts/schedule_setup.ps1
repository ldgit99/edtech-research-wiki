# EdTech Research Wiki — 주간 자동 수집+컴파일 스케줄 등록
# PowerShell 관리자 권한으로 실행: .\schedule_setup.ps1
#
# 필수 환경변수: ANTHROPIC_API_KEY
# 없으면 collect만 실행되고 compile은 건너뜀

$WorkDir     = "D:\OneDrive\Documents\Obsidian Vault\03-Resources\edtech-research"
$Python      = (Get-Command python).Source
$CollectScript = "$WorkDir\scripts\collect_all.py"
$CompileScript = "$WorkDir\scripts\auto_compile.py"

# ── 1. 수집 태스크 (매주 월 07:00) ──────────────────────────────
$T1Name = "EdTechWikiCollect"
$T1Trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At "07:00"
$T1Action  = New-ScheduledTaskAction `
    -Execute $Python `
    -Argument "`"$CollectScript`"" `
    -WorkingDirectory $WorkDir
$T1Settings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Hours 1) `
    -RunOnlyIfNetworkAvailable `
    -StartWhenAvailable

Register-ScheduledTask `
    -TaskName $T1Name -Trigger $T1Trigger `
    -Action $T1Action -Settings $T1Settings `
    -RunLevel Limited -Force | Out-Null

Write-Host "[OK] $T1Name 등록 (매주 월요일 07:00)"

# ── 2. 컴파일 태스크 (매주 월 07:30, 수집 완료 후) ──────────────
$T2Name = "EdTechWikiCompile"
$T2Trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At "07:30"
$T2Action  = New-ScheduledTaskAction `
    -Execute $Python `
    -Argument "`"$CompileScript`"" `
    -WorkingDirectory $WorkDir
$T2Settings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Hours 2) `
    -RunOnlyIfNetworkAvailable `
    -StartWhenAvailable

Register-ScheduledTask `
    -TaskName $T2Name -Trigger $T2Trigger `
    -Action $T2Action -Settings $T2Settings `
    -RunLevel Limited -Force | Out-Null

Write-Host "[OK] $T2Name 등록 (매주 월요일 07:30)"

# ── 안내 ────────────────────────────────────────────────────────
Write-Host ""
Write-Host "=== 등록 완료 ==="
Write-Host "필수: ANTHROPIC_API_KEY 환경변수 설정"
Write-Host "  [시스템 속성 → 환경변수 → 새로 만들기]"
Write-Host "  변수명: ANTHROPIC_API_KEY"
Write-Host "  값:     sk-ant-..."
Write-Host ""
Write-Host "수동 실행:"
Write-Host "  Start-ScheduledTask -TaskName 'EdTechWikiCollect'"
Write-Host "  Start-ScheduledTask -TaskName 'EdTechWikiCompile'"
Write-Host ""
Write-Host "삭제:"
Write-Host "  Unregister-ScheduledTask -TaskName 'EdTechWikiCollect' -Confirm:`$false"
Write-Host "  Unregister-ScheduledTask -TaskName 'EdTechWikiCompile' -Confirm:`$false"
