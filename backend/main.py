from services.agents.old_sql_assistant import SQLQueryAssistant
from tools.get_schema import SchemaAnalyzer
import re
import json
from config import config
from typing import Dict, Any

def validate_query(query: str) -> tuple[bool, str]:
    if not query.strip():
        return False, "Query cannot be empty"
    if len(query) > 1000:
        return False, "Query too long (max 1000 characters)"
    return True, ""

def debug_query(assistant: SQLQueryAssistant, query: str) -> dict:
    print("\nDEBUG MODE:")
    print("1. Analyzing query structure...")
    
    # Check for common SQL injection patterns
    if any(pattern in query.lower() for pattern in ["drop", "delete", "--", ";"]):
        print("⚠️ Warning: Potentially dangerous SQL operations detected")
        proceed = input("Do you want to proceed? (y/n): ").lower()
        if proceed != 'y':
            return {"error": "Query cancelled by user"}
    
    print("2. Generating SQL...")
    result = assistant.process_query(query)
    
    if "error" in result:
        print("\nERROR ANALYSIS:")
        if "no such table" in str(result["error"]):
            print("- Table might not exist in database")
            print("- Available tables: customers, orders, products, etc.")
        elif "syntax error" in str(result["error"]):
            print("- SQL syntax error detected")
            print("- Check query structure") 
    
    return result

def print_menu(debug_mode: bool, sql_only_mode: bool):
    print("\nSQL Query Assistant")
    print("Current Mode:", end=" ")
    if debug_mode:
        print("DEBUG", end=" ")
    if sql_only_mode:
        print("SQL-ONLY", end=" ")
    print("\n")
    print("Options:")
    print("1. Execute query")
    print("2. Toggle debug mode")
    print("3. Toggle SQL-only mode")
    print("4. Show database schema (JSON)")
    print("5. Show readable database schema")
    print("6. Run performance evaluation")
    print("7. Help")
    print("0. Exit")
    print("-" * 50)

def display_evaluation_results(results: Dict[str, Any]):
    print("\nEvaluation Results:")
    print("-" * 50)
    print(f"Total Queries: {results['total_queries']}")
    print(f"Successful Queries: {results['successful_queries']}")
    print(f"Failed Queries: {results['failed_queries']}")
    print(f"Average Similarity: {results['average_similarity']:.2f}")
    
    if results.get('failed_cases'):
        print("\nFailed Cases:")
        print("-" * 50)
        for case in results['failed_cases']:  
            print(f"\nQuery: {case['query']}")
            if 'error' in case:
                print(f"Error: {case['error']}")
            else:
                print(f"Similarity: {case['similarity']:.2f}")
                print(f"Assistant SQL: {case['assistant_sql']}")
                print(f"Ground Truth: {case['ground_truth_sql']}")

def main():
    # Validate API key first
    if not config.openai_api_key:
        print("Error: Please set a valid OpenAI API key in your .env file")
        return
        
    assistant = SQLQueryAssistant()
    analyzer = SchemaAnalyzer()
    debug_mode = False
    sql_only_mode = False
    
    while True:
        try:
            print_menu(debug_mode, sql_only_mode)
            choice = input("Enter option (0-7): ").strip()
            
            if choice == '0':
                print("Exiting...")
                break
            elif choice == '1':
                query = input("\nEnter your question: ").strip()
                # Validate query
                is_valid, error_msg = validate_query(query)
                if not is_valid:
                    print(f"Error: {error_msg}")
                    continue
                
                # Process query based on mode
                if sql_only_mode:
                    result = assistant.process_query(query)
                    print("\nGenerated SQL:")
                    print("-" * 50)
                    print(result.get('sql', 'No SQL generated'))
                else:
                    result = debug_query(assistant, query) if debug_mode else assistant.process_query(query)
                    print("\nResults:")
                    print("-" * 50)
                    if "error" in result:
                        print(f"Error: {result['error']}")
                        if debug_mode:
                            suggestion = input("\nWould you like suggestions to fix this? (y/n): ").lower()
                            if suggestion == 'y':
                                print("\nSuggestions:")
                                print("1. Check table names and column references")
                                print("2. Verify SQL syntax")
                                print("3. Ensure proper data types are used")
                    else:
                        print(f"SQL Query: {result['sql']}")
                        print("\nOutput:")
                        if not result['results']:
                            print("No results found")
                        else:
                            for row in result['results']:
                                print(row)
                        if debug_mode:
                            print("\nQuery Stats:")
                            print(f"- Results returned: {len(result['results'])}")
            elif choice == '2':
                debug_mode = not debug_mode
                print(f"Debug mode {'enabled' if debug_mode else 'disabled'}")
            elif choice == '3':
                sql_only_mode = not sql_only_mode
                print(f"SQL-only mode {'enabled' if sql_only_mode else 'disabled'}")
            elif choice == '4':
                schema = analyzer.get_schema_info(assistant.db_path)
                print("\nDatabase Schema (JSON):")
                print(json.dumps(schema, indent=2))
            elif choice == '5':
                readable_schema = analyzer.get_readable_schema(assistant.db_path)
                print("\nReadable Database Schema:")
                print("-" * 50)
                print(readable_schema)
            elif choice == '6':
                print("\nRunning performance evaluation...")
                print("This may take a while depending on the size of the ground truth dataset.")
                try:
                    results = assistant.evaluate_performance()
                    if "error" in results:
                        print(f"Error: {results['error']}")
                    else:
                        display_evaluation_results(results)
                except Exception as e:
                    print(f"Evaluation failed: {str(e)}")
            elif choice == '7':
                continue
            else:
                print("Invalid option. Please try again.")
                
            input("\nPress Enter to continue...")
                    
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            if debug_mode:
                import traceback
                print("\nFull traceback:")
                print(traceback.format_exc())

if __name__ == "__main__":
    main()
