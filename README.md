# Grok Local Agent Kit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![CI](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml)
[![Version](https://img.shields.io/badge/version-0.10.0-green.svg)](https://github.com/Tryboy869/grok-local-agent-kit)
[![Issues](https://img.shields.io/github/issues/Tryboy869/grok-local-agent-kit)](https://github.com/Tryboy869/grok-local-agent-kit/issues)
[![Stars](https://img.shields.io/github/stars/Tryboy869/grok-local-agent-kit?style=social)](https://github.com/Tryboy869/grok-local-agent-kit/stargazers)

**Offline-first Python toolkit for local AI agents.**  
Ollama + LM Studio · ReAct tool loop · multi-LLM fallback router · JSONL memory · multi-agent orchestrator · real MCP stdio client.

> Run capable agents on your machine. No cloud required. No API keys needed for local models.

Repo: [https://github.com/Tryboy869/grok-local-agent-kit](https://github.com/Tryboy869/grok-local-agent-kit)

---

## Why this exists

Most agent frameworks assume a hosted API. This kit is built for people who want:

- agents that work with **Ollama** or **LM Studio** on a laptop
- **real tools** (files, shell, Python, web search, calculator, MCP)
- a **fallback router** when one local server is down
- **memory** that lives in a JSONL file, not a SaaS vector DB
- a small, readable codebase you can fork in an afternoon

It is MIT-licensed and developed in the open under [Tryboy869](https://github.com/Tryboy869).

---

## Features (v0.10.0)

| Feature | Status |
|---------|--------|
| Multi-LLM (Ollama native + OpenAI-compatible / LM Studio) | done |
| Fallback router (`MultiLLMRouter`, `grok-agent route`, `--router`) | done |
| ReAct-style tool calling loop | done |
| Streaming final answers | done |
| File / web / shell / Python / calculator / MCP tools | done |
| Local JSONL memory (`remember` / `recall` / `forget`) | done |
| Orchestrator (planner + researcher / coder / operator) | done |
| MCP stdio JSON-RPC + auto-register discovered tools | done |
| Named sessions under `.grok/sessions/` | done |
| CLI + examples + unit tests (no live LLM required) | done |
| MCP HTTP/SSE transport | planned |

---

## Quick start

```bash
pip install git+https://github.com/Tryboy869/grok-local-agent-kit.git
grok-agent doctor
grok-agent route
grok-agent chat -v --stream --router
```

From source:

```bash
git clone https://github.com/Tryboy869/grok-local-agent-kit.git
cd grok-local-agent-kit
pip install -e ".[dev]"
pytest -q
```

Requirements: Python 3.10+ and either [Ollama](https://ollama.com) or [LM Studio](https://lmstudio.ai). A good default model:

```bash
ollama pull llama3.2
```

### Python API

```python
from grok_local_agent_kit import create_agent

agent = create_agent(
    model="llama3.2",
    provider="ollama",
    use_router=True,
    verbose=True,
)
print(agent.run("List files and remember that this workspace is the kit repo"))
agent.close()
```

### CLI cheatsheet

```bash
grok-agent doctor          # check local LLM servers
grok-agent route           # probe Ollama then LM Studio
grok-agent chat -v --stream --router
grok-agent memory remember "this repo is grok-local-agent-kit"
grok-agent memory recall "repo"
```

---

## Examples

```bash
python examples/chat_agent.py
python examples/automation_agent.py
python examples/mcp_agent.py --no-llm
python examples/memory_agent.py
python examples/orchestrator_agent.py --no-llm
python examples/custom_tools_agent.py
python examples/code_assistant.py
python examples/research_agent.py
python examples/session_agent.py
```

MCP config template: `examples/.mcp_servers.example.json`.

---

## Architecture (short)

```
create_agent()
    -> Agent (ReAct loop, sessions, tools)
         -> LLM backend (Ollama or OpenAI-compatible)
         -> MultiLLMRouter (optional fallback)
         -> Toolkit (files, shell, python, web, calc, memory, MCP)
         -> MCPClient (stdio JSON-RPC)
         -> MemoryStore (JSONL)
         -> Orchestrator (planner + specialists)
```

Package root: `grok_local_agent_kit/`.

---

## Roadmap

See [ROADMAP.md](ROADMAP.md). Near-term:

1. Record a GIF / asciinema demo ([issue #1](https://github.com/Tryboy869/grok-local-agent-kit/issues/1))
2. MCP HTTP/SSE transport ([issue #2](https://github.com/Tryboy869/grok-local-agent-kit/issues/2))
3. Publish to PyPI as `grok-local-agent-kit`
4. Plugin interface for custom tools and providers

---

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md). Issues and PRs are welcome, especially:

- tests that do not require a live LLM
- MCP transport work
- docs and recorded demos
- real-world example agents

```bash
pip install -e ".[dev]"
pytest -q
ruff check .
```

---

## License

[MIT](LICENSE) · Nexus Studio / [Tryboy869](https://github.com/Tryboy869)

Launch drafts: [SHOW_HN.md](SHOW_HN.md) · [docs/HN_INDIE_HACKERS.md](docs/HN_INDIE_HACKERS.md)
