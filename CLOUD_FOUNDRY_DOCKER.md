# Cloud Foundry Deployment with Docker

## Can You Use Docker on Cloud Foundry?

**Short Answer:** It depends on your Cloud Foundry platform version.

### Two Approaches:

1. **Docker Images (Modern CF)** - If your CF platform supports it
2. **Buildpacks (Traditional CF)** - What you were using before

## Option 1: Deploy Docker Images to Cloud Foundry

### Requirements:
- Cloud Foundry with Docker support (CF v6.30+ or newer platforms)
- SAP BTP Cloud Foundry may or may not support Docker directly
- Check: `cf feature-flags` to see if `diego_docker` is enabled

### If Supported:

1. **Build Docker Images:**
```bash
# Build your images
docker build -t evolveiq-backend .
docker build -t evolveiq-frontend ./frontend

# Tag for Cloud Foundry registry (if available)
docker tag evolveiq-backend your-registry/evolveiq-backend
docker tag evolveiq-frontend your-registry/evolveiq-frontend
```

2. **Push to Cloud Foundry:**
```bash
# If CF supports Docker directly
cf push evolveiq-backend --docker-image your-registry/evolveiq-backend
cf push evolveiq-frontend --docker-image your-registry/evolveiq-frontend
```

**Note:** Most Cloud Foundry platforms (especially SAP BTP) don't support Docker images directly. They use buildpacks instead.

## Option 2: Deploy Docker Compose Services Separately (Recommended)

Since Cloud Foundry doesn't support `docker-compose.yml` directly, you need to deploy each service separately:

### A. Backend API (Python/FastAPI)

**Create `manifest.yml` for backend:**

```yaml
---
applications:
- name: evolveiq-api
  memory: 1G
  disk_quota: 2G
  instances: 1
  buildpacks:
    - python_buildpack
  stack: cflinuxfs4
  path: .
  command: uvicorn api:app --host 0.0.0.0 --port $PORT
  env:
    PYTHON_VERSION: 3.11
    USE_SUPABASE: false
    DB_HOST: your-postgres-service
    DB_PORT: 5432
    DB_NAME: evolveiq_db
    DB_USER: evolveiq
    DB_PASSWORD: ${DB_PASSWORD}
    CORS_ORIGINS: https://evolveiq-frontend.cfapps.us10-001.hana.ondemand.com
  routes:
    - route: evolveiq-api.cfapps.us10-001.hana.ondemand.com
  health-check-type: http
  health-check-http-endpoint: /api/health
  timeout: 180
```

**Deploy:**
```bash
cf push -f manifest.yml
```

### B. Frontend (React)

**Create `frontend/manifest.yml`:**

```yaml
---
applications:
- name: evolveiq-frontend
  memory: 256M
  disk_quota: 512M
  instances: 1
  buildpacks:
    - staticfile_buildpack
  stack: cflinuxfs4
  path: dist
  routes:
    - route: evolveiq-frontend.cfapps.us10-001.hana.ondemand.com
  env:
    FORCE_HTTPS: true
```

**Build and Deploy:**
```bash
cd frontend
npm install
npm run build
# Update VITE_API_BASE_URL in build
cf push -f manifest.yml
```

### C. Database (PostgreSQL)

**Option 1: Use Cloud Foundry PostgreSQL Service:**
```bash
# Create PostgreSQL service
cf create-service postgresql-db standard evolveiq-db

# Bind to backend
cf bind-service evolveiq-api evolveiq-db
cf restage evolveiq-api
```

**Option 2: Use Supabase (External):**
- Set `USE_SUPABASE=true` in backend environment
- Provide `SUPABASE_URL` and `SUPABASE_KEY`

## Option 3: Hybrid Approach (Best for Cloud Foundry)

Deploy services separately but keep Docker for local development:

### Local Development:
```bash
docker compose up -d  # Use Docker locally
```

### Cloud Foundry Deployment:
```bash
# Deploy backend
cf push -f manifest-backend.yml

# Deploy frontend  
cd frontend && cf push -f manifest-frontend.yml

# Setup database service
cf create-service postgresql-db standard evolveiq-db
cf bind-service evolveiq-api evolveiq-db
```

## Key Differences: Docker vs Cloud Foundry

