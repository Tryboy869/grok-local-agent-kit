# grok-local-agent-kit

[![GitHub stars](https://img.shields.io/github/stars/Tryboy869/grok-local-agent-kit?style=social)](https://github.com/Tryboy869/grok-local-agent-kit/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml)
[![Version](https://img.shields.io/badge/version-0.68.0-brightgreen.svg)](https://github.com/Tryboy869/grok-local-agent-kit/releases)

**Open-source toolkit for building local AI agents.**
Ollama + LM Studio, ReAct tool loop, multi-LLM fallback router, MCP, offline-first tools (web search, cwd-safe file ops, calculator, etc.).
Built autonomously by Grok.

> Capable agents on your machine.  
> No cloud required.  
> No API keys for local models.

## Features (v0.68.0)

* **Core Agent** — ReAct-style tool loop, hooks, sessions, parallel tools, MCP attach, multi-LLM routing with health-aware fallback.
* **Multi-LLM** — Ollama native + any OpenAI-compatible endpoint (LM Studio, vLLM…). Circuit breaker + router.
* **Real tools** — web_search (HTML fallback), http_get, cwd-safe file ops, calculator, sandboxed execute_python, restricted shell, MCP, system info, datetime.
* **Offline MVP** — robust intent routing + real tools so demos run fully offline. Compound plans (math → write file, search + note, multi-step).
* **Ready examples** — `python examples/mvp_chat_automation.py` (offline chat + automation), `examples/chat_agent.py` (live interactive), `examples/automation_agent.py` (one-shot multi-tool).

**GIF / Demo storyboard (record with VHS; see docs/gifs/):**  
**Chat agent demo:** `python examples/chat_agent.py --verbose --stream` — interactive ReAct loop with local Ollama/LM Studio, tool calls visible, multi-LLM fallback if configured.
**Automation agent demo:** `python examples/automation_agent.py` — one-shot multi-tool goal execution (files, math, search).
**Offline MVP demo:** `python examples/mvp_chat_automation.py`  
1. Banner “=== grok-local-agent-kit MVP (offline) ===”.  
2. Chat turns: datetime, calculator (2**10 + 42 → 1066), system info, list files, write note, read note, compound math→file.  
3. Lists registered tools.  
4. Runs automation plan steps with short results.  
5. “Done. For live LLM start Ollama/LM Studio…”.  
Fully offline, zero cloud.  

Live demos: `python examples/chat_agent.py --verbose --stream` and `python examples/automation_agent.py`.

## Quick start (1 command)

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
python examples/mvp_chat_automation.py
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
```

Local model (optional — for full ReAct / chat):

```bash
ollama serve && ollama pull llama3.2
# or start LM Studio on http://127.0.0.1:1234/v1
grok-agent chat -v --stream --router
python examples/chat_agent.py --verbose --stream
```

## Examples

See `examples/` for chat, automation, compound chaining, MCP, approvals, and more.  
Start offline with `mvp_chat_automation.py` and the `ready_*` / `enhanced_*` scripts — no model required.  
Live chat: `chat_agent.py`. Multi-tool automation: `automation_agent.py`.
