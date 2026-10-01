#!/usr/bin/env python3
"""Automation agent: one scripted tool call writes a workspace note.

Ready to run with no model server. The live path is examples/automation_agent.py.
"""

from pathlib import Path
import tempfile

from grok_local_agent_kit.offline import run_offline


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="auto-") as raw:
        root = Path(raw)
        text = run_offline("automation: write a note about the run", root)
        note = root / "offline-note.txt"
        print(text)
        print(f"note_exists={note.is_file()}")


if __name__ == "__main__":
    main()
