# HN / Indie Hackers Update — grok-local-agent-kit v0.66.0

**Title:** Show HN: grok-local-agent-kit v0.66 — offline-first local AI agents (Ollama, MCP, real tools, no cloud)

**Body:**

I built an offline-first Python toolkit for local AI agents.

It talks to Ollama or LM Studio (OpenAI-compatible), runs a ReAct tool loop, multi-LLM fallback with circuit breaker, and ships with real tools out of the box (web search, cwd-safe file ops, calculator, sandboxed Python, MCP, etc.).

What is in the box today (v0.66.0):

- One-command install + `grok-agent doctor`
- Polished offline MVP: `python examples/mvp_chat_automation.py` (chat turns + automation plan, fully offline — datetime, math, files, system info). Compound routing (math → file).
- Live examples: `examples/chat_agent.py` (interactive) and `examples/automation_agent.py` (one-shot multi-tool)
- Core Agent with parallel tools, hooks, sessions, MCP attach
- Health-aware MultiLLMRouter (Ollama + any OpenAI-compatible endpoint)
- Ready for community contributions (see CONTRIBUTING.md and ROADMAP.md)

No API key required for local models. Most demos run completely offline.

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
python examples/mvp_chat_automation.py
python examples/chat_agent.py
python examples/automation_agent.py
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit  
License: MIT.  
Python >= 3.10.  
Current version: 0.66.0.  
Built autonomously by Grok.

From source:

```bash
git clone https://github.com/Tryboy869/grok-local-agent-kit.git
cd grok-local-agent-kit
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
grok-agent doctor
python examples/mvp_chat_automation.py
```

With a local model (optional):

```bash
ollama pull llama3.2
grok-agent chat -v --stream --router
python examples/chat_agent.py --verbose
```

## What it is not

Not a hosted product.  
Not an xAI / Grok API client.  
Offline demos work with zero cloud dependency.

Feedback and stars welcome. Next: real GIFs, PyPI publish, community skill packs.
