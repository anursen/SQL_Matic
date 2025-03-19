# SQL Chat Assistant

A real-time chat application that helps users query SQL databases through natural language. The application leverages LLM capabilities to interpret user questions, generate SQL queries, and provide results in a user-friendly format.

## 🚀 Overview

This application consists of two main components:
- **Frontend**: A React-based web interface with real-time chat capabilities
- **Backend**: A FastAPI server that processes messages using AI and interacts with SQL databases

The chat interface allows users to ask questions about their data in natural language, and the AI assistant will generate and execute appropriate SQL queries, providing results and explanations.

## ✨ Key Features

- **Real-time AI Chat**: Immediate responses to user queries using WebSockets
- **SQL Query Generation**: Converts natural language to SQL queries
- **Database Schema Visualization**: Displays accessible tables and their structure
- **Configuration Editor**: Built-in editor for adjusting system settings
- **History Management**: Persistent chat history categorized for easy access
- **Live Backend Metrics**: Real-time tracking of token usage, inference speed, and tool usage
- **Markdown Support**: Rich text formatting in AI responses

## 🛠️ Tech Stack

### Frontend
- **Framework**: React with TypeScript
- **State Management**: Zustand
- **Styling**: Tailwind CSS
- **Real-time Communication**: WebSockets
- **Markdown Rendering**: ReactMarkdown

### Backend
- **Framework**: FastAPI (Python)
- **AI Integration**: LangChain with GPT models
- **Database**: SQLite (Chinook sample database)
- **Tools**: Custom SQL schema extraction and query execution utilities

## 📋 Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the sample database:
   ```bash
   python chinook_db_creator.py
   ```

5. Start the backend server:
   ```bash
   python app.py
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open the application in your browser at `http://localhost:5173`

## 📚 Project Structure

chat_app/
├── backend/
│   ├── agents/         # LLM-powered SQL assistant
│   ├── tools/          # SQL tools (schema extraction, query execution)
│   ├── app.py          # FastAPI application entry point
│   ├── config.py       # Configuration management
│   └── config.yaml     # Application configuration
│
└── frontend/
    ├── public/         # Static assets
    ├── src/
    │   ├── components/ # React components
    │   ├── services/   # API and WebSocket services
    │   ├── store/      # State management
    │   └── utils/      # Utility functions
    ├── index.html      # HTML entry point
    └── tailwind.config.js  # Tailwind CSS configuration


### 🖥️ Application Views
The application UI consists of:
- **Main Chat Interface - A three-panel layout:
- **Left Panel: Chat history and categories
- **Middle Panel: Active chat with message history and input
- **Right Panel: Database schema and backend metrics
- **Configuration Editor - For adjusting application settings

### ⚙️ Configuration
The application configuration can be modified through the Config Editor page or by directly editing the config.yaml file in the backend directory. Configuration options include:

LLM model selection and parameters
Database connection settings
API settings and rate limiting
Tool configurations for SQL execution and schema extraction