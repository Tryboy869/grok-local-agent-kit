#!/usr/bin/env python3
"""Opt-in live-model eval profile.

Default: deterministic stub (no LLM).
Live: GROK_LIVE_EVAL=1 python examples/live_eval_agent.py --live
"""

from __future__ import annotations

import argparse
import json

from grok_local_agent_kit.live_eval import (
    DEFAULT_PROFILE,
    format_live_report,
    load_profile,
    run_profile,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Live-eval profile (stub by default)")
    parser.add_argument("--profile", default="", help="JSON profile path")
    parser.add_argument(
        "--live",
        action="store_true",
        help="Use a real LLM (also set GROK_LIVE_EVAL=1)",
    )
    args = parser.parse_args()
    profile = load_profile(args.profile) if args.profile else DEFAULT_PROFILE
    report = run_profile(profile, live=args.live)
    print(format_live_report(report))
    print(json.dumps({"ok": report["ok"], "backend": report["backend"], "passed": report["passed"]}))
    raise SystemExit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
