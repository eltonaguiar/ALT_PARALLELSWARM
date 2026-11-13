# Pre-requisites — qwen2.5-coder-7b__ollama__alt-swarm

**Model:** `qwen2.5-coder:7b`
**Provider:** `ollama`
**Harness:** ALT_PARALLELSWARM `swarm/agent_runner.py`
**Checked:** 2026-11-13T08:58:13+00:00

| Capability | Result | Consequence |
|---|---|---|
| Native browser tools | NO (worker is API-dispatched) | Cannot browse independently |
| Playwright / shell | NO (no tool loop) | Cannot fetch or verify pages |
| Pre-fetched evidence digest | YES | Write from the supplied evidence only |
| Context window | provider/model dependent | Digest capped at 17000 chars |

## Verdict

**CONDITIONAL PASS.** This worker does not browse. It is intentionally given a
pre-fetched, source-marked evidence digest produced by the orchestrator's own research
(the backup plan required by the task contract). Any claim not present in the digest must
be marked as a gap.
