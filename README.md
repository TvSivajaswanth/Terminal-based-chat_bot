**Terminal Chatbot (Gemini API)**

A simple terminal-based chatbot built with Google's Gemini API. Conversation history persists across sessions using a local memory.json file.

Features
Chat with Gemini directly from your terminal
Conversation history is saved automatically after every message
Previous conversations are loaded on startup, so the bot remembers past context
Type exit to end the session and save your progress
Requirements
Python 3.9+
A Gemini API key
Setup
Clone the repository
bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
Install dependencies
bash
   pip install -r requirements.txt
Create a .env file in the project root with your API key:
   GEMINI_API_KEY=your_api_key_here

⚠️ Never commit your .env file. It's already excluded via .gitignore.

Usage

Run the chatbot:

bash
python chat_bot.py

Example session:

Terminal Chatbot
Type 'exit' to quit.
You: hi
Gemini: Hello! How can I help you today?
You: exit
Chat ended. Bye!
How it works
On startup, load_memory() reads any existing memory.json and seeds the chat session with it, so the model has context from previous sessions.
Each turn, the full conversation history is pulled from the chat object via chat.get_history() and saved back to memory.json.
memory.json is git-ignored since it's local, user-specific runtime data.
Project structure
.
├── chat_bot.py         # Main chatbot script
├── requirements.txt    # Python dependencies
├── .env                # API key (not committed)
├── memory.json         # Conversation history (not committed, auto-generated)
└── .gitignore
Notes
The Gemini model used is set in chat_bot.py — check the Gemini API docs for the current list of available model names if you run into a model-not-found error.
