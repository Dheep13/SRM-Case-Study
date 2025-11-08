# Cloud Foundry Setup Summary

## Files Created for Cloud Foundry Deployment

### Core Configuration Files

1. **manifest.yml** - Main Cloud Foundry manifest
   - Uses Node.js buildpack
   - Configured for production deployment
   - Includes environment variables

2. **server.js** - Express server for serving the app
   - Serves static files from `dist/`
   - Injects environment variables at runtime
   - Handles SPA routing

3. **package.json** - Updated with:
   - React and React-DOM dependencies
   - @vitejs/plugin-react for Vite
   - Express for server
   - Build and start scripts

4. **vite.config.js** - Vite configuration
   - Optimized production builds
   - Code splitting
   - Proper output directory

### Deployment Files

5. **deploy.sh** - Automated deployment script
   - Builds the application
   - Deploys to Cloud Foundry
   - Sets environment variables

6. **DEPLOYMENT.md** - Complete deployment guide
   - Step-by-step instructions
   - Troubleshooting tips
   - Environment variable setup

### Configuration Files

7. **.cfignore** - Files to exclude from deployment
   - node_modules, .git, logs, etc.

8. **.env.example** - Environment variable template

9. **Staticfile** - Alternative staticfile buildpack config (if needed)

10. **manifest-nodejs.yml** - Alternative Node.js manifest

## Quick Start

1. **Update manifest.yml**:
   ```yaml
   - name: evolveiq-frontend  # Your app name
   - route: your-app.apps.your-domain.com  # Your route
   - API_BASE_URL: https://your-backend-api.com/api  # Your API URL
   ```

2. **Deploy**:
   ```bash
   cd frontend
   cf push
   ```

3. **Set API URL** (if not in manifest):
   ```bash
   cf set-env evolveiq-frontend API_BASE_URL https://your-api.com/api
   cf restage evolveiq-frontend
   ```

## Environment Variables

- `API_BASE_URL` - Backend API base URL (required)
- `PORT` - Server port (auto-set by Cloud Foundry)
- `NODE_ENV` - Set to 'production'

## Build Process

1. `npm install` - Installs dependencies
2. `npm run build` - Builds React app to `dist/`
3. `npm start` - Starts Express server serving `dist/`

## Important Notes

- The app uses Express server to inject environment variables at runtime
- Build happens automatically during `cf push` via `postinstall` script
- Static files are served from `dist/` directory
- SPA routing is handled by Express server


