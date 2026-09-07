#!/usr/bin/env python3
"""Run a TOML recipe of built-in tools (no live LLM required)."""

from pathlib import Path

from grok_local_agent_kit.recipes import format_results, load_recipe, run_recipe

HERE = Path(__file__).resolve().parent
RECIPE = HERE / "recipes" / "workspace.toml"


def main() -> None:
    recipe = load_recipe(RECIPE)
    print(f"# {recipe.name}\n{recipe.description}\n")
    print(format_results(run_recipe(recipe)))


if __name__ == "__main__":
    main()
