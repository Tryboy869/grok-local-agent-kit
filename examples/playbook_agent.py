#!/usr/bin/env python3
"""Ready-to-run playbook: chat note, math, system, search, MCP echo.

No model required. If you pass probes with status=up, the report records a
ReAct handoff descriptor and still does not call the model.

Usage:
  python examples/playbook_agent.py
  python examples/playbook_agent.py --playbook examples/playbooks/local_mvp.json
"""

from __future__ import annotations

import argparse
from pathlib import Path

from grok_local_agent_kit import __version__
from grok_local_agent_kit.playbook import format_report, load_playbook, run_playbook
from grok_local_agent_kit.mvp import probe_providers


def main() -> None:
    parser = argparse.ArgumentParser(description="Local playbook agent")
    parser.add_argument("--playbook", default="examples/playbooks/local_mvp.json")
    parser.add_argument("--workspace", default=".grok/playbook")
    args = parser.parse_args()
    print(f"Playbook agent v{__version__}")
    probes = probe_providers(timeout=0.2)
    for name, row in probes.items():
        print(f"  provider {name}: {row['status']}")
    report = run_playbook(load_playbook(Path(args.playbook)), Path(args.workspace), probes=probes)
    print(format_report(report))
    print(f"report: {(Path(args.workspace) / 'playbook-report.json').resolve()}")


if __name__ == "__main__":
    main()
