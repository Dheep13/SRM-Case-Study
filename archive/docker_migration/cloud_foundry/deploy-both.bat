@echo off
echo ========================================
echo Full Stack Deployment - Backend + Frontend
echo ========================================
echo.

echo [1/2] Deploying Backend with CORS fix...
echo.
cf push evolveiq-api
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Backend deployment failed!
    pause
    exit /b 1
)

echo.
echo ✅ Backend deployed successfully!
echo.
timeout /t 5 /nobreak >nul

echo [2/2] Deploying Frontend with API URL...
echo.
cd frontend
cf push evolveiq-frontend
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Frontend deployment failed!
    cd ..
    pause
    exit /b 1
)

cd ..

echo.
echo ========================================
echo ✅ DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo 🔗 Frontend: https://evolveiq-frontend.cfapps.us10-001.hana.ondemand.com
echo 🔗 Backend:  https://evolveiq-api.cfapps.us10-001.hana.ondemand.com
echo.
echo 🧪 To Test:
echo   1. Open the Frontend URL
echo   2. Press F12 (browser console)
echo   3. Look for: "🔧 API Configuration:"
echo   4. Should see backend URL, NOT localhost
echo   5. No CORS errors!
echo.
pause



