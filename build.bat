@echo off
setlocal enabledelayedexpansion

:: ========================================
:: VERSION CONFIGURATION - CHANGE THIS!
:: ========================================
set "VERSION=3.0.0-Pre2"

echo ========================================
echo Building mDirt Application and Updater
echo Version: %VERSION%
echo ========================================

:: Clean previous builds
echo Cleaning previous builds...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.spec del *.spec

:: Build the main application
echo.
echo Building main application...
pyinstaller src/main.py ^
  --name mDirt-%VERSION% ^
  --icon "assets/icon.ico" ^
  --onedir ^
  --windowed ^
  --add-data "lib;lib" ^
  --add-data "assets;assets" ^
  --add-data "src;src" ^
  --add-data "workspaces;workspaces" ^
  --hidden-import=jinja2 ^
  --hidden-import=jinja2.ext

if errorlevel 1 (
    echo ERROR: Main application build failed!
    pause
    exit /b 1
)

:: Build the updater
echo.
echo Building updater...
pyinstaller --onefile --windowed --name="mDirtUpdater" --icon="assets/icon.ico" src/updater.py

if errorlevel 1 (
    echo ERROR: Updater build failed!
    pause
    exit /b 1
)

:: Move updater into main application folder
echo.
echo Moving updater into main application folder...
set "MAIN_APP_DIR=dist\mDirt-%VERSION%"
set "UPDATER_EXE=dist\mDirtUpdater.exe"

if not exist "%MAIN_APP_DIR%" (
    echo ERROR: Main application directory not found!
    pause
    exit /b 1
)

if not exist "%UPDATER_EXE%" (
    echo ERROR: Updater executable not found!
    pause
    exit /b 1
)

move "%UPDATER_EXE%" "%MAIN_APP_DIR%\"
if errorlevel 1 (
    echo ERROR: Failed to move updater!
    pause
    exit /b 1
)

:: Copy version.json
echo Copying version.json...
if exist "version.json" (
    copy "version.json" "%MAIN_APP_DIR%\"
    if errorlevel 1 (
        echo WARNING: Failed to copy version.json
    ) else (
        echo version.json copied successfully
    )
) else (
    echo WARNING: version.json not found in root directory
)

:: Create release directory
echo.
echo Creating release package...
set "RELEASE_DIR=release"
if exist "%RELEASE_DIR%" rmdir /s /q "%RELEASE_DIR%"
mkdir "%RELEASE_DIR%"

:: Copy the complete application to release directory
echo Copying application to release directory...
xcopy "%MAIN_APP_DIR%" "%RELEASE_DIR%\mDirt-%VERSION%\" /E /I /H /Y
if errorlevel 1 (
    echo ERROR: Failed to copy application to release directory!
    pause
    exit /b 1
)

:: Create ZIP file using PowerShell (works on Windows 10+)
echo Creating ZIP archive...
set "ZIP_NAME=mDirt-%VERSION%.zip"
if exist "%ZIP_NAME%" del "%ZIP_NAME%"

powershell -command "Compress-Archive -Path '%RELEASE_DIR%\*' -DestinationPath '%ZIP_NAME%' -CompressionLevel Optimal"
if errorlevel 1 (
    echo ERROR: Failed to create ZIP archive!
    echo Trying alternative method...
    
    :: Alternative using 7-Zip if available
    where 7z >nul 2>nul
    if !errorlevel! equ 0 (
        echo Using 7-Zip...
        7z a "%ZIP_NAME%" "%RELEASE_DIR%\*"
        if errorlevel 1 (
            echo ERROR: 7-Zip also failed!
            goto :MANUAL_ZIP
        )
    ) else (
        goto :MANUAL_ZIP
    )
) else (
    echo ZIP archive created successfully: %ZIP_NAME%
)

goto :SUCCESS

:MANUAL_ZIP
echo.
echo ============================================
echo ZIP creation failed automatically.
echo Please manually zip the contents of the
echo '%RELEASE_DIR%' folder and name it '%ZIP_NAME%'
echo ============================================

:SUCCESS
echo.
echo ========================================
echo Build completed successfully!
echo ========================================
echo.
echo Files created:
echo - Main application: %MAIN_APP_DIR%
echo - Updater: %MAIN_APP_DIR%\mDirtUpdater.exe
echo - Version file: %MAIN_APP_DIR%\version.json
echo - Release package: %RELEASE_DIR%\mDirt-%VERSION%\
if exist "%ZIP_NAME%" echo - ZIP archive: %ZIP_NAME%
echo.

:: Optional: Open the release folder
set /p OPEN_FOLDER="Open release folder? (y/n): "
if /i "%OPEN_FOLDER%"=="y" (
    explorer "%RELEASE_DIR%"
)

echo.
echo Build process complete!
pause