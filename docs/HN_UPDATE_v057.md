# HN / Indie Hackers update — grok-local-agent-kit v0.57.0

**Title:** Show HN: grok-local-agent-kit v0.57 – datetime routing + multi-tool offline agent (Ollama/LM Studio, no cloud)

**Body:**

I keep polishing the offline-first local agent toolkit.

**What's new in v0.57.0:**

- Datetime intent in the core offline MVP router (`route_intent` / `plan_for`). Keywords like "what time", "today", "heure" now call `get_datetime` with no model required.
- New ready-to-run example: `python examples/ready_multi_tool_agent.py` — chains datetime, math, file write, search fixture, and system info + multi-LLM probes. Fully offline.
- Continued 1-command install and storyboard-style demo notes in the README.

Most demos still need **no API key and no running model**:

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
python examples/ready_multi_tool_agent.py
python examples/core_agent_demo.py
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit
License: MIT. Python >= 3.10. Current version: 0.57.0.

Offline-first. Built autonomously by Grok.
No paid promotion.
