# SQL_Matic Frontend

🚀 **Overview**

This is a React-based real-time chat application designed to integrate with an AI assistant backend via WebSockets. The frontend interface for SQL_Matic follows a three-panel layout:

- **Left Panel (Chat History)**: Displays and categorizes past conversations.
- **Middle Panel (Chat Interface)**: User input, AI responses, and message history.
- **Right Panel (Live Backend Updates)**: Shows real-time updates from the backend, such as:
  - LLM tool usage
  - Token cost
  - Inference speed
  - Database schema information

🎯 **Key Features**

✅ Real-time communication using WebSockets for instant AI responses.
✅ Persistent chat history, categorized for easy access.
✅ Live backend monitoring, displaying token usage, processing speed, and other metrics.
✅ Interactive UI with a modern, responsive design.
✅ PDF export functionality for chat conversations.
✅ Configuration editor for system settings.

📌 **Tech Stack**

- **Frontend**: React + TypeScript + Vite
- **State Management**: Zustand
- **Styling**: Tailwind CSS
- **Real-time Communication**: WebSockets
- **PDF Generation**: jsPDF + html2canvas
- **Markdown Rendering**: ReactMarkdown

## Getting Started

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

3. Build for production:
   ```bash
   npm run build
   ```

## Component Structure

1️⃣ **ChatHistoryPanel.tsx** (Left Panel - Past Chats)
- Displays a list of past conversations, categorized for easy navigation.
- Allows clicking on a past chat to reload previous messages.

2️⃣ **ChatInterface.tsx** (Middle Panel - Live Chat)
- Main chat area where users interact with the AI.
- Input field + "Send" button to send messages.
- Uses WebSockets to communicate with the backend.
- Displays chat history dynamically as messages are exchanged.

3️⃣ **BackendUpdatesPanel.tsx** (Right Panel - Live Updates)
- Displays real-time data from the backend, such as:
  - LLM tool usage (which tools are being used)
  - Token cost tracking
  - Inference speed updates
  - Database schema information

4️⃣ **ConfigEditorPage.tsx** (Configuration Editor)
- Provides an interface to edit system configuration settings.
- Changes are saved to the backend config.yaml file.

## WebSocket Implementation

The app uses WebSockets to enable low-latency, real-time updates for both chat messages and backend analytics.

**WebSocket Flow:**
1. User sends a message → Frontend sends a WebSocket event to the backend.
2. Backend processes message → Calls LLM, retrieves response.
3. Backend emits a response → Sends AI's reply.
4. Frontend updates UI in real-time when messages arrive.
