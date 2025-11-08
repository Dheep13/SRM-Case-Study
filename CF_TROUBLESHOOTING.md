# Cloud Foundry Deployment - Troubleshooting Guide

## 🔴 Frontend Build Failures

### Error: "node_modules already exists"
**Symptom**: Buildpack compile fails with "Prebuild detected (node_modules already exists)"

**Cause**: Local `node_modules/` was uploaded to CF

**Fix**:
```bash
# 1. Ensure node_modules is in .cfignore
cd frontend
echo "node_modules/" >> .cfignore

# 2. Delete local node_modules before push
rm -rf node_modules
# or on Windows:
rmdir /s /q node_modules

# 3. Push again
cf push evolveiq-frontend
```

### Error: "ELIFECYCLE npm ERR!" during build
**Symptom**: Build fails with npm lifecycle errors

**Fix**:
```bash
# 1. Update frontend/manifest.yml
# Set: NPM_CONFIG_PRODUCTION: false

# 2. Increase memory and timeout
# memory: 1G  (was 512M)
# timeout: 180  (was 120)

# 3. Push again
cf push evolveiq-frontend
```

### Error: Vite build fails
**Symptom**: "vite build" command fails

**Fix**:
```bash
# 1. Move vite to dependencies (not devDependencies)
cd frontend
# Edit package.json - move vite to "dependencies"

# 2. Test build locally first
npm install
npm run build

# 3. If successful, push
cf push evolveiq-frontend
```

## 🔴 Backend Deployment Issues

### Error: "App instance exited"
**Symptom**: Backend starts but immediately crashes

**Fix**:
```bash
# 1. Check logs
cf logs evolveiq-api --recent

# 2. Common causes:
# - Missing environment variables
cf set-env evolveiq-api OPENAI_API_KEY "your-key"
cf set-env evolveiq-api SUPABASE_URL "your-url"
cf set-env evolveiq-api SUPABASE_KEY "your-key"
cf set-env evolveiq-api TAVILY_API_KEY "your-key"
cf restage evolveiq-api

# - Port binding issue (should use $PORT)
# - Python version mismatch
```

### Error: "ImportError" or "ModuleNotFoundError"
**Symptom**: Python can't find modules

**Fix**:
```bash
# 1. Check requirements.txt is present and complete
# 2. Verify Python version in runtime.txt
cat runtime.txt  # Should be: python-3.11.x

# 3. Clear buildpack cache
cf push evolveiq-api --no-start
cf restage evolveiq-api
```

### Error: Database connection fails
**Symptom**: "Could not connect to Supabase"

**Fix**:
```bash
# 1. Verify Supabase credentials
cf env evolveiq-api | findstr SUPABASE

# 2. Test Supabase connection
cf ssh evolveiq-api
python3 -c "from db_integration.supabase_client import SupabaseManager; db = SupabaseManager(); print('Connected!')"
exit

# 3. Check Supabase firewall/network settings
# 4. Verify Supabase project is not paused
```

## 🔴 Common Deployment Errors

### Error: "Insufficient resources"
**Symptom**: "You have exceeded your organization's memory limit"

**Fix**:
```bash
# 1. Check current usage
cf apps

# 2. Scale down or stop other apps
cf stop other-app

# 3. Reduce memory in manifest.yml
# Frontend: 512M (instead of 1G)
# Backend: 512M (instead of 1G)

# 4. Push again
cf push
```

### Error: "Route already in use"
**Symptom**: "The route is already in use"

**Fix**:
```bash
# 1. Option A: Use a different route
# Edit manifest.yml:
routes:
  - route: evolveiq-frontend-yourname.cfapps.io

# 2. Option B: Unmap the route from other app
cf routes
cf unmap-route old-app cfapps.io --hostname evolveiq-frontend

# 3. Option C: Delete the route
cf delete-route cfapps.io --hostname evolveiq-frontend
```

### Error: "Staging failed"
**Symptom**: Buildpack staging fails

**Fix**:
```bash
# 1. Check logs
cf logs app-name --recent

# 2. Verify .cfignore excludes unnecessary files
# 3. Check manifest.yml syntax
# 4. Ensure buildpack specified

# 5. Try with clean push
cf delete app-name
cf push app-name
```

## 🔴 Runtime Issues

### Frontend can't reach Backend
**Symptom**: API calls fail with CORS or network errors

