import sqlite3
from pathlib import Path
from langchain_core.tools import tool
import sys
import json
import csv
from io import StringIO

# Add the project root to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from config import config

@tool
def execute_sql_query(query: str,max_results:int=None) -> dict:
    '''
    Execute SQL queries on SQLite database with result limits.
    Args:
        query(str): The SQL query to execute
        max_results(int): Maximum number of results to return (default is 100) 
    Returns:
        dict: Contains:
            - message: Summary of results
            - row_count: Number of rows
            - columns: Column names
            - results: Query results
            - format: Result format
            - error: Error message if failed
    '''
    try:
        print(f"[TOOL] execute_sql_query {query}")
        # Get configuration
        
        tool_config = config.tool_execute_sql
        database_config = config.database_config
        if max_results is None:
            max_results = tool_config.get('max_results', 100)
        return_format = tool_config.get('return_format', 'json')
        db_path = database_config.get('default_path', 'database.db')
            
        with sqlite3.connect(str(db_path)) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            
            # Get column names
            column_names = [description[0] for description in cursor.description] if cursor.description else []
            
            # Fetch limited results
            results = cursor.fetchall()
            limited_results = results[:max_results]
            
            # Format results according to return_format
            formatted_data = None
            if return_format.lower() == 'json':
                formatted_data = [dict(zip(column_names, row)) for row in limited_results]
            elif return_format.lower() == 'csv':
                output = StringIO()
                csv_writer = csv.writer(output)
                csv_writer.writerow(column_names)
                csv_writer.writerows(limited_results)
                formatted_data = output.getvalue()
            elif return_format.lower() == 'list':
                formatted_data = limited_results
            else:
                formatted_data = limited_results
            
            return {
                "message": f"{len(results)} results found (limited to {max_results})",
                "row_count": len(limited_results),
                "columns": column_names,
                "results": formatted_data,
                "format": return_format
            }
            
    except Exception as e:
        return {"error": str(e)}

def main():
    """Interactive test function for SQL query execution"""
    print("SQL Query Executor")
    print("----------------")
    print("Enter 'exit' to quit\n")
    
    while True:
        query = input("Enter SQL query: ").strip()
        if query.lower() == 'exit':
            break
            
        result = execute_sql_query(query)
        print("\nResults:")
        print(result)
if __name__ == "__main__":
    main()
