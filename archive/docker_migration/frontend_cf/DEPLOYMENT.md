# Cloud Foundry Deployment Guide

## Prerequisites

1. Install Cloud Foundry CLI: https://github.com/cloudfoundry/cli#downloads
2. Login to your Cloud Foundry instance:
   ```bash
   cf login -a https://api.your-domain.com
   ```

## Pre-Deployment Steps

### 1. Build the Application

```bash
cd frontend
npm install
npm run build
```

This creates a `dist/` folder with the production build.

### 2. Update Configuration

Before deploying, update `manifest.yml` with your actual values:

- **Application Name**: Change `evolveiq-frontend` to your preferred name
- **Route**: Update `evolveiq-frontend.apps.your-domain.com` to your domain
- **API_BASE_URL**: Set your backend API URL in the `env` section

Example:
```yaml
applications:
- name: evolveiq-frontend
  env:
    API_BASE_URL: https://your-backend-api.com/api
  routes:
    - route: evolveiq-frontend.apps.your-domain.com
```

## Deployment

### Option 1: Using Manifest (Recommended)

1. **Update manifest.yml** with your values:
   - Application name
   - Route/domain
   - API_BASE_URL

2. **Deploy**:
   ```bash
   cd frontend
   cf push
   ```

### Option 2: Using Deployment Script

```bash
cd frontend
export API_BASE_URL=https://your-api.com/api
chmod +x deploy.sh
./deploy.sh
```

### Option 3: Manual Push with Environment Variables

```bash
cd frontend
npm install
npm run build
cf push evolveiq-frontend -p . -b nodejs_buildpack
cf set-env evolveiq-frontend API_BASE_URL https://your-api.com/api
cf restage evolveiq-frontend
```

## Post-Deployment

### Set Environment Variables

```bash
cf set-env evolveiq-frontend API_BASE_URL https://your-backend-api.com/api
cf restage evolveiq-frontend
```

### Verify Deployment

```bash
cf apps
cf logs evolveiq-frontend --recent
```

## Troubleshooting

### Build Fails

- Ensure `npm run build` completes successfully locally
- Check that `dist/` folder exists and contains `index.html`

### Static Files Not Loading

- Verify `Staticfile` exists in the root of `frontend/` directory
- Check that `dist/` is the correct build output directory

### API Calls Failing

- Verify `API_BASE_URL` environment variable is set correctly
- Check CORS settings on your backend API
- Ensure backend API is accessible from Cloud Foundry

### Route Issues

- Verify route is available: `cf routes`
- Check domain is correct in manifest.yml

## Environment Variables

The following environment variables can be set:

- `API_BASE_URL`: Backend API base URL (required)
- `FORCE_HTTPS`: Force HTTPS redirects (default: true)

Set them using:
```bash
cf set-env evolveiq-frontend API_BASE_URL https://api.example.com
cf restage evolveiq-frontend
```

## Scaling

To scale the application:

```bash
cf scale evolveiq-frontend -i 2  # 2 instances
cf scale evolveiq-frontend -m 512M  # 512MB memory
```

## Monitoring

View application logs:
```bash
cf logs evolveiq-frontend
```

View application status:
```bash
cf app evolveiq-frontend
```

