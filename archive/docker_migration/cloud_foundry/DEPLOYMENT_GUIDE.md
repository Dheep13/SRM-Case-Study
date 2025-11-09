# SAP BTP Cloud Foundry Deployment Guide

This guide will help you deploy the GenAI Learning Assistant to SAP BTP Cloud Foundry.

## Prerequisites

1. **Cloud Foundry CLI**: Download and install from https://github.com/cloudfoundry/cli/releases
2. **Node.js and npm**: For building the React frontend
3. **Python 3.11**: For local testing

## Your SAP BTP Details

- **API Endpoint**: https://api.cf.us10-001.hana.ondemand.com
- **Org Name**: f8861a98trial
- **Org ID**: 3ccddaed-07b8-489d-96ba-87e6b8420994
- **Memory Limit**: 4,096MB (App uses 1GB)

## Deployment Steps

### 1. Install Cloud Foundry CLI

```powershell
# Download from: https://github.com/cloudfoundry/cli/releases
# Install and verify
cf version
```

### 2. Login to Cloud Foundry

```powershell
cf login -a https://api.cf.us10-001.hana.ondemand.com -o f8861a98trial
```

You'll be prompted for:
- Email
- Password
- Space (select or create one, e.g., "dev")

### 3. Build React Frontend

```powershell
cd frontend
npm install
npm run build
cd ..
```

### 4. Copy Frontend Build to Static Directory

```powershell
# Create static directory
mkdir static

# Copy build files (PowerShell)
Copy-Item -Path "frontend\dist\*" -Destination "static\" -Recurse -Force
```

### 5. Set Environment Variables

Before deploying, set your environment variables:

```powershell
# After first deployment, set environment variables
cf set-env genai-learning-assistant OPENAI_API_KEY "your_openai_key"
cf set-env genai-learning-assistant TAVILY_API_KEY "your_tavily_key"
cf set-env genai-learning-assistant SUPABASE_URL "your_supabase_url"
cf set-env genai-learning-assistant SUPABASE_KEY "your_supabase_key"

# Optional
cf set-env genai-learning-assistant GITHUB_TOKEN "your_github_token"

# Restart to apply changes
cf restage genai-learning-assistant
```

### 6. Deploy Application

```powershell
cf push
```

## Automated Deployment

Use the provided batch script for easy deployment:

```powershell
# Deploy everything automatically
.\deploy_to_cf.bat

# Set environment variables after deployment
.\set_env_vars.bat
```

## Post-Deployment

### View Application URL

```powershell
cf apps
```

Your app will be available at:
**https://genai-learning-assistant.cfapps.us10-001.hana.ondemand.com**

### View Logs

```powershell
# Real-time logs
cf logs genai-learning-assistant

# Recent logs
cf logs genai-learning-assistant --recent
```

### Check Application Status

```powershell
cf app genai-learning-assistant
```

### Scale Application

```powershell
# Increase memory
cf scale genai-learning-assistant -m 2G

# Increase instances
cf scale genai-learning-assistant -i 2
```

## Updating the Application

When you make changes:

```powershell
# Rebuild frontend
cd frontend
npm run build
cd ..

# Copy to static
Copy-Item -Path "frontend\dist\*" -Destination "static\" -Recurse -Force

# Push update
cf push
```

## Troubleshooting

### Application Won't Start

```powershell
# Check logs
cf logs genai-learning-assistant --recent

# Check environment variables
cf env genai-learning-assistant

# Restart app
cf restart genai-learning-assistant
```

### Port Binding Issues

Cloud Foundry automatically assigns a port via `$PORT` environment variable. The app is configured to use this.

### Memory Issues

If the app crashes due to memory:

```powershell
cf scale genai-learning-assistant -m 2G
```

### Environment Variables Not Working

```powershell
# List all env vars
cf env genai-learning-assistant

# Restage after setting env vars
cf restage genai-learning-assistant
```

## Architecture on Cloud Foundry

```
┌─────────────────────────────────────┐
│   SAP BTP Cloud Foundry Platform   │
│                                     │
│  ┌───────────────────────────────┐ │
│  │  genai-learning-assistant     │ │
│  │                               │ │
│  │  ┌─────────────────────────┐ │ │
│  │  │   FastAPI Backend       │ │ │
│  │  │   (Python 3.11)         │ │ │
│  │  │   - REST API            │ │ │
│  │  │   - Agent Orchestration │ │ │
│  │  │   - RAG Chatbot         │ │ │
│  │  └─────────────────────────┘ │ │
│  │                               │ │
│  │  ┌─────────────────────────┐ │ │
│  │  │   Static Files          │ │ │
│  │  │   (React Frontend)      │ │ │
│  │  └─────────────────────────┘ │ │
│  │                               │ │
│  │  Memory: 1GB                  │ │
│  │  Instances: 1                 │ │
│  └───────────────────────────────┘ │
│                                     │
└─────────────────────────────────────┘
              │
              ▼
    ┌──────────────────┐
    │  External APIs   │
    │  - Supabase DB   │
    │  - OpenAI        │
    │  - Tavily        │
    └──────────────────┘
```

## Cost Considerations

- **Memory**: 1GB x 1 instance = ~1GB of your 4GB quota
- **Remaining**: 3GB available for other apps
- **Always Free Tier**: Check SAP BTP trial limitations

## Security Best Practices

1. **Never commit `.env` file** - It's in `.gitignore`
2. **Use CF environment variables** - Set via `cf set-env`
3. **Rotate API keys regularly** - Update in CF env vars
4. **Monitor logs** - Check for suspicious activity

## Additional Commands

```powershell
# Delete app
cf delete genai-learning-assistant

# SSH into app instance (if enabled)
cf ssh genai-learning-assistant

# View app events
cf events genai-learning-assistant

# Map custom domain (if you have one)
cf map-route genai-learning-assistant your-domain.com --hostname genai
```

## Support

- **SAP BTP Documentation**: https://help.sap.com/docs/btp
- **Cloud Foundry Docs**: https://docs.cloudfoundry.org/
- **Your Org**: f8861a98trial

## Next Steps

1. Deploy the application
2. Set environment variables
3. Test all features
4. Monitor performance
5. Scale if needed



