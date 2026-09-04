#!/usr/bin/env python3
"""Planner + scheduler demo (no live LLM)."""

from __future__ import annotations

from pathlib import Path

from grok_local_agent_kit.planner import plan_add, plan_clear, plan_done, plan_list
from grok_local_agent_kit.scheduler import Scheduler


def main() -> None:
    plan_clear(done_only=False)
    print(plan_add("Ship v0.16 local HTTP API"))
    print(plan_add("Write HN draft", notes="Indie Hackers too"))
    print(plan_list())
    print(plan_done(1))
    print(plan_list("open"))

    hits = []

    def tick() -> str:
        hits.append("ok")
        return f"ticks={len(hits)}"

    sched = Scheduler()
    sched.add("heartbeat", 0.2, tick)
    sched.loop(ticks=3, sleep_s=0.05)
    print(sched.describe())
    print("planner_agent ok, hits=", len(hits))
    print("plan file:", Path(".grok/plan.json").resolve())


if __name__ == "__main__":
    main()
