# 04 — Duplicate Avoidance & CMDB Insert/Update (IRE)

This is the configuration that governs **whether a discovered item is inserted or updates an
existing CI**, and **how duplicates are prevented**. It is driven by the **Identification and
Reconciliation Engine (IRE)**.

## 1. Two distinct processes (do not conflate)

| Process | Question it answers | When it runs | Driven by |
|---------|--------------------|--------------|-----------|
| **Identification** | Does this CI already exist in the CMDB? | Always (insert **and** update) | **Identification rules** (CI identifiers) or `source_name`+`source_native_key` |
| **Reconciliation** | Which data source is allowed to write each attribute? | **Only on update** | **Reconciliation rules** + **IRE data source rules** |

> Key rule: **reconciliation is NOT applied on insert.** When IRE inserts a new CI, only
> identification matters. Reconciliation only arbitrates competing sources on an existing CI.

## 2. Identification — how a CI is matched

IRE generates **identifier keys** for payload items and matches them against the CMDB:

1. **`source_name` + `source_native_key`** (from `sys_object_source_info`, `Source [sys_object_source]`).
   If present and unique → fastest match, no identifier rules needed.
   Control: `glide.identification_engine.skip_sys_object_source_matching` forces identifier rules
   even when source keys are available.
2. **Identification rules / identifier entries** — criterion attributes that uniquely identify the CI.
3. **sysId** — if a payload provides the CI's sysId, IRE locates it directly.

### Identifier entry types
- **Regular** — the CI's own attributes (e.g. `name` + `serial_number`).
- **Lookup** — a related table referencing the CI (e.g. `cmdb_serial_number`). Lookup records are
  inserted if missing. Prefer **Enforce exact count match** for stronger rules.
- **Hybrid** — regular + lookup combined.

### Identifier-entry best practices (data quality)
1. Prefer **independent** identification rules over **dependent** ones.
2. If dependent rules are required, keep to **a single dependency level** (max two).
3. Avoid **lookup** identifier entries (performance hit).
4. Limit identifier entries per rule — **ideally 1**.
5. Strongest identifier entries / related entries get **highest priority**.
6. Ensure the rule is defined at the **correct class level**.

## 3. Duplicate avoidance (the de-duplication logic)

When IRE finds **multiple existing CIs** matching an incoming CI, it groups them into a
**de-duplication task** and applies these properties:

| Property | Default | Behaviour |
|----------|---------|-----------|
| `glide.identification_engine.skip_duplicates` | **true** | If duplicates ≤ threshold: pick the **oldest** duplicate as the match, make it the **main CI**, tag others with `duplicate_of = <main>`, and filter tagged ones out during matching. |
| `glide.identification_engine.skip_duplicates.threshold` | **5** | The count boundary above. |
| `glide.duplicate_ci_remediator.max.cis` | (varies) | Caps de-duplication processing for very large duplicate sets. |

- If `skip_duplicates = false` → matching **fails with an error** and **none** of the duplicates are updated.
- **De-duplication tasks are always created** regardless.
- Edge case: if IRE updates any attribute **other than** `duplicate_of` on a duplicate CI, that CI is
  **no longer considered a duplicate** and its `duplicate_of` is cleared.

### Duplicate lookup / related items
- Default: IRE does **not** create de-dup tasks for duplicate lookup (`cmdb_serial_number`) or related
  (`cmdb_software_instance`) items.
- `glide.identification_engine.lookup_match.create_duplicate_task_ci.enabled` (default **false**):
  when true, IRE selects the older CI as match **and** creates a de-dup task. When false, older CI is
  matched but no task is created.
- Allowed tables for lookup/related de-dup tasks: `cmdb_duplicate_lookup_related_allowed_class`.

## 4. Reconciliation — who may update an attribute

Only on **update**. Two rule types:

### Static reconciliation rules (legacy)
- Priority order among **discovery sources** (Discovery, ServiceWatch, ImportSet, EventManagement,
  ManualEntry, Tivoli, …) for each CI attribute.
- Stored in `cmdb_reconciliation_definition`.
- **Empty attribute list** = the source may update the **whole class**.
- **Child-class rules override parent-class rules.**
- **Overlapping** static rules (different sources, same attribute) **coexist** — IRE prevents
  overwriting, it does not exclude the other rule.
- Static rule listing specific attributes **overrides** an "all attributes" rule for that class.

### Dynamic reconciliation rules (CMDB 360)
- **Value-based**: IRE picks the **largest / most-reported** value across sources.
- Stored in `cmdb_dynamic_reconciliation_definition`; **one rule per attribute**.
- Requires **CMDB 360** enabled. **Dynamic overrides static** for the same attribute.

### Data refresh rules
- Mark a CI **stale** for a specific source so a **lower-priority** authorized source may update it.
- Last-touch timestamps live in `cmdb_datasource_last_update`.
- Caveat: attribute-level static rules can still block "all-attribute" rules from overriding even
  after staleness expires. **[verify on instance]**

## 5. Insert vs update — the decision path

```
Incoming payload item
   │
   ├─ has source_name + source_native_key? ──yes──► match by source key
   │                                          └─no──► apply identification rules
   │
   ▼
Match found?
   ├─ NO  → INSERT new CI (reconciliation NOT applied)
   └─ YES → UPDATE existing CI
              │
              ├─ duplicate(s) also match? → de-dup task + skip_duplicates logic
              └─ per-attribute: reconciliation rule decides if THIS source may write it
```

## 6. CI reclassification safety flags
In the IRE payload `settings` block, use to prevent unintended class changes:
- `updateWithoutUpgrade`, `updateWithoutDowngrade`, `updateWithoutSwitch`.
- These **override** system reclassification settings. Use when multiple sources update the same CI.

## 7. Payload hygiene (prevents false duplicates / failed matches)
- Limit payload to **≤ 500 CIs**.
- **No duplicate entries** within a payload (duplicate criterion values → match failure).
- Don't pass system fields (`sys_updated_on`, etc.).
- Provide the **minimum** criterion attributes required by the rule.
- Prefer CI **sysIds** when available.

## 8. Troubleshooting duplicates & identification
- Enable `glide.discovery.debug.ci_identification = true` → **CI Identification Log**.
- Review **De-duplication Tasks** and **Reclassification Tasks**.
- Check reconciliation rules at both class and child-class levels.
- Confirm source keys / identifier entries are not weak (a common root cause of duplicates).

## Sources
- Components & process of Identification and Reconciliation — servicenow.com/docs (c_CompsandProcessIDandReconcil)
- Identification and Reconciliation Engine (IRE) — servicenow.com/docs (ire)
- Detecting duplicate CIs — servicenow.com/docs (id-detect-dup-ci)
- Reconciliation rules — servicenow.com/docs (r_ReconciliationRulesPrinciples)
- General guidelines for CMDB Identification — servicenow.com/docs (best-practices-id-reconcile)
- Identification rules — servicenow.com/docs (c_IdentificationRules)