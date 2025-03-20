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
def get_schema(max_tables: str) -> Dict:
    '''
    Get the schema of the database.
    Args:
        max_tables (str): put 'get_all' string to get all tables.

    Returns:
        Dict: A dictionary containing the schema information or an error message.
    Example:
        get_schema('get_all')

    '''
    print(f"[TOOL] get_schema {max_tables}")

    database_config = config.database_config
    tool_config = config.tool_get_schema
    db_type = database_config.get('type', 'sqlite')
    
    getter = SQLiteSchemaGetter(
                db_path=database_config.get('default_path'),
                config=tool_config
            )

            
    schema_info = getter.get_schema()
    return {
        "Tool Message: >>> ": f"Schema retrieved successfully for {db_type} database.",
            "schema": schema_info
        }
        

if __name__ == "__main__":
    result = get_schema('get_all')
    print(result)
