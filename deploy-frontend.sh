#!/bin/bash

# First, build the React app
cd frontend
npm install
npm run build
cd ..

# Login to Azure
az login

# Create Static Web App
az staticwebapp create \
  --name "chat-app-frontend" \
  --resource-group "chat-app-resource-group" \
  --location "eastus2" \
  --source "frontend" \
  --app-location "/" \
  --output-location "dist" \
  --login-with-github

# Note: The above command will open a browser for GitHub authentication
# After authentication, select your repository to connect it

echo "Frontend deployed. Visit https://chat-app-frontend.azurestaticapps.net when the deployment is complete."
