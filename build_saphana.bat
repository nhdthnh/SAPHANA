@echo off
cls
echo Activating Conda environment...

REM Activate Conda environment (for Windows)
call conda activate env_py37

echo Conda environment has been activated!
echo Packaging .exe file with PyInstaller...

REM Run PyInstaller to build .exe file
pyinstaller --onefile --windowed --icon=icon.ico --name "SAPHANA TOOL" SAPHANA_GUI.py

echo Build successful!
echo Moving .exe file to the root directory...

REM Move .exe file to the root directory
move /Y dist\"SAPHANA TOOL.exe" .

echo Deleting temporary folders...

REM Delete dist, build folders, and .spec file
rmdir /S /Q dist
rmdir /S /Q build
del /F /Q "SAPHANA TOOL.spec"

REM Create folder "SAPHANA SUPPORT TOOL"
mkdir "SAPHANA SUPPORT TOOL"

REM Copy necessary files and folders into the new folder
copy "SAPHANA TOOL.exe" "SAPHANA SUPPORT TOOL\"
copy "icon.ico" "SAPHANA SUPPORT TOOL\"
xcopy "SQL QUERY" "SAPHANA SUPPORT TOOL\SQL QUERY" /E /I
xcopy "Configure" "SAPHANA SUPPORT TOOL\Configure" /E /I

REM Compress the folder into a rar file (ensure WinRAR is installed and in PATH)
"C:\Program Files\WinRAR\Rar.exe" a -r "SAPHANA_SUPPORT_TOOL.rar" "SAPHANA SUPPORT TOOL\*"

REM Delete the folder "SAPHANA SUPPORT TOOL"
rmdir /S /Q "SAPHANA SUPPORT TOOL"

echo Process completed! File "SAPHANA TOOL.exe" has been created and moved to the root directory.
exit
