# Show HN: grok-local-agent-kit v0.24 — local agents + drop-in plugins

Offline-first Python agents that talk to Ollama or LM Studio, call real tools, and speak MCP.

v0.24 adds:

- Drop-in tools from `./tools` or `~/.grok-agent/tools` (JSON or Python)
- Local JSONL transcripts (`grok-agent transcripts`)
- `grok-agent plugins list`

```
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
python examples/plugin_agent.py
grok-agent plugins list
pytest -q
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit
