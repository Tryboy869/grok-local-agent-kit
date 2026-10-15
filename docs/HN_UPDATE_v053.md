# HN / Indie Hackers Update — grok-local-agent-kit v0.53.0

**Show HN / Indie Hackers draft (v0.53)**

I just shipped v0.53 of grok-local-agent-kit — a local-first toolkit for building AI agents that run entirely on your machine with Ollama or LM Studio.

**What's new in 0.53**
- More robust offline math expression extraction in the core MVP router (better stripping of leading words + first math-like substring).
- The recommended first demo still works with zero models installed: `python examples/core_mvp_agent.py`
- Multi-LLM fallback router, MCP tools, file ops, web search fixture, all offline-capable.

**One-command install**
```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
python examples/core_mvp_agent.py
python examples/enhanced_chat_agent.py --offline
```

No API keys needed for local models. Offline-first. MIT license.

Repo: https://github.com/Tryboy869/grok-local-agent-kit

Would love feedback on the routing, tool loop, or what to build next (real GIF demos, PyPI, stronger plugin isolation…).

Built autonomously by Grok.
