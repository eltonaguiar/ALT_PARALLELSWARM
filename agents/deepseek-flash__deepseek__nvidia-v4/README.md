# `deepseek-flash__deepseek__nvidia-v4`

**Model:** `deepseek-flash` · **Provider:** `deepseek` · **Harness:** Kilo CLI ·
**Worktree:** `nvidia-v4` · **Branch:** `agent/deepseek-flash__deepseek__nvidia-v4`

This is the `nvidia-v4` worktree's contribution to the shared `ALT_PARALLELSWARM`
experiment. It owns one task worktree: `SNC_DISC__WT1` (ServiceNow Discovery research).

## Read in this order

1. [`00_MODEL_AND_PROVENANCE.md`](00_MODEL_AND_PROVENANCE.md) — model/provider, what is mine, honesty notes.
2. [`SNC_DISC__WT1/00_PREREQ/PREREQ.md`](SNC_DISC__WT1/00_PREREQ/PREREQ.md) — capability gate + the working docs retrieval recipe.
3. [`SNC_DISC__WT1/01_PLAN/PLAN.md`](SNC_DISC__WT1/01_PLAN/PLAN.md) — goal, phases, risks, success criteria.
4. [`SNC_DISC__WT1/05_FINAL/DISCOVERY_CONFIG_REFERENCE.md`](SNC_DISC__WT1/05_FINAL/DISCOVERY_CONFIG_REFERENCE.md) — **main deliverable**.
5. [`SNC_DISC__WT1/05_FINAL/FINAL_SUMMARY.md`](SNC_DISC__WT1/05_FINAL/FINAL_SUMMARY.md) — result, blockers, clarifications.
6. [`SNC_DISC__WT1/04_QA/QA.md`](SNC_DISC__WT1/04_QA/QA.md) — self-check and external-review disposition.
7. [`SNC_DISC__WT1/nvidia_v4_swarm/README.md`](SNC_DISC__WT1/nvidia_v4_swarm/README.md) — reusable parallel-model runner + usage ledger.

## Layout

```
SNC_DISC__WT1/
  00_PREREQ/          capability gate, retrieval recipe
  01_PLAN/            plan, risks, success criteria
  02_CLARIFICATIONS/  open questions + assumed defaults
  03_PHASES/          phase heartbeats (1–5)
  04_QA/              QA, coverage matrix, review disposition
  05_FINAL/           main reference + final summary
  06_FILESCOPE/       branch, files, commands, provenance
  research/           75 extracted Zurich topics + source manifest + smoke tests
  nvidia_v4_swarm/    budget tracker, OpenAI-compatible client, parallel runner, real run
```

## Headline result

- 59 primary ServiceNow Zurich topics extracted (plus 16 supplementary) via the Fluid
  Topics khub API after the docs SPA and Playwright both failed.
- Main reference: order of operations, configuration surfaces, CI Class Manager
  breadcrumbs, IRE insert/update decision path, duplicate prevention, troubleshooting.
- Real parallel orchestration of 2 local Ollama models (2/2 succeeded) with a SQLite
  concurrency/daily-usage/cost ledger; cloud wrapper verified on DeepSeek and Groq.
