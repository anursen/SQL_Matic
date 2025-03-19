from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from agents.sql_matic import SQLQueryAssistant

app = FastAPI()
assistant = SQLQueryAssistant()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive message from client
            message = await websocket.receive_text()
            print(f"Received message: {message}")
            
            # Process message through SQL assistant
            response = await assistant.process_query(message)
            
            # Send response back to client
            await websocket.send_json({
                "type": "ai_response",
                "content": response
            })
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
