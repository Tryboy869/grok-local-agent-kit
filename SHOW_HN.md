# Show HN: grok-local-agent-kit — offline-first local AI agents (Ollama, MCP, ReAct)

**Title:**

Show HN: grok-local-agent-kit v0.68 – local AI agents that run fully offline (Ollama/LM Studio, real tools, MCP, no cloud)

**Body:**

I built an offline-first Python toolkit for local agents.
It talks to Ollama or LM Studio (OpenAI-compatible), runs a ReAct tool loop, multi-LLM fallback with circuit breaker and health-aware routing, and ships with real tools out of the box.

What is in the box today (v0.68.0):

- One-command install + `grok-agent doctor`
- Polished offline MVP: `python examples/mvp_chat_automation.py` (chat turns + automation plan, fully offline — datetime, math, files, system info)
- Live examples: `examples/chat_agent.py` (interactive) and `examples/automation_agent.py` (one-shot multi-tool)
- Enhanced multi-LLM router with clearer fallback messaging
- Refined offline compound intent routing (math → file, search + note)
- Multi-LLM health-aware router, sessions, playbooks, handoffs, workflows, multi-agent Team + blackboard, local approval gate + TUI, circuit breaker
- MCP (stdio / HTTP / SSE), workspace packer + local RAG, optional vector memory, eval harness, budgets, JSONL transcripts, portable kit snapshot, model catalog

No API key required for local models.
Most demos run completely offline.

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
Current version: 0.68.0.
Stars at time of writing: 1.
No paid promotion, no star exchange.
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
