# swarm/ — free-API-key wrapper + busy/usage tracker + SUBQ

Owner agent: `inkling-2-small__openrouter__kilo` (model `openrouter/thinkingmachines/inkling-2-small:free`, provider OpenRouter, harness Kilo)

## What exists

| file | purpose |
|---|---|
| `free_keys.py` | Provider registry (OpenAI-compatible) + health check + busy (inflight) & daily usage ledger, fcntl-locked, per-provider max_inflight + daily_calls/tokens caps, estimated cost (est tokens at release + actual usage split prompt/completion when the API reports it in `usage`) |
| `subq_snap.py` | SubQ **Snap** (`subq-snap-1.2`) Decisions API client — typed decisions with probabilities; billed on input only ($0.04/1M) |
| `run_swarm.py` | Dispatch one bounded cross-check prompt to N providers in parallel (ThreadPoolExecutor), persist `results/<provider>.json` |
| `state/swarm_ledger.json` | Live ledger (calls, tokens est+actual, cost est+actual, inflight, daily caps per provider) |
| `results/` | Last cross-check run outputs |

## Providers (2026-11-13)

| provider | model | key env | status |
|---|---|---|---|
| groq | openai/gpt-oss-120b | `GROQ_API_KEY` | OK — 200 in 1.9s, free tier |
| cerebras | gpt-oss-120b | `CEREBRAS_API_KEY` (paid account name; free-key variant returned 401) | OK — 200 in 0.4-0.6s |
| gemini | gemini-2.5-flash-lite | `GEMINI_API_KEY`/`GOOGLE_AI_API_KEY` | OK — 200 in 1.0s |
| mistral | mistral-small-latest | `MISTRAL_API_KEY` | HTTP 429 rate-limited; not retried |
| openrouter | google/gemma-4-31b-it:free | `OPENROUTER_API_KEY` | HTTP 429 on free pool; `openrouter/free` meta-router also tried |
| ollama | gemma2:9b (local) | none | OK — 200 in 6.5s |
| **subq_free** | subq-savant-1.4 | `SUBQ_FREE_API_KEY` (fallback `SUBQ_API_KEY`) | **NO_KEY on this box — wired, never called** |
| **subq_paid** | subq-savant-1.4 | `SUBQ_API_KEY` | **NO_KEY on this box — wired, never called** |
| **subq_snap** | subq-snap-1.2 | `SUBQ_FREE_API_KEY`/`SUBQ_API_KEY` | **NO_KEY — wired, never called** |

## SUBQ (Subquadratic) — how to enable

Base URL `https://api.subq.ai/v1` (OpenAI-compatible). Account: console.subq.ai. Docs verified 2026-11-13
(`https://docs.subq.ai/`). Model `subq-savant-1.4` (early access, enabled per org; until then 403
`model_not_allowed`):

- Chat Completions `POST /v1/chat/completions`. Temperature fixed at **1** (other values → 400) — wrapper sends 1.
- `reasoning_effort`: `low` (wrapper default) | `high` (default) | `max`. Reasoning **cannot be turned off**; billed as output.
- `max_tokens` covers reasoning + answer together; a response can be `200` with `content: null`, `finish_reason: "length"` — budget accordingly.
- 4M-token context. Pricing: input **$0.10/1M** (cached $0.01/1M), output **$0.50/1M**. Reasoning bills as output.
- Wrapper sends `store: false` so prompts are not retained under SubQ's data-retention policy.
- Deprecated IDs (`subq-preview`, `subq-1p2-medium`) shut down **2026-11-25** — do not use.
- Snap decisions model `subq-snap-1.2` is **not** chat: `POST /v1/systemone`, input-only billing ($0.04/1M, output free), 384K context — see `subq_snap.py`.

Enable: `export SUBQ_FREE_API_KEY=... SUBQ_API_KEY=...` then `python3 run_swarm.py subq_free subq_paid` and
`python3 subq_snap.py smoke`. Status check: `python3 subq_snap.py status` and `python3 free_keys.py status subq_paid`.

## Cost/usage guard rails
- fcntl lock; `max_inflight` per provider; `daily_calls`/`daily_tokens` day-rolled caps; cost tracked est (release-time, blended) + actual (usage prompt/completion split, SubQ rates where known).
- Paid keys (`DEEPSEEK_API_KEY`, `OPENAI_API_KEY`, and now `SUBQ_API_KEY` once exported) are **never called automatically**; SUBQ entries are capped at 50 (free) / 200 (paid) calls/day and are excluded until keys exist.
- Ledger: `state/swarm_ledger.json` — `python3 free_keys.py status` prints it.

## Observed failure modes (2026-11-13)
- Reasoning models (qwen3.5:4b, gpt-oss-120b at high effort) blew the 900-token completion budget → `content: null`/empty. Wrapper returns `finish_reason` now; SUBQ default effort is `low`.
- All four free-tier answerers hallucinated ≥1 property name (e.g. gemini `discovery.source.attribute`, groq `discovery.ire.identify_by`/`discovery.ire.reconcile`, cerebras `discovery.identify.unique_key`, gemma2:9b `glide.discovery.duplicate.threshold` — **none exists**). None knew `glide.identification_engine.skip_duplicates` or IRE data source rules. Conclusion: free models need the cited digest, not raw freedom — matches HARNESS.md's digest-wrapper rationale.
- HTTP 429s (mistral, openrouter free pool) — recorded in `results/`, not retried.
