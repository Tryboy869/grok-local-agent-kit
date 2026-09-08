#!/usr/bin/env python3
"""Run the offline golden eval suite (no LLM).

Usage:
  python examples/eval_agent.py
  python examples/eval_agent.py --cases examples/eval_cases.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from grok_local_agent_kit.evalkit import DEFAULT_CASES, format_report, load_cases, run_suite


def main() -> None:
    parser = argparse.ArgumentParser(description="Offline agent eval")
    parser.add_argument("--cases", default=None, help="JSON file of cases")
    args = parser.parse_args()
    if args.cases:
        cases = load_cases(args.cases)
    else:
        bundled = Path(__file__).with_name("eval_cases.json")
        cases = load_cases(bundled) if bundled.exists() else DEFAULT_CASES
    report = run_suite(cases)
    print(format_report(report))
    print(json.dumps({"ok": report["ok"], "passed": report["passed"], "total": report["total"]}))
    raise SystemExit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
