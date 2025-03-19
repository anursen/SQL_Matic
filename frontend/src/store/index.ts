import { create } from 'zustand';

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'ai';
  timestamp: number;
}

interface BackendStatus {
  tokenUsage: number;
  inferenceSpeed: number;
  activeTools: string[];
}

interface ChatStore {
  messages: Message[];
  backendStatus: BackendStatus;
  addMessage: (message: Message) => void;
  updateBackendStatus: (status: BackendStatus) => void;
}

export const useChatStore = create<ChatStore>((set) => ({
  messages: [],
  backendStatus: {
    tokenUsage: 0,
    inferenceSpeed: 0,
    activeTools: [],
  },
  addMessage: (message) =>
    set((state) => ({ messages: [...state.messages, message] })),
  updateBackendStatus: (status) =>
    set({ backendStatus: status }),
}));
