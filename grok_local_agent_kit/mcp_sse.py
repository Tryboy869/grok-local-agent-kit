"""Minimal MCP Streamable HTTP / SSE client with reconnect."""

from __future__ import annotations

import json
import time
from typing import Any, Dict, Iterator, Optional

import httpx


class SSEMCPClient:
    def __init__(
        self,
        url: str,
        timeout: float = 30.0,
        max_retries: int = 3,
        backoff: float = 0.4,
        headers: Optional[Dict[str, str]] = None,
    ):
        self.url = url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max(1, max_retries)
        self.backoff = backoff
        self.headers = {
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json",
            **(headers or {}),
        }
        self._id = 0

    def _next_id(self) -> int:
        self._id += 1
        return self._id

    def request(self, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        payload = {"jsonrpc": "2.0", "id": self._next_id(), "method": method}
        if params is not None:
            payload["params"] = params
        last_err: Optional[Exception] = None
        for attempt in range(self.max_retries):
            try:
                with httpx.Client(timeout=self.timeout) as client:
                    r = client.post(self.url, json=payload, headers=self.headers)
                    ctype = (r.headers.get("content-type") or "").lower()
                    if "text/event-stream" in ctype:
                        return self._parse_sse_body(r.text)
                    r.raise_for_status()
                    data = r.json()
                    if isinstance(data, dict):
                        return data
                    return {"result": data}
            except Exception as e:
                last_err = e
                time.sleep(self.backoff * (2**attempt))
        return {"error": {"message": f"SSE/HTTP request failed after retries: {last_err}"}}

    def _parse_sse_body(self, body: str) -> Dict[str, Any]:
        last: Dict[str, Any] = {}
        data_buf: list[str] = []
        for raw in body.splitlines():
            line = raw.strip("\r")
            if not line:
                if data_buf:
                    blob = "\n".join(data_buf)
                    data_buf = []
                    try:
                        last = json.loads(blob)
                    except json.JSONDecodeError:
                        last = {"result": blob}
                continue
            if line.startswith("data:"):
                data_buf.append(line[5:].lstrip())
        if data_buf:
            blob = "\n".join(data_buf)
            try:
                last = json.loads(blob)
            except json.JSONDecodeError:
                last = {"result": blob}
        return last or {"error": {"message": "empty SSE stream"}}

    def iter_events(self, method: str, params: Optional[Dict[str, Any]] = None) -> Iterator[Dict[str, Any]]:
        payload = {"jsonrpc": "2.0", "id": self._next_id(), "method": method}
        if params is not None:
            payload["params"] = params
        with httpx.Client(timeout=self.timeout) as client:
            with client.stream("POST", self.url, json=payload, headers=self.headers) as r:
                buf = ""
                for chunk in r.iter_text():
                    buf += chunk
                    while "\n\n" in buf:
                        event, buf = buf.split("\n\n", 1)
                        data_lines = [
                            ln[5:].lstrip()
                            for ln in event.splitlines()
                            if ln.startswith("data:")
                        ]
                        if not data_lines:
                            continue
                        blob = "\n".join(data_lines)
                        try:
                            yield json.loads(blob)
                        except json.JSONDecodeError:
                            yield {"data": blob}

    def initialize(self) -> Dict[str, Any]:
        return self.request(
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "grok-local-agent-kit", "version": "0.13.0"},
            },
        )

    def list_tools(self) -> Dict[str, Any]:
        return self.request("tools/list")

    def list_prompts(self) -> Dict[str, Any]:
        return self.request("prompts/list")


def probe_sse_mcp(url: str) -> str:
    client = SSEMCPClient(url, max_retries=2)
    init = client.initialize()
    tools = client.list_tools()
    return json.dumps({"initialize": init, "tools": tools}, indent=2, default=str)[:4000]
