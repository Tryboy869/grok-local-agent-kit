#!/usr/bin/env python3
"""Watch a folder for changes (no live LLM required)."""

from __future__ import annotations

import tempfile
from pathlib import Path

from grok_local_agent_kit.watch import diff, format_events, snapshot, watch


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "notes.txt").write_text("hello\n", encoding="utf-8")
        before = snapshot(root)
        (root / "notes.txt").write_text("hello world\n", encoding="utf-8")
        (root / "new.md").write_text("# new\n", encoding="utf-8")
        after = snapshot(root)
        print(format_events(diff(before, after)))
        print("--- poll once ---")
        (root / "new.md").write_text("# updated\n", encoding="utf-8")
        print(format_events(watch(root, interval=0.05, once=True, max_seconds=2.0)))


if __name__ == "__main__":
    main()
