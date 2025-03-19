from typing import Dict
import sys
from pathlib import Path
from langchain_core.tools import tool

# Add the project root to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from config import config
from tools.schema_getters import SQLiteSchemaGetter, MongoDBSchemaGetter, MySQLSchemaGetter, PostgreSQLSchemaGetter

@tool
def get_schema(max_tables: str) -> Dict:
    '''
    Get the schema of the database.
    Args:
        partial (bool): If True, get a partial schema. Defaults to False.
    Returns:
        Dict: A dictionary containing the schema information or an error message.
    Example:
        get_database_schema(partial=False)
        get_database_schema(partial=True)

    '''
    print(f"[TOOL] get_schema {max_tables}")

    database_config = config.database_config
    tool_config = config.tool_get_schema
    db_type = database_config.get('type', 'sqlite')
    
    try:
        if db_type == 'sqlite':
            getter = SQLiteSchemaGetter(
                db_path=database_config.get('default_path'),
                config=tool_config
            )
        elif db_type == 'mongodb':
            getter = MongoDBSchemaGetter(
                connection_string=database_config.get('connection_string'),
                database_name=database_config.get('database_name'),
                config=tool_config
            )
        elif db_type == 'mysql':
            getter = MySQLSchemaGetter(
                host=database_config.get('host'),
                port=database_config.get('port', 3306),
                user=database_config.get('user'),
                password=database_config.get('password'),
                database=database_config.get('database_name'),
                config=tool_config
            )
        elif db_type == 'postgresql':
            getter = PostgreSQLSchemaGetter(
                host=database_config.get('host'),
                port=database_config.get('port', 5432),
                user=database_config.get('user'),
                password=database_config.get('password'),
                database=database_config.get('database_name'),
                config=tool_config
            )
        else:
            return {"error": f"Unsupported database type: {db_type}"}
            
        schema_info = getter.get_schema()
        return {
            "Tool Message: >>> ": f"Schema retrieved successfully for {db_type} database.",
            "schema": schema_info
        }
        
    except Exception as e:
        return {"error": f"Failed to get database schema: {str(e)}"}

if __name__ == "__main__":
    result = get_schema('get_all')
    print(result)
