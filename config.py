import streamlit as st
import os
import re
from dotenv import load_dotenv


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
            
            # Provider selection dropdown - now at the top of the sidebar
            provider_options = [
                "Google",
                "OpenAI",
                "Anthropic",
                "Groq",
                "OpenRouter"
            ]
            selected_provider = st.selectbox(
                "Select Provider:",
                options=provider_options,
                index=provider_options.index(st.session_state.provider) if st.session_state.provider in provider_options else 0
            )
            st.session_state.provider = selected_provider
            
            # API key inputs based on selected provider
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