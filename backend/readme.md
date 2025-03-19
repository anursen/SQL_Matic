# SQL_Matic Backend

## 🚀 Overview

This backend powers the SQL_Matic application by:

- **Processing natural language queries** into SQL statements
- **Handling WebSocket communication** for real-time messaging
- **Executing SQL queries** against a SQLite database
- **Providing database schema information** for frontend visualization
- **Tracking tool usage and metrics** during query processing

## 📌 Tech Stack

- **Backend Framework:** FastAPI (Python)
- **Real-time Communication:** WebSockets
- **Database:** SQLite (Chinook sample database)
- **AI Integration:** LangChain with OpenAI models
- **Orchestration:** LangGraph for tool execution flow
- **Configuration:** YAML-based with environment variable support

## 🛠️ Key Components

### SQL Tools

- **execute_sql_query**: Executes SQL queries against the database with configurable result limits
- **get_schema**: Retrieves database structure including tables, columns, and relationships
- **get_db_field_definition**: Gets field definitions from the data dictionary

### AI Assistant

The `SQLQueryAssistant` class orchestrates:
- LLM initialization with appropriate configuration
- Tool binding for SQL operations
- LangGraph setup for message processing flow
- Session management for persistent conversations

## 🔌 API Implementation

### WebSocket Endpoint

The main communication channel with the frontend:

```python
@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # Extract or generate session_id
    query_params = dict(websocket.query_params)
    session_id = query_params.get('session_id') or str(uuid.uuid4())
    
    try:
        while True:
            # Receive user message
            data = await websocket.receive_json()
            message = data.get('message', '')
            
            # Process with AI assistant
            response = await assistant.process_query(message, session_id)
            
            # Send response back to client
            await websocket.send_json({
                "type": "ai_response",
                "content": response,
                "sessionId": session_id
            })
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()
```

### REST Endpoints

- `GET /schema` → Retrieve database structure for visualization
- `GET /config` → Get the current application configuration
- `POST /config` → Update application configuration

## 📦 Project Structure

```
backend/
│── agents/                  # AI assistant implementation
│   ├── sql_matic.py         # Main assistant class
│   └── __init__.py
│── tools/                   # SQL operation tools
│   ├── execute_sql.py       # SQL query execution tool
│   ├── get_schema.py        # Database schema extraction tool
│   ├── query_data_dictionary.py # Data dictionary lookup tool
│   ├── schema_getters.py    # Schema extraction utilities
│   └── __init__.py
│── app.py                   # FastAPI application entry point
│── config.py                # Configuration management
│── config.yaml              # Application configuration
│── chinook_db_creator.py    # Sample database setup
│── evaluation_service.py    # SQL query accuracy evaluation
│── main.py                  # CLI interface for testing
└── requirements.txt         # Python dependencies
```

## 🔍 Configuration

The application uses a layered configuration approach:

1. **Default settings** in `config.yaml`
2. **Environment variables** for sensitive information
3. **Runtime configuration** via the `/config` endpoint

## 📊 Evaluation

The `SQLEvaluationService` class provides:
- Evaluation of SQL generation quality against ground truth examples
- Cosine similarity measurement between generated and expected SQL
- Detailed reporting of successes and failures

## 🚀 Getting Started

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ENVIRONMENT=development
   ```

4. Set up the sample database:
   ```bash
   python chinook_db_creator.py
   ```

5. Start the server:
   ```bash
   python app.py
   ```

The server will be available at `http://localhost:8000` with WebSocket endpoint at `ws://localhost:8000/ws/chat`.
