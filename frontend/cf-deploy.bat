@echo off
echo ==========================================
echo  EvolveIQ - Cloud Foundry Deployment
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

echo [Step 1/4] Checking CF login status...
cf target >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Not logged in to Cloud Foundry!
    echo Please run: cf login
    pause
    exit /b 1
)

echo [Step 2/4] Installing dependencies...
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: npm install failed!
    pause
    exit /b 1
)

echo [Step 3/4] Building application...
call npm run build
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo [Step 4/4] Deploying to Cloud Foundry...
cf push
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Deployment failed!
    pause
    exit /b 1
)

echo.
echo ==========================================
echo  Deployment Complete!
echo ==========================================
echo.
echo View your app:
cf apps | findstr evolveiq
echo.
echo View logs:
echo   cf logs evolveiq-frontend --recent
echo.
echo Set API URL (if needed):
echo   cf set-env evolveiq-frontend API_BASE_URL https://your-api.cfapps.io/api
echo   cf restage evolveiq-frontend
echo.
pause


