# Transcript

- Agent: `qwen3.5-4b__ollama__nvidia-v4`
- Started: 2026-11-13T09:05:00+00:00

## Prompt

```text
You are a skeptical ServiceNow CMDB/Discovery architect reviewing a reference document.

TASK: find concrete gaps, risky claims, and wrong details. Do not rewrite the document.

Rules:
- Base your review on the excerpt below. If you are unsure, say "unsure" instead of inventing.
- Prefer exact property names, table names, and navigation paths.
- No filler, no praise, no summary of the excerpt.

Return markdown with exactly these sections:
## 1. Five highest-risk gaps
## 2. Suspect property names, defaults, or navigation paths
## 3. Three duplicate-prevention tests that would catch regressions
## 4. One thing a real customer would still get wrong after reading this

EXCERPT:
## 5. IRE deep dive

### 5.1 What IRE is

IRE is the centralized framework that processes incoming CI data from Discovery, Service
Mapping, import sets, and third-party sources. It applies:

- **identification rules** — decide which CI is the same CI;
- **reconciliation rules** — decide which source may write which attribute;
- **IRE data source rules** — decide which source may create CIs of a class;
- **data refresh rules** — decide when source data is stale.

It prevents duplicates and prevents non-authoritative sources from overwriting good data.

### 5.2 Payload and identifier keys

Minimal item:

```json
{
  "items": [{
    "className": "cmdb_ci_win_server",
    "values": { "name": "SAMLABVM52" },
    "sys_object_source_info": {
      "source_native_key": "16777219",
      "source_name": "SCCM",
      "source_feed": "SCCM Computer Identity",
      "source_recency_timestamp": "2019-08-26 13:00:00"
    }
  }]
}
```

IRE computes an identifier key from either:

1. `source_name` + `source_native_key` from `sys_object_source_info`, or
2. the identification criterion attributes.

The fast path is the source key; identification-rule matching is slower. The property
`glide.identification_engine.skip_sys_object_source_matching` controls whether IRE skips
that fast path and prioritises rules.

### 5.3 Identification rules

An identification rule applies to one CI class and contains:

- one **CI identifier** (the class the rule applies to);
- one or more **identifier entries** (priority-ordered);
- optional **related entries** (create/update related records; not identification).

Entry types:

| Type | Match basis | Risk |
|---|---|---|
| **Regular** | CI's own attributes | Preferred; fast and predictable. |
| **Lookup** | A related table with a reference to `cmdb_ci` | Slower; can conflict with a direct identifier rule and create duplicates. |
| **Hybrid** | Regular + lookup | Useful when attributes alone are not unique (e.g. duplicate VM serials); still costly. |

**Independent vs dependent**

- **Independent** — CI exists on its own (e.g. Server); rule uses its own attributes.
- **Dependent** — CI cannot exist without a parent (e.g. Network Adapter inside Hardware,
  Application hosted on Server); the parent must be identified first, and relationship
  qualifiers participate in matching.
- A dependent CI can have only **one parent** with dependency. Support is limited to **two
  dependency levels**; prefer one.
- Qualifier chains: if the payload's qualifier chain differs from the DB, IRE updates the
  DB qualifier chain to match.

**Inheritance**

- Child class with no rule inherits the parent's rule, entries, and related entries.
- Child class with its own rule replaces the inherited rule entirely; re-add any needed
  entries/related entries explicitly.

**Design rules (from ServiceNow guidance)**

1. Prefer independent rules.
2. Minimise dependent levels (max 2).
3. Avoid lookup identifier entries.
4. Ideally **one identifier entry per rule**; each extra entry reduces performance.
5. Put the strongest identifier entry at the highest priority.
6. Ensure the rule is at the correct class level.
7. Never create a lookup-based rule for a class that also has its own direct identifier
   rule — contradictory matching can create duplicates.

**Lookup-table rules**

- The lookup table must reference `cmdb_ci`.
- Prefer **Enforce exact count match (Lookup)** for stronger matching.
- Missing lookup records are inserted by IRE during identification.

### 5.4 Reconciliation

Reconciliation decides **which source can write an attribute**, not **which CI it is**.

**Static rules**

- Legacy priority model: list authorized sources and their precedence per class/attribute.
- Stored in `cmdb_reconciliation_definition`.
- Define a rule for every source authorized to update an attribute.
- Parent/child inheritance applies; child rules override parent rules for the covered
  attributes.
- An empty attribute list authorizes **all attributes** of the class.
- Overlapping static rules for different sources can coexist; enforcement prevents
  overwrites.
- Domain separation: rules can be scoped by domain; child domains inherit unless
  overridden.

**Dynamic rules**

- Based on **CMDB 360 / Multisource CMDB** values, not source priority.
- IRE selects the **largest or most reported** value across sources.
- Requires CMDB 360.
- Only one dynamic rule per class attribute.
- Stored in `cmdb_dynamic_reconciliation_definition`.
- Dynamic takes precedence over static for the same attribute at the same class level.
- A child class static rule can still override a parent dynamic rule for that attribute.

**Data refresh rules**

- Declare staleness per source so a lower-priority source can refresh stale data.
- Stored/edited via CI Class Manager; also available for non-CMDB tables.

### 5.5 IRE data source rules

Purpose: let a source **update** CIs but not **create** them.

- Navigation: `All > Configuration > Identification/Reconciliation > IRE Data Source
  Rule`.
- Fields: **Active**, **Applies to** (class + children), **Data source**, **Insert Not
  Allowed**.
- Stored in `cmdb_ire_data_source_rule`.
- Child rules override parent rules.
- Only one active rule per class/source pair.
- Does not apply to lookup or related items.
- Does not apply when dynamic reconciliation is in effect.
- On a blocked insert: error `INSERT_NOT_ALLOWED_FOR_SOURCE`; with
  `CreateOrUpdateCIEnhanced()` the item is stored as a partial payload. With
  `createOrUpdateCI()` the whole payload fails (no partial commits).
- If a permitted source later inserts the CI, IRE merges the partial payload, deletes the
  partial record, and the previously blocked source can update the CI thereafter.

### 5.6 Partial and incomplete items (enhanced API)

`CreateOrUpdateCIEnhanced()` / `identifyCIEnhanced` support:

| Feature | API option | Default | Effect |
|---|---|---|---|
| Partial payloads | `partial_payloads` | on | Stores unmatched items in `cmdb_ire_partial_payloads` for later merge. Enabling it forces partial commits + dedup. |
| Partial commits | `partial_commits` | on | Commits valid items even when others fail. |
| Deduplicate payload | `deduplicate_payloads` | on | Merges duplicate items inside one payload. |
| Summary | `generate_summary` | off | Adds per-class processing counts. |

- **Partial** = not enough data to identify, or one of `MISSING_MATCHING_ATTRIBUTES`,
  `REQUIRED_ATTRIBUTE_EMPTY`, `MISSING_DEPENDENCY`, `INSERT_NOT_ALLOWED_FOR_SOURCE`.
- **Incomplete** = stored for logging only.
- Partial payloads are deleted after **90 days**.
- Identifier keys are stored in `cmdb_ire_partial_payloads_index` to match later payloads.

### 5.7 Timestamps and recency

- `last_discovered` + `discovery_source`: IRE always updates these; a payload timestamp
  only applies if newer than the CMDB value.
- `first_discovered`: set on first insert; on update, only changed if provided.
- `source_recency_timestamp` can update `last_scan` on `sys_object_source`; controlled by
  `glide.identification_engine.skip_updating_last_scan_if_older` and
  `..._ire_message_listener_skip_updating_last_scan_to_now`.
- Related toggles exist for `last_discovered`.

### 5.8 Reclassification

IRE can reclassify a CI when the payload's class differs. Reclassification can be
configured/limited; use it deliberately. Uncontrolled reclassification plus multiple
sources is a common source of "vanishing" CIs and duplicate classes. **[practitioner]**

### 5.9 Identification Simulation

- `All > Configuration > Identification/Reconciliation > Identification Simulation`.
- Build a payload from a CI class (it auto-adds required dependencies and valid
  structure) or paste an existing payload.
- Choose the **data source** (ServiceNow Discovery = `ServiceNow`).
- Optionally use **Enhanced Identification** (`identifyCIEnhanced`).
- **Run Simulation** → inspect Input / Logs / Output; adjust rules; rerun.
- Simulation **does not commit** to the CMDB.
- Use the IE/service-cache log levels to control verbosity.

This is the safest way to test identification-rule changes before production.

---

## 6. Duplicate prevention and insert-vs-update

### 6.1 The decision path (what IRE does, in order)

```
payload item
  │
  ├─ sys_id supplied? ──yes──► direct match → update
  │
  ├─ sys_object_source_info.source_name + source_native_key? ──yes──► key match → update
  │        (unless glide.identification_engine.skip_sys_object_source_matching prioritises rules)
  │
  ├─ identification rule matching
  │     ├─ dependent CI? → identify parent/dependency first, then match with qualifiers
  │     ├─ identifier entries in priority order (regular → lookup → hybrid)
  │     └─ match count:
  │           0 → INSERT (subject to IRE data source rule)
  │           1 → UPDATE
  │           >1 → duplicate set → skip_duplicates logic (below)
  │
  ├─ reconciliation: is this source allowed to write the attribute?
  │     ├─ static: source precedence
  │     └─ dynamic: CMDB 360 largest/most-reported value
  │
  ├─ data source rule: may this source INSERT this class?
  │     └─ no → INSERT_NOT_ALLOWED_FOR_SOURCE → partial payload (enhanced API)
  │
  └─ commit (or partial/incomplete)
