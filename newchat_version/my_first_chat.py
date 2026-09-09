import os
import sys
from google.genai import types
from pydantic import BaseModel, Field
from google import genai
from google.genai.errors import APIError
from tools_for_win_ai import run_windows_diagnostics

# Define a structured response model for the Gemini model
class StructuredResponse(BaseModel):
    priority: str = Field(description="Must be one of: Low, Medium, High, Critical")
    category: str = Field(description="The IT domain, e.g., Hardware, Software, Network, Access/IAM")
    summary: str = Field(description="A precise, one-sentence summary of the core issue")
    Suggestions: str = Field(description="A concise list of actionable suggestions for resolving the issue")
    

# configuration for the Gemini model to ensure structured output
resp_schema = types.GenerateContentConfig(
    response_mime_type="application/json",
    response_schema=StructuredResponse,
    temperature=0.1, # Low temperature for consistent classificationo
    tools=[run_windows_diagnostics] # should run if user report a slow win machine
    )    

# format of response  from Gemini will be a JSON string that matches the StructuredResponse model
def start_interactive_chat():
    # Ensure the API key is set before starting
    if not os.environ.get("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable is not set.", file=sys.stderr)
        return 

    # Initialize the standard Google GenAI client
    client = genai.Client()
    

    # Start the stateful chat session
    print("Initializing Gemini session (using gemini-3.8-flash)...")
    chat = client.chats.create(model="gemini-3.8-flash", config=resp_schema,) # Google-AI
        
    print("\nChat session started! Type your message and press Enter. (Type 'quit' to exit)\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue

            if user_input.lower() in ['quit', 'exit']:
                print("Ending chat session. Goodbye!")
                break

            response = chat.send_message(user_input)
            print(f"\nGemini: {response.text}\n")
            print(f"history: {chat.get_history()}")

        except APIError as e:
            print(f"An error occurred while communicating with Gemini: {e}", file=sys.stderr)
            continue
        except KeyboardInterrupt:
            print("\nSession interrupted. Goodbye!")
            break
#------------------------------------End of def start_interactive_chat---------------------------------------------------
if __name__ == "__main__":
    start_interactive_chat()