from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from agents.sql_matic import SQLQueryAssistant
from tools.get_schema import get_schema
from fastapi import Body
import os
from pathlib import Path
import yaml
import uuid

app = FastAPI()
assistant = SQLQueryAssistant()

# Set up CORS for production
allowed_origins = [
    "http://localhost:5173",
    "https://chat-app.azurewebsites.net"  # Update with your actual Azure frontend URL
]

if os.environ.get("ALLOWED_ORIGINS"):
    allowed_origins.extend(os.environ.get("ALLOWED_ORIGINS").split(","))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/schema")
async def get_database_schema():
    schema_result = get_schema("get_all")
    
    # Extract the actual schema data from the tool response
    if isinstance(schema_result, dict) and "schema" in schema_result and "tables" in schema_result["schema"]:
        tables = schema_result["schema"]["tables"]
        return {"tables": tables}
    else:
        print("Schema format unexpected:", schema_result)  # Debug print
        # Return an empty array as fallback
        return {"tables": []}

@app.get("/config")
async def get_config():
    """Get the content of the config.yaml file"""
    try:
        config_path = Path(__file__).parent / "config.yaml"
        with open(config_path, 'r') as file:
            content = file.read()
        return {"content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read config file: {str(e)}")

@app.post("/config")
async def update_config(data: dict = Body(...)):
    """Update the content of the config.yaml file"""
    try:
        content = data.get("content")
        if not content:
            raise HTTPException(status_code=400, detail="Content field is required")
            
        # Validate YAML before saving
        try:
            yaml.safe_load(content)
        except yaml.YAMLError as e:
            raise HTTPException(status_code=400, detail=f"Invalid YAML format: {str(e)}")
            
        # Create backup of current config
        config_path = Path(__file__).parent / "config.yaml"
        backup_path = Path(__file__).parent / "config.yaml.bak"
        
        if config_path.exists():
            with open(config_path, 'r') as original:
                with open(backup_path, 'w') as backup:
                    backup.write(original.read())
        
        # Save new config
        with open(config_path, 'w') as file:
            file.write(content)
            
        return {"message": "Configuration updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update config file: {str(e)}")

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # Extract session_id from query parameters or generate new one
    query_params = dict(websocket.query_params)
    session_id = query_params.get('session_id')
    
    if not session_id:
        # Generate a new session ID if none was provided
        session_id = str(uuid.uuid4())
        print(f"No session ID provided, generated new ID: {session_id}")
    else:
        print(f"Using provided session ID: {session_id}")
        
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            message = data.get('message', '')
            
            # Client might send session_id in the message too
            client_session_id = data.get('sessionId')
            if client_session_id and client_session_id != session_id:
                # Update to use the most recent session ID from client
                session_id = client_session_id
                print(f"Updated session ID from message: {session_id}")
            
            print(f"Processing message for session {session_id}: {message}")
            
            # Process message with the session ID as thread_id
            response = await assistant.process_query(message, session_id)
            
            # Send response back to client
            await websocket.send_json({
                "type": "ai_response",
                "content": response,
                "sessionId": session_id
            })
            
    except Exception as e:
        print(f"Error in session {session_id}: {e}")
    finally:
        print(f"WebSocket connection closed for session ID: {session_id}")
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
