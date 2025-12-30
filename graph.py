"""
LangGraph-based chatbot graph implementation.
Uses SqliteSaver for persistent state checkpointing.
"""

from typing import Annotated, Literal
from typing_extensions import TypedDict

from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from history import get_checkpointer


class ChatState(TypedDict):
    """State schema for the chatbot graph."""
    messages: Annotated[list[BaseMessage], add_messages]
    provider: str
    model: str
    api_key: str
    system_prompt: str
    error: str | None


def create_llm(state: ChatState):
    """Create the appropriate LLM based on the provider."""
    provider = state["provider"]
    model = state["model"]
    api_key = state["api_key"]
    
    match provider:
        case "Google":
            return ChatGoogleGenerativeAI(
                model=model,
                google_api_key=api_key,
                temperature=0.7,
                streaming=True
            )
        case "OpenAI":
            return ChatOpenAI(
                model=model,
                openai_api_key=api_key,
                temperature=0.7,
                streaming=True
            )
        case "Anthropic":
            return ChatAnthropic(
                model=model,
                anthropic_api_key=api_key,
                temperature=0.7,
                streaming=True
            )
        case "Groq":
            return ChatGroq(
                model=model,
                groq_api_key=api_key,
                temperature=0.7,
                streaming=True
            )
        case "OpenRouter":
            return ChatOpenAI(
                model=model,
                openai_api_key=api_key,
                temperature=0.7,
                streaming=True,
                base_url="https://openrouter.ai/api/v1"
            )
        case _:
            raise ValueError(f"Unknown provider: {provider}")


def validate_input(state: ChatState) -> ChatState:
    """Validate that we have the required configuration."""
    if not state.get("api_key"):
        return {**state, "error": f"Please enter your {state['provider']} API key in the sidebar!"}
    if not state.get("messages"):
        return {**state, "error": "No messages to process"}
    return {**state, "error": None}


def should_continue(state: ChatState) -> Literal["generate", "error"]:
    """Determine if we should continue to generate or handle error."""
    if state.get("error"):
        return "error"
    return "generate"


def generate_response(state: ChatState) -> ChatState:
    """Generate a response from the LLM."""
    try:
        llm = create_llm(state)
        
        # Build messages with system prompt
        messages = []
        if state.get("system_prompt"):
            messages.append(SystemMessage(content=state["system_prompt"]))
        
        # Add conversation history
        messages.extend(state["messages"])
        
        # Generate response
        response = llm.invoke(messages)
        
        return {
            **state,
            "messages": [response],
            "error": None
        }
    except Exception as e:
        return {**state, "error": str(e)}


def handle_error(state: ChatState) -> ChatState:
    """Handle any errors that occurred."""
    error_message = state.get("error", "An unknown error occurred")
    return {
        **state,
        "messages": [AIMessage(content=f"Error: {error_message}")],
    }


def build_chat_graph(checkpointer=None):
    """Build and compile the chat graph with optional checkpointer."""
    graph_builder = StateGraph(ChatState)
    
    # Add nodes
    graph_builder.add_node("validate", validate_input)
    graph_builder.add_node("generate", generate_response)
    graph_builder.add_node("error", handle_error)
    
    # Add edges
    graph_builder.add_edge(START, "validate")
    graph_builder.add_conditional_edges(
        "validate",
        should_continue,
        {
            "generate": "generate",
            "error": "error"
        }
    )
    graph_builder.add_edge("generate", END)
    graph_builder.add_edge("error", END)
    
    # Compile with checkpointer for persistence
    return graph_builder.compile(checkpointer=checkpointer)


# Create graph with SQLite checkpointer for persistence
checkpointer = get_checkpointer()
chat_graph = build_chat_graph(checkpointer=checkpointer)


def get_thread_config(session_id: str) -> dict:
    """Get the config dict for a specific thread/session."""
    return {"configurable": {"thread_id": session_id}}


def get_session_messages(session_id: str) -> list[BaseMessage]:
    """Get all messages for a session from the checkpoint."""
    config = get_thread_config(session_id)
    try:
        state = chat_graph.get_state(config)
        if state and state.values:
            return state.values.get("messages", [])
    except Exception:
        pass
    return []


def get_chat_response(
    messages: list[BaseMessage],
    provider: str,
    model: str,
    api_key: str,
    system_prompt: str = "",
    session_id: str = ""
) -> tuple[str | None, str | None]:
    """
    Get a response from the chat graph with persistence.
    
    Returns:
        tuple: (response_content, error_message)
    """
    initial_state: ChatState = {
        "messages": messages,
        "provider": provider,
        "model": model,
        "api_key": api_key,
        "system_prompt": system_prompt,
        "error": None
    }
    
    config = get_thread_config(session_id) if session_id else None
    result = chat_graph.invoke(initial_state, config=config)
    
    if result.get("error"):
        return None, result["error"]
    
    # Get the last AI message from the result
    for msg in reversed(result["messages"]):
        if isinstance(msg, AIMessage):
            return msg.content, None
    
    return None, "No response generated"


def stream_chat_response(
    messages: list[BaseMessage],
    provider: str,
    model: str,
    api_key: str,
    system_prompt: str = "",
    session_id: str = ""
):
    """
    Stream a response from the LLM.
    Note: Streaming doesn't use the graph directly for real-time output.
    
    Yields:
        str: Chunks of the response text
    """
    if not api_key:
        yield f"Please enter your {provider} API key in the sidebar!"
        return
    
    try:
        state: ChatState = {
            "messages": messages,
            "provider": provider,
            "model": model,
            "api_key": api_key,
            "system_prompt": system_prompt,
            "error": None
        }
        
        llm = create_llm(state)
        
        # Build messages with system prompt
        all_messages = []
        if system_prompt:
            all_messages.append(SystemMessage(content=system_prompt))
        all_messages.extend(messages)
        
        # Stream response
        for chunk in llm.stream(all_messages):
            if chunk.content:
                yield chunk.content
                
    except Exception as e:
        yield f"Error: {str(e)}"
