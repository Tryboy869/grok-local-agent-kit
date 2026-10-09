"""Run the offline session pack (chat + automation + search + MCP).

No Ollama or LM Studio required.

    python examples/session_pack.py
"""

from pathlib import Path

from grok_local_agent_kit.pack import demo_pack

if __name__ == "__main__":
    root = Path(".grok/pack-example")
    print(demo_pack(root))
    print(f"brief: {(root / 'SESSION.md').resolve()}")
