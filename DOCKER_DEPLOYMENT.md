# Docker Deployment Guide

This guide explains how to deploy the GenAI Learning Assistant application using Docker instead of Cloud Foundry.

## Prerequisites

- Docker Engine 20.10+ installed
- Docker Compose 2.0+ installed
- Environment variables configured (see `.env.example`)

## Quick Start

### Prerequisites
- Docker Desktop installed and running
- `.env` file configured (copy from `.env.docker.example`)

### Step 1: Configure Environment

Create a `.env` file in the root directory:
```bash
# Windows
copy .env.docker.example .env

# Linux/Mac
cp .env.docker.example .env
```

Edit `.env` and add your API keys:
- `OPENAI_API_KEY` (required)
- `TAVILY_API_KEY` (recommended)
- `GITHUB_TOKEN` (optional)

### Step 2: Start Services

**Windows:**
```powershell
docker-start.bat
```

**Linux/Mac:**
```bash
chmod +x docker-start.sh
./docker-start.sh
```

**Or manually:**
```bash
docker-compose up -d
```

### Step 3: Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Database**: localhost:5432 (PostgreSQL)
- **Health Check**: http://localhost:8000/api/health

**Note**: Database initializes automatically on first start (may take 1-2 minutes).

### Common Commands

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

## Architecture

The Docker setup consists of **three separate services**:

### 1. Database Service (`evolveiq-database`)
- **Image**: pgvector/pgvector:pg16 (PostgreSQL 16 with pgvector extension)
- **Port**: 5432
- **Features**:
  - PostgreSQL database with pgvector for vector embeddings
  - Automatic schema initialization on first start
  - Persistent data storage via Docker volumes
- **Alternative**: You can use external Supabase instead by setting `USE_SUPABASE=true`

### 2. Backend Service (`evolveiq-api`)
- **Image**: Python 3.11-slim based
- **Port**: 8000
- **Framework**: FastAPI with Uvicorn
- **Workers**: 2 (configurable)
- **Features**:
  - RESTful API endpoints
  - AI agents (content scraper, trend analyzer)
  - Agentic RAG chatbot
  - Database integration

### 3. Frontend Service (`evolveiq-frontend`)
- **Image**: Multi-stage build (Node.js builder + Nginx)
- **Port**: 3000 (mapped to container port 80)
- **Framework**: React with Vite
- **Server**: Nginx for serving static files

## Database Options

You have two options for the database:

### Option A: Docker PostgreSQL (Default)
The database runs in a Docker container with automatic initialization.

**Advantages:**
- Everything in one Docker setup
- No external dependencies
- Full control over database
- Easy to backup/restore

**Configuration:**
```env
USE_SUPABASE=false
DB_HOST=database
DB_NAME=evolveiq_db
DB_USER=evolveiq
DB_PASSWORD=evolveiq_password
```

### Option B: External Supabase
Use an external Supabase instance (cloud-hosted PostgreSQL).

**Advantages:**
- Managed service
- Built-in authentication
- Supabase dashboard
- Automatic backups

**Configuration:**
```env
USE_SUPABASE=true
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_key
```

## Architecture (Legacy - Combined Service)

You have two deployment options:

### Option 1: Separate Services (Default - Recommended for Production)

The Docker setup consists of two services:

#### Backend Service (`evolveiq-api`)
- **Image**: Python 3.11-slim based
- **Port**: 8000
- **Framework**: FastAPI with Uvicorn
- **Workers**: 2 (configurable)

#### Frontend Service (`evolveiq-frontend`)
- **Image**: Multi-stage build (Node.js builder + Nginx)
- **Port**: 3000 (mapped to container port 80)
- **Framework**: React with Vite
- **Server**: Nginx for serving static files

**Advantages:**
- Better for scaling (scale frontend/backend independently)
- Separation of concerns
- Can deploy to different servers
- Frontend can be served via CDN

### Option 2: Combined Service (Simpler - Single Container)

A single container that serves both frontend and backend:
- **Image**: Python 3.11-slim with built frontend
- **Port**: 8000
- **Framework**: FastAPI serves both API and static frontend files

**Advantages:**
- Simpler deployment (one container)
- Single port to expose
- Easier for small deployments
- Lower resource usage

**To use combined deployment:**
```bash
docker-compose -f docker-compose.combined.yml up -d
```

## Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
LLM_MODEL=gpt-4o-mini
LLM_TEMPERATURE=0.7

# Database Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your_supabase_anon_key_here

# API Keys for Agents
TAVILY_API_KEY=your_tavily_api_key_here
GITHUB_TOKEN=your_github_token_here

