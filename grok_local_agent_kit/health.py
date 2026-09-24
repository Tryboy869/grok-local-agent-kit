"""Per-backend circuit breaker for local LLM endpoints.

Closed → traffic allowed.
Open → traffic denied until cooldown elapses, then half-open.
Half-open → one probe; success closes, failure re-opens.

No network. No LLM. Persist to a cwd-safe JSON file.
"""

from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Union

PathLike = Union[str, Path]

CLOSED = "closed"
OPEN = "open"
HALF_OPEN = "half_open"


def _safe_path(path: PathLike) -> Path:
    p = Path(path).expanduser()
    if not p.is_absolute():
        p = Path.cwd() / p
    p = p.resolve()
    cwd = Path.cwd().resolve()
    try:
        p.relative_to(cwd)
    except ValueError as exc:
        raise ValueError(f"path escapes workspace: {p}") from exc
    return p


@dataclass
class BreakerState:
    name: str
    state: str = CLOSED
    failures: int = 0
    successes: int = 0
    opened_at: float = 0.0
    last_error: str = ""
    threshold: int = 3
    cooldown_s: float = 30.0

    def allow(self, now: Optional[float] = None) -> bool:
        now = time.time() if now is None else now
        if self.state == CLOSED:
            return True
        if self.state == OPEN:
            if now - self.opened_at >= self.cooldown_s:
                self.state = HALF_OPEN
                return True
            return False
        return True

    def record_success(self) -> None:
        self.successes += 1
        self.failures = 0
        self.state = CLOSED
        self.last_error = ""

    def record_failure(self, error: str = "", now: Optional[float] = None) -> None:
        now = time.time() if now is None else now
        self.failures += 1
        self.last_error = error or self.last_error
        if self.state == HALF_OPEN or self.failures >= self.threshold:
            self.state = OPEN
            self.opened_at = now


@dataclass
class HealthBoard:
    breakers: Dict[str, BreakerState] = field(default_factory=dict)
    threshold: int = 3
    cooldown_s: float = 30.0

    def breaker(self, name: str) -> BreakerState:
        if name not in self.breakers:
            self.breakers[name] = BreakerState(
                name=name, threshold=self.threshold, cooldown_s=self.cooldown_s
            )
        return self.breakers[name]

    def allow(self, name: str, now: Optional[float] = None) -> bool:
        return self.breaker(name).allow(now=now)

    def success(self, name: str) -> BreakerState:
        b = self.breaker(name)
        b.record_success()
        return b

    def failure(self, name: str, error: str = "", now: Optional[float] = None) -> BreakerState:
        b = self.breaker(name)
        b.record_failure(error=error, now=now)
        return b

    def trip(self, name: str, error: str = "manual trip", now: Optional[float] = None) -> BreakerState:
        b = self.breaker(name)
        b.failures = max(b.failures, b.threshold)
        b.record_failure(error=error, now=now)
        return b

    def reset(self, name: str) -> BreakerState:
        b = self.breaker(name)
        b.state = CLOSED
        b.failures = 0
        b.opened_at = 0.0
        b.last_error = ""
        return b

    def rows(self) -> List[dict]:
        out = []
        for name in sorted(self.breakers):
            b = self.breakers[name]
            out.append(
                {
                    "name": b.name,
                    "state": b.state,
                    "failures": b.failures,
                    "successes": b.successes,
                    "last_error": b.last_error,
                    "allow": b.allow(),
                }
            )
        return out


def save_board(board: HealthBoard, path: PathLike) -> Path:
    dest = _safe_path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "threshold": board.threshold,
        "cooldown_s": board.cooldown_s,
        "breakers": {k: asdict(v) for k, v in board.breakers.items()},
    }
    dest.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return dest


def load_board(path: PathLike) -> HealthBoard:
    src = _safe_path(path)
    if not src.exists():
        return HealthBoard()
    data = json.loads(src.read_text(encoding="utf-8"))
    board = HealthBoard(
        threshold=int(data.get("threshold") or 3),
        cooldown_s=float(data.get("cooldown_s") or 30.0),
    )
    for name, raw in (data.get("breakers") or {}).items():
        board.breakers[name] = BreakerState(
            name=str(raw.get("name") or name),
            state=str(raw.get("state") or CLOSED),
            failures=int(raw.get("failures") or 0),
            successes=int(raw.get("successes") or 0),
            opened_at=float(raw.get("opened_at") or 0.0),
            last_error=str(raw.get("last_error") or ""),
            threshold=int(raw.get("threshold") or board.threshold),
            cooldown_s=float(raw.get("cooldown_s") or board.cooldown_s),
        )
    return board


def format_board(board: HealthBoard) -> str:
    rows = board.rows()
    if not rows:
        return "health: (empty)"
    lines = ["health board:"]
    for r in rows:
        flag = "ok" if r["allow"] else "block"
        err = f" err={r['last_error']}" if r["last_error"] else ""
        lines.append(
            f"- {r['name']}: {r['state']} allow={flag} fail={r['failures']} ok={r['successes']}{err}"
        )
    return "\n".join(lines)


def demo_health(path: PathLike = "health.json") -> str:
    """Deterministic offline story: ollama stays closed, lmstudio trips then cools."""
    board = HealthBoard(threshold=2, cooldown_s=0.01)
    board.success("ollama")
    board.failure("lmstudio", "connection refused")
    board.failure("lmstudio", "connection refused")
    time.sleep(0.02)
    assert board.allow("lmstudio") is True
    board.failure("lmstudio", "still down")
    dest = save_board(board, path)
    loaded = load_board(dest)
    return format_board(loaded)
