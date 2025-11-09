# Public Deployment Guide

This guide explains how to deploy your EvolveIQ application to make it publicly accessible.

## Deployment Options

### Option 1: Cloud Platforms (Recommended)

**Popular Platforms:**
- **AWS** (EC2, ECS, Lightsail)
- **Google Cloud** (Compute Engine, Cloud Run)
- **Azure** (Container Instances, App Service)
- **DigitalOcean** (Droplets, App Platform)
- **Linode** (Dedicated/Shared CPU)
- **Hetzner** (Budget-friendly)
- **Railway** (Easy Docker deployment)
- **Render** (Free tier available)
- **Fly.io** (Global edge deployment)

### Option 2: VPS (Virtual Private Server)

**Recommended Providers:**
- DigitalOcean Droplets ($6-12/month)
- Linode ($5-10/month)
- Hetzner Cloud ($4-8/month)
- AWS Lightsail ($3.50-10/month)

## Step-by-Step Deployment

### 1. Choose Your Domain

You'll need:
- A domain name (e.g., `evolveiq.com`) - purchase from Namecheap, GoDaddy, etc.
- Or use a subdomain from your provider (e.g., `your-app.railway.app`)

### 2. Update Configuration Files

#### A. Update CORS in `api.py`

Add your public domain to allowed origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://yourdomain.com",           # Add your domain
        "https://www.yourdomain.com",        # Add www version
        "https://evolveiq.yourdomain.com",   # Add subdomain if using
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### B. Update Frontend API URL

**For Docker deployment**, update `docker-compose.yml`:

```yaml
frontend:
  build:
    context: ./frontend
    dockerfile: Dockerfile
    args:
      - VITE_API_BASE_URL=https://api.yourdomain.com  # Your backend URL
  environment:
    - VITE_API_BASE_URL=https://api.yourdomain.com
```

**Or set environment variable:**
```bash
export VITE_API_BASE_URL=https://api.yourdomain.com
```

#### C. Update `.env` file

```bash
# Your public domain
FRONTEND_URL=https://yourdomain.com
API_URL=https://api.yourdomain.com

# Database (keep secure)
POSTGRES_PASSWORD=your_strong_password_here

# API Keys (already configured)
OPENAI_API_KEY=your_key
SUPABASE_URL=your_url
SUPABASE_KEY=your_key
```

### 3. Deploy to Cloud Platform

#### Example: Railway Deployment

1. **Install Railway CLI:**
```bash
npm i -g @railway/cli
railway login
```

2. **Initialize Project:**
```bash
railway init
railway link
```

3. **Deploy:**
```bash
railway up
```

4. **Set Environment Variables:**
```bash
railway variables set OPENAI_API_KEY=your_key
railway variables set VITE_API_BASE_URL=https://your-app.railway.app
```

5. **Add Custom Domain:**
- Go to Railway dashboard
- Select your project
- Go to Settings → Domains
- Add your custom domain

#### Example: DigitalOcean App Platform

1. **Create App:**
   - Go to DigitalOcean → App Platform
   - Connect your GitHub repository
   - Select Docker Compose

2. **Configure Services:**
   - Frontend: Port 80, Public
   - Backend: Port 8000, Public
   - Database: Managed PostgreSQL

3. **Set Environment Variables:**
   - Add all variables from `.env`
   - Set `VITE_API_BASE_URL` to your backend URL

4. **Add Domain:**
   - Settings → Domains
   - Add your custom domain

#### Example: AWS EC2 (VPS)

1. **Launch EC2 Instance:**
   - Choose Ubuntu 22.04 LTS
   - t2.micro (free tier) or t3.small
   - Configure security group:
     - Port 80 (HTTP)
     - Port 443 (HTTPS)
     - Port 8000 (Backend API)
     - Port 22 (SSH)

2. **SSH into Server:**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

3. **Install Docker:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
sudo usermod -aG docker ubuntu
```

4. **Clone and Deploy:**
```bash
git clone your-repo-url
cd Case\ Study
# Update docker-compose.yml with public URLs
docker compose up -d
```

5. **Setup Nginx Reverse Proxy (Recommended):**
```bash
sudo apt update
sudo apt install nginx certbot python3-certbot-nginx

