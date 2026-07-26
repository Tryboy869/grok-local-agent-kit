# 🚀 Grok Local Agent Kit

[![GitHub stars](https://img.shields.io/github/stars/Tryboy869/grok-local-agent-kit?style=social)](https://github.com/Tryboy869/grok-local-agent-kit/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![CI](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/Tryboy869/grok-local-agent-kit/actions)
[![PyPI](https://img.shields.io/pypi/v/grok-local-agent-kit.svg)](https://pypi.org/project/grok-local-agent-kit/)

**The open-source toolkit for powerful, offline-first AI agents.**  
Run autonomous agents locally with Ollama, real tool calling, and a simple ReAct loop. No cloud API keys required.

Built autonomously by Grok to democratize agentic AI.

## ✨ Features

- **Local-first** — Works with any Ollama model (llama3.2, mistral, qwen, etc.)
- **Tool calling** — Web search, Python execution, file system tools out of the box
- **ReAct-style loop** — Agent plans → calls tools → observes → answers
- **CLI + Python SDK** — `grok-agent chat` or `from grok_local_agent_kit import create_agent`
- **Extensible** — Register your own tools in 3 lines of code
- **MCP-ready foundation** — Designed for future Multi-Context Protocol integration
- **Rich terminal UI** — Beautiful output with the `rich` library
- **MIT licensed** — Use it commercially, fork it, ship it

## 🚀 Quickstart

### 1. Prerequisites
```bash
# Install Ollama → https://ollama.com
ollama pull llama3.2
```

### 2. Install the kit
```bash
pip install grok-local-agent-kit
# or from source
pip install -e .
```

### 3. Chat from the terminal
```bash
grok-agent chat "What files are in the current directory? Summarize the project."
# or interactive mode
grok-agent repl
```

### 4. Use in Python
```python
from grok_local_agent_kit import create_agent

agent = create_agent(model="llama3.2")
print(agent.run("Search for the latest news about local LLMs and summarize."))
```

## 🛠️ Built-in Tools

| Tool              | Description                                      |
|-------------------|--------------------------------------------------|
| `web_search`      | DuckDuckGo search (no API key)                   |
| `execute_python`  | Run short Python snippets safely                 |
| `list_directory`  | List files in a folder                           |
| `read_file`       | Read text file content                           |

Add your own:
```python
from grok_local_agent_kit import create_agent
from grok_local_agent_kit.tools import Tool

def my_tool(city: str) -> str:
    return f"Weather in {city}: sunny ☀️"

agent = create_agent()
agent.register_tool(Tool(
    name="weather",
    description="Get fake weather",
    func=my_tool,
    parameters={"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]}
))
```

## 📖 Examples

See the [`examples/`](examples/) folder:
- `chat_agent.py` — Interactive REPL
- `automation_agent.py` — Goal-driven autonomous run

## 🗺️ Roadmap

| Version | Goals                                      | Status     |
|---------|--------------------------------------------|------------|
| 0.4.0   | Solid ReAct agent + tools + CLI + tests    | ✅ Current |
| 0.5.0   | Native Ollama tool-calling API + streaming | Next       |
| 0.6.0   | Multi-agent orchestration                  | Planned    |
| 1.0.0   | Full MCP server/client + vision            | Planned    |
| 2.0.0   | Agent marketplace + distributed runtime    | Future     |

See [ROADMAP.md](ROADMAP.md) for details.

## 🤝 Contributing

PRs and stars are extremely welcome!  
See [CONTRIBUTING.md](CONTRIBUTING.md).

```bash
git clone https://github.com/Tryboy869/grok-local-agent-kit.git
cd grok-local-agent-kit
pip install -e ".[dev]"
pytest
```

## 📄 License

MIT © 2026 Tryboy869 & Grok

---

⭐ **If this project helps you, please star it!**  
Goal: 10 000 stars — help make local agents mainstream.
