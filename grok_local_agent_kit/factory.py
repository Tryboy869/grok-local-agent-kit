"""Agent factory with optional MultiLLMRouter fallback and file config."""

from __future__ import annotations

import os
from typing import Any, Optional

from .agent import Agent
from .agent import create_agent as _create_agent_plain
from .config import load_config
from .hooks import HookBus


def _ensure_hooks(agent: Agent, hooks: Any = None) -> Agent:
    if getattr(agent, "hooks", None) is None:
        agent.hooks = hooks if hooks is not None else HookBus()

    def on(event: str, fn):
        return agent.hooks.on(event, fn)

    agent.on = on  # type: ignore[method-assign]
    return agent


def create_agent(
    model: Optional[str] = None,
    provider: Optional[str] = None,
    base_url: Optional[str] = None,
    use_router: Optional[bool] = None,
    hooks: Any = None,
    **kwargs: Any,
) -> Agent:
    cfg = load_config()
    model = model or cfg.model
    provider = provider or cfg.provider
    base_url = base_url if base_url is not None else cfg.base_url
    if use_router is None:
        use_router = cfg.use_router or (
            os.environ.get("GROK_AGENT_ROUTER", "").strip().lower() in {"1", "true", "yes"}
        )
    for key, value in cfg.to_agent_kwargs().items():
        if key in {"model", "provider", "base_url", "use_router"}:
            continue
        kwargs.setdefault(key, value)
    kwargs.pop("use_router", None)
    kwargs.pop("hooks", None)
    agent = _create_agent_plain(model=model, provider=provider, base_url=base_url, **kwargs)
    _ensure_hooks(agent, hooks)
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
