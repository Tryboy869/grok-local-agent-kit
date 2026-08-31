# Show HN: grok-local-agent-kit 0.12 — local agents with real tools, MCP, and loop hooks

I wanted a small Python kit that runs an agent on my laptop against Ollama or LM Studio without wrapping a cloud API.

v0.12 ships:

- ReAct tool loop (files, web, shell, python sandbox, calculator, MCP)
- Multi-LLM fallback router (Ollama → LM Studio)
- JSONL memory as tools the model can call
- JSON skill packs under `.grok/skills/`
- Hook bus that fires *inside* the loop (`before_tool`, `after_tool`, `on_final`)
- MCP over stdio and HTTP
- Tests that do not need a live LLM

```bash
pip install git+https://github.com/Tryboy869/grok-local-agent-kit.git
grok-agent doctor
grok-agent chat -v --stream --router
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit

Happy to hear what you would require before trusting this in a real workflow.