**Fix**:
```bash
# 1. Verify API_BASE_URL is set
cf env evolveiq-frontend

# 2. Should be:
# API_BASE_URL: https://evolveiq-api.cfapps.io/api

# 3. Test backend directly
curl https://evolveiq-api.cfapps.io/api/health

# 4. If backend works, update frontend
cf set-env evolveiq-frontend API_BASE_URL "https://evolveiq-api.cfapps.io/api"
cf restage evolveiq-frontend
```

### App is slow or timing out
**Symptom**: Requests take too long or timeout

**Fix**:
```bash
# 1. Scale up instances
cf scale app-name -i 2

# 2. Increase memory
cf scale app-name -m 1G

# 3. Check app logs for bottlenecks
cf logs app-name --recent

# 4. Monitor metrics
cf app app-name
```

### Health check failing
**Symptom**: App crashes repeatedly with health check errors

**Fix**:
```bash
# 1. Test health endpoint manually
curl https://app-url/api/health

# 2. Update health check in manifest.yml
health-check-type: http
health-check-http-endpoint: /api/health
timeout: 180

# 3. Or disable temporarily for debugging
health-check-type: process

# 4. Push again
cf push
```

## 🛠️ Debugging Commands

### View Logs
```bash
# Recent logs
cf logs app-name --recent

# Live logs (keep terminal open)
cf logs app-name

# Filter logs
cf logs app-name --recent | grep ERROR
```

### Check App Status
```bash
# Detailed app info
cf app app-name

# All apps
cf apps

# Environment variables
cf env app-name

# Events (restarts, crashes)
cf events app-name
```

### SSH into App
```bash
# SSH to app
cf ssh app-name

# Check disk usage
cf ssh app-name -c "df -h"

# Check memory
cf ssh app-name -c "free -m"

# Test Python imports
cf ssh evolveiq-api
python3 -c "import fastapi; print('OK')"
exit
```

### Restart/Restage
```bash
# Restart app (keeps environment)
cf restart app-name

# Restage app (rebuilds with buildpack)
cf restage app-name

# Stop and start
cf stop app-name
cf start app-name
```

## 📝 Pre-Flight Checklist

Before deploying, verify:

**Frontend**:
- [ ] `node_modules/` in `.cfignore`
- [ ] `dist/` in `.cfignore`
- [ ] `NPM_CONFIG_PRODUCTION: false` in manifest
- [ ] Memory: 1G or more
- [ ] Route defined in manifest or via CLI

**Backend**:
- [ ] `requirements.txt` exists and complete
- [ ] `runtime.txt` specifies Python 3.11
- [ ] `Procfile` uses correct start command
- [ ] All environment variables documented
- [ ] Memory: 1G or more
- [ ] Health endpoint works locally

**Database**:
- [ ] Supabase project created
- [ ] SQL scripts run
- [ ] Connection strings saved
- [ ] Firewall allows CF connections

## 🆘 Still Having Issues?

### 1. Clean Rebuild
```bash
# Delete app completely
cf delete app-name -r

# Clear any cached data
rm -rf node_modules dist __pycache__

# Push fresh
cf push app-name
```

### 2. Check CF Status
```bash
# Check CF platform status
cf marketplace
cf buildpacks
```

### 3. Verify Files
```bash
# What will be uploaded
ls -la

# Check .cfignore
cat .cfignore

# Check manifest
cat manifest.yml
```

### 4. Get Help
- CF Logs: `cf logs app-name --recent`
- CF Community: https://slack.cloudfoundry.org/
- Stack Overflow: https://stackoverflow.com/questions/tagged/cloud-foundry
- Your CF admin/platform team

## 💡 Pro Tips

1. **Always check logs first**: `cf logs app-name --recent`
2. **Test locally before deploying**: Build and run locally first
3. **Use .cfignore properly**: Exclude dev files and dependencies
4. **Start small**: Deploy with minimal config, then optimize
5. **Monitor memory**: Check `cf app app-name` regularly
6. **Use environment variables**: Never hardcode secrets
7. **Version your deployments**: Tag releases in git

## ✅ Successful Deployment Indicators

- ✅ `cf apps` shows "running" status
- ✅ Health endpoint returns 200 OK
- ✅ No errors in `cf logs --recent`
- ✅ App accessible via route
- ✅ All features work end-to-end


