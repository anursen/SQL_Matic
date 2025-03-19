import { useChatStore } from '../store';

class WebSocketService {
  private socket: WebSocket | null = null;
  private readonly SOCKET_URL = 'ws://localhost:8000/ws/chat';

  connect() {
    if (this.socket) {
      return;
    }

    this.socket = new WebSocket(this.SOCKET_URL);

    this.socket.onopen = () => {
      console.log('Connected to WebSocket server');
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
    this.socket.send(JSON.stringify({ message }));
  }

  disconnect() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }
}

export const wsService = new WebSocketService();
