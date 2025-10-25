@echo off
setlocal enabledelayedexpansion

echo ============================================
echo   Verifying Environment Variables
echo ============================================
echo.

REM Check if logged in to CF
cf target >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Not logged in to Cloud Foundry!
    echo Please run: cf login -a https://api.cf.us10-001.hana.ondemand.com -o f8861a98trial
    echo.
    pause
    exit /b 1
)

echo Fetching environment variables from Cloud Foundry...
echo.

cf env genai-learning-assistant

echo.
echo ============================================
echo   Checking Required Variables
echo ============================================
echo.

REM Check for required variables
set "required_vars=OPENAI_API_KEY TAVILY_API_KEY SUPABASE_URL SUPABASE_KEY"

for %%v in (%required_vars%) do (
    cf env genai-learning-assistant | findstr "%%v" >nul
    if !errorlevel! equ 0 (
        echo [OK] %%v is set
    ) else (
        echo [MISSING] %%v is NOT set
    )
)

echo.
echo ============================================
echo.
echo To update variables, run: set_env_vars.bat
echo.
pause



