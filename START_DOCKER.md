# How to Start Docker Services

## Quick Start (Easiest Method)

### Windows:
```powershell
.\docker-start.bat
```

### Linux/Mac:
```bash
chmod +x docker-start.sh
./docker-start.sh
```

This script will:
1. ✅ Check if `.env` file exists
2. ✅ Verify Docker is running
3. ✅ Build Docker images
4. ✅ Start all three services (database, backend, frontend)
5. ✅ Check health status

## Manual Start

### Step 1: Ensure `.env` file exists

If you don't have a `.env` file:
```powershell
# Windows
copy .env.docker.example .env

# Linux/Mac
cp .env.docker.example .env
```

Then edit `.env` and add your API keys:
- `OPENAI_API_KEY` (required)
- `TAVILY_API_KEY` (recommended)
- `GITHUB_TOKEN` (optional)

### Step 2: Start all services

```bash
docker-compose up -d
```

This starts:
- **Database** (PostgreSQL) on port 5432
- **Backend** (FastAPI) on port 8000
- **Frontend** (React) on port 3000

### Step 3: Verify services are running

```bash
docker-compose ps
```

You should see all three services with status "Up".

## Access Your Application

Once started:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Health Check**: http://localhost:8000/api/health
- **Database**: localhost:5432 (PostgreSQL)

## Useful Commands

### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f database
```

### Check status
```bash
docker-compose ps
```

### Stop services
```bash
docker-compose down
```

### Restart services
```bash
docker-compose restart
```

### Rebuild after code changes
```bash
docker-compose up -d --build
```

## Troubleshooting

### Services won't start?
1. Check if Docker Desktop is running
2. Verify ports 3000, 8000, 5432 are not in use
3. Check logs: `docker-compose logs`

### Database not initializing?
- First start may take 1-2 minutes
- Check database logs: `docker-compose logs database`
- Verify schema files exist in `db_integration/`

### Backend can't connect to database?
- Ensure database service is healthy: `docker-compose ps database`
- Check `.env` file has correct database settings
- Verify `USE_SUPABASE=false` for Docker PostgreSQL

### Frontend can't reach backend?
- Check backend is running: `curl http://localhost:8000/api/health`
- Verify CORS settings in `api.py`
- Check frontend logs: `docker-compose logs frontend`

