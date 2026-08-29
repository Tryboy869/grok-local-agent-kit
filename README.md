# 🚀 Grok Local Agent Kit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![CI](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/Tryboy869/grok-local-agent-kit/actions)
[![Version](https://img.shields.io/badge/version-0.9.1-green.svg)](https://github.com/Tryboy869/grok-local-agent-kit)
[![GitHub stars](https://img.shields.io/github/stars/Tryboy869/grok-local-agent-kit?style=social)](https://github.com/Tryboy869/grok-local-agent-kit/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/Tryboy869/grok-local-agent-kit)](https://github.com/Tryboy869/grok-local-agent-kit/issues)

**Open-source toolkit for building powerful local AI agents.**  
Ollama + LM Studio • ReAct tool loop • **real MCP stdio client** • named sessions • offline-first.  
Built autonomously by Grok.

> Run capable agents on your machine. No cloud required. No API keys needed for local models.

---

## ✨ Features (v0.9.1)

| Feature | Status |
|---------|--------|
| Multi-LLM (Ollama native + OpenAI-compatible / LM Studio) | ✅ |
| ReAct-style tool calling loop with routing guidance | ✅ |
| Real streaming of final answers (`stream=True` / CLI `--stream`) | ✅ |
| **21 tools**: web, HTTP, files (cwd-safe + search + mkdir + copy + stat + delete), shell, Python, calculator, datetime, system info, list_tools, **live MCP** (incl. `resources/read`) | ✅ |
| **MCP stdio JSON-RPC client** (initialize, tools/list, tools/call, resources/list, resources/read) | ✅ |
| Auto-register discovered MCP tools as `mcp_<server>_<tool>` | ✅ |
| Named sessions under `.grok/sessions/` (`--session`, `/session`) | ✅ |
| Bundled echo MCP server for tests and demos | ✅ |
| Conversation history save/load (+ CLI `/save` `/load` `/mcp` `/ping` `/attach-mcp`) | ✅ |
| Env defaults (`GROK_AGENT_*`, `GROK_MCP_SERVERS`) | ✅ |
| CLI + ready-to-run examples + unit tests (no live LLM) | ✅ |

---

## 🎬 Demo (what it looks like)

*Suggested recordings (GIF / [asciinema](https://asciinema.org)): `grok-agent chat -v --stream`, `python examples/automation_agent.py`, `python examples/mcp_agent.py --no-llm`.*

**Interactive chat**

```text
$ grok-agent chat -v --stream
Local Agent ready (v0.9.1). Type 'exit' or Ctrl-C to quit.
Special: /save [file], /load [file], /reset, /tools, /mcp, /ping, /session, /attach-mcp

You › List files and create notes/hello.txt
  → tool: mkdir({'path': 'notes'})
  → tool: write_file({'path': 'notes/hello.txt', 'content': 'hello'})
  → tool: file_stat({'path': 'notes/hello.txt'})
Agent › Created notes/hello.txt (FILE, N bytes).

You › /mcp
MCP client: stdio JSON-RPC (v0.9.1)
Configured servers: 0
```

**MCP without an LLM**

```text
$ python examples/mcp_agent.py --no-llm
MCP client: stdio JSON-RPC (v0.9.1)
Configured servers: 1
  1. echo (stdio) python

--- tools/call echo ---
hello from mcp_agent
```

---

## ⚡ Quick start (1 command)

```bash
pip install git+https://github.com/Tryboy869/grok-local-agent-kit.git
```

Or from source:

```bash
git clone https://github.com/Tryboy869/grok-local-agent-kit.git
cd grok-local-agent-kit
pip install -e ".[dev]"
pytest -q
```

### Prerequisites

1. **Ollama** (recommended)
   ```bash
   # https://ollama.com
   ollama pull llama3.2
   ```
2. **Or LM Studio** — start the local server (`http://localhost:1234`).

### Run

```bash
grok-agent chat
grok-agent chat "Search the web for local AI agents and summarize"
grok-agent chat --provider lmstudio --model your-model-name
grok-agent chat -v --stream
grok-agent chat --session demo --attach-mcp
grok-agent doctor
```

### Python

```python
from grok_local_agent_kit import create_agent

agent = create_agent(model="llama3.2", provider="ollama", verbose=True, stream=True)
print(agent.run("List files and create hello.txt"))
print(agent.list_registered_tools())
agent.close()
```

### MCP (stdio)

```bash
export GROK_MCP_SERVERS='[{"name":"echo","command":"python","args":["-m","grok_local_agent_kit.mcp_echo_server"]}]'
python examples/mcp_agent.py --no-llm
```

Copy `examples/.mcp_servers.example.json` to `.mcp_servers.json` in your workspace if you prefer a file over the env var.

HTTP/SSE transport is recognized in config but not implemented yet.

---

## 🛠️ Built-in tools

| Tool | Description |
|------|-------------|
| `web_search` | DuckDuckGo search |
| `http_get` | HTTP GET (text) |
| `list_files` / `search_files` | Workspace listing & content search |
| `read_file` / `write_file` / `append_file` / `delete_file` | Text files (cwd-safe) |
| `mkdir` / `copy_file` / `file_stat` | Directories, copy, metadata |
| `run_shell` | Restricted shell |
| `execute_python` | Safe snippet execution |
| `calculator` | Math |
| `get_datetime` / `get_system_info` / `list_tools` | Context & introspection |
| `mcp_list_resources` / `mcp_list_tools` / `mcp_call_tool` / `mcp_read_resource` | Live MCP stdio client |

---

## 📦 Examples

```bash
python examples/chat_agent.py
python examples/automation_agent.py
python examples/research_agent.py
python examples/code_assistant.py
python examples/custom_tools_agent.py
python examples/mcp_agent.py --no-llm
python examples/session_agent.py
```

---

## 🗺️ Roadmap

See [ROADMAP.md](ROADMAP.md). Next: MCP HTTP/SSE, multi-agent memory, PyPI release.

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Good first issues are labeled on GitHub.

## 📄 License

MIT — see [LICENSE](LICENSE).

---

### Share / discuss (HN · Indie Hackers)

Draft post: [SHOW_HN.md](SHOW_HN.md) · [docs/HN_INDIE_HACKERS.md](docs/HN_INDIE_HACKERS.md)

**Offline-first AI agents that actually call tools — including a real MCP stdio client. No API key for local models.**

```bash
pip install git+https://github.com/Tryboy869/grok-local-agent-kit.git
grok-agent doctor
grok-agent chat -v --stream
python examples/mcp_agent.py --no-llm
```

Built autonomously by Grok · Nexus Studio / Tryboy869  
Repo: https://github.com/Tryboy869/grok-local-agent-kit
