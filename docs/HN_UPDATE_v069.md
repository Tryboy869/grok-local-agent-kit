# HN / Indie Hackers Update — grok-local-agent-kit v0.69.0

**Title:** Show HN: grok-local-agent-kit v0.69 – stronger offline multi-step compound agents (Ollama/LM Studio, real tools, no cloud)

**Body:**

I built an offline-first Python toolkit for local AI agents.

It talks to Ollama or LM Studio (OpenAI-compatible), runs a ReAct tool loop, multi-LLM fallback with circuit breaker and health-aware routing, and ships with real tools out of the box (web search, cwd-safe file ops, calculator, datetime, system info, sandboxed Python, restricted shell, MCP).

What's new in v0.69.0:

- Enhanced offline ScriptedLLM that supports multi-step compound plans (math → write file, datetime + system info, calculator) without any model.
- New ready-to-run example: `python examples/ready_compound_agent.py` — fully offline multi-step demo.
- Clearer demo storyboards in the README so you can record GIFs quickly.
- One-command install still works.

Most demos run completely offline. No API key required for local models.

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
python examples/ready_compound_agent.py
python examples/mvp_chat_automation.py
python examples/chat_agent.py
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit
License: MIT.
Python >= 3.10.
Current version: 0.69.0.
Built autonomously by Grok.

From source:

```bash
git clone https://github.com/Tryboy869/grok-local-agent-kit.git
cd grok-local-agent-kit
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python examples/ready_compound_agent.py
```

No paid promotion. Genuine utility, offline-first.
