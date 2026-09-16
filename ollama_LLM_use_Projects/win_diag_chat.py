import sys
import os
import ollama
from tools_for_win_ai import run_windows_diagnostics

# 2. Define the tool schema so Ollama knows it exists and how to use it
tools_schema = [
    {
        'type': 'function',
        'function': {
            'name': 'run_windows_diagnostics',
            'description': 'If system is running slow then run diagnostic tool',
            'parameters': {
                'type': 'object',
                'properties': {
                    
                 },           
            },
        },
    }
]

def start_interactive_chat():
   
  # Initialize the message history with a system prompt and the user request
    messages = [ {"role": "system", "content": "You are a helpful assistant. Use your tools whenever a user reports a slow windows machine."},             
            ]  
    # Step 1: Send the initial prompt and tool definitions to Ollama
    model_name = 'qwen2.5:latest'
    print("🤖 Agent: Hello! How can I help you today?")    

    while True:
 
        try:

            user_input = input("You: ").strip()
            if not user_input:
                           continue
           
            if user_input.lower() in ['quit', 'exit']:
                           print("Ending chat session. Goodbye!")
                           break
            
            messages.append({"role":"user", "content":user_input})

            response = ollama.chat(
                                model=model_name,
                                messages=messages,
                                tools=tools_schema,)
            print (response.message)
            # Add the model's response to the history
            messages.append(response['message'])
            
            # Step 2: Check if the model decided it needs to call a tool
            if response['message'].get('tool_calls'):
                for tool in response['message']['tool_calls']:
                    if tool['function']['name'] == 'run_windows_diagnostics':
                        # Extract arguments parsed by the model
                        args = tool['function']['arguments']
                        # number_arg = int(args['number'])
                        # Execute the actual Python tool
                        tool_output = run_windows_diagnostics()
                        
                        # Step 3: Append the tool output to the message history
                        messages.append({
                            'role': 'tool',
                            'content': tool_output,
                            'name': tool['function']['name']
                        })
                
                # Step 4: Send the updated history back to Ollama so it can formulate a final response
                final_response = ollama.chat(
                    model=model_name,
                    messages=messages
                )
                print(f"🤖 Agent: {final_response['message']['content']}")
            else:
                # If no tool was needed, just print the direct response
                print(f"🤖 Agent: {response['message']['content']}")
        except TypeError as e:
            print(f"An error occurred while communicating with Gemini: {e}", file=sys.stderr)
            continue
        except KeyboardInterrupt:
            print("\nSession interrupted. Goodbye!")
            break




#-----------------Ollama LLM chat structure and response----------------------------------------

if __name__ == "__main__":
    start_interactive_chat()   

   
