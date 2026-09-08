# Grok Local Agent Kit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![CI](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/Tryboy869/grok-local-agent-kit/actions)
[![Version](https://img.shields.io/badge/version-0.20.0-green.svg)](https://github.com/Tryboy869/grok-local-agent-kit)

**Open-source toolkit for building local AI agents.**
Ollama + LM Studio, ReAct tool loop, multi-LLM fallback router, SQLite vector memory, MCP stdio/HTTP/SSE with session ids + request cancel, local HTTP API, recipes, watcher, offline eval harness. Offline-first. Built autonomously by Grok.

> Capable agents on your machine. No cloud required. No API keys for local models.

## Features (v0.20.0)

- Multi-LLM (Ollama + LM Studio / OpenAI-compat) + fallback router
- ReAct tool loop, streaming, hooks, skills, orchestrator
- File / web / shell / Python sandbox / calculator / MCP tools
- MCP Streamable HTTP session ids (`Mcp-Session-Id`) + JSON-RPC -32800 cancel
- Offline eval harness (`grok-agent eval`)
- Local HTTP API + optional bearer auth, planner, guardrails, cancel tokens
- Workspace watcher, JSON extract, TOML recipes
- Tests without a live LLM

## Demo storyboard

See docs/gifs/README.md. Binary GIFs not in-repo yet.

1. `grok-agent chat -v --stream` list files then compute 21*2
2. `GROK_AGENT_SERVE_TOKEN=dev grok-agent serve --port 8765`
3. `python examples/replay_agent.py --run`
4. `python examples/cancel_agent.py`
5. `python examples/watch_agent.py` and `python examples/recipe_agent.py`
6. `grok-agent eval` and `python examples/mcp_session_agent.py`

## Quick start (1 command)

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
grok-agent init
grok-agent route
grok-agent eval
grok-agent chat -v --stream --router
```

```bash
pip install git+https://github.com/Tryboy869/grok-local-agent-kit.git
git clone https://github.com/Tryboy869/grok-local-agent-kit.git
cd grok-local-agent-kit && pip install -e ".[dev]" && pytest -q
```

Needs Python 3.10+ and Ollama or LM Studio. `ollama pull llama3.2` is a good default.

See ROADMAP.md, CONTRIBUTING.md, SHOW_HN.md, docs/HN_INDIE_HACKERS.md.

Built autonomously by Grok / Nexus Studio / Tryboy869
https://github.com/Tryboy869/grok-local-agent-kit
