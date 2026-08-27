"""Minimal MCP client: JSON-RPC over stdio (and config loading).

Implements enough of the Model Context Protocol to:
  - load server configs from GROK_MCP_SERVERS / .mcp_servers.json / .grok/mcp.json
  - spawn a stdio server
  - initialize, list tools/resources, call tools

HTTP/SSE transport remains a stub that reports configured endpoints.
"""

from __future__ import annotations

import json
import os
import subprocess
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional


PROTOCOL_VERSION = "2024-11-05"


def load_mcp_config() -> Dict[str, Any]:
    raw = os.environ.get("GROK_MCP_SERVERS", "").strip()
    if raw:
        try:
            data = json.loads(raw)
            if isinstance(data, list):
                return {"servers": data}
            if isinstance(data, dict) and "servers" in data:
                return data
        except json.JSONDecodeError as e:
            return {"servers": [], "error": f"Invalid GROK_MCP_SERVERS JSON: {e}"}
    for candidate in (".mcp_servers.json", "mcp_servers.json", ".grok/mcp.json"):
        p = Path(candidate)
        if p.is_file():
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                if isinstance(data, dict) and "servers" in data:
                    return data
                if isinstance(data, list):
                    return {"servers": data}
            except Exception as e:
                return {"servers": [], "error": f"Failed to parse {candidate}: {e}"}
    return {"servers": []}


