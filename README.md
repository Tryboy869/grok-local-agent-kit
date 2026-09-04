# 🚀 Grok Local Agent Kit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![CI](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/Tryboy869/grok-local-agent-kit/actions)
[![Version](https://img.shields.io/badge/version-0.16.0-green.svg)](https://github.com/Tryboy869/grok-local-agent-kit)

**Open-source toolkit for building local AI agents.**  
Ollama + LM Studio • ReAct tool loop • multi-LLM fallback router • JSONL + **SQLite vector memory** • **optional Ollama embeddings** • **on_thought** • **sandboxed execute_python** • skill packs • orchestrator • MCP stdio / HTTP / **SSE with retry** • MCP **prompts** • file config • hooks + **token usage** • **local HTTP API** • **planner** • **tool guardrails + timeouts** • offline-first.  
Built autonomously by Grok.

> Capable agents on your machine. No cloud required. No API keys for local models.

## ✨ Features (v0.16.0)

| Feature | Status |
|---------|--------|
| Multi-LLM (Ollama native + OpenAI-compat / LM Studio) | ✅ |
| Fallback router (`MultiLLMRouter`, `grok-agent route`, `--router`) | ✅ |
| ReAct-style tool calling loop | ✅ |
| Streaming final answers + `on_token` hook | ✅ |
| File / web / shell / Python / calculator / MCP tools | ✅ |
| Memory + SQLite vector memory | ✅ |
| Optional Ollama embeddings | ✅ |
| Restricted `execute_python` sandbox | ✅ |
| Parallel tools + `export_trace()` | ✅ |
| Skill packs + orchestrator + sessions | ✅ |
| MCP stdio / HTTP / SSE + prompts | ✅ |
| **Local HTTP API** (`grok-agent serve`, POST `/v1/chat`) | ✅ |
| **Workspace planner** (`plan_add` / `plan_list` / `plan_done`) | ✅ |
| **Tool allow/deny lists + per-tool timeout** | ✅ |
| **Interval scheduler** for automation agents | ✅ |
| CLI + examples + unit tests (no live LLM required) | ✅ |

## 🎬 Demo GIFs

Storyboard: [docs/gifs/README.md](docs/gifs/README.md). Until binary GIFs land, run:

`grok-agent chat -v --stream` · `python examples/serve_agent.py` · `python examples/planner_agent.py` · `python examples/guardrails_agent.py` · `python examples/parallel_agent.py`

## ⚡ Quick start (1 command)

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
grok-agent init
grok-agent route
grok-agent chat -v --stream --router
```

Local API (loopback only by default):

```bash
grok-agent serve --port 8765
curl -s http://127.0.0.1:8765/health
curl -s -X POST http://127.0.0.1:8765/v1/chat -H 'content-type: application/json' -d '{"prompt":"List files in this folder"}'
```

```bash
pip install git+https://github.com/Tryboy869/grok-local-agent-kit.git
git clone https://github.com/Tryboy869/grok-local-agent-kit.git
cd grok-local-agent-kit && pip install -e ".[dev]" && pytest -q
```

Needs Python 3.10+ and Ollama or LM Studio. `ollama pull llama3.2` is a good default.

```python
from grok_local_agent_kit import create_agent, ToolGuard, set_guard

set_guard(ToolGuard(deny={"run_shell"}, timeout_s=20))
agent = create_agent(model="llama3.2", provider="ollama", use_router=True, verbose=True)
print(agent.run("Add a plan item called ship local API, then list the plan"))
print(agent.usage.summary())
agent.close()
```

## Examples

```bash
python examples/chat_agent.py
python examples/automation_agent.py
python examples/serve_agent.py
python examples/planner_agent.py
python examples/guardrails_agent.py
python examples/mcp_agent.py --no-llm
python examples/parallel_agent.py
```

## Config

- `GROK_AGENT_MODEL`, `GROK_AGENT_PROVIDER`, `GROK_AGENT_BASE_URL`, `GROK_AGENT_ROUTER=1`
- `GROK_EMBED_BACKEND=hash|ollama`
- `GROK_AGENT_ALLOW_TOOLS`, `GROK_AGENT_DENY_TOOLS`, `GROK_AGENT_TOOL_TIMEOUT`

See [ROADMAP.md](ROADMAP.md), [CONTRIBUTING.md](CONTRIBUTING.md), [SHOW_HN.md](SHOW_HN.md), [docs/HN_INDIE_HACKERS.md](docs/HN_INDIE_HACKERS.md).

Built autonomously by Grok · Nexus Studio / Tryboy869  
https://github.com/Tryboy869/grok-local-agent-kit
