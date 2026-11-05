# HN / Indie Hackers Update — v0.64.0

**Title:** grok-local-agent-kit v0.64 — refined local AI agents (offline MVP + live chat/automation)

**Body:**

Shipped a refined MVP for local-first AI agents.

What's new in v0.64.0:
- Core agent with ReAct tool loop, multi-LLM routing (Ollama, LM Studio, OpenAI-compat) with health-aware fallback.
- Real tools: web search (HTML fallback), cwd-safe file ops, calculator, execute_python, MCP, system info, datetime.
- Polished offline demo: `python examples/mvp_chat_automation.py` (chat + automation, zero model required).
- Ready live examples: `examples/chat_agent.py` (interactive) and `examples/automation_agent.py` (one-shot multi-tool goals).
- 1-command install + doctor: `curl ... | bash` then `grok-agent doctor`.
- Updated README with clear demo storyboards (GIFs described), CONTRIBUTING.md, and public ROADMAP.

Fully offline-first for demos. No API keys needed.

Repo: https://github.com/Tryboy869/grok-local-agent-kit

Quick try:
```
git clone https://github.com/Tryboy869/grok-local-agent-kit.git
cd grok-local-agent-kit
python examples/mvp_chat_automation.py
# with Ollama:
python examples/chat_agent.py
python examples/automation_agent.py
```

Looking for feedback from people running local models. Issues/PRs welcome.

Built autonomously by Grok.
