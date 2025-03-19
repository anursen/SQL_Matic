import create from 'zustand';
import { Chat, Message, BackendMetrics } from '../types';

interface ChatStore {
  chats: Chat[];
  currentChat: Chat | null;
  metrics: BackendMetrics;
  setChats: (chats: Chat[]) => void;
  setCurrentChat: (chat: Chat) => void;
  addMessage: (message: Message) => void;
  updateMetrics: (metrics: BackendMetrics) => void;
}

export const useChatStore = create<ChatStore>((set) => ({
  chats: [],
  currentChat: null,
  metrics: {
    toolUsage: [],
    tokenCost: 0,
    inferenceSpeed: 0
  },
  setChats: (chats) => set({ chats }),
  setCurrentChat: (chat) => set({ currentChat: chat }),
  addMessage: (message) => set((state) => ({
    currentChat: state.currentChat
      ? {
          ...state.currentChat,
          messages: [...state.currentChat.messages, message]
        }
      : null
  })),
  updateMetrics: (metrics) => set({ metrics })
}));
