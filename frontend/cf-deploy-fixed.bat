@echo off
echo ==========================================
echo  EvolveIQ Frontend - CF Deployment
echo  (With Buildpack Fix)
echo ==========================================
echo.

REM Check if CF CLI is installed
where cf >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Cloud Foundry CLI not found!
    echo Please install from: https://github.com/cloudfoundry/cli#downloads
    pause
    exit /b 1
)

REM Check if logged in
cf target >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Not logged in to Cloud Foundry!
    echo Please run: cf login
    pause
    exit /b 1
)

echo [1/5] Cleaning up local artifacts...

REM Kill any Node processes that might lock files
taskkill /F /IM node.exe 2>nul
taskkill /F /IM npm.exe 2>nul
timeout /t 1 /nobreak >nul

if exist "node_modules" (
    echo   Removing node_modules/...
    rd /s /q node_modules 2>nul
    
    REM If still locked, try forced removal
    if exist "node_modules" (
        echo   ⚠️  Files locked, trying force removal...
        call force-cleanup.bat
    )
)

if exist "dist" (
    echo   Removing dist/...
    rd /s /q dist 2>nul
)

if exist "node_modules" (
    echo   ⚠️  WARNING: node_modules still exists!
    echo   This may cause deployment issues.
    echo   Options:
    echo   1. Close all editors/terminals and try again
    echo   2. Restart your computer
    echo   3. Continue anyway (may fail)
    set /p CONTINUE="Continue anyway? (y/n): "
    if /i not "%CONTINUE%"=="y" exit /b 1
) else (
    echo   ✓ Cleanup complete
)

echo.
echo [2/5] Verifying .cfignore...
findstr /C:"node_modules/" .cfignore >nul
if %ERRORLEVEL% NEQ 0 (
    echo   Adding node_modules/ to .cfignore...
    echo node_modules/ >> .cfignore
)
echo   ✓ .cfignore configured

echo.
echo [3/5] Verifying manifest.yml...
if not exist "manifest.yml" (
    echo   ERROR: manifest.yml not found!
    pause
    exit /b 1
)
echo   ✓ manifest.yml found

echo.
echo [4/5] Deploying to Cloud Foundry...
echo   This may take 3-5 minutes...
cf push evolveiq-frontend

if %ERRORLEVEL% NEQ 0 (
    echo   ERROR: Deployment failed!
    echo.
    echo   Troubleshooting:
    echo   1. Check logs: cf logs evolveiq-frontend --recent
    echo   2. Verify manifest.yml configuration
    echo   3. Check .cfignore excludes node_modules
    echo   4. See CF_TROUBLESHOOTING.md for more help
    pause
    exit /b 1
)

echo.
echo [5/5] Setting environment variables...
set /p SET_API="Set API_BASE_URL now? (y/n): "
if /i "%SET_API%"=="y" (
    set /p API_URL="Enter backend API URL (e.g., https://evolveiq-api.cfapps.io): "
    cf set-env evolveiq-frontend API_BASE_URL "%API_URL%/api"
    echo   Restaging app to apply changes...
    cf restage evolveiq-frontend
)

echo.
echo ==========================================
echo  Deployment Complete!
echo ==========================================
echo.
cf app evolveiq-frontend
echo.
echo Next steps:
echo 1. Test your app at the URL above
echo 2. Verify API connectivity
echo 3. Check all features work
echo.
pause

