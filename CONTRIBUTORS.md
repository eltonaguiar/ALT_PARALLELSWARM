# CONTRIBUTORS — who wrote which folder, on which model

Every agent that adds work to this repo owns **one** folder under `agents/` named
`<model>__<provider>__<harness>` (see `HARNESS.md`). Never edit another agent's folder.

| agent folder | model | provider | harness | worktree(s) | contributed |
|---|---|---|---|---|---|
| `deepseek-v4-flash__deepseek__hermes` | `deepseek-v4-flash` | DeepSeek API (`api.deepseek.com`) | Hermes CLI | WT1 (self) + WT2–WT4 (local Ollama workers) | scaffold harness (`shared/`), roster, first pass |
| `deepseek-v4.1-flash-fast__freebuff__buffy` | `DeepSeek V4.1 Flash Fast` | **Freebuff / Codebuff (Buffy)** agent runtime — model served by the Freebuff client, not a direct vendor key | Buffy native tools (`web_search`, `read_url`) | SNC_DISC__WT1 | evidence-backed Discovery reference, `CONTRIBUTORS.md`, free-cloud budget defaults, `--no-push` fix |
| `deepseek-flash__deepseek__nvidia-v4` | `deepseek-flash` | `deepseek` (DeepSeek model family) | Kilo CLI | `SNC_DISC__WT1` (`nvidia-v4`) | Discovery/IRE configuration reference from 59 Zurich topics; CI Class Manager breadcrumbs; duplicate + insert/update guide; parallel local-model harness with SQLite usage/cost ledger |

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
