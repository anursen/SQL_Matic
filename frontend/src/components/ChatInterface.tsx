import React, { useState, useRef, useEffect } from 'react';
import { useChatStore } from '../store';
import { wsService } from '../services/websocket';
import { getSessionHistory, renameSession } from '../utils/sessionManager';

const ChatInterface: React.FC = () => {
  const [input, setInput] = useState('');
  const messages = useChatStore((state) => state.messages);
  const addMessage = useChatStore((state) => state.addMessage);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [currentSession, setCurrentSession] = useState<string | null>(null);

  useEffect(() => {
    // Get current session when component mounts
    setCurrentSession(wsService.getCurrentSession());
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const message = {
      id: Date.now().toString(),
      content: input,
      sender: 'user' as const,
      timestamp: Date.now(),
    };

    addMessage(message);
    wsService.sendMessage(input);
    setInput('');
  };

  const handleNewSession = () => {
    // Clear messages in store
    useChatStore.getState().clearMessages();
    
    // Start a new WebSocket session
    const newSessionId = wsService.startNewSession();
    setCurrentSession(newSessionId);
  };

  return (
    <div className="flex flex-col h-full bg-gray-50">
      {/* Header area */}
      <div className="bg-white p-2 border-b flex justify-between items-center">
        <div className="text-sm text-gray-500">
          {currentSession ? `Session: ${currentSession.substring(0, 8)}...` : 'No active session'}
        </div>
        <button
          onClick={handleNewSession}
          className="px-3 py-1 bg-blue-500 text-white text-sm rounded hover:bg-blue-600"
        >
          New Session
        </button>
      </div>
      
      {/* Messages area with fixed constraints to prevent overflow */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4" style={{ maxHeight: 'calc(100vh - 150px)' }}>
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[70%] p-3 rounded-2xl ${
                msg.sender === 'user'
                  ? 'bg-blue-600 text-white rounded-br-none'
                  : 'bg-white shadow-md rounded-bl-none'
              }`}
            >
              <p className="text-sm">{msg.content}</p>
              <span className={`text-xs mt-1 block ${msg.sender === 'user' ? 'text-blue-100' : 'text-gray-400'}`}>
                {new Date(msg.timestamp).toLocaleTimeString()}
              </span>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      
      {/* Input area with fixed height */}
      <form onSubmit={handleSubmit} className="p-4 bg-white border-t shadow-lg" style={{ minHeight: '80px' }}>
        <div className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="flex-1 p-3 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Type your message..."
          />
          <button
            type="submit"
            className="px-6 py-3 bg-blue-600 text-white rounded-full hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
          >
            Send
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatInterface;
