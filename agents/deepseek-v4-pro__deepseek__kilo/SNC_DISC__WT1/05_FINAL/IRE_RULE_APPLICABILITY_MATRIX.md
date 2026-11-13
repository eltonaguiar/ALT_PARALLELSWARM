# IRE Rule Families — Scope, Insert vs Update, and Controlling Parameters

*Follow-up to `DISCOVERY_CONFIG_REFERENCE.md` (deepseek-v4-pro__deepseek__kilo). Corrects an
oversimplification: the four IRE controls are **not** uniformly "per class, on both insert and update."
Each has a distinct scope, a distinct insert-vs-update applicability, and distinct controlling fields/properties.
All claims cite `docs.servicenow.com` (Brazil release).*

---

## 1. The corrected truth table

| # | Rule family | Scope (granularity) | INSERT? | UPDATE? | Controlling fields / parameters |
|---|---|---|---|---|---|
| 1 | **Identification rules** | One rule **per CI class** (descendants derive from parent unless overridden) | **YES** — "no match → create" | **YES** — "match → update" | Identifier entries (Priority, Criterion Attributes; regular/lookup/hybrid; "Enforce exact count match (Lookup)"); **identification inclusion rule** ("Active record condition"); properties `glide.required.attribute.enabled`, `glide.identification_engine.skip_duplicates[.threshold]`, `…enable_identifier_optional_condition`, `…skip_sys_object_source_matching` |
| 2 | **Reconciliation rules** (static & dynamic) | **Per class + per source + per attribute** (or "Apply to all attributes"); optional **Filter Condition** to a row-subset | **NO** | **YES** — which source may overwrite which field | Static: `Active`, `Discovery Source`, `Priority`, `Apply to all attributes` vs `Attributes`, `Update with Null`, `Filter Condition`. Dynamic: `Dynamic Rule Type`, `Select Attributes`, `Filter Condition`. Property `glide.reconciliation.override.null`, `…enable_reconciliation_filter_before_update` |
| 3 | **IRE data source rules** | **Per class + per source** (one active rule per class/source pair) | **YES — blocks insert** ("Insert Not Allowed") | **NO** — update still allowed | `Active`, `Applies to` (class), `Data source`, `Insert Not Allowed` |
| 4 | **Data refresh rules** | **Per class + per source** | **NO** | **YES** — staleness lets a lower-priority source update | `Discovery source`, `Effective Duration`, `Active` |

**Fifth control (not one of the four):** *Exclude classes from Dynamic IRE* (`cmdb_dynamic_ire_skip_class`) —
when Dynamic IRE is on, a class (and descendants) can be excluded so **Static** IRE rules keep applying to it.

## 2. "All classes, or some classes?" — the answer

- **All four are class-scoped**, and **inherit down the hierarchy**:
  - Identification rules, IRE data source rules: child derives from parent; a child's own rule **overrides** the derived one.
  - Reconciliation rules: "rules defined for a child class override the rules defined for its parent class" (per attribute).
- **Narrower than a whole class** is possible via two mechanisms:
  - **Identification inclusion rule** ("Inclusion Rule (Advanced)") — an `Active record condition` that restricts *which rows of that class* participate (e.g. only `Operational status = Operational`). "When no identification inclusion rules exist, all CIs are included."
  - **Reconciliation `Filter Condition`** — e.g. `[Department] [is] [Finance]` restricts the rule to a subset of CIs.
- **Global switch:** `glide.identification_engine.dynamic_ire_enabled` turns Dynamic IRE on (Static IRE off) instance-wide;
  the `cmdb_dynamic_ire_skip_class` table carves out classes that should keep using Static IRE.

## 3. The parameters that control it

**Per-rule fields** (the "dial" on each rule) — see the last column of §1.

**Identification inclusion rule** (`create-id-inclusion-rule.html`): class-level, one `Active record condition`.
"There are no predefined identification inclusion rules" OOTB. "Impacts any script that calls IRE."

**Reconciliation rule hard limits** (`create-reconciliation-rule.html`):
- You **cannot** create a reconciliation rule for **system fields** or **IRE-specific fields** such as `discovery_source`.
- Rules **cannot be dot-walked** through reference fields.
- Precedence (static): specific-attribute rule > "Apply to all attributes" rule (regardless of priority); class-specific > derived; then priority (smaller number = higher).

**Relevant system properties** (`properties-id-reconciliation.html`) — the global knobs:

