@echo off
echo ============================================
echo   Deploying to SAP BTP Cloud Foundry
echo ============================================

echo.
echo [1/5] Checking CF CLI installation...
where cf >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Cloud Foundry CLI not found!
    echo Please install from: https://github.com/cloudfoundry/cli/releases
    pause
    exit /b 1
)

echo [OK] CF CLI found
echo.

echo [2/5] Building React frontend...
cd frontend
call npm run build
if %errorlevel% neq 0 (
    echo ERROR: Frontend build failed!
    cd ..
    pause
    exit /b 1
)
cd ..
echo [OK] Frontend built successfully
echo.

echo [3/5] Copying frontend build to static directory...
if exist "static" rmdir /s /q static
xcopy /E /I /Y frontend\dist static
echo [OK] Frontend copied
echo.

echo [4/5] Logging in to Cloud Foundry...
cf login -a https://api.cf.us10-001.hana.ondemand.com -o f8861a98trial
if %errorlevel% neq 0 (
    echo ERROR: Login failed!
    pause
    exit /b 1
)
echo [OK] Logged in
echo.

echo [5/5] Deploying application...
cf push
if %errorlevel% neq 0 (
    echo ERROR: Deployment failed!
    pause
    exit /b 1
)

echo.
echo ============================================
echo   Deployment Complete!
echo ============================================
echo.
echo Application URL: https://genai-learning-assistant.cfapps.us10-001.hana.ondemand.com
echo.

REM Ask if user wants to set environment variables
echo.
echo ============================================
echo.
set /p SET_ENV="Do you want to set environment variables from .env file now? (Y/N): "
if /i "%SET_ENV%"=="Y" (
    echo.
    echo Setting environment variables...
    call set_env_vars.bat
) else (
    echo.
    echo Skipping environment variable setup.
    echo You can run 'set_env_vars.bat' later to set them.
    echo.
    echo Useful commands:
    echo   View logs:    cf logs genai-learning-assistant --recent
    echo   Set env vars: set_env_vars.bat
    echo   Restart app:  cf restart genai-learning-assistant
)

echo.
pause

