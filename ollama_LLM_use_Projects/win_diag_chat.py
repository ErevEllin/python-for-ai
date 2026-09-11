import os
import sys
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain.agents import create_agent 
from langchain.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langgraph.checkpoint.memory import MemorySaver # Handles the context loop
from tools_for_win_ai import run_windows_diagnostics
import psutil


#-----------------Ollama LLM chat structure and response----------------------------------------

model = ChatOllama(model="qwen2.5-coder:14b", temperature=0.1, base_url="http://localhost:11434") #initialize ollama LLM
context_memory = MemorySaver()
tools  = [run_windows_diagnostics]
config = {"configurable": {"thread_id": "user_session_1"}} #need an ID to keep short memory context


myagent = create_agent(
        model = model,
        tools = tools,
        system_prompt = """You are an expert IT Support triage assistant. Analyze the user's input. If the user reports a slow Windows machine then MUST execute the 'run_windows_diagnostics' 
        tool to gather performance logs before responding.""",
        checkpointer= context_memory,)


def start_interactive_chat():
     
    print("\nChat session started! Type your message and press Enter. (Type 'quit' to exit)\n")
       
    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue

            if user_input.lower() in ['quit', 'exit']:
                print("Ending chat session. Goodbye!")
                break

            for result in myagent.stream({"messages": [{"role": "user", "content": user_input}]}, config = config ):
                print(result)
        except Exception as e:
            print(f"An unexpected error occurred: {e}", file=sys.stderr)
            continue
        except KeyboardInterrupt:
            print("\nSession interrupted. Goodbye!")
            break
#------------------------------------End of def start_interactive_chat---------------------------------------------------
if __name__ == "__main__":
    start_interactive_chat()   

   
