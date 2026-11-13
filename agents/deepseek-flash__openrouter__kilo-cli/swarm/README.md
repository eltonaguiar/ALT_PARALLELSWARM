# ALT Parallel Swarm harness

A small, dependency-free (stdlib only) orchestrator for running several models in
parallel, each in its own git worktree, with a hard budget gate and a documented
artifact contract.

**Author:** `deepseek-flash__openrouter__kilo-cli` — model `deepseek/deepseek-flash`,
provider OpenRouter (inferred), harness Kilo CLI.

## Files

| File | Purpose |
|---|---|
| `registry.json` | Provider endpoints, env-var names, conservative caps, model→provider map |
| `roster.json` | The three-worker roster used for this run |
| `usage_tracker.py` | File-locked concurrency + daily-call/token + cost ledger |
| `router.py` | One OpenAI-compatible chat interface (plus native Ollama) |
| `worktree_manager.py` | Create worktree/branch, scaffold folder, commit/push one folder |
| `agent_runner.py` | Worker lifecycle with prereq/plan/phases/QA/final/filescope |
| `orchestrator.py` | Bounded parallel dispatch + aggregate report |
| `evidence/` | Pre-fetched, source-marked digests given to workers (they have no browser) |
| `state/` | Ledger, last run, worker logs (committed as evidence) |

## Design rules

1. **One worktree per agent, one branch per agent, one folder per agent.** A worker
   stages only `agents/<id>/`, so branches merge without conflicts.
2. **The worker never browses.** It receives a digest produced by a researching agent.
   This is the documented backup plan, not a hidden capability.
3. **The tracker is the gate.** `acquire()` refuses when `inflight`, `daily_calls`, or
   `daily_tokens` would be exceeded. It never sees or stores API keys.
4. **A phase file is written when the phase starts.** An interrupted run is diagnosable.
5. **QA is a gate, not a formality.** If the primary model's output fails the automated
   gate, the runner tries the fallback model; the report records every attempt.

## Usage

```bash
# 1. See the ledger
python3 usage_tracker.py --status

# 2. Smoke-test one model (no worktree)
python3 router.py --model qwen3.5:4b --max-tokens 24

# 3. Dry run: create worktrees and drafts, no push
python3 orchestrator.py --repo /path/to/ALT_PARALLELSWARM --no-push

# 4. Real run (pushes each agent branch)
python3 orchestrator.py --repo /path/to/ALT_PARALLELSWARM

# 5. Run only selected agents
python3 orchestrator.py --repo /path/to/ALT_PARALLELSWARM \
  --only qwen3.5-4b__ollama__alt-swarm
```

## Free-tier safety

Caps in `registry.json` are **operator guards**, not vendor-verified limits:

```json
"openrouter": { "max_inflight": 2, "daily_calls": 120, "daily_tokens": 600000 }
```

A single free key shared by many workers will still hit upstream 429s. The observed
failure in this run was exactly that: a large prompt to a `:free` Gemma model returned
`429 ... upstream_provider_shared_pool`. The harness recovered by switching to
Particle AI with a Baidu ERNIE fallback.

If you add a paid provider, set `price_per_1k`; the ledger then accumulates
`cost_usd` per provider and per day.

## Adding a worker

1. Add a provider entry (if new) to `registry.json`.
2. Add a model entry with `{ "provider": "..." }`.
3. Add a roster entry with `id`, `model`, `provider`, `wt`, `evidence`, `out`, `brief`,
   and optional `fallbacks`.
4. Add or reuse a digest in `evidence/` with `[S1]`, `[S2]` source markers.
5. Run with `--only <id>`.

## Known limitations

- The router assumes OpenAI-compatible chat plus Ollama; native Gemini/Anthropic APIs
  are not implemented.
- Reasoning-token variance can consume the output budget; set `max_tokens` generously
  for reasoning models.
- The runner's automated QA cannot verify factual truth; a human or a stronger
  synthesis pass must still review the drafts.
- `git push` uses the ambient credentials. Use `--no-push` in untrusted environments.
