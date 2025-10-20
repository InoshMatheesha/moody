Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/InoshMatheesha/SecureShopCTF/refs/heads/main/docs/index.html' -OutFile "$env:USERPROFILE\Downloads\test.html"; Start-Process "$env:USERPROFILE\Downloads\test.html"


