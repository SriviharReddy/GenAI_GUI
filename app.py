import streamlit as st
from config import Configuration
from chatbot import MultiProviderChatbot


class Application:
    """Main application class that manages the Streamlit UI and overall flow."""
    
    def __init__(self):
        # Set up the page configuration
        st.set_page_config(
            page_title="Multi-Provider Chatbot",
            page_icon="💬",
            layout="wide"
        )
        
        # Initialize components
        self.config = Configuration()
        self.chatbot = MultiProviderChatbot()
    
    def run(self):
        """Run the main application."""
        # Render the sidebar configuration (which now includes provider selection)
        self.config.render_sidebar()
        
        # Main title (now without the provider in the title since it's in the sidebar)
        st.title(f"🤖 {st.session_state.provider} Chatbot")
        st.caption(f"Powered by {st.session_state.provider} via LangChain")
        
        # Display chat history
        self.chatbot.display_chat_history()
        
        # Handle user input
        if user_input := st.chat_input("Type your message here..."):
            # Add user message to chat history
            self.chatbot.add_message("human", user_input)
            
            # Display user message
            with st.chat_message("human"):
                st.write(user_input)
            
            # Get and display AI response
            with st.chat_message("ai"):
                with st.spinner("Thinking..."):
                    response = self.chatbot.get_response(user_input)
                    if response:
                        st.write(response)
                        # Add AI message to chat history
                        self.chatbot.add_message("ai", response)


# Run the application
if __name__ == "__main__":
    app = Application()
    app.run()