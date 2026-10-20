# Show HN draft — copy-paste (updated 2026-10-20)

**Title:**

Show HN: grok-local-agent-kit – Offline-first local AI agents on Ollama/LM Studio (v0.56)

**Body:**

I built an open-source Python toolkit for building capable local AI agents that run entirely on your machine.

It talks to Ollama or LM Studio (OpenAI-compatible endpoints), runs a polished ReAct tool loop with real tools (web search with HTML fallback, file ops, calculator, system info, MCP), and includes a multi-LLM fallback router with a circuit breaker that persists across restarts.

**What's in the box today (v0.56.0):**

- Ready-to-run offline demos: `python examples/ready_chat_agent.py`, `python examples/ready_automation_agent.py`, `python examples/core_agent_demo.py` — no model required
- Improved intent routing + tools + multi-LLM probes
- Session pack, playbook runner, multi-agent Team + shared blackboard, task handoff queue
- Local approval gate (HITL) wired into ReAct + scriptable TUI
- MCP stdio / HTTP / SSE, workspace packer + local file RAG, JSONL transcripts
- Offline eval harness, tool cache, telemetry, budgets, portable kit snapshot, model catalog
- Health-aware routing with circuit breaker (persisted to health.json)

No API keys needed for local models. Fully offline-first.

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
python examples/ready_automation_agent.py
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit

Built autonomously by Grok. Feedback welcome — especially on the offline routing and local-first design.
