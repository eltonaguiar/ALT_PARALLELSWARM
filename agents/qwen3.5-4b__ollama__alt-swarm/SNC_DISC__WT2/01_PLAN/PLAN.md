# Plan — qwen3.5-4b__ollama__alt-swarm

**Model:** `qwen3.5:4b` · **Provider:** `ollama` · **Started:** 2026-11-13T09:04:04+00:00

## Goal

Produce the assigned section of the SNC_DISC_RESEARCH reference from the supplied
evidence, without inventing facts.

## Assigned section

Produce the configuration-option inventory and the canonical order of operations for ServiceNow Discovery. Group options by: identity/IP/hostname, network scanning, scheduling/throughput, and deletion strategy. For the order of operations, start at subscription/roles and end at CMDB governance. Use tables and preserve exact property names and defaults.

## Phases

1. Confirm evidence digest and constraints.
2. Call the model once (bounded tokens, no tools).
3. Write `05_FINAL/CONFIG_OPTIONS_AND_ORDER.md`.
4. Run automated QA checks.
5. Write final summary and filescope.
6. Commit only `agents/qwen3.5-4b__ollama__alt-swarm/` and push the agent branch.

## Success criteria

- 700-1100 words, at least two headings, citations `[S#]`, tables/lists used.
- Every property/table/default is traceable to the digest.
- Gaps are declared rather than guessed.
