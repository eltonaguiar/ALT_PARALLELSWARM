# ALT_PARALLELSWARM

**Parallel, multi-model research swarm with per-model worktrees, capability gating,
phase tracking, and free-API-key usage accounting.**

The idea: instead of one agent grinding a task alone, spin up **N models in parallel**,
each in its **own worktree / sub-folder**, each with a declared *goal*, *output format*,
*files-scope*, and a *phase ledger*. A thin orchestrator dispatches work, a usage
tracker keeps free API keys from being abused (concurrency + daily + cost caps), and a
capability probe refuses to hand a task to a model that can't actually do it (e.g. no
web browsing).

```
                      ┌──────────────────────────────────────────────┐
                      │                ORCHESTRATOR                   │
                      │  swarm/orchestrator.py  (dispatch + monitor)  │
                      └───────────────┬──────────────────────────────┘
                                      │  plan → gate → dispatch → collect
        ┌──────────────┬──────────────┼──────────────┬──────────────┐
        ▼              ▼              ▼              ▼              ▼
   ┌─────────┐   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
   │ WT1     │   │ WT2     │    │ WT3     │    │ WT4     │    │ WTn     │
   │ model A │   │ model B │    │ model C │    │ model D │    │ model Z │
   └────┬────┘   └────┬────┘    └────┬────┘    └────┬────┘    └────┬────┘
        │             │              │              │              │
   goal.md        goal.md        goal.md        goal.md        goal.md
   phase1.md      phase1.md      phase1.md      phase1.md      phase1.md
   files/         files/         files/         files/         files/
        └─────────────┴──────┬───────┴──────────────┴──────────────┘
                             ▼
                  ┌─────────────────────┐
                  │  usage_tracker.json │  concurrency / daily / cost
                  └─────────────────────┘
```

## Layout

```
ALT_PARALLELSWARM/
├── README.md                      ← you are here
├── docs/
│   ├── MODEL_REGISTRY.md          ← every model/provider, tier, context, capabilities
│   ├── ORCHESTRATION.md           ← how the swarm is planned & run
│   ├── API_WRAPPERS.md            ← free-key wrapper + tracker design
│   └── agents/
│       ├── _template.md
│       └── kilo-ernie-5.5-flash.md   ← this agent's identity (model/provider)
├── swarm/                         ← the framework (Python, stdlib only)
│   ├── registry.json              ← model catalog + capability matrix
│   ├── llm_router.py              ← unified chat() across providers
│   ├── usage_tracker.py           ← thread-safe concurrency/daily/cost ledger
│   ├── capability_probe.py        ← live capability + context-window probe
│   ├── worktree_manager.py        ← scaffold per-model worktrees
│   └── orchestrator.py            ← plan → gate → dispatch → collect
└── tasks/
    └── SNC_DISC_RESEARCH/         ← first real task (ServiceNow Discovery)
        ├── _PLAN/                 ← charter, clarifications, phases, risks, success
        ├── _ORCHESTRATION/        ← phase_state.json, usage_log.jsonl
        └── worktrees/
            ├── WT1_kilo-ernie-5.5-flash/   ← this agent
            └── WT2_.../                    ← orchestrated peers
```

## Worktree file protocol

Every worktree carries the same contract so the orchestrator (and humans) can audit it
at a glance:

| File | Purpose |
|------|---------|
| `00_WORKTREE.md` | What this worktree is, which model, which task, which branch |
| `01_GOAL.md` | The goal in one paragraph + success criteria |
| `02_OUTPUTFORMAT.md` | The exact format of deliverables |
| `03_FILESSCOPE.md` | Which files this agent is allowed to touch |
| `phases/phaseN.md` | A phase marker written *when the phase starts* (so you can see progress live) |
| `files/` | The actual deliverables |
| `05_QA.md` | Self-QA: did it meet the bar? |
| `06_FINALSUMMARY.md` | Goal achieved? blockers? clarifications needed? |

## Quick start

All commands run **from this folder** (the namespace folder), because `swarm/` lives here:

```bash
cd agents/kilo-ernie-5.5-flash__baidu__kilo

# (stdlib only — nothing to install)
# 1) probe what each free key / local model can actually do
python -m swarm.capability_probe --all

# 2) scaffold a task's worktrees from task.json
python -m swarm.worktree_manager --task SNC_DISC_RESEARCH

# 3) run the swarm (respects usage caps)
python -m swarm.orchestrator --task SNC_DISC_RESEARCH \
    --shared-context tasks/SNC_DISC_RESEARCH/_ORCHESTRATION/shared_context.md

# 4) inspect usage
python -m swarm.usage_tracker --report
```

## Design principles

1. **Capability before assignment.** Never hand a web-research task to a model that can't browse.
2. **Phase markers up front.** If a phase started, a file says so — no silent stalls.
3. **Free-tier safety.** Concurrency, daily request, and daily token caps per provider.
4. **Provenance.** Every worktree names its model/provider explicitly (`docs/agents/*`).
5. **Fail loud, degrade gracefully.** A model that can't do a sub-task hands off to a backup.