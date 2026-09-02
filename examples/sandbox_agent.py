#!/usr/bin/env python3
"""Demonstrate the restricted execute_python sandbox (no LLM required)."""

from grok_local_agent_kit.tools import execute_python

SNIPPETS = [
    "print(sum(range(10)))",
    "import math\nprint(round(math.pi, 4))",
    "import os",
    "print((1).__class__)",
]


def main() -> None:
    print("execute_python sandbox demo\n")
    for code in SNIPPETS:
        preview = code.replace("\n", " | ")
        print(f">>> {preview}")
        print(f"    {execute_python(code)}\n")


if __name__ == "__main__":
    main()
