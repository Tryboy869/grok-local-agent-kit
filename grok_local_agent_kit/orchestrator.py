"""Lightweight multi-agent orchestrator: planner + specialist workers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional


@dataclass
class Role:
    name: str
    instruction: str


DEFAULT_ROLES: Dict[str, Role] = {
    "planner": Role("planner", "Break the user goal into 2-5 concrete steps. Do not solve the whole task yourself."),
    "researcher": Role("researcher", "Gather facts with tools (web_search, http_get, read_file). Cite sources. Be brief."),
    "coder": Role("coder", "Write or inspect code with file tools and execute_python. Prefer small patches."),
    "operator": Role("operator", "Execute workspace actions: files, shell (safe), memory. Confirm what changed."),
}


class Orchestrator:
    def __init__(self, agent_factory: Callable[..., object], roles: Optional[Dict[str, Role]] = None):
        self.agent_factory = agent_factory
        self.roles = roles or dict(DEFAULT_ROLES)

    def run(self, goal: str, specialists: Optional[List[str]] = None, verbose: bool = False) -> str:
        specialists = specialists or ["researcher", "operator"]
        planner = self.agent_factory()
        plan = planner.run(  # type: ignore[attr-defined]
            f"{self.roles['planner'].instruction}\n\nGoal:\n{goal}\n\nReturn a numbered list of steps only."
        )
        outputs = [f"## Plan\n{plan}"]
        for name in specialists:
            role = self.roles.get(name)
            if role is None:
                outputs.append(f"## {name}\nunknown role")
                continue
            worker = self.agent_factory()
            result = worker.run(  # type: ignore[attr-defined]
                f"You are the {role.name} specialist.\n{role.instruction}\n\nOverall goal:\n{goal}\n\nPlan:\n{plan}\n\nDo your part, use tools, then summarize what you did."
            )
            outputs.append(f"## {name}\n{result}")
            if verbose:
                outputs.append(f"(specialist={name} done)")
        return "\n\n".join(outputs)