```

### 6.2 Duplicate handling at match time

Controlled by:

- `glide.identification_engine.skip_duplicates` (default **true**)
- `glide.identification_engine.skip_duplicates.threshold` (default **5**)
- the number of duplicates found

Behaviour:

| Condition | Result |
|---|---|
| `skip_duplicates=true` and duplicates < threshold | Oldest duplicate is chosen as the match/main CI and updated; the rest get `duplicate_of` set to it. IRE filters `duplicate_of` CIs during matching. |
| `skip_duplicates=false` | Matching fails with an error; none of the duplicates are updated. |
| Duplicates ≥ threshold | See the large-duplicate handling in remediation; `glide.duplicate_ci_remediator.max.cis` applies. |

De-duplication tasks are **always** created when duplicates are detected.

`duplicate_of` is cleared automatically if any other attribute of the duplicate is updated
by IRE — at that point it is no longer treated as a duplicate.

### 6.3 Duplicate detection and remediation

- IRE groups each duplicate set into a **de-duplication task**.
- Choose a **main CI** to retain; duplicates reference it via `duplicate_of`.
- Bulk: **CMDB Workspace → De-duplication dashboard + Template Library**.
- Single: **Duplicate CI Remediator** wizard (attributes, relationships, related items).
- The main CI's `duplicate_of` must be empty; a main CI cannot be deleted until its
  duplicates are disassociated or deleted.
- Asset-related attributes/relationships are not merged (excluded from the default related
  items list).
- Change requests: if the CI is deleted and the change is not `New`, the CI field is
  cleared; if `New`, it is updated to the main CI. Problems/incidents remain valid because
  the main CI is merged in.
- Large sets: >1,000 duplicates restrict remediation; hard cap 5,000. Only recommended
  main-CI selection is available and reconciliation is limited.
- Duplicate serial numbers can create tasks, but relationship merging does not apply.
- Large related-item sets may time out; restricted mode
  (`glide.duplicate_ci_remediator.enable_restricted_mode=true`) limits related items and
  lets remediation proceed.

**Remediation properties**

| Property | Default | Purpose |
|---|---|---|
| `glide.duplicate_ci_remediator.max.field_length` | `4000` | Excludes/truncates long attributes in remediation. |
| `glide.duplicate_ci_remediator.related_items_blacklist` | `cert_task.cmdb_ci,cert_audit_result.configuration_item,discovery_log.cmdb_ci,alm_hardware.ci,alm_asset.ci,fm_expense_line.ci` | Related tables excluded from merge. |
| `glide.duplicate_ci_remediator.max.cis` | `1000` (cap 5000) | Large-set threshold. |
| `glide.duplicate_ci_remediator.dry_run` | `false` | Test remediation without writing. |
| `glide.duplicate_ci_remediator

