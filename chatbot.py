"""
Chatbot manager with session-based chat history.
"""

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

from graph import stream_chat_response, get_chat_response, get_session_messages
from history import (
    create_session, get_session, get_all_sessions,
    update_session_title, update_session_timestamp, delete_session,
    generate_title_from_message, ChatSession
)


class ChatbotManager:
    """
    Manages chatbot functionality with session-based history.
    """
    
    def __init__(self):
        """Initialize the chatbot manager and session state."""
        # Current session
        if "current_session_id" not in st.session_state:
            st.session_state.current_session_id = None
        
        # Messages for current session (in-memory cache)
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        if "is_streaming" not in st.session_state:
            st.session_state.is_streaming = False
    
    @property
    def current_session_id(self) -> str | None:
        """Get the current session ID."""
        return st.session_state.current_session_id
    
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
        return st.session_state.get("model", "gemini-3-pro")
    
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
    
    def new_chat(self) -> ChatSession:
        """Create a new chat session."""
        session = create_session(provider=self.provider, model=self.model)
        st.session_state.current_session_id = session.id
        st.session_state.messages = []
        return session
    
    def load_session(self, session_id: str) -> None:
        """Load an existing chat session."""
        session = get_session(session_id)
        if session:
            st.session_state.current_session_id = session_id
            # Load messages from checkpoint
            st.session_state.messages = get_session_messages(session_id)
    
    def delete_current_session(self) -> None:
        """Delete the current session."""
        if self.current_session_id:
            delete_session(self.current_session_id)
            st.session_state.current_session_id = None
            st.session_state.messages = []
    
    def get_sessions(self) -> list[ChatSession]:
        """Get all chat sessions."""
        return get_all_sessions()
    
    def add_message(self, role: str, content: str) -> None:
        """Add a message to the chat history."""
        if role == "human":
            st.session_state.messages.append(HumanMessage(content=content))
            
            # Auto-generate title from first message
            if self.current_session_id and len(st.session_state.messages) == 1:
                title = generate_title_from_message(content)
                update_session_title(self.current_session_id, title)
        elif role == "ai":
            st.session_state.messages.append(AIMessage(content=content))
        
        # Update session timestamp
        if self.current_session_id:
            update_session_timestamp(self.current_session_id)
    
    def clear_history(self) -> None:
        """Clear the current chat history."""
        st.session_state.messages = []
    
    def display_chat_history(self) -> None:
        """Display all messages in the chat history."""
        for message in self.messages:
            role = "human" if isinstance(message, HumanMessage) else "ai"
            with st.chat_message(role):
                st.markdown(message.content)
    
    def ensure_session(self) -> None:
        """Ensure there's an active session, create one if needed."""
        if not self.current_session_id:
            self.new_chat()
    
    def get_streaming_response(self, user_input: str):
        """Get a streaming response."""
        self.ensure_session()
        messages_with_input = self.messages + [HumanMessage(content=user_input)]
        
        yield from stream_chat_response(
            messages=messages_with_input,
            provider=self.provider,
            model=self.model,
            api_key=self.api_key,
            system_prompt=self.system_prompt,
            session_id=self.current_session_id or ""
        )
    
    def get_response(self, user_input: str) -> tuple[str | None, str | None]:
        """Get a non-streaming response."""
        self.ensure_session()
        messages_with_input = self.messages + [HumanMessage(content=user_input)]
        
        return get_chat_response(
            messages=messages_with_input,
            provider=self.provider,
            model=self.model,
            api_key=self.api_key,
            system_prompt=self.system_prompt,
            session_id=self.current_session_id or ""
        )


# Legacy alias
MultiProviderChatbot = ChatbotManager