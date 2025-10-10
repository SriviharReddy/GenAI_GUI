import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up the page configuration
st.set_page_config(
    page_title="Gemini Chatbot",
    page_icon="💬",
    layout="wide"
)

# Initialize session state for API key, messages, model, and system prompt
if "api_key" not in st.session_state:
    st.session_state.api_key = os.getenv("GEMINI_API_KEY", "")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "model" not in st.session_state:
    st.session_state.model = "gemini-2.5-flash"  # default model

if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = "You are a helpful and friendly AI assistant."

# Sidebar for API key input
with st.sidebar:
    st.title("Configuration")
    api_key_input = st.text_input(
        "Enter your Gemini API Key:", 
        value=st.session_state.api_key, 
        type="password",
        help="API key will be loaded from .env file if not entered here"
    )
    if api_key_input and api_key_input != st.session_state.get("last_saved_api_key", ""):
        st.session_state.api_key = api_key_input
        
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
            import re
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
            st.session_state.last_saved_api_key = api_key_input
            
        except Exception as e:
            st.warning(f"Could not save API key to .env file: {str(e)}")
    
    # Model selection dropdown
    model_options = [
        "gemini-2.5-flash",
        "gemini-2.5-pro",
        "gemini-2.0-flash",
        "gemini-1.5-pro",
        "gemini-1.5-flash",
        "gemini-1.0-pro"
    ]
    selected_model = st.selectbox(
        "Select Gemini Model:",
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
    st.markdown("This is a chatbot powered by Google's Gemini LLM using LangChain and Streamlit.")
    st.markdown("- Enter your API key to get started")
    st.markdown("- Select from various Gemini models using the dropdown")
    st.markdown("- Customize AI behavior with the system prompt")

# Main title
st.title("🤖 Gemini Chatbot")
st.caption("Powered by Google's Gemini via LangChain")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message.type):
        st.write(message.content)

# Function to get response from Gemini
def get_gemini_response(user_input):
    if not st.session_state.api_key:
        st.error("Please enter your Gemini API key in the sidebar!")
        return None

    try:
        # Initialize the model with the API key and selected model
        llm = ChatGoogleGenerativeAI(
            model=st.session_state.model,
            google_api_key=st.session_state.api_key,
            temperature=0.7
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

# Chat input
if user_input := st.chat_input("Type your message here..."):
    # Add user message to session state
    st.session_state.messages.append(HumanMessage(content=user_input))
    
    # Display user message in chat
    with st.chat_message("human"):
        st.write(user_input)
    
    # Get and display AI response
    with st.chat_message("ai"):
        with st.spinner("Thinking..."):
            response = get_gemini_response(user_input)
            if response:
                st.write(response)
                # Add AI message to session state
                st.session_state.messages.append(AIMessage(content=response))