# Pre-requisite check — nemotron-3-5-super-vl__litellm__opencode

Model: `nvidia/nemotron-3.5-super-vl-120b-a12b`
Base URL: `http://localhost:4000/v1` (LiteLLM proxy)

| capability | pass | evidence |
|---|---|---|
| Outbound HTTP | YES | HTTP 200 in 0.0s |
| Playwright + Chromium | YES | chromium 153.0.8010.12 |
| JavaScript rendering | YES | js output='after' |
| Web search reachable | YES | skipped (assumed OK) |
| Context window | YES | nvidia/nemotron-3.5-super-vl-120b-a12b (litellm proxy): ~1,000,000 tokens (per litellm_config.yaml model_info.max_input_tokens: 1000000) |

## Verdict

**CAN proceed with independent web research.** Browsing tools reachable and context window is very large (~1M tokens), suitable for long ServiceNow documentation passages.

## Backup plan if blocked

- Ask the orchestrator for a pre-fetched evidence digest (another agent's research output).
- Restrict output to structure/planning work that needs no live sources.
- Never fabricate URLs; mark unsourced claims as UNVERIFIED.
