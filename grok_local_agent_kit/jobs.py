"""File-backed job ledger for local automation.

Jobs point at declarative workflows (file ops, injectable search, MCP echo).
A tick runs only what is due. Clock is injectable so tests never sleep.
No daemon and no live LLM required.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from .workflow import Workflow, run_workflow

SearchFn = Callable[[str], str]
McpFn = Callable[[str, Dict[str, Any]], str]


@dataclass
class JobSpec:
    name: str
    every_s: float
    workflow: Dict[str, Any]
    enabled: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "every_s": self.every_s,
            "enabled": self.enabled,
            "workflow": self.workflow,
        }


@dataclass
class JobLedger:
    jobs: List[JobSpec] = field(default_factory=list)
    runs: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    path: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {"jobs": [job.to_dict() for job in self.jobs]}

    def state_dict(self) -> Dict[str, Any]:
        return {"runs": self.runs}


def load_ledger(path: str | Path) -> JobLedger:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    jobs = []
    for raw in data.get("jobs") or []:
        if "workflow" not in raw:
            raise ValueError(f"job {raw.get('name')!r} needs a workflow")
        jobs.append(
            JobSpec(
                name=str(raw["name"]),
                every_s=float(raw.get("every_s") or 60),
                workflow=dict(raw["workflow"]),
                enabled=bool(raw.get("enabled", True)),
            )
        )
    ledger = JobLedger(jobs=jobs, path=str(path))
    state_path = Path(path).with_name("jobs-state.json")
    if state_path.is_file():
        state = json.loads(state_path.read_text(encoding="utf-8"))
        ledger.runs = dict(state.get("runs") or {})
    return ledger


def save_ledger(ledger: JobLedger, path: str | Path) -> Path:
    target = Path(path)
    target.write_text(json.dumps(ledger.to_dict(), indent=2) + "\n", encoding="utf-8")
    ledger.path = str(target)
    return target


def save_state(ledger: JobLedger, path: str | Path | None = None) -> Path:
    if path is None:
        if not ledger.path:
            raise ValueError("ledger has no path; pass path=")
        path = Path(ledger.path).with_name("jobs-state.json")
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(ledger.state_dict(), indent=2) + "\n", encoding="utf-8")
    return target


def due(ledger: JobLedger, now: float) -> List[JobSpec]:
    ready: List[JobSpec] = []
    for job in ledger.jobs:
        if not job.enabled:
            continue
        last = float((ledger.runs.get(job.name) or {}).get("last_run") or 0)
        if now - last >= job.every_s:
            ready.append(job)
    return ready


def tick(
    ledger: JobLedger,
    workspace: str | Path,
    *,
    now: float,
    search: Optional[SearchFn] = None,
    mcp: Optional[McpFn] = None,
    persist: bool = False,
) -> Dict[str, Any]:
    """Run every due job once. `now` is required so callers control time."""
    fired = []
    for job in due(ledger, now):
        result = run_workflow(Workflow(
            name=str(job.workflow.get("name") or job.name),
            steps=list(job.workflow.get("steps") or []),
            meta=dict(job.workflow.get("meta") or {}),
        ), workspace, search=search, mcp=mcp)
        previous = int((ledger.runs.get(job.name) or {}).get("runs") or 0)
        ledger.runs[job.name] = {
            "last_run": now,
            "runs": previous + 1,
            "last_ok": bool(result.get("ok")),
            "last_steps": result.get("steps"),
        }
        fired.append({"name": job.name, "ok": result.get("ok"), "steps": result.get("steps")})
    if persist:
        save_state(ledger)
    return {
        "ok": all(item["ok"] for item in fired) if fired else True,
        "fired": [item["name"] for item in fired],
        "results": fired,
        "skipped": [job.name for job in ledger.jobs if job.name not in {item["name"] for item in fired}],
    }


def demo_jobs(workspace: Optional[Path] = None) -> str:
    """One due digest job writes a note. A second tick at the same clock is a no-op."""
    import tempfile

    root = workspace or Path(tempfile.mkdtemp(prefix="glak-jobs-"))
    root.mkdir(parents=True, exist_ok=True)
    (root / "inbox.txt").write_text("local agent inbox\n", encoding="utf-8")
    ledger = JobLedger(jobs=[
        JobSpec(
            name="inbox-digest",
            every_s=3600,
            workflow={
                "name": "inbox-digest",
                "steps": [
                    {"tool": "list_files", "arguments": {"path": "."}, "save_as": "listing"},
                    {
                        "tool": "write_file",
                        "arguments": {
                            "path": "digest.txt",
                            "content": "automation digest\n{{listing}}\n",
                        },
                    },
                    {
                        "tool": "web_search",
                        "arguments": {"query": "ollama lm studio"},
                    },
                ],
            },
        )
    ])

    def fixture_search(query: str) -> str:
        return f"offline hit for {query}"

    first = tick(ledger, root, now=1_700_000_000, search=fixture_search)
    second = tick(ledger, root, now=1_700_000_000, search=fixture_search)
    wrote = (root / "digest.txt").is_file()
    lines = [
        f"jobs ok={first['ok']} fired={','.join(first['fired']) or '-'} wrote={wrote}",
        f"second_tick fired={','.join(second['fired']) or '-'} skipped={','.join(second['skipped'])}",
        "providers=ollama,lmstudio (routing unchanged; jobs do not call them)",
        "tools=list_files,write_file,web_search",
    ]
    if workspace is None:
        lines.append(f"workspace={root}")
    return "\n".join(lines)
