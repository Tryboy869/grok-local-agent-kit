# 90-day growth plan (no cheating)

Goal: 10k GitHub stars in ~90 days is **extremely hard** for a new toolkit from an account with ~9 followers. Treat 10k as a stretch north star. The plan below is the only honest path.

## Reality check

| Signal today | Value |
|--------------|-------|
| Stars | 0 |
| Forks | 0 |
| Followers on owner account | 9 |
| Product | real Python kit, tests, CLI, MCP |

Buying stars, star-for-star groups, or bot farms will get the repo flagged and is explicitly out of scope.

## What actually moves stars

1. A 15-second demo people can paste.
2. A README that answers "why not LangChain / CrewAI / smolagents?" in one screen.
3. Weekly shipping so HN / Reddit / X posts have a *new* hook.
4. Fast issue response. First-time contributors who land a GIF or test stay.
5. Being useful in someone else's blog post or YouTube video.

## Week-by-week (repeat)

### Every Monday
- Tag a minor release if there is a real feature.
- Update CHANGELOG + README version badge.
- Record or refresh one GIF (`docs/gifs/`).

### Every Wednesday
- One technical post: X thread + Dev.to / Hashnode. Show a command and output, not slogans.

### Every Friday
- Close or triage every open issue.
- Add one `good first issue` if the queue is empty.

### Launch windows (do not spam)
- Show HN: once, when GIF #1 exists. Title in SHOW_HN.md.
- r/LocalLLaMA, r/ollama, r/MachineLearning (if the post is a *demo*, not an ad).
- HN "Who is hiring" is the wrong thread. "Show HN" and "Ask HN: what should a local agent kit include?" are the right ones.

## Product bets that earn stars

- Publish to PyPI (`pip install grok-local-agent-kit`) — git+https is a conversion killer.
- One 20s GIF above the fold.
- `grok-agent doctor` should tell a first-time user exactly what to install.
- Compare table vs LiteLLM + LangGraph + smolagents (honest: we are smaller, local-first).
- Optional: GitHub Pages docs site.

## Metrics to watch (weekly)

- Unique clones + visitors (Insights → Traffic)
- Stars / forks / unique cloners
- Issues opened by non-owner
- PyPI downloads (after publish)

If traffic is zero after two honest Show HN + r/LocalLLaMA posts, the problem is positioning or missing demo — not "need more features."
