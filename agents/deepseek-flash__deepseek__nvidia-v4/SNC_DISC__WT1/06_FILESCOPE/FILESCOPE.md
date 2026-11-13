# 06 — Filescope

## Identity

| Field | Value |
|---|---|
| Model | `deepseek-flash` |
| Provider | `deepseek` |
| Harness | Kilo CLI |
| Agent id | `deepseek-flash__deepseek__nvidia-v4` |
| Worktree | `nvidia-v4` |
| Branch | `agent/deepseek-flash__deepseek__nvidia-v4` |
| Task | `SNC_DISC__WT1` — ServiceNow Discovery configuration research |
| Run window | 2026-11-13T08:51Z – 2026-11-13T09:25Z |
| Commit | recorded after push |

## Files written (all under this agent folder unless noted)

### Root

| File | Purpose |
|---|---|
| `00_MODEL_AND_PROVENANCE.md` | Model/provider/worktree, ownership, honesty notes. |
| `README.md` | Human entry point and reading order. |

### `SNC_DISC__WT1/`

| File | Purpose |
|---|---|
| `00_PREREQ/PREREQ.md` | Capability gate; working khub API recipe. |
| `01_PLAN/PLAN.md` | Goal, output contract, phases, risks, success criteria. |
| `02_CLARIFICATIONS/CLARIFY.md` | 12 scoping questions + assumed defaults. |
| `03_PHASES/phase1_capability_gate.md` | Playwright/SPA failure, API success. |
| `03_PHASES/phase2_corpus.md` | 75 topics extracted. |
| `03_PHASES/phase3_synthesis.md` | Reference structure. |
| `03_PHASES/phase4_qa_and_orchestration.md` | QA + 2-model parallel run. |
| `03_PHASES/phase5_publish.md` | Publish steps. |
| `04_QA/QA.md` | Success criteria, coverage, review disposition. |
| `05_FINAL/DISCOVERY_CONFIG_REFERENCE.md` | **Main deliverable.** |
| `05_FINAL/FINAL_SUMMARY.md` | Goal, blockers, clarifications, confidence. |
| `06_FILESCOPE/FILESCOPE.md` | This file. |

### `research/`

- 75 markdown files: 59 core + 16 supplementary Zurich topics.
- `source_manifest.json` — title, map, pretty URL, local file.
- `cloud_wrapper_smoke_test.md` — DeepSeek/Groq verification.
- `README.md` — corpus naming/version caveat.

### `nvidia_v4_swarm/`

| File | Purpose |
|---|---|
| `usage_tracker.py` | SQLite concurrency/daily/cost ledger. |
| `llm_client.py` | OpenAI-compatible client (7 providers). |
| `run_swarm.py` | Parallel runner, per-agent folders. |
| `models.yaml` | Roster; 2 local enabled, 6 cloud disabled. |
| `README.md` | Design, usage, caveats. |
| `.gitignore` | Excludes `state/`, `__pycache__/`. |
| `runs/20261113T090332Z/` | Real 2-model run (summary, manifest, per-agent folders). |

### Root shared files (additive only)

| File | Change |
|---|---|
| `CONTRIBUTORS.md` | One row for this agent. |
| `agents.yaml` | One `self_runs:` entry. |

## Not touched

- Every other `agents/<id>/` folder.
- `shared/`.
- Root `README.MD`, `HARNESS.md`, `ORCHESTRATION.md`, `.gitignore`.

## Commands used (high level)

```bash
git clone https://github.com/eltonaguiar/ALT_PARALLELSWARM.git
git checkout -b agent/deepseek-flash__deepseek__nvidia-v4

# research retrieval
curl -s -H 'Accept: application/json' .../api/khub/maps
curl -s -H 'Accept: application/json' .../api/khub/maps/<id>/toc
curl -s -H 'Referer: https://www.servicenow.com/docs/' .../topics/<contentId>/content
python3 /tmp/sn_extract.py           # HTML → markdown, 59 topics
python3 /tmp/sn_extras.py            # +16 supplementary topics

# swarm
python3 -m py_compile usage_tracker.py llm_client.py run_swarm.py
python3 run_swarm.py --dry-run
python3 run_swarm.py --max-parallel 2 --timeout 600
python3 usage_tracker.py --status
```

## Side effects outside the repo

- Local Ollama inference (no external cost).
- Two tiny cloud smoke calls: DeepSeek 16 tokens (~$0.000008), Groq 108 tokens ($0.00
  tracked).
- `/tmp/sn_research/`, `/tmp/pw_test*.py`, `/tmp/sn_extract.py` are scratch only; the
  committed copies are under `research/`.

## Verification

- `git status` shows only this agent folder + the two additive root rows.
- `python3 -m py_compile` passes for all three scripts.
- Swarm run: 2/2 `ok`, ledger `inflight=0`.
- No API key values were written to disk or printed.
