# Pre-requisite check — phi4-mini__ollama__kilocode

Model: `phi4-mini:latest`
Base URL: `http://localhost:11434/v1`

| capability | pass | evidence |
|---|---|---|
| Outbound HTTP | YES | HTTP 200 in 0.0s |
| Playwright + Chromium | YES | chromium 153.0.8010.12 |
| JavaScript rendering | YES | js output='after' |
| Web search reachable | YES | 40 servicenow.com results |
| Context window | YES | phi4-mini:latest (ollama): 131072 tokens |

## Verdict

**CAN proceed with independent web research.** Browsing tools reachable and context is adequate.

## Backup plan if blocked

- Ask the orchestrator for a pre-fetched evidence digest (another agent's research output).
- Restrict output to structure/planning work that needs no live sources.
- Never fabricate URLs; mark unsourced claims as UNVERIFIED.
