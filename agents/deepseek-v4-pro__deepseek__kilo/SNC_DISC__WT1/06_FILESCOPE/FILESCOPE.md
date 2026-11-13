# File scope — deepseek-v4-pro__deepseek__kilo

- **Worktree:** `/home/eaguiar2015/wt-deepseek-v4-pro__deepseek__kilo`
- **Branch:** `agent/deepseek-v4-pro__deepseek__kilo`
- **Folder:** `agents/deepseek-v4-pro__deepseek__kilo/SNC_DISC__WT1`
- **Model / provider / harness:** `deepseek-v4-pro` / `deepseek` (DeepSeek API) / `kilo`

## Files this agent wrote

```
00_PREREQ/PREREQ.md
01_PLAN/PLAN.md
02_CLARIFICATIONS/CLARIFY.md
03_PHASES/phase1_capability_gate.md
03_PHASES/phase2_research_started.md
03_PHASES/phase3_research_done.md
03_PHASES/phase4_synthesis_done.md
04_QA/QA.md
05_FINAL/DISCOVERY_CONFIG_REFERENCE.md
05_FINAL/FINAL_SUMMARY.md
06_FILESCOPE/FILESCOPE.md
research/_fetch_driver.py          (search->digest driver, reused shared/research_harness.py)
research/_fetch_docs.py            (docs fetcher via Playwright render fallback)
research/20261113_085219_*.md      (10 search digests)
research/20261113_085414_DOC_*.md  (5 docs-render digests)
research/official_docs/*.md        (13 official ServiceNow docs, GitHub markdown mirror)
```

## git status (worktree)

Only `agents/deepseek-v4-pro__deepseek__kilo/` is added by this agent. Shared tooling
(`shared/free_api_registry.py`) and the dated results/transcript folder are committed on
`main` (they are not per-agent).

## Shared tooling contributed (on `main`)

- `shared/free_api_registry.py` — unified free/paid key catalog + `complete()` wrapper +
  budget-tracker integration (busy/inflight + daily calls/tokens + cost).