```

## Response

```text
Thinking Process:

1.  **Analyze the Request:**
    *   **Role:** Skeptical ServiceNow CMDB/Discovery architect reviewing a reference document.
    *   **Task:** Find concrete gaps, risky claims, and wrong details in the provided excerpt.
    *   **Constraints:** Do not rewrite the document. Base review on the excerpt (say "unsure" if unsure). Prefer exact property names, table names, navigation paths. No filler, no praise, no summary.
    *   **Output Format:** Markdown with exactly four sections: 1. Five highest-risk gaps, 2. Suspect property names, defaults, or navigation paths, 3. Three duplicate-prevention tests that would catch regressions, 4. One thing a real customer would still get wrong after reading this.

2.  **Analyze the Excerpt:**
    *   **Section 5.1 (IRE deep dive):** Defines IRE rules (identification, reconciliation, data source, refresh). Claims it prevents duplicates and non-authoritative overwrites.
    *   **Section 5.2 (Payload and identifier keys):** Shows JSON payload structure. Claims IRE computes an identifier key from `source_name` + `source_native_key` OR identification criterion attributes. Mentions property `glide.identification_engine.skip_sys_object_source_matching`.
    *   **Section 5.3 (Identification rules):** Discusses rule types (Regular, Lookup, Hybrid). Independent vs Dependent. Inheritance. Design rules. Claims lookup tables must reference `cmdb_ci`. Claims missing lookup records are inserted by IRE during identification.
    *   **Section 5.4 (Reconciliation):** Static vs Dynamic rules. Static stored in `cmdb_reconciliation_definition`. Dynamic stored in `cmdb_dynamic_reconciliation_definition`. Mentions CMDB 360 for dynamic.
    *   **Section 5.5 (IRE data source rules):** Navigation path: `All > Configuration > Identification/Reconciliation > IRE Data Source Rule`. Table: `cmdb_ire_data_source_rule`. Error `INSERT_NOT_ALLOWED_FOR_SOURCE`. Mentions partial payload handling with `CreateOrUpdateCIEnhanced()`.
    *   **Section 5.6 (Partial and incomplete items):** API options (`partial_payloads`, `partial_commits`, `deduplicate_payloads`). Table: `cmdb_ire_partial_payloads_index`. Partial payloads deleted after 90 days.
    *   **Section 5.7 (Timestamps and recency):** Mentions `last_discovered`, `first_discovered`, `source_recency_timestamp`. Properties like `glide.identification_engine.skip_updating_last_scan_if_older`.
    *   **Section 5.8 (Reclassification):** Mentions uncontrolled reclassification causes "vanishing" CIs.
    *   **Section 5.9 (Identification Simulation):** Navigation path: `All > Configuration > Identification/Reconciliation > Identification Simulation`.
    *   **Section 6.1 (Decision path):** Flowchart logic. Mentions `glide.identification_engine.skip_sys_object_source_matching` again.
    *   **Section 6.2 (Duplicate handling at match time):** Properties: `glide.identification_engine.skip_duplicates`, `glide.identification_engine.skip_duplicates.threshold`. Default threshold 5. Behavior table.
    *   **Section 6.3 (Duplicate detection and remediation):** De-duplication tasks. Bulk via CMDB Workspace. Single via Duplicate CI Remediator. Properties: `glide.duplicate_ci_remediator.max.field_length`, `glide.duplicate_ci_remediator.related_items_blacklist`, `glide.duplicate_ci_remediator.max.cis` (1000 cap 5000).

