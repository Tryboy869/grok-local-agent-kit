"""Session pack: batch the offline MVP across chat, automation, search, and MCP.

No model socket is opened. Provider probes are optional and never fail the run.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from .mvp import probe_providers, run_mvp

SearchFn = Callable[[str], str]

DEFAULT_GOALS: List[Dict[str, str]] = [
    {
        "id": "chat",
        "role": "chat",
        "prompt": "compute sqrt(144) + 10",
    },
    {
        "id": "automation",
        "role": "automation",
        "prompt": "write a note that the local agent ran",
    },
    {
        "id": "research",
        "role": "research",
        "prompt": "search local AI agents",
    },
    {
        "id": "mcp",
        "role": "mcp",
        "prompt": "mcp echo ping from the session pack",
    },
]


def load_pack(path: Path) -> List[Dict[str, str]]:
    """Load a JSON list of {id, role, prompt} goals."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("goals") or []
    goals: List[Dict[str, str]] = []
    for item in data:
        if not isinstance(item, dict) or not item.get("prompt"):
            continue
        goals.append(
            {
                "id": str(item.get("id") or f"goal-{len(goals)+1}"),
                "role": str(item.get("role") or "task"),
                "prompt": str(item["prompt"]),
            }
        )
    if not goals:
        raise ValueError(f"no goals in {path}")
    return goals


def run_pack(
    goals: List[Dict[str, str]],
    workspace: Path,
    search: Optional[SearchFn] = None,
    probes: Optional[Dict[str, Dict[str, Any]]] = None,
    probe: bool = False,
) -> Dict[str, Any]:
    """Route and execute each goal. Writes pack-report.json and SESSION.md."""
    workspace = Path(workspace)
    workspace.mkdir(parents=True, exist_ok=True)
    search = search or (lambda q: f"1. local agents\n2. ollama\n3. {q}")
    if probes is None and probe:
        probes = probe_providers(timeout=0.4)
    provider_table = probes or {
        "ollama": {"status": "not-probed"},
        "lmstudio": {"status": "not-probed"},
    }
    results: List[Dict[str, Any]] = []
    for goal in goals:
        outcome = run_mvp(goal["prompt"], workspace, search=search)
        results.append(
            {
                "id": goal.get("id"),
                "role": goal.get("role"),
                "prompt": goal["prompt"],
                "intent": outcome["intent"],
                "ok": outcome["ok"],
                "answer": outcome["answer"],
                "tools": [step["tool"] for step in outcome["steps"]],
            }
        )
    report = {
        "kit": "grok-local-agent-kit",
        "version": "0.48.0",
        "goals": len(results),
        "ok": all(item["ok"] for item in results) if results else False,
        "providers": provider_table,
        "results": results,
    }
    (workspace / "pack-report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (workspace / "SESSION.md").write_text(format_brief(report), encoding="utf-8")
    return report


def format_brief(report: Dict[str, Any]) -> str:
    lines = [
        "# Session pack",
        "",
        f"Kit {report.get('version')} · goals {report.get('goals')} · ok {report.get('ok')}",
        "",
        "## Providers",
        "",
    ]
    for name, spec in (report.get("providers") or {}).items():
        status = spec.get("status") if isinstance(spec, dict) else spec
        lines.append(f"- {name}: {status}")
    lines.extend(["", "## Goals", ""])
    for item in report.get("results") or []:
        answer = str(item.get("answer") or "").strip().splitlines()
        preview = answer[0] if answer else ""
        lines.append(
            f"- **{item.get('id')}** ({item.get('role')}) intent=`{item.get('intent')}` "
            f"tools={','.join(item.get('tools') or [])} ok={item.get('ok')}"
        )
        if preview:
            lines.append(f"  - {preview[:180]}")
    lines.append("")
    return "\n".join(lines)


def demo_pack(workspace: Path, search: Optional[SearchFn] = None) -> str:
    """Offline chat + automation + search + MCP pack. No network."""
    report = run_pack(DEFAULT_GOALS, workspace, search=search, probe=False)
    return format_brief(report)
