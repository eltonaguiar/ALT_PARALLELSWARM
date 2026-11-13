# QA — SNC_DISC__WT1

**Agent:** `deepseek-v4.1-flash-fast__freebuff__buffy` · `DeepSeek V4.1 Flash Fast` / Freebuff

## Coverage against the brief (and the operator's quality bar)

The operator supplied the bar mid-run: a quality answer covers **identification rules**,
**reconciliation rules**, **IRE data source rules** and **Data Refresh Rules**. Checked explicitly:

| rule family | covered? | where | notes |
|---|---|---|---|
| identification rules | YES | §11 | entries, lookup/hybrid, inheritance, Order, default rules, nil-serial pitfalls |
| reconciliation rules | YES | §12 | static vs dynamic, 8 precedence rules, attribute-list-vs-all, child-over-parent |
| IRE data source rules | YES | §12A | `cmdb_ire_data_source_rule`, separate module path, Insert Not Allowed, derived by children, one active per pair |
| **Data Refresh Rules** | YES (added) | §12B | per-source Effective Duration, static-reconciliation-only, no effect under dynamic rules, non-CMDB `cmdb_datasource_staleness` |
| the three "stale" mechanisms distinguished | YES | §12B table | data refresh (IRE) vs CMDB Health staleness (reporting) vs Data Manager (lifecycle) |

| other asked-for area | where | grade |
|---|---|---|
| Discovery configuration options | §3, §5–§9 | covered: schedule fields, MID selection, credentials, IP ranges/excludes, 14 properties with defaults |
| order of operations | §4A (setup) + §4B (runtime), §15 (observe it) | covered |
| CI Class Manager bread crumbs | §10 | covered, incl. the Data Refresh Rules location and the fact that IRE data source rules are *not* in CI Class Manager |
| avoiding duplicates | §13 (13 causes → control → where) | covered |
| updates / insertion into CMDB | §13 decision table, §12–§12B | covered, incl. insert-vs-update asymmetry and the one rule that can stop an insert |

## Claim discipline

- 28 distinct sources cited; `[S1]`–`[S28]` resolve in §18.
- 0 invented menu paths: every path string traces to a doc page.
- 4 items flagged **UNVERIFIED** in §17 plus a scope note on Data Manager policies.
- One deliberate spelling warning: ServiceNow renders the skip-duplicates property two ways; both are
  shown in §9 instead of guessing.

## Known weaknesses

1. **No instance verification.** Paths are doc-sourced, not clicked; labels drift by release.
2. **Release drift.** Sources span Brazil / Zurich / Xanadu / Washington DC; release-specific claims say so.
3. **Patterns are shallow** (clarification C2) — the natural `SNC_DISC__WT2`.
4. **Data Manager lifecycle policies** named only, not documented (scope note in §17).
5. `last_discovered` write semantics explicitly left UNVERIFIED rather than inferred.

## Verdict

**PASS.** Four rule families the operator asked for are all present, each with its own configuration
path and interaction rules; the distinctions that actually cause production mistakes
(identification vs reconciliation vs data source rule vs data refresh) are stated explicitly.
