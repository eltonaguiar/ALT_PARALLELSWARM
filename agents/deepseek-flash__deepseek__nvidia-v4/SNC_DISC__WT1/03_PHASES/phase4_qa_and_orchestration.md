# Phase 4 — QA + parallel model orchestration (STARTED → DONE)

- Started: 2026-11-13T09:12Z
- Finished: 2026-11-13T09:22Z

## Built

`nvidia_v4_swarm/`:

- `usage_tracker.py` — SQLite ledger, atomic reservations, per-provider concurrency + daily
  calls/tokens, cost accounting, event log, `--repair` for stale slots.
- `llm_client.py` — dependency-free OpenAI-compatible client for Ollama, DeepSeek, Groq,
  Gemini, Cerebras, Mistral, OpenRouter. Keys from env only.
- `run_swarm.py` — thread-pool parallel runner; one folder per agent with
  prereq/plan/phases/review/filescope/transcript.
- `models.yaml` — 2 local models enabled; 6 cloud entries disabled by default.

## Real run

`runs/20261113T090332Z/` — 2 local Ollama models, max_parallel=2:

| model | status | time | tokens |
|---|---|---|---|
| `qwen2.5-coder:7b` | ok | 32.8 s | 3036/725 |
| `qwen3.5:4b` | ok | 88.2 s | 3157/2500 |

Cloud smoke test: DeepSeek OK; Groq initially blocked by Cloudflare 1010 (UA) and a stale
model id, then OK with `openai/gpt-oss-120b` after the UA fix.

## Review disposition

Accepted: clarify that `skip_duplicates` does not suppress de-duplication task creation.
Rejected: claims contradicting primary sources (lookup-record insertion, oldest-duplicate
selection, 90-day partial retention). Full table in `04_QA/QA.md` §4.

## Blocker

None. `qwen3.5:4b` exhausted its token budget and returned text in `reasoning`; recorded,
not hidden.
