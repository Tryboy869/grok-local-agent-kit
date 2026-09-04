#!/usr/bin/env python3
"""Show tool allow/deny + timeout without a live LLM."""

from __future__ import annotations

import time

from grok_local_agent_kit.guardrails import ToolGuard


def main() -> None:
    guard = ToolGuard(allow={"calculator", "list_files"}, deny={"run_shell"}, timeout_s=0.2)
    print(guard.check("run_shell"))
    print(guard.check("web_search"))
    print(guard.check("calculator"))

    def slow() -> str:
        time.sleep(1)
        return "done"

    print(guard.run("calculator", slow, {}))
    print("guardrails_agent ok")


if __name__ == "__main__":
    main()
