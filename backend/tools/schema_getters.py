from abc import ABC, abstractmethod
import sqlite3
from typing import Dict

class SchemaGetter(ABC):
    @abstractmethod
    def get_schema(self) -> Dict:
        pass

class SQLiteSchemaGetter(SchemaGetter):
    def __init__(self, db_path: str, config: Dict):
        self.db_path = db_path
        self.config = config

    def get_schema(self) -> Dict:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        schema_info = {"tables": [], "indexes": []}
        
        tables_query = """
            SELECT name FROM sqlite_master 
            WHERE type='table'
            {}
            LIMIT ?
        """.format("AND name NOT LIKE 'sqlite_%'" if self.config.get('exclude_system_tables') else "")
        
        tables = cursor.execute(tables_query, [self.config.get('max_tables', 100)]).fetchall()
        
        for table in tables:
            table_name = table[0]
            columns = cursor.execute(f"PRAGMA table_info('{table_name}')").fetchall()
            foreign_keys = cursor.execute(f"PRAGMA foreign_key_list('{table_name}')").fetchall()
            
            table_info = {
                "name": table_name,
                "columns": [
                    {
                        "name": col[1],
                        "type": col[2],
                        "notnull": bool(col[3]),
                        "pk": bool(col[5])
                    } for col in columns
                ],
                "foreign_keys": [
                    {
                        "from": fk[3],
                        "to_table": fk[2],
                        "to_column": fk[4]
                    } for fk in foreign_keys
                ] if self.config.get('include_relationships') else []
            }
            
            schema_info["tables"].append(table_info)
            
            if self.config.get('include_indexes'):
                indexes = cursor.execute(f"PRAGMA index_list('{table_name}')").fetchall()
                for idx in indexes:
                    schema_info["indexes"].append({
                        "table": table_name,
                        "name": idx[1],
                        "unique": bool(idx[2])
                    })
        
        conn.close()
        return schema_info
