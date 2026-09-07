#!/usr/bin/env python3
"""Parse messy LLM-ish text into JSON (no live LLM required)."""

from grok_local_agent_kit.structured import extract_json, require_keys

SAMPLE = '''
Sure — here is the plan:

```json
{"task": "summarize logs", "priority": 2, "done": false}
```
'''


def main() -> None:
    payload = extract_json(SAMPLE)
    require_keys(payload, ["task", "priority"])
    print(payload)


if __name__ == "__main__":
    main()
