#!/usr/bin/env python3
"""Persist MultiLLMRouter HealthBoard decisions to health.json.

No live model is contacted. Fake clients stand in for Ollama / LM Studio.
"""

from __future__ import annotations

from grok_local_agent_kit.router import demo_persisted_route


def main() -> None:
    print(demo_persisted_route("health.json"))


if __name__ == "__main__":
    main()
