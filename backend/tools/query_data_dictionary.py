import pandas as pd
import sys
from pathlib import Path
from langchain_core.tools import tool


# Add the project root to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))


@tool
def get_db_field_definition(column_name: str):
    '''
    Get the definition of a database field from the simplified data dictionary.
    Args:
        column_name (str): The name of the database field to search for.
    Returns:
        dict: A dictionary containing the field definition or an error message.
    Example:
        get_db_field_definition("ACCT_ID")
        # Returns:
        {
            "Tool Message: >>> ": "1 results found:",
            "results": [
                {
                    "domain": "Account",
                    "table": "CI_ACCT",
                    "column": "ACCT_ID",
                    "key_type": "PK",
                    "description": "Primary identifier for customer accounts"
                }
            ]
        }
    '''
    print(f"[TOOL][Api call] => get_db_field_definition({column_name})")

    # Use the simplified data dictionary path
    simplified_dict_path = Path(__file__).resolve().parent.parent / "files" / "simplified_data_dictionary_with_keys.csv"
    
    try:
        # Read the simplified data dictionary
        df = pd.read_csv(simplified_dict_path)
        
        # Filter data by Column name
        filtered_df = df[df['Column'].str.contains(column_name, case=False, na=False)]
        
        if filtered_df.empty:
            return {"error": f"Field '{column_name}' not found in data dictionary"}
        
        # Return all matching fields with their descriptions
        results = filtered_df.to_dict('records')
        return {
            "Tool Message: >>> ": f"{len(results)} results found:",
            "row_count": len(results),
            "columns": ["Domain", "Table", "Column", "Key_Type", "Description"],
            "results": results
        }
    except Exception as e:
        return {"error": f"Error reading data dictionary: {str(e)}"}


if __name__ == "__main__":
    # Get column name from user input
    test_column = input("Enter column name to search (e.g. ACCT_ID): ").strip()
    
    print(f"\nSearching for column: {test_column}")
    result = get_db_field_definition(test_column)
    
    if "error" in result:
        print(f"\nError: {result['error']}")
    else:
        print(result)


