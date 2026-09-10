# grok-local-agent-kit

[![CI](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Offline-first](https://img.shields.io/badge/offline-first-success.svg)](#)
[![MCP](https://img.shields.io/badge/MCP-stdio%20%7C%20HTTP%20%7C%20SSE-informational.svg)](#mcp)

**Open-source toolkit for building capable local AI agents.**

Talk to [Ollama](https://ollama.com) or LM Studio. Run a ReAct tool loop. Speak MCP (stdio / Streamable HTTP / SSE). Cache tool results. Measure latency offline. Serve a local HTTP API. No cloud required. No API keys for local models.

> Capable agents on your machine.
> Built autonomously by Grok / Nexus Studio / [Tryboy869](https://github.com/Tryboy869).

**Repo:** https://github.com/Tryboy869/grok-local-agent-kit  
**Current:** v0.21.0 — tool-result TTL cache + offline telemetry

---

## Why this exists

Most agent frameworks assume a cloud LLM, a paid embedding API, and a vector database. This kit assumes the opposite:

- your laptop already runs `llama3.2` via Ollama
- tools should be first-class (files, shell, python sandbox, calculator, web, MCP)
- repeated tool calls should be cheap (TTL cache)
- you should be able to eval an agent with no network
- MCP is the interop layer, not an afterthought

If you want LangGraph-scale graphs in the cloud, use those. If you want a small, readable Python package that actually runs offline, start here.

---

## Features (v0.21.0)

| Area | What you get |
|---|---|
| LLMs | Ollama + LM Studio / OpenAI-compatible + fallback router |
| Loop | ReAct tool loop, streaming, hooks, skills, planner, orchestrator |
| Tools | files, web, shell, Python sandbox, calculator, custom tools, MCP |
| MCP | stdio, Streamable HTTP (`Mcp-Session-Id`), SSE, JSON-RPC cancel `-32800` |
| Memory | SQLite-backed memory + embeddings hook |
| Runtime | local HTTP API + optional bearer token, cancel tokens, guardrails |
| Ops | workspace watcher, TOML recipes, JSON extract |
| Quality | offline eval harness (`grok-agent eval`) |
| Cost | **tool-result TTL cache** (`grok-agent cache`) |
| Observability | **offline telemetry** (`grok-agent telemetry`) — latency, hits, errors |

---

## Quick start

```bash
# one-liner
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash

grok-agent doctor
grok-agent init
grok-agent route
grok-agent eval
python examples/cache_agent.py
grok-agent chat -v --stream --router
```

Or from source:

```bash
git clone https://github.com/Tryboy869/grok-local-agent-kit.git
cd grok-local-agent-kit
pip install -e ".[dev]"
pytest -q
```

**Requirements:** Python 3.10+ and Ollama or LM Studio.  
Recommended first model: `ollama pull llama3.2`

---

## Minimal Python API

```python
from grok_local_agent_kit import Agent

agent = Agent()  # picks Ollama / LM Studio if available
print(agent.run("List the files in this folder, then compute 21*2."))
```

Custom tools:

```python
from grok_local_agent_kit import Agent, tool

@tool
def greet(name: str) -> str:
    """Say hello."""
    return f"hello {name}"

agent = Agent(tools=[greet])
print(agent.run("greet the world"))
```

See `examples/` for chat, MCP sessions, cache, telemetry, watcher, recipes, eval, cancel, orchestrator.

---

## CLI

```text
grok-agent doctor          # check local LLM + deps
grok-agent init            # write grok-agent.toml
grok-agent chat -v --stream --router
grok-agent serve --port 8765
grok-agent eval
grok-agent cache
grok-agent telemetry
grok-agent route
```

Serve with a token:

```bash
GROK_AGENT_SERVE_TOKEN=dev grok-agent serve --port 8765
```

---

## Architecture (high level)

```text
                 +------------------+
  CLI / HTTP  -> |     Agent        | <- hooks / guardrails / cancel
                 |  ReAct loop      |
                 +--------+---------+
                          |
          +---------------+---------------+
          |               |               |
     LLM router      Tool registry     Memory
   Ollama/LMStudio   files/shell/MCP   SQLite + cache
          |               |
     fallback         telemetry
```

Nothing here phones home. Telemetry stays on disk.

---

## MCP

- stdio servers via config (`examples/.mcp_servers.example.json`)
- Streamable HTTP with session ids (`Mcp-Session-Id`)
- SSE client with session headers
- request cancel via JSON-RPC `-32800`

Start with `python examples/mcp_agent.py` and `python examples/mcp_session_agent.py`.

---

## Demo storyboard

See `docs/gifs/README.md` (binary GIFs not in-repo yet).

1. `grok-agent chat -v --stream` — list files then `21*2`
2. `GROK_AGENT_SERVE_TOKEN=dev grok-agent serve --port 8765`
3. `python examples/replay_agent.py --run`
4. `python examples/cancel_agent.py`
5. `python examples/watch_agent.py` and `python examples/recipe_agent.py`
6. `grok-agent eval` and `python examples/mcp_session_agent.py`
7. `python examples/cache_agent.py` and `python examples/telemetry_agent.py`

---

## Roadmap (honest)

See [ROADMAP.md](ROADMAP.md).

Near-term:

- sqlite-vec memory path
- terminal GIFs in docs
- PyPI package `grok-local-agent-kit`
- more MCP transports / auth profiles

90-day growth (no cheat, no bought stars):

1. Ship a real PyPI release + one-command install that never breaks
2. 3 tight demos (chat+tools, MCP session, cache/telemetry) as GIFs
3. Show HN + r/LocalLLaMA + relevant Discord/forums — listen, fix issues in <24h
4. Weekly small releases, not vapor
5. Good first issues only if they are actually good

Stars follow usefulness. Usefulness follows demos that work on a cold laptop.

---

## Contributing

[CONTRIBUTING.md](CONTRIBUTING.md) · [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) · [SECURITY.md](SECURITY.md)

MIT licensed — [LICENSE](LICENSE).

---

Built autonomously by Grok for Nexus Studio / Tryboy869.
