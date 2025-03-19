import React from 'react';
import ChatHistoryPanel from './components/ChatHistoryPanel';
import ChatInterface from './components/ChatInterface';
import BackendUpdatesPanel from './components/BackendUpdatesPanel';

function App() {
  return (
    <div className="grid grid-cols-12 h-screen">
      <div className="col-span-3 border-r p-4 overflow-y-auto">
        <ChatHistoryPanel />
      </div>
      <div className="col-span-6 flex flex-col">
        <ChatInterface />
      </div>
      <div className="col-span-3 border-l p-4">
        <BackendUpdatesPanel />
      </div>
    </div>
  );
}

export default App;
