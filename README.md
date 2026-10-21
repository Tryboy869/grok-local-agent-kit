# grok-local-agent-kit

[![GitHub stars](https://img.shields.io/github/stars/Tryboy869/grok-local-agent-kit?style=social)](https://github.com/Tryboy869/grok-local-agent-kit/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml)
[![Version](https://img.shields.io/badge/version-0.58.0-brightgreen.svg)](https://github.com/Tryboy869/grok-local-agent-kit/releases)

**Open-source toolkit for building local AI agents.**
Ollama + LM Studio, ReAct tool loop, multi-LLM fallback router **with a circuit breaker on the hot path**, SQLite vector memory with **optional sqlite-vec**, MCP stdio/HTTP/SSE, local HTTP API, recipes, watcher, offline eval harness, **opt-in live-model eval profile**, tool cache + telemetry + budgets, **drop-in tool plugins with a Python sandbox**, **JSONL transcripts**, **workspace packer + local file RAG**, **web search with HTML fallback**, **multi-agent Team + shared blackboard**, **blackboard + roster persistence**, **task handoff queue**, **local approval gate wired into ReAct**, **scriptable approval TUI**, **circuit breaker health board for local backends**, **routed health persisted to health.json**, **portable kit snapshot**, **local model catalog**, **router defaults from Catalog.pick**, **offline scripted loop**, **declarative workflow runner (files + search + MCP, no daemon)**.
Offline-first.
Built autonomously by Grok.

> Capable agents on your machine.
> No cloud required.
> No API keys for local models.

## Features (v0.57.0)

* **Datetime intent** — offline MVP router now detects time/date queries and calls `get_datetime`.
* **Multi-tool ready example** — `python examples/enhanced_core_agent.py
python examples/ready_multi_tool_agent.py` chains datetime, math, files, search fixture, and system info + probes. Fully offline.
* **Polished core agent** — improved intent routing + real tools (web search, file ops, calculator, system info, MCP echo) + multi-LLM probes.
* **Ready-to-run examples** — `python examples/ready_chat_agent.py` and `python examples/ready_automation_agent.py` (fully offline).
* **Smarter offline core** — regex math detection + expanded keywords + ready demos.
* **Session pack** — one command batches chat, file automation, search, and MCP echo, then writes `SESSION.md`.
* **Playbook runner** — chat + automation + search + MCP in one JSON file.
* Multi-LLM (Ollama + LM Studio / OpenAI-compat) + fallback router with health-aware routing.
* **Health-aware routing** — open breakers are skipped.
* **Persisted route health**, **kit snapshot**, **model catalog**, **catalog → router**.

**GIF — multi-tool / ready agent demo (storyboard):**  
Terminal runs `python examples/enhanced_core_agent.py
python examples/ready_multi_tool_agent.py`.  
1. Prints multi-LLM probes (Ollama / LM Studio status).  
2. Datetime goal → current UTC time.  
3. Math goal → calculator result.  
4. File write goal → intent=files, creates mvp_note.txt.  
5. Search goal → fixture results.  
6. System goal → OS / Python info.  
7. Ends with success message. Fully offline.  
Recreate with VHS from docs/gifs (binary GIF optional until recorded).

## Quick start (1 command)

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
python examples/enhanced_core_agent.py
python examples/ready_multi_tool_agent.py
python examples/core_agent_demo.py
python examples/ready_chat_agent.py
python examples/ready_automation_agent.py
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
python examples/enhanced_core_agent.py
python examples/ready_multi_tool_agent.py
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
| `examples/ready_multi_tool_agent.py` | no | chains datetime + math + files + search + system + probes |
| `examples/enhanced_core_agent.py` | no | polished core routing + datetime/math/files/search/system/MCP + probes |
| `examples/core_agent_demo.py` | no | enhanced core routing + tools + probes |
| `examples/ready_chat_agent.py` | no | offline chat-style turns with tools + probes |
| `examples/ready_automation_agent.py` | no | one-shot automation goals + tools + probes |
| `examples/core_mvp_agent.py` | no | clean core offline routing + tools + probes |
| `examples/enhanced_automation_agent.py` | no | polished offline automation: routing + file/math/system/search |
| `examples/enhanced_chat_agent.py` | optional (`--offline`) | chat with multi-LLM probe + offline MVP fallback |
| `examples/mvp_core_demo.py` | no | core offline routing + tools + probes |
| `examples/chat_agent.py` | yes | interactive ReAct chat |
| `examples/automation_agent.py` | yes | one-shot goal with tools |
| `examples/team_agent.py` | no (`--llm` optional) | multi-agent blackboard |
| `examples/handoff_agent.py` | no | offer / claim / complete |
| `examples/approve_agent.py` | no | HITL allow / deny / decide |
| `examples/workflow_agent.py` | no | files + search fixture + MCP echo |
| ... | | (many more in examples/) |

## GIF — enhanced core agent (storyboard)

Terminal runs `python examples/enhanced_core_agent.py`:
1. Multi-LLM probes (Ollama / LM Studio status)
2. Datetime goal → current time
3. Math goal → calculator result (supports ** and sqrt)
4. File write goal → creates note
5. Search goal → offline fixture results
6. System goal → OS / Python info
7. MCP echo goal → structured payload
8. Ends with success message. Fully offline.

Recreate with VHS from docs/gifs when recorded.


## Demo storyboard (GIF)

Binary GIFs are not checked in yet (record them locally with VHS/agg). Until then, this is the terminal storyboard for the ready multi-tool agent:

1. `00:00` prompt: `python examples/enhanced_core_agent.py
python examples/ready_multi_tool_agent.py`
2. `00:02` multi-LLM probes: Ollama and LM Studio status
3. `00:04` datetime goal → current time
4. `00:07` math goal → calculator result
5. `00:10` file write goal → writes mvp_note.txt
6. `00:12` search goal → fixture results
7. `00:14` system goal → OS/Python info
8. Ends with “Multi-tool demo complete. Offline-first.”

Record:

```bash
# asciinema rec docs/gifs/ready-multi-tool.cast
python examples/enhanced_core_agent.py
python examples/ready_multi_tool_agent.py
# agg docs/gifs/ready-multi-tool.cast docs/gifs/ready-multi-tool.gif
```

## Docs

* [CONTRIBUTING.md](CONTRIBUTING.md)
* [ROADMAP.md](ROADMAP.md)
* [CHANGELOG.md](CHANGELOG.md)
* [SHOW_HN.md](SHOW_HN.md)
* [docs/HN_INDIE_HACKERS.md](docs/HN_INDIE_HACKERS.md)
* [docs/HN_UPDATE_v057.md](docs/HN_UPDATE_v057.md)

MIT © Nexus Studio / Tryboy869
