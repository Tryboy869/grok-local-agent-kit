#!/usr/bin/env python3
"""Show MultiLLMRouter skipping an open HealthBoard breaker.

No live model is contacted. Fake clients stand in for Ollama / LM Studio.
"""

from __future__ import annotations

from grok_local_agent_kit.router import demo_routed_health


def main() -> None:
    print(demo_routed_health())


if __name__ == "__main__":
    main()
