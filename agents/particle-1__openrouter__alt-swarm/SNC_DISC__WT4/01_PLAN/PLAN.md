# Plan — particle-1__openrouter__alt-swarm

**Model:** `particle-ai/particle-1:free` · **Provider:** `openrouter` · **Started:** 2026-11-13T09:02:19+00:00

## Goal

Produce the assigned section of the SNC_DISC_RESEARCH reference from the supplied
evidence, without inventing facts.

## Assigned section

Produce the CI Class Manager breadcrumb and workflow section. Give the exact navigation path, role requirements, the class hierarchy navigation, every tab used for class definitions / identification / reconciliation / dependencies / health, the child-class wizard order, and the related screens outside the tool (identification simulation, IRE data source rule, properties). Add a short pre-flight checklist for configuring a new class.

## Phases

1. Confirm evidence digest and constraints.
2. Call the model once (bounded tokens, no tools).
3. Write `05_FINAL/CI_CLASS_MANAGER_BREADCRUMBS.md`.
4. Run automated QA checks.
5. Write final summary and filescope.
6. Commit only `agents/particle-1__openrouter__alt-swarm/` and push the agent branch.

## Success criteria

- 700-1100 words, at least two headings, citations `[S#]`, tables/lists used.
- Every property/table/default is traceable to the digest.
- Gaps are declared rather than guessed.
