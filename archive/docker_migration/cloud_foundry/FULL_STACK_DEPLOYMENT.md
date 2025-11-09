# EvolveIQ Full Stack - Cloud Foundry Deployment

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Cloud Foundry                            │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────┐         ┌──────────────────┐          │
│  │   Frontend       │         │   Backend API    │          │
│  │   (React/Node)   │────────▶│   (Python/       │          │
│  │                  │         │    FastAPI)      │          │
│  │ evolveiq-        │         │ evolveiq-api     │          │
│  │ frontend         │         │                  │          │
│  └──────────────────┘         └────────┬─────────┘          │
│                                        │                     │
│                                        │                     │
│                                        ▼                     │
└────────────────────────────────────────────────────────────-┘
                                         │
                                         │
                                         ▼
                              ┌──────────────────┐
                              │   Supabase       │
                              │   (PostgreSQL +  │
                              │    Vector DB)    │
                              └──────────────────┘
                                         │
                                         ▼
                              ┌──────────────────┐
                              │  External APIs   │
                              │  - OpenAI        │
                              │  - Tavily        │
                              │  - GitHub        │
                              └──────────────────┘
```

## 📦 Components to Deploy

### 1. Backend API (evolveiq-api)
- **Language**: Python 3.11
- **Framework**: FastAPI + Uvicorn
- **Memory**: 1GB
- **Features**:
  - RESTful API endpoints
  - AI agents (content scraper, trend analyzer)
  - Agentic RAG chatbot
  - Database integration
  - Admin configuration system

### 2. Frontend (evolveiq-frontend)
- **Framework**: React 18 + Vite
- **Server**: Express (Node.js)
- **Memory**: 512MB
- **Features**:
  - Interactive UI
  - Real-time chat
  - Analytics dashboard
  - Expert consultation
  - Teacher tools

### 3. Database (Supabase)
- **Type**: PostgreSQL with pgvector
- **Hosting**: External (Supabase Cloud)
- **Features**:
  - Vector embeddings for RAG
  - Skill and resource storage
  - Trend tracking
  - Admin configuration

## 🚀 Quick Deploy (Full Stack)

### Prerequisites
- Cloud Foundry CLI installed
- CF account with sufficient quota
- Supabase project created
- API keys ready (OpenAI, Tavily)

### One-Command Deploy

```bash
.\deploy-full-stack.bat
```

This will:
1. Deploy backend API
2. Set environment variables
3. Deploy frontend
4. Link frontend to backend
5. Verify deployments

## 📋 Step-by-Step Deployment

### Step 1: Setup Supabase

1. Create Supabase project: https://supabase.com/dashboard
2. Run SQL scripts:
   ```sql
   -- In Supabase SQL Editor:
   -- 1. Run: db_integration/schema.sql
   -- 2. Run: db_integration/vector_embeddings.sql
   -- 3. Run: db_integration/admin_schema.sql
   ```
3. Note your:
   - Project URL: `https://xxx.supabase.co`
   - Anon Key: `eyJxxx...`

### Step 2: Prepare API Keys

Collect these keys:
- **OpenAI API Key**: https://platform.openai.com/api-keys
- **Tavily API Key**: https://tavily.com/
- **GitHub Token**: https://github.com/settings/tokens (optional)
- **Supabase URL & Key**: From Step 1

### Step 3: Update Configuration Files

#### Backend (`manifest.yml`)
```yaml
applications:
- name: evolveiq-api
  memory: 1G
  # Uncomment and set your route:
  # routes:
  #   - route: evolveiq-api.cfapps.io
```

#### Frontend (`frontend/manifest.yml`)
```yaml
applications:
- name: evolveiq-frontend
  memory: 512MB
  env:
    # Will be set automatically during deployment
    # API_BASE_URL: https://evolveiq-api.cfapps.io/api
  # Uncomment and set your route:
  # routes:
  #   - route: evolveiq-frontend.cfapps.io
```

### Step 4: Login to Cloud Foundry

```bash
cf login -a https://api.your-cf-domain.com
```

### Step 5: Deploy Backend

```bash
# Deploy backend API
.\deploy-backend.bat

# Or manually:
cf push evolveiq-api

# Set environment variables
.\set_cf_env.bat

# Restage to apply environment variables
cf restage evolveiq-api
```

