"""MCP Streamable HTTP session ids + in-flight request cancellation."""

from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class MCPSession:
    session_id: str
    created_at: float = field(default_factory=time.time)
    last_seen: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)
    inflight: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    cancelled_requests: List[str] = field(default_factory=list)

    def touch(self) -> None:
        self.last_seen = time.time()

    def header(self) -> Dict[str, str]:
        return {"Mcp-Session-Id": self.session_id}


class MCPSessionRegistry:
    """Track Streamable HTTP sessions and cancel pending JSON-RPC ids."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._sessions: Dict[str, MCPSession] = {}

    def open(self, session_id: Optional[str] = None, **metadata: Any) -> MCPSession:
        sid = session_id or str(uuid.uuid4())
        with self._lock:
            sess = self._sessions.get(sid)
            if sess is None:
                sess = MCPSession(session_id=sid, metadata=dict(metadata))
                self._sessions[sid] = sess
            else:
                sess.metadata.update(metadata)
                sess.touch()
            return sess

    def get(self, session_id: str) -> Optional[MCPSession]:
        with self._lock:
            return self._sessions.get(session_id)

    def close(self, session_id: str) -> bool:
        with self._lock:
            return self._sessions.pop(session_id, None) is not None

    def begin_request(self, session_id: str, request_id: str, method: str) -> MCPSession:
        sess = self.open(session_id)
        with self._lock:
            sess.inflight[str(request_id)] = {
                "method": method,
                "started": time.time(),
            }
            sess.touch()
        return sess

    def finish_request(self, session_id: str, request_id: str) -> None:
        sess = self.get(session_id)
        if not sess:
            return
        with self._lock:
            sess.inflight.pop(str(request_id), None)
            sess.touch()

    def cancel_request(self, session_id: str, request_id: str) -> bool:
        sess = self.get(session_id)
        if not sess:
            return False
        rid = str(request_id)
        with self._lock:
            gone = sess.inflight.pop(rid, None)
            sess.cancelled_requests.append(rid)
            sess.touch()
        return gone is not None

    def is_cancelled(self, session_id: str, request_id: str) -> bool:
        sess = self.get(session_id)
        if not sess:
            return False
        return str(request_id) in sess.cancelled_requests

    def list_sessions(self) -> List[Dict[str, Any]]:
        with self._lock:
            out = []
            for s in self._sessions.values():
                out.append(
                    {
                        "session_id": s.session_id,
                        "age_s": round(time.time() - s.created_at, 3),
                        "inflight": list(s.inflight),
                        "cancelled": list(s.cancelled_requests),
                        "metadata": dict(s.metadata),
                    }
                )
            return out


_REGISTRY = MCPSessionRegistry()


def get_registry() -> MCPSessionRegistry:
    return _REGISTRY


def reset_registry() -> MCPSessionRegistry:
    global _REGISTRY
    _REGISTRY = MCPSessionRegistry()
    return _REGISTRY


def run_cancellable(
    session_id: str,
    request_id: str,
    method: str,
    fn: Callable[[], Any],
) -> Any:
    """Run fn unless the request was cancelled before or during start."""
    reg = get_registry()
    if reg.is_cancelled(session_id, request_id):
        return {"error": {"code": -32800, "message": "Request cancelled"}}
    reg.begin_request(session_id, request_id, method)
    try:
        if reg.is_cancelled(session_id, request_id):
            return {"error": {"code": -32800, "message": "Request cancelled"}}
        return fn()
    finally:
        reg.finish_request(session_id, request_id)
