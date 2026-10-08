"""Opt-in ReAct handoff on top of the offline playbook.

Default path uses scripted_react (no daemon). Pass --live to call Agent.run
when Ollama or LM Studio answers the probe.

    python examples/handoff_react_agent.py
    python examples/handoff_react_agent.py --live
"""

from __future__ import annotations

import argparse
from pathlib import Path

from grok_local_agent_kit.playbook import (
    builtin_playbook,
    demo_react,
    format_report,
    probe_providers,
    run_playbook,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Playbook with an executed ReAct handoff")
    parser.add_argument("--live", action="store_true", help="Call the local agent if a provider is up")
    parser.add_argument("--workspace", default=".grok/handoff")
    args = parser.parse_args()
    workspace = Path(args.workspace)
    if args.live:
        report = run_playbook(
            builtin_playbook(),
            workspace,
            probes=probe_providers(timeout=0.4),
            live=True,
        )
        print(format_report(report))
        print(f"react_called={report['react_called']}")
        return
    print(demo_react(workspace))


if __name__ == "__main__":
    main()
