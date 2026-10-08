"""Playbook runner: sequence MVP goals and optionally hand off to a live model.

The scripted path never needs Ollama or LM Studio. A probe that is up records
a ReAct handoff. v0.47 calls that loop only when the caller passes a react
callable or live=True. The default demo still opens no chat socket.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from .mvp import PROVIDERS, probe_providers, run_mvp

SearchFn = Callable[[str], str]


def load_playbook(path: Path) -> Dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("steps"), list):
        raise ValueError("playbook must be an object with a steps list")
    if not data["steps"]:
        raise ValueError("playbook steps must not be empty")
    for step in data["steps"]:
        if not isinstance(step, dict) or not str(step.get("goal") or "").strip():
            raise ValueError("each step needs a non-empty goal")
    return data


ReactFn = Callable[[Dict[str, Any]], str]


def handoff_plan(prompt: str, probes: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Describe a live ReAct handoff when a local provider is up."""
    for name in ("ollama", "lmstudio"):
        row = probes.get(name) or {}
        if row.get("status") == "up":
            spec = PROVIDERS[name]
            return {
                "mode": "react",
                "provider": name,
                "base_url": spec["base_url"],
                "model": row.get("model") or ("llama3.2" if name == "ollama" else "local-model"),
                "prompt": prompt,
                "reason": "provider probe is up",
            }
    return {
        "mode": "scripted",
        "provider": None,
        "base_url": None,
        "model": None,
        "prompt": prompt,
        "reason": "no local provider up",
    }


def scripted_react(plan: Dict[str, Any]) -> str:
    """Offline stand-in for the ReAct loop. Used by demos and tests."""
    provider = plan.get("provider") or "none"
    prompt = plan.get("prompt") or ""
    return f"[react-scripted] {provider} :: {prompt}"


def _live_react(plan: Dict[str, Any]) -> Dict[str, Any]:
    """Opt-in call into Agent.run. Failures stay in the report; they do not raise."""
    try:
        from .agent import create_agent

        provider = "openai" if plan.get("provider") == "lmstudio" else "ollama"
        agent = create_agent(
            model=plan.get("model"),
            provider=provider,
            base_url=plan.get("base_url"),
        )
        try:
            answer = agent.run(str(plan.get("prompt") or ""))
        finally:
            agent.close()
        return {
            "executed": True,
            "mode": "react",
            "answer": answer,
            "error": None,
            "reason": "live agent.run",
        }
    except Exception as exc:  # pragma: no cover - depends on a local daemon
        return {
            "executed": False,
            "mode": "react",
            "answer": None,
            "error": str(exc),
            "reason": "live agent failed",
        }


def execute_handoff(
    plan: Dict[str, Any],
    react: Optional[ReactFn] = None,
    live: bool = False,
) -> Dict[str, Any]:
    """Call the ReAct loop only when mode is react and a runner is provided."""
    if plan.get("mode") != "react":
        return {
            "executed": False,
            "mode": plan.get("mode") or "scripted",
            "answer": None,
            "error": None,
            "reason": plan.get("reason") or "no local provider up",
        }
    if react is not None:
        try:
            answer = react(plan)
        except Exception as exc:
            return {
                "executed": False,
                "mode": "react",
                "answer": None,
                "error": str(exc),
                "reason": "injected react failed",
            }
        return {
            "executed": True,
            "mode": "react",
            "answer": str(answer),
            "error": None,
            "reason": "injected react callable",
        }
    if live:
        return _live_react(plan)
    return {
        "executed": False,
        "mode": "react",
        "answer": None,
        "error": None,
        "reason": "descriptor only; pass react= or live=True",
    }


def run_playbook(
    playbook: Dict[str, Any],
    workspace: Path,
    search: Optional[SearchFn] = None,
    probes: Optional[Dict[str, Dict[str, Any]]] = None,
    react: Optional[ReactFn] = None,
    live: bool = False,
) -> Dict[str, Any]:
    """Run every goal through the MVP router and write playbook-report.json."""
    workspace = Path(workspace)
    workspace.mkdir(parents=True, exist_ok=True)
    search = search or (lambda q: f"1. local agents\n2. ollama\n3. {q}")
    probes = probes if probes is not None else probe_providers(timeout=0.2)
    steps_out: List[Dict[str, Any]] = []
    for index, step in enumerate(playbook["steps"]):
        goal = str(step["goal"])
        result = run_mvp(goal, workspace, search=search)
        handoff = handoff_plan(goal, probes)
        called = execute_handoff(handoff, react=react, live=live)
        steps_out.append(
            {
                "id": str(step.get("id") or f"step-{index + 1}"),
                "goal": goal,
                "intent": result["intent"],
                "ok": bool(result["ok"]),
                "answer": result["answer"],
                "handoff": handoff,
                "react": called,
            }
        )
    called_n = sum(1 for row in steps_out if row["react"]["executed"])
    report = {
        "name": str(playbook.get("name") or "playbook"),
        "ok": all(row["ok"] for row in steps_out),
        "providers": {name: probes.get(name, {}).get("status", "unknown") for name in PROVIDERS},
        "handoff_mode": steps_out[-1]["handoff"]["mode"] if steps_out else "scripted",
        "react_called": called_n,
        "steps": steps_out,
    }
    (workspace / "playbook-report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return report


def builtin_playbook() -> Dict[str, Any]:
    return {
        "name": "local-mvp",
        "steps": [
            {"id": "chat", "goal": "write a note that the chat agent is ready"},
            {"id": "math", "goal": "compute sqrt(144) + 10"},
            {"id": "system", "goal": "what is the python version"},
            {"id": "search", "goal": "search local AI agents"},
            {"id": "mcp", "goal": "mcp ping the playbook"},
        ],
    }


def format_report(report: Dict[str, Any]) -> str:
    lines = [
        f"Playbook {report['name']} ok={report['ok']} handoff={report['handoff_mode']}",
        "providers: "
        + ", ".join(f"{name}={status}" for name, status in report["providers"].items()),
    ]
    for step in report["steps"]:
        first = str(step["answer"]).splitlines()[0][:100] if step["answer"] else ""
        react = step.get("react") or {}
        called = "called" if react.get("executed") else "skipped"
        lines.append(
            f"- {step['id']} intent={step['intent']} ok={step['ok']} "
            f"handoff={step['handoff']['mode']} react={called} :: {first}"
        )
    return "\n".join(lines)


def demo_playbook(workspace: Path, probes: Optional[Dict[str, Dict[str, Any]]] = None) -> str:
    report = run_playbook(builtin_playbook(), workspace, probes=probes)
    return format_report(report)


def demo_react(workspace: Path, probes: Optional[Dict[str, Dict[str, Any]]] = None) -> str:
    """Call the ReAct seam with the offline stand-in. No daemon required."""
    probes = probes or {
        "ollama": {"status": "up", "model": "llama3.2"},
        "lmstudio": {"status": "down"},
    }
    report = run_playbook(builtin_playbook(), workspace, probes=probes, react=scripted_react)
    return format_report(report)
