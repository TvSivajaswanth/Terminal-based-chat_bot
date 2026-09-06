import os
import json
from google import genai
from google.genai import errors
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")


client = genai.Client(api_key=GEMINI_API_KEY)


MEMORY_FILE = "memory.json"

def load_memory():
    
    if not os.path.exists(MEMORY_FILE):
        return []
    
    try:
        with open(MEMORY_FILE,"r",encoding="utf-8") as file:
            return json.load(file)
        
    except (json.JSONDecodeError, OSError):       return []    
    
def save_memory(messages):
    
    messages_dict = [message.model_dump(mode ="json",exclude_none=True) for message in messages]
    
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        
        json.dump(messages_dict, file, indent=2, ensure_ascii=False)
        
def chat():
    messages = load_memory()
    
    print("Terminal Chatbot")
    print("Type 'exit' to quit.")  
    # Create ONE chat for the entire session
         
    chat = client.chats.create( model="gemini-3.6-flash", history=messages
        )
              
    while True:
        user_message = input("You: ")
        
        
        if user_message.lower() == "exit":
            save_memory(chat.get_history())
            print("Chat ended. Bye!")
            break

        try:
            response = chat.send_message(user_message)
            
            print("Gemini:", response.text)
        
           # Save the updated conversation after every message
            save_memory(chat.get_history())
            
        except Exception as e:
            print("Error:", e)
            
if __name__ == "__main__":
    chat()        