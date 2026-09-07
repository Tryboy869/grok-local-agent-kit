# 🚀 Grok Local Agent Kit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![CI](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/Tryboy869/grok-local-agent-kit/actions)
[![Version](https://img.shields.io/badge/version-0.19.0-green.svg)](https://github.com/Tryboy869/grok-local-agent-kit)

**Open-source toolkit for building local AI agents.**  
Ollama + LM Studio • ReAct tool loop • multi-LLM fallback router • JSONL + **SQLite vector memory** • **optional Ollama embeddings** • **on_thought** • **sandboxed execute_python** • skill packs • orchestrator • MCP stdio / HTTP / **SSE with retry** • MCP **prompts** • file config • hooks + **token usage** • **local HTTP API + optional bearer auth** • **trace replay** • **planner** • **tool guardrails + timeouts** • **cancel tokens that kill hung shells** • **workspace file watcher** • **JSON extract** • **TOML recipes** • offline-first.  
Built autonomously by Grok.

> Capable agents on your machine. No cloud required. No API keys for local models.

## ✨ Features (v0.19.0)

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
| **Trace replay** (`grok-agent replay`, `examples/replay_agent.py`) | ✅ |
| Skill packs + orchestrator + sessions | ✅ |
| MCP stdio / HTTP / SSE + prompts | ✅ |
| **Local HTTP API** (`grok-agent serve`, POST `/v1/chat`) | ✅ |
| **Optional bearer auth** (`--token` / `GROK_AGENT_SERVE_TOKEN`) | ✅ |
| **Workspace planner** | ✅ |
| **Tool allow/deny lists + per-tool timeout** | ✅ |
| **Cancel tokens + process-group kill** for `run_shell` | ✅ |
| **Workspace file watcher** (`grok-agent watch`, `examples/watch_agent.py`) | ✅ |
| **Structured JSON extract** from messy model text | ✅ |
| **TOML/JSON tool recipes** (no LLM required) | ✅ |
| **Interval scheduler** for automation agents | ✅ |
| CLI + examples + unit tests (no live LLM required) | ✅ |

## 🎬 Demo GIFs

Storyboard: [docs/gifs/README.md](docs/gifs/README.md).

Binary recordings are not in-repo yet — described demos:

**Demo 1 — chat + tools**  
`grok-agent chat -v --stream` → “list files then compute 21*2” → thoughts → parallel tools → streamed answer.

**Demo 2 — local API + bearer**  
`GROK_AGENT_SERVE_TOKEN=dev grok-agent serve --port 8765` then curl `/health` and `/v1/chat`.

**Demo 3 — replay**  
`python examples/replay_agent.py --run` re-executes a calculator tool call with no LLM.

**Demo 4 — cancel hung shell**  
`python examples/cancel_agent.py` starts `sleep 10` then cancels the child.

**Demo 5 — watch + recipes (no LLM)**  
`python examples/watch_agent.py` diffs a temp folder. `python examples/recipe_agent.py` runs tools from TOML. `python examples/structured_agent.py` pulls JSON out of fenced model text.

## ⚡ Quick start (1 command)

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
grok-agent init
grok-agent route
grok-agent chat -v --stream --router
```

```bash
pip install git+https://github.com/Tryboy869/grok-local-agent-kit.git
git clone https://github.com/Tryboy869/grok-local-agent-kit.git
cd grok-local-agent-kit && pip install -e ".[dev]" && pytest -q
```

Needs Python 3.10+ and Ollama or LM Studio. `ollama pull llama3.2` is a good default.

```python
from grok_local_agent_kit import create_agent, extract_json, load_recipe, run_recipe, watch
```

See [ROADMAP.md](ROADMAP.md), [CONTRIBUTING.md](CONTRIBUTING.md), [SHOW_HN.md](SHOW_HN.md), [docs/HN_INDIE_HACKERS.md](docs/HN_INDIE_HACKERS.md).

Built autonomously by Grok · Nexus Studio / Tryboy869  
https://github.com/Tryboy869/grok-local-agent-kit
