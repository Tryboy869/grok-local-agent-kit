# grok-local-agent-kit

**Open-source toolkit for building local AI agents.**
Ollama + LM Studio, ReAct tool loop, multi-LLM fallback router **with a circuit breaker on the hot path**, SQLite vector memory with **optional sqlite-vec**, MCP stdio/HTTP/SSE, local HTTP API, recipes, watcher, offline eval harness, **opt-in live-model eval profile**, tool cache + telemetry + budgets, **drop-in tool plugins with a Python sandbox**, **JSONL transcripts**, **workspace packer + local file RAG**, **web search with HTML fallback**, **multi-agent Team + shared blackboard**, **blackboard + roster persistence**, **task handoff queue**, **local approval gate wired into ReAct**, **scriptable approval TUI**, **circuit breaker health board for local backends**, **routed health persisted to health.json**, **portable kit snapshot**, **local model catalog**, **router defaults from Catalog.pick**, **offline scripted loop**, **declarative workflow runner (files + search + MCP, no daemon)**.
Offline-first.
Built autonomously by Grok.

> Capable agents on your machine.
> No cloud required.
> No API keys for local models.

## Features (v0.45.0)

* Multi-LLM (Ollama + LM Studio / OpenAI-compat) + fallback router
* **Health-aware routing** — open breakers are skipped in `pick` / `probe` / `chat` (`grok-agent route demo`)
* **Persisted route health** — `_mark` writes `health.json`; a new process hydrates it (`grok-agent route persist`)
* **Kit snapshot** — version, tools, file presence in one JSON (`grok-agent snapshot demo`)
* **Model catalog** — list Ollama tags + LM Studio `/v1/models`, persist `catalog.json` (`grok-agent models demo`)
* **Catalog → router** — `Catalog.pick` rewrites endpoint models (`grok-agent route catalog`)
* **Offline scripted loop** — list + write with a fake LLM (`grok-agent offline demo`)
* **Workflow runner** — JSON steps for file ops, web search, MCP echo (`grok-agent workflow demo`)
* ReAct tool loop, streaming, hooks, skills, orchestrator
* **Team + Blackboard** — coordinator / researcher / operator share posts (`grok-agent team demo`)
* **Persist the board** — JSONL or SQLite (`grok-agent board demo`)
* **Persist the roster** — who is on the team + optional per-member LLM bindings (`grok-agent roster demo`)
* **Handoff queue** — offer / claim / complete tasks on the board (`grok-agent handoff demo`)
* **Approval gate** — allow / deny tools locally, now on the ReAct path (`grok-agent approve demo|react`)
* **Approval TUI** — decide pending items with a script or bulk policy (`grok-agent approve tui|queue`)
* **Live eval profile** — stub in CI; real model only with `--live` + `GROK_LIVE_EVAL=1` (`grok-agent eval-demo|eval-live`)
* **Health board** — per-backend circuit breaker, no LLM (`grok-agent health demo|show|trip|reset`)
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

**GIF 4 — live eval stub**  
`grok-agent eval-demo` prints `live-eval[stub] 2/2 passed`. No model process is started.

**GIF 5 — health board**  
`grok-agent health demo` → ollama closed/allow=ok, lmstudio open after two refused connections.

**GIF 6 — health-aware router**  
`grok-agent route demo` trips LM Studio, then `pick()` lands on Ollama. Probe lists `lmstudio → breaker-open` without pinging it.

**GIF 7 — persisted route health**  
`grok-agent route persist` writes `health.json`. A second router loads it and still blocks LM Studio.

**GIF 8 — kit snapshot**  
`grok-agent snapshot demo` writes `kit-snapshot.json` with version, tools, and file presence. No LLM.

**GIF 9 — model catalog**  
`grok-agent models demo` probes Ollama `/api/tags` and LM Studio `/v1/models`, writes `catalog.json`. Down backends are marked `down` instead of crashing.

**GIF 10 — catalog → router**  
`grok-agent route catalog` replaces placeholder endpoint models with `Catalog.pick` names (`llama3.2:latest`, `qwen2.5-7b`). No live chat.

```
┌───────────────────────────────────────────┐
│  You › grok-agent route catalog                              │
│  catalog-route                                               │
│  before:                                                     │
│    ollama model=llama3.2                                     │
│    lmstudio model=local-model                                │
│  changes:                                                    │
│    ollama: llama3.2 -> llama3.2:latest                        │
│    lmstudio: local-model -> qwen2.5-7b                        │
└───────────────────────────────────────────┘
```

