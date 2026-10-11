# Show HN: grok-local-agent-kit — local AI agents (Ollama, MCP, offline MVP)

Title:

Show HN: grok-local-agent-kit – local AI agents on Ollama/LM Studio (offline MVP, no cloud)

Body:

I built an offline-first Python toolkit for local agents. It talks to Ollama or LM Studio (OpenAI-compatible), runs a ReAct tool loop, and can fall back across models with a circuit breaker that survives restart.

What is in the box today (v0.49.0):

- `python examples/mvp_core_demo.py` (or `grok-agent mvp`) runs offline intent routing + real tools (write_file, calculator, list_files, system info, MCP echo) + multi-LLM probes — no model required
- `grok-agent pack demo` batches chat math, file write, search fixture, and MCP echo, then writes SESSION.md
- `grok-agent playbook demo` and `grok-agent handoff demo` still run offline; live handoff is opt-in
- CLI: `grok-agent doctor`, chat, tools, model catalog, health-aware router, snapshot, team, board, roster, approve TUI
- MCP over stdio / HTTP / SSE
- Workspace packer + local file RAG (no network)
- Multi-agent team, shared blackboard, handoff queue
- Local approval gate (denied tools never run) and a scriptable TUI
- JSON workflows and a file-backed job ledger that runs them offline
- Optional SQLite memory, eval harness, budgets, JSONL transcripts, circuit breaker health board

No API key is required for local models. Demos that do not chat (`doctor`, `pack demo`, `playbook demo`, `mvp`, `tools demo`, `mvp_core_demo.py`) run without a model.

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
grok-agent pack demo
python examples/mvp_core_demo.py
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit
License: MIT. Python >= 3.10. Current package version: 0.49.0.
Audit: 2026-10-11. Public stars at audit time: 1. Forks: 0. No paid promotion, no star exchange.

From source:

```bash
git clone https://github.com/Tryboy869/grok-local-agent-kit.git
cd grok-local-agent-kit
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
grok-agent doctor
```

Chat needs a local model:

```bash
ollama pull llama3.2
grok-agent chat -v --stream --router
```

## What it is not

Not a hosted agent product. Not a Grok / xAI API client. Demos that do not need a model run offline; chat and live eval need Ollama or LM Studio on the machine. Star count is not a feature.

## Ask

Looking for people who already run Ollama locally and want a small MIT toolkit rather than another cloud agent framework. Issues and PRs welcome: https://github.com/Tryboy869/grok-local-agent-kit/issues