| Property | What it controls | Default |
|---|---|---|
| `glide.required.attribute.enabled` | required attrs cannot be null during identification/reconciliation | true |
| `glide.identification_engine.skip_duplicates` + `.threshold` | auto-pick oldest duplicate & mark others `duplicate_of` (below threshold, default 5) | true / 5 |
| `glide.identification_engine.enable_identifier_optional_condition` | advanced conditions on **regular** identifier entries | false |
| `glide.identification_engine.skip_sys_object_source_matching` | prefer IRE identification over `source_native_key` lookup | false |
| `glide.reconciliation.override.null` | allow a **lower-priority** source to fill an **empty** field | true |
| `glide.identification_engine.enable_reconciliation_filter_before_update` | apply reconciliation Filter Condition before vs after value change | false |
| `glide.identification_engine.dynamic_ire_enabled` | use Dynamic IRE instead of Static IRE | false |
| `glide.identification_engine.skip_updating_source_last_discovered_if_older` | don't back-date `last_discovered`/`discovery_source` | true |
| `glide.identification_engine.lookup_match.create_duplicate_task_ci.enabled` | dedup tasks for duplicate lookup items | false |
| `glide.identification_engine.granular_insert_locking` | multiple granular vs single global insert lock | true |
| `glide.identification_engine.batch_update_last_discovered` | batch-update of `last_discovered` | true |

## 4. Extensive permutation examples

Legend: **I** = identification, **R** = reconciliation, **DSR** = IRE data source rule, **DR** = data refresh rule.
"insert" = the payload would create a new CI; "update" = it would modify an existing CI.

### 4.1 Identification — INSERT

