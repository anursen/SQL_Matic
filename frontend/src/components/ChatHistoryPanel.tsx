import React from 'react';

const ChatHistoryPanel: React.FC = () => {
  return (
    <div className="h-full bg-gray-50 p-6 overflow-y-auto" style={{ maxHeight: 'calc(100vh - 120px)' }}>
      <h2 className="text-xl font-semibold text-gray-800 mb-6">Chat History(V2)</h2>
      <div className="space-y-3">
        <div className="p-4 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow cursor-pointer border border-gray-100">
          <h3 className="font-medium text-gray-800 mb-1">Database Query Chat</h3>
          <p className="text-sm text-gray-500">Last message: 2 hours ago</p>
        </div>
        <div className="p-4 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow cursor-pointer border border-gray-100">
          <h3 className="font-medium text-gray-800 mb-1">Schema Analysis</h3>
          <p className="text-sm text-gray-500">Last message: 5 hours ago</p>
        </div>
        <div className="p-4 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow cursor-pointer border border-gray-100">
          <h3 className="font-medium text-gray-800 mb-1">Data Exploration</h3>
          <p className="text-sm text-gray-500">Last message: 1 day ago</p>
        </div>
      </div>
    </div>
  );
};

export default ChatHistoryPanel;
