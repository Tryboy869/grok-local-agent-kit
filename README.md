# grok-local-agent-kit

**Open-source toolkit for building local AI agents.**
Ollama + LM Studio, ReAct tool loop, multi-LLM fallback router **with a circuit breaker on the hot path**, SQLite vector memory with **optional sqlite-vec**, MCP stdio/HTTP/SSE, local HTTP API, recipes, watcher, offline eval harness, **opt-in live-model eval profile**, tool cache + telemetry + budgets, **drop-in tool plugins with a Python sandbox**, **JSONL transcripts**, **workspace packer + local file RAG**, **web search with HTML fallback**, **multi-agent Team + shared blackboard**, **blackboard + roster persistence**, **task handoff queue**, **local approval gate wired into ReAct**, **scriptable approval TUI**, **circuit breaker health board for local backends**, **routed health persisted to health.json**, **portable kit snapshot**, **local model catalog**, **router defaults from Catalog.pick**, **offline scripted loop**, **declarative workflow runner (files + search + MCP, no daemon)**.
Offline-first.
Built autonomously by Grok.

> Capable agents on your machine.
> No cloud required.
> No API keys for local models.

## Features (v0.52.0)

* **Smarter offline core** — improved intent routing (regex math detection + expanded keywords) + ready-to-run chat & automation examples (`python examples/enhanced_chat_agent.py --offline`, `python examples/enhanced_automation_agent.py`)
* **Core MVP demo** — one script runs intent routing + tools + multi-LLM probes (`python examples/core_mvp_agent.py` or `python examples/mvp_core_demo.py`)
* **Session pack** — one command batches chat, file automation, search, and MCP echo, then writes `SESSION.md` (`grok-agent pack demo`)
* **Playbook runner** — chat + automation + search + MCP in one JSON file; ReAct handoff recorded when a provider probe is up (`grok-agent playbook demo`)
* **ReAct handoff call** — opt-in: `grok-agent handoff demo` runs a scripted loop; `grok-agent handoff live` calls `Agent.run` only if Ollama or LM Studio is up
* Multi-LLM (Ollama + LM Studio / OpenAI-compat) + fallback router
* **Health-aware routing** — open breakers are skipped in `pick` / `probe` / `chat` (`grok-agent route demo`)
* **Persisted route health** — `_mark` writes `health.json`; a new process hydrates it (`grok-agent route persist`)
* **Kit snapshot** — version, tools, file presence in one JSON (`grok-agent snapshot demo`)
* **Model catalog** — list Ollama tags + LM Studio `/v1/models`, persist `catalog.json` (`grok-agent models demo`)
* **Catalog → router** — `Catalog.pick` rewrites endpoint models (`grok-agent route catalog`)

**GIF — core MVP (storyboard):** terminal runs `python examples/core_mvp_agent.py`. It prints provider probes (Ollama / LM Studio: down or up), then walks five scenarios: files (writes a note), math (`15 * 3 + sqrt(81)`), system info, web search fixture, and MCP echo. Each step shows the detected intent and truncated tool output. Ends with “Core MVP finished. No cloud, no API keys required.” Recreate with VHS from `docs/gifs/core-mvp.md` (binary GIF optional).

## Quick start (1 command)

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
python examples/core_mvp_agent.py
python examples/mvp_core_demo.py
python examples/enhanced_automation_agent.py
python examples/enhanced_chat_agent.py --offline
```

From source:
```bash
git clone https://github.com/Tryboy869/grok-local-agent-kit.git
cd grok-local-agent-kit
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
grok-agent doctor
python examples/enhanced_automation_agent.py
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
| `examples/core_mvp_agent.py` | no | clean core offline routing + tools + probes |
| `examples/enhanced_automation_agent.py` | no | polished offline automation: routing + file/math/system/search |
| `examples/enhanced_chat_agent.py` | optional (`--offline`) | chat with multi-LLM probe + offline MVP fallback |
| `examples/mvp_core_demo.py` | no | core offline routing + tools + probes |
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
| `examples/session_pack.py` | no | chat + automation + search + MCP brief |
| `examples/mvp_chat.py` | no | intent-routed chat math |
| `examples/mvp_automation.py` | no | write a workspace note |
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
* [docs/HN_UPDATE_v050.md](docs/HN_UPDATE_v050.md)
* [docs/HN_UPDATE_v051.md](docs/HN_UPDATE_v051.md)
* [docs/HN_UPDATE_v052.md](docs/HN_UPDATE_v052.md)

MIT © Nexus Studio / Tryboy869
