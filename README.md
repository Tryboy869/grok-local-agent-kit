# 🚀 Grok Local Agent Kit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![CI](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/Tryboy869/grok-local-agent-kit/actions)
[![Version](https://img.shields.io/badge/version-0.6.0-green.svg)](https://github.com/Tryboy869/grok-local-agent-kit)

**Open-source toolkit for building powerful local AI agents.**  
Ollama + LM Studio • real tool calling • MCP-ready • offline-first.  
Built autonomously by Grok.

---

## ✨ Features (v0.6.0)

| Feature | Status |
|---------|--------|
| Multi-LLM (Ollama native + OpenAI-compatible / LM Studio) | ✅ |
| ReAct-style tool calling loop | ✅ |
| Tools: web search, read/write/list files (cwd-safe), safe shell, execute_python, calculator | ✅ |
| Tool-result truncation & clearer LLM errors | ✅ |
| Provider aliases (`lmstudio` → OpenAI-compat) | ✅ |
| Enhanced MCP stub (list resources/tools + call) | ✅ |
| CLI (`grok-agent chat / doctor`) | ✅ |
| Ready-to-run examples (chat, automation, research) | ✅ |
| One-command install | ✅ |
| Unit tests (no live LLM required) | ✅ |

---

## ⚡ Quick start (1 command)

```bash
pip install git+https://github.com/Tryboy869/grok-local-agent-kit.git
```

Or from source:

```bash
git clone https://github.com/Tryboy869/grok-local-agent-kit.git
cd grok-local-agent-kit
pip install -e .
```

### Prerequisites

1. **Ollama** (recommended)  
   ```bash
   # install from https://ollama.com then:
   ollama pull llama3.2
   ```

2. **Or LM Studio**  
   Start the local server (default `http://localhost:1234`).

### Run

```bash
# Interactive chat
grok-agent chat

# One-shot
grok-agent chat "Search the web for local AI agents and summarize"

# With LM Studio
grok-agent chat --provider lmstudio --model your-model-name

# Health check
grok-agent doctor
```

### Python

```python
from grok_local_agent_kit import create_agent

agent = create_agent(model="llama3.2", provider="ollama", verbose=True)
print(agent.run("List files in the current directory and create a hello.txt"))
agent.close()
```

---

## 🎬 Demo (described)

> **GIF 1 – Chat agent**  
> Terminal shows `You › What files are here?` → agent calls `list_files` → returns directory listing → answers in natural language.

> **GIF 2 – Automation**  
> `python examples/automation_agent.py` → creates `hello_from_agent.py`, lists dir, runs calculator, web search, prints final summary.

> **GIF 3 – Research**  
> `python examples/research_agent.py --topic "MCP protocol"` → web_search → writes `research_YYYYMMDD_HHMM.md` → short confirmation.

> **GIF 4 – LM Studio**  
> Same chat flow with `--provider lmstudio`, model selector visible in LM Studio UI.

> **GIF 5 – execute_python / calculator**  
> Agent receives “compute fibonacci(10)” or “sqrt(144)+10” → calls the right tool → returns the number.

*(Real GIFs will be added once recorded — PRs welcome!)*

---

## 📦 Project layout

```
grok_local_agent_kit/
├── agent.py      # Core Agent + ReAct loop
├── llm.py        # Ollama + OpenAI-compatible client
├── tools.py      # web_search, files (cwd-safe), shell, execute_python, calculator, MCP
├── cli.py        # grok-agent CLI
└── __init__.py
examples/
├── chat_agent.py
├── automation_agent.py
└── research_agent.py
tests/
└── test_agent.py
```

---

## 🛠️ Extending

```python
agent = create_agent()

def my_tool(x: str) -> str:
    return f"Got {x}"

agent.register_tool(
    name="my_tool",
    func=my_tool,
    description="Does something useful",
    parameters={
        "type": "object",
        "properties": {"x": {"type": "string"}},
        "required": ["x"],
    },
)
```

---

## 🗺️ Roadmap

See [ROADMAP.md](ROADMAP.md).

- **v0.6.x / 0.7** — Real MCP client (stdio + SSE)
- **v0.8** — Multi-agent orchestration
- **v1.0** — Vision, memory, skill marketplace

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Issues and PRs are welcome!

---

## License

MIT © Nexus Studio / contributors

⭐ **Star the repo if local agents matter to you.**
