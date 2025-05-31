import React, { useState } from "react";
import ChatHistoryPanel from "./components/ChatHistoryPanel";
import ChatInterface from "./components/ChatInterface";
import BackendUpdatesPanel from "./components/BackendUpdatesPanel";
import ConfigEditorPage from "./components/ConfigEditorPage";
import EvaluationPage from "./components/EvaluationPage";
import LogsViewer from "./components/LogsViewer";

function App() {
  const [currentView, setCurrentView] = useState("chat");

  return (
    <div className="grid grid-cols-12 h-screen bg-gray-100 overflow-hidden">
      <div className="col-span-3 border-r border-gray-200 overflow-y-auto">
        <div className="p-4 border-b border-gray-200">
          <nav className="flex flex-col space-y-2">
            <button
              onClick={() => setCurrentView("chat")}
              className={`px-4 py-2 rounded-lg text-left ${
                currentView === "chat"
                  ? "bg-blue-600 text-white"
                  : "bg-white text-gray-700 hover:bg-gray-100"
              }`}
            >
              Chat Interface
            </button>
            <button
              onClick={() => setCurrentView("config")}
              className={`px-4 py-2 rounded-lg text-left ${
                currentView === "config"
                  ? "bg-blue-600 text-white"
                  : "bg-white text-gray-700 hover:bg-gray-100"
              }`}
            >
              Config Editor
            </button>
            <button
              onClick={() => setCurrentView("evaluation")}
              className={`px-4 py-2 rounded-lg text-left ${
                currentView === "evaluation"
                  ? "bg-blue-600 text-white"
                  : "bg-white text-gray-700 hover:bg-gray-100"
              }`}
            >
              SQL Evaluation
            </button>
            <button
              onClick={() => setCurrentView("logs")}
              className={`px-4 py-2 rounded-lg text-left ${
                currentView === "logs"
                  ? "bg-blue-600 text-white"
                  : "bg-white text-gray-700 hover:bg-gray-100"
              }`}
            >
              Application Logs
            </button>
            <button
              onClick={async () => {
                try {
                  const response = await fetch(
                    "http://localhost:8000/update-db",
                    {
                      method: "POST",
                    }
                  );

                  if (!response.ok) {
                    throw new Error("Failed to update database");
                  }

                  const data = await response.json();
                  alert(data.message);
                } catch (error) {
                  console.error("Error updating database:", error);
                  alert(
                    "Failed to update database. Please check the console for details."
                  );
                }
              }}
              className="px-4 py-2 rounded-lg text-left bg-white text-gray-700 hover:bg-gray-100"
            >
              Update DB
            </button>
            <button
              onClick={async () => {
                try {
                  const response = await fetch(
                    "http://localhost:8000/populate-db",
                    {
                      method: "POST",
                    }
                  );

                  if (!response.ok) {
                    throw new Error("Failed to populate database");
                  }

                  const data = await response.json();
                  alert(data.message);
                } catch (error) {
                  console.error("Error populating database:", error);
                  alert(
                    "Failed to populate database. Please check the console for details."
                  );
                }
              }}
              className="px-4 py-2 rounded-lg text-left bg-white text-gray-700 hover:bg-gray-100"
            >
              Populate DB
            </button>
          </nav>
        </div>
        <ChatHistoryPanel />
      </div>

      <div className="col-span-6 flex flex-col overflow-hidden">
        {currentView === "chat" && <ChatInterface />}
        {currentView === "config" && <ConfigEditorPage />}
        {currentView === "evaluation" && <EvaluationPage />}
        {currentView === "logs" && (
          <LogsViewer maxHeight="calc(100vh - 120px)" />
        )}
      </div>

      <div className="col-span-3 border-l border-gray-200 overflow-y-auto">
        <BackendUpdatesPanel />
      </div>
    </div>
  );
}

export default App;
