# Coverage Gap Analysis — my findings vs. the Discovery guide

**Compared against:** `eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/modules/discovery/discovery-guide/`
**My findings source:** `results/…/DISCOVERY_CONFIG_REFERENCE.md` (deepseek-v4-pro__deepseek__kilo)

Verdict per finding: ✅ already covered · ⚠️ partial · ❌ not covered (my reference fills the gap).

| # | My condensed finding | In discovery-guide? | Evidence in guide |
|---|---|---|---|
| 1 | **4-phase order of operations** — Scan (Shazzam) → Classify → Identify → Explore, via ECC queue + MID Server | ✅ **FULLY covered** | "Discovery Phases — Scan → Classify → Identify → Explore" mermaid + "How Discovery Works" section + "MID Server → ECC Queue → CI Flow" diagram |
| 2 | **CI Class Manager bread crumbs** (Identification / Reconciliation / Dependencies tabs; IRE Data Source Rule location) | ❌ **NOT covered** | 0 hits for "CI Class Manager". Only "All > Configuration > Identification/Reconciliation (CI Identifiers)" appears (line ~617). No Reconciliation tab, no Data Refresh Rules section, no IRE Data Source Rule path. |
| 3 | **Four IRE rule families** — identification, reconciliation, IRE data source, data refresh | ⚠️ **PARTIAL** | **Identification rules:** high-level only ("`cmdb_identifier` and its entries, per CI class… match an incoming payload to an existing CI"). **Reconciliation:** mnemonic-only ("IRE — Identification Before Reconciliation" + "Order vs Priority" lower-number-wins), no static/dynamic/precedence detail. **IRE data source rules:** 0 hits. **Data refresh rules:** 0 hits ("staleness" 0; "stale" only in KPI/SLA context, not the rule config). |
| 4 | **Insert vs update mechanics** — identification ≠ field-update; no change → no write → `sys_updated_on` unchanged; `last_discovered`/`discovery_source` always refresh; `install_status` not auto-reactivated | ⚠️ **MINIMAL** | "identify = match existing or create new" is stated. But `sys_updated_on` 0 hits; `install_status` 1 hit (only the "Retire Before Delete" mnemonic); "insert" 1 hit (Transform Script "Coalesce = Match" mnemonic). The no-write / lifecycle nuance is absent. |

## Net result

- **Finding 1 is redundant with the guide** — the Discovery guide already nails the 4 phases and ECC/MID flow.
- **Findings 2–4 are where my reference adds value the guide does not have**, specifically:
  1. **CI Class Manager** navigation (tabs + IRE Data Source Rule module path).
  2. **Reconciliation rules** — static vs dynamic, the four precedence principles, `cmdb_reconciliation_definition` / `cmdb_dynamic_reconciliation_definition`.
  3. **IRE data source rules** — "Insert Not Allowed", `cmdb_ire_data_source_rule`, partial payloads.
  4. **Data refresh rules** — "Effective Duration" staleness semantics, lower-priority-takeover.
  5. **Insert-vs-update nuance** — separate identification vs field-update steps, `sys_updated_on` no-write behaviour, `install_status` not in the OOTB payload.

## Recommendation

The Discovery guide should get a new subsection (or the **CMDB guide**, which owns IRE, should) covering the
**"four IRE rule families + CI Class Manager"** material that Findings 2–4 carry — that is the part of
SNC_DISC_RESEARCH the guide currently leaves to the reader to find in `docs.servicenow.com`.
