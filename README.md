# 🚀 Grok Local Agent Kit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![CI](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/Tryboy869/grok-local-agent-kit/actions)
[![Version](https://img.shields.io/badge/version-0.10.0-green.svg)](https://github.com/Tryboy869/grok-local-agent-kit)

**Open-source toolkit for building powerful local AI agents.**  
Ollama + LM Studio • ReAct tool loop • **multi-LLM fallback router** • **local memory** • **orchestrator** • real MCP stdio client • offline-first.  
Built autonomously by Grok.

> Run capable agents on your machine. No cloud required. No API keys needed for local models.

## ✨ Features (v0.10.0)

| Feature | Status |
|---------|--------|
| Multi-LLM (Ollama native + OpenAI-compatible / LM Studio) | ✅ |
| **Fallback router** (`MultiLLMRouter`, `grok-agent route`, `GROK_AGENT_ROUTER=1`) | ✅ |
| ReAct-style tool calling loop | ✅ |
| Streaming final answers | ✅ |
| File / web / shell / Python / calculator / MCP tools | ✅ |
| **Local JSONL memory** (`remember` / `recall` / `forget`) | ✅ |
| **Orchestrator** (planner + researcher / coder / operator) | ✅ |
| MCP stdio JSON-RPC + auto-register discovered tools | ✅ |
| Named sessions under `.grok/sessions/` | ✅ |
| CLI + examples + unit tests (no live LLM required) | ✅ |

## 🎬 Demo GIFs (record with asciinema / VHS)

1. `demo-chat.gif` — `grok-agent chat -v --stream`
2. `demo-route.gif` — `grok-agent route` (Ollama then LM Studio)
3. `demo-mcp.gif` — `python examples/mcp_agent.py --no-llm`
4. `demo-memory.gif` — `grok-agent memory remember` / `recall`

## ⚡ Quick start (1 command)

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

Needs Python 3.10+ and Ollama or LM Studio. `ollama pull llama3.2` is a good default.

```python
from grok_local_agent_kit import create_agent

agent = create_agent(model="llama3.2", provider="ollama", use_router=True, verbose=True)
print(agent.run("List files and remember that this workspace is the kit repo"))
agent.close()
```

## Examples

```bash
python examples/chat_agent.py
python examples/automation_agent.py
python examples/mcp_agent.py --no-llm
python examples/memory_agent.py
python examples/orchestrator_agent.py --no-llm
```

## Roadmap / contributing / license

See [ROADMAP.md](ROADMAP.md), [CONTRIBUTING.md](CONTRIBUTING.md), [LICENSE](LICENSE).

Launch drafts: [SHOW_HN.md](SHOW_HN.md) · [docs/HN_INDIE_HACKERS.md](docs/HN_INDIE_HACKERS.md)

Built autonomously by Grok · Nexus Studio / Tryboy869  
https://github.com/Tryboy869/grok-local-agent-kit
