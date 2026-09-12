# grok-local-agent-kit

**Open-source toolkit for building local AI agents.**
Ollama + LM Studio, ReAct tool loop, multi-LLM fallback router, SQLite vector memory with **optional sqlite-vec**, MCP stdio/HTTP/SSE, local HTTP API, recipes, watcher, offline eval harness, tool cache + telemetry + budgets, **drop-in tool plugins with a Python sandbox**, **JSONL transcripts**.
Offline-first.
Built autonomously by Grok.

> Capable agents on your machine.
> No cloud required.
> No API keys for local models.

## Features (v0.25.0)

* Multi-LLM (Ollama + LM Studio / OpenAI-compat) + fallback router
* ReAct tool loop, streaming, hooks, skills, orchestrator
* File / web / shell / Python sandbox / calculator / MCP tools
* MCP Streamable HTTP session ids (`Mcp-Session-Id`) + JSON-RPC `-32800` cancel
* Offline eval harness (`grok-agent eval`)
* Local HTTP API + optional bearer auth, planner, guardrails, cancel tokens
* Workspace watcher, JSON extract, LLM-free TOML recipes
* Tool-result TTL cache, telemetry, tool-call budgets, retry helper
* Optional sqlite-vec (`GROK_VEC_BACKEND`, `grok-agent vec`)
* Drop-in plugins — JSON always; **Python only when opted in** (`GROK_AGENT_ALLOW_PY_PLUGINS` or allowlist)
* Transcripts — local JSONL logs (`grok-agent transcripts list`)
* `grok-agent sandbox status|skipped`

## Demo storyboard

Binary GIFs are not generated in this environment. Recreate them with VHS or `script` + `agg`. Storyboards live in `docs/gifs/README.md`.

1. `grok-agent chat -v --stream` — list files, then `calculator` for `21*2`
2. `GROK_AGENT_SERVE_TOKEN=dev grok-agent serve --port 8765`
3. `python examples/plugin_agent.py` then `grok-agent plugins list`
4. `python examples/sandbox_plugin_agent.py` then `grok-agent sandbox status`
5. `python examples/transcript_agent.py` then `grok-agent transcripts list`

## Quick start (1 command)

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
grok-agent init
grok-agent plugins list
grok-agent sandbox status
python examples/plugin_agent.py
python examples/sandbox_plugin_agent.py
pytest -q
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
