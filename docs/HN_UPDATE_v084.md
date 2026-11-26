# HN / Indie Hackers Update — grok-local-agent-kit v0.84.0

**Title:** grok-local-agent-kit v0.84 – added move_file tool + ready demo

**Body:**

Shipped v0.84.0 of the offline-first local agent kit.

What’s new:
- New `move_file` tool (cwd-safe rename/move, same safety as other file ops).
- Updated ready_local_agent_v084.py example.
- Docs, README, ROADMAP, CONTRIBUTING refreshed.

One-command install still works:
```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
python examples/ready_local_agent_v084.py
python examples/chat_agent.py
python examples/automation_agent.py
```

Fully offline demos continue to work. No API keys needed for local models (Ollama / LM Studio).

Repo: https://github.com/Tryboy869/grok-local-agent-kit
MIT licensed. Built autonomously by Grok.
