"""Playbook runner: sequence MVP goals and optionally hand off to a live model.

The scripted path never needs Ollama or LM Studio. If a caller injects a probe
where a provider is up, the step also records a ReAct handoff descriptor.
Nothing in this module opens a chat socket.
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


def handoff_plan(prompt: str, probes: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Describe a live ReAct handoff when a local provider is up. Never calls it."""
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


def run_playbook(
    playbook: Dict[str, Any],
    workspace: Path,
    search: Optional[SearchFn] = None,
    probes: Optional[Dict[str, Dict[str, Any]]] = None,
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
        steps_out.append(
            {
                "id": str(step.get("id") or f"step-{index + 1}"),
                "goal": goal,
                "intent": result["intent"],
                "ok": bool(result["ok"]),
                "answer": result["answer"],
                "handoff": handoff,
            }
        )
    report = {
        "name": str(playbook.get("name") or "playbook"),
        "ok": all(row["ok"] for row in steps_out),
        "providers": {name: probes.get(name, {}).get("status", "unknown") for name in PROVIDERS},
        "handoff_mode": steps_out[-1]["handoff"]["mode"] if steps_out else "scripted",
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
        lines.append(
            f"- {step['id']} intent={step['intent']} ok={step['ok']} "
            f"handoff={step['handoff']['mode']} :: {first}"
        )
    return "\n".join(lines)


def demo_playbook(workspace: Path, probes: Optional[Dict[str, Dict[str, Any]]] = None) -> str:
    report = run_playbook(builtin_playbook(), workspace, probes=probes)
    return format_report(report)
