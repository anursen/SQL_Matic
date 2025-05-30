import React from "react";

const ChatHistoryPanel: React.FC = () => {
  const handleUpdateDatabase = async () => {
    try {
      const response = await fetch("http://localhost:8000/update-db", {
        method: "POST",
      });

      if (!response.ok) {
        throw new Error("Failed to update database");
      }

      const data = await response.json();
      alert(data.message);
    } catch (error) {
      console.error("Error updating database:", error);
      alert("Failed to update database. Please check the console for details.");
    }
  };

  return (
    <div
      className="h-full bg-gray-50 p-6 overflow-y-auto"
      style={{ maxHeight: "calc(100vh - 120px)" }}
    >
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-semibold text-gray-800">
          Chat History(V2)
        </h2>
        <button
          onClick={handleUpdateDatabase}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          Update DB
        </button>
      </div>
      <div className="space-y-3">
        <div className="p-4 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow cursor-pointer border border-gray-100">
          <h3 className="font-medium text-gray-800 mb-1">
            Database Query Chat
          </h3>
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
