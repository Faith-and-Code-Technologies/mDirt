@echo off
setlocal enabledelayedexpansion

:: ================================
:: CONFIGURABLE VERSION NUMBER
:: ================================
set "VERSION=3.0.0-RC2"
set "ZIP_NAME=mDirt-%VERSION%.zip"
set "RELEASE_DIR=release"
set "MAIN_APP_DIR=dist\mDirt-%VERSION%"
set "UPDATER_EXE=dist\mDirtUpdater.exe"

echo ========================================
echo Building mDirt Application and Updater
echo Version: %VERSION%
echo ========================================

:: ========================================
:: BUILD MAIN APPLICATION
:: ========================================
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
  --hidden-import=jinja2 ^
  --hidden-import=jinja2.ext

if errorlevel 1 (
    echo ERROR: Main application build failed!
    pause
    exit /b 1
)

:: ========================================
:: BUILD UPDATER
:: ========================================
echo.
echo Building updater...
pyinstaller --onefile --windowed --name="mDirtUpdater" --icon="assets/icon.ico" src/updater.py

if errorlevel 1 (
    echo ERROR: Updater build failed!
    pause
    exit /b 1
)

:: ========================================
:: MOVE UPDATER INTO MAIN APP DIRECTORY
:: ========================================
echo.
echo Moving updater into main application folder...

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

move "%UPDATER_EXE%" "%MAIN_APP_DIR%\" >nul
if errorlevel 1 (
    echo ERROR: Failed to move updater!
    pause
    exit /b 1
)

:: ========================================
:: COPY VERSION FILE
:: ========================================
echo Copying version.json...
if exist "version.json" (
    copy "version.json" "%MAIN_APP_DIR%\" >nul
    if errorlevel 1 (
        echo WARNING: Failed to copy version.json
    ) else (
        echo version.json copied successfully
    )
) else (
    echo WARNING: version.json not found in root directory
)

:: ========================================
:: CREATE RELEASE DIRECTORY AND COPY APP
:: ========================================
echo.
echo Creating release directory...
if not exist "%RELEASE_DIR%" mkdir "%RELEASE_DIR%"

echo Copying application to release directory...
xcopy "%MAIN_APP_DIR%" "%RELEASE_DIR%\mDirt-%VERSION%\" /E /I /H /Y >nul
if errorlevel 1 (
    echo ERROR: Failed to copy application to release directory!
    pause
    exit /b 1
)

:: ========================================
:: CREATE ZIP ARCHIVE
:: ========================================
echo Creating ZIP archive...

powershell -NoLogo -NoProfile -Command ^
    "Try { Compress-Archive -Path '%RELEASE_DIR%\*' -DestinationPath '%ZIP_NAME%' -CompressionLevel Optimal -Force; exit 0 } Catch { Write-Error $_.Exception.Message; exit 1 }"

if errorlevel 1 (
    echo ERROR: PowerShell ZIP failed. Trying 7-Zip...
    where 7z >nul 2>nul
    if !errorlevel! equ 0 (
        7z a -tzip "%ZIP_NAME%" "%RELEASE_DIR%\*" >nul
        if errorlevel 1 (
            echo ERROR: 7-Zip also failed!
            goto :MANUAL_ZIP
        ) else (
            echo ZIP archive created successfully with 7-Zip: %ZIP_NAME%
        )
    ) else (
        goto :MANUAL_ZIP
    )
) else (
    echo ZIP archive created successfully: %ZIP_NAME%
)

:: ========================================
:: MOVE ZIP TO RELEASE AND CLEAN RELEASE
:: ========================================
echo.
echo Moving ZIP to release folder and cleaning extras...

move /Y "%ZIP_NAME%" "%RELEASE_DIR%\%ZIP_NAME%" >nul

:: Delete everything in release/ EXCEPT the ZIP file
for /f "delims=" %%F in ('dir /b /a-d "%RELEASE_DIR%"') do (
    if /i not "%%F"=="%ZIP_NAME%" del "%RELEASE_DIR%\%%F"
)

for /d %%D in ("%RELEASE_DIR%\*") do (
    rmdir /s /q "%%D"
)

goto :CLEANUP

:MANUAL_ZIP
echo.
echo ============================================
echo ZIP creation failed automatically.
echo Please manually zip the contents of:
echo '%RELEASE_DIR%' -> '%ZIP_NAME%'
echo ============================================

:CLEANUP
:: ========================================
:: FINAL CLEANUP (build/, dist/, *.spec)
:: ========================================
echo.
echo Cleaning up build artifacts...

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
for %%f in (*.spec) do del "%%f"

goto :SUCCESS

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
echo - Release ZIP: %RELEASE_DIR%\%ZIP_NAME%
echo.

set /p OPEN_FOLDER="Open release folder? (y/n): "
if /i "%OPEN_FOLDER%"=="y" (
    explorer "%RELEASE_DIR%"
)

echo.
echo Build process complete!
pause
