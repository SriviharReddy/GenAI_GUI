"""
Modern Multi-Provider Chatbot Application
Built with Streamlit and LangGraph for state-of-the-art conversation management.
"""

import streamlit as st
from config import Configuration
from chatbot import ChatbotManager


# Page configuration
st.set_page_config(
    page_title="AI Chatbot | Multi-Provider",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS for better styling
def inject_custom_css():
    """Inject custom CSS for a more polished look."""
    st.markdown("""
    <style>
        /* Main container styling */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Chat message styling */
        .stChatMessage {
            padding: 1rem;
            border-radius: 0.75rem;
        }
        
        /* Input styling */
        .stChatInput {
            border-radius: 1rem;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            padding-top: 1rem;
        }
        
        /* Header styling */
        h1 {
            background: linear-gradient(90deg, #f97316 0%, #ea580c 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        /* Status indicator */
        .status-indicator {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.25rem 0.75rem;
            background: rgba(249, 115, 22, 0.1);
            border-radius: 1rem;
            font-size: 0.875rem;
        }
        
        /* Streaming animation */
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .streaming-indicator {
            animation: pulse 1.5s ease-in-out infinite;
        }
    </style>
    """, unsafe_allow_html=True)


def render_header():
    """Render the application header."""
    provider = st.session_state.get("provider", "AI")
    model = st.session_state.get("model", "")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.title("🤖 AI Chatbot")
        st.caption(f"Powered by **{provider}** via LangGraph")
    
    with col2:
        # Status indicator
        api_key_map = {
            "Google": "gemini_api_key",
            "OpenAI": "openai_api_key", 
            "Anthropic": "anthropic_api_key",
            "Groq": "groq_api_key",
            "OpenRouter": "openrouter_api_key"
        }
        key_name = api_key_map.get(provider, "gemini_api_key")
        has_key = bool(st.session_state.get(key_name, ""))
        
        if has_key:
            st.success(f"✓ {model}", icon="🟢")
        else:
            st.warning("Add API key →", icon="🔴")


def handle_user_input(chatbot: ChatbotManager):
    """Handle user input and generate response."""
    if user_input := st.chat_input("Type your message here...", key="chat_input"):
        # Display user message
        with st.chat_message("human"):
            st.markdown(user_input)
        
        # Add to history
        chatbot.add_message("human", user_input)
        
        # Generate and display AI response
        with st.chat_message("ai"):
            if st.session_state.get("use_streaming", True):
                # Streaming response
                response_placeholder = st.empty()
                full_response = ""
                
                for chunk in chatbot.get_streaming_response(user_input):
                    full_response += chunk
                    response_placeholder.markdown(full_response + "▌")
                
                response_placeholder.markdown(full_response)
                
                if full_response and not full_response.startswith("❌"):
                    chatbot.add_message("ai", full_response)
            else:
                # Non-streaming response
                with st.spinner("Thinking..."):
                    response, error = chatbot.get_response(user_input)
                
                if error:
                    st.error(f"❌ {error}")
                elif response:
                    st.markdown(response)
                    chatbot.add_message("ai", response)


def main():
    """Main application entry point."""
    # Inject custom styling
    inject_custom_css()
    
    # Initialize components
    config = Configuration()
    chatbot = ChatbotManager()
    
    # Render sidebar configuration
    config.render_sidebar()
    
    # Render header
    render_header()
    
    # Add some spacing
    st.markdown("---")
    
    # Display chat history
    chatbot.display_chat_history()
    
    # Handle user input
    handle_user_input(chatbot)


if __name__ == "__main__":
    main()