"""v0.40 — local model catalog (Ollama + LM Studio).

Discovers installed models through injectable HTTP probes so tests never
touch a live daemon. Writes catalog.json next to the cwd.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

Fetch = Callable[[str, float], Any]

OLLAMA_TAGS = "http://127.0.0.1:11434/api/tags"
LMSTUDIO_MODELS = "http://127.0.0.1:1234/v1/models"


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _cwd_safe(path: str | Path) -> Path:
    p = Path(path).expanduser()
    if not p.is_absolute():
        p = Path.cwd() / p
    return p.resolve()


@dataclass
class ModelEntry:
    provider: str
    name: str
    size: int | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    def key(self) -> str:
        return f"{self.provider}:{self.name}"


@dataclass
class Catalog:
    created_at: str
    backends: dict[str, dict[str, Any]] = field(default_factory=dict)
    models: list[ModelEntry] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "created_at": self.created_at,
            "backends": self.backends,
            "models": [asdict(m) for m in self.models],
        }

    def dumps(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False) + "\n"

    def names(self, provider: str | None = None) -> list[str]:
        rows = self.models
        if provider:
            rows = [m for m in rows if m.provider == provider]
        return [m.name for m in rows]

    def pick(self, provider: str | None = None, prefer: str | None = None) -> ModelEntry | None:
        rows = self.models
        if provider:
            rows = [m for m in rows if m.provider == provider]
        if not rows:
            return None
        if prefer:
            for m in rows:
                if m.name == prefer or m.name.startswith(prefer):
                    return m
        return rows[0]


def _default_fetch(url: str, timeout: float) -> Any:
    import httpx

    r = httpx.get(url, timeout=timeout)
    r.raise_for_status()
    return r.json()


def _parse_ollama(payload: Any) -> list[ModelEntry]:
    models = []
    if isinstance(payload, dict):
        raw = payload.get("models") or []
    elif isinstance(payload, list):
        raw = payload
    else:
        raw = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name") or item.get("model") or "").strip()
        if not name:
            continue
        size = item.get("size")
        models.append(
            ModelEntry(
                provider="ollama",
                name=name,
                size=int(size) if isinstance(size, int) else None,
                extra={"digest": item.get("digest"), "modified_at": item.get("modified_at")},
            )
        )
    return models


def _parse_lmstudio(payload: Any) -> list[ModelEntry]:
    models = []
    if isinstance(payload, dict):
        raw = payload.get("data") or payload.get("models") or []
    elif isinstance(payload, list):
        raw = payload
    else:
        raw = []
    for item in raw:
        if isinstance(item, str):
            name = item.strip()
            extra: dict[str, Any] = {}
        elif isinstance(item, dict):
            name = str(item.get("id") or item.get("name") or "").strip()
            extra = {"owned_by": item.get("owned_by")}
        else:
            continue
        if not name:
            continue
        models.append(ModelEntry(provider="lmstudio", name=name, extra=extra))
    return models


def probe_backend(
    name: str,
    url: str,
    parser,
    *,
    fetch: Fetch | None = None,
    timeout: float = 1.5,
) -> tuple[dict[str, Any], list[ModelEntry]]:
    fetcher = fetch or _default_fetch
    try:
        payload = fetcher(url, timeout)
        models = parser(payload)
        return {"reachable": True, "url": url, "count": len(models)}, models
    except Exception as exc:
        return {"reachable": False, "url": url, "error": str(exc), "count": 0}, []


def collect(
    *,
    fetch: Fetch | None = None,
    ollama_url: str = OLLAMA_TAGS,
    lmstudio_url: str = LMSTUDIO_MODELS,
    timeout: float = 1.5,
) -> Catalog:
    backends: dict[str, dict[str, Any]] = {}
    models: list[ModelEntry] = []
    info, rows = probe_backend("ollama", ollama_url, _parse_ollama, fetch=fetch, timeout=timeout)
    backends["ollama"] = info
    models.extend(rows)
    info, rows = probe_backend(
        "lmstudio", lmstudio_url, _parse_lmstudio, fetch=fetch, timeout=timeout
    )
    backends["lmstudio"] = info
    models.extend(rows)
    return Catalog(created_at=_now(), backends=backends, models=models)


def write_catalog(path: str | Path = "catalog.json", catalog: Catalog | None = None, **kwargs: Any) -> Path:
    dest = _cwd_safe(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    cat = catalog if catalog is not None else collect(**kwargs)
    dest.write_text(cat.dumps(), encoding="utf-8")
    return dest


def load_catalog(path: str | Path = "catalog.json") -> Catalog:
    p = _cwd_safe(path)
    data = json.loads(p.read_text(encoding="utf-8"))
    models = [ModelEntry(**m) for m in data.get("models") or []]
    return Catalog(
        created_at=str(data.get("created_at") or ""),
        backends=dict(data.get("backends") or {}),
        models=models,
    )


def format_catalog(cat: Catalog | None = None, **kwargs: Any) -> str:
    if cat is None:
        cat = collect(**kwargs)
    lines = [f"model-catalog {cat.created_at} models={len(cat.models)}"]
    for name, info in cat.backends.items():
        flag = "up" if info.get("reachable") else "down"
        extra = f" count={info.get('count', 0)}"
        err = info.get("error")
        if err:
            extra += f" err={err}"
        lines.append(f"  {name}: {flag}{extra}")
    for m in cat.models:
        size = f" size={m.size}" if m.size is not None else ""
        lines.append(f"    {m.provider}:{m.name}{size}")
    if not cat.models:
        lines.append("    (no models — backends down or empty)")
    return "\n".join(lines)


def demo_catalog(
    path: str = "catalog.json",
    *,
    fetch: Fetch | None = None,
) -> str:
    cat = collect(fetch=fetch)
    dest = write_catalog(path, catalog=cat)
    loaded = load_catalog(dest)
    return f"wrote={dest}\n{format_catalog(loaded)}\n"
