# `plans/` — plans and run status, per worktree

The `HARNESS.md` contract puts every agent's plan inside its own worktree at
`agents/<agent_id>/SNC_DISC__WT<n>/01_PLAN/PLAN.md`. That is correct for the harness but it is four
levels deep, so this folder is the **browsable root-level view**: one subfolder per worktree, plus
the index below.

Task: **SNC_DISC_RESEARCH** — ServiceNow Discovery configuration reference.

## Index of worktrees

| agent id | worktree | model / provider | plan | deliverable | effort |
|---|---|---|---|---|---|
| `deepseek-v4-flash__deepseek__hermes` | `SNC_DISC__WT1` | `deepseek-v4-flash` / `deepseek` | [plan](../agents/deepseek-v4-flash__deepseek__hermes/SNC_DISC__WT1/01_PLAN/PLAN.md) | [reference](../agents/deepseek-v4-flash__deepseek__hermes/SNC_DISC__WT1/05_FINAL/DISCOVERY_CONFIG_REFERENCE.md) | 151 lines / 0 citations |
| `deepseek-v4.1-flash-fast__freebuff__buffy` **(this worktree)** | `SNC_DISC__WT1` | `deepseek-v4.1-flash-fast` / `freebuff` | [plan](../agents/deepseek-v4.1-flash-fast__freebuff__buffy/SNC_DISC__WT1/01_PLAN/PLAN.md) | [reference](../agents/deepseek-v4.1-flash-fast__freebuff__buffy/SNC_DISC__WT1/05_FINAL/DISCOVERY_CONFIG_REFERENCE.md) | 542 lines / 28 citations |
| `llama3.1-8b__ollama__hermes` | `SNC_DISC__WT3` | `llama3.1-8b` / `ollama` | [plan](../agents/llama3.1-8b__ollama__hermes/SNC_DISC__WT3/01_PLAN/PLAN.md) | [reference](../agents/llama3.1-8b__ollama__hermes/SNC_DISC__WT3/05_FINAL/DISCOVERY_CONFIG_REFERENCE.md) | 18 lines / 0 citations |
| `openrouter-free__openrouter__kilo` | `SNC_DISC__WT5` | `openrouter-free` / `openrouter` | [plan](../agents/openrouter-free__openrouter__kilo/SNC_DISC__WT5/01_PLAN/PLAN.md) | [reference](../agents/openrouter-free__openrouter__kilo/SNC_DISC__WT5/05_FINAL/DISCOVERY_CONFIG_REFERENCE.md) | 140 lines / 0 citations |
| `qwen2.5-7b__ollama__hermes` | `SNC_DISC__WT2` | `qwen2.5-7b` / `ollama` | [plan](../agents/qwen2.5-7b__ollama__hermes/SNC_DISC__WT2/01_PLAN/PLAN.md) | [reference](../agents/qwen2.5-7b__ollama__hermes/SNC_DISC__WT2/05_FINAL/DISCOVERY_CONFIG_REFERENCE.md) | 18 lines / 0 citations |
| `qwen3-30b-a3b__ollama__hermes` | `SNC_DISC__WT4` | `qwen3-30b-a3b` / `ollama` | [plan](../agents/qwen3-30b-a3b__ollama__hermes/SNC_DISC__WT4/01_PLAN/PLAN.md) | [reference](../agents/qwen3-30b-a3b__ollama__hermes/SNC_DISC__WT4/05_FINAL/DISCOVERY_CONFIG_REFERENCE.md) | 78 lines / 0 citations |

## Mirror rule

A worktree subfolder here holds a **mirror** of that worktree's `01_PLAN/PLAN.md`. The in-worktree
file stays authoritative (it is what `shared/agent_runner.py` writes and what `HARNESS.md` requires);
the mirror exists so the plan is readable without clicking through `agents/<id>/SNC_DISC__WT<n>/`.
Both files change in the same commit. Each subfolder may also carry a `STATUS.md` with the honest
outcome of that run — what was produced, what was verified, and what the agent actually could not do.

## Layout of one worktree folder

```
plans/<agent_id>__WT<n>/
  PLAN.md      # mirror of 01_PLAN/PLAN.md: goal, output format, phases, risks, success criteria
  STATUS.md    # optional: outcome, verification evidence, blockers
```

Full per-worktree artifacts (prereq gate, phase heartbeats, QA, final summary, filescope, evidence
digest) remain under `agents/<agent_id>/SNC_DISC__WT<n>/`.
