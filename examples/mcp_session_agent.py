#!/usr/bin/env python3
"""Demonstrate MCP Streamable HTTP session ids + request cancel (no network)."""

from __future__ import annotations

from grok_local_agent_kit.mcp_session import get_registry, reset_registry, run_cancellable


def main() -> None:
    reset_registry()
    reg = get_registry()
    sess = reg.open(metadata={"server": "demo"})
    print("session", sess.session_id)
    print("headers", sess.header())

    def work() -> dict:
        return {"result": "pong"}

    print("rpc", run_cancellable(sess.session_id, "1", "ping", work))
    reg.begin_request(sess.session_id, "2", "slow")
    print("cancelled", reg.cancel_request(sess.session_id, "2"))
    print(
        "after cancel",
        run_cancellable(sess.session_id, "2", "slow", work),
    )
    print("sessions", reg.list_sessions())


if __name__ == "__main__":
    main()