## MVP (runs with zero models)

```bash
pip install -e .
grok-agent mvp
python examples/mvp_chat.py "compute sqrt(144) + 10"
python examples/mvp_automation.py
```

The scripted router picks an intent, then calls the same tools as the ReAct agent (`write_file`, `list_files`, `calculator`, `web_search`, `get_system_info`, MCP echo). Ollama and LM Studio are probed but not required.

**GIF — offline MVP (storyboard, binary not in repo):** terminal runs `grok-agent mvp`, prints `intent=math` / `22.0`, confirms `mvp_note.txt`, then shows provider probes `down` or `up`. Recreate with VHS from `docs/gifs/mvp-demo.md`.

## Quick start (1 command)

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
grok-agent tools demo
grok-agent models demo
grok-agent route catalog
grok-agent snapshot demo
grok-agent team demo
grok-agent board demo
grok-agent roster demo
grok-agent handoff demo
grok-agent approve demo
grok-agent approve react
grok-agent approve tui --seed --script A003=approved,A004=denied
grok-agent eval-demo
grok-agent health demo
grok-agent route demo
grok-agent route persist
grok-agent offline demo
grok-agent workflow demo
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

Local model (optional — only needed for chat / ReAct / live eval):

```bash
ollama serve && ollama pull llama3.2
# or start LM Studio on http://127.0.0.1:1234/v1
grok-agent chat -v --stream --router
GROK_LIVE_EVAL=1 grok-agent eval-live --live
```

## Examples

| Script | Needs LLM | What it shows |
|---|---|---|
| `examples/tools_demo_agent.py` | no | calculator, list_files, system info |
| `examples/catalog_agent.py` | no | local Ollama / LM Studio model list |
| `examples/catalog_route_agent.py` | no | Catalog.pick → router models |
| `examples/snapshot_agent.py` | no | portable kit snapshot JSON |
| `examples/chat_agent.py` | yes | interactive ReAct chat |
| `examples/automation_agent.py` | yes | one-shot goal with tools |
| `examples/team_agent.py` | no (`--llm` optional) | multi-agent blackboard |
| `examples/persist_agent.py` | no | save / reload board |
| `examples/roster_agent.py` | no (`--llm` optional) | persist roster + bindings |
| `examples/handoff_agent.py` | no | offer / claim / complete |
| `examples/approve_agent.py` | no | HITL allow / deny / decide |
| `examples/react_approve_agent.py` | no | ReAct batch behind the gate |
| `examples/approve_tui_agent.py` | no | scriptable HITL queue |
| `examples/live_eval_agent.py` | no (unless `--live`) | stub / live eval profile |
| `examples/health_agent.py` | no | circuit breaker board |
| `examples/route_health_agent.py` | no | router skips an open breaker |
| `examples/persist_route_agent.py` | no | router writes / reloads health.json |
| `examples/workspace_agent.py` | no | pack + local file RAG |
| `examples/mcp_agent.py` | optional | MCP stdio / HTTP / SSE |
| `examples/workflow_agent.py` | no | files + search fixture + MCP echo |
| `examples/offline_chat_agent.py` | no | scripted chat loop |
| `examples/offline_automation_agent.py` | no | scripted write |


## Demo storyboard (GIF)

Binary GIFs are not checked in yet (record them locally; script below). Until then, this is the 12-second terminal storyboard for `docs/gifs/workflow-demo.gif`:

1. `00:00` prompt: `grok-agent workflow demo`
2. `00:02` step 1 `list_files` prints `inbox.txt`
3. `00:04` step 2 `write_file` creates `automation-note.txt`
4. `00:07` step 3 `web_search` returns the offline fixture (Ollama + LM Studio)
5. `00:10` step 4 `mcp_call` echoes the listing as JSON
6. `00:12` line `wrote=True` — no cloud key, no daemon

Record:

```bash
# asciinema rec docs/gifs/workflow-demo.cast
grok-agent workflow demo
# agg docs/gifs/workflow-demo.cast docs/gifs/workflow-demo.gif
```

## Docs

* [CONTRIBUTING.md](CONTRIBUTING.md)
* [ROADMAP.md](ROADMAP.md)
* [CHANGELOG.md](CHANGELOG.md)
* [SHOW_HN.md](SHOW_HN.md)
* [docs/HN_INDIE_HACKERS.md](docs/HN_INDIE_HACKERS.md)

MIT © Nexus Studio / Tryboy869
