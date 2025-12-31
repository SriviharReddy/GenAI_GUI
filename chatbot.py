"""
Chatbot manager with session-based chat history.
Uses LangGraph checkpointer for message persistence.
"""

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

from graph import (
    get_session_messages, 
    invoke_chat, 
    stream_chat,
    generate_chat_title
)
from history import (
    create_session, 
    get_session, 
    get_all_sessions,
    update_session_title, 
    update_session_timestamp, 
    delete_session,
    ChatSession
)


class ChatbotManager:
    """
    Manages chatbot functionality with session-based history.
    Messages are persisted via LangGraph's SqliteSaver checkpointer.
    """
    
    def __init__(self):
        """Initialize the chatbot manager and session state."""
        if "current_session_id" not in st.session_state:
            st.session_state.current_session_id = None
        
        # Message history for display (loaded from checkpointer)
        if "message_history" not in st.session_state:
            st.session_state.message_history = []
    
    @property
    def current_session_id(self) -> str | None:
        """Get the current session ID."""
        return st.session_state.current_session_id
    
    @property
    def message_history(self) -> list[dict]:
        """Get the current message history for display."""
        return st.session_state.message_history
    
    @property
    def provider(self) -> str:
        """Get the current provider."""
        return st.session_state.get("provider", "Google")
    
    @property
    def model(self) -> str:
        """Get the current model."""
        return st.session_state.get("model", "gemini-2.5-flash")
    
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
    
    def new_chat(self) -> None:
        """Start a new chat (clears current view, session created on first message)."""
        st.session_state.current_session_id = None
        st.session_state.message_history = []
    
    def _create_session(self) -> ChatSession:
        """Actually create a session in the database."""
        session = create_session(provider=self.provider, model=self.model)
        st.session_state.current_session_id = session.id
        return session
    
    def load_session(self, session_id: str) -> None:
        """Load an existing chat session."""
        session = get_session(session_id)
        if session:
            st.session_state.current_session_id = session_id
            
            # Load messages from LangGraph checkpointer
            messages = get_session_messages(session_id)
            
            # Convert to display format
            temp_messages = []
            for msg in messages:
                if isinstance(msg, HumanMessage):
                    role = 'user'
                else:
                    role = 'assistant'
                temp_messages.append({'role': role, 'content': msg.content})
            
            st.session_state.message_history = temp_messages
    
    def delete_current_session(self) -> None:
        """Delete the current session."""
        if self.current_session_id:
            delete_session(self.current_session_id)
            st.session_state.current_session_id = None
            st.session_state.message_history = []
    
    def get_sessions(self) -> list[ChatSession]:
        """Get all chat sessions."""
        return get_all_sessions()
    
    def ensure_session(self) -> None:
        """Ensure there's an active session, create one if needed."""
        if not self.current_session_id:
            self._create_session()
    
    def display_chat_history(self) -> None:
        """Display all messages in the chat history."""
        for message in self.message_history:
            role = "human" if message['role'] == 'user' else "ai"
            with st.chat_message(role):
                st.markdown(message['content'])
    
    def send_message(self, user_input: str) -> str:
        """
        Send a message and get a response (non-streaming).
        Persists to LangGraph checkpointer.
        """
        self.ensure_session()
        
        # Add user message to display history
        st.session_state.message_history.append({
            'role': 'user', 
            'content': user_input
        })
        
        # Generate title from first message
        if len(st.session_state.message_history) == 1:
            title = generate_chat_title(
                first_message=user_input,
                provider=self.provider,
                model=self.model,
                api_key=self.api_key
            )
            update_session_title(self.current_session_id, title)
        
        # Get response through graph (persists to checkpointer)
        response = invoke_chat(
            user_message=user_input,
            thread_id=self.current_session_id,
            provider=self.provider,
            model=self.model,
            api_key=self.api_key,
            system_prompt=self.system_prompt
        )
        
        # Add AI response to display history
        st.session_state.message_history.append({
            'role': 'assistant', 
            'content': response
        })
        
        # Update session timestamp
        update_session_timestamp(self.current_session_id)
        
        return response
    
    def stream_message(self, user_input: str):
        """
        Stream a message response.
        Persists to LangGraph checkpointer.
        
        Yields:
            Chunks of the response text
        """
        self.ensure_session()
        
        # Add user message to display history
        st.session_state.message_history.append({
            'role': 'user', 
            'content': user_input
        })
        
        # Generate title from first message
        if len(st.session_state.message_history) == 1:
            title = generate_chat_title(
                first_message=user_input,
                provider=self.provider,
                model=self.model,
                api_key=self.api_key
            )
            update_session_title(self.current_session_id, title)
        
        # Stream response through graph
        yield from stream_chat(
            user_message=user_input,
            thread_id=self.current_session_id,
            provider=self.provider,
            model=self.model,
            api_key=self.api_key,
            system_prompt=self.system_prompt
        )
        
        # Update session timestamp
        update_session_timestamp(self.current_session_id)


# Legacy alias
MultiProviderChatbot = ChatbotManager