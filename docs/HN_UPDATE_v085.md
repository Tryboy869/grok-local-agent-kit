# HN / Indie Hackers Update — grok-local-agent-kit v0.85.0

**Title:** grok-local-agent-kit v0.85 – real offline MVP routing + result injection + ready demo

**Body:**

Shipped v0.85.0 of the offline-first local agent kit.

What’s new:
- Functional `mvp.py` with `route_intent` / `run_mvp` that executes real tools offline.
- Compound plans now inject previous results (shell→file, list→file, search_files→file, http→file, math→file+verify, code→file, web→file, system→file, datetime→file, copy, mkdir, move).
- New `examples/ready_local_agent_v085.py` demo that runs fully offline.
- Docs, README, ROADMAP, CONTRIBUTING, STATUS refreshed.

One-command install:
```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
python examples/ready_local_agent_v085.py
python examples/chat_agent.py
python examples/automation_agent.py
```

Fully offline demos continue to work. No API keys needed for local models (Ollama / LM Studio).

Repo: https://github.com/Tryboy869/grok-local-agent-kit
MIT licensed. Built autonomously by Grok.
