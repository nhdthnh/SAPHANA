@echo off
cls
echo 🔄 Đang kích hoạt môi trường Conda...

REM Kích hoạt môi trường Conda (dành cho Windows)
call conda activate env_py37

echo ✅ Môi trường Conda đã được kích hoạt!
echo 🔄 Đang đóng gói file .exe với PyInstaller...

REM Chạy PyInstaller để build file .exe
pyinstaller --onefile --windowed --icon=icon.ico --name "SAPHANA TOOL" SAPHANA_GUI.py

echo ✅ Build thành công!
echo 🔄 Đang di chuyển file .exe về thư mục gốc...

REM Di chuyển file .exe ra thư mục gốc
move /Y dist\"SAPHANA TOOL.exe" .

echo 🔄 Đang xoá các thư mục tạm...

REM Xoá thư mục dist, build, và file .spec
rmdir /S /Q dist
rmdir /S /Q build
del /F /Q "SAPHANA TOOL.spec"

echo ✅ Quá trình hoàn tất! File "SAPHANA TOOL.exe" đã được tạo và di chuyển về thư mục gốc.
pause
