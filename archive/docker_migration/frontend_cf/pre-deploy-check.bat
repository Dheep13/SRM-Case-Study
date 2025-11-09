@echo off
echo ==========================================
echo  Pre-Deployment Verification
echo ==========================================
echo.

set ERROR_COUNT=0

echo [1/8] Checking required files...
if not exist "manifest.yml" (
    echo   ❌ manifest.yml missing!
    set /a ERROR_COUNT+=1
) else (
    echo   ✓ manifest.yml found
)

if not exist "package.json" (
    echo   ❌ package.json missing!
    set /a ERROR_COUNT+=1
) else (
    echo   ✓ package.json found
)

if not exist "server.js" (
    echo   ❌ server.js missing!
    set /a ERROR_COUNT+=1
) else (
    echo   ✓ server.js found
)

if not exist "vite.config.js" (
    echo   ❌ vite.config.js missing!
    set /a ERROR_COUNT+=1
) else (
    echo   ✓ vite.config.js found
)

echo.
echo [2/8] Checking CF CLI installation...
where cf >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo   ❌ Cloud Foundry CLI not installed!
    echo   Install from: https://github.com/cloudfoundry/cli
    set /a ERROR_COUNT+=1
) else (
    echo   ✓ CF CLI installed
)

echo.
echo [3/8] Checking CF login status...
cf target >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo   ⚠️  Not logged in to Cloud Foundry
    echo   Run: cf login
    set /a ERROR_COUNT+=1
) else (
    echo   ✓ Logged in to Cloud Foundry
    cf target
)

echo.
echo [4/8] Checking Node.js installation...
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo   ❌ Node.js not installed!
    set /a ERROR_COUNT+=1
) else (
    node --version
    echo   ✓ Node.js installed
)

echo.
echo [5/8] Checking npm installation...
where npm >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo   ❌ npm not installed!
    set /a ERROR_COUNT+=1
) else (
    npm --version
    echo   ✓ npm installed
)

echo.
echo [6/8] Checking manifest.yml configuration...
findstr /C:"your-api-domain" manifest.yml >nul
if %ERRORLEVEL% EQU 0 (
    echo   ⚠️  manifest.yml contains placeholder values
    echo   Update API_BASE_URL in manifest.yml
) else (
    echo   ✓ manifest.yml appears configured
)

findstr /C:"your-domain.com" manifest.yml >nul
if %ERRORLEVEL% EQU 0 (
    echo   ⚠️  manifest.yml contains placeholder route
    echo   Update routes in manifest.yml
) else (
    echo   ✓ Routes appear configured
)

echo.
echo [7/8] Testing build process...
echo   Running: npm install
call npm install >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo   ❌ npm install failed!
    set /a ERROR_COUNT+=1
) else (
    echo   ✓ npm install successful
)

echo   Running: npm run build
call npm run build >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo   ❌ npm run build failed!
    set /a ERROR_COUNT+=1
) else (
    echo   ✓ Build successful
)

echo.
echo [8/8] Checking build output...
if not exist "dist\index.html" (
    echo   ❌ dist/index.html not found!
    set /a ERROR_COUNT+=1
) else (
    echo   ✓ dist/index.html exists
)

echo.
echo ==========================================
if %ERROR_COUNT% EQU 0 (
    echo  ✅ ALL CHECKS PASSED!
    echo  Ready to deploy with: cf-deploy.bat
) else (
    echo  ❌ FOUND %ERROR_COUNT% ISSUE(S)
    echo  Please fix the issues above before deploying
)
echo ==========================================
echo.
pause



