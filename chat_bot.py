import os
import json
from google import genai
from google.genai import errors
from dotenv import load_dotenv

# 1. Load environment variables from .env file
load_dotenv()

# 2. Retrieve Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file. Please add GEMINI_API_KEY=your_key to your .env file.")

# 3. Initialize the Google GenAI client
client = genai.Client(api_key=GEMINI_API_KEY)

# 4. Define the local JSON file used to persist chat history
MEMORY_FILE = "memory.json"


def load_memory():
    """
    Loads previous chat history from the local JSON file.
    
    Returns:
        list: A list of previously saved message dictionaries, or an empty list
              if the file doesn't exist or is corrupted.
    """
    if not os.path.exists(MEMORY_FILE):
        return []
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        # Fallback to an empty list if file cannot be read or parsed
        return []


def save_memory(messages):
    """
    Saves the chat conversation history into the local JSON file.
    
    Args:
        messages (list): List of chat Content/message objects from Gemini chat history.
    """
    # Convert Pydantic model objects from the SDK into serializable JSON dictionaries
    messages_dict = [
        message.model_dump(mode="json", exclude_none=True) 
        for message in messages
    ]
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(messages_dict, file, indent=2, ensure_ascii=False)


def chat():
    """
    Runs the main interactive terminal chatbot loop.
    - Loads existing memory.
    - Starts a multi-turn chat session with history.
    - Takes user input, sends it to Gemini, displays response, and updates memory.
    """
    messages = load_memory()
    print("========================================")
    print("           Terminal Chatbot             ")
    print("       Type 'exit' to quit chat         ")
    print("========================================\n")

    # Create one continuous chat session with existing history
    chat_session = client.chats.create(
        model="gemini-3.8-flash",
        history=messages
    )

    while True:
        try:
            user_message = input("You: ").strip()
            
            # Skip empty inputs
            if not user_message:
                continue

            # Quit command
            if user_message.lower() == "exit":
                save_memory(chat_session.get_history())
                print("\nChat ended. Conversation saved. Bye!")
                break

            # Send user message to the Gemini chat session
            response = chat_session.send_message(user_message)
            print(f"\nGemini: {response.text}\n")

            # Persist updated history after each interaction
            save_memory(chat_session.get_history())

        except KeyboardInterrupt:
            print("\n\nSession interrupted. Saving conversation...")
            save_memory(chat_session.get_history())
            print("Saved. Goodbye!")
            break
        except Exception as e:
            print(f"\n[Error]: {e}\n")


if __name__ == "__main__":
    chat()
