@echo off
echo ==========================================
echo  EvolveIQ - Check Cloud Foundry Logs
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

echo Which logs would you like to view?
echo.
echo 1. Backend API (evolveiq-api)
echo 2. Frontend (evolveiq-frontend)
echo 3. Both (sequential)
echo 4. Both (side-by-side in new windows)
echo 5. Live logs - Backend
echo 6. Live logs - Frontend
echo 7. Exit
echo.
set /p CHOICE="Enter choice (1-7): "

if "%CHOICE%"=="1" goto backend
if "%CHOICE%"=="2" goto frontend
if "%CHOICE%"=="3" goto both
if "%CHOICE%"=="4" goto sidebyside
if "%CHOICE%"=="5" goto live_backend
if "%CHOICE%"=="6" goto live_frontend
if "%CHOICE%"=="7" exit /b 0
echo Invalid choice!
pause
exit /b 1

:backend
echo.
echo ==========================================
echo  Backend API Logs (Recent)
echo ==========================================
echo.
cf logs evolveiq-api --recent
echo.
pause
exit /b 0

:frontend
echo.
echo ==========================================
echo  Frontend Logs (Recent)
echo ==========================================
echo.
cf logs evolveiq-frontend --recent
echo.
pause
exit /b 0

:both
echo.
echo ==========================================
echo  Backend API Logs
echo ==========================================
echo.
cf logs evolveiq-api --recent
echo.
echo.
echo ==========================================
echo  Frontend Logs
echo ==========================================
echo.
cf logs evolveiq-frontend --recent
echo.
pause
exit /b 0

:sidebyside
echo.
echo Opening logs in separate windows...
start "Backend API Logs" cmd /k "cf logs evolveiq-api --recent && echo. && echo Press any key to close... && pause>nul"
timeout /t 1 /nobreak >nul
start "Frontend Logs" cmd /k "cf logs evolveiq-frontend --recent && echo. && echo Press any key to close... && pause>nul"
echo.
echo Logs opened in new windows!
echo.
pause
exit /b 0

:live_backend
echo.
echo ==========================================
echo  Backend API - LIVE Logs
echo  (Press Ctrl+C to stop)
echo ==========================================
echo.
cf logs evolveiq-api
pause
exit /b 0

:live_frontend
echo.
echo ==========================================
echo  Frontend - LIVE Logs
echo  (Press Ctrl+C to stop)
echo ==========================================
echo.
cf logs evolveiq-frontend
pause
exit /b 0



