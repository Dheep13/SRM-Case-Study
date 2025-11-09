@echo off
echo ==========================================
echo  EvolveIQ Backend - CF Deployment
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

echo [1/3] Deploying Backend API...
cf push evolveiq-api

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Backend deployment failed!
    pause
    exit /b 1
)

echo.
echo [2/3] Setting environment variables...
echo Run set_cf_env.bat to configure environment variables
echo Or set them manually using:
echo   cf set-env evolveiq-api OPENAI_API_KEY your_key
echo   cf set-env evolveiq-api SUPABASE_URL your_url
echo   cf set-env evolveiq-api SUPABASE_KEY your_key
echo   cf set-env evolveiq-api TAVILY_API_KEY your_key
echo   cf restage evolveiq-api
echo.

set /p SET_ENV="Do you want to set environment variables now? (y/n): "
if /i "%SET_ENV%"=="y" (
    call set_cf_env.bat
    echo.
    echo [3/3] Restaging application...
    cf restage evolveiq-api
) else (
    echo [3/3] Skipping environment variable setup
    echo Remember to set environment variables before using the API!
)

echo.
echo ==========================================
echo  Backend Deployment Complete!
echo ==========================================
echo.
cf app evolveiq-api
echo.
pause



