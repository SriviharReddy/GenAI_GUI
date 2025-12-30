# 🤖 GenAI GUI - Multi-Provider Chatbot

A modern, feature-rich AI chatbot application built with **Streamlit** and **LangGraph**. Supports multiple AI providers with streaming responses and a clean, intuitive interface.

![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2+-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-red.svg)

## ✨ Features

- **Multi-Provider Support** - Seamlessly switch between:
  - 🟢 Google (Gemini)
  - 🔵 OpenAI (GPT-4, GPT-3.5)
  - 🟣 Anthropic (Claude)
  - 🟠 Groq (LLaMA, Mixtral)
  - 🔴 OpenRouter (access 100+ models)

- **LangGraph Integration** - Modern state machine architecture for:
  - Proper conversation flow management
  - Validation and error handling nodes
  - Extensible graph-based design

- **Streaming Responses** - Real-time token-by-token output with visual feedback

- **Persistent API Keys** - Keys are automatically saved to `.env` file

- **Customizable System Prompts** - Define AI personality and behavior

- **Modern UI** - Polished interface with custom styling

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/GenAI_GUI.git
   cd GenAI_GUI
   ```

2. **Install dependencies**
   
   Using uv (recommended):
   ```bash
   uv sync
   ```
   
   Using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API keys** (optional)
   
   Create a `.env` file:
   ```env
   GEMINI_API_KEY=your_google_api_key
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   GROQ_API_KEY=your_groq_api_key
   OPENROUTER_API_KEY=your_openrouter_api_key
   ```
   
   Or enter them directly in the sidebar—they'll be saved automatically.

4. **Run the application**
   ```bash
   streamlit run app.py
   ```
   
   Or with uv:
   ```bash
   uv run streamlit run app.py
   ```

## 🏗️ Architecture

```
GenAI_GUI/
├── app.py          # Main Streamlit application
├── chatbot.py      # ChatbotManager - UI/Graph interface
├── config.py       # Configuration and sidebar management
├── graph.py        # LangGraph state machine implementation
├── pyproject.toml  # Project configuration
└── requirements.txt
```

### LangGraph Flow

```
┌─────────┐     ┌──────────┐     ┌──────────┐     ┌─────┐
│  START  │ ──► │ validate │ ──► │ generate │ ──► │ END │
└─────────┘     └──────────┘     └──────────┘     └─────┘
                      │                              ▲
                      │          ┌─────────┐         │
                      └────────► │  error  │ ────────┘
                    (on error)   └─────────┘
```

## 📝 Usage

1. **Select a Provider** - Choose from Google, OpenAI, Anthropic, Groq, or OpenRouter
2. **Enter API Key** - Input your API key (auto-saved to `.env`)
3. **Choose a Model** - Select from available models for your provider
4. **Set System Prompt** - Customize the AI's behavior (optional)
5. **Start Chatting!** - Type your message and press Enter

### Streaming Toggle

Enable/disable streaming responses from the sidebar. Streaming provides real-time feedback; disable it for complete responses at once.

## 🔧 Extending the Application

### Adding a New Provider

1. Add the provider configuration in `config.py`:
   ```python
   PROVIDERS["NewProvider"] = ProviderConfig(
       name="NewProvider",
       env_key="NEW_PROVIDER_API_KEY",
       session_key="new_provider_api_key",
       models=["model-1", "model-2"]
   )
   ```

2. Add the LLM initialization in `graph.py`:
   ```python
   case "NewProvider":
       return ChatNewProvider(
           model=model,
           api_key=api_key,
           temperature=0.7,
           streaming=True
       )
   ```

### Adding Custom Nodes to the Graph

Edit `graph.py` to add new nodes:

```python
def my_custom_node(state: ChatState) -> ChatState:
    # Your custom logic here
    return state

# In build_chat_graph():
graph_builder.add_node("custom", my_custom_node)
graph_builder.add_edge("validate", "custom")
graph_builder.add_edge("custom", "generate")
```

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `langchain` | Core LLM abstractions |
| `langgraph` | Graph-based state management |
| `langchain-*` | Provider integrations |
| `streamlit` | Web UI framework |
| `python-dotenv` | Environment variable management |

## 📄 License

MIT License - feel free to use this project for learning and development!

---

Built with ❤️ using LangGraph and Streamlit
