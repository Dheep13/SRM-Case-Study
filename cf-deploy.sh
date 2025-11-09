#!/bin/bash
# Cloud Foundry Deployment Script

echo "🚀 Deploying EvolveIQ to Cloud Foundry..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if CF CLI is installed
if ! command -v cf &> /dev/null; then
    echo "❌ Cloud Foundry CLI not found. Install from: https://github.com/cloudfoundry/cli/releases"
    exit 1
fi

# Check if logged in
if ! cf target &> /dev/null; then
    echo "⚠️  Not logged in to Cloud Foundry. Please run: cf login"
    exit 1
fi

echo -e "${GREEN}✓${NC} Cloud Foundry CLI found and logged in"

# Get API URL from backend manifest
API_URL=$(grep -A 1 "routes:" manifest-backend.yml | grep "route:" | awk '{print $2}' | head -1)
FRONTEND_URL=$(grep -A 1 "routes:" frontend/manifest-frontend.yml | grep "route:" | awk '{print $2}' | head -1)

if [ -z "$API_URL" ]; then
    echo "⚠️  Could not determine API URL from manifest. Using default."
    API_URL="https://evolveiq-api.cfapps.us10-001.hana.ondemand.com"
fi

echo -e "${YELLOW}Using API URL: ${API_URL}${NC}"

# Step 1: Build Frontend with API URL
echo ""
echo "📦 Building frontend..."
cd frontend
npm install
VITE_API_BASE_URL=$API_URL npm run build

if [ ! -d "dist" ]; then
    echo "❌ Frontend build failed. dist/ directory not found."
    exit 1
fi

echo -e "${GREEN}✓${NC} Frontend built successfully"

# Step 2: Deploy Backend
echo ""
echo "🚀 Deploying backend..."
cd ..
cf push -f manifest-backend.yml

if [ $? -ne 0 ]; then
    echo "❌ Backend deployment failed"
    exit 1
fi

echo -e "${GREEN}✓${NC} Backend deployed"

# Step 3: Set CORS for backend
echo ""
echo "🔧 Setting CORS origins..."
cf set-env evolveiq-api CORS_ORIGINS "https://${FRONTEND_URL#https://},https://www.${FRONTEND_URL#https://}"

# Step 4: Deploy Frontend
echo ""
echo "🚀 Deploying frontend..."
cd frontend
cf push -f manifest-frontend.yml

if [ $? -ne 0 ]; then
    echo "❌ Frontend deployment failed"
    exit 1
fi

echo -e "${GREEN}✓${NC} Frontend deployed"

# Step 5: Restage backend to apply CORS changes
echo ""
echo "🔄 Restaging backend to apply CORS changes..."
cf restage evolveiq-api

echo ""
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""
echo "Frontend: https://${FRONTEND_URL#https://}"
echo "Backend API: ${API_URL}"
echo ""
echo "⚠️  Don't forget to set environment variables:"
echo "   cf set-env evolveiq-api OPENAI_API_KEY your_key"
echo "   cf set-env evolveiq-api SUPABASE_URL your_url"
echo "   cf set-env evolveiq-api SUPABASE_KEY your_key"
echo "   cf restage evolveiq-api"

