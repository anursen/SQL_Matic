import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'
import { wsService } from './services/websocket'

// Initialize WebSocket connection
wsService.connect();

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
