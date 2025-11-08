#!/bin/bash

# Cloud Foundry Deployment Script for EvolveIQ Frontend

echo "=========================================="
echo "  EvolveIQ Frontend - Cloud Foundry Deploy"
echo "=========================================="
echo ""

# Check if cf CLI is installed
if ! command -v cf &> /dev/null; then
    echo "Error: Cloud Foundry CLI not found!"
    echo "Please install it from: https://github.com/cloudfoundry/cli#downloads"
    exit 1
fi

# Check if logged in
if ! cf target &> /dev/null; then
    echo "Error: Not logged in to Cloud Foundry!"
    echo "Please run: cf login"
    exit 1
fi

# Build the application
echo "[1/3] Building application..."
npm install
npm run build

if [ $? -ne 0 ]; then
    echo "Error: Build failed!"
    exit 1
fi

# Check if API_BASE_URL is set
if [ -z "$API_BASE_URL" ]; then
    echo "Warning: API_BASE_URL not set!"
    echo "Please set it using: export API_BASE_URL=https://your-api.com/api"
    echo "Or update manifest.yml before deploying"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Deploy to Cloud Foundry
echo ""
echo "[2/3] Deploying to Cloud Foundry..."
cf push

if [ $? -ne 0 ]; then
    echo "Error: Deployment failed!"
    exit 1
fi

# Set environment variables if provided
if [ ! -z "$API_BASE_URL" ]; then
    echo ""
    echo "[3/3] Setting environment variables..."
    cf set-env evolveiq-frontend API_BASE_URL "$API_BASE_URL"
    cf restage evolveiq-frontend
fi

echo ""
echo "=========================================="
echo "  Deployment Complete!"
echo "=========================================="
echo ""
echo "View your app:"
cf apps | grep evolveiq-frontend
echo ""
echo "View logs:"
echo "  cf logs evolveiq-frontend --recent"
echo ""


