# grok-local-agent-kit

[![GitHub stars](https://img.shields.io/github/stars/Tryboy869/grok-local-agent-kit?style=social)](https://github.com/Tryboy869/grok-local-agent-kit/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml)
[![Version](https://img.shields.io/badge/version-0.63.0-brightgreen.svg)](https://github.com/Tryboy869/grok-local-agent-kit/releases)

**Open-source toolkit for building local AI agents.**
Ollama + LM Studio, ReAct tool loop, multi-LLM fallback router, MCP, offline-first tools (web search, cwd-safe file ops, calculator, etc.).
Built autonomously by Grok.

> Capable agents on your machine.  
> No cloud required.  
> No API keys for local models.

## Features (v0.63.0)

* **Core Agent** — ReAct-style tool loop, hooks, sessions, parallel tools, MCP attach.
* **Multi-LLM** — Ollama native + any OpenAI-compatible endpoint (LM Studio, vLLM…). Health-aware router.
* **Real tools** — web_search (with HTML fallback), http_get, cwd-safe file ops (list/read/write/search/delete…), calculator, execute_python (sandboxed), shell (restricted), MCP stdio, system info, datetime.
* **Offline MVP** — intent routing + real tools so demos run without a model.
* **Ready examples** — `python examples/mvp_chat_automation.py`, `ready_compound_agent.py`, `enhanced_core_agent.py`, etc.

**GIF / Demo storyboard (describe & record with VHS):**  
Terminal: `python examples/mvp_chat_automation.py`  
1. Prints “MVP (offline)”.  
2. Chat turns: time → datetime, math → calculator result, system info, write note, read note.  
3. Shows registered tools.  
4. Automation plan steps execute and print short results.  
5. Ends with “Done. For live LLM…”.  
Fully offline. Source storyboards live in `docs/gifs/`.

## Quick start (1 command)

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
python examples/mvp_chat_automation.py
python examples/ready_compound_agent.py
python examples/enhanced_core_agent.py
```

From source:

```bash
git clone https://github.com/Tryboy869/grok-local-agent-kit.git
cd grok-local-agent-kit
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python examples/mvp_chat_automation.py
```

Local model (optional — for full ReAct / chat):

```bash
ollama serve && ollama pull llama3.2
# or start LM Studio on http://127.0.0.1:1234/v1
grok-agent chat -v --stream --router
```

## Examples

See `examples/` for chat, automation, compound chaining, MCP, approvals, and more.  
Start offline with `mvp_chat_automation.py` and the `ready_*` / `enhanced_*` scripts — no model required.
