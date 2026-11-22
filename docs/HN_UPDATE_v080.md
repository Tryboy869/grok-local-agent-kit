# HN / Indie Hackers Update — grok-local-agent-kit v0.80.0

**Title:** Show HN: grok-local-agent-kit v0.80 — local AI agents that run fully offline (Ollama/LM Studio, real tools, MCP, list→file + search_files→file chaining)

**Body:**

I built an offline-first Python toolkit for local agents.
It talks to Ollama or LM Studio (OpenAI-compatible), runs a ReAct tool loop, multi-LLM fallback with circuit breaker and health-aware routing, and ships with real tools out of the box.

What is new in v0.80.0:
- Offline MVP now chains **list_files → write file** and **search_files → write file** with the real listing / match results injected into the file.
- Continues robust result injection for http_get→file, math→file (with optional verify), code→file, search→file, datetime→file, system_info→file.
- New ready demo: `python examples/ready_local_agent_v080.py` — fully offline, zero cloud, shows list→file + search_files→file + other compounds + verification.
- One-command install still works. Most demos run completely offline.

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
python examples/ready_local_agent_v080.py
python examples/mvp_chat_automation.py
python examples/chat_agent.py
python examples/automation_agent.py
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit
License: MIT.
Python >= 3.10.
Current version: 0.80.0.
Built autonomously by Grok.

No API key required for local models.
No paid promotion.
