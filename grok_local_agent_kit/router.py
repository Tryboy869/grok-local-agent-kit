"""Multi-LLM router with ordered fallback (Ollama, LM Studio, OpenAI-compat)."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Union

from .llm import LLMClient

try:
    from .health import HealthBoard, load_board as load_health, save_board as save_health
except Exception:  # pragma: no cover
    HealthBoard = None  # type: ignore
    load_health = None  # type: ignore
    save_health = None  # type: ignore

PathLike = Union[str, Path]
DEFAULT_HEALTH_PATH = "health.json"


@dataclass
class LLMEndpoint:
    name: str
    provider: str
    model: str
    base_url: Optional[str] = None
    api_key: Optional[str] = None
    temperature: float = 0.3


DEFAULT_CHAIN: List[LLMEndpoint] = [
    LLMEndpoint(
        name="ollama",
        provider="ollama",
        model=os.environ.get("GROK_AGENT_MODEL", "llama3.2"),
        base_url=os.environ.get("GROK_AGENT_OLLAMA_URL", "http://localhost:11434"),
    ),
    LLMEndpoint(
        name="lmstudio",
        provider="openai",
        model=os.environ.get("GROK_AGENT_LMSTUDIO_MODEL", "local-model"),
        base_url=os.environ.get("GROK_AGENT_LMSTUDIO_URL", "http://localhost:1234/v1"),
        api_key=os.environ.get("GROK_AGENT_LMSTUDIO_KEY", "lm-studio"),
    ),
]


def endpoint_from_env(preferred: Optional[str] = None) -> List[LLMEndpoint]:
    preferred = (preferred or os.environ.get("GROK_AGENT_PROVIDER") or "ollama").lower().strip()
    if preferred == "lmstudio":
        preferred = "openai"
    chain = list(DEFAULT_CHAIN)
    if preferred in {"openai"}:
        chain = [e for e in chain if e.provider == "openai"] + [e for e in chain if e.provider != "openai"]
    elif preferred == "ollama":
        chain = [e for e in chain if e.provider == "ollama"] + [e for e in chain if e.provider != "ollama"]
    extra_url = os.environ.get("GROK_AGENT_BASE_URL")
    extra_model = os.environ.get("GROK_AGENT_MODEL")
    if extra_url and preferred in {"openai", "lmstudio"}:
        chain.insert(0, LLMEndpoint(name="custom", provider="openai", model=extra_model or "local-model", base_url=extra_url))
    return chain


class MultiLLMRouter:
    def __init__(
        self,
        chain: Optional[Iterable[LLMEndpoint]] = None,
        sticky: bool = True,
        health: Optional["HealthBoard"] = None,
        persist_path: Optional[PathLike] = None,
    ):
        self.chain: List[LLMEndpoint] = list(chain or endpoint_from_env())
        self.sticky = sticky
        self.active: Optional[LLMEndpoint] = None
        self._clients: Dict[str, LLMClient] = {}
        self.last_error: Optional[str] = None
        self.health = health
        self.persist_path: Optional[str] = str(persist_path) if persist_path else None

    def attach_persist(self, path: PathLike, load_existing: bool = True) -> Path:
        """Bind this router to a cwd-safe health.json and optionally hydrate the board."""
        self.persist_path = str(path)
        if load_existing and load_health is not None:
            loaded = load_health(path)
            if self.health is None:
                self.health = loaded
            else:
                for name, br in loaded.breakers.items():
                    self.health.breakers.setdefault(name, br)
        elif self.health is None and HealthBoard is not None:
            self.health = HealthBoard()
        return self.persist()

    def persist(self) -> Path:
        if not self.persist_path:
            raise ValueError("no persist_path set; call attach_persist() first")
        if self.health is None or save_health is None:
            raise ValueError("no HealthBoard attached")
        return save_health(self.health, self.persist_path)

    def _client_for(self, ep: LLMEndpoint) -> LLMClient:
        if ep.name not in self._clients:
            self._clients[ep.name] = LLMClient(
                model=ep.model, provider=ep.provider, base_url=ep.base_url, api_key=ep.api_key, temperature=ep.temperature
            )
        return self._clients[ep.name]

    def _allowed(self, ep: LLMEndpoint, now: Optional[float] = None) -> bool:
        if self.health is None:
            return True
        return bool(self.health.allow(ep.name, now=now))

    def _mark(self, ep: LLMEndpoint, status: str) -> None:
        if self.health is None:
            return
        if status.startswith("ok"):
            self.health.success(ep.name)
        else:
            self.health.failure(ep.name, error=status)
        if self.persist_path and save_health is not None:
            save_health(self.health, self.persist_path)

    def probe(self) -> List[Dict[str, str]]:
        rows = []
        for ep in self.chain:
            allowed = self._allowed(ep)
            if not allowed:
                rows.append(
                    {
                        "name": ep.name,
                        "provider": ep.provider,
                        "model": ep.model,
                        "base_url": ep.base_url or "",
                        "status": "breaker-open",
                    }
                )
                continue
            client = self._client_for(ep)
            status = client.ping()
            self._mark(ep, status)
            rows.append(
                {
                    "name": ep.name,
                    "provider": ep.provider,
                    "model": ep.model,
                    "base_url": ep.base_url or "",
                    "status": status,
                }
            )
        return rows

    def pick(self, now: Optional[float] = None) -> tuple[LLMEndpoint, LLMClient]:
        if self.sticky and self.active is not None:
            if self._allowed(self.active, now=now):
                return self.active, self._client_for(self.active)
            self.active = None
        errors: List[str] = []
        for ep in self.chain:
            if not self._allowed(ep, now=now):
                errors.append(f"{ep.name}: breaker-open")
                continue
            client = self._client_for(ep)
            status = client.ping()
            self._mark(ep, status)
            if status.startswith("ok"):
                self.active = ep
                self.last_error = None
                return ep, client
            errors.append(f"{ep.name}: {status}")
        self.last_error = "; ".join(errors) or "no endpoints configured"
        for ep in self.chain:
            if self._allowed(ep, now=now):
                self.active = ep
                return ep, self._client_for(ep)
        ep = self.chain[0]
        self.active = ep
        return ep, self._client_for(ep)

    def chat(self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]] = None, tool_choice: str = "auto") -> Dict[str, Any]:
        ep, client = self.pick()
        result = client.chat(messages, tools=tools, tool_choice=tool_choice)
        content = result.get("content") or ""
        if isinstance(content, str) and content.startswith("[LLM error]"):
            self._mark(ep, content)
            self.active = None
            for other in self.chain:
                if other.name == ep.name:
                    continue
                if not self._allowed(other):
                    continue
                alt = self._client_for(other)
                status = alt.ping()
                self._mark(other, status)
                if not status.startswith("ok"):
                    continue
                self.active = other
                alt_result = alt.chat(messages, tools=tools, tool_choice=tool_choice)
                alt_result["routed_via"] = other.name
                return alt_result
        else:
            self._mark(ep, "ok")
        result["routed_via"] = ep.name
        return result

    def close(self) -> None:
        for c in self._clients.values():
            c.close()
        self._clients.clear()
        self.active = None


def format_probe(rows: List[Dict[str, str]]) -> str:
    lines = ["LLM route probe:"]
    for r in rows:
        lines.append(f"- {r['name']} ({r['provider']}/{r['model']}) @ {r['base_url'] or '-'} → {r['status']}")
    return "\n".join(lines)


def demo_routed_health() -> str:
    """Offline story: open breaker skips lmstudio; pick lands on ollama."""
    from .health import HealthBoard

    board = HealthBoard(threshold=1, cooldown_s=60)
    board.trip("lmstudio", error="connection refused")

    class _Fake:
        def __init__(self, name: str, status: str):
            self.name = name
            self.status = status

        def ping(self) -> str:
            return self.status

        def chat(self, *a, **k):
            return {"content": f"ok via {self.name}", "tool_calls": []}

        def close(self) -> None:
            return None

    router = MultiLLMRouter(health=board, sticky=False)
    router._clients["ollama"] = _Fake("ollama", "ok")  # type: ignore[assignment]
    router._clients["lmstudio"] = _Fake("lmstudio", "ok")  # type: ignore[assignment]
    ep, _ = router.pick()
    probe = format_probe(router.probe())
    return f"picked={ep.name}\n{probe}\nlast_error={router.last_error or '-'}"


def demo_persisted_route(path: PathLike = DEFAULT_HEALTH_PATH) -> str:
    """Offline story: probe() writes health.json; a second router reloads it."""
    from .health import HealthBoard, format_board, load_board

    board = HealthBoard(threshold=1, cooldown_s=60)
    router = MultiLLMRouter(health=board, sticky=False, persist_path=path)

    class _Fake:
        def __init__(self, name: str, status: str):
            self.name = name
            self.status = status

        def ping(self) -> str:
            return self.status

        def chat(self, *a, **k):
            return {"content": f"ok via {self.name}", "tool_calls": []}

        def close(self) -> None:
            return None

    router._clients["ollama"] = _Fake("ollama", "ok")  # type: ignore[assignment]
    router._clients["lmstudio"] = _Fake("lmstudio", "connection refused")  # type: ignore[assignment]
    router.probe()
    ep, _ = router.pick()
    dest = router.persist()
    reloaded = load_board(dest)
    second = MultiLLMRouter(sticky=False)
    second.attach_persist(dest)
    assert second.health is not None
    assert second.health.breaker("lmstudio").state == "open"
    return (
        f"picked={ep.name}\n"
        f"wrote={dest}\n"
        f"{format_board(reloaded)}"
    )
