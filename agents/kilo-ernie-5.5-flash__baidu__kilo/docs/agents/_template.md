# Agent Identity Template

Copy this file to `docs/agents/<provider>-<model>.md` when a new agent joins the swarm.

## Model / Provider (explicit)

| Field | Value |
|-------|-------|
| **Agent / worktree** | `WT<n>_<provider>-<model>` |
| **Model ID (exact)** | `provider/model:tag` |
| **Model family** | ... |
| **Provider / gateway** | ... |
| **Auth** | env var name (NEVER the secret value) |
| **Tier** | free / paid |
| **Context window** | ... |
| **Host runtime** | ... |
| **Created** | YYYY-MM-DD |

## Capability self-assessment (prerequisites)

Fill this from a real probe (`python -m swarm.capability_probe --model ...`), not a guess.

| Capability | Status | Evidence |
|------------|--------|----------|
| Web browse (search) | ? | |
| Web fetch | ? | |
| Headless browser (Playwright) | ? | |
| Large context window | ? | |
| File / shell access | ? | |

## Assigned task

## Output contract