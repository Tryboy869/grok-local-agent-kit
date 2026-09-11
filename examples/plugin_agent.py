"""Load a JSON plugin from a temp tools/ dir and call it without an LLM."""

from pathlib import Path
from tempfile import TemporaryDirectory

from grok_local_agent_kit.plugins import apply_plugins
from grok_local_agent_kit.tools import execute_tool, get_default_tools


def main() -> None:
    with TemporaryDirectory() as tmp:
        tools_dir = Path(tmp) / "tools"
        tools_dir.mkdir()
        (tools_dir / "shout.json").write_text(
            '{"name":"shout","description":"uppercase","kind":"template","template":"{text}!","parameters":{"type":"object","properties":{"text":{"type":"string"}}}}',
            encoding="utf-8",
        )
        specs, funcs = get_default_tools()
        specs, funcs = apply_plugins(specs, funcs, extra_dirs=[tools_dir])
        print("plugin tools:", [s["function"]["name"] for s in specs if s["function"]["name"] == "shout"])
        print(execute_tool("shout", {"text": "local agents"}, funcs))


if __name__ == "__main__":
    main()
