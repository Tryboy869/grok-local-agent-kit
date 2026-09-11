# grok-local-agent-kit

[![CI](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-0.22.0-informational.svg)](CHANGELOG.md)
[![Offline-first](https://img.shields.io/badge/offline--first-yes-success.svg)](#quick-start-1-command)

**Open-source toolkit for building local AI agents.**
Ollama + LM Studio, ReAct tool loop, multi-LLM fallback router, SQLite vector memory, MCP stdio/HTTP/SSE with session ids + request cancel, local HTTP API, recipes, watcher, offline eval harness, tool-result cache + telemetry, **tool-call budgets + retries**.

Offline-first. Built autonomously by Grok.

> Capable agents on your machine.
> No cloud required.
> No API keys for local models.

## Features (v0.22.0)

- Multi-LLM (Ollama + LM Studio / OpenAI-compat) + fallback router
- ReAct tool loop, streaming, hooks, skills, orchestrator
- File / web / shell / Python sandbox / calculator / MCP tools
- MCP Streamable HTTP session ids (`Mcp-Session-Id`) + JSON-RPC `-32800` cancel
- Offline eval harness (`grok-agent eval`)
- Local HTTP API + optional bearer auth, planner, guardrails, cancel tokens
- Workspace watcher, JSON extract, LLM-free TOML recipes
- **Tool-result TTL cache** (`grok-agent cache`) — skip repeated calculator / file reads
- **Tool telemetry** (`grok-agent telemetry`) — latency, hits, errors, no network
- **Tool-call budget** (`grok-agent budget`) — global + per-tool caps, env `GROK_AGENT_MAX_TOOL_CALLS`
- **Retry helper** (`retry_call`) — exponential backoff for flaky local backends

## Quick start (1 command)

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
grok-agent init
grok-agent route
grok-agent eval
python examples/cache_agent.py
python examples/budget_agent.py
grok-agent budget stats
grok-agent chat -v --stream --router
```

```bash
pip install git+https://github.com/Tryboy869/grok-local-agent-kit.git
# or
git clone https://github.com/Tryboy869/grok-local-agent-kit.git
cd grok-local-agent-kit && pip install -e ".[dev]" && pytest -q
```

Needs Python 3.10+ and Ollama or LM Studio. `ollama pull llama3.2` is a good default.

## Demo storyboard

See [docs/gifs/README.md](docs/gifs/README.md).

1. `grok-agent chat -v --stream` list files then compute `21*2`
2. `GROK_AGENT_SERVE_TOKEN=dev grok-agent serve --port 8765`
3. `python examples/replay_agent.py --run`
4. `python examples/cancel_agent.py`
5. `python examples/watch_agent.py` and `python examples/recipe_agent.py`
6. `grok-agent eval` and `python examples/mcp_session_agent.py`
7. `python examples/cache_agent.py` and `python examples/telemetry_agent.py`
8. `python examples/budget_agent.py` and `python examples/retry_agent.py`

## Architecture

```
CLI / HTTP API / Python SDK
        |
   Agent (ReAct loop)
        |
  +-----+-----+------+
  |     |     |      |
 LLM  Tools  MCP   Memory
router         sessions  (SQLite + vectors)
```

## Docs

- [ROADMAP.md](ROADMAP.md)
- [CHANGELOG.md](CHANGELOG.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [SHOW_HN.md](SHOW_HN.md)
- [GROWTH.md](GROWTH.md)
- [docs/HN_INDIE_HACKERS.md](docs/HN_INDIE_HACKERS.md)

## License

MIT. Built autonomously by Grok / Nexus Studio / [Tryboy869](https://github.com/Tryboy869).

https://github.com/Tryboy869/grok-local-agent-kit
