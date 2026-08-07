# 🚀 Grok Local Agent Kit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![CI](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/Tryboy869/grok-local-agent-kit/actions)
[![Version](https://img.shields.io/badge/version-0.7.0-green.svg)](https://github.com/Tryboy869/grok-local-agent-kit)
[![GitHub stars](https://img.shields.io/github/stars/Tryboy869/grok-local-agent-kit?style=social)](https://github.com/Tryboy869/grok-local-agent-kit/stargazers)

**Open-source toolkit for building powerful local AI agents.**  
Ollama + LM Studio • real tool calling • MCP-ready • offline-first.  
Built autonomously by Grok.

> Run capable agents on your machine. No cloud required. No API keys needed for local models.

---

## ✨ Features (v0.7.0)

| Feature | Status |
|---------|--------|
| Multi-LLM (Ollama native + OpenAI-compatible / LM Studio) | ✅ |
| ReAct-style tool calling loop | ✅ |
| 12 tools: web search, files (cwd-safe), shell, execute_python, calculator, datetime, list_tools, MCP stubs | ✅ |
| Conversation history save/load | ✅ |
| Tool-result truncation & clearer LLM errors | ✅ |
| Provider aliases (`lmstudio` → OpenAI-compat) | ✅ |
| Enhanced MCP stub (list resources/tools + call) | ✅ |
| CLI (`grok-agent chat / doctor`) | ✅ |
| Ready-to-run examples (chat, automation, research, code_assistant) | ✅ |
| One-command install | ✅ |
| Unit tests (no live LLM required) | ✅ |

---

## 🎬 Demo (what it looks like)

**Interactive chat**
```text
$ grok-agent chat -v
Local Agent ready (v0.7.0). Type 'exit' or Ctrl-C to quit.

You › List files and create a note saying hello
  → tool: list_files({'path': '.'})
  ← FILE  README.md ...
  → tool: write_file({'path': 'note.txt', 'content': 'hello'})
  ← Successfully wrote ...
Agent › Done. Created note.txt and listed the workspace.
```

**Automation agent**
```text
$ python examples/automation_agent.py
🤖 Automation Agent (v0.7.0)
  → tool: write_file(...)
  → tool: list_files(...)
  → tool: calculator(...)
  → tool: web_search(...)
=== Final answer ===
I created hello_from_agent.py, confirmed it, computed 22.0, and found ...
```

*(Replace the text demos above with real terminal GIFs / asciinema when available.  
Suggested: record `grok-agent chat -v` creating a file + web search, and the automation example.)*

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
agent.save_history("session.json")   # new in 0.7
agent.close()
```

---

## 🛠️ Built-in tools

| Tool | Description |
|------|-------------|
| `web_search` | DuckDuckGo search |
| `list_files` | List files (cwd-safe) |
| `read_file` / `write_file` | Read/write text files (cwd-safe) |
| `run_shell` | Restricted shell commands |
| `execute_python` | Safe Python snippet execution |
| `calculator` | Math expressions |
| `get_datetime` | Current UTC time |
| `list_tools` | Introspect available tools |
| `mcp_*` | MCP discovery & call stubs |

---

## 📦 Examples

```bash
python examples/chat_agent.py
python examples/automation_agent.py
python examples/research_agent.py
python examples/code_assistant.py
```

All examples are ready-to-run once a local LLM is available.

---

## 🗺️ Roadmap

See [ROADMAP.md](ROADMAP.md). Next major focus: **real MCP client**.

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Highest priority: full MCP stdio/SSE client.

## 📄 License

MIT — see [LICENSE](LICENSE).

---

Built autonomously by Grok · Nexus Studio / Tryboy869
