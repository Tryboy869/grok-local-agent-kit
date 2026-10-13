# Show HN / Indie Hackers update — v0.51.0

**Title:** Show HN: grok-local-agent-kit – core offline MVP for local AI agents (routing, tools, multi-LLM, no cloud)

**Body:**

Shipped a clean core MVP for building local AI agents.

What you get today (v0.51.0):

- Offline intent routing + real tools (write_file, calculator, list_files, system info, web search fixture, MCP echo)
- Multi-LLM support with probes for Ollama and LM Studio (OpenAI-compatible) — demos run even if both are down
- Ready-to-run entry point: python examples/core_mvp_agent.py
- 1-command install

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
python examples/core_mvp_agent.py
python examples/enhanced_automation_agent.py
```

Once you have a local model:

```bash
ollama pull llama3.2
python examples/chat_agent.py
# or with router fallback
grok-agent chat --router
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit
License: MIT
Python >= 3.10

Offline-first. No API keys required for the core demos.
Built autonomously by Grok.
