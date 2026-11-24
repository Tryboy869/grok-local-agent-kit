# grok-local-agent-kit

[![GitHub stars](https://img.shields.io/github/stars/Tryboy869/grok-local-agent-kit?style=social)](https://github.com/Tryboy869/grok-local-agent-kit/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml)
[![Version](https://img.shields.io/badge/version-0.82.0-brightgreen.svg)](https://github.com/Tryboy869/grok-local-agent-kit/releases)

**Open-source toolkit for building local AI agents.**
Ollama + LM Studio, ReAct tool loop, multi-LLM fallback router, MCP, offline-first tools (web search, cwd-safe file ops, calculator, sandboxed Python, etc.).
Built autonomously by Grok.

> Capable agents on your machine.  
> No cloud required.  
> No API keys for local models.

## Features (v0.82.0)

* **Core Agent** — ReAct-style tool loop, hooks, sessions, parallel tools, MCP attach, multi-LLM routing with health-aware fallback.
* **Multi-LLM** — Ollama native + any OpenAI-compatible endpoint (LM Studio, vLLM…). Circuit breaker + router.
* **Real tools** — web_search (HTML fallback), http_get, cwd-safe file ops, calculator, sandboxed execute_python, restricted shell, MCP, system info, datetime, search_files.
* **Offline MVP** — robust intent routing + real tools so demos run fully offline. Compound plans (math → write file with result injection + optional read verification, **code → write file with result injection**, **search → write file with result injection**, **datetime → write file with result injection**, **system info → write file with result injection**, **http_get → write file with result injection**, **list_files → write file with result injection**, **search_files → write file with result injection**, **shell → write file with result injection**, **mkdir → write file inside new directory**, multi-step).
* **Ready examples** — `python examples/mvp_chat_automation.py` (offline chat + automation), `examples/chat_agent.py` (live interactive), `examples/automation_agent.py` (one-shot multi-tool), `examples/ready_compound_agent.py`, `examples/ready_local_agent.py`, `examples/ready_local_agent_v080.py`, **new** `examples/ready_local_agent_v082.py`.
 * **v0.82 polish** — offline MVP now chains restricted shell → file write with the real command output injected. Continues robust previous-result injection for all compound plans. Ready demo includes shell→file + list→file + search_files→file + http→file + math→file + verify + list.

**GIF / Demo storyboard (record with VHS; see docs/gifs/):**  
**Chat agent demo:** `python examples/chat_agent.py --verbose --stream` — interactive ReAct loop with local Ollama/LM Studio, tool calls visible, multi-LLM fallback if configured. Shows thoughts, parallel tools, final answer.  
**Automation agent demo:** `python examples/automation_agent.py` — one-shot multi-tool goal execution (files, math, search, system info).  
**Offline MVP / Ready local demo:** `python examples/mvp_chat_automation.py` or `python examples/ready_local_agent.py` or `python examples/ready_local_agent_v082.py`  
1. Banner “=== grok-local-agent-kit Ready Local Agent (v0.82) ===”.  
2. Chat turns: shell→file, list→file, search_files→file, math→file + verify, system→file, datetime→file, calculator (2**10 + 42 → 1066), **code execution** (print(sum(range(1,11))) → 55), **code→file** (result written to sum_result.txt), **search→file** (results written to search_note.txt), write note, compound math→file.  
3. Lists registered tools.  
4. Runs automation plan steps with short results.  
5. “Done. For live LLM start Ollama/LM Studio…”.  
Fully offline, zero cloud. Includes sandboxed Python + restricted shell + result injection for multi-step plans.  

Live demos: `python examples/chat_agent.py --verbose --stream` and `python examples/automation_agent.py`.

## Quick start (1 command)

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
python examples/mvp_chat_automation.py
python examples/ready_local_agent.py
python examples/ready_local_agent_v080.py
python examples/ready_local_agent_v082.py
python examples/chat_agent.py
python examples/automation_agent.py
```

From source:

```bash
git clone https://github.com/Tryboy869/grok-local-agent-kit.git
cd grok-local-agent-kit
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python examples/mvp_chat_automation.py
python examples/ready_local_agent.py
python examples/ready_local_agent_v080.py
python examples/ready_local_agent_v082.py
```

Local model (optional — for full ReAct / chat):

```bash
ollama serve && ollama pull llama3.2
# or start LM Studio on http://127.0.0.1:1234/v1
grok-agent chat -v --stream --router
python examples/chat_agent.py --verbose --stream
python examples/ready_local_agent.py --live
```

## Examples

See `examples/` for chat, automation, compound chaining, MCP, approvals, and more.  
Start offline with `mvp_chat_automation.py`, `ready_local_agent.py`, `ready_local_agent_v082.py` and the `ready_*` / `enhanced_*` scripts — no model required.  
Live chat: `chat_agent.py`. Multi-tool automation: `automation_agent.py`.
