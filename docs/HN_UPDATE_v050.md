# Show HN / Indie Hackers update — v0.50.0

**Title:** Show HN: grok-local-agent-kit – enhanced offline MVP for local AI agents (Ollama / LM Studio, no cloud)

**Body:**

Shipped a polished offline-first core for local AI agents.

New in v0.50.0:

- Improved intent routing (better math expression extraction from natural language)
- Ready-to-run examples that need zero models:
  - `python examples/enhanced_automation_agent.py` — file write, calculator, list_files, search fixture, system info
  - `python examples/enhanced_chat_agent.py --offline` — multi-LLM probes + MVP fallback
- One-command install still works; demos run even if Ollama and LM Studio are down

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
python examples/enhanced_automation_agent.py
python examples/mvp_core_demo.py
```

Once you start a local model:

```bash
python examples/chat_agent.py
# or
python examples/enhanced_chat_agent.py
```

Tools: web search (with HTML fallback), cwd-safe file ops, calculator, MCP echo, system info, and more. Multi-LLM router with circuit breaker.

Repo: https://github.com/Tryboy869/grok-local-agent-kit  
License: MIT. Python >= 3.10.  
No API keys required for local models.

Audit: 2026-10-12. Public stars: (check live). No paid promotion.
