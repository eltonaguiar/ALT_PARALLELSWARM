# Plan — SNC_DISC_RESEARCH

**Agent:** `deepseek-flash__openrouter__kilo-cli`
**Model:** `deepseek/deepseek-flash` · **Provider:** OpenRouter (inferred) · **Harness:** Kilo CLI
**Planned:** 2026-11-13T08:50Z

## Goal

Produce the most complete, source-cited configuration reference possible for the
**ServiceNow Discovery** module (Brazil release), covering:

1. all material configuration options and their interactions;
2. the correct order of operations to stand Discovery up;
3. the key navigation breadcrumbs inside **CI Class Manager**;
4. how configuration prevents duplicate CIs and controls **insert vs. update** in the CMDB;
5. risks, validation steps, and explicit clarifications.

## Output format

- Primary document: `05_FINAL/DISCOVERY_CONFIG_REFERENCE.md`
  - Markdown, tables for options, exact property names and defaults, canonical doc URL
    after each section.
- Evidence file: `research/SOURCES.md` (topic → API URL → canonical page).
- QA: `04_QA/QA.md` with a requirement-by-requirement pass/fail and evidence.
- Final summary: goal met? blockers? clarifications?
- Dated run report: `runs/2026-11-13T0846Z_.../REPORT.md`.

## Phases and heartbeat policy

A phase file is written **when the phase starts**, not after it finishes. If the run is
interrupted, the last heartbeat identifies exactly where it stopped.

| Phase | Name | Output | Exit criterion |
|---|---|---|---|
| 0 | Prerequisite gate | `00_PREREQ/PREREQ.md` | Browse path proven end-to-end |
| 1 | Discover the documentation corpus | `research/SOURCES.md` | Map + 60 topic IDs resolved |
| 2 | Retrieve authoritative content | `research/raw/` + `_meta.json` | ≥ 50 topics fetched, < 5 hard failures |
| 3 | Extract the configuration model | `03_PHASES/phase3_extract.md` | Order of operations + option inventory drafted |
| 4 | Write the reference | `05_FINAL/DISCOVERY_CONFIG_REFERENCE.md` | All 12 sections complete and cited |
| 5 | Build and test the swarm harness | `swarm/` | Tracker enforces quotas; one dry-run passes |
| 6 | Dispatch parallel workers | `swarm/ORCHESTRATION.md` | ≥ 2 workers complete in isolated worktrees |
| 7 | QA and final summary | `04_QA/QA.md`, `05_FINAL/FINAL_SUMMARY.md` | Success criteria scored |

## Success criteria

| # | Criterion | Measurement |
|---|---|---|
| SC1 | Coverage: options across Discovery properties, schedules, IP ranges, MID/behaviors, classifiers, identifiers, IRE, duplicates | Section present with named properties |
| SC2 | Correct order of operations | Ordered phase list with prerequisites and exit checks |
| SC3 | CI Class Manager breadcrumbs | Exact nav path + tab/operation map |
| SC4 | Duplicate prevention + insert/update control | Mechanism, properties, decision table, remediation |
| SC5 | Traceability | Every non-obvious claim has a ServiceNow docs source |
| SC6 | No fabricated URLs/properties | Spot-check every property name against fetched text |
| SC7 | Honest limitations | Blockers/clarifications section present |
| SC8 | Parallel orchestration demonstrated | ≥ 2 worker worktrees with phase docs and commits |
| SC9 | Safe free-tier usage | Tracker enforces per-provider inflight/daily caps and cost |

## Risks and mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Docs API changes or blocks unauthenticated access | Medium | High | Capture raw content immediately; cite API + canonical URL; Playwright fallback |
| Release drift (Brazil vs. older docs) | High | Medium | Declare release/date at the top; use Brazil map only |
| Confusing probe-based vs. pattern-based identification | High | High | Explicit two-path section and decision table |
| Over-generalizing "duplicate prevention" | Medium | High | Separate design-time rules, runtime IRE properties, and remediation |
| Free-tier keys rate-limit or fail mid-run | Medium | Medium | Provider ledger with caps; fall back to local Ollama; never retry blindly |
| Local model output is low quality | High | Low | Workers are independent drafts; primary doc is human/agent-reviewed; QA scores each |
| Context overload | Medium | Medium | Fetch to files, read selectively; keep the digest per worker small |
| Stale/incorrect UI labels | Medium | Medium | Use docs wording; put UI paths in backticks and cite source |

## Clarifications needed before a *production* run

1. Target ServiceNow release and patch level (this reference uses Brazil).
2. Whether the customer uses probe-based discovery, pattern-based discovery, or both.
3. Existing data sources and their authority order (IRE reconciliation design depends on it).
4. Whether CMDB 360 and dynamic IRE are licensed/enabled.
5. Scope of "duplicate" — CI duplicates only, or also lookup/related item duplicates.

These do not block the documentation research; they block customer-specific tuning.
