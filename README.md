# MyAPI Chat

Got an API key? Start chatting in seconds.

Many AI providers offer free tiers or credits to get started:
- **Google Gemini** — free tier with generous limits
- **Groq** — free, incredibly fast inference
- **OpenRouter** — free credits, access to 100+ models
- **OpenAI** / **Anthropic** — paid, but industry standards

This app lets you use any of them through a single interface. Paste your key, pick a model, and go. Keys save locally so you don't re-enter them. Chat history persists across sessions.

Built with LangGraph for proper conversation management—easy to extend with RAG, tools, or multi-agent flows later.

## Screenshots
<img width="2559" height="1427" alt="Screenshot 2025-12-30 190635" src="https://github.com/user-attachments/assets/82721af5-d70d-402e-9714-4bc09922a53c" />


## Quick start

**Requirements:** Python 3.12+

```bash
git clone https://github.com/SriviharReddy/GenAI_GUI.git
cd GenAI_GUI
uv sync  # or: pip install -r requirements.txt
uv run streamlit run app.py
```

Paste your API key in the sidebar. Or add to `.env`:

```env
GEMINI_API_KEY=...
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
GROQ_API_KEY=...
OPENROUTER_API_KEY=...
```

## Where to get keys

| Provider | Link | Notes |
|----------|------|-------|
| Google Gemini | [aistudio.google.com](https://aistudio.google.com/apikey) | Free tier available |
| Groq | [console.groq.com](https://console.groq.com/keys) | Free, very fast |
| OpenRouter | [openrouter.ai](https://openrouter.ai/keys) | Free credits, many models |
| OpenAI | [platform.openai.com](https://platform.openai.com/api-keys) | Paid |
| Anthropic | [console.anthropic.com](https://console.anthropic.com/) | Paid |

## Project structure

```
app.py          - Streamlit UI
chatbot.py      - Session & message management
config.py       - Provider configs, sidebar
graph.py        - LangGraph state machine
history.py      - SQLite chat persistence
```

## Extending

Add a new provider in `config.py`:
```python
PROVIDERS["NewProvider"] = ProviderConfig(
    name="NewProvider",
    env_key="NEW_PROVIDER_API_KEY",
    session_key="new_provider_api_key",
    models=["model-1", "model-2"]
)
```

Then add the LLM init in `graph.py`:
```python
case "NewProvider":
    return ChatNewProvider(model=model, api_key=api_key, ...)
```

## Tech

- LangGraph for state management
- Streamlit for UI  
- SQLite for chat history persistence
- Supports streaming responses

MIT License