class StdioMCPClient:
    """JSON-RPC client talking to one MCP server over stdin/stdout."""

    def __init__(self, command: str, args: Optional[List[str]] = None, env: Optional[Dict[str, str]] = None, timeout: float = 20.0):
        self.command = command
        self.args = args or []
        self.env = env
        self.timeout = timeout
        self._proc: Optional[subprocess.Popen[str]] = None
        self._id = 0
        self._lock = threading.Lock()
        self._initialized = False

    def start(self) -> None:
        if self._proc is not None:
            return
        env = os.environ.copy()
        if self.env:
            env.update({str(k): str(v) for k, v in self.env.items()})
        self._proc = subprocess.Popen(
            [self.command, *self.args],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            env=env,
        )

    def close(self) -> None:
        if self._proc is None:
            return
        try:
            self._proc.terminate()
            self._proc.wait(timeout=3)
        except Exception:
            try:
                self._proc.kill()
            except Exception:
                pass
        self._proc = None
        self._initialized = False

    def _next_id(self) -> int:
        self._id += 1
        return self._id

    def request(self, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if self._proc is None:
            self.start()
        assert self._proc is not None and self._proc.stdin and self._proc.stdout
        with self._lock:
            msg = {"jsonrpc": "2.0", "id": self._next_id(), "method": method}
            if params is not None:
                msg["params"] = params
            line = json.dumps(msg, ensure_ascii=False) + "\n"
            try:
                self._proc.stdin.write(line)
                self._proc.stdin.flush()
            except Exception as e:
                return {"error": {"message": f"write failed: {e}"}}
            deadline = time.time() + self.timeout
            while time.time() < deadline:
                if self._proc.poll() is not None:
                    err = ""
                    if self._proc.stderr:
                        err = self._proc.stderr.read()[:2000]
                    return {"error": {"message": f"server exited ({self._proc.returncode}): {err}"}}
                raw = self._proc.stdout.readline()
                if not raw:
                    time.sleep(0.02)
                    continue
                raw = raw.strip()
                if not raw:
                    continue
                try:
                    obj = json.loads(raw)
                except json.JSONDecodeError:
                    continue
                if obj.get("id") == msg["id"]:
                    return obj
            return {"error": {"message": f"timeout after {self.timeout}s waiting for {method}"}}

    def notify(self, method: str, params: Optional[Dict[str, Any]] = None) -> None:
        if self._proc is None:
            self.start()
        assert self._proc is not None and self._proc.stdin
        msg: Dict[str, Any] = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            msg["params"] = params
        with self._lock:
            self._proc.stdin.write(json.dumps(msg) + "\n")
            self._proc.stdin.flush()

    def initialize(self) -> Dict[str, Any]:
        result = self.request(
            "initialize",
            {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": {"name": "grok-local-agent-kit", "version": "0.9.0"},
            },
        )
        if "error" not in result:
            try:
                self.notify("notifications/initialized")
            except Exception:
                pass
            self._initialized = True
        return result

    def list_tools(self) -> Dict[str, Any]:
        if not self._initialized:
            init = self.initialize()
            if "error" in init and "result" not in init:
                return init
        return self.request("tools/list")

    def list_resources(self) -> Dict[str, Any]:
        if not self._initialized:
            init = self.initialize()
            if "error" in init and "result" not in init:
                return init
        return self.request("resources/list")

    def call_tool(self, name: str, arguments: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if not self._initialized:
            init = self.initialize()
            if "error" in init and "result" not in init:
                return init
        return self.request("tools/call", {"name": name, "arguments": arguments or {}})


def _format_rpc(resp: Dict[str, Any]) -> str:
    if "error" in resp:
        err = resp["error"]
        if isinstance(err, dict):
            return f"MCP error: {err.get('message', err)}"
        return f"MCP error: {err}"
    result = resp.get("result", resp)
    try:
        return json.dumps(result, indent=2, ensure_ascii=False)
    except TypeError:
        return str(result)


class MCPManager:
    """Manage configured MCP servers and dispatch list/call operations."""

    def __init__(self) -> None:
        self._clients: Dict[str, StdioMCPClient] = {}

    def _server_key(self, server: Dict[str, Any], index: int) -> str:
        return str(server.get("name") or server.get("command") or f"server_{index}")

    def _ensure_stdio(self, server: Dict[str, Any], index: int) -> StdioMCPClient:
        key = self._server_key(server, index)
        if key not in self._clients:
            cmd = server.get("command")
            if not cmd:
                raise RuntimeError(f"Server '{key}' has no command (stdio required)")
            client = StdioMCPClient(
                command=str(cmd),
                args=list(server.get("args") or []),
                env=server.get("env") if isinstance(server.get("env"), dict) else None,
            )
            self._clients[key] = client
        return self._clients[key]

    def describe(self) -> str:
        cfg = load_mcp_config()
        servers = cfg.get("servers") or []
        lines = [
            "MCP client: stdio JSON-RPC (v0.9.0)",
            f"Configured servers: {len(servers)}",
        ]
        if cfg.get("error"):
            lines.append(f"Config note: {cfg['error']}")
        for i, s in enumerate(servers[:20], 1):
            if not isinstance(s, dict):
                lines.append(f"  {i}. (invalid {type(s).__name__})")
                continue
            name = s.get("name") or s.get("command") or f"server_{i}"
            transport = s.get("transport") or ("stdio" if s.get("command") else s.get("url") and "http" or "unknown")
            extra = s.get("command") or s.get("url") or ""
            lines.append(f"  {i}. {name} ({transport}) {extra}".rstrip())
        if not servers:
            lines.append("No servers configured. Set GROK_MCP_SERVERS or create .mcp_servers.json.")
            lines.append(
                'Example: [{"name":"echo","command":"python","args":["-m","grok_local_agent_kit.mcp_echo_server"]}]'
            )
        return "\n".join(lines)

    def list_tools(self) -> str:
        cfg = load_mcp_config()
        servers = [s for s in (cfg.get("servers") or []) if isinstance(s, dict)]
        if not servers:
            return (
                "No MCP servers configured.\n"
                "Set GROK_MCP_SERVERS or add .mcp_servers.json, then retry mcp_list_tools."
            )
        chunks: List[str] = []
        for i, s in enumerate(servers, 1):
            name = self._server_key(s, i)
            transport = s.get("transport") or ("stdio" if s.get("command") else "http")
            if transport != "stdio" and not s.get("command"):
                chunks.append(f"[{name}] HTTP/SSE transport not implemented yet (url={s.get('url')})")
                continue
            try:
                client = self._ensure_stdio(s, i)
                resp = client.list_tools()
                chunks.append(f"[{name}] tools/list:\n{_format_rpc(resp)}")
            except Exception as e:
                chunks.append(f"[{name}] failed: {e}")
        return "\n\n".join(chunks) if chunks else "No tools discovered."

    def list_resources(self) -> str:
        cfg = load_mcp_config()
        servers = [s for s in (cfg.get("servers") or []) if isinstance(s, dict)]
        header = self.describe()
        if not servers:
            return header
        chunks = [header]
        for i, s in enumerate(servers, 1):
            name = self._server_key(s, i)
            if not s.get("command"):
                chunks.append(f"[{name}] skip (no stdio command)")
                continue
            try:
                client = self._ensure_stdio(s, i)
                resp = client.list_resources()
                chunks.append(f"[{name}] resources/list:\n{_format_rpc(resp)}")
            except Exception as e:
                chunks.append(f"[{name}] failed: {e}")
        return "\n\n".join(chunks)

    def call_tool(self, name: str, arguments: Optional[Dict[str, Any]] = None) -> str:
        cfg = load_mcp_config()
        servers = [s for s in (cfg.get("servers") or []) if isinstance(s, dict)]
        if not servers:
            return f"Cannot call '{name}': no MCP servers configured."
        last_err = "no stdio server available"
        for i, s in enumerate(servers, 1):
            if not s.get("command"):
                continue
            key = self._server_key(s, i)
            try:
                client = self._ensure_stdio(s, i)
                resp = client.call_tool(name, arguments or {})
                if "error" in resp and "result" not in resp:
                    last_err = _format_rpc(resp)
                    continue
                return f"[{key}] tools/call {name}:\n{_format_rpc(resp)}"
            except Exception as e:
                last_err = str(e)
        return f"MCP call '{name}' failed: {last_err}"

    def close(self) -> None:
        for c in self._clients.values():
            c.close()
        self._clients.clear()


_MANAGER: Optional[MCPManager] = None


def get_manager() -> MCPManager:
    global _MANAGER
    if _MANAGER is None:
        _MANAGER = MCPManager()
    return _MANAGER
