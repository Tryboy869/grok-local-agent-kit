# Show HN: grok-local-agent-kit v0.25 — local agents + plugin sandbox

Offline-first Python agents that talk to Ollama or LM Studio, call real tools, and speak MCP.

v0.25 adds a plugin sandbox:

- JSON tools in `./tools` still load automatically (data only)
- Python `.py` plugins are **not imported** unless you set `GROK_AGENT_ALLOW_PY_PLUGINS=1` or an allowlist
- `grok-agent sandbox status|skipped`

```
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
python examples/sandbox_plugin_agent.py
grok-agent sandbox status
pytest -q
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit
