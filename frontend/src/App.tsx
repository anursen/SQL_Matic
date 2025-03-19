import React from 'react';
import ChatHistoryPanel from './components/ChatHistoryPanel';
import ChatInterface from './components/ChatInterface';
import BackendUpdatesPanel from './components/BackendUpdatesPanel';

function App() {
  return (
    <div className="grid grid-cols-12 h-screen bg-gray-100">
      <div className="col-span-3 border-r border-gray-200">
        <ChatHistoryPanel />
      </div>
      <div className="col-span-6">
        <ChatInterface />
      </div>
      <div className="col-span-3 border-l border-gray-200">
        <BackendUpdatesPanel />
      </div>
    </div>
  );
}

export default App;
