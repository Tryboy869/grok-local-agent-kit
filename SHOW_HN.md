# Show HN: grok-local-agent-kit — local AI agents (Ollama, MCP, offline workflows)

Local-first Python toolkit for AI agents. Talks to Ollama or LM Studio, runs a ReAct tool loop, packs a workspace for local RAG, and can orchestrate a small multi-agent team — all without a cloud API key.

Repo: https://github.com/Tryboy869/grok-local-agent-kit
License: MIT. Python >= 3.10. Current package version: 0.46.0.
Audit: 2026-10-09. Public stars at audit time: 1. Forks: 0. No paid promotion, no star exchange.

## What it does

- Multi-LLM router (Ollama + OpenAI-compatible / LM Studio) with a circuit breaker that skips open backends on pick / probe / chat
- Health decisions persist to `health.json` and survive process restart
- ReAct tool loop, drop-in JSON tools, opt-in sandboxed Python plugins
- MCP over stdio / HTTP / SSE
- SQLite session memory, optional sqlite-vec
- Workspace packer + local file RAG (no network)
- Web search with HTML fallback when you opt in
- Multi-agent Team, shared blackboard, roster, task handoff queue
- File-backed approval gate and a small approval TUI
- Offline workflow runner, file-backed job ledger, and a playbook runner (chat + automation + search + MCP in one JSON file)
- Offline eval harness plus an opt-in live-model profile
- Local HTTP API, JSONL transcripts, budgets, telemetry, portable kit snapshot

## Try it

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
grok-agent tools demo
grok-agent models demo
grok-agent route catalog
grok-agent snapshot demo
grok-agent team demo
grok-agent playbook demo
grok-agent eval-demo
grok-agent health demo
grok-agent route demo
grok-agent route persist
grok-agent workflow demo
grok-agent approve tui --seed --script A003=approved,A004=denied
```

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
