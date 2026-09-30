"""v0.41 — bind Catalog.pick() onto MultiLLMRouter endpoint models."""

from __future__ import annotations

from typing import Iterable, List, Optional, Tuple

from .catalog import Catalog, ModelEntry
from .router import LLMEndpoint, MultiLLMRouter

Change = Tuple[str, str, str]  # name, old_model, new_model


def _catalog_provider(ep: LLMEndpoint) -> str:
    if ep.name == "lmstudio" or ep.provider in {"openai", "lmstudio"}:
        return "lmstudio"
    return ep.provider or "ollama"


def apply_catalog(
    router: MultiLLMRouter,
    catalog: Catalog,
    prefer: Optional[str] = None,
) -> List[Change]:
    """Rewrite endpoint.model from Catalog.pick for each backend.

    Cached LLMClient instances for changed endpoints are dropped so the
    next pick() uses the discovered name. Endpoints with no catalog hit
    keep their previous model.
    """
    changes: List[Change] = []
    for ep in router.chain:
        provider = _catalog_provider(ep)
        picked: ModelEntry | None = catalog.pick(provider, prefer=prefer)
        if picked is None:
            continue
        old = ep.model
        if old == picked.name:
            continue
        ep.model = picked.name
        router._clients.pop(ep.name, None)
        if router.active is ep:
            router.active = None
        changes.append((ep.name, old, picked.name))
    return changes


def chain_models(router: MultiLLMRouter) -> list[dict[str, str]]:
    return [
        {"name": ep.name, "provider": ep.provider, "model": ep.model}
        for ep in router.chain
    ]


def demo_catalog_route(
    catalog: Optional[Catalog] = None,
    prefer: Optional[str] = "llama3.2",
    chain: Optional[Iterable[LLMEndpoint]] = None,
) -> str:
    """Offline story: placeholder models become catalog picks."""
    if catalog is None:
        catalog = Catalog(
            created_at="2026-09-30T00:00:00Z",
            backends={
                "ollama": {"reachable": True, "count": 2},
                "lmstudio": {"reachable": True, "count": 1},
            },
            models=[
                ModelEntry(provider="ollama", name="llama3.2:latest", size=2048),
                ModelEntry(provider="ollama", name="nomic-embed-text", size=512),
                ModelEntry(provider="lmstudio", name="qwen2.5-7b"),
            ],
        )
    router = MultiLLMRouter(chain=chain, sticky=False)
    before = chain_models(router)
    changes = apply_catalog(router, catalog, prefer=prefer)
    after = chain_models(router)
    lines = ["catalog-route"]
    lines.append("before:")
    for row in before:
        lines.append(f"  {row['name']} model={row['model']}")
    lines.append("changes:")
    if not changes:
        lines.append("  (none)")
    for name, old, new in changes:
        lines.append(f"  {name}: {old} -> {new}")
    lines.append("after:")
    for row in after:
        lines.append(f"  {row['name']} model={row['model']}")
    picked = catalog.pick("ollama", prefer=prefer)
    if picked:
        lines.append(f"pick(ollama, prefer={prefer})={picked.name}")
    return "\n".join(lines) + "\n"
