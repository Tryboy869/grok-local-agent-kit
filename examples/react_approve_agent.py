#!/usr/bin/env python3
"""Offline demo: ReAct-style tool batch gated by ApprovalGate (no live LLM)."""

from grok_local_agent_kit.approvals import ApprovalGate, save_approvals
from grok_local_agent_kit.react_gate import gated_execute
from grok_local_agent_kit.tools import execute_tool, get_default_tools


def main() -> None:
    _, funcs = get_default_tools()
    gate = ApprovalGate(
        allow=["calculator", "list_files", "get_system_info"],
        deny=["run_shell", "shell", "delete_file"],
        default="pending",
    )

    plan = [
        ("calculator", {"expression": "21*2"}),
        ("list_files", {"path": "."}),
        ("run_shell", {"command": "rm -rf /"}),
        ("web_search", {"query": "local-first agents"}),
    ]
    print("ReAct batch (simulated, no LLM)")
    for name, args in plan:
        result = gated_execute(gate, name, execute_tool, name, args, funcs)
        preview = result.replace("\n", " ")[:160]
        print(f"  {name}: {preview}")
    print("--- gate ---")
    print(gate.dump())
    save_approvals(gate, "approvals.json")
    print("saved approvals.json")


if __name__ == "__main__":
    main()
