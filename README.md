# Gemini Chatbot UI

This is a simple web interface for interacting with Google's Gemini models using Streamlit and LangChain. The application has been refactored to follow object-oriented programming principles, making it more maintainable and extensible. This project was created as part of my learning journey to practice working with LLMs, web interfaces, and API integration.

<img width="2559" height="1386" alt="image" src="https://github.com/user-attachments/assets/cfe40997-0672-4204-8a89-e7a99d9739b4" />

## Features

- Clean, user-friendly chat interface
- Secure API key input with automatic .env file saving
- Conversation history
- Real-time chat responses
- Multiple Gemini model selection (gemini-2.5-flash, gemini-2.5-pro, gemini-1.5-pro, etc.)
- Customizable system prompt
- Clear chat history functionality
- Object-oriented architecture for better maintainability

## Architecture

The application follows an object-oriented design with three main components:
- `Application`: Manages the main Streamlit app flow and UI
- `Configuration`: Handles API key, model selection, and system prompt management
- `GeminiChatbot`: Manages chatbot functionality and communication with Gemini API

## Requirements

- Python 3.8+
- Streamlit
- LangChain
- LangChain Google GenAI
- python-dotenv
- Google Gemini API key

## Setup

1. Clone this repository
2. Install the required packages: `pip install -r requirements.txt`
3. Create a `.env` file in the root directory and add your API key: `GEMINI_API_KEY=your_actual_api_key_here`
4. Run the application: `streamlit run app.py`
5. Your API key will be loaded from the .env file, or you can enter it in the sidebar as an alternative
6. Select your preferred Gemini model from the dropdown
7. Optionally customize the AI behavior with the system prompt
8. Start chatting with the bot!

## Notes

This is a learning project and may be updated as I continue to develop my skills in working with LLMs and building web interfaces. The OOP refactoring improves code organization, maintainability, and extensibility. Feel free to explore, modify, and use this code as a starting point for your own projects.
