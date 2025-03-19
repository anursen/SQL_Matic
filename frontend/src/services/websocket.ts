import { useChatStore } from '../store';
import { getSessionId, createNewSession } from '../utils/sessionManager';

class WebSocketService {
  private socket: WebSocket | null = null;
  private readonly SOCKET_URL = 'ws://localhost:8000/ws/chat';
  private sessionId: string | null = null;

  connect() {
    if (this.socket) {
      return;
    }

    // Get existing session ID or create a new one
    this.sessionId = getSessionId();
    if (!this.sessionId) {
      this.sessionId = createNewSession();
    }
    
    // Add session ID to WebSocket URL
    const wsUrl = `${this.SOCKET_URL}?session_id=${this.sessionId}`;
    this.socket = new WebSocket(wsUrl);

    this.socket.onopen = () => {
      console.log(`Connected to WebSocket server with session: ${this.sessionId}`);
    };

    this.socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'ai_response') {
          useChatStore.getState().addMessage({
            id: Date.now().toString(),
            content: data.content,
            sender: 'ai',
            timestamp: Date.now(),
          });
        }
      } catch (error) {
        console.error('Error parsing message:', error);
      }
    };

    this.socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    this.socket.onclose = () => {
      console.log('WebSocket connection closed');
      this.socket = null;
      // Attempt to reconnect after 5 seconds
      setTimeout(() => this.connect(), 5000);
    };
  }

  sendMessage(message: string) {
    if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
      console.error('WebSocket is not connected');
      return;
    }
    // Include session ID with each message
    this.socket.send(JSON.stringify({ 
      message,
      sessionId: this.sessionId 
    }));
  }

  // Create a method to start a new session
  startNewSession() {
    this.sessionId = createNewSession();
    // Reconnect with new session
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
    this.connect();
    return this.sessionId;
  }

  // Get current session ID
  getCurrentSession() {
    return this.sessionId;
  }

  disconnect() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }
}

export const wsService = new WebSocketService();
