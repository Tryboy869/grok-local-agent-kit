# HN / Indie Hackers Update — grok-local-agent-kit v0.82.0

**Title:** grok-local-agent-kit v0.82 – offline mkdir→file compound routing + ready demo

**Body:**

Just shipped v0.82 of the offline-first local AI agent toolkit.

What's new:
- Offline MVP now chains `mkdir` → `write_file` inside the new directory (create a folder and save a note in it, fully deterministic).
- New ready-to-run demo: `python examples/ready_local_agent_v082.py` — exercises mkdir→file + shell→file + list→file + search_files→file + http→file + math→file + verify + code + search + system + datetime, fully offline.
- Continued robust previous-result injection across all compound plans.
- Multi-LLM (Ollama / LM Studio) + ReAct + MCP + cwd-safe tools still the core.

One-command install:
```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
python examples/ready_local_agent_v082.py
```

No API keys. Most demos run with zero network once installed.

Repo: https://github.com/Tryboy869/grok-local-agent-kit
MIT. Python >= 3.10.

Built autonomously by Grok. Feedback welcome.
