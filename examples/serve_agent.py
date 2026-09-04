#!/usr/bin/env python3
"""Local HTTP API demo (no live LLM required for --dry-run)."""

from __future__ import annotations

import json
import sys
import threading
import time
from http.client import HTTPConnection

from grok_local_agent_kit.serve import serve


class FakeAgent:
    def __init__(self) -> None:
        self.last_trace = [{"type": "final", "text": "pong"}]
        self.usage = type("U", (), {"as_dict": staticmethod(lambda: {"prompt_tokens": 1})})()

    def run(self, prompt: str) -> str:
        return f"echo:{prompt}"

    def chat(self, prompt: str) -> str:
        return f"chat:{prompt}"

    def list_registered_tools(self) -> list:
        return ["web_search", "read_file", "plan_add"]

    def close(self) -> None:
        return None


def main() -> None:
    if "--help" in sys.argv:
        print("Usage: python examples/serve_agent.py [--dry-run]")
        return
    httpd = serve("127.0.0.1", 0, agent_factory=FakeAgent)
    host, port = httpd.server_address
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.05)
    conn = HTTPConnection("127.0.0.1", port, timeout=3)
    conn.request("GET", "/health")
    health = json.loads(conn.getresponse().read().decode())
    conn.request("POST", "/v1/chat", body=json.dumps({"prompt": "hello local"}), headers={"Content-Type": "application/json"})
    chat = json.loads(conn.getresponse().read().decode())
    conn.close()
    httpd.shutdown()
    print("health:", health)
    print("chat:", chat)
    assert health.get("ok") is True
    assert chat.get("text") == "echo:hello local"
    print("serve_agent dry-run ok")


if __name__ == "__main__":
    main()
