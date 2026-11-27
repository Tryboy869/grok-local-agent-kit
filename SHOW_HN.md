# Show HN: grok-local-agent-kit — offline-first local AI agents (Ollama, MCP, ReAct)

**Title:**

Show HN: grok-local-agent-kit v0.85 – local AI agents that run fully offline (Ollama/LM Studio, real tools, MCP, no cloud)

**Body:**

I built an offline-first Python toolkit for local agents.
It talks to Ollama or LM Studio (OpenAI-compatible), runs a ReAct tool loop, multi-LLM fallback with circuit breaker and health-aware routing, and ships with real tools out of the box.

What is in the box today (v0.85.0):

- One-command install + `grok-agent doctor`
- Real offline MVP (`route_intent` + `run_mvp`) with result injection for compound plans (math/code/shell/list/search_files/http/system/datetime → file, copy, mkdir, move)
- MCP (stdio / HTTP / SSE), workspace packer + local RAG, optional vector memory, eval harness, budgets, JSONL transcripts, portable kit snapshot, model catalog
- Real tools: web_search, http_get, cwd-safe file ops (incl. move/copy/mkdir), calculator, sandboxed execute_python, restricted shell, system info, datetime, search_files, list_files

No API key required for local models.
Most demos run completely offline (including compound plans with result injection).

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
python examples/mvp_chat_automation.py
python examples/ready_local_agent_v085.py
python examples/chat_agent.py
python examples/automation_agent.py
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit
License: MIT.

Python >= 3.10.
Current version: 0.85.0.
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
python examples/ready_local_agent_v085.py
```