3.  **Identify Gaps, Risks, and Wrong Details:**

    *   *Gap/Risk:* Section 5.2 says IRE computes an identifier key from `source_name` + `source_native_key`. However, ServiceNow Discovery often uses a different mechanism for native keys (e.g., `sys_id` vs `native_key`). The excerpt implies `source_native_key` is always available and reliable. In reality, Discovery payloads might not always include this if the source feed isn't configured correctly or if it's a non-native key scenario.
    *   *Gap/Risk:* Section 5.3 says "Missing lookup records are inserted by IRE during identification." This is risky. Lookup tables usually need to exist in the CMDB for the relationship to be valid. IRE doesn't typically create the *lookup table record* itself; it matches against existing records or creates a CI if missing, but the phrasing suggests IRE creates the lookup row which might not be accurate.
    *   *Gap/Risk:* Section 5.4 says "Dynamic takes precedence over static for the same attribute at the same class level." However, ServiceNow documentation often states that Static rules are the baseline and Dynamic is an enhancement, but there can be conflicts if domains differ or inheritance levels aren't managed correctly. The claim about dynamic overriding static *at the same class level* might be oversimplified regarding domain scoping.
    *   *Gap/Risk:* Section 5.6 says "Partial payloads are deleted after **90 days**." This is a specific retention policy that might not be accurate or configurable in all versions (e.g., ServiceNow 2023 vs older). It's presented as fact without qualification.
    *   *Gap/Risk:* Section 5.8 says "Uncontrolled reclassification plus multiple sources is a common source of 'vanishing' CIs". While true, the excerpt implies IRE handles this automatically ("IRE can reclassify..."). The risk is that IRE doesn't always prevent it if rules aren't tuned.
    *   *Gap/Risk:* Section 6.2 says "De-duplication tasks are **always** created when duplicates are detected." This contradicts the `skip_duplicates` property logic described in the same section (if `skip_duplicates=true`, it filters them out). The text says "Controlled by... skip_duplicates... De-duplication tasks are always created". This is a contradiction.
    *   *Gap/Risk:* Section 6.3 says `glide.duplicate_ci_remediator.max.cis` default is `1000 (cap 5000)`. ServiceNow documentation often cites different numbers or thresholds depending on the version (e.g., 2024 vs 2023).
    *   *Gap/Risk:* Section 5.5 says "On a blocked insert: error `INSERT_NOT_ALLOWED_FOR_SOURCE`; with `CreateOrUpdateCIEnhanced()` the item is stored as a partial payload." This implies the API handles the block gracefully. However, standard `createOrUpdateCI` fails completely. This distinction is correct but the behavior of partial payloads might vary based on version.
    *   *Gap/Risk:* Section 5.2 says "The fast path is the source key; identification-rule matching is slower." This implies a performance trade-off that might not hold for all payload types (e.g., non-native sources).
    *   *Gap/Risk:* Section 6.1 Decision Path shows `sys_id supplied? -> direct match`. In ServiceNow, if a CI has no sys_id in the payload but is being created, it goes to identification rules. If it has a sys_id, it updates. This is generally correct but the "direct match" logic might not apply to all update scenarios (e.g., partial payloads).
    *   *Gap/Risk:* Section 5.3 says "Prefer **Enforce exact count match (Lookup)** for stronger matching." The property name `cmdb_ci` lookup table reference is correct, but the phrasing "Enforce exact count match" might be a specific feature name that doesn't exist or is misnamed in the excerpt.
    *   *Gap/Risk:* Section 5.6 says "Partial payloads are deleted after **90 days**." This is a very specific number. In ServiceNow, retention policies for partial payloads are often configurable via `cmdb_ire_partial_payloads` table settings or system properties, but 90 days might be a legacy default or incorrect.
    *   *Gap/Risk:* Section 5.4 says "Dynamic takes precedence over static... A child class static rule can still override a parent dynamic rule for that attribute." This is complex inheritance logic. The excerpt simplifies it significantly.
    *   *Gap/Risk:* Section 6.3 says `glide.duplicate_ci_remediator.related_items_blacklist` excludes specific tables. The list includes `cert_task.cmdb_ci`, etc. These table names look correct for ServiceNow, but the property name might be slightly different (e.g., `related_items_blacklist` vs `blacklist`).
    *   *Gap/Risk:* Section 5.2 says "IRE computes an identifier key from either: 1. `source_name` + `source_native_key`... or 2. the identification criterion attributes." This implies a fallback mechanism. However, if the source feed is Discovery, the native key might not be available in the payload structure shown (Discovery often uses `sys_id` or specific discovery keys).
    *   *Gap/Risk:* Section 5.3 says "Child class with its own rule replaces the inherited rule entirely; re-add any needed entries/related entries explicitly." This is generally correct but might miss edge cases where parent rules are still needed for relationships.
    *   *Gap/Risk:* Section 6.2 says "Oldest duplicate is chosen as the match/main CI and updated". ServiceNow's de-duplication logic often chooses based on specific criteria (e.g., most recent, or first found) depending on configuration. The excerpt claims "Oldest" without qualification.
    *   *Gap/Risk:* Section 5.6 says "Identifier keys are stored in `cmdb_ire_partial_payloads_index`". This table name might be incorrect. ServiceNow often uses `cmdb_ire_partial_payloads` for storage, and the index might be internal or named differently (e.g., `cmdb_ire_partial_payloads_index` is plausible but needs verification).
    *   *Gap/Risk:* Section 5.1 says "It prevents duplicates and prevents non-authoritative sources from overwriting good data." This is a general claim that might not hold if the identification rules are misconfigured (e.g., weak rules allow duplicates to pass).

4.  **Drafting the Review:**

    *   **Section 1: Five highest-risk gaps**
        1.  Contradiction in duplicate handling logic (skip_duplicates vs always create tasks).
        2.  Retention policy for partial payloads (90 days) is presented as absolute fact without version qualification.
        3.  Lookup table insertion claim ("Missing lookup records are inserted by IRE") risks data integrity if the lookup table isn't meant to be populated by IRE.
        4.  Dynamic vs Static precedence logic oversimplifies inheritance and domain scoping rules.
        5.  `glide.duplicate_ci_remediator.max.cis` default value (1000) might be version-specific or incorrect for current ServiceNow versions.

    *   **Section 2: Suspect property names, defaults, or navigation paths**
        1.  Property `glide.identification_engine.skip_sys_object_source_matching` is correct but the behavior description ("prioritises rules") is vague.
        2.  Table `cmdb_ire_partial_payloads_index` might be incorrect; ServiceNow often uses `cmdb_ire_partial_payloads` for storage, index details are internal.
        3.  Navigation
```
