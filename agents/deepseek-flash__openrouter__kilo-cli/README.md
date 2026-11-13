# deepseek-flash × OpenRouter × Kilo CLI — SNC_DISC_RESEARCH

> **Model:** `deepseek/deepseek-flash`
> **Provider:** OpenRouter (inferred from model-ID namespace + environment; see `00_MODEL/MODEL_PROVIDER.md`)
> **Harness:** Kilo CLI
> **Run:** 2026-11-13T08:46Z → 2026-11-13T~09:30Z
> **Task:** thorough ServiceNow Discovery configuration reference (Brazil release)

This folder is self-contained. It does not modify any other agent's folder.

## Read this first

| What | Where |
|---|---|
| Model/provider disclosure | [`00_MODEL/MODEL_PROVIDER.md`](00_MODEL/MODEL_PROVIDER.md) |
| Capability gate (browse? Playwright? context?) | [`SNC_DISC__WT1/00_PREREQ/PREREQ.md`](SNC_DISC__WT1/00_PREREQ/PREREQ.md) |
| Plan, risks, success criteria | [`SNC_DISC__WT1/01_PLAN/PLAN.md`](SNC_DISC__WT1/01_PLAN/PLAN.md) |
| Clarifications / blockers | [`SNC_DISC__WT1/02_CLARIFICATIONS/CLARIFY.md`](SNC_DISC__WT1/02_CLARIFICATIONS/CLARIFY.md) |
| Phase heartbeats | [`SNC_DISC__WT1/03_PHASES/`](SNC_DISC__WT1/03_PHASES/) |
| **Main deliverable** | [`SNC_DISC__WT1/05_FINAL/DISCOVERY_CONFIG_REFERENCE.md`](SNC_DISC__WT1/05_FINAL/DISCOVERY_CONFIG_REFERENCE.md) |
| Final summary | [`SNC_DISC__WT1/05_FINAL/FINAL_SUMMARY.md`](SNC_DISC__WT1/05_FINAL/FINAL_SUMMARY.md) |
| QA | [`SNC_DISC__WT1/04_QA/QA.md`](SNC_DISC__WT1/04_QA/QA.md) |
| Files / branch / worktree | [`SNC_DISC__WT1/06_FILESCOPE/FILESCOPE.md`](SNC_DISC__WT1/06_FILESCOPE/FILESCOPE.md) |
| Dated report + transcript | [`runs/2026-11-13T0846Z_deepseek-flash__openrouter__kilo-cli/REPORT.md`](runs/2026-11-13T0846Z_deepseek-flash__openrouter__kilo-cli/REPORT.md) |
| Sources and evidence | [`research/SOURCES.md`](research/SOURCES.md) |
| Parallel swarm harness | [`swarm/README.md`](swarm/README.md) |
| Swarm run results | [`swarm/ORCHESTRATION.md`](swarm/ORCHESTRATION.md) |

## What was built

1. **The research itself** — a 12-section, source-cited ServiceNow Discovery
   configuration reference covering:
   - end-to-end order of operations;
   - Discovery properties with exact names/defaults;
   - schedule form + run options + MID selection;
   - classifiers/patterns and the two identification paths;
   - IRE identification/reconciliation rules in depth;
   - duplicate prevention, detection, and remediation;
   - CI Class Manager navigation breadcrumbs and tab map;
   - validation, observability, risks, and clarifications.
2. **A working free-key swarm harness** — an OpenAI-compatible router, a
   concurrency/daily-quota/cost ledger with file locking, git-worktree manager,
   phase-gated agent runner, and parallel orchestrator. See `swarm/`.
3. **A real parallel dispatch** — three worker models in isolated worktrees:
   - `qwen3.5:4b` (Ollama, local)
   - `qwen2.5-coder:7b` (Ollama, local)
   - `google/gemma-4-31b-it:free` (OpenRouter, free tier)

## Reproduce

```bash
cd agents/deepseek-flash__openrouter__kilo-cli/swarm
python3 usage_tracker.py --status
python3 orchestrator.py --roster roster.json --repo /tmp/kilo/ALT_PARALLELSWARM
```

The harness refuses to over-subscribe a provider: it enforces `max_inflight`,
`daily_calls`, and `daily_tokens` per provider, and records estimated cost. It never
prints or stores API keys; only the environment-variable *name* is recorded.

## Scope boundary

This is a **configuration reference**, not a runbook for a specific customer network.
Values such as scan ranges, credentials, and schedule windows must be set from the
customer's own network facts. Every recommendation here is traceable to a ServiceNow
documentation page listed in `research/SOURCES.md`.