| Aspect | Docker | Cloud Foundry |
|--------|--------|---------------|
| **Deployment Unit** | Container images | Buildpacks + source code |
| **Orchestration** | docker-compose.yml | manifest.yml per app |
| **Database** | Docker container | Managed service or external |
| **Networking** | Docker network | CF internal networking |
| **Scaling** | Manual or orchestration | `cf scale` command |
| **Configuration** | .env files | Environment variables via CF |

## Migration Steps: Docker → Cloud Foundry

### 1. Create Cloud Foundry Manifests

**Backend `manifest-backend.yml`:**
```yaml
---
applications:
- name: evolveiq-api
  memory: 1G
  disk_quota: 2G
  buildpacks:
    - python_buildpack
  stack: cflinuxfs4
  path: .
  command: uvicorn api:app --host 0.0.0.0 --port $PORT
  env:
    PYTHON_VERSION: 3.11
    USE_SUPABASE: ${USE_SUPABASE:-true}
    CORS_ORIGINS: ${CORS_ORIGINS}
  routes:
    - route: evolveiq-api.cfapps.us10-001.hana.ondemand.com
```

**Frontend `frontend/manifest-frontend.yml`:**
```yaml
---
applications:
- name: evolveiq-frontend
  memory: 256M
  buildpacks:
    - staticfile_buildpack
  path: dist
  routes:
    - route: evolveiq-frontend.cfapps.us10-001.hana.ondemand.com
```

### 2. Update Frontend Build

The frontend needs the API URL baked into the build:

**Option A: Build with environment variable:**
```bash
cd frontend
VITE_API_BASE_URL=https://evolveiq-api.cfapps.us10-001.hana.ondemand.com npm run build
```

**Option B: Use runtime configuration (server.js):**
Keep the `server.js` approach from your archived CF setup to inject API URL at runtime.

### 3. Setup Database

**For Cloud Foundry PostgreSQL:**
```bash
# Create service
cf create-service postgresql-db standard evolveiq-db

# Get connection details
cf env evolveiq-api | grep DATABASE_URL

# Update backend env vars
cf set-env evolveiq-api DB_HOST <host>
cf set-env evolveiq-api DB_PORT 5432
cf set-env evolveiq-api DB_NAME <database>
cf set-env evolveiq-api DB_USER <user>
cf set-env evolveiq-api DB_PASSWORD <password>
```

**Or use Supabase (easier):**
```bash
cf set-env evolveiq-api USE_SUPABASE true
cf set-env evolveiq-api SUPABASE_URL https://your-project.supabase.co
cf set-env evolveiq-api SUPABASE_KEY your_key
```

### 4. Deploy

```bash
# Backend
cf push -f manifest-backend.yml

# Frontend
cd frontend
npm run build
cf push -f manifest-frontend.yml
```

## Recommended Approach for Your Setup

Since you have:
- ✅ Docker setup working locally
- ✅ Cloud Foundry access (SAP BTP)
- ✅ Authentication system

**Best Strategy:**

1. **Keep Docker for local development** - Use `docker compose up`
2. **Deploy to Cloud Foundry separately** - Use manifests for each service
3. **Use Supabase for database** - Easier than CF PostgreSQL service
4. **Build frontend with API URL** - Set `VITE_API_BASE_URL` during build

## Quick Cloud Foundry Deployment

### Step 1: Create Manifests

I can create the manifest files for you based on your current setup.

### Step 2: Build Frontend

```bash
cd frontend
VITE_API_BASE_URL=https://evolveiq-api.cfapps.us10-001.hana.ondemand.com npm run build
```

### Step 3: Deploy

```bash
# Backend
cf push -f manifest-backend.yml

# Frontend  
cd frontend && cf push -f manifest-frontend.yml
```

### Step 4: Set Environment Variables

```bash
cf set-env evolveiq-api OPENAI_API_KEY your_key
cf set-env evolveiq-api CORS_ORIGINS https://evolveiq-frontend.cfapps.us10-001.hana.ondemand.com
cf restage evolveiq-api
```

## Summary

**Can you use the same Docker setup?**
- ❌ Not directly - Cloud Foundry doesn't run `docker-compose.yml`
- ✅ But you can deploy the same code using Cloud Foundry buildpacks
- ✅ Keep Docker for local dev, use CF manifests for deployment

**Should you use Cloud Foundry or Docker platforms?**
- **Cloud Foundry**: If you already have access (SAP BTP), familiar with CF
- **Docker platforms** (Railway, Render): Easier, more modern, better Docker support

Would you like me to create the Cloud Foundry manifest files for your current setup?

