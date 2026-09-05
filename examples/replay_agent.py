#!/usr/bin/env python3
"""Replay a saved trace without a live LLM.

    python examples/replay_agent.py
    python examples/replay_agent.py --trace .grok/traces/last.json --run
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from grok_local_agent_kit.replay import load_trace, replay_tools, summarize_trace


SAMPLE = [
    {"type": "thought", "text": "Compute 21 * 2 with the calculator tool."},
    {"type": "tool", "name": "calculator", "arguments": {"expression": "21 * 2"}},
    {"type": "final", "text": "42"},
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace", default="")
    parser.add_argument("--run", action="store_true", help="Re-execute tools instead of dry-run")
    args = parser.parse_args()

    if args.trace and Path(args.trace).exists():
        trace = load_trace(args.trace)
        print(f"loaded {args.trace} ({len(trace)} events)")
    else:
        trace = SAMPLE
        print("no trace file — using built-in sample")

    print(summarize_trace(trace))
    results = replay_tools(trace, dry_run=not args.run)
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
