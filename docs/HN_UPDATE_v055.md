# HN / Indie Hackers Update — v0.55.0

**Title:** Show HN: grok-local-agent-kit v0.55 – enhanced core local AI agents (Ollama/LM Studio, offline MVP, real tools)

**Body:**

Shipped v0.55 of grok-local-agent-kit — offline-first Python toolkit for local AI agents.

Run capable agents on your machine with Ollama or LM Studio. No API keys required for the local path.

**What’s new:**

- Enhanced core agent with better intent routing and real tools out of the box: web search (fixture + HTML fallback), file operations (cwd-safe), calculator, system info, MCP echo.
- New ready-to-run example: `python examples/core_agent_demo.py` — full offline demo of routing + tools + multi-LLM health probes.
- One-command install still works:
  ```bash
  curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
  grok-agent doctor
  python examples/core_agent_demo.py
  ```
- Demo storyboard (GIF to record): probes → file write → math → system → search → MCP echo. Ends offline with no cloud.

Also: ReAct loop, multi-LLM fallback router with circuit breaker, MCP (stdio/HTTP/SSE), multi-agent teams, approval gates, workflows, memory, eval, and more.

**Try it:**

```bash
git clone https://github.com/Tryboy869/grok-local-agent-kit.git
cd grok-local-agent-kit
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python examples/core_agent_demo.py   # offline core
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit  
License: MIT. Python ≥ 3.10. Version: 0.55.0.

Feedback welcome. Built autonomously by Grok for local-first agents.
