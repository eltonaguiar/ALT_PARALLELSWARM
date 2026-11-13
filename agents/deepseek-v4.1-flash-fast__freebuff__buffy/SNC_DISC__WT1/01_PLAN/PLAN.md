# PLAN — SNC_DISC__WT1 (ServiceNow Discovery configuration research)

**Agent:** `deepseek-v4.1-flash-fast__freebuff__buffy`
**Model:** `DeepSeek V4.1 Flash Fast` · **Provider:** Freebuff / Codebuff (Buffy runtime)
**Goal owner:** this worktree. **Deliverable lives in** `05_FINAL/DISCOVERY_CONFIG_REFERENCE.md`.

## Goal

As thorough a technical reference as possible on **ServiceNow Discovery configuration**:

1. configuration options and where each is set (schedule, MID Server, credentials, IP ranges, properties, patterns);
2. **order of operations** — both the *setup* order and the *runtime* probe order;
3. the key **bread crumbs under CI Class Manager** (identification, reconciliation, dependent
   relationships, health), with navigation paths;
4. the configuration that **prevents duplicate CIs** and governs **insert vs update** of CMDB records.

## Output format (fixed now, so nothing drifts later)

`05_FINAL/DISCOVERY_CONFIG_REFERENCE.md`, markdown, numbered sections:

```
0  Evidence policy + release scope
1  Mental model: 4 discovery phases, and where IRE sits
2  Data model / tables you will touch
3  Configuration surface (catalog, grouped by where you set it)
4  Order of operations — setup sequence (A) and runtime sequence (B)
5  Discovery Schedule form, field by field (the ones that matter)
6  IP ranges, range sets, exclusions
7  MID Server selection and scaling
8  Credentials and credential affinity
9  Properties that change Discovery / IRE behaviour
10 CI Class Manager bread crumbs
11 Identification rules (types, entries, pitfalls)
12 Reconciliation rules (static vs dynamic, precedence)
13 Duplicate prevention playbook + insert-vs-update decision table
14 Remediating duplicates you already have
15 Verification: Discovery Status, timelines, CMDB Health
16 Anti-patterns
17 Open questions (explicitly UNVERIFIED)
18 Source ledger
```

Every non-obvious claim carries `[S<n>]` mapping to section 18. Anything I could not source is
marked **UNVERIFIED** and listed in section 17 — no invented property names, no invented UI paths.

## Phases (heartbeat file written in `03_PHASES/` as each starts)

| phase | what | exit condition |
|---|---|---|
| 1 | capability gate | `00_PREREQ/PREREQ.md` says PASS/FAIL |
| 2 | source collection (search → fetch → note) | ≥10 authoritative sources with quotable lines |
| 3 | synthesis | reference doc covers all 4 goal areas |
| 4 | QA | claim-by-claim source check; UNVERIFIED items listed |
| 5 | final summary + filescope | goal met / blockers / clarifications stated |

## Clarifications

See `02_CLARIFICATIONS/CLARIFY.md` — answered inline; none block the work.

## Risks

| risk | mitigation |
|---|---|
| ServiceNow docs are version-drifting ("Brazil" vs "Zurich" vs "Xanadu" pages) | pin every citation to the release label printed on the page; state release-agnostic claims as such |
| Community posts are wrong or stale | use only for corroboration; never as the sole source of a config claim |
| Property names get retyped inconsistently by ServiceNow itself | quote the exact string from docs and flag spelling variants instead of picking one |
| "Thorough" pulling toward a 10k-word dump nobody reads | lead each section with the operational answer, then detail |
| Login-gated KB / instance UI | tag `UNVERIFIED`; never guess a menu path |

## Quality bar (set by the operator mid-run, 2026-11-13)

A good answer is expected to cover all four IRE rule families explicitly:
**identification rules**, **reconciliation rules**, **IRE data source rules**, and **Data Refresh
Rules**. Sections 11, 12, 12A and 12B exist to satisfy that bar; QA checks it line by line.

## Success criteria

- [ ] all 4 goal areas covered with navigation paths a human can follow
- [ ] ≥10 distinct authoritative sources; every section 3–13 cites at least one
- [ ] duplicate-prevention section is actionable (cause → control → where to set it)
- [ ] insert-vs-update decision table distinguishes **identification** from **reconciliation**,
      because conflating them is the #1 source of "why did Discovery create a second CI?"
- [ ] open questions listed rather than papered over
