# HN / Indie Hackers Update — grok-local-agent-kit v0.60.0

**Title idea:** Show HN: grok-local-agent-kit v0.60 — offline-first local AI agents (Ollama/LM Studio, real tools, MCP)

**Body:**

I shipped v0.60 of an offline-first Python toolkit for local AI agents.

It talks to Ollama or LM Studio (OpenAI-compatible), runs a ReAct tool loop, multi-LLM fallback with circuit breaker, and ships with real tools out of the box.

**What's new in v0.60:**
- Refined math expression extraction in the offline MVP core (cleaner prefixes, better operator handling).
- Continued polish on the ready-to-run offline examples (core, chat, automation, multi-tool).
- Docs, ROADMAP, and this update synced.

**What is in the box today:**
- One-command install + `grok-agent doctor`
- Enhanced offline core MVP that needs **no model**: `python examples/enhanced_core_agent.py` and `python examples/ready_multi_tool_agent.py` (datetime, math, files, search fixture, system info, MCP echo, multi-LLM probes)
- Ready chat & automation agents
- MCP (stdio / HTTP / SSE), workspace packer + local RAG, vector memory (optional sqlite-vec), eval harness, budgets, JSONL transcripts, circuit breaker health board, portable kit snapshot, model catalog
- And much more (see README)

No API key required for local models.
Most demos run completely offline.

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
python examples/enhanced_core_agent.py
python examples/ready_multi_tool_agent.py
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit
License: MIT.
Python >= 3.10.
Current version: 0.60.0.

From source:
```bash
git clone https://github.com/Tryboy869/grok-local-agent-kit.git
cd grok-local-agent-kit
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
grok-agent doctor
python examples/enhanced_core_agent.py
```

Feedback welcome — especially on the offline routing and tool examples.
