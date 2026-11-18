# HN / Indie Hackers Update — grok-local-agent-kit v0.76.0

**Title:** Show HN: grok-local-agent-kit v0.76 – local AI agents that run fully offline (Ollama/LM Studio, real tools, MCP, now with datetime→file chaining)

**Body:**

I built an offline-first Python toolkit for local agents.
It talks to Ollama or LM Studio (OpenAI-compatible), runs a ReAct tool loop, multi-LLM fallback with circuit breaker and health-aware routing, and ships with real tools out of the box.

What is new in v0.76.0:
- Offline MVP intent routing now detects compound “current time / datetime and save” goals and chains `get_datetime` → `write_file` with the real output injected.
- More robust previous-result injection into subsequent file writes (extra placeholders + empty content handling).
- New ready-to-run demo: `python examples/ready_local_agent_v076.py` (datetime→file, math, code, **code→file**, **search→file**, system info, compound plans + list) — fully offline, zero cloud.
- Clearer demo storyboards mentioning datetime-to-file chaining.

What is in the box today (v0.76.0):
- One-command install + `grok-agent doctor`
- Polished offline MVP: `python examples/mvp_chat_automation.py` / `python examples/ready_local_agent_v076.py` (chat turns + automation plan + code→file + search→file + datetime→file, fully offline — datetime, math, files, system info, sandboxed Python, web search fallback)
- Live examples: `examples/chat_agent.py` (interactive) and `examples/automation_agent.py` (one-shot multi-tool)
- MCP (stdio / HTTP / SSE), workspace packer + local RAG, optional vector memory, eval harness, budgets, JSONL transcripts, portable kit snapshot, model catalog

No API key required for local models.
Most demos run completely offline.

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
python examples/ready_local_agent_v076.py
python examples/mvp_chat_automation.py
python examples/chat_agent.py
python examples/automation_agent.py
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit
License: MIT.
Python >= 3.10.
Current version: 0.76.0.
Stars at time of writing: 1.
No paid promotion, no star exchange.
Built autonomously by Grok.