# Frontend API URL (optional - defaults to http://localhost:8000)
VITE_API_BASE_URL=http://localhost:8000
```

### Port Configuration

Default ports can be changed in `docker-compose.yml`:

```yaml
services:
  backend:
    ports:
      - "8000:8000"  # Change first number to change host port
  frontend:
    ports:
      - "3000:80"    # Change first number to change host port
```

## Docker Commands

### Build and Start
```bash
# Build and start in detached mode
docker-compose up -d

# Build and start with logs
docker-compose up

# Rebuild images
docker-compose build

# Rebuild and start
docker-compose up -d --build
```

### Stop and Remove
```bash
# Stop containers
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop, remove containers, and volumes
docker-compose down -v
```

### View Logs
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs backend
docker-compose logs frontend

# Follow logs
docker-compose logs -f
```

### Execute Commands
```bash
# Run command in backend container
docker-compose exec backend python setup_chatbot.py

# Access backend shell
docker-compose exec backend bash

# Access frontend shell
docker-compose exec frontend sh
```

### Health Checks
```bash
# Check service status
docker-compose ps

# Check health
curl http://localhost:8000/api/health
curl http://localhost:3000/health
```

## Production Deployment

### 1. Environment Configuration

For production, ensure:
- All API keys are set in `.env`
- `VITE_API_BASE_URL` points to your production backend URL
- Database credentials are secure

### 2. Build Production Images

```bash
# Build with no cache for clean build
docker-compose build --no-cache

# Tag for registry (optional)
docker tag evolveiq-api:latest your-registry/evolveiq-api:latest
docker tag evolveiq-frontend:latest your-registry/evolveiq-frontend:latest
```

### 3. Deploy to Production Server

```bash
# Copy files to server
scp -r . user@server:/path/to/app

# On server, start services
cd /path/to/app
docker-compose up -d
```

### 4. Using Docker Registry

If using a container registry (Docker Hub, AWS ECR, etc.):

```bash
# Push images
docker push your-registry/evolveiq-api:latest
docker push your-registry/evolveiq-frontend:latest

# On server, pull and run
docker-compose pull
docker-compose up -d
```

## Troubleshooting

### Backend Issues

**Problem**: Backend won't start
```bash
# Check logs
docker-compose logs backend

# Check if port is in use
netstat -an | grep 8000

# Restart service
docker-compose restart backend
```

**Problem**: Missing environment variables
```bash
# Verify .env file exists
cat .env

# Check environment in container
docker-compose exec backend env | grep OPENAI
```

### Frontend Issues

**Problem**: Frontend can't connect to backend
```bash
# Check VITE_API_BASE_URL
docker-compose exec frontend env | grep VITE

# Verify backend is running
docker-compose ps backend
curl http://localhost:8000/api/health
```

**Problem**: Frontend shows blank page
```bash
# Check nginx logs
docker-compose logs frontend

# Verify build output
docker-compose exec frontend ls -la /usr/share/nginx/html
```

### Database Connection Issues

**Problem**: Can't connect to Supabase
```bash
# Verify credentials
docker-compose exec backend env | grep SUPABASE

# Test connection
docker-compose exec backend python -c "from db_integration.supabase_client import SupabaseManager; db = SupabaseManager(); print('Connected')"
```

## Volume Management

The `docker-compose.yml` mounts volumes for:
- `./outputs` - Chart outputs and generated files
- `./static` - Static files served by backend

To persist data, you can add volume mounts:

```yaml
volumes:
  outputs-data:
  static-data:

services:
  backend:
    volumes:
      - outputs-data:/app/outputs
      - static-data:/app/static
```

## Scaling

To run multiple backend instances:

```bash
# Scale backend service
docker-compose up -d --scale backend=3

# Note: You'll need a load balancer (nginx, traefik) in front
```

## Security Considerations

1. **Never commit `.env` file** - It contains sensitive API keys
2. **Use secrets management** in production (Docker secrets, AWS Secrets Manager, etc.)
3. **Keep images updated** - Regularly rebuild with latest base images
4. **Use HTTPS** - Set up reverse proxy (nginx, traefik) with SSL certificates
5. **Limit network exposure** - Only expose necessary ports

## Migration from Cloud Foundry

If migrating from Cloud Foundry:

1. **Export environment variables** from CF:
   ```bash
   cf env evolveiq-api > cf-env.txt
   ```

2. **Create `.env` file** with the exported variables

3. **Update CORS settings** in `api.py` if needed for your new domain

4. **Remove Cloud Foundry files** (optional):
   - `manifest.yml`
   - `Procfile`
   - `runtime.txt`

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [React Deployment](https://react.dev/learn/start-a-new-react-project#production-builds)

## Support

For issues or questions:
1. Check logs: `docker-compose logs`
2. Verify environment: `docker-compose exec backend env`
3. Test health endpoints: `curl http://localhost:8000/api/health`

