# Launch update — v0.25.0 (HN / Indie Hackers)

**One-liner:** Local AI agents that call tools, fail over Ollama ↔ LM Studio, speak MCP — now with a plugin sandbox so a random `tools/*.py` in your workspace cannot execute on import.

**What's new since v0.24**

- Python plugins require `GROK_AGENT_ALLOW_PY_PLUGINS=1` or `GROK_AGENT_PY_PLUGIN_ALLOWLIST`
- JSON plugins still load (templates / static returns, no code exec)
- `discover_plugins(allow_py=True)` for explicit loads in your own scripts
- `grok-agent sandbox status|skipped`
- Example: `examples/sandbox_plugin_agent.py`
- Tests: `tests/test_v025.py` (no live LLM)

**Install**

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
python examples/sandbox_plugin_agent.py
grok-agent sandbox status
pytest -q
```

**Ask:** Next blocker for 1.0 — recorded GIFs, PyPI, or subprocess-isolated plugins?

Repo: https://github.com/Tryboy869/grok-local-agent-kit
