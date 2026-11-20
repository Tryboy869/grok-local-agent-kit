# Show HN Draft (ready to copy-paste) — v0.77.0

**Title:**

Show HN: grok-local-agent-kit v0.77 – local AI agents that run fully offline (Ollama/LM Studio, real tools, MCP, no cloud)

**Body:**

I built an offline-first Python toolkit for local agents.
It talks to Ollama or LM Studio (OpenAI-compatible), runs a ReAct tool loop, multi-LLM fallback with circuit breaker and health-aware routing, and ships with real tools out of the box.

What is in the box today (v0.77.0):

- One-command install + `grok-agent doctor`
- Polished offline MVP: `python examples/mvp_chat_automation.py` (chat turns + automation plan, fully offline — datetime, math, files, system info, code, search)
- Ready demos: `examples/ready_local_agent_v077.py` (system→file, datetime→file, code→file, search→file with result injection)
- Live examples: `examples/chat_agent.py` (interactive) and `examples/automation_agent.py` (one-shot multi-tool)
- Compound offline routing: math→file, code→file, search→file, datetime→file, system_info→file (real result injected)
- Multi-LLM health-aware router, sessions, playbooks, handoffs, workflows, multi-agent Team + blackboard, local approval gate + TUI, circuit breaker
- MCP (stdio / HTTP / SSE), workspace packer + local RAG, optional vector memory, eval harness, budgets, JSONL transcripts, portable kit snapshot, model catalog
- Full CI (pytest + ruff), MIT license, detailed README with badges, ROADMAP, CONTRIBUTING

No API key required for local models.
Most demos run completely offline (zero cloud).

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
python examples/mvp_chat_automation.py
python examples/ready_local_agent_v077.py
python examples/chat_agent.py
python examples/automation_agent.py
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit
License: MIT.
Python >= 3.10.
Current version: 0.77.0.
Stars at time of writing: 1.
No paid promotion, no star exchange.
Built autonomously by Grok (Nexus Studio / Tryboy869).

From source:

```bash
git clone https://github.com/Tryboy869/grok-local-agent-kit.git
cd grok-local-agent-kit
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
grok-agent doctor
python examples/ready_local_agent_v077.py
```

Feedback, issues, and stars welcome. Goal: useful local agents for everyone.
