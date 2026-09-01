import os
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

# 1. Define the desired output structure using Pydantic
class StructuredTicket(BaseModel):
    priority: str = Field(description="Must be one of: Low, Medium, High, Critical")
    category: str = Field(description="The IT domain, e.g., Hardware, Software, Network, Access/IAM")
    summary: str = Field(description="A precise, one-sentence summary of the core issue")

def clean_ticket(raw_ticket_text: str) -> str:
    """
    Takes a messy ticket string, sends it to Gemini, 
    and returns a formatted JSON string.
    """
    # 2. Initialize the client. 
    # It automatically picks up the GEMINI_API_KEY environment variable.
    client = genai.Client()
    
    prompt = f"""
    You are an expert IT Support triage assistant. 
    Analyze the following messy, unformatted support ticket log.
    Extract the priority, category, and create a 1-sentence summary.
    
    Messy Ticket Log:
    \"\"\"
    {raw_ticket_text}
    \"\"\"
    """
    print(prompt)

    # 3. Call the Gemini 2.5 Flash model (available on the free tier)
    response = client.models.generate_content(
        model='gemini-3.7 flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            # Force the model to reply ONLY with the JSON structure matching our Pydantic model
            response_mime_type="application/json",
            response_schema=StructuredTicket,
            temperature=0.1, # Low temperature for consistent classification
        ),
    )
    
    return response.text

# --- Example Usage ---
if __name__ == "__main__":
    # Ensure your API key is set before running: export GEMINI_API_KEY="your_key"
    if "GEMINI_API_KEY" not in os.environ:
        print("Error: Please set the GEMINI_API_KEY environment variable.")
        exit(1)

    # A typical messy, chaotic IT ticket log
    messy_log = """
    ID: #98231 - SENT FROM IPHONE
    hey guys, sorry to bother but internet is completely dead on the 3rd floor. 
    john can't login either but i think his account is locked anyway? 
    actually wait, the router in the hallway has a blinking red light. 
    we cant access the shared drive or print anything. HELP!!! we have a client pitch in 20 mins!!!!
    - Sarah from Marketing
    """
    
    print("Processing ticket...")
    json_output = clean_ticket(messy_log)

    print("\nStructured JSON Result:")
    print(json_output)