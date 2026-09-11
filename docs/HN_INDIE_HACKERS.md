# Launch update — v0.24.0 (HN / Indie Hackers)

**One-liner:** Local AI agents that call tools, fail over Ollama ↔ LM Studio, speak MCP — now with drop-in tool plugins (JSON or Python) and JSONL transcripts that never leave your disk.

**What's new since v0.23**

- `./tools` and `~/.grok-agent/tools` are scanned on `get_default_tools()`
- JSON plugins: `kind=template|json` plus optional static `returns`
- Python plugins: `handler()` or `register()`
- `grok-agent plugins list|dirs`
- Transcripts: `append_turn` / `grok-agent transcripts list|show|new`
- Examples: `plugin_agent.py`, `transcript_agent.py`, `examples/tools/workspace_ping.json`
- Tests: `tests/test_v024.py` (no live LLM)

**Install**

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
python examples/plugin_agent.py
python examples/transcript_agent.py
grok-agent plugins list
pytest -q
```

**Ask:** Next blocker for 1.0 — recorded GIFs, PyPI, or a plugin sandbox?

Repo: https://github.com/Tryboy869/grok-local-agent-kit
