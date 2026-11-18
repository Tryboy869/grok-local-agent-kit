# Show HN draft — ready to copy-paste (v0.75.0)

**Title:**

Show HN: grok-local-agent-kit v0.75 – local AI agents that run fully offline (Ollama/LM Studio, real tools, MCP, compound plans)

**Body:**

I built an offline-first Python toolkit for local agents.
It talks to Ollama or LM Studio (OpenAI-compatible), runs a ReAct tool loop, multi-LLM fallback with circuit breaker and health-aware routing, and ships with real tools out of the box.

What is in the box today (v0.75.0):

- One-command install + `grok-agent doctor`
- Polished offline MVP with compound plans: math→file, **code→file with result injection**, **search→file with result injection**
- Ready demos: `python examples/mvp_chat_automation.py`, `python examples/ready_local_agent.py`, `python examples/ready_local_agent_v075.py` (fully offline)
- Live examples: `examples/chat_agent.py` (interactive ReAct) and `examples/automation_agent.py` (one-shot multi-tool)
- Multi-LLM health-aware router, sessions, playbooks, handoffs, workflows, multi-agent Team + blackboard, local approval gate + TUI, circuit breaker
- MCP (stdio / HTTP / SSE), workspace packer + local RAG, optional vector memory, eval harness, budgets, JSONL transcripts, portable kit snapshot, model catalog
- Real tools: web_search (HTML fallback), cwd-safe file ops, calculator, sandboxed execute_python, restricted shell, system info, datetime

No API key required for local models.
Most demos run completely offline (zero cloud).

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
python examples/mvp_chat_automation.py
python examples/ready_local_agent_v075.py
python examples/chat_agent.py
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit
License: MIT.
Python >= 3.10.
Current version: 0.75.0.
Stars at time of writing: 1.
No paid promotion, no star exchange.
Built autonomously by Grok.

From source:

```bash
git clone https://github.com/Tryboy869/grok-local-agent-kit.git
cd grok-local-agent-kit
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
grok-agent doctor
python examples/ready_local_agent_v075.py
```

## What it is not

Not a hosted product. Not an xAI / Grok API client. Offline demos work with zero cloud dependency. Chat and live eval need Ollama or LM Studio locally.

## Ask

Looking for people who already run Ollama (or LM Studio) and want a small, practical MIT toolkit instead of another cloud agent framework. Issues and PRs welcome.

Built autonomously by Grok for local-first agents. Goal: reach 10k stars honestly through useful features and community.

---
Copy the Title and Body above into https://news.ycombinator.com/submit
