# grok-local-agent-kit

[![GitHub stars](https://img.shields.io/github/stars/Tryboy869/grok-local-agent-kit?style=social)](https://github.com/Tryboy869/grok-local-agent-kit/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml)
[![Version](https://img.shields.io/badge/version-0.62.0-brightgreen.svg)](https://github.com/Tryboy869/grok-local-agent-kit/releases)

**Open-source toolkit for building local AI agents.**
Ollama + LM Studio, ReAct tool loop, multi-LLM fallback router **with a circuit breaker on the hot path**, SQLite vector memory with **optional sqlite-vec**, MCP stdio/HTTP/SSE, local HTTP API, recipes, watcher, offline eval harness, **opt-in live-model eval profile**, tool cache + telemetry + budgets, **drop-in tool plugins with a Python sandbox**, **JSONL transcripts**, **workspace packer + local file RAG**, **web search with HTML fallback**, **multi-agent Team + shared blackboard**, **blackboard + roster persistence**, **task handoff queue**, **local approval gate wired into ReAct**, **scriptable approval TUI**, **circuit breaker health board for local backends**, **routed health persisted to health.json**, **portable kit snapshot**, **local model catalog**, **router defaults from Catalog.pick**, **offline scripted loop**, **declarative workflow runner (files + search + MCP, no daemon)**.
Offline-first.
Built autonomously by Grok.

> Capable agents on your machine.
> No cloud required.
> No API keys for local models.

## Features (v0.62.0)

* **Compound intent routing** — offline MVP now chains tools for goals like “calculate 2**10 + 42 and save to result.txt” (calculator → write_file with real result injected).
* **Read-file intent** — simple “read result.txt” goals call `read_file`.
* **Ready compound example** — `python examples/ready_compound_agent.py` demonstrates math→file chaining + read-back. Fully offline.
* **Datetime intent** — offline MVP router detects time/date queries and calls `get_datetime`.
* **Multi-tool ready examples** — `python examples/enhanced_core_agent.py` and `python examples/ready_multi_tool_agent.py` chain datetime, math, files, search fixture, and system info + probes.
* **Polished core agent** — improved intent routing + real tools (web search, file ops, calculator, system info, MCP echo) + multi-LLM probes.
* **Ready-to-run examples** — `python examples/ready_chat_agent.py` and `python examples/ready_automation_agent.py` (fully offline).
* Multi-LLM (Ollama + LM Studio / OpenAI-compat) + fallback router with health-aware routing.
* **Health-aware routing**, **persisted route health**, **kit snapshot**, **model catalog**.

**GIF — compound / multi-tool demo (storyboard):**  
Terminal runs `python examples/ready_compound_agent.py` then `python examples/enhanced_core_agent.py`.  
1. Prints multi-LLM probes (Ollama / LM Studio status).  
2. Datetime goal → current UTC time.  
3. Compound math+save goal → calculator then writes result.txt with the actual value.  
4. Read goal → shows the file content.  
5. System / file goals → OS info and notes.  
6. Ends with success message. Fully offline.  
Recreate with VHS from docs/gifs (binary GIF optional until recorded).

## Quick start (1 command)

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
python examples/ready_compound_agent.py
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
python examples/ready_compound_agent.py
python examples/enhanced_core_agent.py
```

Local model (optional — only needed for chat / ReAct / live eval):

```bash
ollama serve && ollama pull llama3.2
# or start LM Studio on http://127.0.0.1:1234/v1
grok-agent chat -v --stream --router
GROK_LIVE_EVAL=1 grok-agent eval-live --live
```

## Examples

See `examples/` for chat, automation, compound chaining, MCP, approvals, and more.
Start offline with the ready_* and enhanced_* scripts — no model required.
