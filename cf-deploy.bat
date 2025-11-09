@echo off
REM Cloud Foundry Deployment Script for Windows

echo 🚀 Deploying EvolveIQ to Cloud Foundry...

REM Check if CF CLI is installed
where cf >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Cloud Foundry CLI not found. Install from: https://github.com/cloudfoundry/cli/releases
    exit /b 1
)

REM Check if logged in
cf target >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️  Not logged in to Cloud Foundry. Please run: cf login
    exit /b 1
)

echo ✓ Cloud Foundry CLI found and logged in

REM Get API URL (default)
set API_URL=https://evolveiq-api.cfapps.us10-001.hana.ondemand.com
set FRONTEND_URL=https://evolveiq-frontend.cfapps.us10-001.hana.ondemand.com

echo Using API URL: %API_URL%

REM Step 1: Build Frontend with API URL
echo.
echo 📦 Building frontend...
cd frontend
call npm install
set VITE_API_BASE_URL=%API_URL%
call npm run build

if not exist "dist" (
    echo ❌ Frontend build failed. dist/ directory not found.
    exit /b 1
)

echo ✓ Frontend built successfully

REM Step 2: Deploy Backend
echo.
echo 🚀 Deploying backend...
cd ..
cf push -f manifest-backend.yml

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Backend deployment failed
    exit /b 1
)

echo ✓ Backend deployed

REM Step 3: Set CORS for backend
echo.
echo 🔧 Setting CORS origins...
cf set-env evolveiq-api CORS_ORIGINS "https://evolveiq-frontend.cfapps.us10-001.hana.ondemand.com,https://www.evolveiq-frontend.cfapps.us10-001.hana.ondemand.com"

REM Step 4: Deploy Frontend
echo.
echo 🚀 Deploying frontend...
cd frontend
cf push -f manifest-frontend.yml

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Frontend deployment failed
    exit /b 1
)

echo ✓ Frontend deployed

REM Step 5: Restage backend to apply CORS changes
echo.
echo 🔄 Restaging backend to apply CORS changes...
cd ..
cf restage evolveiq-api

echo.
echo ✅ Deployment complete!
echo.
echo Frontend: %FRONTEND_URL%
echo Backend API: %API_URL%
echo.
echo ⚠️  Don't forget to set environment variables:
echo    cf set-env evolveiq-api OPENAI_API_KEY your_key
echo    cf set-env evolveiq-api SUPABASE_URL your_url
echo    cf set-env evolveiq-api SUPABASE_KEY your_key
echo    cf restage evolveiq-api

