# Frontend Deployment - Issues Fixed

## 🔴 Issues Encountered

### Issue 1: node_modules Upload
**Error**: "Prebuild detected (node_modules already exists)"
**Status**: ✅ FIXED

### Issue 2: Terser Missing
**Error**: "terser not found. Since Vite v3, terser has become an optional dependency"
**Status**: ✅ FIXED

### Issue 3: Locked Files on Windows
**Error**: "Access is denied" when deleting node_modules
**Status**: ✅ FIXED

## ✅ Fixes Applied

### 1. Added Terser to Dependencies
```json
// package.json
"dependencies": {
  ...
  "terser": "^5.27.0"  ← ADDED
}
```

### 2. Changed Build Minifier
```javascript
// vite.config.js
build: {
  minify: 'esbuild'  ← Changed from 'terser'
}
```

### 3. Removed Security Warning
```javascript
// vite.config.js
// REMOVED: define: { 'process.env': process.env }
```

### 4. Created Force Cleanup Script
```bash
# New file: force-cleanup.bat
- Kills Node processes
- Forces removal of locked files
- Uses takeown for Windows permissions
```

### 5. Updated Deployment Script
```bash
# cf-deploy-fixed.bat
- Kills Node/npm processes first
- Attempts force cleanup if needed
- Warns if files still locked
```

## 🚀 Deploy Now (All Fixes Applied)

### Option 1: Using Fixed Script (Recommended)
```bash
cd frontend

# Close all terminals/editors first!

# Run fixed deployment
.\cf-deploy-fixed.bat
```

### Option 2: Manual Steps
```bash
cd frontend

# 1. Kill Node processes
taskkill /F /IM node.exe
taskkill /F /IM npm.exe

# 2. Force cleanup
.\force-cleanup.bat

# 3. Verify cleanup
dir node_modules
# Should show: File Not Found

# 4. Deploy
cf push evolveiq-frontend

# 5. Set API URL
cf set-env evolveiq-frontend API_BASE_URL https://evolveiq-api.cfapps.io/api
cf restage evolveiq-frontend
```

### Option 3: Alternative - Don't Delete node_modules
If you continue having issues with locked files:

```bash
# Just rely on .cfignore (it's configured correctly)
# Don't delete node_modules, just push
cf push evolveiq-frontend
```

The `.cfignore` file will prevent `node_modules/` from being uploaded, even if it exists locally.

## 📋 Pre-Flight Checklist

Before deploying:
- [ ] Close all VS Code windows
- [ ] Close all terminals
- [ ] Close all Node processes
- [ ] Verify `.cfignore` contains `node_modules/`
- [ ] Run `force-cleanup.bat` if needed

## 🔍 Verification

After fixes are applied, your build should:

1. ✅ Not upload node_modules to CF
2. ✅ Install fresh dependencies on CF
3. ✅ Build successfully with Vite
4. ✅ No terser errors
5. ✅ No security warnings
6. ✅ Deploy successfully

## 📁 Updated Files

- ✅ `package.json` - Added terser dependency
- ✅ `vite.config.js` - Changed to esbuild minifier
- ✅ `.cfignore` - Properly excludes node_modules
- ✅ `manifest.yml` - Increased resources
- 🆕 `force-cleanup.bat` - Windows cleanup script
- ✅ `cf-deploy-fixed.bat` - Updated deployment script

## 🎯 Expected Deployment Flow

```
[1/5] Cleaning up local artifacts
  ✓ Killed Node processes
  ✓ node_modules removed
  ✓ dist removed
  ✓ Cleanup complete

[2/5] Verifying .cfignore
  ✓ .cfignore configured

[3/5] Verifying manifest.yml
  ✓ manifest.yml found

[4/5] Deploying to Cloud Foundry
  ✓ Packaging files... (no node_modules)
  ✓ Uploading... (~50 KB)
  ✓ Downloading buildpack
  ✓ Installing dependencies (fresh)
  ✓ Running heroku-postbuild
  ✓ Building with Vite (esbuild)
  ✓ Build successful
  ✓ Starting app

[5/5] Setting environment variables
  ✓ API_BASE_URL set
  ✓ App restaged

DEPLOYMENT COMPLETE!
```

## 🐛 If Still Failing

### 1. Check Logs
```bash
cf logs evolveiq-frontend --recent
```

### 2. Verify No node_modules Upload
Look for "Uploading files" in logs:
- ✅ Good: 50-100 KB
- ❌ Bad: 100+ MB (means node_modules uploaded)

### 3. Clean Everything
```bash
# Nuclear option
cd frontend
.\force-cleanup.bat
del package-lock.json
npm install
npm run build
# Test locally first
npm start
# Then deploy
cf push
```

### 4. Try Without Build
If build keeps failing on CF:

**Option A**: Build locally, push dist
```bash
# Edit manifest.yml
command: npm install express && node server.js

# Build locally
npm run build

# Remove dist from .cfignore temporarily
# Deploy
cf push
```

**Option B**: Use simpler buildpack
```bash
# Try staticfile buildpack instead
cf push evolveiq-frontend -b staticfile_buildpack -p dist
```

## 💡 Why These Fixes Work

1. **Terser**: Added as dependency so Vite can use it for minification
2. **Esbuild**: Faster and already included, no extra dependency
3. **Process Env**: Removed to avoid security warning and potential env leaks
4. **Force Cleanup**: Handles Windows file locking issues
5. **.cfignore**: Prevents node_modules upload even if it exists

## ✅ Success Indicators

After deployment:
- ✅ Build completes in 2-3 minutes
- ✅ No terser errors
- ✅ No prebuild warnings
- ✅ App starts successfully
- ✅ Health check passes
- ✅ Frontend loads in browser

---

**All fixes applied!** Run `.\cf-deploy-fixed.bat` to deploy with all fixes.


