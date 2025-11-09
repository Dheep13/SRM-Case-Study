# Docker Quick Start Guide

## Prerequisites
- Docker Desktop installed and running
- `.env` file configured (copy from `.env.example`)

## Architecture

Three separate services:
1. **Database** - PostgreSQL with pgvector (port 5432)
2. **Backend** - FastAPI with agents and APIs (port 8000)
3. **Frontend** - React app served by Nginx (port 3000)

## Deployment Options

### Option 1: Three Separate Services (Default)
Database, backend, and frontend run in separate containers.

**Start:**
```bash
# Windows
docker-start.bat

# Linux/Mac
chmod +x docker-start.sh
./docker-start.sh

# Or manually
docker-compose up -d
```

**Access:**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Database**: localhost:5432 (PostgreSQL)
- **Health Check**: http://localhost:8000/api/health

**Note**: Database initializes automatically on first start (may take 1-2 minutes).

### Option 2: Combined Service (Single Container)
Backend serves both API and frontend from one container.

**Start:**
```bash
docker-compose -f docker-compose.combined.yml up -d
```

**Access:**
- **Application**: http://localhost:8000 (serves both)
- **Health Check**: http://localhost:8000/api/health

## Common Commands

```bash
# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart services
docker-compose restart

# Rebuild after code changes
docker-compose up -d --build

# Check status
docker-compose ps

# Execute command in container
docker-compose exec backend python setup_chatbot.py
```

## Troubleshooting

**Services won't start?**
- Check if ports 3000 and 8000 are available
- Verify `.env` file exists and has required keys
- Check logs: `docker-compose logs`

**Frontend can't connect to backend?**
- Verify backend is running: `curl http://localhost:8000/api/health`
- Check CORS settings in `api.py`
- Rebuild frontend: `docker-compose up -d --build frontend`

**Need to update environment variables?**
- Edit `.env` file
- Restart services: `docker-compose restart`

For detailed documentation, see [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md)

