# Orchestration

How a task goes from charter to finished report across parallel model worktrees.

## 1. Charter the task
Write `_PLAN/00_CHARTER.md` with the goal, the worktree split, and out-of-scope.
Write `task.json` describing each worktree: `id`, `slug`, `model` (or `null` for the lead),
`role`, `goal`, `output_file`, `max_tokens`, and optional `context_files`.

## 2. Probe capabilities (gate)
```bash
python -m swarm.capability_probe --all
```
Writes `swarm/probe.json`. The orchestrator refuses to dispatch to a model marked
unreachable — no wasted tokens, no silent failure.

## 3. Scaffold worktrees
```bash
python -m swarm.worktree_manager --task SNC_DISC_RESEARCH
```
Creates `tasks/<task>/worktrees/WT<n>_<slug>/` with the standard contract
(`00_WORKTREE.md` … `06_FINALSUMMARY.md`, `phases/`, `files/`).

## 4. Lead does the browsing
The lead agent (this worktree, `WT1`) runs live web research with its own tools
(`websearch`, `webfetch`, `defuddle`, Playwright) and writes distilled notes to a shared
context file, e.g. `tasks/SNC_DISC_RESEARCH/_ORCHESTRATION/shared_context.md`.
Local models have no browser; they reason over this fetched context.

## 5. Dispatch (parallel, usage-capped)
```bash
python -m swarm.orchestrator --task SNC_DISC_RESEARCH \
    --shared-context tasks/SNC_DISC_RESEARCH/_ORCHESTRATION/shared_context.md
```
- Runs worktrees concurrently in a thread pool (tracker caps per-provider concurrency).
- Each worktree writes its reply to `files/<output_file>` + a `phases/phaseN.md` marker.
- Records `done / error / skipped-unreachable` in `_ORCHESTRATION/phase_state.json`.

Run a single worktree while iterating: `--only WT2`. Preview without spending: `--dry-run`.

## 6. Collect & integrate
The lead assembles `files/COMBINED_REPORT.md` from every worktree's output, reconciles
contradictions, and does integration QA.

## 7. QA + FinalSummary
Each worktree fills `05_QA.md` and `06_FINALSUMMARY.md` (goal met? blockers? clarifications?).

## Degrade-gracefully rules
- Model unreachable → marked `skipped-unreachable`; its slice falls back to the lead or a bigger peer.
- Free key exhausted (429/quota) → tracker blocks further calls that day; run continues with what's reachable.
- Small model gives weak output → escalate the slice to a reasoning model (e.g. deepseek-r1:32b).

## Status at a glance
`_ORCHESTRATION/phase_state.json` is the single file to read for "who's done, who's
blocked, what did it cost".