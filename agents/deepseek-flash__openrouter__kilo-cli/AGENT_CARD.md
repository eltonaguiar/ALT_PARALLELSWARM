# Agent card — `deepseek-flash__openrouter__kilo-cli`

**Model:** `deepseek/deepseek-flash`
**Provider:** **OpenRouter** (inferred from the `vendor/model` ID namespace, the
`OPENROUTER` env vars, and the `openrouter2nd` worktree; not introspectable from inside
the session — see `00_MODEL/MODEL_PROVIDER.md`)
**Harness:** Kilo CLI
**Run:** 2026-11-13T08:46Z → 2026-11-13T09:10Z

## Where this work lives

| | |
|---|---|
| self worktree | `/tmp/kilo/ALT_PARALLELSWARM` (clone of the target repo) |
| branch | `agent/deepseek-flash__openrouter__kilo-cli` |
| folder in repo | `agents/deepseek-flash__openrouter__kilo-cli/SNC_DISC__WT1/` |
| worker worktrees | `/tmp/kilo/wt-{qwen3.5-4b,qwen2.5-coder-7b,particle-1}...` |

## Goal

Produce a thorough, source-cited reference on ServiceNow **Discovery configuration**:
configuration options/properties, order of operations, CI Class Manager breadcrumbs, and
the configuration that prevents duplicate CIs and governs insert-vs-update in the CMDB.

## Output format

`SNC_DISC__WT1/05_FINAL/DISCOVERY_CONFIG_REFERENCE.md` — 12 sections, tables for
options, exact property names/defaults, canonical docs links. Plus `04_QA/QA.md`,
`05_FINAL/FINAL_SUMMARY.md`, `06_FILESCOPE/FILESCOPE.md`, and a dated run report under
`runs/2026-11-13T0846Z_deepseek-flash__openrouter__kilo-cli/REPORT.md`.

## Self-reported status

- capability gate: **PASS** — browsing works via the ServiceNow docs khub JSON API;
  naive `webfetch` and Playwright body extraction do **not** work on the SPA.
- primary reference: **complete** (12 sections, 68 documented topics indexed).
- QA: **PASS** (SC1–SC10); one worker-draft imprecision flagged. Terminology audit
  against the CMDB/Discovery learning guides passed after correcting the IRE Data Source
  Rule to **insert-only** and keeping Reconciliation/Data Refresh **update-only**.
- parallel workers: **3/3 QA PASS** — `qwen3.5:4b` (Ollama), `qwen2.5-coder:7b`
  (Ollama), `particle-ai/particle-1:free` (OpenRouter free).
- free-tier spend: **$0.00** recorded.

## Files modified

Only `agents/deepseek-flash__openrouter__kilo-cli/` plus the append-only
`CONTRIBUTORS.md` / `agents.yaml` entry and a `results/` report folder. No other
agent's folder is touched.

Full list: `SNC_DISC__WT1/06_FILESCOPE/FILESCOPE.md`.
