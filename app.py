import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
import os
from dotenv import load_dotenv
import re


class Configuration:
    """Manages configuration settings for the chatbot."""
    
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Initialize session state for configuration
        if "provider" not in st.session_state:
            st.session_state.provider = "Google"
        
        if "gemini_api_key" not in st.session_state:
            st.session_state.gemini_api_key = os.getenv("GEMINI_API_KEY", "")
        
        if "openai_api_key" not in st.session_state:
            st.session_state.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        
        if "anthropic_api_key" not in st.session_state:
            st.session_state.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")
        
        if "groq_api_key" not in st.session_state:
            st.session_state.groq_api_key = os.getenv("GROQ_API_KEY", "")
            
        if "openrouter_api_key" not in st.session_state:
            st.session_state.openrouter_api_key = os.getenv("OPENROUTER_API_KEY", "")
        
        if "model" not in st.session_state:
            st.session_state.model = "gemini-2.5-flash"  # default model for Google
            
        if "system_prompt" not in st.session_state:
            st.session_state.system_prompt = "You are a helpful and friendly AI assistant."
    
    def render_sidebar(self):
        """Render the configuration sidebar."""
        with st.sidebar:
            st.title("Configuration")
            
            # API key inputs based on selected provider (which is now available from top selection)
            if st.session_state.provider == "Google":
                api_key_input = st.text_input(
                    "Enter your Gemini API Key:", 
                    value=st.session_state.gemini_api_key, 
                    type="password",
                    help="API key will be loaded from .env file if not entered here"
                )
                
                if api_key_input and api_key_input != st.session_state.get("last_saved_gemini_api_key", ""):
                    st.session_state.gemini_api_key = api_key_input
                    
                    # Save the API key to .env file if it's different from what's already saved
                    try:
                        # Read the current .env content
                        env_content = ""
                        try:
                            with open(".env", "r") as f:
                                env_content = f.read()
                        except FileNotFoundError:
                            env_content = ""
                        
                        # Update or add the API key in the content
                        if "GEMINI_API_KEY=" in env_content:
                            # Update existing key
                            env_content = re.sub(r"GEMINI_API_KEY=.*", f"GEMINI_API_KEY={api_key_input}", env_content)
                        else:
                            # Add new key
                            if env_content and not env_content.endswith('\n'):
                                env_content += "\n"
                            env_content += f"GEMINI_API_KEY={api_key_input}\n"
                        
                        # Write back to .env file
                        with open(".env", "w") as f:
                            f.write(env_content)
                        
                        # Update the last saved key to avoid repetitive writes
                        st.session_state.last_saved_gemini_api_key = api_key_input
                        
                    except Exception as e:
                        st.warning(f"Could not save API key to .env file: {str(e)}")
            
            elif st.session_state.provider == "OpenAI":
                api_key_input = st.text_input(
                    "Enter your OpenAI API Key:", 
                    value=st.session_state.openai_api_key, 
                    type="password",
                    help="API key will be loaded from .env file if not entered here"
                )
                
                if api_key_input and api_key_input != st.session_state.get("last_saved_openai_api_key", ""):
                    st.session_state.openai_api_key = api_key_input
                    
                    # Save the API key to .env file if it's different from what's already saved
                    try:
                        # Read the current .env content
                        env_content = ""
                        try:
                            with open(".env", "r") as f:
                                env_content = f.read()
                        except FileNotFoundError:
                            env_content = ""
                        
                        # Update or add the API key in the content
                        if "OPENAI_API_KEY=" in env_content:
                            # Update existing key
                            env_content = re.sub(r"OPENAI_API_KEY=.*", f"OPENAI_API_KEY={api_key_input}", env_content)
                        else:
                            # Add new key
                            if env_content and not env_content.endswith('\n'):
                                env_content += "\n"
                            env_content += f"OPENAI_API_KEY={api_key_input}\n"
                        
                        # Write back to .env file
                        with open(".env", "w") as f:
                            f.write(env_content)
                        
                        # Update the last saved key to avoid repetitive writes
                        st.session_state.last_saved_openai_api_key = api_key_input
                        
                    except Exception as e:
                        st.warning(f"Could not save API key to .env file: {str(e)}")
            
            elif st.session_state.provider == "Anthropic":
                api_key_input = st.text_input(
                    "Enter your Anthropic API Key:", 
                    value=st.session_state.anthropic_api_key, 
                    type="password",
                    help="API key will be loaded from .env file if not entered here"
                )
                
                if api_key_input and api_key_input != st.session_state.get("last_saved_anthropic_api_key", ""):
                    st.session_state.anthropic_api_key = api_key_input
                    
                    # Save the API key to .env file if it's different from what's already saved
                    try:
                        # Read the current .env content
                        env_content = ""
                        try:
                            with open(".env", "r") as f:
                                env_content = f.read()
                        except FileNotFoundError:
                            env_content = ""
                        
                        # Update or add the API key in the content
                        if "ANTHROPIC_API_KEY=" in env_content:
                            # Update existing key
                            env_content = re.sub(r"ANTHROPIC_API_KEY=.*", f"ANTHROPIC_API_KEY={api_key_input}", env_content)
                        else:
                            # Add new key
                            if env_content and not env_content.endswith('\n'):
                                env_content += "\n"
                            env_content += f"ANTHROPIC_API_KEY={api_key_input}\n"
                        
                        # Write back to .env file
                        with open(".env", "w") as f:
                            f.write(env_content)
                        
                        # Update the last saved key to avoid repetitive writes
                        st.session_state.last_saved_anthropic_api_key = api_key_input
                        
                    except Exception as e:
                        st.warning(f"Could not save API key to .env file: {str(e)}")
            
            elif st.session_state.provider == "Groq":
                api_key_input = st.text_input(
                    "Enter your Groq API Key:", 
                    value=st.session_state.groq_api_key, 
                    type="password",
                    help="API key will be loaded from .env file if not entered here"
                )
                
                if api_key_input and api_key_input != st.session_state.get("last_saved_groq_api_key", ""):
                    st.session_state.groq_api_key = api_key_input
                    
                    # Save the API key to .env file if it's different from what's already saved
                    try:
                        # Read the current .env content
                        env_content = ""
                        try:
                            with open(".env", "r") as f:
                                env_content = f.read()
                        except FileNotFoundError:
                            env_content = ""
                        
                        # Update or add the API key in the content
                        if "GROQ_API_KEY=" in env_content:
                            # Update existing key
                            env_content = re.sub(r"GROQ_API_KEY=.*", f"GROQ_API_KEY={api_key_input}", env_content)
                        else:
                            # Add new key
                            if env_content and not env_content.endswith('\n'):
                                env_content += "\n"
                            env_content += f"GROQ_API_KEY={api_key_input}\n"
                        
                        # Write back to .env file
                        with open(".env", "w") as f:
                            f.write(env_content)
                        
                        # Update the last saved key to avoid repetitive writes
                        st.session_state.last_saved_groq_api_key = api_key_input
                        
                    except Exception as e:
                        st.warning(f"Could not save API key to .env file: {str(e)}")
            
            elif st.session_state.provider == "OpenRouter":
                api_key_input = st.text_input(
                    "Enter your OpenRouter API Key:", 
                    value=st.session_state.openrouter_api_key, 
                    type="password",
                    help="API key will be loaded from .env file if not entered here"
                )
                
                if api_key_input and api_key_input != st.session_state.get("last_saved_openrouter_api_key", ""):
                    st.session_state.openrouter_api_key = api_key_input
                    
                    # Save the API key to .env file if it's different from what's already saved
                    try:
                        # Read the current .env content
                        env_content = ""
                        try:
                            with open(".env", "r") as f:
                                env_content = f.read()
                        except FileNotFoundError:
                            env_content = ""
                        
                        # Update or add the API key in the content
                        if "OPENROUTER_API_KEY=" in env_content:
                            # Update existing key
                            env_content = re.sub(r"OPENROUTER_API_KEY=.*", f"OPENROUTER_API_KEY={api_key_input}", env_content)
                        else:
                            # Add new key
                            if env_content and not env_content.endswith('\n'):
                                env_content += "\n"
                            env_content += f"OPENROUTER_API_KEY={api_key_input}\n"
                        
                        # Write back to .env file
                        with open(".env", "w") as f:
                            f.write(env_content)
                        
                        # Update the last saved key to avoid repetitive writes
                        st.session_state.last_saved_openrouter_api_key = api_key_input
                        
                    except Exception as e:
                        st.warning(f"Could not save API key to .env file: {str(e)}")
            
            # Model selection dropdown based on provider
            if st.session_state.provider == "Google":
                model_options = [
                    "gemini-2.5-flash",
                    "gemini-2.5-pro",
                    "gemini-2.0-flash",
                    "gemini-1.5-pro",
                    "gemini-1.5-flash",
                    "gemini-1.0-pro"
                ]
            elif st.session_state.provider == "OpenAI":
                model_options = [
                    "gpt-4o",
                    "gpt-4o-mini",
                    "gpt-4-turbo",
                    "gpt-4",
                    "gpt-3.5-turbo"
                ]
            elif st.session_state.provider == "Anthropic":
                model_options = [
                    "claude-3-5-sonnet-20241022",
                    "claude-3-sonnet-20240229",
                    "claude-3-opus-20240229",
                    "claude-3-haiku-20240307"
                ]
            elif st.session_state.provider == "Groq":
                model_options = [
                    "llama-3.1-70b-versatile",
                    "llama-3.1-8b-instant",
                    "llama3-groq-70b-8192-tool-use-preview",
                    "llama3-groq-8b-8192-tool-use-preview",
                    "mixtral-8x7b-32768",
                    "gemma2-9b-it",
                    "gemma-7b-it"
                ]
            elif st.session_state.provider == "OpenRouter":
                model_options = [
                    "openai/gpt-4o",
                    "openai/gpt-4o-mini",
                    "anthropic/claude-3.5-sonnet",
                    "anthropic/claude-3-haiku",
                    "google/gemini-pro",
                    "meta-llama/llama-3.1-405b-instruct",
                    "meta-llama/llama-3.1-70b-instruct",
                    "nousresearch/hermes-3-llama-3.1-405b"
                ]
            
            selected_model = st.selectbox(
                f"Select {st.session_state.provider} Model:",
                options=model_options,
                index=model_options.index(st.session_state.model) if st.session_state.model in model_options else 0
            )
            st.session_state.model = selected_model
            
            # System prompt input
            system_prompt_input = st.text_area(
                "System Prompt:",
                value=st.session_state.system_prompt,
                height=150,
                help="Set the behavior and context for the AI assistant"
            )
            if system_prompt_input:
                st.session_state.system_prompt = system_prompt_input
            
            # Button to clear chat history
            if st.button("Clear Chat"):
                st.session_state.messages = []
            
            st.divider()
            st.markdown("### About")
            st.markdown(f"This is a chatbot powered by {st.session_state.provider} LLM using LangChain and Streamlit.")
            st.markdown("- Enter your API key to get started")
            st.markdown("- Select from various models using the dropdown")
            st.markdown("- Customize AI behavior with the system prompt")


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
        # Provider selection at the very top of the page, above sidebar
        # Provider selection dropdown at the top left of the page
        provider_options = [
            "Google",
            "OpenAI", 
            "Anthropic",
            "Groq",
            "OpenRouter"
        ]
        selected_provider = st.selectbox(
            "Provider:",
            options=provider_options,
            index=provider_options.index(st.session_state.provider) if st.session_state.provider in provider_options else 0,
            key="top_provider_select"
        )
        st.session_state.provider = selected_provider
        
        # Render the sidebar configuration
        self.config.render_sidebar()
        
        # Main title next to the provider selector (in the main content area)
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