#!/bin/bash

# Make scripts executable
chmod +x deploy-backend.sh
chmod +x deploy-frontend.sh
chmod +x backend/startup.sh

echo "=== Deploying Chat App to Azure ==="
echo "1. Installing prerequisites..."

# Check for Azure CLI
if ! command -v az &> /dev/null
then
    echo "Azure CLI not found. Installing..."
    curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
else
    echo "Azure CLI is already installed."
fi

# Login to Azure
echo "2. Logging in to Azure..."
az login

# Create resource group
echo "3. Creating Resource Group..."
az group create --name chat-app-resource-group --location eastus

# Deploy backend
echo "4. Deploying Backend..."
./deploy-backend.sh

# Deploy frontend
echo "5. Deploying Frontend..."
./deploy-frontend.sh

echo "=== Deployment Complete ==="
echo "Backend: https://chat-app-backend.azurewebsites.net"
echo "Frontend: https://chat-app-frontend.azurestaticapps.net"
echo ""
echo "Note: It may take a few minutes for your services to be fully available."
