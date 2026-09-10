#!/usr/bin/env python3
"""Demo: retry a flaky callable with backoff (no live LLM required)."""

from grok_local_agent_kit.retry import retry_call


class Boom(RuntimeError):
    pass


def main() -> None:
    state = {"n": 0}

    def flaky() -> str:
        state["n"] += 1
        if state["n"] < 3:
            raise Boom(f"fail #{state['n']}")
        return "ok"

    result = retry_call(flaky, attempts=4, base_delay=0.0, retry_on=(Boom,), sleep=lambda _: None)
    print("result:", result, "tries:", state["n"])


if __name__ == "__main__":
    main()
