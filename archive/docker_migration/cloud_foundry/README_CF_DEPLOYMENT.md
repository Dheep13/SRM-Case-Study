# Quick Deployment to SAP BTP Cloud Foundry

## 🚀 Quick Start (Windows)

### 1. Install CF CLI
Download from: https://github.com/cloudfoundry/cli/releases

### 2. One-Click Deploy
```powershell
.\deploy_to_cf.bat
```

That's it! The script will:
- Build React frontend
- Login to CF
- Deploy the app

### 3. Set Environment Variables
```powershell
.\set_env_vars.bat
```

### 4. Access Your App
**URL**: https://genai-learning-assistant.cfapps.us10-001.hana.ondemand.com

---

## 📋 Your SAP BTP Details

- **API Endpoint**: https://api.cf.us10-001.hana.ondemand.com
- **Org**: f8861a98trial
- **Memory**: 4GB total (app uses 1GB)

---

## 🔧 Manual Deployment (if script fails)

### Step 1: Login
```powershell
cf login -a https://api.cf.us10-001.hana.ondemand.com -o f8861a98trial
```

### Step 2: Build Frontend
```powershell
cd frontend
npm install
npm run build
cd ..
```

### Step 3: Copy Build Files
```powershell
# Create static directory
New-Item -ItemType Directory -Force -Path static

# Copy build files
Copy-Item -Path "frontend\dist\*" -Destination "static\" -Recurse -Force
```

### Step 4: Deploy
```powershell
cf push
```

### Step 5: Set Environment Variables
```powershell
cf set-env genai-learning-assistant OPENAI_API_KEY "your_key_here"
cf set-env genai-learning-assistant TAVILY_API_KEY "your_key_here"
cf set-env genai-learning-assistant SUPABASE_URL "your_url_here"
cf set-env genai-learning-assistant SUPABASE_KEY "your_key_here"

# Restart to apply
cf restage genai-learning-assistant
```

---

## 📊 Useful Commands

```powershell
# View app status
cf apps

# View logs
cf logs genai-learning-assistant --recent

# Real-time logs
cf logs genai-learning-assistant

# Restart app
cf restart genai-learning-assistant

# Scale memory
cf scale genai-learning-assistant -m 2G

# SSH into app
cf ssh genai-learning-assistant

# Delete app
cf delete genai-learning-assistant
```

---

## 🔍 Troubleshooting

### App Won't Start
```powershell
cf logs genai-learning-assistant --recent
```

### Check Environment Variables
```powershell
cf env genai-learning-assistant
```

### Memory Issues
```powershell
cf scale genai-learning-assistant -m 2G
```

### Need to Update Code
```powershell
# Rebuild and redeploy
.\deploy_to_cf.bat
```

---

## 📁 Files Created for Deployment

- `manifest.yml` - CF deployment configuration
- `Procfile` - Start command
- `runtime.txt` - Python version
- `.cfignore` - Files to exclude
- `deploy_to_cf.bat` - Automated deployment script
- `set_env_vars.bat` - Set environment variables

---

## ✅ Post-Deployment Checklist

- [ ] App deployed successfully
- [ ] Environment variables set
- [ ] Can access app URL
- [ ] Chat feature works
- [ ] Discover feature works
- [ ] Analytics loads
- [ ] All API endpoints responding

---

## 💡 Tips

1. **Memory Quota**: Your trial has 4GB. The app uses 1GB.
2. **Buildpack**: Python buildpack is auto-detected
3. **Port**: Cloud Foundry assigns port via `$PORT` env var
4. **Logs**: Always check logs if something fails
5. **Environment**: Use CF env vars, not `.env` file

---

## 🔗 Resources

- **SAP BTP Docs**: https://help.sap.com/docs/btp
- **CF CLI Docs**: https://docs.cloudfoundry.org/
- **Your CF Dashboard**: https://cockpit.us10-001.hana.ondemand.com/

---

## 🆘 Need Help?

Check `DEPLOYMENT_GUIDE.md` for detailed instructions and troubleshooting.



