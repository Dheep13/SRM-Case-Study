# Deploy EvolveIQ to Cloud Foundry NOW

## 🚀 Quick Deploy (3 Steps)

### Step 1: Update Configuration (2 minutes)

Edit `manifest.yml` and uncomment/update:

```yaml
# Line 22: Set your backend API URL
API_BASE_URL: https://your-backend-api.cfapps.io/api

# Line 27: Set your route
routes:
  - route: evolveiq-frontend.cfapps.io
```

### Step 2: Login to Cloud Foundry (1 minute)

```bash
cf login -a https://api.your-cf-domain.com
# Enter your credentials
```

### Step 3: Deploy! (5-10 minutes)

**Option A: Windows**
```cmd
cd frontend
cf-deploy.bat
```

**Option B: Mac/Linux**
```bash
cd frontend
chmod +x deploy.sh
./deploy.sh
```

**Option C: Manual**
```bash
cd frontend
npm install
npm run build
cf push
```

## ✅ Verification

After deployment completes:

1. **Check Status**
   ```bash
   cf apps
   ```
   Should show "running" status

2. **Open App**
   ```bash
   cf app evolveiq-frontend
   ```
   Note the URL and open in browser

3. **Check Logs**
   ```bash
   cf logs evolveiq-frontend --recent
   ```
   Should show no errors

## 🔧 Set API URL (If Needed)

If you didn't set `API_BASE_URL` in manifest.yml:

```bash
cf set-env evolveiq-frontend API_BASE_URL https://your-backend-api.cfapps.io/api
cf restage evolveiq-frontend
```

## 📊 Your Deployment

**Application**: EvolveIQ Frontend
**Buildpack**: Node.js
**Memory**: 512MB
**Instances**: 1

**What Gets Deployed**:
- React app (built with Vite)
- Express server (for runtime config)
- All source code and dependencies

**Build Process**:
1. `npm install` - Install dependencies
2. `npm run build` - Build React app
3. `npm start` - Start Express server

## 🆘 Troubleshooting

### "cf: command not found"
Install CF CLI: https://github.com/cloudfoundry/cli#downloads

### "Not logged in"
```bash
cf login
```

### "Route already exists"
Change route in manifest.yml:
```yaml
routes:
  - route: my-unique-name.cfapps.io
```

### "Build failed"
Test locally first:
```bash
npm install
npm run build
```

### "App crashes after deploy"
Check logs:
```bash
cf logs evolveiq-frontend --recent
```

Common fixes:
- Set API_BASE_URL: `cf set-env evolveiq-frontend API_BASE_URL https://...`
- Increase memory: Update manifest.yml memory to 1G
- Check backend API is accessible

## 📁 Files Overview

**Core Files**:
- `manifest.yml` - CF configuration ⚙️ UPDATE THIS
- `package.json` - Dependencies and scripts
- `server.js` - Express server
- `vite.config.js` - Build configuration

**Deployment Scripts**:
- `cf-deploy.bat` - Windows deployment script
- `deploy.sh` - Mac/Linux deployment script

**Documentation**:
- `DEPLOY_NOW.md` - This file (quick start)
- `CF_DEPLOYMENT_CHECKLIST.md` - Detailed checklist
- `DEPLOYMENT.md` - Full deployment guide
- `CLOUD_FOUNDRY_SETUP.md` - Setup summary

## 🎯 Next Steps After Deploy

1. **Test the Application**
   - Open the route URL
   - Test all features
   - Verify API connectivity

2. **Configure Backend API**
   - Ensure backend is deployed
   - Set correct API_BASE_URL
   - Enable CORS if needed

3. **Scale if Needed**
   ```bash
   cf scale evolveiq-frontend -i 2  # 2 instances
   cf scale evolveiq-frontend -m 1G  # 1GB memory
   ```

4. **Set up Custom Domain** (Optional)
   ```bash
   cf map-route evolveiq-frontend your-domain.com --hostname www
   ```

## 📞 Support

- **Cloud Foundry Docs**: https://docs.cloudfoundry.org/
- **Node.js Buildpack**: https://docs.cloudfoundry.org/buildpacks/node/
- **Vite Docs**: https://vitejs.dev/
- **React Docs**: https://react.dev/

---

**Ready to deploy?** Update `manifest.yml` and run `cf-deploy.bat` (Windows) or `./deploy.sh` (Mac/Linux)!



