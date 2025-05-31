from typing import Dict
import sys
from pathlib import Path
from langchain_core.tools import tool

# Add the project root to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from config import config
from tools.schema_getters import SQLiteSchemaGetter


@tool
def get_schema(table_name: str = "all") -> Dict:
    """
    Get the schema of the database.
    Args:
        table_name (str): The name of the table to get the schema for.
        If 'all', retrieves the schema for all tables.

    Returns:
        Dict: A dictionary containing the schema information or an error message.
    Example:
        get_schema('all')
        get_schema('CI_ACCT')
    """
    print(f"[TOOL] get_schema {table_name}")

    database_config = config.database_config
    tool_config = config.tool_get_schema
    db_type = database_config.get("type", "sqlite")

    getter = SQLiteSchemaGetter(
        db_path=database_config.get("default_path"), config=tool_config
    )

    schema_info = getter.get_schema()

    if table_name.lower() != "all":
        # Filter for specific table
        matching_tables = [
            table
            for table in schema_info["tables"]
            if table["name"].lower() == table_name.lower()
        ]

        if not matching_tables:
            return {
                "error": f"Table '{table_name}' not found in the database schema.",
                "available_tables": [table["name"] for table in schema_info["tables"]],
            }

        filtered_schema = {
            "tables": matching_tables,
            "indexes": [
                idx
                for idx in schema_info.get("indexes", [])
                if idx["table"].lower() == table_name.lower()
            ],
        }

        return {
            "Tool Message: >>> ": f"Schema retrieved successfully for table {table_name}",
            "schema": filtered_schema,
        }

    return {
        "Tool Message: >>> ": f"Schema retrieved successfully for {db_type} database.",
        "schema": schema_info,
    }


if __name__ == "__main__":
    result = get_schema("all")
    print(result)
