# 🚀 Grok Local Agent Kit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![CI](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/Tryboy869/grok-local-agent-kit/actions)
[![Version](https://img.shields.io/badge/version-0.8.2-green.svg)](https://github.com/Tryboy869/grok-local-agent-kit)
[![GitHub stars](https://img.shields.io/github/stars/Tryboy869/grok-local-agent-kit?style=social)](https://github.com/Tryboy869/grok-local-agent-kit/stargazers)

**Open-source toolkit for building powerful local AI agents.**  
Ollama + LM Studio • real tool calling • MCP foundation • offline-first.  
Built autonomously by Grok.

> Run capable agents on your machine. No cloud required. No API keys needed for local models.

---

## ✨ Features (v0.8.2)

| Feature | Status |
|---------|--------|
| Multi-LLM (Ollama native + OpenAI-compatible / LM Studio) | ✅ |
| ReAct-style tool calling loop | ✅ |
| **Real streaming of final answers** (`stream=True` / CLI `--stream`) | ✅ |
| **13 tools**: web search, files (cwd-safe + append), shell, execute_python, calculator, datetime, list_tools, MCP foundation | ✅ |
| MCP server config via env / JSON (foundation for full client) | ✅ |
| Conversation history save/load (+ CLI `/save` `/load`) | ✅ |
| Env defaults (`GROK_AGENT_MODEL`, `GROK_AGENT_PROVIDER`, `GROK_AGENT_BASE_URL`) | ✅ |
| `register_tools()` batch helper + `get_history()` | ✅ |
| Configurable tool-result truncation | ✅ |
| CLI (`grok-agent chat / doctor`) with interactive helpers + `--stream` | ✅ |
| Ready-to-run examples (chat, automation, research, code_assistant) | ✅ |
| One-command install + `py.typed` | ✅ |
| Unit tests (no live LLM required) | ✅ |

---

## 🎬 Demo (what it looks like)

**Interactive chat** — *suggested GIF / asciinema: `grok-agent chat -v --stream` creating a file + web search*

```text
$ grok-agent chat -v --stream
Local Agent ready (v0.8.2). Type 'exit' or Ctrl-C to quit.
Special: /save [file], /load [file], /reset, /tools

You › List files and create a note saying hello
  → tool: list_files({'path': '.'})
  ← FILE  README.md ...
  → tool: write_file({'path': 'note.txt', 'content': 'hello'})
  ← Successfully wrote ...
Agent › Done. Created note.txt and listed the workspace.

You › /tools
Available tools (13):
- web_search: Search the web ...
...
```

**Automation agent** — *suggested GIF: full one-shot goal with tool trace*

```text
$ python examples/automation_agent.py
🤖 Automation Agent (v0.8.2)
  → tool: write_file(...)
  → tool: list_files(...)
  → tool: calculator(...)
  → tool: web_search(...)
=== Final answer ===
I created hello_from_agent.py, confirmed it, computed 22.0, and found ...
```

*(Replace the text demos above with real terminal GIFs / asciinema when available.  
Suggested recordings: `grok-agent chat -v --stream` creating a file + web search, and the automation example.)*

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

# Stream final answer tokens + show tool trace
grok-agent chat -v --stream

# Save history on exit
grok-agent chat --save-history session.json

# Health check
grok-agent doctor
```

### Python

```python
from grok_local_agent_kit import create_agent

agent = create_agent(model="llama3.2", provider="ollama", verbose=True, stream=True)
print(agent.run("List files in the current directory and create a hello.txt"))
agent.save_history("session.json")
print(len(agent.get_history()), "messages")
agent.close()
```

Environment defaults (optional):

```bash
export GROK_AGENT_MODEL=llama3.2
export GROK_AGENT_PROVIDER=ollama
# export GROK_AGENT_BASE_URL=http://localhost:1234/v1
# Optional MCP foundation:
# export GROK_MCP_SERVERS='[{"name":"fs","command":"npx","args":["-y","@modelcontextprotocol/server-filesystem","."]}]'
```

---

## 🛠️ Built-in tools

| Tool | Description |
|------|-------------|
| `web_search` | DuckDuckGo search |
| `list_files` | List files (cwd-safe) |
| `read_file` / `write_file` / `append_file` | Read/write/append text files (cwd-safe) |
| `run_shell` | Restricted shell commands |
| `execute_python` | Safe Python snippet execution |
| `calculator` | Math expressions |
| `get_datetime` | Current UTC time |
| `list_tools` | Introspect available tools |
| `mcp_*` | MCP discovery & call (foundation — full client next) |

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

See [ROADMAP.md](ROADMAP.md). Current focus: **real MCP client** (stdio + SSE) in the 0.8.x series.

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Highest priority: full MCP stdio/SSE client.

## 📄 License

MIT — see [LICENSE](LICENSE).

---

### Share / discuss (HN · Indie Hackers)

**Offline-first AI agents that actually call tools — no API key required for local models.**

- ReAct-style loop with 13 built-in tools (web, files, shell, code, math…)
- Ollama + LM Studio (any OpenAI-compatible endpoint)
- MCP foundation already wired; full client is next
- One-command install, CLI + Python API, zero live-LLM unit tests

```bash
pip install git+https://github.com/Tryboy869/grok-local-agent-kit.git
grok-agent doctor
grok-agent chat -v --stream
```

Built autonomously by Grok · Nexus Studio / Tryboy869  
Repo: https://github.com/Tryboy869/grok-local-agent-kit
