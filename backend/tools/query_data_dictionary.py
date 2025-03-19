import pandas as pd
import sys
from pathlib import Path
from langchain_core.tools import tool


# Add the project root to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from config import config


@tool
def get_db_field_definition(column_name: str):
    '''
    Get the definition of a database field from a data dictionary.
    Args:
        column_name (str): The name of the database field to search for.
    Returns:
        dict: A dictionary containing the field definition or an error message.
    Example:
        get_db_field_definition("customer_id")
        # Returns:
        {
            "Tool Message: >>> ": "1 results found:",
            "results": [
                {
                    "column_name": "customer_id",
                    "data_type": "INTEGER",
                    "description": "Unique identifier for a customer"
                }
            ]
        }
    '''
    print(f"[TOOL][Api call] => get_db_field_definition({column_name})")

    tool_config = config.tool_get_data_dictionary
    file_path = tool_config['file_path']
    filter_column = tool_config['filter_column']
    return_columns = tool_config['return_columns']
    max_results = tool_config.get('max_results', 5)  # Default to 5 if not specified
    
    # Read file based on extension
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)
    
    # Filter data using the configured filter_column
    filtered_df = df[df[filter_column].str.contains(column_name, case=False, na=False)]
    
    if filtered_df.empty:
        return {"error": f"Field '{column_name}' not found in data dictionary"}
    else:
        # Only return the configured columns and limit results
        filtered_df = filtered_df[return_columns].head(max_results)
        results = filtered_df.to_dict('records')
        return {
            "Tool Message: >>> ": f"{len(results)} results found (limited to {max_results}):",
            "row_count": len(results),
            "columns": return_columns,
            "results": results
        }

if __name__ == "__main__":
    # Get column name from user input
    test_column = input("Enter column name to search (e.g. customer_id): ").strip()
    
    print(f"\nSearching for column: {test_column}")
    result = get_db_field_definition(test_column)
    
    if "error" in result:
        print(f"\nError: {result['error']}")
    else:
        print(result)


