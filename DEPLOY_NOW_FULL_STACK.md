# 🚀 Deploy EvolveIQ Full Stack NOW

## Quick 5-Step Deployment

### ✅ Prerequisites (5 minutes)

1. **Cloud Foundry CLI** - Installed? Run: `cf --version`
2. **Supabase Account** - Create at: https://supabase.com
3. **API Keys Ready**:
   - OpenAI: https://platform.openai.com/api-keys
   - Tavily: https://tavily.com/
4. **CF Login**: Run `cf login`

### 🗃️ Step 1: Setup Database (10 minutes)

1. **Create Supabase Project**:
   - Go to https://supabase.com/dashboard
   - Click "New Project"
   - Note your Project URL and API Key

2. **Run SQL Scripts** (in Supabase SQL Editor):
   ```sql
   -- Copy and run these in order:
   -- 1. db_integration/schema.sql
   -- 2. db_integration/vector_embeddings.sql  
   -- 3. db_integration/admin_schema.sql
   ```

3. **Save Credentials**:
   - Supabase URL: `https://xxxxx.supabase.co`
   - Supabase Key: `eyJxxx...`

### ⚙️ Step 2: Configure Files (2 minutes)

**Backend manifest.yml** (lines 35-36):
```yaml
# Uncomment and set your route:
routes:
  - route: evolveiq-api.cfapps.io
```

**Frontend manifest.yml** (lines 25-27):
```yaml
# Uncomment and set your route:
routes:
  - route: evolveiq-frontend.cfapps.io
```

### 🚀 Step 3: Deploy Full Stack (15 minutes)

```bash
# Run the full stack deployment script
.\deploy-full-stack.bat
```

**What it does**:
1. ✅ Deploys backend API
2. ✅ Prompts for API keys and credentials
3. ✅ Sets all environment variables
4. ✅ Deploys frontend
5. ✅ Links frontend to backend

**You'll be asked for**:
- OpenAI API Key
- Supabase URL
- Supabase Key
- Tavily API Key
- GitHub Token (optional)

### ✓ Step 4: Initialize Data (5 minutes)

```bash
# SSH into backend
cf ssh evolveiq-api

# Load initial data
python load_and_visualize.py "GenAI skills for IT students"

# Generate embeddings
python setup_chatbot.py

# Exit
exit
```

### 🎉 Step 5: Test Everything (5 minutes)

1. **Backend API**:
   - Health: `https://evolveiq-api.cfapps.io/api/health`
   - Docs: `https://evolveiq-api.cfapps.io/docs`

2. **Frontend**:
   - Open: `https://evolveiq-frontend.cfapps.io`
   - Test chat, analytics, expert consultation

## 📝 Alternative: Manual Deployment

### Backend First

```bash
# Deploy
cf push evolveiq-api

# Set environment variables
cf set-env evolveiq-api OPENAI_API_KEY "sk-..."
cf set-env evolveiq-api SUPABASE_URL "https://xxx.supabase.co"
cf set-env evolveiq-api SUPABASE_KEY "eyJxxx..."
cf set-env evolveiq-api TAVILY_API_KEY "tvly-..."
cf set-env evolveiq-api LLM_MODEL "gpt-4o-mini"

# Restage to apply
cf restage evolveiq-api
```

### Frontend Second

```bash
cd frontend

# Get backend URL
cf app evolveiq-api

# Set API URL
cf set-env evolveiq-frontend API_BASE_URL "https://evolveiq-api.cfapps.io/api"

# Deploy
cf push evolveiq-frontend

cd ..
```

## ✅ Verification Checklist

- [ ] Backend deployed and running
- [ ] Backend health check passing
- [ ] All environment variables set
- [ ] Frontend deployed and running
- [ ] Frontend can reach backend API
- [ ] Database has initial data
- [ ] Embeddings generated
- [ ] Chat works
- [ ] Analytics loads
- [ ] All features tested

## 🐛 Quick Troubleshooting

**Backend won't start**:
```bash
cf logs evolveiq-api --recent
# Check for missing environment variables
cf env evolveiq-api
```

**Frontend can't reach backend**:
```bash
# Verify API_BASE_URL
cf env evolveiq-frontend
# Should show: API_BASE_URL: https://evolveiq-api.cfapps.io/api
```

**Database connection fails**:
```bash
# Check Supabase credentials
cf env evolveiq-api | findstr SUPABASE
```

## 📊 Monitor Your Apps

```bash
# View all apps
cf apps

# Backend logs
cf logs evolveiq-api --recent

# Frontend logs  
cf logs evolveiq-frontend --recent

# App details
cf app evolveiq-api
cf app evolveiq-frontend
```

## 🔄 Update Deployed Apps

```bash
# Update backend
cf push evolveiq-api

# Update frontend
cd frontend
cf push evolveiq-frontend
cd ..
```

## 📞 Need Help?

See detailed guides:
- **FULL_STACK_DEPLOYMENT.md** - Complete deployment guide
- **frontend/DEPLOY_NOW.md** - Frontend-specific guide

---

**Ready?** Run `.\deploy-full-stack.bat` now!


