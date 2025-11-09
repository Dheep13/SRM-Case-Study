@echo off
REM Docker startup script for GenAI Learning Assistant (Windows)

echo 🐳 Starting GenAI Learning Assistant with Docker...

REM Check if .env file exists
if not exist .env (
    echo ⚠️  Warning: .env file not found!
    echo 📝 Creating .env from .env.example...
    if exist .env.example (
        copy .env.example .env
        echo ✅ Created .env file. Please edit it with your API keys before continuing.
        pause
        exit /b 1
    ) else (
        echo ❌ .env.example not found. Please create .env file manually.
        pause
        exit /b 1
    )
)

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running. Please start Docker and try again.
    pause
    exit /b 1
)

REM Build and start services
echo 🔨 Building Docker images...
docker-compose build

echo 🚀 Starting services...
docker-compose up -d

echo ⏳ Waiting for services to start...
timeout /t 10 /nobreak >nul

REM Check backend health
echo 🏥 Checking backend health...
curl -f http://localhost:8000/api/health >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Backend health check failed. Check logs with: docker-compose logs backend
) else (
    echo ✅ Backend is healthy!
)

REM Check frontend
echo 🌐 Checking frontend...
curl -f http://localhost:3000 >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Frontend check failed. Check logs with: docker-compose logs frontend
) else (
    echo ✅ Frontend is accessible!
)

echo.
echo 🎉 Services started!
echo 📱 Frontend: http://localhost:3000
echo 🔌 Backend API: http://localhost:8000
echo 🏥 Health Check: http://localhost:8000/api/health
echo.
echo 📋 Useful commands:
echo   - View logs: docker-compose logs -f
echo   - Stop services: docker-compose down
echo   - Restart: docker-compose restart
echo   - View status: docker-compose ps
echo.
pause

