import os
import sys
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain.agents import create_agent 
from langchain.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langgraph.checkpoint.memory import MemorySaver # Handles the context loop
from tools_for_win_ai import run_windows_diagnostics


#--------------------end of  modules import

# Define a structured response model for the Gemini model
class StructuredResponse(BaseModel):
    priority: str = Field(description="Must be one of: Low, Medium, High, Critical")
    category: str = Field(description="The IT domain, e.g., Hardware, Software, Network, Access/IAM")
    summary: str = Field(description="A precise, one-sentence summary of the core issue")
    Suggestions: str = Field(description="If user report windows run slow need to run the tool 'run_windows_diagnostics' and  returns added to Suggestions Desription")

    
#-----------------Ollama LLM chat structure and response----------------------------------------

model = ChatOllama(model="qwen2.5-coder:14b", temperature=0.1, base_url="http://localhost:11434") #initialize ollama LLM
context_memory = MemorySaver()
tools  = [run_windows_diagnostics]

agent = create_agent(
        model = model,
        tools = tools,
        system_prompt = """You are an expert IT Support triage assistant.Recommend reactive remediation of issues""",
        checkpointer= context_memory,)

config = {"configurable": {"thread_id": "user_session_1"}} #need an ID to keep short memory context

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
            for resp in agent.stream({"messages": [{"role": "user", "content":user_input}]}, config = config):    
                print (resp)       

        except Exception as e:
            print(f"An unexpected error occurred: {e}", file=sys.stderr)
            continue
        except KeyboardInterrupt:
            print("\nSession interrupted. Goodbye!")
            break
#------------------------------------End of def start_interactive_chat---------------------------------------------------
if __name__ == "__main__":
    start_interactive_chat()   