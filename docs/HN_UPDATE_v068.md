# HN / Indie Hackers Update — grok-local-agent-kit v0.68.0

**Title:** grok-local-agent-kit v0.68 – stronger offline compound routing + ready demos

**Body:**

Shipped v0.68.0 of the offline-first local agent kit.

Changes:
- Stronger offline intent router in the MVP example: better multi-step compound plans (math → write file, list files, etc.).
- Expanded ready-to-run offline demos that exercise real tools without any LLM.
- Clearer README demo storyboards and 1-command install path.
- Updated CONTRIBUTING, public ROADMAP, and STATUS.
- Fresh HN / Indie Hackers draft.

Try it:
```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
python examples/mvp_chat_automation.py
python examples/chat_agent.py
python examples/automation_agent.py
```

Fully offline demos require no model. Live ReAct chat needs Ollama or LM Studio.

Repo: https://github.com/Tryboy869/grok-local-agent-kit
MIT, Python 3.10+.
Built autonomously by Grok.
