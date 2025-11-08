# 🚨 Frontend Deployment - Quick Fix

## The Issue You Hit

**Error**: "Prebuild detected (node_modules already exists)" causing buildpack compile failure.

**Root Cause**: Local `node_modules/` and `dist/` were uploaded to Cloud Foundry, causing conflicts during the build process.

## ✅ Quick Fix (Choose One)

### Option 1: Use Fixed Deployment Script (Easiest)

```bash
cd frontend
.\cf-deploy-fixed.bat
```

This script automatically:
1. ✅ Removes local `node_modules/`
2. ✅ Removes local `dist/`  
3. ✅ Verifies `.cfignore` is correct
4. ✅ Deploys to CF
5. ✅ Sets environment variables

### Option 2: Manual Cleanup

```bash
cd frontend

# 1. Remove local artifacts
rmdir /s /q node_modules
rmdir /s /q dist

# 2. Verify .cfignore (should contain "node_modules/")
type .cfignore | findstr "node_modules"

# 3. Deploy
cf push evolveiq-frontend
```

### Option 3: Pre-Cleanup Then Deploy

```bash
cd frontend

# Run cleanup script
.\pre-deploy-cleanup.bat

# Then deploy normally
cf push evolveiq-frontend
```

## 🔧 What Was Fixed

### 1. Updated `.cfignore`
Now properly excludes:
```
node_modules/  ← CRITICAL: Must be first line
dist/
.cache/
```

### 2. Updated `manifest.yml`
```yaml
memory: 1G  ← Increased from 512M
disk_quota: 2G  ← Increased for build space
env:
  NPM_CONFIG_PRODUCTION: false  ← Allows devDependencies
timeout: 180  ← Longer build time
```

### 3. Updated `package.json`
```json
"heroku-postbuild": "npm run build"  ← CF uses this
```

## 🎯 Deploy Now (Fixed)

```bash
# 1. Go to frontend directory
cd frontend

# 2. Clean up (IMPORTANT!)
rmdir /s /q node_modules
rmdir /s /q dist

# 3. Deploy
cf push evolveiq-frontend

# 4. Set API URL
cf set-env evolveiq-frontend API_BASE_URL https://evolveiq-api.cfapps.io/api
cf restage evolveiq-frontend
```

## ✅ Verification

After deployment:
```bash
# Check status
cf apps

# Should show:
# evolveiq-frontend   running   1/1   ...

# View logs
cf logs evolveiq-frontend --recent

# Test app
# Open: https://evolveiq-frontend.cfapps.io
```

## 🔴 If Still Failing

1. **Check logs first**:
   ```bash
   cf logs evolveiq-frontend --recent
   ```

2. **Verify .cfignore**:
   ```bash
   type .cfignore
   # First line should be: node_modules/
   ```

3. **Increase resources** in `manifest.yml`:
   ```yaml
   memory: 2G
   disk_quota: 3G
   ```

4. **Try clean push**:
   ```bash
   cf delete evolveiq-frontend
   cf push evolveiq-frontend
   ```

5. **See detailed troubleshooting**:
   - Read: `CF_TROUBLESHOOTING.md`
   - Section: "Frontend Build Failures"

## 📋 Complete Deployment Steps (Safe)

```bash
# === BACKEND ===
# (if not already deployed)
cd ..
cf push evolveiq-api
.\set_cf_env.bat
cf restage evolveiq-api

# Get backend URL
cf app evolveiq-api
# Note the URL, e.g., https://evolveiq-api.cfapps.io

# === FRONTEND ===
cd frontend

# Clean up
rmdir /s /q node_modules 2>nul
rmdir /s /q dist 2>nul

# Deploy
cf push evolveiq-frontend

# Configure
cf set-env evolveiq-frontend API_BASE_URL https://evolveiq-api.cfapps.io/api
cf restage evolveiq-frontend

# Verify
cf app evolveiq-frontend
```

## 💡 Why This Happens

Cloud Foundry's Node.js buildpack:
1. Expects clean environment (no `node_modules/`)
2. Installs dependencies fresh
3. Runs build scripts
4. Starts the app

When `node_modules/` already exists:
- ❌ Buildpack gets confused
- ❌ May use incompatible binaries
- ❌ Build fails

**Solution**: Always exclude `node_modules/` and `dist/` from CF uploads!

## 🎯 Prevention

**Always** before deploying:
1. Ensure `.cfignore` contains `node_modules/`
2. Clean local artifacts: `rm -rf node_modules dist`
3. Test build locally: `npm install && npm run build`
4. Then deploy: `cf push`

## 📞 Need More Help?

- **Troubleshooting Guide**: `CF_TROUBLESHOOTING.md`
- **Full Stack Guide**: `FULL_STACK_DEPLOYMENT.md`
- **Frontend Guide**: `frontend/DEPLOY_NOW.md`

---

**Fixed!** Use `.\cf-deploy-fixed.bat` for hassle-free deployment.


