import sqlite3
import os
import sys
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import START, END, Graph
from typing import Dict, Any
from config import config
import yaml
from pathlib import Path
from langchain.chat_models import init_chat_model


def load_config():
    config_path = Path(__file__).parent.parent.parent / "config.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)


class SQLQueryAssistant:
    '''We need to redefine graph again.
    It should use execute_query and get_schema_info functions as tools
    these functions are running local and not consumpting tokens.
    so they can be used as required without any constraint.
    generate_sql function will be a llm call and llm will anayze which toll to 
    use or output the response.
    '''
    
    def __init__(self, db_path=None):
        self.db_path = db_path or config.database_config['default_path']
        
        self.llm = init_chat_model(
        config.llm_config['model'],
        temperature=config.llm_config['temperature'],
        max_tokens=config.llm_config['max_tokens'],
        streaming=config.llm_config['streaming'])
        
        self.db = SQLDatabase.from_uri(f"sqlite:///{self.db_path}")
        self.setup_graph()
        self.ground_truth_path = Path(__file__).parent.parent.parent / config.evaluation_config['ground_truth_path']

    def setup_graph(self):
        def generate_sql(state: Dict[str, Any]):
            query = state["query"]
            # Get database schema
            db_schema = self.db.get_table_info()
            
            template = config.templates_config.get('sql_query')
            
            prompt = ChatPromptTemplate.from_template(template)
            chain = prompt | self.llm | StrOutputParser()
            sql_query = chain.invoke({
                "question": query,
                "db_schema": db_schema
            })
            state["sql"] = sql_query
            return state

        def execute_query(state: Dict[str, Any]):
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            try:
                results = cursor.execute(state["sql"]).fetchall()
                state["results"] = results
            except Exception as e:
                state["error"] = str(e)
            finally:
                conn.close()
            return state

        workflow = Graph()
        workflow.add_edge(START,'generate_sql')
        workflow.add_node("generate_sql", generate_sql)
        workflow.add_node("execute_query", execute_query)
        workflow.add_edge("generate_sql", "execute_query")
        workflow.add_edge("execute_query", END)

        self.graph = workflow.compile()

    def process_query(self, query: str) -> Dict[str, Any]:
        result = self.graph.invoke({"query": query})
        return result

    def evaluate_performance(self) -> Dict[str, Any]:
        """
        Evaluates the SQL assistant's performance against ground truth data.
        Returns a dictionary containing performance metrics.
        """
        # Load ground truth data
        try:
            df = pd.read_csv(self.ground_truth_path).head(5)
        except Exception as e:
            return {"error": f"Failed to load ground truth data: {str(e)}"}

        # Initialize vectorizer for cosine similarity
        vectorizer = TfidfVectorizer(lowercase=True, strip_accents='unicode')

        # Store results
        results = {
            "total_queries": len(df),
            "successful_queries": 0,
            "failed_queries": 0,
            "average_similarity": 0.0,
            "similarities": [],
            "failed_cases": []
        }

        for idx, row in df.iterrows():
            try:
                # Get assistant's SQL query
                assistant_result = self.process_query(row["User Input"])
                assistant_sql = assistant_result.get("sql", "").lower().strip()
                ground_truth_sql = row["Ground Truth SQL"].lower().strip()

                # Calculate similarity
                if assistant_sql and ground_truth_sql:
                    tfidf_matrix = vectorizer.fit_transform([assistant_sql, ground_truth_sql])
                    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
                    
                    results["similarities"].append({
                        "query": row["User Input"],
                        "similarity": similarity,
                        "assistant_sql": assistant_sql,
                        "ground_truth_sql": ground_truth_sql
                    })
                    
                    if similarity >= config.evaluation_config.get('similarity_threshold', 0.8):
                        results["successful_queries"] += 1
                    else:
                        results["failed_queries"] += 1
                        results["failed_cases"].append({
                            "query": row["User Input"],
                            "assistant_sql": assistant_sql,
                            "ground_truth_sql": ground_truth_sql,
                            "similarity": similarity
                        })
                else:
                    results["failed_queries"] += 1
                    
            except Exception as e:
                results["failed_queries"] += 1
                results["failed_cases"].append({
                    "query": row["User Input"],
                    "error": str(e)
                })

        # Calculate average similarity
        if results["similarities"]:
            results["average_similarity"] = np.mean([s["similarity"] for s in results["similarities"]])

        return results

def main():
    # Create an instance of SQLQueryAssistant
    assistant = SQLQueryAssistant()
    
    # Test query
    test_input = "Show me all tables in the database"
    print(f"Testing query: {test_input}")
    
    # Process the query
    try:
        result = assistant.process_query(test_input)
        print("\nQuery Results:")
        print("SQL Query:", result.get("sql"))
        print("Results:", result.get("results"))
        if "error" in result:
            print("Error:", result["error"])
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
