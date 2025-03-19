
🚀 Overview
This is a React-based real-time chat application designed to integrate with an AI assistant backend via WebSockets. The app follows a three-panel layout:

Left Panel (Chat History): Displays and categorizes past conversations.
Middle Panel (Chat Interface): User input, AI responses, and message history.
Right Panel (Live Backend Updates): Shows real-time updates from the backend, such as:
LLM tool usage
Token cost
Inference speed
Any other backend events
🎯 Key Features
✅ Real-time communication using WebSockets for instant AI responses.
✅ Persistent chat history, categorized for easy access.
✅ Live backend monitoring, displaying token usage, processing speed, and other metrics.
✅ Interactive UI with a modern, responsive design.

📌 Tech Stack
Frontend: React + TypeScript
State Management: Zustand (or Redux if needed)
Styling: Tailwind CSS + Shadcn (for UI components)
Real-time Communication: WebSockets (socket.io-client)
Backend API Communication: REST (for fetching history) + WebSockets (for live chat)
🏗️ Component Breakdown
1️⃣ ChatHistoryPanel.tsx (Left Panel - Past Chats)
Displays a list of past conversations, categorized for easy navigation.
Uses REST API to fetch chat history (GET /chats).
Allows clicking on a past chat to reload previous messages.
2️⃣ ChatInterface.tsx (Middle Panel - Live Chat)
Main chat area where users interact with the AI.
Input field + "Send" button to send messages.
Uses WebSockets to send user messages to the backend and receive AI responses.
Displays chat history dynamically as messages are exchanged.
3️⃣ BackendUpdatesPanel.tsx (Right Panel - Live Updates)
Displays real-time data from the backend, such as:
🔥 LLM tool usage (which tools are being used)
💰 Token cost tracking
⚡ Inference speed updates
Uses WebSockets to listen for backend updates.
🔌 WebSocket Implementation
The app will use WebSockets to enable low-latency, real-time updates for both chat messages and backend analytics.

WebSocket Flow:
User sends a message → Frontend sends a WebSocket event ("user_message") to the backend.
Backend processes message → Calls LLM, retrieves response.
Backend emits a response → Sends "ai_response" event with AI’s reply.
Backend also emits analytics → Sends "backend_status" event with live metrics.
Frontend updates UI in real-time when messages and analytics arrive.
Example WebSocket Events:
tsx
Copy
Edit
// Send message to backend
socket.emit("user_message", { message: userInput });

// Listen for AI response
socket.on("ai_response", (data) => {
  updateChatHistory(data.message);
});

// Listen for backend updates
socket.on("backend_status", (status) => {
  updateBackendMetrics(status);
});
📡 API Endpoints
REST API (Used for Fetching Data)
GET /chats → Fetch past chat history.
GET /chat/{id} → Load a specific chat session.
WebSocket Events (Used for Real-Time Updates)
Event Name	Direction	Description
user_message	→ Backend	Sends user message to AI
ai_response	← Frontend	AI sends a response message
backend_status	← Frontend	Sends live analytics like token usage & inference speed
chat_history	← Frontend	Returns chat history updates
🎨 UI Layout (Grid-based Design)
tsx
Copy
Edit
<div className="grid grid-cols-12 h-screen">
  {/* Left Panel - Chat History */}
  <div className="col-span-3 border-r p-4 overflow-y-auto">
    <ChatHistoryPanel />
  </div>

  {/* Middle Panel - Chat Interface */}
  <div className="col-span-6 flex flex-col">
    <ChatInterface />
  </div>

  {/* Right Panel - Backend Updates */}
  <div className="col-span-3 border-l p-4">
    <BackendUpdatesPanel />
  </div>
</div>
🛠️ Next Steps
 Set up WebSocket connection in React.
 Create initial UI components with Tailwind.
 Integrate WebSocket events into the frontend.
 Build a mock backend to test real-time updates.
