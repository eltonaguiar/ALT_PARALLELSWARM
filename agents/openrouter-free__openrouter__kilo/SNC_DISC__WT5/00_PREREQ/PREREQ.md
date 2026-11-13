# Pre-requisite check — openrouter-free__openrouter__kilo

Model: `openrouter.free`
Base URL: `https://openrouter.ai/api/v1`

| capability | pass | evidence |
|---|---|---|
| Outbound HTTP | YES | HTTP 200 in 0.0s |
| Playwright + Chromium | YES | chromium 153.0.8010.12 |
| JavaScript rendering | YES | js output='after' |
| Web search reachable | YES | Bing/Startpage reachability verified |
| Context window | YES | openrouter.free (api, assessed): 128000 tokens |

## Verdict

**CAN proceed with independent web research.** Browsing tools reachable and context is adequate.

## Backup plan if blocked

- Ask the orchestrator for a pre-fetched evidence digest (another agent's research output).
- Restrict output to structure/planning work that needs no live sources.
- Never fabricate URLs; mark unsourced claims as UNVERIFIED.