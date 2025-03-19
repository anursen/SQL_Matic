import sys
import os
import asyncio
from pathlib import Path

# Add the parent directory to sys.path
current_dir = Path(__file__).resolve().parent
src_dir = current_dir.parent  # This should point to the 'src' directory
sys.path.append(str(src_dir))

from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from tools.ha_tools import ha_get_entities_containing, ha_get_state_of_a_specific_entity, ha_get_entity_history, ha_get_logbook
import aioconsole  # Added for asynchronous input


async def jarvis_with_memory(human_message: str, system_message, user_id, user_storage):
    print(user_storage)
    '''User Storage is a MemorySaver '''
    #TODO memory storage only available in session level. No hard memory available
    #TODO No session level memory available,    
    llm = ChatOpenAI(model="gpt-4o-mini")
    tools = [ha_get_entities_containing
            ,ha_get_state_of_a_specific_entity
            ,ha_get_entity_history
            ,ha_get_logbook]

    llm_with_tools = llm.bind_tools(tools)

    # System message
    sys_msg = SystemMessage(
        content="You are Jarvis, a smart home assistant designed to help with managing home devices and providing information about their statuses. "
                "You have access to the Home Assistant API through various tools. "
                "You can perform the following tasks: "
                "1. Query Home Assistant for a list of entities in the home. "
                "2. Retrieve the current status of any entity. "
                "3. Get the historical data of an entity to analyze past behaviors. "
                f"Always provide accurate and concise information while ensuring a {system_message} tone.")

    # Node
    async def assistant(state: MessagesState):
       return {"messages": [await llm_with_tools.ainvoke([sys_msg] + state["messages"])]}


    # Graph
    builder = StateGraph(MessagesState)

    # Define nodes: these do the work
    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolNode(tools))

    # Define edges: these determine how the control flow moves
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges(
        "assistant",
        # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
        # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
        tools_condition,
    )
    builder.add_edge("tools", "assistant")
    react_graph = builder.compile()

    # Show
    #display(Image(react_graph.get_graph(xray=True).draw_mermaid_png()))

    memory = MemorySaver()

    react_graph_memory = builder.compile(checkpointer=user_storage)

    # Specify a thread
    config = {"configurable": {"thread_id": user_id}}

    # Specify an input
    messages = [HumanMessage(content=human_message)]

        # Run
    messages = await react_graph_memory.ainvoke({"messages": messages},config)
    #for m in messages['messages']:
    #    m.pretty_print()


    return messages['messages'][-1].content

async def main():
    user_storage = MemorySaver()  # Creating a MemorySaver instance for user_storage
    user_id = "12345"
    system_message = "friendly"  # Adjust tone as needed
    print("Enter 'exit' to quit.")
    while True:
        human_message = await aioconsole.ainput("You: ")
        if human_message.lower() in ["exit", "quit"]:
            break
        response = await jarvis_with_memory(human_message, system_message, user_id, user_storage)
        print("Jarvis:", response)

if __name__ == "__main__":
    asyncio.run(main())


