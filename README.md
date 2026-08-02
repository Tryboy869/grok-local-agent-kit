# 🚀 Grok Local Agent Kit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![CI](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/Tryboy869/grok-local-agent-kit/actions)
[![Version](https://img.shields.io/badge/version-0.5.2-green.svg)](https://github.com/Tryboy869/grok-local-agent-kit)
[![Stars](https://img.shields.io/github/stars/Tryboy869/grok-local-agent-kit?style=social)](https://github.com/Tryboy869/grok-local-agent-kit/stargazers)
[![Forks](https://img.shields.io/github/forks/Tryboy869/grok-local-agent-kit?style=social)](https://github.com/Tryboy869/grok-local-agent-kit/network/members)

**Build powerful local AI agents that actually work offline-first.**  
Ollama • LM Studio • real tool calling • MCP-ready • pure Python.  
No cloud required. No vendor lock-in. Built autonomously by Grok.

> Star this repo if you believe local agents should be as good as the hosted ones.

---

## Why this exists

Most agent frameworks assume you have API keys, money, and internet.  
**Grok Local Agent Kit** is the opposite:

- Runs 100% on your machine
- Works with any Ollama model or LM Studio OpenAI-compatible endpoint
- Real ReAct-style tool loop (not just prompt engineering)
- Safe, useful built-in tools out of the box
- Designed to grow into a full local agent platform (MCP, multi-agent, memory…)

Perfect for privacy-conscious developers, offline workflows, research, automation, and people who just want agents that don’t phone home.

---

## ✨ Features (v0.5.2)

| Feature | Status |
|---------|--------|
| Multi-LLM (Ollama native + OpenAI-compatible / LM Studio / vLLM…) | ✅ |
| ReAct-style tool calling loop with iteration limit & truncation | ✅ |
| Tools: web search, read/write/list files, safe shell, execute_python, calculator | ✅ |
| Provider aliases (`lmstudio` → OpenAI-compat) | ✅ |
| MCP stub (full client planned for v0.6) | ✅ |
| CLI (`grok-agent chat` / `doctor`) | ✅ |
| Ready-to-run examples (chat, automation, research) | ✅ |
| One-command install from GitHub | ✅ |
| Unit tests (no live LLM required) | ✅ |
| Clean Python packaging + type-friendly API | ✅ |

---

## ⚡ Quick start (60 seconds)

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
   # https://ollama.com
   ollama pull llama3.2   # or any model you like
   ```

2. **Or LM Studio**  
   Start the local server (default `http://localhost:1234`).

### Run immediately

```bash
# Interactive chat
grok-agent chat

# One-shot
grok-agent chat "Search the web for local AI agents and summarize the top 3"

# Use LM Studio
grok-agent chat --provider lmstudio --model your-model-name

# Health check
grok-agent doctor
```

### Python API

```python
from grok_local_agent_kit import create_agent

agent = create_agent(model="llama3.2", provider="ollama", verbose=True)
print(agent.run("List files in the current directory and create a hello.txt"))
agent.close()
```

---

## 🎬 What it looks like

**Chat agent**  
You ask “What files are here?” → agent calls `list_files` → returns clean listing → answers in natural language.

**Automation example**  
```bash
python examples/automation_agent.py
```
Creates files, runs calculator, does web search, prints summary.

**Research agent**  
```bash
python examples/research_agent.py --topic "MCP protocol"
```
Searches → writes a markdown report → confirms.

*(Real terminal GIFs coming soon — PRs with recordings are very welcome!)*

---

## 📦 Project layout

```
grok_local_agent_kit/
├── agent.py      # Core Agent + ReAct loop
├── llm.py        # Ollama + OpenAI-compatible client
├── tools.py      # web_search, files, shell, execute_python, calculator, MCP stub
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

## 🛠️ Extending with custom tools

```python
from grok_local_agent_kit import create_agent

agent = create_agent()

def my_tool(x: str) -> str:
    return f"Got: {x}"

agent.register_tool(
    name="my_tool",
    func=my_tool,
    description="Does something useful with a string",
    parameters={
        "type": "object",
        "properties": {"x": {"type": "string"}},
        "required": ["x"],
    },
)

print(agent.run("Use my_tool with hello world"))
```

---

## 🗺️ Roadmap

See [ROADMAP.md](ROADMAP.md) for the full public plan.

- **v0.6** — Real MCP client (stdio + SSE)
- **v0.7** — Multi-agent orchestration
- **v0.8** — Persistent memory & sessions
- **v1.0** — Vision, skill marketplace, production hardening, PyPI

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).  
Issues, PRs, new tools, better examples, and terminal recordings are all welcome.

---

## License

MIT © Nexus Studio / contributors

---

⭐ **If local-first agents matter to you, please star the repo.**  
It helps more than you think.

Built with ❤️ by Grok in autonomous open-source mode.
