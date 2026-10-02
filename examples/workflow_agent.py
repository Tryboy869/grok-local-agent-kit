"""Ready-to-run workflow agent. No Ollama / LM Studio required.

    python examples/workflow_agent.py
    python examples/workflow_agent.py --workspace ./tmp-workspace
"""

from __future__ import annotations

import argparse
from pathlib import Path

from grok_local_agent_kit.workflow import demo_workflow, load_workflow, run_workflow


def main() -> None:
    parser = argparse.ArgumentParser(description="Offline workflow agent (files, search fixture, MCP echo)")
    parser.add_argument("--workspace", default=None, help="Workspace directory (default: temp)")
    parser.add_argument("--spec", default=None, help="Workflow JSON (default: built-in demo)")
    args = parser.parse_args()
    if args.spec:
        root = Path(args.workspace or ".").resolve()
        root.mkdir(parents=True, exist_ok=True)
        result = run_workflow(load_workflow(args.spec), root)
        print(f"ok={result['ok']} steps={result['steps']}")
        for item in result["trace"]:
            print(f"{item['step']}. {item['tool']} ok={item['ok']}")
            print(item["output"][:400])
        raise SystemExit(0 if result["ok"] else 1)
    workspace = Path(args.workspace).resolve() if args.workspace else None
    if workspace:
        workspace.mkdir(parents=True, exist_ok=True)
    print(demo_workflow(workspace))


if __name__ == "__main__":
    main()
