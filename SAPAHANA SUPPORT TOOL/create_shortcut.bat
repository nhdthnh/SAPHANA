@echo off
set APP_NAME=SAPHANA TOOL
set APP_PATH="%~dp0SAPHANA TOOL.exe"
set DESKTOP_PATH=%USERPROFILE%\Desktop
set SHORTCUT_PATH="%DESKTOP_PATH%\%APP_NAME%.lnk"

:: Tạo shortcut trên Desktop bằng cách sử dụng Windows Shell
powershell -command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%SHORTCUT_PATH%'); $s.TargetPath = '%APP_PATH%'; $s.WorkingDirectory = '%~dp0'; $s.Save()"

echo Shortcut created successfully!
exit
