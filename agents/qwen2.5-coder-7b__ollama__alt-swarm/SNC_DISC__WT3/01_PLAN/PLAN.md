# Plan — qwen2.5-coder-7b__ollama__alt-swarm

**Model:** `qwen2.5-coder:7b` · **Provider:** `ollama` · **Started:** 2026-11-13T09:04:04+00:00

## Goal

Produce the assigned section of the SNC_DISC_RESEARCH reference from the supplied
evidence, without inventing facts.

## Assigned section

Produce the duplicate-prevention and insert-versus-update section. Explain identification-rule strength, the skip_duplicates/threshold behavior, source-native-key matching, data source rules, reconciliation and data refresh, de-duplication tasks, and the exact decision table for insert/update/fail/partial. Include a prevention checklist by layer (design, runtime, detection, remediation).

## Phases

1. Confirm evidence digest and constraints.
2. Call the model once (bounded tokens, no tools).
3. Write `05_FINAL/DUPLICATE_PREVENTION.md`.
4. Run automated QA checks.
5. Write final summary and filescope.
6. Commit only `agents/qwen2.5-coder-7b__ollama__alt-swarm/` and push the agent branch.

## Success criteria

- 700-1100 words, at least two headings, citations `[S#]`, tables/lists used.
- Every property/table/default is traceable to the digest.
- Gaps are declared rather than guessed.
