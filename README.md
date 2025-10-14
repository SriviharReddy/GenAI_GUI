# Multi-Provider Chatbot UI

This is a simple web interface for interacting with multiple LLM providers (Google Gemini, OpenAI, Anthropic, Groq, and OpenRouter) using Streamlit and LangChain. The application has been refactored to follow object-oriented programming principles and a modular architecture, making it more maintainable and extensible. This project was created as part of my learning journey to practice working with LLMs, web interfaces, and API integration.

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
3. Create a `.env` file in the root directory and add your API key(s):
   - For Google: `GEMINI_API_KEY=your_actual_api_key_here`
   - For OpenAI: `OPENAI_API_KEY=your_actual_api_key_here`
   - For Anthropic: `ANTHROPIC_API_KEY=your_actual_api_key_here`
   - For Groq: `GROQ_API_KEY=your_actual_api_key_here`
   - For OpenRouter: `OPENROUTER_API_KEY=your_actual_api_key_here`
4. Run the application: `streamlit run app.py`
5. Select your preferred provider from the dropdown in the sidebar
6. Enter your corresponding API key in the sidebar
7. Select your preferred model from the dropdown
8. Optionally customize the AI behavior with the system prompt
9. Start chatting with the bot!

## Notes

This is a learning project and may be updated as I continue to develop my skills in working with LLMs and building web interfaces. The modular refactoring improves code organization, maintainability, and extensibility. Feel free to explore, modify, and use this code as a starting point for your own projects.
