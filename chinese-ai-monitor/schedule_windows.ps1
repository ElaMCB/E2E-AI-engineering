# PowerShell script to schedule weekly Chinese AI monitor on Windows
# Run this script as Administrator

$scriptPath = Join-Path $PSScriptRoot "monitor.py"
$pythonPath = (Get-Command python).Source

if (-not (Test-Path $scriptPath)) {
    Write-Host "Error: monitor.py not found at $scriptPath" -ForegroundColor Red
    exit 1
}

Write-Host "Setting up scheduled task for Chinese AI Monitor..." -ForegroundColor Green
Write-Host "Script: $scriptPath" -ForegroundColor Yellow
Write-Host "Python: $pythonPath" -ForegroundColor Yellow

# Create the action
$action = New-ScheduledTaskAction `
    -Execute $pythonPath `
    -Argument "`"$scriptPath`"" `
    -WorkingDirectory $PSScriptRoot

# Create the trigger (every Monday at 9 AM)
$trigger = New-ScheduledTaskTrigger `
    -Weekly `
    -DaysOfWeek Monday `
    -At 9AM

# Create the principal (run as current user)
$principal = New-ScheduledTaskPrincipal `
    -UserId $env:USERNAME `
    -LogonType Interactive `
    -RunLevel Limited

# Create settings
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable

# Register the task
try {
    Register-ScheduledTask `
        -TaskName "ChineseAIMonitor" `
        -Action $action `
        -Trigger $trigger `
        -Principal $principal `
        -Settings $settings `
        -Description "Weekly monitoring of Chinese AI market developments" `
        -Force
    
    Write-Host "`nScheduled task created successfully!" -ForegroundColor Green
    Write-Host "Task will run every Monday at 9:00 AM" -ForegroundColor Cyan
    Write-Host "`nTo view the task: Get-ScheduledTask -TaskName ChineseAIMonitor" -ForegroundColor Yellow
    Write-Host "To remove the task: Unregister-ScheduledTask -TaskName ChineseAIMonitor -Confirm:`$false" -ForegroundColor Yellow
}
catch {
    Write-Host "Error creating scheduled task: $_" -ForegroundColor Red
    Write-Host "Make sure you're running PowerShell as Administrator" -ForegroundColor Yellow
}

