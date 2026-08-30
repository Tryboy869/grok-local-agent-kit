"""Load kit settings from env + optional TOML/JSON config files."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional


CONFIG_FILENAMES = (
    "grok-agent.toml",
    "grok-agent.json",
    ".grok/config.toml",
    ".grok/config.json",
)


@dataclass
class KitConfig:
    model: str = "llama3.2"
    provider: str = "ollama"
    base_url: Optional[str] = None
    temperature: float = 0.3
    max_iterations: int = 12
    verbose: bool = False
    stream: bool = False
    use_router: bool = False
    attach_mcp: bool = False
    session_name: str = "default"
    tool_result_max_chars: int = 6000
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_agent_kwargs(self) -> Dict[str, Any]:
        return {
            "model": self.model,
            "provider": self.provider,
            "base_url": self.base_url,
            "temperature": self.temperature,
            "max_iterations": self.max_iterations,
            "verbose": self.verbose,
            "stream": self.stream,
            "use_router": self.use_router,
            "attach_mcp": self.attach_mcp,
            "session_name": self.session_name,
            "tool_result_max_chars": self.tool_result_max_chars,
        }


def _parse_toml(text: str) -> Dict[str, Any]:
    try:
        import tomllib
    except ModuleNotFoundError:  # pragma: no cover
        try:
            import tomli as tomllib  # type: ignore
        except ModuleNotFoundError:
            return {}
    return tomllib.loads(text)


def _read_file(path: Path) -> Dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        data = json.loads(raw)
        return data if isinstance(data, dict) else {}
    data = _parse_toml(raw)
    return data if isinstance(data, dict) else {}


def discover_config_path(start: Optional[Path] = None) -> Optional[Path]:
    here = (start or Path.cwd()).resolve()
    for base in [here, *here.parents]:
        for name in CONFIG_FILENAMES:
            candidate = base / name
            if candidate.is_file():
                return candidate
    env = os.environ.get("GROK_AGENT_CONFIG")
    if env:
        p = Path(env).expanduser()
        if p.is_file():
            return p
    return None


def load_config(path: Optional[str | Path] = None) -> KitConfig:
    data: Dict[str, Any] = {}
    found = Path(path).expanduser() if path else discover_config_path()
    if found and found.is_file():
        try:
            data = _read_file(found)
        except Exception:
            data = {}
        if isinstance(data.get("agent"), dict):
            data = {**data["agent"], **{k: v for k, v in data.items() if k != "agent"}}

    def _env(key: str, default: Any) -> Any:
        val = os.environ.get(key)
        return default if val is None or val == "" else val

    def _bool(v: Any, default: bool) -> bool:
        if v is None:
            return default
        if isinstance(v, bool):
            return v
        return str(v).strip().lower() in {"1", "true", "yes", "on"}

    cfg = KitConfig(
        model=str(_env("GROK_AGENT_MODEL", data.get("model", "llama3.2"))),
        provider=str(_env("GROK_AGENT_PROVIDER", data.get("provider", "ollama"))),
        base_url=_env("GROK_AGENT_BASE_URL", data.get("base_url")),
        temperature=float(data.get("temperature", 0.3)),
        max_iterations=int(data.get("max_iterations", 12)),
        verbose=_bool(data.get("verbose"), False),
        stream=_bool(data.get("stream"), False),
        use_router=_bool(_env("GROK_AGENT_ROUTER", data.get("use_router")), False),
        attach_mcp=_bool(data.get("attach_mcp"), False),
        session_name=str(data.get("session_name", "default")),
        tool_result_max_chars=int(data.get("tool_result_max_chars", 6000)),
        extra={k: v for k, v in data.items() if k not in KitConfig.__dataclass_fields__},
    )
    return cfg


DEFAULT_TOML = """# grok-agent.toml — local kit defaults (commit or keep private)
[agent]
model = "llama3.2"
provider = "ollama"
# base_url = "http://localhost:11434"
temperature = 0.3
max_iterations = 12
verbose = false
stream = false
use_router = false
attach_mcp = false
session_name = "default"
"""


def write_example_config(path: str | Path = "grok-agent.toml") -> Path:
    p = Path(path)
    if not p.parent.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        p.write_text(DEFAULT_TOML, encoding="utf-8")
    return p
