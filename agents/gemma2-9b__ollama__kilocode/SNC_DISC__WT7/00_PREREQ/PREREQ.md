# Pre-requisite check — gemma2-9b__ollama__kilocode

Model: `gemma2:9b`
Base URL: `http://localhost:11434/v1`

| capability | pass | evidence |
|---|---|---|
| Outbound HTTP | YES | HTTP 200 in 0.0s |
| Playwright + Chromium | YES | chromium 153.0.8010.12 |
| JavaScript rendering | YES | js output='after' |
| Web search reachable | YES | 32 servicenow.com results |
| Context window | NO | gemma2:9b (ollama): 8192 tokens |

## Verdict

**CANNOT browse independently.** Per instructions, this agent must (a) state the blocker here, (b) write a backup request in `02_CLARIFICATIONS/`, and (c) fall back to answering from supplied evidence rather than pretending to research.

## Backup plan if blocked

- Ask the orchestrator for a pre-fetched evidence digest (another agent's research output).
- Restrict output to structure/planning work that needs no live sources.
- Never fabricate URLs; mark unsourced claims as UNVERIFIED.
