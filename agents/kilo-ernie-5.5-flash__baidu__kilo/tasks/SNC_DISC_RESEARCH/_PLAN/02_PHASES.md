# 02 — Phases

Each worktree writes a marker into its own `phases/` folder **as a phase starts**
(`phase1.md`, `phase2.md`, ...) so progress is visible live. The lead worktree also
maintains the shared task state in `_ORCHESTRATION/phase_state.json`.

## Global phases (task-level)

- **P0 Plan** — charter, clarifications, risks, success criteria (this folder). ✅
- **P1 Probe** — capability probe of all models; mark reachable/unreachable. ✅ (`swarm/probe.json`)
- **P2 Scaffold** — create worktrees + contract files. ✅ (`worktree_manager.py`)
- **P3 Dispatch** — lead does live web research; orchestrator fans out peer prompts. 
- **P4 Collect** — gather each worktree's `files/`, assemble the combined report.
- **P5 QA** — each worktree self-QA (`05_QA.md`) + lead integration QA.
- **P6 FinalSummary** — goal achieved? blockers? clarifications?

## Per-worktree phases (standard)

| Phase | Marker file | Meaning |
|-------|-------------|---------|
| 1 | `phases/phase1.md` | Scope confirmed, first model call issued / research started |
| 2 | `phases/phase2.md` | First draft / output written to `files/` |
| 3 | `phases/phase3.md` | Self-review + fixes |
| 4 | `phases/phase4.md` | QA + FinalSummary written |

## Phase state file
`_ORCHESTRATION/phase_state.json` is rewritten by `orchestrator.py` after each run:
per-worktree status (done / error / skipped-unreachable), output path, latency, usage.