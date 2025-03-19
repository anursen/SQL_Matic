#!/bin/bash

# Login to Azure
az login

# Create resource group if not exists
az group create --name chat-app-resource-group --location eastus

# Create app service plan for backend
az appservice plan create --name chat-app-backend-plan --resource-group chat-app-resource-group --sku B1 --is-linux

# Create web app for backend with Python
az webapp create --name chat-app-backend --resource-group chat-app-resource-group --plan chat-app-backend-plan --runtime "PYTHON|3.9"

# Set startup command for the app
az webapp config set --name chat-app-backend --resource-group chat-app-resource-group --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 --workers 4 app:app"

# Configure environment variables
az webapp config appsettings set --name chat-app-backend --resource-group chat-app-resource-group --settings \
  OPENAI_API_KEY="your_api_key_here" \
  ENVIRONMENT="production" \
  WEBSITE_HTTPLOGGING_RETENTION_DAYS=3 \
  SCM_DO_BUILD_DURING_DEPLOYMENT=true

# Enable WebSocket support
az webapp config set --name chat-app-backend --resource-group chat-app-resource-group --web-sockets-enabled true

# Deploy the code (from local directory)
cd backend && zip -r ../backend.zip * && cd ..
az webapp deployment source config-zip --src backend.zip --name chat-app-backend --resource-group chat-app-resource-group

echo "Backend deployed to: https://chat-app-backend.azurewebsites.net"
