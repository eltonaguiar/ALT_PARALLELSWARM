# File scope

**Agent:** `deepseek-flash__openrouter__kilo-cli`
**Model:** `deepseek/deepseek-flash` · **Provider:** OpenRouter (inferred) · **Harness:** Kilo CLI
**Task:** `SNC_DISC_RESEARCH`

## Git identity

| Field | Value |
|---|---|
| Repository | `https://github.com/eltonaguiar/ALT_PARALLELSWARM` |
| Self-run worktree | `/tmp/kilo/ALT_PARALLELSWARM` (clone of the target repo) |
| Self branch | `agent/deepseek-flash__openrouter__kilo-cli` |
| Worker worktrees | `/tmp/kilo/wt-qwen3.5-4b__ollama__alt-swarm`, `/tmp/kilo/wt-qwen2.5-coder-7b__ollama__alt-swarm`, `/tmp/kilo/wt-particle-1__openrouter__alt-swarm` |
| Worker branches | `agent/qwen3.5-4b__ollama__alt-swarm`, `agent/qwen2.5-coder-7b__ollama__alt-swarm`, `agent/particle-1__openrouter__alt-swarm` |

## Files written (this folder only)

```
agents/deepseek-flash__openrouter__kilo-cli/
├── README.md
├── 00_MODEL/MODEL_PROVIDER.md
├── research/
│   ├── SOURCES.md
│   ├── topics.json
│   ├── EXCERPTS.md
│   └── raw/README.md
├── SNC_DISC__WT1/
│   ├── 00_PREREQ/PREREQ.md
│   ├── 01_PLAN/PLAN.md
│   ├── 02_CLARIFICATIONS/CLARIFY.md
│   ├── 03_PHASES/phase0..phase7
│   ├── 04_QA/QA.md
│   ├── 05_FINAL/DISCOVERY_CONFIG_REFERENCE.md
│   ├── 05_FINAL/FINAL_SUMMARY.md
│   └── 06_FILESCOPE/FILESCOPE.md
├── swarm/
│   ├── README.md
│   ├── registry.json
│   ├── roster.json
│   ├── usage_tracker.py
│   ├── router.py
│   ├── worktree_manager.py
│   ├── agent_runner.py
│   ├── orchestrator.py
│   ├── ORCHESTRATION.md
│   ├── evidence/options.md, duplicates.md, classmanager.md
│   └── state/ (ledger + logs; see note)
└── runs/2026-11-13T0846Z_deepseek-flash__openrouter__kilo-cli/REPORT.md
```

## Shared files touched outside the folder

Only the append-only registry entries required by the repo contract:

- `CONTRIBUTORS.md` — one row per agent folder.
- `agents.yaml` — `self_runs:` entry for this agent plus a non-dispatched
  `alt_swarm_workers:` note.

No other agent's folder is modified.

## State files

`swarm/state/` contains the run ledger and logs. The ledger records provider counters,
not secrets. Logs contain model output and error messages. They are useful evidence of
the free-tier 429 and the recovery path, so they are committed. API keys are never
written.
