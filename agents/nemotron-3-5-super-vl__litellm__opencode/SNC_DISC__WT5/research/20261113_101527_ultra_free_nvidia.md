# v3 run

model: ULTRA_FREE_NVIDIA
elapsed: 60.4s
research_calls: 6
error: None

## Question
How do you configure ServiceNow to avoid duplicate CIs and to control whether an existing CI is updated versus a new CI inserted into the CMDB?

## Answer
# Configuring ServiceNow to Avoid Duplicate CIs and Control CI Updates vs. Inserts

ServiceNow uses the **Identification and Reconciliation Engine (IRE)** as the centralized framework that processes all CI payloads—whether from Discovery, Import Sets, Service Mapping, or direct API calls—to decide whether to **update an existing CI** or **insert a new one**. The behavior is governed by three layers of configuration:

---

## 1. Identification Rules — The Primary Duplicate-Prevention Mechanism
**Purpose:** Define the *unique fingerprint* of a CI class so the IRE can find an existing record instead of creating a duplicate.

- **One rule per CI class** (defined at the class level in **CI Class Manager** → *Identification Rule* section)【0†source】.
- Each rule contains **one or more criteria sets** (AND/OR groups of attribute conditions). A payload must satisfy *at least one* complete criteria set to be considered a match【2†source】.
- Typical attributes used: `name`, `serial_number`, `mac_address`, `host_name`, `correlation_id`, etc., chosen per class (e.g., `cmdb_ci_server`, `cmdb_ci_network_gear`).
- **If a match is found** → the IRE proceeds to the *update* path (subject to reconciliation rules).  
  **If no match is found** → the IRE inserts a new CI.

> **Best practice:** Make criteria specific enough to avoid false positives (which cause wrong updates) but broad enough to catch the same CI reported by different sources. Weak criteria are a leading cause of duplicate CIs【1†source】.

---

## 2. Reconciliation Rules — Controlling *Whether* and *How* an Existing CI Is Updated
**Purpose:** Authorize *which data sources* may update *which attributes* and at *what priority*.

- Defined in **Identification/Reconciliation → Reconciliation Rules**【0†source】.
- Each rule binds a **data source** (or group of sources) to a **priority** for a given CI class and attribute set.
- **Insert path:** When the IRE creates a brand-new CI, reconciliation rules are *bypassed*—the record is written regardless of source priority【3†source】.
- **Update path:** For an existing CI, the IRE checks:
  1. Is the incoming source *authorized* by a reconciliation rule for this class/attribute?
  2. Has a *higher-priority* source already written this attribute? If yes, the lower-priority update is **skipped** for that attribute【3†source】.
- This prevents less-reliable sources (e.g., manual spreadsheet imports) from overwriting authoritative sources (e.g., Discovery).

---

## 3. Duplicate-Detection Safety Net (System Properties)
Even with solid identification rules, edge cases can produce duplicates. Two system properties provide a backstop:

| Property | Default | Behavior |
|----------|---------|----------|
| `glide.identification_engine.skip_duplicates` | `true` | When the IRE detects *multiple* CIs matching the same identification criteria, it **picks the oldest** as the “main” CI, updates it, and flags the others as duplicates【1†source】. |
| `glide.identification_engine.skip_duplicates.threshold` | `5` | If the number of duplicates exceeds this threshold, the IRE **stops auto-picking** and instead creates a **de-duplication task** for manual review【1†source】. |

Duplicate CIs are tagged with a `duplicate_of` reference pointing to the main CI and are surfaced in the **CMDB Workspace → CI De-duplication** module for remediation【1†source】.

---

## 4. Inclusion Rules — Narrowing the Scope of Identification
- Optional rules (configured alongside identification rules) that **filter which CIs participate** in the IRE process at all.
- Example: Exclude retired CIs (`install_status = Retired`) so they are never matched or updated.
- **Caution:** Overly broad inclusion rules (e.g., using “Class” as a condition on a parent class) can *cause* duplicates by excluding child-class CIs from identification【1†source】.

---

## 5. Data Source Precedence (cmdb_datasource_precedence)
- A ranked list of data sources (e.g., `ServiceNow Discovery` > `SCCM` > `Manual Import`).
- Used by reconciliation rules to break ties when multiple authorized sources supply the same attribute.
- Maintained in **Configuration → CI Class Manager → Data Source Precedence** (or via the `cmdb_datasource_precedence` table).

---

## Configuration Checklist for Administrators

| Step | Navigation | Action |
|------|------------|--------|
| 1 | **CI Class Manager** | Open each critical CI class → *Identification Rule* → **Edit/Add** criteria sets that uniquely identify the CI (serial number, MAC, correlation ID, etc.). |
| 2 | **Identification/Reconciliation → Reconciliation Rules** | Create rules per class: assign **priority** to each data source for each attribute group (e.g., Discovery = 100 for hardware attrs, SCCM = 50 for software attrs). |
| 3 | **System Properties** (`sys_properties.list`) | Verify/adjust `glide.identification_engine.skip_duplicates` and `glide.identification_engine.skip_duplicates.threshold` for your tolerance. |
| 4 | **CI Class Manager → Inclusion Rules** | Add only if you need to exclude specific CI states (retired, decommissioned) from IRE processing. |
| 5 | **CMDB Workspace → CI De-duplication** | Schedule regular reviews of auto-created de-duplication tasks. |
| 6 | **Data Source Precedence** | Ensure the precedence list reflects your trust hierarchy; reconciliation rules reference this ranking. |

---

## Summary Flow
1. **Payload arrives** → IRE extracts `source_name` + `source_native_key` + identification attributes.
2. **Identification Rule** runs → **Match found?**  
   - **Yes** → Go to *Reconciliation Rules* → Is source authorized & highest priority for each attribute? → **Update allowed attributes**.  
   - **No** → **Insert new CI** (reconciliation rules ignored on insert).
3. **Multiple matches?** → `skip_duplicates` logic picks oldest or creates de-dup task.
4. **Result** → Single authoritative CI per real-world asset, with controlled attribute ownership.

By tightening **identification criteria**, aligning **reconciliation priorities** with your data-source trust model, and monitoring the **duplicate-detection safety net**, you eliminate unintended CI duplication and gain deterministic control over update vs. insert behavior.

**Sources**  
- ServiceNow Docs: *CMDB Identification and Reconciliation*【0†source】  
- ServiceNow Docs: *Detecting duplicate CIs*【1†source】  
- KB1064718: *CMDB Identification and Reconciliation Engine fundamentals*【2†source】  
- KB0756709: *How CMDB reconciliation and data precedence rules work*【3†source】  
- KB0869861: *How to troubleshoot duplicate CMDB CI records*【1†source】

## Transcript
```
[0] research(identification reconciliation avoid duplicate CIs CMDB update existing CI insert new) -> 3186c
[0] research(ServiceNow CMDB avoid duplicate CIs identification rule reconciliation update existing CI ) -> 2616c
[0] research(ServiceNow identification and reconciliation engine identification rule reconciliation rul) -> 2799c
[1] research(create identification rule CMDB CI class criteria attributes) -> 2249c
[1] research(reconciliation rule data source precedence update priority CMDB) -> 2320c
[1] research(ServiceNow identification rule criteria attributes unique CI identification reconciliation) -> 2963c
[2] answer()
```
