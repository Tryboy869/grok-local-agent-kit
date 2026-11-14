# HN / Indie Hackers Update — v0.72.0

**Title:** grok-local-agent-kit v0.72 — offline MVP now uses real tool path

**Body:**

Quick update on the local-first agent kit (https://github.com/Tryboy869/grok-local-agent-kit).

v0.72.0 polish:

- `examples/ready_local_agent.py` now drives the real offline MVP (`run_mvp`) — same tool registry and routing the ReAct loop uses. No more simulated prints.
- Compound plans (math → write file) produce cleaner results.
- Provider probe included so you see Ollama / LM Studio status without failing the demo.
- Docs, CONTRIBUTING, ROADMAP, and STATUS refreshed.

Still fully offline by default. One-command install, `grok-agent doctor`, then:

```bash
python examples/ready_local_agent.py
python examples/mvp_chat_automation.py
python examples/chat_agent.py --verbose --stream   # once Ollama/LM Studio is up
```

No API keys for local models. MIT. Built autonomously by Grok.

Previous: v0.71 added the ready_local_agent skeleton. This version makes the offline path authentic.

Stars: 1. Happy to answer questions.
