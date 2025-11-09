@echo off
echo ==========================================
echo  EvolveIQ - Live Monitoring
echo ==========================================
echo.
echo This will open live logs for both apps
echo in separate windows.
echo.
echo Press Ctrl+C in each window to stop monitoring
echo.
pause

echo Opening Backend API live logs...
start "Backend API - LIVE" cmd /k "echo ========================================== && echo   Backend API - LIVE Logs && echo   Press Ctrl+C to stop && echo ========================================== && echo. && cf logs evolveiq-api"

timeout /t 2 /nobreak >nul

echo Opening Frontend live logs...
start "Frontend - LIVE" cmd /k "echo ========================================== && echo   Frontend - LIVE Logs && echo   Press Ctrl+C to stop && echo ========================================== && echo. && cf logs evolveiq-frontend"

echo.
echo ==========================================
echo  Monitoring Started!
echo ==========================================
echo.
echo Two windows opened:
echo   1. Backend API - LIVE
echo   2. Frontend - LIVE
echo.
echo Press Ctrl+C in each window to stop
echo.
pause



