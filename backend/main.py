import os

from agents.sql_matic import SQLQueryAssistant
import asyncio
from config import config
from typing import Dict, Any



async def main():
    assistant = SQLQueryAssistant(purpose='regular')
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Exiting the chatbot. Goodbye!")
            break
        elif user_input.lower() == 'help':
            print("Available commands: 'exit', 'quit', 'help'")
            continue   
        else:        
            response = await assistant.process_query(user_input)
            print(response)

if __name__ == "__main__":
    asyncio.run(main())
