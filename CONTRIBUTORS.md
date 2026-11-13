# CONTRIBUTORS — who wrote which folder, on which model

Every agent that adds work to this repo owns **one** folder under `agents/` named
`<model>__<provider>__<harness>` (see `HARNESS.md`). Never edit another agent's folder.

| agent folder | model | provider | harness | worktree(s) | contributed |
|---|---|---|---|---|---|
| `deepseek-v4-flash__deepseek__hermes` | `deepseek-v4-flash` | DeepSeek API (`api.deepseek.com`) | Hermes CLI | WT1 (self) + WT2–WT4 (local Ollama workers) | scaffold harness (`shared/`), roster, first pass |
| `deepseek-v4.1-flash-fast__freebuff__buffy` | `DeepSeek V4.1 Flash Fast` | **Freebuff / Codebuff (Buffy)** agent runtime — model served by the Freebuff client, not a direct vendor key | Buffy native tools (`web_search`, `read_url`) | SNC_DISC__WT1 | evidence-backed Discovery reference, `CONTRIBUTORS.md`, free-cloud budget defaults, `--no-push` fix |
| `deepseek-v4-pro__deepseek__kilo` | `deepseek-v4-pro` | DeepSeek API (`api.deepseek.com`) | Kilo (native `webfetch` + shared harness) | SNC_DISC__WT1 (self) + WT6–WT8 (local Ollama workers) | Discovery reference covering all 4 IRE rule families, `shared/free_api_registry.py`, orchestrated 3 local models |
| `inkling-2-small__openrouter__kilo` | `thinkingmachines/inkling-2-small:free` (reported as `openrouter/thinkingmachines/inkling-2-small:free`) | **OpenRouter** (free tier) | Kilo CLI | SNC_DISC__WT1 | Fluid-Topics-API evidence corpus (17 Australia docs), cited config reference, `swarm/` free-key wrapper + busy/usage ledger, SUBQ (Savant 1.4 + Snap 1.2) wiring |
| `deepseek-flash__openrouter__kilo-cli` | `deepseek/deepseek-flash` | **OpenRouter** (inferred from model ID + env; see folder's `00_MODEL/MODEL_PROVIDER.md`) | Kilo CLI | SNC_DISC__WT1 (self) + WT2–WT4 (dispatched workers) | 68-topic Brazil docs corpus, 12-section cited Discovery reference, `swarm/` harness (worktree manager, router, fcntl usage/cost ledger, QA-aware fallback), orchestrated 3 workers |
| `qwen3.5-4b__ollama__alt-swarm` | `qwen3.5:4b` | ollama (local) | ALT swarm harness | SNC_DISC__WT2 | configuration-options + order-of-operations draft (QA pass) |
| `qwen2.5-coder-7b__ollama__alt-swarm` | `qwen2.5-coder:7b` | ollama (local) | ALT swarm harness | SNC_DISC__WT3 | duplicate-prevention / insert-vs-update draft (QA pass; one imprecision flagged) |
| `particle-1__openrouter__alt-swarm` | `particle-ai/particle-1:free` | OpenRouter (free) | ALT swarm harness | SNC_DISC__WT4 | CI Class Manager breadcrumbs draft (QA pass) |

## Adding yourself

1. Pick an id: `<model>__<provider>__<harness>`, lowercase, dots allowed (e.g. `qwen3-30b-a3b__ollama__hermes`).
2. Create `agents/<id>/SNC_DISC__WT<n>/` using the folder contract in `HARNESS.md`.
3. Declare **model + provider** in `00_PREREQ/PREREQ.md`, `01_PLAN/PLAN.md`, `05_FINAL/FINAL_SUMMARY.md`, `06_FILESCOPE/FILESCOPE.md`.
4. Add a row to this table and an entry to `agents.yaml` (`agents:` if the harness dispatches you,
   `self_runs:` if you drove your own tools).
5. Only commit your own folder (plus this table row and your roster entry).

## Self-driven runs (`agents.yaml → self_runs`)

`orchestrate.py` reads only the `agents:` list. A model that ran under its own native tooling
(no API dispatch) belongs in `self_runs:` so the roster stays truthful without being re-run.
| `deepseek-v4.1-flash-fast__freebuff__buffy` | `DeepSeek V4.1 Flash Fast` | **Freebuff / Codebuff (Buffy)** agent runtime | Buffy native tools (`web_search`, `read_url`) | SNC_DISC__WT1 | 28-source Discovery reference incl. IRE data source + data refresh rules |
| `deepseek-v4-pro__deepseek__kilo` | `deepseek-v4-pro` | DeepSeek API | Kilo (`webfetch` + `ServiceNowDocs` mirror + shared harness) | SNC_DISC__WT1 | 25-source Discovery reference incl. IRE data source + data refresh rules; free-key wrapper; orchestrated 3 local Ollama models |
