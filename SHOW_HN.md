# Show HN: grok-local-agent-kit 0.19 — watch files, parse JSON, run recipes offline

I keep shipping a small Python kit for **offline-first agents** on Ollama / LM Studio.

v0.19 adds the unglamorous glue that actually gets used:

- `grok-agent watch` polls a folder and prints created/modified/deleted files
- `extract_json()` pulls the first object out of messy fenced model text
- `grok-agent recipe workspace.toml` runs built-in tools with **no LLM at all**

Still in the box: cancel hung shells, bearer token on `grok-agent serve`, MCP stdio/HTTP/SSE, router, planner, guardrails.

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
python examples/watch_agent.py
python examples/recipe_agent.py
pytest -q
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit
