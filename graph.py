"""
LangGraph-based chatbot graph implementation.
Uses SqliteSaver for persistent state checkpointing.
SECURITY: Only messages are persisted - API keys are never stored.
"""

import sqlite3
from typing import Annotated
from typing_extensions import TypedDict

from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver


# Database connection for checkpointer
DB_PATH = "chat_history.db"
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)


class ChatState(TypedDict):
    """
    State schema for the chatbot graph.
    SECURITY: Only 'messages' is persisted by the checkpointer.
    Sensitive fields (api_key) are passed at runtime and NOT stored.
    """
    messages: Annotated[list[BaseMessage], add_messages]


def create_llm(provider: str, model: str, api_key: str):
    """Create the appropriate LLM based on the provider."""
    match provider:
        case "Google":
            return ChatGoogleGenerativeAI(
                model=model,
                google_api_key=api_key,
                temperature=0.7,
            )
        case "OpenAI":
            return ChatOpenAI(
                model=model,
                openai_api_key=api_key,
                temperature=0.7,
            )
        case "Anthropic":
            return ChatAnthropic(
                model=model,
                anthropic_api_key=api_key,
                temperature=0.7,
            )
        case "Groq":
            return ChatGroq(
                model=model,
                groq_api_key=api_key,
                temperature=0.7,
            )
        case "OpenRouter":
            return ChatOpenAI(
                model=model,
                openai_api_key=api_key,
                temperature=0.7,
                base_url="https://openrouter.ai/api/v1"
            )
        case _:
            raise ValueError(f"Unknown provider: {provider}")


# Simple graph that just persists messages
def passthrough(state: ChatState) -> dict:
    """Passthrough node - actual LLM call happens outside graph for security."""
    return {}


# Build the graph - just for message persistence
graph = StateGraph(ChatState)
graph.add_node("chat", passthrough)
graph.add_edge(START, "chat")
graph.add_edge("chat", END)

# Compile with checkpointer for persistence
chatbot = graph.compile(checkpointer=checkpointer)


def get_thread_config(thread_id: str) -> dict:
    """Get the config dict for a specific thread."""
    return {"configurable": {"thread_id": thread_id}}


def get_session_messages(thread_id: str) -> list[BaseMessage]:
    """Get all messages for a thread from the checkpoint."""
    try:
        state = chatbot.get_state(config=get_thread_config(thread_id))
        if state and state.values:
            return state.values.get("messages", [])
    except Exception:
        pass
    return []


def save_messages(thread_id: str, messages: list[BaseMessage]) -> None:
    """Save messages to the checkpoint."""
    config = get_thread_config(thread_id)
    chatbot.invoke({"messages": messages}, config=config)


def invoke_chat(
    user_message: str,
    thread_id: str,
    provider: str,
    model: str,
    api_key: str,
    system_prompt: str = ""
) -> str:
    """
    Send a message and get a response.
    API key is used at runtime but NEVER persisted.
    
    Returns:
        The AI response content
    """
    if not api_key:
        return f"Please enter your {provider} API key in the sidebar!"
    
    try:
        # Get existing messages from checkpoint
        existing_messages = get_session_messages(thread_id)
        
        # Create LLM with runtime credentials (not persisted)
        llm = create_llm(provider, model, api_key)
        
        # Build messages with system prompt for LLM call
        llm_messages = []
        if system_prompt:
            llm_messages.append(SystemMessage(content=system_prompt))
        llm_messages.extend(existing_messages)
        llm_messages.append(HumanMessage(content=user_message))
        
        # Generate response
        response = llm.invoke(llm_messages)
        
        # Save both user message and AI response to checkpoint
        # Only messages are persisted, NOT the api_key
        save_messages(thread_id, [
            HumanMessage(content=user_message),
            response
        ])
        
        return response.content
        
    except Exception as e:
        return f"Error: {str(e)}"


def stream_chat(
    user_message: str,
    thread_id: str,
    provider: str,
    model: str,
    api_key: str,
    system_prompt: str = ""
):
    """
    Stream a chat response.
    API key is used at runtime but NEVER persisted.
    
    Yields:
        Chunks of the response text
    """
    if not api_key:
        yield f"Please enter your {provider} API key in the sidebar!"
        return
    
    try:
        # Get existing messages from checkpoint
        existing_messages = get_session_messages(thread_id)
        
        # Create LLM with runtime credentials (not persisted)
        llm = create_llm(provider, model, api_key)
        
        # Build messages with system prompt for LLM call
        llm_messages = []
        if system_prompt:
            llm_messages.append(SystemMessage(content=system_prompt))
        llm_messages.extend(existing_messages)
        llm_messages.append(HumanMessage(content=user_message))
        
        # Stream response
        full_response = ""
        for chunk in llm.stream(llm_messages):
            if chunk.content:
                full_response += chunk.content
                yield chunk.content
        
        # Save messages to checkpoint after streaming completes
        save_messages(thread_id, [
            HumanMessage(content=user_message),
            AIMessage(content=full_response)
        ])
                
    except Exception as e:
        yield f"Error: {str(e)}"


def generate_chat_title(
    first_message: str,
    provider: str,
    model: str,
    api_key: str
) -> str:
    """Generate a short chat title using the LLM."""
    if not api_key:
        return first_message[:40] + ("..." if len(first_message) > 40 else "")
    
    try:
        llm = create_llm(provider, model, api_key)
        
        prompt = f"""Generate a very short title (max 5 words) for a chat that starts with this message. 
Reply with ONLY the title, no quotes, no punctuation at the end.

Message: {first_message[:200]}"""
        
        response = llm.invoke([HumanMessage(content=prompt)])
        title = response.content.strip().strip('"\'')
        
        if len(title) > 50:
            title = title[:47] + "..."
            
        return title
        
    except Exception:
        return first_message[:40] + ("..." if len(first_message) > 40 else "")
