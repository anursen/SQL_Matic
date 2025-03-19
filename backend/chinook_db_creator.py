import subprocess
import os
import sys

def setup_chinook_db():
    print("Setting up Chinook database...")
    
    db_path = os.path.join(os.path.dirname(__file__), "Chinook.db")
    sql_url = "https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sql"
    
    try:
        # Remove existing database if it exists
        if os.path.exists(db_path):
            os.remove(db_path)
            print("Removed existing database.")
        
        # Download and create database using curl and sqlite3
        cmd = f"curl -s {sql_url} | sqlite3 {db_path}"
        subprocess.run(cmd, shell=True, check=True)
        
        if os.path.exists(db_path):
            print(f"Successfully created Chinook database at: {db_path}")
            return True
        else:
            print("Error: Database file was not created")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    if setup_chinook_db():
        sys.exit(0)
    else:
        sys.exit(1)