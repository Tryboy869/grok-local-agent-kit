"""Agent factory with optional MultiLLMRouter fallback and file config."""

from __future__ import annotations

import os
from typing import Any, Optional

from .agent import Agent
from .agent import create_agent as _create_agent_plain
from .config import load_config
from .hooks import HookBus
from .usage import UsageStats


def _ensure_hooks(agent: Agent, hooks: Any = None) -> Agent:
    if getattr(agent, "hooks", None) is None:
        agent.hooks = hooks if hooks is not None else HookBus()

    def on(event: str, fn):
        return agent.hooks.on(event, fn)

    agent.on = on  # type: ignore[method-assign]
    return agent


def _attach_usage(agent: Agent) -> None:
    if getattr(agent, "_usage_attached", False):
        return
    agent.usage = UsageStats()

    def _start(**_):
        agent.usage = UsageStats()

    def _before_llm(*, messages=None, **_):
        agent.usage.record_prompt(messages or [])

    def _after_tool(**_):
        agent.usage.record_tool()

    def _on_final(*, text="", **_):
        agent.usage.record_completion(text or "")
        try:
            agent.hooks.emit("on_token", agent=agent, text=text or "")
        except Exception:
            pass

    def _on_thought(*, text="", **_):
        if text:
            agent.usage.record_completion(text)
            try:
                agent.hooks.emit("on_token", agent=agent, text=text, kind="thought")
            except Exception:
                pass

    agent.hooks.on("on_start", _start)
    agent.hooks.on("before_llm", _before_llm)
    agent.hooks.on("after_tool", _after_tool)
    agent.hooks.on("on_final", _on_final)
    agent.hooks.on("on_thought", _on_thought)
    agent._usage_attached = True


def _attach_planner_tools(agent: Agent) -> None:
    if getattr(agent, "_planner_attached", False):
        return
    from .planner import plan_add, plan_done, plan_list

    if "plan_add" not in agent.tool_funcs:
        agent.register_tool(
            "plan_add",
            plan_add,
            "Add an item to the local workspace plan (.grok/plan.json).",
            {
                "type": "object",
                "properties": {"title": {"type": "string"}, "notes": {"type": "string"}},
                "required": ["title"],
            },
        )
        agent.register_tool(
            "plan_list",
            plan_list,
            "List workspace plan items. status=all|open|done.",
            {"type": "object", "properties": {"status": {"type": "string"}}, "required": []},
        )
        agent.register_tool(
            "plan_done",
            plan_done,
            "Mark a workspace plan item done by numeric id.",
            {
                "type": "object",
                "properties": {"item_id": {"type": "integer"}},
                "required": ["item_id"],
            },
        )
    agent._planner_attached = True


def _attach_guard(agent: Agent) -> None:
    from .agent_guard import apply as apply_guard
    from .guardrails import ToolGuard, get_guard, set_guard

    if getattr(agent, "guard", None) is None:
        agent.guard = get_guard() if isinstance(get_guard(), ToolGuard) else ToolGuard()
        set_guard(agent.guard)
    apply_guard(agent)


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
    _attach_usage(agent)
    _attach_planner_tools(agent)
    _attach_guard(agent)
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
