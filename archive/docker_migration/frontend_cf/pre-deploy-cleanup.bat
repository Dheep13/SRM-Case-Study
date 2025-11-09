@echo off
echo ==========================================
echo  Frontend Pre-Deployment Cleanup
echo ==========================================
echo.
echo This script prepares the frontend for CF deployment
echo by removing local build artifacts and dependencies.
echo.

echo [1/3] Removing node_modules...
if exist "node_modules" (
    rmdir /s /q node_modules
    echo   ✓ node_modules removed
) else (
    echo   ✓ node_modules not found (already clean)
)

echo.
echo [2/3] Removing dist folder...
if exist "dist" (
    rmdir /s /q dist
    echo   ✓ dist removed
) else (
    echo   ✓ dist not found (already clean)
)

echo.
echo [3/3] Verifying .cfignore...
findstr /C:"node_modules/" .cfignore >nul
if %ERRORLEVEL% EQU 0 (
    echo   ✓ .cfignore configured correctly
) else (
    echo   ⚠️  Adding node_modules/ to .cfignore
    echo node_modules/ >> .cfignore
)

echo.
echo ==========================================
echo  Cleanup Complete!
echo ==========================================
echo.
echo Your frontend is ready for Cloud Foundry deployment.
echo.
echo Next steps:
echo   1. cd frontend
echo   2. cf push evolveiq-frontend
echo.
pause



