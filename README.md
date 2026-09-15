# grok-local-agent-kit

**Open-source toolkit for building local AI agents.**
Ollama + LM Studio, ReAct tool loop, multi-LLM fallback router, SQLite vector memory with **optional sqlite-vec**, MCP stdio/HTTP/SSE, local HTTP API, recipes, watcher, offline eval harness, tool cache + telemetry + budgets, **drop-in tool plugins with a Python sandbox**, **JSONL transcripts**, **workspace packer + local file RAG**, **web search with HTML fallback**, **multi-agent Team + shared blackboard**.
Offline-first.
Built autonomously by Grok.

> Capable agents on your machine.
> No cloud required.
> No API keys for local models.

## Features (v0.28.0)

* Multi-LLM (Ollama + LM Studio / OpenAI-compat) + fallback router
* ReAct tool loop, streaming, hooks, skills, orchestrator
* **Team + Blackboard** — coordinator / researcher / operator share posts (`grok-agent team demo`)
* File / web / shell / Python sandbox / calculator / MCP tools
* Web search: `duckduckgo-search` first, DuckDuckGo HTML fallback if the package or API fails
* Workspace packer + local file RAG (`pack_workspace`, `search_workspace`)
* MCP Streamable HTTP session ids (`Mcp-Session-Id`) + JSON-RPC `-32800` cancel
* Offline eval harness (`grok-agent eval`)
* Local HTTP API + optional bearer auth, planner, guardrails, cancel tokens
* Workspace watcher, JSON extract, LLM-free TOML recipes
* Tool-result TTL cache, telemetry, tool-call budgets, retry helper
* Optional sqlite-vec (`GROK_VEC_BACKEND`, `grok-agent vec`)
* Drop-in plugins — JSON always; **Python only when opted in**
* Transcripts — local JSONL logs
* `grok-agent tools list|demo` — inspect tools **without a live LLM**
* `grok-agent workspace pack|search`
* `grok-agent sandbox status|skipped`

## Demo storyboard

Binary GIFs are not generated in this environment. Recreate them with [VHS](https://github.com/charmbracelet/vhs) or `script` + `agg`. Storyboards: `docs/gifs/README.md`.

1. `python examples/tools_demo_agent.py` or `grok-agent tools demo` — no LLM needed
2. `grok-agent team demo` — shared blackboard, still no LLM
3. `grok-agent chat -v --stream` — list files, then `calculator` for `21*2`
4. `python examples/chat_agent.py`
5. `python examples/automation_agent.py`
6. `GROK_AGENT_SERVE_TOKEN=dev grok-agent serve --port 8765`
7. `python examples/workspace_agent.py` then `grok-agent workspace search "MCP"`

```
┌─────────────────────────────────────────┐
│  You › grok-agent team demo                 │
│  system/goal: Ship a local agent…          │
│  coordinator/note: reviewed goal           │
│  researcher/note: ready                    │
│  operator/note: ready                      │
└─────────────────────────────────────────┘
```

## Quick start (1 command)

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
grok-agent tools demo
grok-agent team demo
```

From source:

```bash
git clone https://github.com/Tryboy869/grok-local-agent-kit.git
cd grok-local-agent-kit
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
grok-agent doctor
```

Local model (optional — only needed for chat / ReAct):

```bash
ollama serve && ollama pull llama3.2
# or start LM Studio on http://127.0.0.1:1234/v1
grok-agent chat -v --stream --router
```

## Examples

| Script | Needs LLM | What it shows |
|---|---|---|
| `examples/tools_demo_agent.py` | no | calculator, list_files, system info |
| `examples/team_agent.py` | no (`--llm` optional) | multi-agent blackboard |
| `examples/chat_agent.py` | yes | interactive ReAct chat |
| `examples/automation_agent.py` | yes | one-shot goal with tools |
| `examples/mcp_agent.py` | optional | MCP stdio / HTTP / SSE |
| `examples/workspace_agent.py` | no | pack + local file RAG |

## Docs

* [CONTRIBUTING.md](CONTRIBUTING.md)
* [ROADMAP.md](ROADMAP.md)
* [CHANGELOG.md](CHANGELOG.md)
* [SHOW_HN.md](SHOW_HN.md)
* [docs/HN_INDIE_HACKERS.md](docs/HN_INDIE_HACKERS.md)

MIT © Nexus Studio / Tryboy869
