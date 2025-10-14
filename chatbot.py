import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage


class MultiProviderChatbot:
    """Manages the multi-provider chatbot functionality."""
    
    def __init__(self):
        # Initialize session state for messages if not already
        if "messages" not in st.session_state:
            st.session_state.messages = []
    
    def get_response(self, user_input):
        """Get response from the selected provider's API."""
        # Check if API key is available based on selected provider
        api_key = None
        if st.session_state.provider == "Google":
            api_key = st.session_state.gemini_api_key
        elif st.session_state.provider == "OpenAI":
            api_key = st.session_state.openai_api_key
        elif st.session_state.provider == "Anthropic":
            api_key = st.session_state.anthropic_api_key
        elif st.session_state.provider == "Groq":
            api_key = st.session_state.groq_api_key
        elif st.session_state.provider == "OpenRouter":
            api_key = st.session_state.openrouter_api_key
        
        if not api_key:
            st.error(f"Please enter your {st.session_state.provider} API key in the sidebar!")
            return None

        try:
            # Initialize the model based on the selected provider
            if st.session_state.provider == "Google":
                llm = ChatGoogleGenerativeAI(
                    model=st.session_state.model,
                    google_api_key=api_key,
                    temperature=0.7
                )
            elif st.session_state.provider == "OpenAI":
                llm = ChatOpenAI(
                    model=st.session_state.model,
                    openai_api_key=api_key,
                    temperature=0.7
                )
            elif st.session_state.provider == "Anthropic":
                llm = ChatAnthropic(
                    model=st.session_state.model,
                    anthropic_api_key=api_key,
                    temperature=0.7
                )
            elif st.session_state.provider == "Groq":
                llm = ChatGroq(
                    model=st.session_state.model,
                    groq_api_key=api_key,
                    temperature=0.7
                )
            elif st.session_state.provider == "OpenRouter":
                # For OpenRouter, we set the base URL to OpenRouter's endpoint
                llm = ChatOpenAI(
                    model=st.session_state.model,
                    openai_api_key=api_key,
                    temperature=0.7,
                    base_url="https://openrouter.ai/api/v1"
                )
            
            # Prepare the messages for the model
            messages = []
            
            # Add system prompt as the first message if it exists and this is the first interaction
            if st.session_state.system_prompt and not st.session_state.messages:
                messages.append(HumanMessage(content=st.session_state.system_prompt))
                messages.append(AIMessage(content="I understand. I'll follow the instructions in your system prompt. How can I assist you today?"))
            
            # Add the existing conversation history
            for msg in st.session_state.messages:
                if isinstance(msg, HumanMessage):
                    messages.append(HumanMessage(content=msg.content))
                elif isinstance(msg, AIMessage):
                    messages.append(AIMessage(content=msg.content))
            
            # Add the current user input
            messages.append(HumanMessage(content=user_input))
            
            # Get the response from the model
            response = llm.invoke(messages)
            return response.content
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return None
    
    def display_chat_history(self):
        """Display the chat messages in the UI."""
        for message in st.session_state.messages:
            with st.chat_message(message.type):
                st.write(message.content)
    
    def add_message(self, role, content):
        """Add a message to the chat history."""
        if role == "human":
            st.session_state.messages.append(HumanMessage(content=content))
        elif role == "ai":
            st.session_state.messages.append(AIMessage(content=content))