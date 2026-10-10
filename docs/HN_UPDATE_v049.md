# Show HN / Indie Hackers update — v0.49.0

**Title:** Show HN: grok-local-agent-kit – polished offline MVP for local AI agents (Ollama / LM Studio)

**Body:**

I shipped a ready-to-run core demo for the local agent toolkit.

`python examples/mvp_core_demo.py` (after `pip install -e .`) runs:

- Offline intent routing (files, math, system, search, MCP)
- Real tool calls from the shared registry (write_file, calculator, list_files, get_system_info, mcp_echo)
- Multi-LLM provider probes for Ollama (:11434) and LM Studio (:1234/v1) — never fails if they are down

No model required for the MVP. Once you start Ollama or LM Studio:

```
python examples/chat_agent.py
python examples/automation_agent.py
```

One-command install still works:

```
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
python examples/mvp_core_demo.py
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit  
MIT. Python >= 3.10. Offline-first.

Feedback welcome on routing, tools, or MCP.
