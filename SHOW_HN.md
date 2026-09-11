# Show HN: grok-local-agent-kit v0.23 — local agents + optional sqlite-vec

Offline-first Python agents that talk to Ollama or LM Studio, call real tools, and speak MCP.

v0.23 adds a vector backend switch:

- `GROK_VEC_BACKEND=auto|hash|sqlite-vec`
- `grok-agent vec info|search|remember`
- Hash cosine fallback so nothing extra is required
- `pip install -e ".[vec]"` when you want sqlite-vec

```
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
python examples/sqlite_vec_agent.py
grok-agent vec info
pytest -q
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit
