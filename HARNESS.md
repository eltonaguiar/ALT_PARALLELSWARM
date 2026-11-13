# ALT_PARALLELSWARM — parallel agents, isolated worktrees

A shared playground for running **multiple models in parallel**, each in its **own git worktree**,
each documenting its own plan → phases → QA → final summary so nothing drifts silently.

Task on this pass: **SNC_DISC_RESEARCH** — a thorough ServiceNow Discovery *configuration* reference
(options/properties, order of operations, CI Class Manager bread crumbs, duplicate prevention and
insert-vs-update behaviour in the CMDB).

## Folder contract

Every agent writes inside its own worktree under:

```
agents/<agent_id>/SNC_DISC__WT<n>/
  00_PREREQ/PREREQ.md            # can I browse? playwright? is my context big enough?
  01_PLAN/PLAN.md                # goal, output format, phases, risks, success criteria
  02_CLARIFICATIONS/CLARIFY.md   # what I need from others, or "blocked, need backup"
  03_PHASES/phaseN_*.md          # heartbeat per phase
  04_QA/QA.md                    # self-check against the success criteria
  05_FINAL/DISCOVERY_CONFIG_REFERENCE.md
  05_FINAL/FINAL_SUMMARY.md      # goal met? blockers? clarifications?
  06_FILESCOPE/FILESCOPE.md      # files written, branch, worktree path
  research/                      # raw search→digest transcripts
```

`<agent_id>` = `<model>__<provider>__<harness>` so two agents never collide.

## Shared tooling (`shared/`)

| file | purpose |
|---|---|
| `orchestrate.py` | creates worktrees, runs agents in parallel, commits + pushes per branch |
| `agent_runner.py` | one agent's full lifecycle (prereq → plan → phases → research → QA → final) |
| `prereq_probe.py` | capability gate: HTTP, Playwright/Chromium, JS rendering, search reachability, context size |
| `research_harness.py` | search→digest wrapper: search engine → authority ranking → paragraph extraction → evidence digest |
| `budget.py` | concurrency + daily-usage ledger per provider (prevents burning a free key / overspending) |

## Why a digest wrapper and not raw browser tools

Tested on this box: small models given raw browser primitives (search/open/click/find links) flail —
20+ steps, no notes, empty answers. Given a **digest** (server-side retrieval + extraction), the same
model produces cited answers. The wrapper absorbs what the model is bad at.

## Running

```bash
python3 shared/orchestrate.py --roster agents.yaml
python3 shared/budget.py ollama        # usage ledger
```

---

## This pass: who ran what

**Author of this pass:** Hermes CLI agent, running **`deepseek-v4-flash`** via the **`deepseek`** provider.
Its folder is `agents/deepseek-v4-flash__deepseek__hermes/` — that is my run, not a local model's.

Other agents in this pass are locally-served Ollama models driven by the same harness.
Each declares its own model + provider in its `00_PREREQ/PREREQ.md`, `01_PLAN/PLAN.md` and
`06_FILESCOPE/FILESCOPE.md`.

---

## Grading — private rubrics live OUTSIDE this repo

`shared/judge.py` scores finished documents against a rubric that must not be visible to the
agents being graded. Two hard rules:

1. **The rubric file lives outside the git tree** (currently `~/.alt_parallelswarm_private/`).
   `judge.py` refuses to run if the rubric path resolves inside this repo, so it can never be
   committed, read by an agent, or scraped from GitHub.
2. **No rubric terms appear in any prompt, question, or plan template.** Agent prompts are built by
   `agent_runner.py` + `research_harness.py`; if a rubric term ever shows up there, the run is
   contaminated and must be discarded.

Scoring is post-hoc and local — no model calls, so grading cannot leak through a prompt either.
`shared/state/rubric_scores.json` stores item **ids and counts only**, never rubric text.

Why this matters: the built-in `TOPICS` regex check in `agent_runner.py` measures *presence of
words*, so a doc can score 8/8 there while missing half the things a domain expert would require.
The private rubric is the real bar.

