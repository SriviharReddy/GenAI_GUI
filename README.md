# GenAI GUI

A multi-provider AI chatbot built with Streamlit and LangGraph. Started as a learning project when I was getting into LangChain, now upgraded to use modern patterns.

## What it does

Switch between different AI providers (Google, OpenAI, Anthropic, Groq, OpenRouter) without changing code. API keys persist to `.env` so you don't have to re-enter them. Responses stream in real-time.

Under the hood, it uses LangGraph for conversation flow—validation, generation, and error handling are separate nodes in a state machine. This makes it easy to extend later (RAG, tools, multi-agent, etc).

## Setup

**Requirements:** Python 3.12+

```bash
# Clone and install
git clone https://github.com/SriviharReddy/GenAI_GUI.git
cd GenAI_GUI
uv sync  # or: pip install -r requirements.txt

# Run
uv run streamlit run app.py  # or: streamlit run app.py
```

API keys can go in a `.env` file or just paste them in the sidebar—they'll save automatically.

```env
GEMINI_API_KEY=...
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
GROQ_API_KEY=...
OPENROUTER_API_KEY=...
```

## Project structure

```
app.py          - Streamlit UI
chatbot.py      - Bridges UI and graph
config.py       - Provider configs, sidebar
graph.py        - LangGraph state machine
```

The graph flow is simple:

```
START → validate → generate → END
              ↓
            error → END
```

## Adding providers

1. Add config in `config.py`:
```python
PROVIDERS["NewProvider"] = ProviderConfig(
    name="NewProvider",
    env_key="NEW_PROVIDER_API_KEY",
    session_key="new_provider_api_key",
    models=["model-1", "model-2"]
)
```

2. Add LLM init in `graph.py`:
```python
case "NewProvider":
    return ChatNewProvider(model=model, api_key=api_key, ...)
```

## Adding graph nodes

```python
def my_node(state: ChatState) -> ChatState:
    # do something
    return state

# in build_chat_graph():
graph_builder.add_node("my_node", my_node)
graph_builder.add_edge("validate", "my_node")
graph_builder.add_edge("my_node", "generate")
```

## Dependencies

- `langchain` / `langgraph` - LLM framework
- `langchain-google-genai`, `langchain-openai`, etc. - provider integrations  
- `streamlit` - web UI
- `python-dotenv` - env file loading

MIT License