### Step 6: Deploy Frontend

```bash
cd frontend

# Get backend URL
cf app evolveiq-api

# Set API URL in frontend
cf set-env evolveiq-frontend API_BASE_URL https://evolveiq-api.cfapps.io/api

# Deploy frontend
cf push evolveiq-frontend

cd ..
```

### Step 7: Verify Deployment

```bash
# Check both apps are running
cf apps

# Test backend health
curl https://evolveiq-api.cfapps.io/api/health

# Test frontend
# Open https://evolveiq-frontend.cfapps.io in browser
```

## 🔐 Environment Variables

### Backend (evolveiq-api)

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | ✅ | OpenAI API key for LLM |
| `SUPABASE_URL` | ✅ | Supabase project URL |
| `SUPABASE_KEY` | ✅ | Supabase anon key |
| `TAVILY_API_KEY` | ✅ | Tavily search API key |
| `LLM_MODEL` | ⚙️ | Model name (default: gpt-4o-mini) |
| `LLM_TEMPERATURE` | ⚙️ | Temperature (default: 0.7) |
| `GITHUB_TOKEN` | ⚪ | GitHub API token (optional) |

Set them using:
```bash
cf set-env evolveiq-api OPENAI_API_KEY "your-key"
cf set-env evolveiq-api SUPABASE_URL "https://xxx.supabase.co"
cf set-env evolveiq-api SUPABASE_KEY "your-key"
cf set-env evolveiq-api TAVILY_API_KEY "your-key"
cf restage evolveiq-api
```

### Frontend (evolveiq-frontend)

| Variable | Required | Description |
|----------|----------|-------------|
| `API_BASE_URL` | ✅ | Backend API URL |

Set it using:
```bash
cf set-env evolveiq-frontend API_BASE_URL "https://evolveiq-api.cfapps.io/api"
cf restage evolveiq-frontend
```

## 🎯 Post-Deployment Configuration

### 1. Initialize Database Data

```bash
# SSH into backend app
cf ssh evolveiq-api

# Run data loader
python load_and_visualize.py "GenAI skills for IT students"

# Generate embeddings
python setup_chatbot.py

# Exit SSH
exit
```

### 2. Configure Admin Settings

1. Open frontend: https://evolveiq-frontend.cfapps.io
2. Click "Admin" button (top right)
3. Click settings icon (⚙️)
4. Configure:
   - AI Model settings
   - Agent behavior
   - Platform access controls
   - Trending thresholds

### 3. Test Features

- ✅ Chat with Agentic RAG
- ✅ Discover resources
- ✅ View analytics
- ✅ Expert consultation booking
- ✅ Create assignments
- ✅ Today's class content

## 📊 Monitoring

### View Logs

```bash
# Backend logs
cf logs evolveiq-api --recent

# Frontend logs
cf logs evolveiq-frontend --recent

# Live logs
cf logs evolveiq-api  # Keep terminal open
```

### Check Health

```bash
# Backend health
cf app evolveiq-api
curl https://evolveiq-api.cfapps.io/api/health

# Frontend health
cf app evolveiq-frontend
```

### View Metrics

```bash
# CF Dashboard
cf app evolveiq-api

# Or use CF web interface
```

## 🔧 Scaling

### Scale Backend

```bash
# Increase instances
cf scale evolveiq-api -i 2

# Increase memory
cf scale evolveiq-api -m 2G

# Both
cf scale evolveiq-api -i 2 -m 2G
```

### Scale Frontend

```bash
cf scale evolveiq-frontend -i 2
```

## 🐛 Troubleshooting

### Backend Issues

**App won't start**:
```bash
cf logs evolveiq-api --recent

# Check environment variables
cf env evolveiq-api

# Common fixes:
# - Set missing environment variables
# - Increase memory if OOM errors
# - Check requirements.txt dependencies
```

**Database connection fails**:
```bash
# Verify Supabase credentials
cf env evolveiq-api | findstr SUPABASE

# Test Supabase connection
cf ssh evolveiq-api
python -c "from db_integration.supabase_client import SupabaseManager; db = SupabaseManager(); print('Connected!')"
```

**API errors**:
```bash
# Check API documentation
# Open: https://evolveiq-api.cfapps.io/docs

# View recent errors
cf logs evolveiq-api --recent
```

