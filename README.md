# Multi-Provider Chatbot UI

This is a simple web interface for interacting with multiple LLM providers (Google Gemini, OpenAI, Anthropic, Groq, and OpenRouter) using Streamlit and LangChain. The application has been refactored to follow object-oriented programming principles and a modular architecture, making it more maintainable and extensible. This project was created as part of my learning journey to practice working with LLMs, web interfaces, and API integration.

<img width="2559" height="1387" alt="image" src="https://github.com/user-attachments/assets/f2b29381-7c23-45e7-9be9-8e79caf518ad" />


## Features

- Clean, user-friendly chat interface
- Support for multiple LLM providers (Google Gemini, OpenAI, Anthropic, Groq, OpenRouter)
- Secure API key input with automatic .env file saving
- Conversation history
- Real-time chat responses
- Provider-specific model selection
- Customizable system prompt
- Clear chat history functionality
- Modular architecture with separate files for configuration and chatbot logic

## Architecture

The application follows a modular design with separate files:
- `app.py`: Main application entry point and UI flow management
- `config.py`: Handles provider selection, API key management, model selection, and system prompts
- `chatbot.py`: Manages chatbot functionality and communication with multiple LLM providers

## Requirements

- Python 3.8+
- Streamlit
- LangChain
- LangChain Google GenAI
- LangChain OpenAI
- LangChain Anthropic
- LangChain Groq
- python-dotenv

## Setup

1. Clone this repository
2. Install the required packages: `pip install -r requirements.txt`
3. Run the application: `streamlit run app.py`
4. Select your preferred provider from the dropdown in the sidebar
5. Enter your corresponding API key in the sidebar (the .env file will be automatically created)
6. Select your preferred model from the dropdown
7. Optionally customize the AI behavior with the system prompt
8. Start chatting with the bot!

Note: The application will automatically create and update a `.env` file to store your API keys. You do not need to manually create this file.

## Notes

This is a learning project and may be updated as I continue to develop my skills in working with LLMs and building web interfaces. The modular refactoring improves code organization, maintainability, and extensibility. Feel free to explore, modify, and use this code as a starting point for your own projects.
