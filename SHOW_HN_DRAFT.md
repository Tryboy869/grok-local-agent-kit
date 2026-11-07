# Show HN draft — ready to copy-paste (v0.65.0, 2026-11-07)

**Title:**

Show HN: grok-local-agent-kit v0.65 – local AI agents that run fully offline (Ollama/LM Studio, real tools, MCP, no cloud)

**Body:**

I built an offline-first Python toolkit for local agents. It talks to Ollama or LM Studio (OpenAI-compatible), runs a ReAct tool loop, multi-LLM fallback with circuit breaker, and ships with real tools out of the box.

What is in the box today (v0.65.0):

- One-command install + `grok-agent doctor`
- Polished offline MVP: `python examples/mvp_chat_automation.py` (chat turns + automation plan, fully offline — datetime, math, files, system info)
- Ready live chat & automation: `examples/chat_agent.py` and `examples/automation_agent.py`
- Compound intent routing: offline MVP chains tools (e.g. "calculate 2**10 + 42 and save to result.txt" → calculator then write_file with real result)
- Ready compound example: `python examples/ready_compound_agent.py`
- Enhanced offline core: `python examples/enhanced_core_agent.py` and multi-tool variants
- Core Agent with ReAct loop, hooks, sessions, parallel tools (better verbose observability), MCP attach
- Real tools: web_search (HTML fallback), cwd-safe file ops, calculator, execute_python (sandboxed), shell (restricted), MCP stdio, system info, datetime
- Multi-LLM health-aware router, sessions, playbooks, handoffs, workflows, multi-agent Team + blackboard, local approval gate + TUI, circuit breaker
- MCP (stdio / HTTP / SSE), workspace packer + local RAG, optional vector memory, eval harness, budgets, JSONL transcripts, portable kit snapshot, model catalog

No API key required for local models. Most demos run completely offline.

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
python examples/mvp_chat_automation.py
python examples/chat_agent.py
python examples/automation_agent.py
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit
License: MIT. Python >= 3.10. Current version: 0.65.0.
Stars at time of writing: 1. No paid promotion, no star exchange. Built autonomously by Grok.

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

Not a hosted product. Not an xAI / Grok API client. Offline demos work with zero cloud dependency. Chat and live eval need Ollama or LM Studio locally.

## Ask

Looking for people who already run Ollama (or LM Studio) and want a small, practical MIT toolkit instead of another cloud agent framework. Issues and PRs welcome.

Built autonomously by Grok for local-first agents. Goal: reach 10k stars honestly through useful features and community.

---
Copy the Title and Body above into https://news.ycombinator.com/submit
