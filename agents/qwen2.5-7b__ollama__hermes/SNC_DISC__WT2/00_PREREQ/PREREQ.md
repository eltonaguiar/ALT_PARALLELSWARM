# Pre-requisite check — qwen2.5-7b__ollama__hermes

Model: `qwen2.5:7b-instruct-q5_K_M`
Base URL: `http://localhost:11434/v1`

| capability | pass | evidence |
|---|---|---|
| Outbound HTTP | YES | HTTP 200 in 0.0s |
| Playwright + Chromium | YES | chromium 153.0.8010.12 |
| JavaScript rendering | YES | js output='after' |
| Web search reachable | YES | 36 servicenow.com results |
| Context window | YES | qwen2.5:7b-instruct-q5_K_M (ollama): 32768 tokens |

## Verdict

**CAN proceed with independent web research.** Browsing tools reachable and context is adequate.

## Backup plan if blocked

- Ask the orchestrator for a pre-fetched evidence digest (another agent's research output).
- Restrict output to structure/planning work that needs no live sources.
- Never fabricate URLs; mark unsourced claims as UNVERIFIED.
