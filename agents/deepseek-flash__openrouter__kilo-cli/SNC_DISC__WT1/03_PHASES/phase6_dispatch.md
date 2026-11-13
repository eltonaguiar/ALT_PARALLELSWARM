# Phase 6 — dispatch parallel workers

**Status:** COMPLETE
**Started:** 2026-11-13T08:57Z
**Finished:** 2026-11-13T09:06Z

## What ran

| Worker | Model | Provider | Worktree | WT | Result |
|---|---|---|---|---|---|
| `qwen3.5-4b__ollama__alt-swarm` | `qwen3.5:4b` | ollama (local) | `/tmp/kilo/wt-qwen3.5-4b__ollama__alt-swarm` | WT2 | QA PASS, 1266 words |
| `qwen2.5-coder-7b__ollama__alt-swarm` | `qwen2.5-coder:7b` | ollama (local) | `/tmp/kilo/wt-qwen2.5-coder-7b__ollama__alt-swarm` | WT3 | QA PASS, 671 words |
| `particle-1__openrouter__alt-swarm` | `particle-ai/particle-1:free` | openrouter (free) | `/tmp/kilo/wt-particle-1__openrouter__alt-swarm` | WT4 | QA PASS, 1328 words |

- Wall time for the final three-worker pass: **88.6 s**.
- Each worker had its own branch `agent/<id>`, its own folder, and its own phase files.
- Each worker received a pre-fetched evidence digest and had no browser/shell.
- All three branches were committed and pushed.

## Failure and recovery evidence

- `google/gemma-4-31b-it:free` and `google/gemma-4-26b-a4b-it:free` failed with
  upstream `429` on the large prompt (the tiny probe had succeeded, so this was load,
  not auth).
- The harness was upgraded with a QA-aware fallback gate; the free worker moved to
  `particle-ai/particle-1:free` with `baidu/ernie-5.5-flash-preview:free` as fallback.
- One particle run returned only 183 words because reasoning consumed the budget; a
  larger token budget fixed it.

## Exit criterion

≥ 2 workers complete in isolated worktrees with committed artifacts. ✅
