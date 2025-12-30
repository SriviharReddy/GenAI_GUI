"""
Configuration management for the multi-provider chatbot.
Handles API keys, model selection, and sidebar UI.
"""

import streamlit as st
import os
import re
from pathlib import Path
from dotenv import load_dotenv
from dataclasses import dataclass


@dataclass
class ProviderConfig:
    """Configuration for a single provider."""
    name: str
    env_key: str
    session_key: str
    models: list[str]


# Provider configurations
PROVIDERS: dict[str, ProviderConfig] = {
    "Google": ProviderConfig(
        name="Google",
        env_key="GEMINI_API_KEY",
        session_key="gemini_api_key",
        models=[
            "gemini-3-pro",
            "gemini-3-flash",
            "gemini-2.5-pro",
            "gemini-2.5-flash",
            "gemini-2.5-flash-lite",
            "gemini-2.0-flash",
        ]
    ),
    "OpenAI": ProviderConfig(
        name="OpenAI",
        env_key="OPENAI_API_KEY",
        session_key="openai_api_key",
        models=[
            "gpt-5.2",
            "gpt-5",
            "gpt-5-mini",
            "o3",
            "o3-mini",
            "o1",
            "gpt-4o",
        ]
    ),
    "Anthropic": ProviderConfig(
        name="Anthropic",
        env_key="ANTHROPIC_API_KEY",
        session_key="anthropic_api_key",
        models=[
            "claude-opus-4.5",
            "claude-sonnet-4.5",
            "claude-haiku-4.5",
            "claude-opus-4",
            "claude-sonnet-4",
            "claude-3.5-sonnet-20241022",
        ]
    ),
    "Groq": ProviderConfig(
        name="Groq",
        env_key="GROQ_API_KEY",
        session_key="groq_api_key",
        models=[
            "llama-4-maverick-17b-128e-instruct",
            "llama-4-scout-17b-16e-instruct",
            "llama-3.3-70b-versatile",
            "llama-3.3-70b-specdec",
            "deepseek-r1-distill-llama-70b",
            "qwen-qwq-32b",
            "mixtral-8x7b-32768",
        ]
    ),
    "OpenRouter": ProviderConfig(
        name="OpenRouter",
        env_key="OPENROUTER_API_KEY",
        session_key="openrouter_api_key",
        models=[
            "google/gemini-3-pro",
            "openai/gpt-5.2",
            "anthropic/claude-opus-4.5",
            "anthropic/claude-sonnet-4.5",
            "meta-llama/llama-4-maverick",
            "deepseek/deepseek-v3",
            "xai/grok-code-fast-1",
            "qwen/qwen-2.5-coder-32b-instruct",
            "mistralai/devstral-2",
        ]
    )
}


class Configuration:
    """Manages configuration settings for the chatbot."""
    
    def __init__(self):
        """Initialize configuration and load environment variables."""
        load_dotenv()
        self._init_session_state()
    
    def _init_session_state(self) -> None:
        """Initialize all session state variables."""
        # Provider selection
        if "provider" not in st.session_state:
            st.session_state.provider = "Google"
        
        # API keys from environment
        for provider in PROVIDERS.values():
            if provider.session_key not in st.session_state:
                st.session_state[provider.session_key] = os.getenv(provider.env_key, "")
        
        # Model selection (default to first model of selected provider)
        if "model" not in st.session_state:
            st.session_state.model = PROVIDERS["Google"].models[0]
        
        # System prompt
        if "system_prompt" not in st.session_state:
            st.session_state.system_prompt = "You are a helpful and friendly AI assistant."
        
        # Streaming preference
        if "use_streaming" not in st.session_state:
            st.session_state.use_streaming = True
    
    def _save_api_key_to_env(self, env_key: str, api_key: str) -> None:
        """
        Save an API key to the .env file.
        
        Args:
            env_key: The environment variable name
            api_key: The API key value
        """
        env_path = Path(".env")
        
        try:
            env_content = ""
            if env_path.exists():
                env_content = env_path.read_text()
            
            # Update or add the key
            pattern = f"{env_key}=.*"
            if re.search(pattern, env_content):
                env_content = re.sub(pattern, f"{env_key}={api_key}", env_content)
            else:
                if env_content and not env_content.endswith('\n'):
                    env_content += "\n"
                env_content += f"{env_key}={api_key}\n"
            
            env_path.write_text(env_content)
            
        except Exception as e:
            st.warning(f"Could not save API key to .env file: {e}")
    
    def _render_api_key_input(self, provider_config: ProviderConfig) -> None:
        """
        Render the API key input for a provider.
        
        Args:
            provider_config: The provider configuration
        """
        current_key = st.session_state.get(provider_config.session_key, "")
        last_saved_key = st.session_state.get(f"last_saved_{provider_config.session_key}", "")
        
        api_key_input = st.text_input(
            f"Enter your {provider_config.name} API Key:",
            value=current_key,
            type="password",
            help="API key will be loaded from .env file if available"
        )
        
        if api_key_input and api_key_input != last_saved_key:
            st.session_state[provider_config.session_key] = api_key_input
            self._save_api_key_to_env(provider_config.env_key, api_key_input)
            st.session_state[f"last_saved_{provider_config.session_key}"] = api_key_input
    
    def _render_model_selector(self, provider_config: ProviderConfig) -> None:
        """
        Render the model selector for a provider.
        
        Args:
            provider_config: The provider configuration
        """
        models = provider_config.models
        current_model = st.session_state.model
        
        # If current model isn't in this provider's list, default to first
        default_index = 0
        if current_model in models:
            default_index = models.index(current_model)
        
        selected_model = st.selectbox(
            f"Select {provider_config.name} Model:",
            options=models,
            index=default_index
        )
        st.session_state.model = selected_model
    
    def render_sidebar(self) -> None:
        """Render the complete configuration sidebar."""
        with st.sidebar:
            st.title("⚙️ Configuration")
            
            # Provider selection
            st.subheader("Provider")
            provider_names = list(PROVIDERS.keys())
            current_provider_index = provider_names.index(st.session_state.provider) \
                if st.session_state.provider in provider_names else 0
            
            selected_provider = st.selectbox(
                "Select Provider:",
                options=provider_names,
                index=current_provider_index,
                label_visibility="collapsed"
            )
            st.session_state.provider = selected_provider
            
            provider_config = PROVIDERS[selected_provider]
            
            # Divider
            st.divider()
            
            # API Key
            st.subheader("🔑 API Key")
            self._render_api_key_input(provider_config)
            
            # Divider
            st.divider()
            
            # Model Selection
            st.subheader("🤖 Model")
            self._render_model_selector(provider_config)
            
            # Divider
            st.divider()
            
            # Streaming toggle
            st.subheader("⚡ Options")
            st.session_state.use_streaming = st.toggle(
                "Enable Streaming",
                value=st.session_state.use_streaming,
                help="Stream responses token by token"
            )
            
            # Divider
            st.divider()
            
            # System Prompt
            st.subheader("📝 System Prompt")
            system_prompt = st.text_area(
                "System Prompt:",
                value=st.session_state.system_prompt,
                height=120,
                help="Define the AI's behavior and personality",
                label_visibility="collapsed"
            )
            if system_prompt:
                st.session_state.system_prompt = system_prompt
            
            # Divider
            st.divider()
            
            # Clear chat button
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
            
            # Display current config
            st.divider()
            st.caption(f"**Current:** {selected_provider} / {st.session_state.model}")