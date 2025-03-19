import React from 'react';

const ChatHistoryPanel: React.FC = () => {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Chat History</h2>
      <div className="space-y-2">
        {/* Placeholder for chat history */}
        <div className="p-2 bg-gray-100 rounded cursor-pointer hover:bg-gray-200">
          Previous Chat 1
        </div>
        <div className="p-2 bg-gray-100 rounded cursor-pointer hover:bg-gray-200">
          Previous Chat 2
        </div>
      </div>
    </div>
  );
};

export default ChatHistoryPanel;
