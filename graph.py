"""
LangGraph-based chatbot graph implementation.
Uses SqliteSaver for persistent state checkpointing.
"""

import sqlite3
from typing import Annotated, Literal
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
    """State schema for the chatbot graph."""
    messages: Annotated[list[BaseMessage], add_messages]
    provider: str
    model: str
    api_key: str
    system_prompt: str


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


def chat_node(state: ChatState) -> dict:
    """Process a chat message and generate a response."""
    provider = state["provider"]
    model = state["model"]
    api_key = state["api_key"]
    system_prompt = state.get("system_prompt", "")
    
    if not api_key:
        return {"messages": [AIMessage(content=f"Please enter your {provider} API key in the sidebar!")]}
    
    try:
        llm = create_llm(provider, model, api_key)
        
        # Build messages with system prompt
        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        messages.extend(state["messages"])
        
        # Generate response
        response = llm.invoke(messages)
        return {"messages": [response]}
        
    except Exception as e:
        return {"messages": [AIMessage(content=f"Error: {str(e)}")]}


# Build the graph
graph = StateGraph(ChatState)
graph.add_node("chat", chat_node)
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


def retrieve_all_threads() -> list[str]:
    """Retrieve all thread IDs from the checkpointer."""
    all_threads = set()
    try:
        for checkpoint in checkpointer.list(None):
            thread_id = checkpoint.config.get('configurable', {}).get('thread_id')
            if thread_id:
                all_threads.add(thread_id)
    except Exception:
        pass
    return list(all_threads)


def invoke_chat(
    user_message: str,
    thread_id: str,
    provider: str,
    model: str,
    api_key: str,
    system_prompt: str = ""
) -> str:
    """
    Send a message and get a response, with persistence.
    
    Returns:
        The AI response content
    """
    config = get_thread_config(thread_id)
    
    result = chatbot.invoke(
        {
            "messages": [HumanMessage(content=user_message)],
            "provider": provider,
            "model": model,
            "api_key": api_key,
            "system_prompt": system_prompt,
        },
        config=config
    )
    
    # Get the last AI message
    for msg in reversed(result["messages"]):
        if isinstance(msg, AIMessage):
            return msg.content
    
    return "No response generated"


def stream_chat(
    user_message: str,
    thread_id: str,
    provider: str,
    model: str,
    api_key: str,
    system_prompt: str = ""
):
    """
    Stream a chat response with persistence.
    
    Yields:
        Chunks of the response text
    """
    config = get_thread_config(thread_id)
    
    # First, we need to add the user message to state and generate response
    # For streaming, we invoke the graph then stream from the final message
    
    try:
        # Stream using LangGraph's stream mode
        for chunk, metadata in chatbot.stream(
            {
                "messages": [HumanMessage(content=user_message)],
                "provider": provider,
                "model": model,
                "api_key": api_key,
                "system_prompt": system_prompt,
            },
            config=config,
            stream_mode="messages"
        ):
            if hasattr(chunk, 'content') and chunk.content:
                yield chunk.content
                
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
