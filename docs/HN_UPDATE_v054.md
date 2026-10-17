# HN / Indie Hackers Update — v0.54.0

**Title:** Show HN: grok-local-agent-kit v0.54 – local AI agents (Ollama / LM Studio, offline MVP, real tools)

**Body:**

Just shipped v0.54 of grok-local-agent-kit — an offline-first Python toolkit for building local AI agents.

Core idea: run capable agents entirely on your machine with Ollama or LM Studio. No API keys, no cloud.

**What’s new / polished in the MVP:**

- Solid core agent with ReAct tool loop, multi-LLM routing (Ollama + LM Studio), and provider health probes.
- Real tools out of the box: web search (with offline fixture + HTML fallback), file ops (read/write/list/search/delete, cwd-safe), shell, execute_python, calculator, system info, MCP foundation.
- Ready-to-run examples:
  - `python examples/chat_agent.py` — interactive chat with tools
  - `python examples/automation_agent.py` — one-shot goal that writes files, calculates, searches, etc.
  - Offline core demo: `python examples/core_mvp_agent.py` or `grok-agent mvp` (works with zero models)
- One-command install:
  ```bash
  curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
  grok-agent doctor
  ```
- Demo storyboards (GIFs to be recorded):
  - Chat agent: user asks a question → agent calls web_search or calculator → streams answer.
  - Automation agent: goal to create a Python file, list dir, compute sqrt, search files, web search → final summary.

Also included: MCP (stdio/HTTP/SSE), multi-agent team + blackboard, local approval gates, workflows, vector memory, eval harness, circuit breaker router, and more.

**Try it:**

```bash
git clone https://github.com/Tryboy869/grok-local-agent-kit.git
cd grok-local-agent-kit
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python examples/core_mvp_agent.py   # offline
# or with a model:
# ollama pull llama3.2 && python examples/chat_agent.py
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit  
License: MIT. Python ≥ 3.10. Version: 0.54.0.

Feedback welcome — especially on the offline path and local LLM routing.

Built autonomously by Grok for local-first agents.
