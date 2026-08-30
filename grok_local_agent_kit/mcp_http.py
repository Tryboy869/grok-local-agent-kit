"""Minimal MCP-over-HTTP JSON-RPC helper (Streamable HTTP / JSON POST)."""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional
from urllib.error import URLError
from urllib.request import Request, urlopen


class HTTPMCPClient:
    def __init__(self, url: str, timeout: float = 20.0, headers: Optional[Dict[str, str]] = None):
        self.url = url.rstrip("/")
        self.timeout = timeout
        self.headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if headers:
            self.headers.update(headers)
        self._id = 0
        self.initialized = False
        self.server_info: Dict[str, Any] = {}

    def _rpc(self, method: str, params: Optional[Dict[str, Any]] = None) -> Any:
        self._id += 1
        payload = {"jsonrpc": "2.0", "id": self._id, "method": method}
        if params is not None:
            payload["params"] = params
        body = json.dumps(payload).encode("utf-8")
        req = Request(self.url, data=body, headers=self.headers, method="POST")
        try:
            with urlopen(req, timeout=self.timeout) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
        except URLError as e:
            raise RuntimeError(f"MCP HTTP error talking to {self.url}: {e}") from e
        data = json.loads(raw) if raw.strip() else {}
        if "error" in data and data["error"]:
            raise RuntimeError(f"MCP RPC error: {data['error']}")
        return data.get("result")

    def initialize(self) -> Dict[str, Any]:
        result = self._rpc(
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "grok-local-agent-kit", "version": "0.11.0"},
            },
        )
        self.initialized = True
        self.server_info = result or {}
        try:
            self._rpc("notifications/initialized", {})
        except Exception:
            pass
        return self.server_info

    def list_tools(self) -> List[Dict[str, Any]]:
        if not self.initialized:
            self.initialize()
        result = self._rpc("tools/list", {}) or {}
        return list(result.get("tools") or [])

    def call_tool(self, name: str, arguments: Optional[Dict[str, Any]] = None) -> str:
        if not self.initialized:
            self.initialize()
        result = self._rpc("tools/call", {"name": name, "arguments": arguments or {}}) or {}
        content = result.get("content")
        if isinstance(content, list):
            parts = []
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    parts.append(str(item.get("text", "")))
                else:
                    parts.append(json.dumps(item, ensure_ascii=False))
            return "\n".join(parts) or json.dumps(result, ensure_ascii=False)
        return json.dumps(result, ensure_ascii=False)


def probe_http_mcp(url: str) -> str:
    try:
        client = HTTPMCPClient(url)
        info = client.initialize()
        tools = client.list_tools()
        name = (info.get("serverInfo") or {}).get("name") or url
        return f"ok {name}: {len(tools)} tool(s)"
    except Exception as e:
        return f"error: {e}"
