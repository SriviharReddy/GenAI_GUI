"""
Modern chatbot module using LangGraph for state management.
Provides a clean interface between the Streamlit UI and the graph.
"""

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

from graph import stream_chat_response, get_chat_response


class ChatbotManager:
    """
    Manages the chatbot functionality with LangGraph integration.
    Handles message history, streaming, and UI interactions.
    """
    
    def __init__(self):
        """Initialize the chatbot manager and session state."""
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "is_streaming" not in st.session_state:
            st.session_state.is_streaming = False
    
    @property
    def messages(self) -> list[BaseMessage]:
        """Get the current message history."""
        return st.session_state.messages
    
    @property
    def provider(self) -> str:
        """Get the current provider."""
        return st.session_state.get("provider", "Google")
    
    @property
    def model(self) -> str:
        """Get the current model."""
        return st.session_state.get("model", "gemini-2.0-flash")
    
    @property
    def api_key(self) -> str:
        """Get the API key for the current provider."""
        provider_key_map = {
            "Google": "gemini_api_key",
            "OpenAI": "openai_api_key",
            "Anthropic": "anthropic_api_key",
            "Groq": "groq_api_key",
            "OpenRouter": "openrouter_api_key"
        }
        key_name = provider_key_map.get(self.provider, "gemini_api_key")
        return st.session_state.get(key_name, "")
    
    @property
    def system_prompt(self) -> str:
        """Get the current system prompt."""
        return st.session_state.get("system_prompt", "")
    
    def add_message(self, role: str, content: str) -> None:
        """
        Add a message to the chat history.
        
        Args:
            role: Either 'human' or 'ai'
            content: The message content
        """
        if role == "human":
            st.session_state.messages.append(HumanMessage(content=content))
        elif role == "ai":
            st.session_state.messages.append(AIMessage(content=content))
    
    def clear_history(self) -> None:
        """Clear the chat history."""
        st.session_state.messages = []
    
    def display_chat_history(self) -> None:
        """Display all messages in the chat history."""
        for message in self.messages:
            role = "human" if isinstance(message, HumanMessage) else "ai"
            with st.chat_message(role):
                st.markdown(message.content)
    
    def get_streaming_response(self, user_input: str):
        """
        Get a streaming response from the LangGraph.
        
        Args:
            user_input: The user's message
            
        Yields:
            str: Chunks of the response
        """
        # Add user message to history for context
        messages_with_input = self.messages + [HumanMessage(content=user_input)]
        
        yield from stream_chat_response(
            messages=messages_with_input,
            provider=self.provider,
            model=self.model,
            api_key=self.api_key,
            system_prompt=self.system_prompt
        )
    
    def get_response(self, user_input: str) -> tuple[str | None, str | None]:
        """
        Get a non-streaming response from the LangGraph.
        
        Args:
            user_input: The user's message
            
        Returns:
            tuple: (response_content, error_message)
        """
        messages_with_input = self.messages + [HumanMessage(content=user_input)]
        
        return get_chat_response(
            messages=messages_with_input,
            provider=self.provider,
            model=self.model,
            api_key=self.api_key,
            system_prompt=self.system_prompt
        )


# Legacy alias for backward compatibility
MultiProviderChatbot = ChatbotManager