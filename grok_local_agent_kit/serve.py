"""Local HTTP API for the agent (stdlib only). Bind 127.0.0.1 by default."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Optional
from urllib.parse import urlparse


def make_handler(agent_factory):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt: str, *args: Any) -> None:
            return

        def _json(self, code: int, payload: dict) -> None:
            raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def do_GET(self) -> None:
            path = urlparse(self.path).path
            if path in {"/", "/health", "/v1/health"}:
                self._json(200, {"ok": True, "service": "grok-local-agent-kit"})
                return
            if path == "/v1/tools":
                agent = agent_factory()
                try:
                    self._json(200, {"tools": agent.list_registered_tools()})
                finally:
                    agent.close()
                return
            self._json(404, {"error": "not found"})

        def do_POST(self) -> None:
            path = urlparse(self.path).path
            length = int(self.headers.get("Content-Length") or 0)
            body = self.rfile.read(length) if length else b"{}"
            try:
                data = json.loads(body.decode("utf-8") or "{}")
            except json.JSONDecodeError:
                self._json(400, {"error": "invalid json"})
                return
            if path not in {"/v1/chat", "/chat", "/v1/run"}:
                self._json(404, {"error": "not found"})
                return
            prompt = (data.get("prompt") or data.get("message") or data.get("input") or "").strip()
            if not prompt:
                self._json(400, {"error": "prompt is required"})
                return
            agent = agent_factory()
            try:
                text = agent.chat(prompt) if data.get("session") else agent.run(prompt)
                payload = {
                    "ok": True,
                    "text": text,
                    "trace": getattr(agent, "last_trace", []),
                }
                usage = getattr(agent, "usage", None)
                if usage is not None and hasattr(usage, "as_dict"):
                    payload["usage"] = usage.as_dict()
                self._json(200, payload)
            except Exception as e:
                self._json(500, {"error": str(e)})
            finally:
                agent.close()

    return Handler


def serve(
    host: str = "127.0.0.1",
    port: int = 8765,
    agent_factory=None,
) -> ThreadingHTTPServer:
    if agent_factory is None:
        from .factory import create_agent

        agent_factory = lambda: create_agent()  # noqa: E731
    httpd = ThreadingHTTPServer((host, port), make_handler(agent_factory))
    return httpd


def run_forever(host: str = "127.0.0.1", port: int = 8765, agent_factory=None) -> None:
    httpd = serve(host, port, agent_factory)
    print(f"grok-agent serve listening on http://{host}:{port}  (POST /v1/chat)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
