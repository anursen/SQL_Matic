import { useChatStore } from '../store';
import { getSessionId, createNewSession } from '../utils/sessionManager';
import { logger } from '../utils/logger';

class WebSocketService {
  private socket: WebSocket | null = null;
  private sessionId: string | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  
  // Get the appropriate WebSocket URL based on the environment
  private getWebSocketUrl(): string {
    const isProd = process.env.NODE_ENV === 'production';
    const baseUrl = isProd 
      ? 'wss://chat-app-backend.azurewebsites.net' 
      : 'ws://localhost:8000';
    
    return `${baseUrl}/ws/chat`;
  }
  
  connect() {
    if (this.socket) {
      logger.info('WebSocket already connected');
      return;
    }
    
    // Get or create a session ID
    this.sessionId = getSessionId();
    if (!this.sessionId) {
      this.sessionId = createNewSession();
      logger.info('Created new session: %s', this.sessionId);
    } else {
      logger.info('Using existing session: %s', this.sessionId);
    }
    
    const wsUrl = `${this.getWebSocketUrl()}?session_id=${this.sessionId}`;
    logger.info('Connecting to WebSocket: %s', wsUrl);
    
    try {
      this.socket = new WebSocket(wsUrl);
      
      this.socket.onopen = () => {
        logger.info('WebSocket connection established');
        this.reconnectAttempts = 0;
      };
      
      this.socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          logger.debug('WebSocket message received: %j', data);
          
          if (data.type === 'ai_response') {
            useChatStore.getState().addMessage({
              id: Date.now().toString(),
              content: data.content,
              sender: 'ai',
              timestamp: Date.now(),
            });
          }
          
          if (data.type === 'backend_status') {
            useChatStore.getState().updateBackendStatus(data.metrics);
          }
        } catch (error) {
          logger.error('Error parsing WebSocket message: %s', error);
        }
      };
      
      this.socket.onerror = (error) => {
        logger.error('WebSocket error: %j', error);
      };
      
      this.socket.onclose = () => {
        logger.warn('WebSocket connection closed');
        this.socket = null;
        
        // Attempt to reconnect if we haven't exceeded max attempts
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
          this.reconnectAttempts++;
          const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
          logger.info('Attempting to reconnect in %d ms (attempt %d/%d)', 
                     delay, this.reconnectAttempts, this.maxReconnectAttempts);
          setTimeout(() => this.connect(), delay);
        } else {
          logger.error('Max reconnection attempts reached. Please refresh the page.');
        }
      };
    } catch (error) {
      logger.error('Failed to create WebSocket connection: %s', error);
    }
  }
  
  getCurrentSession(): string | null {
    return this.sessionId;
  }
  
  startNewSession(): string {
    // Close existing connection if any
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
    
    // Create a new session
    this.sessionId = createNewSession();
    logger.info('Started new session: %s', this.sessionId);
    
    // Connect with the new session
    this.connect();
    
    return this.sessionId;
  }
  
  sendMessage(message: string): void {
    if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
      logger.warn('WebSocket not connected, attempting to reconnect...');
      this.connect();
      setTimeout(() => this.sendMessage(message), 1000);
      return;
    }
    
    try {
      logger.debug('Sending message via WebSocket: %s', message);
      this.socket.send(JSON.stringify({
        message,
        sessionId: this.sessionId
      }));
    } catch (error) {
      logger.error('Error sending message: %s', error);
    }
  }
}

export const wsService = new WebSocketService();
