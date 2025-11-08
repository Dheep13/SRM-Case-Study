@echo off
echo ========================================
echo Quick CF Deploy - Updated server.js
echo ========================================

cd /d "%~dp0"

echo.
echo [1/3] Setting API_BASE_URL environment variable...
cf set-env evolveiq-frontend API_BASE_URL "https://evolveiq-api.cfapps.us10-001.hana.ondemand.com"

echo.
echo [2/3] Pushing updated code to Cloud Foundry...
echo This will rebuild on CF...
cf push evolveiq-frontend

echo.
echo [3/3] Deployment complete!
echo.
echo Frontend URL: https://evolveiq-frontend.cfapps.us10-001.hana.ondemand.com
echo.
echo Check the browser console - you should see:
echo   "API_BASE_URL injected: https://evolveiq-api.cfapps.us10-001.hana.ondemand.com"
echo.
pause


