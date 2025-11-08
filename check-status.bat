@echo off
echo ==========================================
echo  EvolveIQ - Check App Status
echo ==========================================
echo.

REM Check if CF CLI is installed
where cf >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Cloud Foundry CLI not found!
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

echo Current Target:
cf target
echo.

echo ==========================================
echo  All Apps
echo ==========================================
cf apps
echo.

echo ==========================================
echo  Backend API Details
echo ==========================================
cf app evolveiq-api 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️  Backend not deployed
)
echo.

echo ==========================================
echo  Frontend Details
echo ==========================================
cf app evolveiq-frontend 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️  Frontend not deployed
)
echo.

echo ==========================================
echo  Environment Variables
echo ==========================================
echo.
set /p CHECK_ENV="Check environment variables? (y/n): "
if /i "%CHECK_ENV%"=="y" (
    echo.
    echo === Backend Environment ===
    cf env evolveiq-api 2>nul
    echo.
    echo === Frontend Environment ===
    cf env evolveiq-frontend 2>nul
)

echo.
echo ==========================================
echo  Quick Health Check
echo ==========================================
echo.
set /p HEALTH_CHECK="Run health check? (y/n): "
if /i "%HEALTH_CHECK%"=="y" (
    echo.
    echo Checking Backend API health...
    for /f "tokens=2 delims=:" %%i in ('cf app evolveiq-api ^| findstr "routes:"') do (
        set BACKEND_URL=%%i
    )
    if defined BACKEND_URL (
        echo Testing: https://%BACKEND_URL%/api/health
        curl -s https://%BACKEND_URL%/api/health
        echo.
    ) else (
        echo Cannot determine backend URL
    )
    
    echo.
    echo Checking Frontend...
    for /f "tokens=2 delims=:" %%i in ('cf app evolveiq-frontend ^| findstr "routes:"') do (
        set FRONTEND_URL=%%i
    )
    if defined FRONTEND_URL (
        echo Frontend accessible at: https://%FRONTEND_URL%
    )
)

echo.
pause


