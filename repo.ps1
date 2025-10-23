Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/InoshMatheesha/moody/refs/heads/main/index.html' -OutFile "$env:USERPROFILE\Downloads\test.html"; Start-Process "$env:USERPROFILE\Downloads\test.html"