1. **I + insert + no match** → new CI is created. A fresh server (`serial = S1`) is discovered, no `cmdb_ci_server` has `S1` → **INSERT**. (`c_IdentificationRules.html`)
2. **I + insert + match found** → not really an insert; the engine flips to **update** of the matched CI. (Identification always runs first; it decides insert-vs-update.)
3. **I + insert + match but excluded by inclusion rule** → the matched CI is *not* considered (e.g. it's `Retired`, and inclusion rule says only `Operational`) → **new CI created** (potential duplicate). (`create-id-inclusion-rule.html`)
4. **I + insert + multiple duplicates** (fewer than threshold) → `glide.identification_engine.skip_duplicates=true` picks the **oldest** match, updates it, sets `duplicate_of` on the rest. (`properties-id-reconciliation.html`)
5. **I + insert + multiple duplicates** (more than threshold) → treated as `skip_duplicates=false`: **match fails, error logged**, no automatic pick.
6. **I + insert + required attribute missing** → `glide.required.attribute.enabled=true` rejects (required criterion attribute is null).

### 4.2 Identification — UPDATE

7. **I + update + strong identifier** (`name` + `serial_number`) → matches existing CI → **update** in place; no duplicate.
8. **I + update + weak/missing identifier** → no match on criterion attributes → **creates a second CI** (the classic "new CI even though same name" bug). (`developer-forum/…/m-p/3590971`)
9. **I + update + `sys_id` provided** → IRE uses `sys_id` to locate the CI directly, ignoring criterion attributes (no match cost). (`best-practices-id-reconcile.html`)
10. **I + update + lookup identifier entry** (matches on a related `Serial Number` row) vs a separate CI identifier on the same table → **contradicting rules can create duplicates** in the lookup table. (`c_IdentificationRules.html` §Guidelines)
11. **I + update + dependent CI** (e.g. Tomcat WAR depends on Tomcat depends on Server) → must identify the parents first; max 2 dependency levels. (`best-practices-id-reconcile.html`)

### 4.3 Reconciliation — UPDATE (this is the only phase reconciliation governs)

12. **R + update + specific attribute, static** → "Discovery is exclusively authorized to update `name` on `cmdb_ci_computer`". Any other source's update to `name` is rejected. (`r_ReconciliationRulesPrinciples.html`)
13. **R + update + "Apply to all attributes" (blank `Attributes`)** → source authorized for the whole class; a specific-attribute rule still overrides it. (`create-reconciliation-rule.html`)
14. **R + update + child overrides parent** → parent says Discovery owns `name`; child `cmdb_ci_linux_server` says ServiceWatch owns `name` → on Linux servers, ServiceWatch wins for `name`. (`r_ReconciliationRulesPrinciples.html`)
15. **R + update + same source re-updates** → allowed.
16. **R + update + higher-priority source** → allowed; it overwrites the lower-priority source's value.
17. **R + update + lower-priority source, field NOT stale, not first writer** → **rejected**.
18. **R + update + lower-priority source is the FIRST writer** (field currently empty) → **allowed** (subject to `glide.reconciliation.override.null=true`).
19. **R + update + `Update with Null`** → by default a source cannot null-out a non-null value; only attributes listed in `Update with Null` may be set null.
20. **R + update + `Filter Condition`** → rule applies only to CIs where `[Department]=[Finance]`; other rows ignore the rule. (`create-reconciliation-rule.html`)
21. **R + update + dynamic rule (largest value)** → with CMDB 360, IRE picks the **largest reported value** across sources, not the highest-priority source.
22. **R + update + static AND dynamic for same attribute** → dynamic wins.
23. **R + update + system field (`discovery_source`)** → **cannot create a rule**; IRE-specific/system fields are excluded. (`create-reconciliation-rule.html`)

### 4.4 IRE data source rule — INSERT

24. **DSR + insert + blocked source** → insert **fails** (`INSERT_NOT_ALLOWED_FOR_SOURCE`); with `CreateOrUpdateCIEnhanced()` the payload is stored in `cmdb_ire_partial_payloads`. (`create-ire-data-source-rule.html`)
25. **DSR + insert + blocked source + plain `createOrUpdateCI()`** → the **entire payload fails** (no partial commits allowed).
26. **DSR + insert + permitted source later inserts same CI** → IRE merges the stored partial payload, deletes it, then the previously-blocked source may update that CI.
27. **DSR + insert + child class** → child derives parent's rule; a child's own rule overrides the derived one.
28. **DSR + insert + lookup/related item** → **does not apply** (data source rules don't cover lookup/related items).
29. **DSR + insert + Dynamic IRE enabled** → **no impact** (dynamic reconciliation is in effect).

### 4.5 IRE data source rule — UPDATE

30. **DSR + update + blocked source** → **allowed**. The whole design intent: "don't trust it to create, but trust it to update existing CIs."

### 4.6 Data refresh rule — UPDATE

31. **DR + update + lower-priority source, within `Effective Duration`** → field not stale → lower-priority source **rejected**.
32. **DR + update + lower-priority source, past `Effective Duration`** → field stale → lower-priority source **allowed** to update. (`create-datasource-staleness-rule.html`)
33. **DR + update + `Effective Duration = 0`** → CI is stale immediately after an update → lower-priority source **always allowed**.
34. **DR + update + "Apply to all attributes" rule vs specific-attribute rule, even when stale** → "a reconciliation rule that applies to all attributes doesn't have precedence over a lower-priority rule that applies to a specific attribute, even if the CI is stale." (`create-reconciliation-rule.html`)
35. **DR + update + Dynamic IRE enabled** → **no impact**.

### 4.7 Cross-cutting combinations

36. **I (match) + R (higher-priority source) + DSR (blocked-insert source) + DR (not stale)** on an **update**:
    identification matches → it's an update; DSR irrelevant (insert-only); R lets the higher-priority source write; DR doesn't trigger (higher-priority source). → clean update.
37. **I (match) + R (lower-priority source) + DR (stale)** on an **update**:
    identification matches; R would normally reject the lower-priority source, but DR says the field is stale → lower-priority source writes the stale field only.
38. **I (no match) + DSR (blocked source)** on an **insert**:
    identification finds no match; DSR blocks the insert → no CI; partial payload stored. (Reconciliation and DR never get a chance — they are update-only.)
39. **Dynamic IRE on + class excluded via `cmdb_dynamic_ire_skip_class`**:
    that class and descendants fall back to **Static IRE** — so static reconciliation, IRE data source rules, and data refresh rules **resume effect** there, where they would be ignored under Dynamic IRE.

## 5. One-line mental model

- **Identification** runs first on **both** insert and update — it only answers *"same CI or new CI?"* (and applies inclusion rules).
- **IRE data source rule** is the **insert** gate — *"may this source create this class?"*
- **Reconciliation** + **data refresh** are the **update** gates — *"may this source overwrite this field, and is it stale enough to hand off to a lower-priority source?"*
- Dynamic IRE (CMDB 360) supersedes the static update gates and neutralizes IRE data source + data refresh rules, unless the class is explicitly excluded.
