import sys
from pathlib import Path
import os

# Add project root to Python path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

from langgraph.prebuilt import tools_condition, ToolNode

from config import config
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model
from langgraph.graph import START, MessagesState, StateGraph
from tools.get_schema import get_schema
from tools.execute_sql import execute_sql_query
from tools.query_data_dictionary import get_db_field_definition
from langgraph.checkpoint.memory import MemorySaver
from typing import Literal

class SQLQueryAssistant:
    '''We need to redefine graph again.
    It should use execute_query and get_schema_info functions as tools
    these functions are running local and not consumpting tokens.
    so they can be used as required without any constraint.
    generate_sql function will be a llm call and llm will anayze which toll to 
    use or output the response.
    '''
    
    def __init__(self,purpose : Literal['regular','evaluator']):
        self.db_path = config.database_config['default_path']
        self.memory = MemorySaver()
        self.purpose = purpose
    
        
        self.llm = init_chat_model(
            config.llm_config['model'],
            temperature=config.llm_config['temperature'],
            max_tokens=config.llm_config['max_tokens'],
            streaming=config.llm_config['streaming']
        )
        
        self.tools = [get_schema, execute_sql_query, get_db_field_definition]
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.setup_graph()
        

    def setup_graph(self):
        # Define the system message and tools
        if self.purpose == 'regular':
            system_message = config.assistant_config['regular_system_message']
        else:
            system_message = config.assistant_config['evaluator_system_message']
        sys_msg = SystemMessage(content=system_message)        
        
        async def assistant(state: MessagesState):
            return {"messages": [await self.llm_with_tools.ainvoke([sys_msg] + state["messages"])]}

        # Graph
        builder = StateGraph(MessagesState)
        
        # Define nodes
        builder.add_node("assistant", assistant)
        builder.add_node("tools", ToolNode(self.tools))
        
        # Define edges
        builder.add_edge(START, "assistant")
        builder.add_conditional_edges(
            "assistant",
            tools_condition,
        )
        builder.add_edge("tools", "assistant")
        
        self.graph = builder.compile(checkpointer=self.memory)

    async def process_query(self, query: str, thread_id=None) -> str:
        if not thread_id:
            thread_id = config.assistant_config['process']['default_thread_id']
        messages = [HumanMessage(content=query)]
        config_params = {
            "configurable": {
                "thread_id": thread_id
            }
        }
        result = await self.graph.ainvoke({"messages": messages}, config_params)
        return result['messages'][-1].content

