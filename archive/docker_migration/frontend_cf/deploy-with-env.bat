@echo off
echo ========================================
echo Deploying Frontend with API URL Baked In
echo ========================================

cd /d "%~dp0"

echo.
echo Current directory: %CD%
echo.
echo Configuration:
echo   Backend API: https://evolveiq-api.cfapps.us10-001.hana.ondemand.com
echo   This will be built into the frontend JavaScript
echo.

echo [1/2] Pushing to Cloud Foundry...
echo CF will run: npm install, then npm run build (which uses .env.production)
echo.
cf push evolveiq-frontend

echo.
echo [2/2] Deployment complete!
echo.
echo ✅ Frontend URL: https://evolveiq-frontend.cfapps.us10-001.hana.ondemand.com
echo.
echo 🔍 To verify:
echo   1. Open the frontend URL above
echo   2. Press F12 to open browser console
echo   3. Look for: "🔧 API Configuration:"
echo   4. It should show API_BASE_URL: https://evolveiq-api.cfapps.us10-001.hana.ondemand.com
echo.
pause



