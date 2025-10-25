@echo off
setlocal enabledelayedexpansion

echo ============================================
echo   Setting Environment Variables in CF
echo ============================================

echo.
echo This script will read your .env file and set all variables in Cloud Foundry.
echo.

REM Check if .env file exists
if not exist .env (
    echo ERROR: .env file not found!
    echo Please create a .env file with your environment variables.
    echo You can copy .env.example and fill in your values.
    echo.
    pause
    exit /b 1
)

echo Found .env file. Reading variables...
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

echo Current CF Target:
cf target
echo.
echo ============================================
echo.

set count=0

REM Read .env file and set each variable
for /f "usebackq tokens=1,* delims==" %%a in (".env") do (
    set "line=%%a"
    set "value=%%b"
    
    REM Skip empty lines and comments
    if not "!line!"=="" (
        if not "!line:~0,1!"=="#" (
            REM Remove any quotes from the value
            set "value=!value:"=!"
            
            echo [Setting] %%a
            cf set-env genai-learning-assistant %%a "!value!"
            
            if !errorlevel! equ 0 (
                echo [OK] %%a set successfully
                set /a count+=1
            ) else (
                echo [ERROR] Failed to set %%a
            )
            echo.
        )
    )
)

echo.
echo ============================================
echo   Summary
echo ============================================
echo Successfully set %count% environment variables
echo.

echo.
echo ============================================
echo   Restarting application...
echo ============================================
echo This will apply the new environment variables...
echo.

cf restage genai-learning-assistant

if %errorlevel% equ 0 (
    echo.
    echo ============================================
    echo   SUCCESS!
    echo ============================================
    echo All environment variables have been set and applied.
    echo Your app is now running with the updated configuration.
    echo.
    echo App URL: https://genai-learning-assistant.cfapps.us10-001.hana.ondemand.com
) else (
    echo.
    echo ERROR: Restaging failed! Check the logs:
    echo cf logs genai-learning-assistant --recent
)

echo.
pause

