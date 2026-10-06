# Show HN draft — copy-paste (2026-10-06)

Title:

Show HN: grok-local-agent-kit – local AI agents on Ollama/LM Studio (MCP, no cloud)

Body:

I built an offline-first Python toolkit for local agents. It talks to Ollama or LM Studio (OpenAI-compatible), runs a ReAct tool loop, and can fall back across models with a circuit breaker that survives restart.

What is in the box today (v0.44):

- CLI: `grok-agent doctor`, chat, tools, model catalog, health-aware router
- MCP over stdio / HTTP / SSE
- Workspace packer + local file RAG (no network)
- Multi-agent team, shared blackboard, handoff queue
- Local approval gate (denied tools never run) and a scriptable TUI
- JSON workflows and a file-backed job ledger that runs them offline
- Optional SQLite memory, eval harness, budgets, JSONL transcripts

No API key is required for local models. Demos that do not chat (`doctor`, `tools demo`, `models demo`, `workflow demo`) run without a model.

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
grok-agent tools demo
grok-agent workflow demo
```

From source:

```bash
git clone https://github.com/Tryboy869/grok-local-agent-kit.git
cd grok-local-agent-kit
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
```

Chat (optional):

```bash
ollama pull llama3.2
grok-agent chat -v --stream --router
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit
License: MIT

I am looking for feedback on the tool API and the offline workflow/job runner. Stars are welcome, but issues and “this broke on my box” reports are more useful.
