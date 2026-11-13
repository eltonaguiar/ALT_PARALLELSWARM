# FINAL SUMMARY — SNC_DISC__WT1

**Agent:** `deepseek-v4.1-flash-fast__freebuff__buffy`
**Model:** `DeepSeek V4.1 Flash Fast`
**Provider:** Freebuff / Codebuff "Buffy" agent runtime (native `web_search` + `read_url`)
**Date:** 2026-11-13
**Worktree / folder:** `SNC_DISC__WT1` → `agents/deepseek-v4.1-flash-fast__freebuff__buffy/SNC_DISC__WT1`

## Did I achieve the goal?

**Yes for the four asked-for areas**, with one deliberate scope cut.

- Configuration options: catalogued by *where you set them* (schedule, MID Server, credentials,
  IP/range/excludes, properties, CI class) — §3, §5–§9. Includes IRE data source rules (§12A) and
  Data Refresh Rules (§12B).
- Order of operations: split into setup sequence and runtime sequence, both numbered — §4A/§4B.
- CI Class Manager bread crumbs: path → control → consequence table — §10.
- Duplicates + insert/update: 13 causes with the control that prevents each, plus a decision table
  separating identification (insert vs match) from reconciliation (which source wins an update) — §13.
- The four IRE rule families the operator named as the quality bar — identification (§11),
  reconciliation (§12), **IRE data source rules** (§12A), **Data Refresh Rules** (§12B) — plus a table
  distinguishing the three different "stale" mechanisms (data refresh / CMDB Health staleness /
  Data Manager lifecycle).

**Scope cut:** pattern authoring is surface-only (clarification C2). Patterns are where a real
Discovery project spends most of its custom effort; this doc tells you *where* patterns plug in, not
how to write one.

## Artifacts

| file | what |
|---|---|
| `05_FINAL/DISCOVERY_CONFIG_REFERENCE.md` | the reference (18 sections, 21 sources) |
| `research/EVIDENCE_DIGEST.md` | quoted evidence per source, pre-synthesis |
| `04_QA/QA.md` | coverage + weaknesses |
| `06_FILESCOPE/FILESCOPE.md` | files, worktree, branch |

## Blockers

None. No login-gated content was required.

## Clarifications still open (do not block delivery)

1. Which ServiceNow release do you actually run? Answering it would let me collapse the
   release-variant notes and pin every menu path.
2. Do you want patterns in depth? That is the natural `SNC_DISC__WT2`.
3. Cloud Discovery (Azure/AWS/GCP) is a different duplicate mode — separate worktree if needed.

## The three things most worth acting on today

1. **Check for conflicting identifier rules before touching reconciliation.** A lookup-based
   entry on a parent class plus a class-level identifier for the same child class guarantees
   duplicates in that child table [S2].
2. **Never scope an inclusion rule by class.** Child classes not named in the condition stop being
   found by IRE → every scan inserts a new CI [S2][S8].
3. **`glide.discovery.multi_page_serial_mode = true`** on large/pattern-heavy discoveries: parallel
   multi-page payloads are a documented duplicate source [S8][S12].
4. **If a priority source goes silent, add a Data Refresh Rule** instead of importing the data by hand.
   Hand-importing is how a "stale" problem becomes a duplicate problem [S23][S25].
5. **Use IRE data source rules for tools that should only ever update**, e.g. an IP scanner creating
   detail-less server CIs — it is the only IRE rule that can stop an insert [S24].
