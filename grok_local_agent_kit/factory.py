"""Agent factory with optional MultiLLMRouter fallback."""

from __future__ import annotations

import os
from typing import Any, Optional

from .agent import Agent
from .agent import create_agent as _create_agent_plain


def create_agent(
    model: Optional[str] = None,
    provider: Optional[str] = None,
    base_url: Optional[str] = None,
    use_router: Optional[bool] = None,
    **kwargs: Any,
) -> Agent:
    if use_router is None:
        use_router = os.environ.get("GROK_AGENT_ROUTER", "").strip().lower() in {"1", "true", "yes"}
    kwargs.pop("use_router", None)
    agent = _create_agent_plain(model=model, provider=provider, base_url=base_url, **kwargs)
    agent.use_router = bool(use_router)
    agent.router = None
    agent.routed_via = getattr(agent.llm, "provider", provider or "ollama")
    if use_router:
        from .router import MultiLLMRouter, endpoint_from_env

        preferred = (provider or os.environ.get("GROK_AGENT_PROVIDER", "ollama")).lower().strip()
        chain = endpoint_from_env(preferred=preferred)
        if chain:
            if model:
                chain[0].model = model
            if base_url:
                chain[0].base_url = base_url
        router = MultiLLMRouter(chain)
        ep, client = router.pick()
        try:
            agent.llm.close()
        except Exception:
            pass
        agent.llm = client
        agent.router = router
        agent.routed_via = ep.name
        _orig_close = agent.close

        def _close() -> None:
            try:
                router.close()
            except Exception:
                pass
            _orig_close()

        agent.close = _close  # type: ignore[method-assign]
    return agent
