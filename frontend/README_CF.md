# EvolveIQ Frontend - Cloud Foundry Deployment

## 🚀 Quick Start

```bash
# 1. Update manifest.yml with your settings
# 2. Run pre-deployment check
.\pre-deploy-check.bat

# 3. Deploy
.\cf-deploy.bat
```

## 📁 Deployment Files

| File | Purpose |
|------|---------|
| `manifest.yml` | CF configuration - **UPDATE THIS** |
| `server.js` | Express server for runtime config |
| `package.json` | Dependencies and build scripts |
| `vite.config.js` | Build configuration |
| `.cfignore` | Files to exclude from deployment |
| `cf-deploy.bat` | Windows deployment script |
| `deploy.sh` | Mac/Linux deployment script |
| `pre-deploy-check.bat` | Pre-deployment verification |

## 📖 Documentation

- **[DEPLOY_NOW.md](DEPLOY_NOW.md)** - Quick 3-step deployment guide ⭐ START HERE
- **[CF_DEPLOYMENT_CHECKLIST.md](CF_DEPLOYMENT_CHECKLIST.md)** - Detailed checklist
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Full deployment guide
- **[CLOUD_FOUNDRY_SETUP.md](CLOUD_FOUNDRY_SETUP.md)** - Technical setup details

## ⚙️ Configuration Required

### 1. Edit `manifest.yml`

**Line 22** - Set your backend API URL:
```yaml
API_BASE_URL: https://your-backend-api.cfapps.io/api
```

**Line 27** - Uncomment and set your route:
```yaml
routes:
  - route: evolveiq-frontend.cfapps.io
```

### 2. Login to Cloud Foundry

```bash
cf login -a https://api.your-cf-domain.com
```

### 3. Deploy

```bash
cf push
```

## 🔍 Verification Commands

```bash
# Check app status
cf apps

# View logs
cf logs evolveiq-frontend --recent

# Check environment
cf env evolveiq-frontend

# View app details
cf app evolveiq-frontend
```

## 🛠️ Common Commands

```bash
# Set API URL
cf set-env evolveiq-frontend API_BASE_URL https://api.example.com
cf restage evolveiq-frontend

# Scale app
cf scale evolveiq-frontend -i 2  # 2 instances
cf scale evolveiq-frontend -m 1G  # 1GB memory

# Restart app
cf restart evolveiq-frontend

# View SSH
cf ssh evolveiq-frontend
```

## 📊 Application Details

- **Name**: evolveiq-frontend
- **Buildpack**: Node.js (auto-detected)
- **Runtime**: Node.js + Express
- **Build Tool**: Vite
- **Framework**: React 18
- **Memory**: 512MB (configurable)
- **Disk**: 1GB (configurable)

## 🏗️ Build Process

1. `npm install` - Install dependencies
2. `npm run build` - Build React app with Vite
3. Output: `dist/` folder with optimized production build
4. `npm start` - Start Express server serving `dist/`

## 🌐 Features

- ✅ Runtime environment variable injection
- ✅ SPA routing support
- ✅ Production-optimized builds
- ✅ Automatic health checks
- ✅ Zero-downtime deployments
- ✅ Easy scaling

## 🔐 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `API_BASE_URL` | Backend API URL | Yes |
| `NODE_ENV` | Environment (production) | Auto-set |
| `PORT` | Server port | Auto-set by CF |

Set via:
```bash
cf set-env evolveiq-frontend API_BASE_URL https://api.example.com
cf restage evolveiq-frontend
```

## 🐛 Troubleshooting

### App won't start
```bash
cf logs evolveiq-frontend --recent
```

Common fixes:
- Check API_BASE_URL is set
- Verify dist/ folder was built
- Check memory allocation

### API calls failing
```bash
# Check environment
cf env evolveiq-frontend

# Update API URL
cf set-env evolveiq-frontend API_BASE_URL https://correct-url.com/api
cf restage evolveiq-frontend
```

### Route issues
```bash
# Check routes
cf routes

# Map new route
cf map-route evolveiq-frontend cfapps.io --hostname my-app
```

## 📞 Support

- CF CLI Docs: https://docs.cloudfoundry.org/cf-cli/
- Node.js Buildpack: https://docs.cloudfoundry.org/buildpacks/node/
- Vite Docs: https://vitejs.dev/
- React Docs: https://react.dev/

## ✅ Pre-Deployment Checklist

- [ ] CF CLI installed
- [ ] Logged into CF (`cf login`)
- [ ] `manifest.yml` updated
- [ ] API_BASE_URL configured
- [ ] Route configured
- [ ] Build tested locally (`npm run build`)
- [ ] Ready to deploy!

---

**Next**: Run `.\pre-deploy-check.bat` then `.\cf-deploy.bat`


