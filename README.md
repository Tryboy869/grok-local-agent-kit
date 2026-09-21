# grok-local-agent-kit

**Open-source toolkit for building local AI agents.**
Ollama + LM Studio, ReAct tool loop, multi-LLM fallback router, SQLite vector memory with **optional sqlite-vec**, MCP stdio/HTTP/SSE, local HTTP API, recipes, watcher, offline eval harness, tool cache + telemetry + budgets, **drop-in tool plugins with a Python sandbox**, **JSONL transcripts**, **workspace packer + local file RAG**, **web search with HTML fallback**, **multi-agent Team + shared blackboard**, **blackboard + roster persistence**, **task handoff queue**, **local approval gate wired into ReAct**, **scriptable approval TUI**.
Offline-first.
Built autonomously by Grok.

> Capable agents on your machine.
> No cloud required.
> No API keys for local models.

## Features (v0.34.0)

* Multi-LLM (Ollama + LM Studio / OpenAI-compat) + fallback router
* ReAct tool loop, streaming, hooks, skills, orchestrator
* **Team + Blackboard** — coordinator / researcher / operator share posts (`grok-agent team demo`)
* **Persist the board** — JSONL or SQLite (`grok-agent board demo`)
* **Persist the roster** — who is on the team + optional per-member LLM bindings (`grok-agent roster demo`)
* **Handoff queue** — offer / claim / complete tasks on the board (`grok-agent handoff demo`)
* **Approval gate** — allow / deny tools locally, now on the ReAct path (`grok-agent approve demo|react`)
* **Approval TUI** — decide pending items with a script or bulk policy (`grok-agent approve tui|queue`)
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

## Demo storyboard

Binary GIFs are not generated in this environment. Recreate them with [VHS](https://github.com/charmbracelet/vhs) or `script` + `agg`. Storyboards: `docs/gifs/README.md`.

**GIF 1 — tools (no LLM)**  
Terminal: `grok-agent tools demo` → calculator `21*2` = 42, `list_files` shows the workspace.

**GIF 2 — team + board**  
`grok-agent team demo` then `grok-agent board demo --path board.jsonl` → posts survive restart via `board show`.

**GIF 3 — roster + handoff + approvals on ReAct**  
`grok-agent roster demo` writes `roster.json`.  
`grok-agent handoff demo` offers tasks.  
`grok-agent approve demo` allow-lists `calculator`, denies `shell`.  
`grok-agent approve react` runs a fake ReAct batch: calc runs, shell is blocked, search stays pending.
`grok-agent approve tui --seed --script A003=approved,A004=denied` drains the pending queue.

```
┌───────────────────────────────────────────┐
│  You › grok-agent approve react                   │
│  calculator → 42                                 │
│  run_shell → blocked by approval gate            │
│  web_search → blocked: pending approval required │
│  saved approvals.json                            │
└───────────────────────────────────────────┘
```

## Quick start (1 command)

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
grok-agent tools demo
grok-agent team demo
grok-agent board demo
grok-agent roster demo
grok-agent handoff demo
grok-agent approve demo
grok-agent approve react
grok-agent approve tui --seed --script A003=approved,A004=denied
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
| `examples/chat_agent.py` | yes | interactive ReAct chat |
| `examples/automation_agent.py` | yes | one-shot goal with tools |
| `examples/team_agent.py` | no (`--llm` optional) | multi-agent blackboard |
| `examples/persist_agent.py` | no | save / reload board |
| `examples/roster_agent.py` | no (`--llm` optional) | persist roster + bindings |
| `examples/handoff_agent.py` | no | offer / claim / complete |
| `examples/approve_agent.py` | no | HITL allow / deny / decide |
| `examples/react_approve_agent.py` | no | ReAct batch behind the gate |
| `examples/approve_tui_agent.py` | no | scriptable HITL queue |
| `examples/workspace_agent.py` | no | pack + local file RAG |
| `examples/mcp_agent.py` | optional | MCP stdio / HTTP / SSE |

## Docs

* [CONTRIBUTING.md](CONTRIBUTING.md)
* [ROADMAP.md](ROADMAP.md)
* [CHANGELOG.md](CHANGELOG.md)
* [SHOW_HN.md](SHOW_HN.md)
* [docs/HN_INDIE_HACKERS.md](docs/HN_INDIE_HACKERS.md)

MIT © Nexus Studio / Tryboy869