# Create nginx config
sudo nano /etc/nginx/sites-available/evolveiq
```

Nginx configuration:
```nginx
# Frontend
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Backend API
server {
    listen 80;
    server_name api.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

6. **Enable HTTPS (SSL):**
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com -d api.yourdomain.com
```

### 4. Setup DNS

Point your domain to your server:

**A Record:**
```
yourdomain.com     → Your server IP
www.yourdomain.com → Your server IP
api.yourdomain.com → Your server IP
```

**Or CNAME (for cloud platforms):**
```
yourdomain.com     → your-app.railway.app
api.yourdomain.com → your-api.railway.app
```

### 5. Security Checklist

✅ **Before going public:**

1. **Change default passwords:**
   - Database password
   - Remove test users or change passwords

2. **Enable HTTPS:**
   - Use Let's Encrypt (free SSL)
   - Force HTTPS redirects

3. **Update CORS:**
   - Only allow your domain
   - Remove localhost in production

4. **Environment Variables:**
   - Never commit `.env` to git
   - Use secure secret management

5. **Database Security:**
   - Don't expose database port (5432) publicly
   - Use strong passwords
   - Enable SSL connections

6. **Rate Limiting:**
   - Add rate limiting to API endpoints
   - Prevent abuse

7. **Firewall:**
   - Only open necessary ports
   - Block direct database access

## Quick Deployment Scripts

### Update for Public Deployment

Create `deploy-public.sh`:

```bash
#!/bin/bash

# Set your domain
DOMAIN="yourdomain.com"
API_DOMAIN="api.yourdomain.com"

# Update CORS in api.py (manual step)
echo "1. Update CORS in api.py to include: https://$DOMAIN"

# Update docker-compose.yml
sed -i "s|VITE_API_BASE_URL=http://localhost:8000|VITE_API_BASE_URL=https://$API_DOMAIN|g" docker-compose.yml

# Rebuild and deploy
docker compose build
docker compose up -d

echo "Deployment complete! Update DNS to point to this server."
```

## Environment Variables for Production

Create `.env.production`:

```bash
# Domain Configuration
FRONTEND_URL=https://yourdomain.com
API_URL=https://api.yourdomain.com
VITE_API_BASE_URL=https://api.yourdomain.com

# Database (Docker PostgreSQL)
USE_SUPABASE=false
DB_HOST=database
DB_PORT=5432
DB_NAME=evolveiq_db
DB_USER=evolveiq
DB_PASSWORD=your_strong_password_here

# API Keys
OPENAI_API_KEY=your_key
TAVILY_API_KEY=your_key
SUPABASE_URL=your_url
SUPABASE_KEY=your_key

# Security
NODE_ENV=production
PYTHON_ENV=production
```

## Monitoring & Maintenance

### Health Checks

Monitor your services:
```bash
# Check container status
docker compose ps

# View logs
docker compose logs -f

# Check API health
curl https://api.yourdomain.com/api/health
```

### Backup Database

```bash
# Backup
docker exec evolveiq-database pg_dump -U evolveiq evolveiq_db > backup.sql

# Restore
docker exec -i evolveiq-database psql -U evolveiq evolveiq_db < backup.sql
```

### Update Application

```bash
git pull
docker compose build
docker compose up -d
```

## Troubleshooting

### CORS Errors
- Check `api.py` CORS settings
- Verify domain is in `allow_origins`
- Check browser console for exact error

### API Connection Failed
- Verify `VITE_API_BASE_URL` is correct
- Check backend is accessible
- Verify firewall rules

### Database Connection Issues
- Ensure database is not exposed publicly
- Check network connectivity between containers
- Verify credentials in `.env`

## Cost Estimates

**Budget Option (VPS):**
- DigitalOcean Droplet: $6/month
- Domain: $10-15/year
- **Total: ~$7-8/month**

**Managed Platform:**
- Railway: $5-20/month
- Render: $7-25/month
- Fly.io: $5-15/month

**Enterprise:**
- AWS/GCP/Azure: $20-100+/month
- Depends on traffic and resources

## Next Steps

1. Choose your deployment platform
2. Update configuration files
3. Deploy and test
4. Setup domain and SSL
5. Monitor and maintain

For platform-specific help, check their documentation or ask for assistance!

