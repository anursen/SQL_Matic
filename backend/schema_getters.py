from abc import ABC, abstractmethod
import sqlite3
from typing import Dict, List
import pymongo
import mysql.connector
import psycopg2
from psycopg2.extensions import connection as pg_connection

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

class MongoDBSchemaGetter(SchemaGetter):
    def __init__(self, connection_string: str, database_name: str, config: Dict):
        self.connection_string = connection_string
        self.database_name = database_name
        self.config = config

    def get_schema(self) -> Dict:
        client = pymongo.MongoClient(self.connection_string)
        db = client[self.database_name]
        
        schema_info = {"collections": []}
        
        for collection_name in db.list_collection_names():
            sample_doc = db[collection_name].find_one()
            if sample_doc:
                fields = self._analyze_document(sample_doc)
                schema_info["collections"].append({
                    "name": collection_name,
                    "fields": fields
                })
                
                if self.config.get('include_indexes'):
                    indexes = list(db[collection_name].list_indexes())
                    schema_info["collections"][-1]["indexes"] = indexes
        
        client.close()
        return schema_info
    
    def _analyze_document(self, doc: Dict, prefix: str = "") -> List[Dict]:
        fields = []
        for key, value in doc.items():
            if key == "_id":
                continue
                
            field_name = f"{prefix}{key}"
            field_type = type(value).__name__
            
            if isinstance(value, dict):
                fields.extend(self._analyze_document(value, f"{field_name}."))
            else:
                fields.append({
                    "name": field_name,
                    "type": field_type
                })
        return fields

class MySQLSchemaGetter(SchemaGetter):
    def __init__(self, host: str, port: int, user: str, password: str, database: str, config: Dict):
        self.connection_params = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': database
        }
        self.config = config

    def get_schema(self) -> Dict:
        conn = mysql.connector.connect(**self.connection_params)
        cursor = conn.cursor(dictionary=True)
        
        schema_info = {"tables": [], "indexes": []}
        
        # Get tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = DATABASE()
            LIMIT %s
        """, [self.config.get('max_tables', 100)])
        
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table['table_name']
            
            # Get columns
            cursor.execute("""
                SELECT column_name, data_type, is_nullable, column_key
                FROM information_schema.columns
                WHERE table_schema = DATABASE() AND table_name = %s
            """, [table_name])
            columns = cursor.fetchall()
            
            # Get foreign keys if enabled
            foreign_keys = []
            if self.config.get('include_relationships'):
                cursor.execute("""
                    SELECT 
                        column_name,
                        referenced_table_name,
                        referenced_column_name
                    FROM information_schema.key_column_usage
                    WHERE table_schema = DATABASE()
                        AND table_name = %s
                        AND referenced_table_name IS NOT NULL
                """, [table_name])
                foreign_keys = cursor.fetchall()
            
            table_info = {
                "name": table_name,
                "columns": [
                    {
                        "name": col['column_name'],
                        "type": col['data_type'],
                        "notnull": col['is_nullable'] == 'NO',
                        "pk": col['column_key'] == 'PRI'
                    } for col in columns
                ],
                "foreign_keys": [
                    {
                        "from": fk['column_name'],
                        "to_table": fk['referenced_table_name'],
                        "to_column": fk['referenced_column_name']
                    } for fk in foreign_keys
                ]
            }
            
            schema_info["tables"].append(table_info)
            
            # Get indexes if enabled
            if self.config.get('include_indexes'):
                cursor.execute("""
                    SHOW INDEX FROM {}
                """.format(table_name))
                indexes = cursor.fetchall()
                for idx in indexes:
                    schema_info["indexes"].append({
                        "table": table_name,
                        "name": idx['Key_name'],
                        "unique": not idx['Non_unique']
                    })
        
        cursor.close()
        conn.close()
        return schema_info

class PostgreSQLSchemaGetter(SchemaGetter):
    def __init__(self, host: str, port: int, user: str, password: str, database: str, config: Dict):
        self.connection_params = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': database
        }
        self.config = config

    def get_schema(self) -> Dict:
        conn: pg_connection = psycopg2.connect(**self.connection_params)
        cursor = conn.cursor()
        
        schema_info = {"tables": [], "indexes": []}
        
        # Get tables
        cursor.execute("""
            SELECT tablename 
            FROM pg_catalog.pg_tables 
            WHERE schemaname = 'public'
            LIMIT %s
        """, [self.config.get('max_tables', 100)])
        
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            
            # Get columns
            cursor.execute("""
                SELECT 
                    column_name,
                    data_type,
                    is_nullable,
                    CASE 
                        WHEN pk.colname IS NOT NULL THEN true 
                        ELSE false 
                    END as is_pk
                FROM information_schema.columns c
                LEFT JOIN (
                    SELECT a.attname as colname
                    FROM pg_index i
                    JOIN pg_attribute a ON a.attrelid = i.indrelid
                    AND a.attnum = ANY(i.indkey)
                    WHERE i.indrelid = %s::regclass
                    AND i.indisprimary
                ) pk ON pk.colname = c.column_name
                WHERE table_name = %s
            """, [table_name, table_name])
            columns = cursor.fetchall()
            
            # Get foreign keys if enabled
            foreign_keys = []
            if self.config.get('include_relationships'):
                cursor.execute("""
                    SELECT
                        kcu.column_name,
                        ccu.table_name AS foreign_table_name,
                        ccu.column_name AS foreign_column_name
                    FROM information_schema.table_constraints AS tc
                    JOIN information_schema.key_column_usage AS kcu
                        ON tc.constraint_name = kcu.constraint_name
                    JOIN information_schema.constraint_column_usage AS ccu
                        ON ccu.constraint_name = tc.constraint_name
                    WHERE tc.constraint_type = 'FOREIGN KEY'
                        AND tc.table_name = %s
                """, [table_name])
                foreign_keys = cursor.fetchall()
            
            table_info = {
                "name": table_name,
                "columns": [
                    {
                        "name": col[0],
                        "type": col[1],
                        "notnull": col[2] == 'NO',
                        "pk": col[3]
                    } for col in columns
                ],
                "foreign_keys": [
                    {
                        "from": fk[0],
                        "to_table": fk[1],
                        "to_column": fk[2]
                    } for fk in foreign_keys
                ]
            }
            
            schema_info["tables"].append(table_info)
            
            # Get indexes if enabled
            if self.config.get('include_indexes'):
                cursor.execute("""
                    SELECT
                        i.relname as index_name,
                        ix.indisunique as is_unique
                    FROM pg_class t
                    JOIN pg_index ix ON t.oid = ix.indrelid
                    JOIN pg_class i ON i.oid = ix.indexrelid
                    WHERE t.relname = %s
                """, [table_name])
                indexes = cursor.fetchall()
                for idx in indexes:
                    schema_info["indexes"].append({
                        "table": table_name,
                        "name": idx[0],
                        "unique": idx[1]
                    })
        
        cursor.close()
        conn.close()
        return schema_info
