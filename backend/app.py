from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from agents.sql_matic import SQLQueryAssistant
from tools.get_schema import get_schema
from fastapi import Body
import os
from pathlib import Path
import yaml
import uuid
from evaluation_service import SQLEvaluationService
from typing import Optional
from logger import logger
from chinook_db_creator import setup_chinook_db

app = FastAPI()
regular_assistant = SQLQueryAssistant("regular")
evaluator_assistant = SQLQueryAssistant("evaluator")
# Set up CORS for production
allowed_origins = [
    "http://localhost:5173",
    "https://chat-app.azurewebsites.net",  # Update with your actual Azure frontend URL
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
    if (
        isinstance(schema_result, dict)
        and "schema" in schema_result
        and "tables" in schema_result["schema"]
    ):
        tables = schema_result["schema"]["tables"]
        if not tables:
            logger.warning(
                "Database schema returned empty tables array - attempting to recreate database"
            )
            if setup_chinook_db():
                logger.info("Successfully recreated the Chinook database")
                # Try to get schema again after database recreation
                schema_result = get_schema("get_all")
                if (
                    isinstance(schema_result, dict)
                    and "schema" in schema_result
                    and "tables" in schema_result["schema"]
                ):
                    tables = schema_result["schema"]["tables"]
                    logger.info(
                        "Successfully retrieved schema after database recreation"
                    )
            else:
                logger.error("Failed to recreate the Chinook database")
        return {"tables": tables}
    else:
        logger.warning(
            "Schema format unexpected: %s", schema_result
        )  # Using logger instead of print
        # Return an empty array as fallback
        return {"tables": []}


@app.get("/config")
async def get_config():
    """Get the content of the config.yaml file"""
    try:
        config_path = Path(__file__).parent / "config.yaml"
        with open(config_path, "r") as file:
            content = file.read()
        return {"content": content}
    except Exception as e:
        logger.error("Failed to read config file: %s", str(e))
        raise HTTPException(
            status_code=500, detail=f"Failed to read config file: {str(e)}"
        )


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
            raise HTTPException(
                status_code=400, detail=f"Invalid YAML format: {str(e)}"
            )

        # Create backup of current config
        config_path = Path(__file__).parent / "config.yaml"
        backup_path = Path(__file__).parent / "config.yaml.bak"

        if config_path.exists():
            with open(config_path, "r") as original:
                with open(backup_path, "w") as backup:
                    backup.write(original.read())

        # Save new config
        with open(config_path, "w") as file:
            file.write(content)

        logger.info("Configuration updated successfully")
        return {"message": "Configuration updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to update config file: %s", str(e))
        raise HTTPException(
            status_code=500, detail=f"Failed to update config file: {str(e)}"
        )


@app.get("/evaluate")
async def evaluate_assistant_endpoint(num_queries: Optional[int] = None):
    """Run evaluation of SQL assistant against ground truth data"""
    try:
        logger.info("Starting evaluation with num_queries=%s", num_queries)
        eval_service = SQLEvaluationService()
        results = await eval_service.evaluate_assistant(
            evaluator_assistant, num_queries
        )
        logger.info("Evaluation completed. Results: %s", list(results.keys()))
        if "error" in results:
            logger.error("Evaluation error: %s", results["error"])
        return results
    except Exception as e:
        import traceback

        logger.error("Evaluation endpoint error: %s", str(e))
        logger.error("Traceback: %s", traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")


@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # Extract session_id from query parameters or generate new one
    query_params = dict(websocket.query_params)
    session_id = query_params.get("session_id")

    if not session_id:
        # Generate a new session ID if none was provided
        session_id = str(uuid.uuid4())
        logger.info("No session ID provided, generated new ID: %s", session_id)
    else:
        logger.info("Using provided session ID: %s", session_id)

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            message = data.get("message", "")

            # Client might send session_id in the message too
            client_session_id = data.get("sessionId")
            if client_session_id and client_session_id != session_id:
                # Update to use the most recent session ID from client
                session_id = client_session_id
                logger.info("Updated session ID from message: %s", session_id)

            logger.info("Processing message for session %s: %s", session_id, message)

            # Process message with the session ID as thread_id
            response = await regular_assistant.process_query(message, session_id)

            # Send response back to client
            await websocket.send_json(
                {"type": "ai_response", "content": response, "sessionId": session_id}
            )

    except Exception as e:
        logger.error("Error in session %s: %s", session_id, e)
    finally:
        logger.info("WebSocket connection closed for session ID: %s", session_id)
        await websocket.close()


@app.post("/update-db")
async def update_database():
    try:
        from files.create_tables import create_database_from_data_dict

        create_database_from_data_dict()
        return {"status": "success", "message": "Database updated successfully"}
    except Exception as e:
        logger.error("Failed to update database: %s", str(e))
        raise HTTPException(
            status_code=500, detail=f"Failed to update database: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting SQL_Matic backend server")
    uvicorn.run(app, host="0.0.0.0", port=8000)
