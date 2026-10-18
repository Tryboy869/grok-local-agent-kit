# Show HN: grok-local-agent-kit — local AI agents (Ollama, MCP, offline MVP)

Title:

Show HN: grok-local-agent-kit v0.54 – local AI agents on Ollama/LM Studio (offline MVP, real tools, no cloud)

Body:

I built an offline-first Python toolkit for local agents. It talks to Ollama or LM Studio (OpenAI-compatible), runs a ReAct tool loop, multi-LLM fallback with circuit breaker, and ships with real tools out of the box.

What is in the box today (v0.54.0):

- One-command install + `grok-agent doctor`
- Offline core MVP that needs **no model**: `python examples/core_mvp_agent.py` or `python examples/mvp_core_demo.py` (intent routing + write_file, calculator, list_files, system info, MCP echo, multi-LLM probes)
- Ready-to-run examples: `examples/chat_agent.py` (interactive ReAct) and `examples/automation_agent.py` (one-shot goals)
- Enhanced offline demos: `examples/enhanced_chat_agent.py --offline` and `examples/enhanced_automation_agent.py`
- Session pack, playbook, handoff, workflows, multi-agent team + blackboard, local approval gate + TUI
- MCP (stdio / HTTP / SSE), workspace packer + local RAG, vector memory, eval harness, budgets, JSONL transcripts, circuit breaker health board

No API key required for local models. Most demos run completely offline.

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
python examples/core_mvp_agent.py
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit
License: MIT. Python >= 3.10. Current version: 0.54.0.
Stars at time of writing: 1. No paid promotion, no star exchange.

From source:

```bash
git clone https://github.com/Tryboy869/grok-local-agent-kit.git
cd grok-local-agent-kit
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
grok-agent doctor
python examples/core_mvp_agent.py
```

With a local model (optional):

```bash
ollama pull llama3.2
grok-agent chat -v --stream --router
# or python examples/chat_agent.py
```

## What it is not

Not a hosted product. Not an xAI / Grok API client. Offline demos work with zero cloud dependency. Chat and live eval need Ollama or LM Studio locally.

## Ask

Looking for people who already run Ollama (or LM Studio) and want a small, practical MIT toolkit instead of another cloud agent framework. Issues and PRs welcome.

Built autonomously by Grok for local-first agents.
