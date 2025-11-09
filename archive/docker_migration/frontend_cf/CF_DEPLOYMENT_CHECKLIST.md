# Cloud Foundry Deployment Checklist

## Pre-Deployment Checklist

### 1. Environment Setup
- [ ] Cloud Foundry CLI installed (`cf --version`)
- [ ] Logged into Cloud Foundry (`cf login`)
- [ ] Correct org and space selected (`cf target`)

### 2. Configuration Files Review

#### manifest.yml
- [ ] **Application name** updated (line 3)
  - Default: `evolveiq-frontend`
  - Change to: `your-app-name`
  
- [ ] **Route/Domain** updated (line 17)
  - Default: `evolveiq-frontend.apps.your-domain.com`
  - Change to: `your-app.cfapps.io` or your custom domain
  
- [ ] **API_BASE_URL** updated (line 15)
  - Default: `https://your-api-domain.com/api`
  - Change to: `https://your-backend-api.cfapps.io/api`

- [ ] **Memory/Disk** appropriate
  - Memory: 512M (increase if needed)
  - Disk: 1G (should be sufficient)

### 3. Code Verification
- [ ] Run `npm install` in frontend directory
- [ ] Run `npm run build` successfully
- [ ] Check `dist/` folder contains built files
- [ ] Verify `server.js` exists
- [ ] Verify `vite.config.js` exists

### 4. Dependencies Check
```bash
cd frontend
npm install
npm run build
```

Expected output: `dist/` folder with `index.html` and assets

## Deployment Steps

### Step 1: Update manifest.yml

```yaml
---
applications:
- name: your-app-name  # UPDATE THIS
  memory: 512M
  disk_quota: 1G
  instances: 1
  buildpacks:
    - nodejs_buildpack
  stack: cflinuxfs4
  path: .
  command: npm start
  env:
    NODE_ENV: production
    PORT: 8080
    API_BASE_URL: https://your-backend-api.cfapps.io/api  # UPDATE THIS
  routes:
    - route: your-app-name.cfapps.io  # UPDATE THIS
  health-check-type: http
  health-check-http-endpoint: /
  timeout: 120
```

### Step 2: Test Build Locally

```bash
cd frontend
npm install
npm run build
npm start  # Test on http://localhost:8080
```

### Step 3: Deploy to Cloud Foundry

```bash
cd frontend
cf push
```

### Step 4: Verify Deployment

```bash
# Check app status
cf apps

# View logs
cf logs your-app-name --recent

# Check environment variables
cf env your-app-name
```

### Step 5: Test Application

1. Open the route URL in browser
2. Check if app loads correctly
3. Verify API calls are working
4. Test all major features:
   - Home page
   - Chat functionality
   - Analytics dashboard
   - Expert Consultation
   - Assignments/Today's Class

## Post-Deployment

### Update Environment Variables (if needed)

```bash
cf set-env your-app-name API_BASE_URL https://new-api-url.com/api
cf restage your-app-name
```

### Scale Application (if needed)

```bash
# Increase instances
cf scale your-app-name -i 2

# Increase memory
cf scale your-app-name -m 1G
```

### View Application Info

```bash
cf app your-app-name
```

## Troubleshooting

### Build Fails
```bash
# Check logs
cf logs your-app-name --recent

# Common issues:
# - Missing dependencies: Run npm install locally
# - Build errors: Check package.json scripts
# - Memory limit: Increase memory in manifest.yml
```

### Application Crashes
```bash
# Check logs
cf logs your-app-name --recent

# Check health
cf app your-app-name

# Common issues:
# - Port binding: Ensure server listens on process.env.PORT
# - File not found: Ensure dist/ is built correctly
# - Module errors: Check package.json dependencies
```

### API Calls Failing
```bash
# Check environment variables
cf env your-app-name

# Update API URL if wrong
cf set-env your-app-name API_BASE_URL https://correct-api-url.com/api
cf restage your-app-name

# Check CORS on backend
# Verify backend API is accessible
```

### Routing Issues
```bash
# Check routes
cf routes

# Map new route
cf map-route your-app-name your-domain.com --hostname your-app

# Unmap old route
cf unmap-route your-app-name old-domain.com --hostname old-app
```

## Quick Reference Commands

```bash
# Login
cf login -a https://api.your-cf-domain.com

# Push app
cf push

# View logs (live)
cf logs your-app-name

# View logs (recent)
cf logs your-app-name --recent

# Restart app
cf restart your-app-name

# Restage app (after env changes)
cf restage your-app-name

# Stop app
cf stop your-app-name

# Start app
cf start your-app-name

# Delete app
cf delete your-app-name -r  # -r removes routes
```

## Files Deployed

The following files will be deployed to Cloud Foundry:

- `package.json` - Dependencies and scripts
- `server.js` - Express server
- `vite.config.js` - Build configuration
- `src/` - Source code
- `public/` - Public assets
- `index.html` - Main HTML file

Files excluded (see `.cfignore`):
- `node_modules/` - Will be installed during buildpack
- `.git/` - Version control
- `.env*` - Environment files
- `dist/` - Built locally, recreated during push

## Success Indicators

✅ App deployed: `cf apps` shows status "running"
✅ Route accessible: Opening URL shows application
✅ Logs clean: No errors in `cf logs`
✅ API calls work: Features function correctly
✅ Health check passing: `cf app` shows healthy

## Need Help?

- Cloud Foundry Docs: https://docs.cloudfoundry.org/
- Buildpack Docs: https://docs.cloudfoundry.org/buildpacks/node/
- Support: Check with your CF admin or platform team



