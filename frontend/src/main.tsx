import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'
import { wsService } from './services/websocket'
import { logger } from './utils/logger'

// Initialize logger
logger.info('Application starting...');

// Initialize WebSocket connection
wsService.connect();

logger.info('WebSocket connection initialized');

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
