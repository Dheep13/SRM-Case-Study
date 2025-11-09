@echo off
echo ==========================================
echo  Force Cleanup - Windows
echo ==========================================
echo.
echo This script forces removal of locked files
echo using Windows commands.
echo.

echo [1/2] Killing any Node processes...
taskkill /F /IM node.exe 2>nul
taskkill /F /IM npm.exe 2>nul
timeout /t 2 /nobreak >nul

echo [2/2] Force removing node_modules and dist...
if exist "node_modules" (
    echo   Removing node_modules...
    rd /s /q node_modules 2>nul
    
    REM If still exists, try takeown
    if exist "node_modules" (
        echo   Using takeown for locked files...
        takeown /f node_modules /r /d y >nul 2>&1
        icacls node_modules /grant administrators:F /t >nul 2>&1
        rd /s /q node_modules 2>nul
    )
    
    if exist "node_modules" (
        echo   ⚠️  Some files still locked. Please:
        echo   1. Close all editors/terminals
        echo   2. Restart computer if needed
        echo   3. Manually delete node_modules folder
    ) else (
        echo   ✓ node_modules removed
    )
) else (
    echo   ✓ node_modules not found
)

if exist "dist" (
    echo   Removing dist...
    rd /s /q dist 2>nul
    if exist "dist" (
        takeown /f dist /r /d y >nul 2>&1
        icacls dist /grant administrators:F /t >nul 2>&1
        rd /s /q dist 2>nul
    )
    
    if not exist "dist" (
        echo   ✓ dist removed
    )
)

echo.
echo ==========================================
echo  Cleanup Complete!
echo ==========================================
echo.
pause



