@echo off
echo ========================================
echo  GenAI Learning Assistant - DEV MODE
echo ========================================
echo.
echo Starting development servers...
echo.
echo [1/2] Starting FastAPI Backend...
start "FastAPI Backend" cmd /k "python api.py"
timeout /t 3 /nobreak > nul
echo.
echo [2/2] Starting React Frontend...
cd frontend
start "React Frontend" cmd /k "npm run dev"
echo.
echo ========================================
echo  SERVERS STARTED!
echo ========================================
echo.
echo Backend API: http://localhost:8000
echo Frontend UI: http://localhost:5173
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to stop all servers...
pause > nul
taskkill /FI "WINDOWTITLE eq FastAPI Backend*" /F
taskkill /FI "WINDOWTITLE eq React Frontend*" /F