### Frontend Issues

**API calls failing**:
```bash
# Check API_BASE_URL
cf env evolveiq-frontend | findstr API_BASE_URL

# Verify backend is accessible
curl https://evolveiq-api.cfapps.io/api/health

# Update if wrong
cf set-env evolveiq-frontend API_BASE_URL "https://correct-url.cfapps.io/api"
cf restage evolveiq-frontend
```

**Build fails**:
```bash
# Check logs
cf logs evolveiq-frontend --recent

# Verify package.json
# Increase memory if needed
cf scale evolveiq-frontend -m 1G
```

### Network Issues

**CORS errors**:
The backend API is configured to allow CORS. If you see CORS errors:
1. Verify `api.py` has CORS middleware enabled
2. Check frontend is using correct API_BASE_URL
3. Ensure both apps are on same CF domain or CORS allows cross-origin

## 🔄 Updates and Redeployment

### Update Backend

```bash
# Make code changes
# Commit to git (optional)

# Redeploy
cf push evolveiq-api

# If environment variables changed
cf restage evolveiq-api
```

### Update Frontend

```bash
cd frontend

# Make code changes
# Commit to git (optional)

# Rebuild and redeploy
npm run build
cf push evolveiq-frontend

cd ..
```

### Zero-Downtime Deployment

```bash
# Deploy new version alongside old
cf push evolveiq-api-v2

# Test new version
curl https://evolveiq-api-v2.cfapps.io/api/health

# Switch traffic
cf map-route evolveiq-api-v2 cfapps.io --hostname evolveiq-api
cf unmap-route evolveiq-api cfapps.io --hostname evolveiq-api

# Delete old version
cf delete evolveiq-api
cf rename evolveiq-api-v2 evolveiq-api
```

## 📁 Files Reference

### Root Directory
- `manifest.yml` - Backend CF configuration
- `.cfignore` - Files to exclude
- `runtime.txt` - Python version
- `Procfile` - Process commands
- `requirements.txt` - Python dependencies
- `deploy-backend.bat` - Backend deployment script
- `deploy-full-stack.bat` - Full stack deployment script
- `set_cf_env.bat` - Environment variable setup script

### Frontend Directory
- `frontend/manifest.yml` - Frontend CF configuration
- `frontend/.cfignore` - Frontend exclusions
- `frontend/server.js` - Express server
- `frontend/package.json` - Node dependencies
- `frontend/vite.config.js` - Build configuration

## 💡 Best Practices

1. **Environment Variables**: Never commit secrets to git
2. **Database**: Use managed Supabase, don't deploy PostgreSQL on CF
3. **Scaling**: Start with 1 instance, scale based on load
4. **Monitoring**: Check logs regularly with `cf logs`
5. **Updates**: Test locally before deploying
6. **Backups**: Export Supabase data regularly
7. **Security**: Rotate API keys periodically
8. **Performance**: Use CF metrics to optimize resource allocation

## 📞 Support Resources

- **Cloud Foundry Docs**: https://docs.cloudfoundry.org/
- **Python Buildpack**: https://docs.cloudfoundry.org/buildpacks/python/
- **Node.js Buildpack**: https://docs.cloudfoundry.org/buildpacks/node/
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Supabase Docs**: https://supabase.com/docs
- **React Docs**: https://react.dev/

## ✅ Deployment Checklist

### Pre-Deployment
- [ ] Supabase project created
- [ ] SQL scripts run on Supabase
- [ ] API keys collected
- [ ] CF CLI installed
- [ ] Logged into CF
- [ ] Manifest files updated

### Backend Deployment
- [ ] Backend deployed (`cf push evolveiq-api`)
- [ ] Environment variables set
- [ ] Backend health check passing
- [ ] API docs accessible (`/docs`)

### Frontend Deployment
- [ ] Frontend deployed (`cf push evolveiq-frontend`)
- [ ] API_BASE_URL set
- [ ] Frontend loads in browser
- [ ] Can make API calls

### Post-Deployment
- [ ] Database initialized with data
- [ ] Admin settings configured
- [ ] All features tested
- [ ] Monitoring set up
- [ ] Logs reviewed

---

**Ready to deploy?** Run `.\deploy-full-stack.bat` and follow the prompts!



