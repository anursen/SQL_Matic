import { io, Socket } from 'socket.io-client';
import { useChatStore } from '../store/chatStore';

class SocketService {
  private socket: Socket | null = null;

  connect() {
    if (this.socket) return;
    
    this.socket = io('http://localhost:3001', {
      reconnection: true,
      reconnectionAttempts: 5,
      reconnectionDelay: 1000
    });
    
    this.socket.on('connect', () => {
      console.log('Connected to WebSocket server');
    });

    this.socket.on('connect_error', (error) => {
      console.error('Socket connection error:', error);
    });

    this.setupListeners();
  }

  private setupListeners() {
    this.socket?.on('ai_response', ({ message }) => {
      useChatStore.getState().addMessage({
        id: Date.now().toString(),
        content: message,
        sender: 'ai',
        timestamp: new Date()
      });
    });

    this.socket?.on('backend_status', (metrics) => {
      useChatStore.getState().updateMetrics(metrics);
    });
  }

  sendMessage(message: string) {
    if (!this.socket?.connected) {
      console.error('Socket not connected');
      return;
    }
    this.socket.emit('user_message', { message });
  }

  disconnect() {
    this.socket?.disconnect();
  }
}

export const socketService = new SocketService();
