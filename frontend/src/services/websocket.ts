import { io, Socket } from 'socket.io-client';
import { useChatStore } from '../store';

class WebSocketService {
  private socket: Socket | null = null;
  private readonly SOCKET_URL = 'ws://localhost:8000/ws/chat';

  connect() {
    this.socket = io(this.SOCKET_URL);

    this.socket.on('connect', () => {
      console.log('Connected to WebSocket server');
    });

    this.socket.on('ai_response', (data) => {
      useChatStore.getState().addMessage({
        id: Date.now().toString(),
        content: data.message,
        sender: 'ai',
        timestamp: Date.now(),
      });
    });

    this.socket.on('backend_status', (status) => {
      useChatStore.getState().updateBackendStatus(status);
    });
  }

  sendMessage(message: string) {
    if (!this.socket) return;
    this.socket.emit('user_message', { message });
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }
}

export const wsService = new WebSocketService();
