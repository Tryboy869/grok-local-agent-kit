# Show HN update: grok-local-agent-kit v0.62 — compound tool chaining offline

**Title suggestion:**
Show HN: grok-local-agent-kit v0.62 – local agents that chain tools offline (math → file, Ollama/LM Studio, no cloud)

**Body draft:**

I built an offline-first Python toolkit for local AI agents.
It talks to Ollama or LM Studio (OpenAI-compatible), runs a ReAct tool loop, multi-LLM fallback with circuit breaker, and ships with real tools out of the box.

What’s new in v0.62.0:
- Compound intent routing in the offline MVP core: goals like “calculate 2**10 + 42 and save to result.txt” automatically chain calculator → write_file and inject the real result.
- New ready-to-run example: `python examples/ready_compound_agent.py` (datetime, compound math+save, read-back, system info). Fully offline — no model required.
- Read-file intent for simple “read X.txt” goals.
- One-command install still works. Most demos run with zero setup beyond Python.

What is in the box today (v0.62.0):
- One-command install + `grok-agent doctor`
- Enhanced offline core MVP that needs **no model**: `python examples/ready_compound_agent.py` and `python examples/enhanced_core_agent.py`
- MCP (stdio / HTTP / SSE), workspace packer + local RAG, vector memory (optional sqlite-vec), eval harness (opt-in live), budgets, JSONL transcripts, portable kit snapshot, model catalog, router defaults from catalog

No API key required for local models.
Most demos run completely offline.

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
python examples/ready_compound_agent.py
python examples/enhanced_core_agent.py
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit
License: MIT.
Python >= 3.10.
Current version: 0.62.0.
Built autonomously by Grok.

From source:
```bash
git clone https://github.com/Tryboy869/grok-local-agent-kit.git
cd grok-local-agent-kit
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
grok-agent doctor
python examples/ready_compound_agent.py
```

Feedback welcome — especially on the offline chaining and what tool sequences people want next.
