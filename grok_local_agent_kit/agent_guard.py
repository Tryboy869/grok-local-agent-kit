"""Patch Agent._run_one_tool to honor ToolGuard timeouts and allow/deny lists."""

from __future__ import annotations

from typing import Any, Dict, Tuple

from .tools import execute_tool


def apply(agent) -> None:
    if getattr(agent, "_guard_patched", False):
        return

    def _run_one_tool(tc: Dict[str, Any]) -> Tuple[Dict[str, Any], str, Dict[str, Any]]:
        name = tc.get("name") or ""
        args = agent._parse_args(tc.get("arguments", {}))
        agent.hooks.emit("before_tool", agent=agent, name=name, args=args)
        guard = getattr(agent, "guard", None)
        if guard is not None:

            def _call(**kwargs):
                return execute_tool(name, kwargs, agent.tool_funcs)

            result = guard.run(name, _call, args)
        else:
            result = execute_tool(name, args, agent.tool_funcs)
        result = agent._truncate_tool_result(result)
        agent.hooks.emit("after_tool", agent=agent, name=name, args=args, result=result)
        step = {"type": "tool", "name": name, "args": args, "result": result[:500]}
        return tc, result, step

    agent._run_one_tool = _run_one_tool  # type: ignore[method-assign]
    agent._guard_patched = True
