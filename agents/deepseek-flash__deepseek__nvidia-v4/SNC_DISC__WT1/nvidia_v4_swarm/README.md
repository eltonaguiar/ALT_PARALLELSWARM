# nvidia_v4_swarm — parallel model runner with a real usage ledger

Built for `SNC_DISC__WT1` by `deepseek-flash` (provider `deepseek`, Kilo CLI, worktree
`nvidia-v4`). It is deliberately small and dependency-light so another agent can audit it.

## Why this exists

Running several models in parallel is easy. Running them **without burning a free key** or
silently overspending is not. This harness separates three concerns:

1. **Concurrency** — per-provider in-flight slots.
2. **Daily quota** — calls and tokens per provider, per UTC day.
3. **Cost** — per-provider input/output price, recorded per call.
4. **Isolation** — every worker writes to its own folder with a visible phase trail.

## Files

| File | Role |
|---|---|
| `usage_tracker.py` | SQLite ledger. Atomic reserve/release, daily rollover, event log, cost. |
| `llm_client.py` | One OpenAI-compatible client. No SDKs. Keys from env only. |
| `run_swarm.py` | Thread-pool runner. Creates one worktree-like folder per agent. |
| `models.yaml` | Roster: local models enabled, cloud entries opt-in. |
| `state/usage.sqlite3` | Ledger (git-ignored). |

## Quick start

```bash
cd nvidia_v4_swarm

# 1. See who would run and whether keys are present (no secrets printed)
python3 run_swarm.py --dry-run

# 2. Run the enabled local models in parallel
python3 run_swarm.py --max-parallel 2

# 3. Run a specific cloud model (must be enabled or named explicitly)
python3 run_swarm.py --agents deepseek-chat__deepseek__nvidia-v4 --max-parallel 1

# 4. Inspect the ledger
python3 usage_tracker.py --status

# 5. Clear stale in-flight slots after a crash (only when no workers run)
python3 usage_tracker.py --repair
```

## What each worker produces

```
runs/<UTC>/
  PROMPT.md
  RUN_SUMMARY.md
  run_manifest.json
  <agent_id>/
    00_PREREQ/PREREQ.md          model, provider, base URL, key-present flag
    01_PLAN/PLAN.md              goal/format/constraints/budget
    03_PHASES/phase1_started.md
    03_PHASES/phase2_llm_call.md
    03_PHASES/phase3_complete.md (or phase3_failed / phase2_blocked)
    05_FINAL/MODEL_REVIEW.md     raw model output
    06_FILESCOPE/FILESCOPE.md    status, tokens, time, folder
    transcript.md                prompt + response
```

## Ledger design

- `providers` = caps and prices.
- `usage` = one row per provider per day: calls, tokens in/out, cost, in-flight.
- `events` = audit trail per call.
- `acquire()` uses `BEGIN IMMEDIATE`, checks caps, increments in-flight and calls, commits,
  then yields a `Reservation`. The request happens **outside** the transaction.
- `Reservation.release(tokens_in=..., tokens_out=...)` decrements in-flight and records
  measured usage exactly once. The context manager releases with zero usage if you forget,
  so a slot cannot leak on an exception.
- A hard crash can still leave an in-flight slot; `--repair` zeroes today's counters.

## Adding a provider

Add to `DEFAULT_BASE_URLS` / `DEFAULT_KEY_ENVS` in `llm_client.py`, then add a roster entry:

```yaml
- id: my-model__myprovider__nvidia-v4
  provider: myprovider
  model: my-model-id
  base_url: https://api.example.com/v1
  api_key_env: MYPROVIDER_API_KEY
  enabled: false
  max_inflight: 1
  daily_calls: 100
  daily_tokens: 300000
  price_in_per_1k: 0.0
  price_out_per_1k: 0.0
```

The endpoint must implement `POST /chat/completions` with the OpenAI request/response
shape. Streaming and tool calls are not implemented.

## Real run captured in this repo

`runs/20261113T090332Z/` — 2 local Ollama models, 2 parallel, 88.2 s wall:

| model | status | time | tokens in/out |
|---|---|---|---|
| `qwen2.5-coder:7b` | ok | 32.8 s | 3036 / 725 |
| `qwen3.5:4b` | ok | 88.2 s | 3157 / 2500 |

Cloud smoke test (`research/cloud_wrapper_smoke_test.md`): DeepSeek OK; Groq required a
browser UA and an available model id (`openai/gpt-oss-120b`).

## Caveats

- The tracker enforces concurrency and daily caps, **not** provider per-minute RPM limits.
  Add a token-bucket if you hammer a free tier.
- Price fields are manual. They are estimates, not billing truth.
- Model IDs in `models.yaml` decay. `--dry-run` tells you what would be called; it does not
  validate that the provider still serves that model.
- `qwen3.5:4b` is a thinking model. It may return empty `content` and put text in
  `reasoning`; the client falls back and labels that in the review file.
- Never commit `state/` or any key. `.gitignore` covers the ledger.
