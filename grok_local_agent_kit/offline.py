"""Offline scripted LLM that drives the real Agent tool loop.

No Ollama, LM Studio, or network. Used by `grok-agent offline demo` and the
ready-to-run examples so the ReAct path is testable in CI.
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional


class ScriptedLLM:
    """Minimal LLMClient stand-in: one tool call, then a final answer."""

    def __init__(self, note_name: str = "offline-note.txt", note_body: str = "written by the offline agent\n"):
        self.note_name = note_name
        self.note_body = note_body
        self.calls = 0

    def chat(self, messages: List[Dict[str, Any]], tools: Optional[list] = None, stream: bool = False) -> Dict[str, Any]:
        self.calls += 1
        if messages and messages[-1].get("role") == "tool":
            body = messages[-1].get("content") or ""
            return {
                "content": "Done (offline). Last tool result:\n" + str(body)[:800],
                "tool_calls": None,
                "raw": None,
            }
        user = ""
        for msg in messages:
            if msg.get("role") == "user":
                user = str(msg.get("content") or "")
        low = user.lower()
        if any(word in low for word in ("write", "note", "save", "automation")):
            return {
                "content": "Writing a workspace note.",
                "tool_calls": [
                    {
                        "id": "off_1",
                        "name": "write_file",
                        "arguments": {"path": self.note_name, "content": self.note_body},
                    }
                ],
                "raw": None,
            }
        return {
            "content": "Listing the workspace.",
            "tool_calls": [
                {
                    "id": "off_1",
                    "name": "list_files",
                    "arguments": {"path": ".", "pattern": "*"},
                }
            ],
            "raw": None,
        }

    def close(self) -> None:
        return None


def run_offline(prompt: str, workspace: Path, note_name: str = "offline-note.txt") -> str:
    """Run Agent.run against ScriptedLLM inside `workspace`."""
    from .agent import Agent

    workspace.mkdir(parents=True, exist_ok=True)
    llm = ScriptedLLM(note_name=note_name)
    agent = Agent(llm=llm, verbose=False, parallel_tools=False)
    cwd = Path.cwd()
    try:
        import os

        os.chdir(workspace)
        return agent.run(prompt)
    finally:
        os.chdir(cwd)
        agent.close()


def demo_offline() -> str:
    """Chat-style list plus automation-style write. No daemon."""
    lines = ["offline-agent", "provider=scripted", "backends=none"]
    with tempfile.TemporaryDirectory(prefix="glak-offline-") as raw:
        root = Path(raw)
        (root / "seed.txt").write_text("seed\n", encoding="utf-8")
        chat = run_offline("list files in the workspace", root)
        lines.append("chat:")
        lines.append(chat.strip()[:500])
        auto = run_offline("automation: write a note", root, note_name="offline-note.txt")
        note = root / "offline-note.txt"
        lines.append("automation:")
        lines.append(auto.strip()[:500])
        lines.append(f"wrote={note.is_file()} bytes={note.stat().st_size if note.is_file() else 0}")
    return "\n".join(lines)
