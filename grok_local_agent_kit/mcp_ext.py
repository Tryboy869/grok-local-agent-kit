"""Patch MCP stdio client/manager with prompts/list and prompts/get."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .mcp import MCPManager, StdioMCPClient, _format_rpc


def _client_list_prompts(self) -> Dict[str, Any]:
    err = self._ensure_init()
    if err is not None:
        return err
    return self.request("prompts/list")


def _client_get_prompt(self, name: str, arguments: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    err = self._ensure_init()
    if err is not None:
        return err
    params: Dict[str, Any] = {"name": name}
    if arguments:
        params["arguments"] = arguments
    return self.request("prompts/get", params)


def _mgr_list_prompts(self) -> str:
    pairs = self._stdio_servers()
    if not pairs:
        return "No MCP servers configured for prompts/list."
    chunks: List[str] = []
    for i, s in pairs:
        name = self._server_key(s, i)
        if not s.get("command"):
            chunks.append(f"[{name}] skip (no stdio command)")
            continue
        try:
            client = self._ensure_stdio(s, i)
            resp = client.list_prompts()
            chunks.append(f"[{name}] prompts/list:\n{_format_rpc(resp)}")
        except Exception as e:
            chunks.append(f"[{name}] failed: {e}")
    return "\n\n".join(chunks) if chunks else "No prompts discovered."


def _mgr_get_prompt(self, name: str, arguments: Optional[Dict[str, Any]] = None) -> str:
    name = (name or "").strip()
    if not name:
        return "Error: prompt name is required"
    last_err = "no stdio server available"
    for i, s in self._stdio_servers():
        if not s.get("command"):
            continue
        key = self._server_key(s, i)
        try:
            client = self._ensure_stdio(s, i)
            resp = client.get_prompt(name, arguments or {})
            if "error" in resp and "result" not in resp:
                last_err = _format_rpc(resp)
                continue
            return f"[{key}] prompts/get {name}:\n{_format_rpc(resp)}"
        except Exception as e:
            last_err = str(e)
    return f"MCP prompts/get '{name}' failed: {last_err}"


def apply() -> None:
    StdioMCPClient.list_prompts = _client_list_prompts  # type: ignore[method-assign]
    StdioMCPClient.get_prompt = _client_get_prompt  # type: ignore[method-assign]
    MCPManager.list_prompts = _mgr_list_prompts  # type: ignore[method-assign]
    MCPManager.get_prompt = _mgr_get_prompt  # type: ignore[method-assign]


apply()
