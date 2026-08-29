"""Multi-LLM router with ordered fallback (Ollama, LM Studio, OpenAI-compat)."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional

from .llm import LLMClient


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
    def __init__(self, chain: Optional[Iterable[LLMEndpoint]] = None, sticky: bool = True):
        self.chain: List[LLMEndpoint] = list(chain or endpoint_from_env())
        self.sticky = sticky
        self.active: Optional[LLMEndpoint] = None
        self._clients: Dict[str, LLMClient] = {}
        self.last_error: Optional[str] = None

    def _client_for(self, ep: LLMEndpoint) -> LLMClient:
        if ep.name not in self._clients:
            self._clients[ep.name] = LLMClient(
                model=ep.model, provider=ep.provider, base_url=ep.base_url, api_key=ep.api_key, temperature=ep.temperature
            )
        return self._clients[ep.name]

    def probe(self) -> List[Dict[str, str]]:
        rows = []
        for ep in self.chain:
            client = self._client_for(ep)
            status = client.ping()
            rows.append({"name": ep.name, "provider": ep.provider, "model": ep.model, "base_url": ep.base_url or "", "status": status})
        return rows

    def pick(self) -> tuple[LLMEndpoint, LLMClient]:
        if self.sticky and self.active is not None:
            return self.active, self._client_for(self.active)
        errors: List[str] = []
        for ep in self.chain:
            client = self._client_for(ep)
            status = client.ping()
            if status.startswith("ok"):
                self.active = ep
                self.last_error = None
                return ep, client
            errors.append(f"{ep.name}: {status}")
        self.last_error = "; ".join(errors) or "no endpoints configured"
        ep = self.chain[0]
        self.active = ep
        return ep, self._client_for(ep)

    def chat(self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]] = None, tool_choice: str = "auto") -> Dict[str, Any]:
        ep, client = self.pick()
        result = client.chat(messages, tools=tools, tool_choice=tool_choice)
        content = result.get("content") or ""
        if isinstance(content, str) and content.startswith("[LLM error]") and self.sticky:
            self.active = None
            for other in self.chain:
                if other.name == ep.name:
                    continue
                alt = self._client_for(other)
                status = alt.ping()
                if not status.startswith("ok"):
                    continue
                self.active = other
                return alt.chat(messages, tools=tools, tool_choice=tool_choice)
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
