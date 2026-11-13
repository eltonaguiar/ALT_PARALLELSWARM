# ServiceNow Discovery Configuration — Consolidated Master Reference

> **Merged from 10+ agent outputs, de-duplicated, validated, and augmented with flowcharts**
> **Release scope:** Brazil (primary) / Australia (new-customer defaults noted)
> **Last updated:** 2026-11-13

---

## 📋 TABLE OF CONTENTS

1. [Quick-Start Mental Model](#1-quick-start-mental-model)
2. [Discovery Phases & Runtime Order](#2-discovery-phases--runtime-order)
3. [Configuration Surface Catalog](#3-configuration-surface-catalog)
4. [CI Class Manager — Breadcrumbs & Wizard](#4-ci-class-manager--breadcrumbs--wizard)
5. [IRE — The Four Rule Families](#5-ire--the-four-rule-families)
6. [Insert vs Update Decision Logic](#6-insert-vs-update-decision-logic)
7. [Duplicate Prevention Playbook](#7-duplicate-prevention-playbook)
8. [Discovery Source A vs B Decision Matrix](#8-discovery-source-a-vs-b-decision-matrix)
9. [Properties Reference (Brazil + Australia Deltas)](#9-properties-reference-brazil--australia-deltas)
10. [Verification & Observability](#10-verification--observability)
11. [Anti-Patterns (25 Confirmed)](#11-anti-patterns-25-confirmed)
12. [Coverage Gaps & Unexplored Sources](#12-coverage-gaps--unexplored-sources)

---

## 1. QUICK-START MENTAL MODEL

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         DISCOVERY → CMDB PIPELINE                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  SCHEDULE → MID SERVER → SHAZZAM (scan) → CLASSIFY → IDENTIFY → EXPLORE│
│                                                                    │    │
│                                                                    ▼    │
│                                                              ┌─────────┐ │
│                                                              │   IRE   │ │
│                                                              │ PIPELINE│ │
│                                                              └────┬────┘ │
│                                                                   │     │
│                              ┌────────────────────────────────────┼────┐ │
│                              ▼                                    ▼    ▼ │
│                       ┌──────────┐                       ┌──────────┐     │
│                       │  MATCH?  │                       │ NO MATCH │     │
│                       └────┬─────┘                       └────┬─────┘     │
│                            │                                 │           │
│                            ▼                                 ▼           │
│                     ┌──────────────┐                ┌─────────────────┐  │
│                     │ RECONCILIATION │               │ IRE DATA SOURCE │  │
│                     │   (update)     │               │   RULE (insert) │  │
│                     └──────┬─────────┘               └────────┬────────┘  │
│                            │                                  │           │
│                            ▼                                  ▼           │
│                     ┌──────────────┐                ┌─────────────────┐  │
│                     │ DATA REFRESH │                │ INSERT / BLOCKED│  │
│                     │   (staleness)│                │  (partial ok)   │  │
│                     └──────┬─────────┘               └─────────────────┘  │
│                            │                                               │
│                            ▼                                               │
│                     ┌──────────────┐                                       │
│                     │  CMDB WRITE  │                                       │
│                     │ (last_disc,  │                                       │
│                     │ discovery_s) │                                       │
│                     └──────────────┘                                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Key separation:**
- **Identification** runs first on BOTH insert and update — answers "same CI or new CI?"
- **IRE Data Source Rule** is the **insert gate** — "may this source CREATE this class?"
- **Reconciliation + Data Refresh** are **update gates** — "may this source OVERWRITE this field?"

---

## 2. DISCOVERY PHASES & RUNTIME ORDER

### 2.1 Setup Sequence (one-time)

| Step | Action | Where | Role |
|------|--------|-------|------|
| 1 | Provision MID Server(s) | Physical/virtual hosts | `discovery_admin` |
| 2 | Assign MID Server apps | MID Server record | `discovery_admin` |
| 3 | Configure credentials | Instance (UNIX/SNMP) or MID service login (Windows) | `discovery_admin` |
| 4 | Create IP ranges / range sets | `Discovery > IP Ranges` | `discovery_admin` |
| 5 | Create Discovery Schedule | `Discovery > Schedules` | `discovery_admin` |
| 6 | Configure CI Class Manager | `All > Configuration > CI Class Manager` | `sn_cmdb_admin` + `itil_admin` + `personalize_dictionary` |

### 2.2 Runtime Sequence (per device)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        RUNTIME FLOW (per device)                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. SHAZZAM SCAN                                                        │
│     ├─ MID Server launches Shazzam probe                               │
│     ├─ ICMP/SNMP/TCP port scan                                         │
│     ├─ Results → ECC Queue → Instance                                  │
│     └─ OPEN PORTS → Classification                                     │
│                                                                         │
│  2. CLASSIFICATION                                                      │
│     ├─ Device classifier → OS/device type                              │
│     ├─ Process classifier → running processes (exploration phase)      │
│     ├─ IP scan classifier → banner typing (no CI write)                │
│     └─ Criteria: parameter operator value (case-sensitive for process) │
│                                                                         │
│  3. IDENTIFICATION (IRE)                                               │
│     ├─ Fast path: source_name + source_native_key in sys_object_source │
│     │   (skipped if glide.identification_engine.skip_sys_object_source  │
│     │    _matching=true)                                                │
│     ├─ Identifier rule matching: criterion attributes                  │
│     │   ├─ Regular entry (CI table) → preferred                        │
│     │   ├─ Lookup entry (cmdb_ci_network_adapter, cmdb_serial_number)  │
│     │   └─ Hybrid entry (both)                                         │
│     ├─ Inclusion rule filter (Active record condition)                 │
│     └─ Outcome: MATCH → update path | NO MATCH → insert path          │
│                                                                         │
│  4. RECONCILIATION (update path only)                                  │
│     ├─ Static: source priority per class/attribute                     │
│     ├─ Dynamic: CMDB 360 value-based (wins over static)               │
│     ├─ Specific-attribute rule > all-attributes rule (always)         │
│     ├─ Child-class rule > parent-class rule                           │
│     ├─ Filter Condition scopes to row subset                          │
│     ├─ glide.reconciliation.override.null=true (default)              │
│     └─ Update with Null: only listed attrs may be nulled              │
│                                                                         │
│  5. DATA REFRESH (update path, static reconciliation only)             │
│     ├─ Measures staleness via cmdb_datasource_last_update             │
│     ├─ Effective Duration = 0 → immediately stale                     │
│     ├─ Stale → lower-priority source allowed (if authorized by recon) │
│     └─ NO EFFECT under Dynamic IRE                                     │
│                                                                         │
│  6. EXPLORATION                                                        │
│     ├─ Credentialed probes/patterns run                               │
│     ├─ Collects: hardware, software, relationships, processes         │
│     ├─ File-Based Discovery (FBD): cmdb_file_information, etc.        │
│     └─ Configuration Console filters what gets written                │
│                                                                         │
│  7. CMDB COMMIT                                                        │
│     ├─ last_discovered = now                                           │
│     ├─ discovery_source = source_name                                  │
│     ├─ sys_updated_on NOT updated if no field changed (KB3222102)     │
│     └─ install_status NOT auto-flipped from Retired (KB0755747)       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. CONFIGURATION SURFACE CATALOG

### 3.1 Discovery Schedule — Field Reference

| Field | Purpose | Guidance |
|-------|---------|----------|
| **Discover** | What to scan: Configuration items, IP addresses, Networks, Service, Serverless, Cloud application, Cloud resources, Certificates | Use **Configuration items** for CMDB population; IP scans don't update CMDB |
| **MID Server selection** | Auto-Select, Specific MID Cluster, Specific MID Server, Use Behavior | Auto-Select for simple; Behavior for multi-domain/ACL/load balancing |
| **Max run time** | Cancels remaining tasks at limit | Match change window |
| **Max Idle time** | Cancels stalled runs (hidden by default) | Add column, set for safety |
| **Shazzam batch size** | IPs per Shazzam probe (default 1000) | Min effective 256; larger = less overhead, slower classification |
| **Run options** | On Demand, Daily, Weekly, Monthly, Periodically, Once, Weekdays, Weekends, Month Last Day, Calendar Quarter End, **After Discovery** | `After Discovery` chains schedules; `Even if canceled` decouples chain |

**Concurrency guard:** `glide.discovery.max_concurrent_invocations_per_schedule` = 3 (0/neg disables). Doesn't apply to `After Discovery` + `Even if canceled`.

### 3.2 Behaviors (Multi-MID Orchestration)

| Component | Description |
|-----------|-------------|
| **Functionality** | Protocol set (SSH, WMI, SNMP, etc.) |
| **MID Server assignment** | Which MID Server(s) run this functionality |
| **Phase** | Integer; same-phase functionalities share one Shazzam pass |
| **Criteria** | `mid_server`, `win_domain`, `mid_win_domain` — gates Windows MIDs to domains |
| **When to use** | Multiple Windows domains, SNMP ACLs, SSH vs SNMP preference, load balancing |

---

## 4. CI CLASS MANAGER — BREADCRUMBS & WIZARD

### 4.1 Navigation & Roles

```
All > Configuration > CI Class Manager
```

| Task | Required Role(s) |
|------|------------------|
| General access (full) | `sn_cmdb_admin` |
| General access (read) | `sn_cmdb_editor` |
| Create child class | `sn_cmdb_admin` OR `itil_admin` + `personalize_dictionary` |
| Dependent relationship rules (read) | `sn_cmdb_editor` + `itil` |
| Dependent relationship rules (full) | `sn_cmdb_admin` + `itil_admin` |
| Identification simulation | `sn_cmdb_admin` OR `admin` |

**Not in CI Class Manager:** IRE Data Source Rules (see §5.2)

### 4.2 Tool Navigation

```
CI Class Manager
└── Hierarchy → select class (Add Child Class only if Is_Extendable=true)
    ├── Class Info
    │   ├── Basic Info (label ≤80, table auto u_cmdb_ci_*, Extensible, Principal Class)
    │   ├── Attributes (per column; double-click Identification Rule col → true = identifier)
    │   ├── Reconciliation Rules → static + Data Refresh Rules (Add)
    │   └── Suggested Relationships (Query Builder)
    ├── Identification
    │   ├── Identification Rule (entries + optional condition)
    │   └── (d) Dependent Rules → hosting/containment (if dependent ID rule exists)
    └── Health
        ├── Compliance Audit
        ├── Certification Template
        ├── Orphan Rule
        ├── Staleness Rule
        ├── Mandatory/Recommended Attributes
        └── Health Inclusion Rules
```

### 4.3 Child-Class Wizard Order

1. **Provide Basic Info** — label, table name, description, icon, Extensible, Principal Class
2. **Add Attributes** — add columns; mark identifier cols via Identification Rule column = true
3. **Set Identification Rule** — inspect derived rule; **Replace** to author class-specific entries
4. **Dependencies** — add dependent rules (conditional on dependent ID rule existing)
5. **Add Reconciliation Rules** — add Reconciliation Rules + Data Refresh Rules
6. **Add Suggested Relationships** — review derived diagram; add Relationship + Target Class

### 4.4 Related Screens Outside CI Class Manager

| Task | Path |
|------|------|
| Identification Simulation | `All > Configuration > Identification/Reconciliation > Identification Simulation` |
| IRE Data Source Rules | `All > Configuration > Identification/Reconciliation > IRE Data Source Rule` (guide: **Data Sources**) |
| Identification Inclusion Rules | `All > Configuration > Identification/Reconciliation > Identification Inclusion Rules` |
| CMDB IRE Properties | `All > Configuration > CMDB Properties > Identification/Reconciliation Properties` |
| Discovery Properties | `All > Discovery > Discovery Definition > Properties` |
| Metadata Editor (hosting/containment) | `All > Configuration > Metadata Editor` |
| Domain Overrides | `All > Configuration > Domain Support > Domain Overrides` (CMDB) |

### 4.5 Pre-Flight Checklist (New Class)

- [ ] Parent class `Is_Extendable=true`
- [ ] Operator has `sn_cmdb_admin`/`itil_admin` + `personalize_dictionary`
- [ ] Display name ≤80 chars; table name remainder after `u_cmdb_ci` prefix
- [ ] Principal Class decision made
- [ ] Attributes prepared; identifier cols marked
- [ ] Derived identification rule accepted OR Replaced
- [ ] Dependent ID rule exists if Dependencies needed
- [ ] Reconciliation + Data Refresh rules prepared
- [ ] Suggested relationships prepared
- [ ] **Identification Simulation PASS** before first broad scan

---

## 5. IRE — THE FOUR RULE FAMILIES

### 5.1 Canonical Truth Table

| # | Rule Family | Table | Scope | INSERT? | UPDATE? | Controlling Fields |
|---|-------------|-------|-------|---------|---------|-------------------|
| 1 | **Identification Rule** | `cmdb_identifier` + `cmdb_identifier_entry` | Per class (inherited; child overrides) | **YES** — no match → create | **YES** — match → update | Entries (Priority, Criterion Attrs; regular/lookup/hybrid); Inclusion Rule (Active record condition); Props: `skip_duplicates`, `threshold`, `enable_identifier_optional_condition`, `skip_sys_object_source_matching` |
| 2 | **Reconciliation Rule** | `cmdb_reconciliation_definition` (static) / `cmdb_dynamic_reconciliation_definition` (dynamic) | Per class + per source + per attribute (or all); Filter Condition optional | **NO** | **YES** — which source overwrites which field | Static: Active, Discovery Source, Priority (lower=higher), Apply to All vs Attributes, Update with Null, Filter Condition. Dynamic: Dynamic Rule Type, Select Attributes, Filter Condition. Props: `glide.reconciliation.override.null`, `enable_reconciliation_filter_before_update` |
| 3 | **IRE Data Source Rule** | `cmdb_ire_data_source_rule` | Per class + per source (one active per pair; child overrides) | **YES — blocks** ("Insert Not Allowed") | **NO** | Active, Applies to (class), Data source, Insert Not Allowed |
| 4 | **Data Refresh Rule** | Same as Reconciliation UI (Effective Duration / Refreshable) or `cmdb_datasource_staleness` (non-CMDB) | Per class + per source | **NO** | **YES — stale ⇒ lower-priority allowed** | Discovery source, Effective Duration (0 = always stale), Active |

**Fifth control:** `cmdb_dynamic_ire_skip_class` — excludes class+descendants from Dynamic IRE (keeps Static IRE).

---

### 5.2 IRE Pipeline Flowchart

```mermaid
flowchart TD
    Payload[Payload Item Arrives] --> FastPath{Fast Path:<br/>source_name + source_native_key<br/>in sys_object_source_info?}
    
    FastPath -->|Yes & skip_sys_object_source_matching=false| UpdatePath[UPDATE Existing CI]
    FastPath -->|No OR skip_sys_object_source_matching=true| IdMatch[Identification Rule Matching]
    
    IdMatch --> Match{Match Found?}
    
    Match -->|Yes| InclusionCheck{Inclusion Rule<br/>Allows This CI?}
    Match -->|No| DSRGate[IRE Data Source Rule Gate]
    
    InclusionCheck -->|Yes| Reconcile[Reconciliation Rules]
    InclusionCheck -->|No| InsertPath[INSERT New CI<br/>⚠️ Potential Duplicate]
    
    Reconcile --> StaticOrDynamic{Static or Dynamic<br/>Reconciliation?}
    
    StaticOrDynamic -->|Static| DataRefresh{Data Refresh Rule<br/>Stale?}
    StaticOrDynamic -->|Dynamic| CMDBWrite[CMDB Write<br/>Dynamic wins]
    
    DataRefresh -->|Not Stale| CMDBWrite
    DataRefresh -->|Stale & Lower-Priority<br/>Source Authorized| CMDBWrite
    DataRefresh -->|Stale but No Auth| SkipField[Field Skipped]
    
    DSRGate --> DSRBlocked{Insert Not Allowed?}
    DSRBlocked -->|Yes| PartialPayload[Partial Payload Stored<br/>CreateOrUpdateCIEnhanced()]
    DSRBlocked -->|No| InsertCI[INSERT New CI]
    
    CMDBWrite --> Done[Complete]
    InsertCI --> Done
    PartialPayload --> Done
    SkipField --> Done
    InsertPath --> Done
    
    classDef fast fill:#e8f5e9,stroke:#2e7d32
    classDef gate fill:#fff3e0,stroke:#ef6c00
    classDef write fill:#e3f2fd,stroke:#1565c0
    classDef decision fill:#fce4ec,stroke:#c2185b
    
    class FastPath,UpdatePath fast
    class DSRGate,InclusionCheck,DSRBlocked gate
    class CMDBWrite,InsertCI,PartialPayload write
    class Match,StaticOrDynamic,DataRefresh decision
```

---

### 5.3 Identification Rules — Deep Dive

**Identifier Entry Types:**

| Type | Source | Use When | Performance |
|------|--------|----------|-------------|
| **Regular** | CI's own table (or inherited `cmdb_ci` fields) | Preferred — identifying attr lives on CI | ⭐ Fastest |
| **Lookup** | Related table (`cmdb_ci_network_adapter` for MAC, `cmdb_serial_number`) | Identifying attr genuinely lives on related table | ⚠️ Join cost; avoid when regular works |
| **Hybrid** | Both CI table + related table | Neither source alone is unique | ⚠️ Complex |

**Rules:**
- One rule per class (descendants derive until child defines own)
- Order: low → high (defaults 100/200); custom must use different Order
- Strongest entry FIRST (lowest Order)
- Limit entries — ideally **one**
- Avoid Lookup entries; if unavoidable, add `Enforce exact count match`
- `sys_class_name` CANNOT be entry for independent rules
- Child rule **REPLACES** parent entirely — must re-add related entries
- Deactivate (Active=false) instead of deleting

**Default Base-System Rules:**

| Rule | Class | Attributes |
|------|-------|------------|
| Hardware | `cmdb_ci_hardware` | `serial_number`, `serial_number_type`, `name`, `ip_address`, `mac_address` + Serial Number & Network Adapter lookups |
| ESX Server | `cmdb_ci_esx_server` | `correlation_id` |
| Storage Server | `cmdb_ci_storage_server` | `cim_object_path`, `name`, serial fields, `mac_address`, `ip_address` + lookups |
| WBEM Service | `cmdb_ci_wbem_service` | `cim_object_path` |

---

### 5.4 IRE Data Source Rules — Insert Gate

**Purpose:** Prevent a source from CREATING new CIs of a class. **Create-only gate.**

- Config: `All > Configuration > Identification/Reconciliation > IRE Data Source Rule`
- Fields: **Active**, **Applies to** (class + children), **Data source**, **Insert Not Allowed**
- Child derives parent; child's own rule overrides
- **Only evaluated when identification finds NO MATCH**
- **No effect on updates** — blocked source CAN update existing CIs (subject to Reconciliation)
- **No effect under Dynamic IRE** (Dynamic wins)
- `INSERT_NOT_ALLOWED_FOR_SOURCE` logged; Enhanced API stores partial payload

**Example:** IP-scan tool discovers network gear but creates thin server CIs → Block that source from inserting `cmdb_ci_server`; it can still update servers Discovery created.

---

### 5.5 Reconciliation Rules — Update Authority

**Static Reconciliation:**
- One rule per authorized source + attribute (or all-attributes)
- Priority: **lower number = higher authority**
- Specific-attribute rule **ALWAYS beats** all-attributes rule (regardless of priority)
- Child-class rule beats parent (attr-specific across static/dynamic)
- Overlapping static rules coexist — enforced via `cmdb_datasource_last_update`
- `glide.reconciliation.override.null=true` (default) — lower-priority may fill empty field
- Cannot target system/IRE fields (`discovery_source`, etc.); no dot-walking

**Dynamic Reconciliation:**
- CMDB 360 value-based (largest/most-reported)
- **Wins over static** for same attribute
- One dynamic rule per class+attribute
- Requires CMDB 360 license + enable

---

### 5.6 Data Refresh Rules — Staleness Override

**Purpose:** Let lower-priority source refresh when higher-priority source's data is stale.

- Config: CI Class Manager → Class Info → Reconciliation Rules → Data Refresh Rules → Add
- Fields: **Discovery source**, **Effective Duration**, **Active**
- **Effective Duration = 0** → immediately stale → lower-priority always allowed
- Refresh can ONLY write fields authorized by Reconciliation Rules
- **NO EFFECT under Dynamic IRE**
- Uses `cmdb_datasource_last_update` (Data Source History), NOT `sys_updated_on`
- NOT the same as CMDB Health staleness KPI or Data Manager lifecycle policies

---

## 6. INSERT VS UPDATE DECISION LOGIC

### 6.1 Complete Decision Table (39 Permutations)

| Situation | Outcome | Decided By |
|-----------|---------|------------|
| Exactly one CI matches (inclusion eligible) | **Update** attr-by-attr | Reconciliation rules |
| No match + DSR permits | **Insert** (reconciliation NOT consulted) | IRE + Data Source Rule |
| No match + DSR blocks | **Blocked** → partial (Enhanced) or fail (plain) | IRE Data Source Rule |
| Match excluded by inclusion rule | **Insert → potential duplicate** | Identification Inclusion Rule |
| Match, 2+ CIs, count < threshold, skip_duplicates=true | Update oldest; others `duplicate_of`; de-dup task | `skip_duplicates` [threshold=5] |
| Match, count ≥ threshold or skip_duplicates=false | **Match fails**, error; de-dup task | Threshold |
| Lookup-matched duplicates | Oldest referenced CI chosen; set prop to force tasks | `lookup_match.create_duplicate_task_ci.enabled` |
| Match, no reconciliation rule for source×attr | Attribute skipped silently | Static/Dynamic |
| Match, lower vs higher priority, non-stale | Lower rejected (first-writer/empty: override.null) | Priority + override.null |
| Match, field empty + lower-priority source | Filled (default override.null=true) | override.null |
| Match, class move beneficial + blocked | Reclassification task | Restriction rules / payload flags |
| Match + ACL/BR hides CI | **Insert → duplicate** | Platform (ACLs, query BRs, domain) |
| Scan type ≠ Configuration items | No CI at all | Schedule type |
| Active `duplicate_of` set / source=Duplicate | IRE refuses match → **Insert → duplicate** | KB0869861 |
| Concurrent discoveries same dependent CI | Duplicates | Schedule sequencing + platform |

---

### 6.2 Source-Native-Key Fast Path

```
Payload has source_name + source_native_key
         │
         ▼
┌─────────────────────────────────────┐
│ sys_object_source_info lookup       │
│ (exact match on source + native key)│
└─────────────────────────────────────┘
         │
    ┌────┴────┐
    │         │
  Found    Not Found
    │         │
    ▼         ▼
UPDATE CI  Identification
(skip       Rule Matching
 rules)
```

**Disable with:** `glide.identification_engine.skip_sys_object_source_matching=true`
→ Forces ALL payloads through identification rule matching (useful when native keys churn but attributes stable)

---

## 7. DUPLICATE PREVENTION PLAYBOOK

### 7.1 Root Causes (15 Confirmed)

| # | Cause | Evidence |
|---|-------|----------|
| 1 | Weak identifier entries (name-only) | v4-flash |
| 2 | Renamed adapters/hostnames → match breaks | A,B,C |
| 3 | Unstable serials / custom serial prefixes | A,B |
| 4 | Multiple sources w/o authority model | A,C |
| 5 | Lookup-table duplication pointing at different CIs | A,B |
| 6 | Over-broad schedules / overlapping behaviors | C |
| 7 | Multi-page payloads processed in parallel | openrouter-free + KB0869861 |
| 8 | Inclusion rule class-scoped on parent → children invisible | openrouter-free + KB0869861 |
| 9 | ACL/query BR hides existing CI from IRE | v4-flash + KB0869861 |
| 10 | `duplicate_of` set or `discovery_source=Duplicate` → IRE skips | KB0869861 |
| 11 | Manually created CIs w/ empty source — never reconciled | buffy+KB |
| 12 | Custom identifier Order collides with base rule | A,B,C |
| 13 | Reconciliation blocks update → human hand-creates "real" CI | buffy/v4-flash |
| 14 | High-priority source silent; attrs "frozen"; re-imports dup | buffy |
| 15 | Weak identification on child class while parent inherits | B |

---

### 7.2 Prevention Controls by Layer

#### Design-Time (CI Class Manager)
- One **independent** identifier per class (max 2 dependency levels)
- Strongest entry first; **1 entry ideal**
- `Enforce exact count match` for lookup entries
- **NEVER** define child-table identifier in parent rule AND child rule
- **NEVER** `sys_class_name` on independent rule
- Custom Order ≠ defaults (100/200)
- Enable `Enable Identifier Optional Condition` only after reviewing pre-configured entries

#### Runtime (Properties + IRE)
```properties
glide.identification_engine.skip_duplicates = true
glide.identification_engine.skip_duplicates.threshold = 5
glide.identification_engine.skip_sys_object_source_matching = true  # when source keys churn
glide.discovery.multi_page_serial_mode = true  # pattern-heavy estates
glide.discovery.enable_mac_address_verification = true  # DHCP fleets
glide.discovery.enforce_unique_ips = true  # ONLY as IP-invariant (not first resort)
```

#### Detection
- De-dup tasks (batch via dashboard)
- **Identification Simulation** before ANY rule change
- CMDB Health duplicate metric (narrow: only classes w/ ID rules + empty discovery_source OR active de-dup task)
- Discovery Status `Scan N of M` + Identification Logs (`glide.discovery.debug.ci_identification`)

#### Remediation
- Pick **main CI** explicitly
- Merge attributes/relationships/related items
- `duplicate_of` reference (no chains; main can't be a dup)
- Bulk: templates (NOT retroactive) + dashboard
- Single: Remediator wizard
- Roles: `itil` read, `itil_admin`/`cmdb_dedup_admin` write

---

## 8. DISCOVERY SOURCE A vs B DECISION MATRIX

> **Scenario:** You are Discovery Source A vs Discovery Source B under `cmdb_ci_computer` class.
> **Question:** Am I allowed to update? What rules control this?

### 8.1 Decision Flowchart

```mermaid
flowchart TD
    Start[Discovery Source A or B<br/>payload for cmdb_ci_computer] --> FastPath{Fast Path:<br/>source + native_key<br/>in sys_object_source_info?}
    
    FastPath -->|Yes & skip_sys_object_source_matching=false| UpdateA[UPDATE existing CI<br/>Reconciliation applies]
    FastPath -->|No OR skip=true| Identify[Identification Rule Matching<br/>Hardware Rule entries]
    
    Identify --> Match{Match Found?}
    
    Match -->|Yes| Inclusion{Inclusion Rule<br/>Active record condition<br/>allows this CI?}
    Match -->|No| DSRGate[IRE Data Source Rule<br/>for this Source + Class]
    
    Inclusion -->|Yes| Recon[Reconciliation Rules<br/>Static or Dynamic]
    Inclusion -->|No| InsertPath[INSERT NEW CI<br/>⚠️ Duplicate Risk]
    
    Recon --> ReconType{Reconciliation Type?}
    
    ReconType -->|Static| DataRefresh{Data Refresh Rule<br/>for this Source?}
    ReconType -->|Dynamic| DynamicWin[Dynamic Wins<br/>Value-based via CMDB 360]
    
    DataRefresh -->|No Rule| PriorityCheck{Priority Check:<br/>This Source vs Other}
    DataRefresh -->|Rule Exists| StaleCheck{Field Stale?<br/>(Effective Duration<br/>vs cmdb_datasource_last_update)}
    
    PriorityCheck -->|This Source Higher Priority| UpdateField[Update Field]
    PriorityCheck -->|This Source Lower Priority| EmptyCheck{Field Empty?}
    
    EmptyCheck -->|Yes & override.null=true| UpdateField
    EmptyCheck -->|No| RejectUpdate[Reject Update]
    
    StaleCheck -->|Not Stale| PriorityCheck
    StaleCheck -->|Stale & Lower-Priority<br/>Authorized by Recon| UpdateField
    StaleCheck -->|Stale but Not Authorized| RejectUpdate
    
    DSRGate --> DSRBlocked{Insert Not Allowed?}
    DSRBlocked -->|Yes| Partial[Partial Payload<br/>Stored for Merge]
    DSRBlocked -->|No| InsertCI[INSERT New CI]
    
    classDef update fill:#e3f2fd,stroke:#1565c0
    classDef insert fill:#fff3e0,stroke:#ef6c00
    classDef reject fill:#fce4ec,stroke:#c2185b
    classDef gate fill:#f3e5f5,stroke:#7b1fa2
    classDef decision fill:#e8f5e9,stroke:#2e7d32
    
    class UpdateA,UpdateField,DynamicWin update
    class InsertPath,InsertCI,Partial insert
    class RejectUpdate reject
    class DSRGate,Inclusion gate
    class Match,ReconType,DataRefresh,StaleCheck,PriorityCheck,EmptyCheck,DSRBlocked decision
```

---

### 8.2 Source A vs B — Configuration Matrix

| Configuration | Source A (Higher Priority) | Source B (Lower Priority) | Who Wins |
|---------------|---------------------------|--------------------------|----------|
| **No reconciliation rules** | Can insert & update all attrs | Can insert & update all attrs | **Last writer wins** (race) |
| **Static recon: A priority 10, B priority 20, all-attrs** | Authorized for all attrs | Authorized but lower priority | **A wins** on conflicts; B fills empty (override.null) |
| **Static recon: A priority 10 (name only), B priority 20 (all-attrs)** | Authorized for `name` | Authorized for all except `name` | **Specific beats all**: A wins `name`; B wins other attrs |
| **Static recon + Data Refresh: A 10, B 20, Effective Duration 90d** | Authorized | Authorized; stale check | **B updates stale fields** (after 90d) if authorized by its recon rule |
| **Dynamic IRE enabled** | Dynamic value-based | Dynamic value-based | **CMDB 360 decides** (largest/most-reported); Static rules ignored |
| **Dynamic IRE + cmdb_dynamic_ire_skip_class has cmdb_ci_computer** | Static rules apply | Static rules apply | **Static rules resume** |
| **IRE Data Source Rule: B blocked from insert** | Insert allowed | **Insert BLOCKED** | B can still UPDATE existing CIs |
| **Inclusion rule: only Operational CIs** | Updates Operational CIs | Updates Operational CIs | Retired CIs → new CI created (dup risk) |
| **ACL hides CI from Source B** | Can see & update | **Cannot see CI** → Inserts duplicate | **Fix ACL** or use DSR |
| **glide.discovery.enforce_unique_ips=true** | IP cleared from others | IP cleared from others | **DANGEROUS**: erases VIPs/NAT — not a dup control |
| **glide.discovery.enable_mac_address_verification=true** | MAC mismatch → stops | MAC mismatch → stops | Prevents DHCP dup; good for fleets |

---

### 8.3 Scenario Walkthroughs

#### Scenario 1: Source A = ServiceNow Discovery, Source B = SCCM

```
Configuration:
├─ IRE Data Source Rule: SCCM blocked from inserting cmdb_ci_computer
├─ Reconciliation: Discovery priority 10 (all-attrs), SCCM priority 20 (serial_number only)
└─ Data Refresh: Discovery Effective Duration = 90 days

Outcome:
├─ Discovery runs → inserts/updates computers (full authority)
├─ SCCM runs → CANNOT insert new computers (DSR blocks)
├─ SCCM CAN update serial_number on existing computers (recon authorizes)
├─ If Discovery hasn't refreshed in 90 days → SCCM can update other attrs (if recon allows)
└─ No duplicates from SCCM inserts
```

#### Scenario 2: Source A = Discovery, Source B = Monitoring Tool (no DSR)

```
Configuration:
├─ No IRE Data Source Rules
├─ No Reconciliation Rules
└─ No Data Refresh Rules

Outcome:
├─ Both can insert freely → DUPLICATES
├─ Both can update freely → last writer wins (race)
├─ skip_duplicates=true + threshold=5 may auto-merge small sets
├─ But: weak identifiers → more duplicates
└─ FIX: Add DSR for Monitoring (block insert), Recon for Discovery (priority 10 all-attrs)
```

#### Scenario 3: Dynamic IRE Enabled, cmdb_ci_computer NOT skipped

```
Configuration:
├─ glide.identification_engine.dynamic_ire.enabled = true
├─ cmdb_ci_computer NOT in cmdb_dynamic_ire_skip_class
├─ CMDB 360 licensed and populated

Outcome:
├─ Static Reconciliation Rules IGNORED
├─ Data Refresh Rules IGNORED
├─ IRE Data Source Rules IGNORED
├─ CMDB 360 value-based resolution wins (largest/most-reported)
├─ Source with most complete data wins per attribute
└─ To keep Static for computers: add cmdb_ci_computer to cmdb_dynamic_ire_skip_class
```

---

## 9. PROPERTIES REFERENCE (BRAZIL + AUSTRALIA DELTAS)

### 9.1 Identity / Hostname / Verification

| Property | Brazil Default | Australia Default (new customers) | Effect |
|----------|---------------|-----------------------------------|--------|
| `glide.discovery.use_cmdb_identifiers` | `true` | `true` | Routes through CMDB IRE |
| `glide.discovery.hostname.always_update` | `true` | `true` | Latest trusted value wins |
| `glide.discovery.hostname.case` | `Lower case` | `Lower case` | Normalization |
| `glide.discovery.hostname.include_domain` | `false` | `false` | FQDN in name |
| `glide.discovery.hostname.dns_nbt_trusted` | `true` | `true` | Trust DNS/NBT |
| `glide.discovery.hostname.snmp_trusted` | `false` | **`true`** | Trust SNMP name |
| `glide.discovery.hostname.ssh_trusted` | `false` | **`true`** | Trust SSH name |
| `glide.discovery.hostname.wmi_trusted` | `false` | **`true`** | Trust WMI name |
| `glide.discovery.source_name` | `ServiceNow` | `ServiceNow` | Written to discovery_source |
| `glide.discovery.debug.ci_identification` | `false` | `false` | CI Identification Log verbose |

### 9.2 IP / Network / Scanning

| Property | Default | Effect |
|----------|---------|--------|
| `glide.discovery.exclude_ip_sync_classes` | `cmdb_ci_lb` | LB IPs stay as-discovered |
| `glide.discovery.enforce_unique_ips` | `false` | Clears IP on other CIs — NOT a dup control |
| `glide.discovery.enable_mac_address_verification` | `false` | Stops processing on MAC mismatch (DHCP) |
| `glide.discovery.ip_service_affinity` | `false` → **new-customer `true`** | Remembers last good protocol/port per IP |
| `glide.discovery.shazzam_simplify_ranges` | `true` | Dedup overlapping ranges (single-behavior only) |
| `glide.discovery.max_concurrent_invocations_per_schedule` | `3` | Per-schedule concurrency cap |

### 9.3 Scheduling / Sensors / Throughput

| Property | Default | Effect |
|----------|---------|--------|
| `glide.discovery.schedule_ipv4_limit` | `65,536` | IPAM autogen cap |
| `glide.discovery.schedule_ipv6_limit` | `20,000` (≤5,000 ≤ZP3/YP9) | IPAM autogen cap |
| `glide.discovery.multi_page_serial_mode` | `false` | **`true` = serial pattern payloads (fixes dups)** |
| `glide.discovery.use_probe_results_cache` | `false` | Skip sensor if results unchanged |
| `discovery.use.event.processing` | `false` | Event Framework for sensors |
| `glide.discovery.sam_batch_update_size` | `100` | Batches cmdb_sam_sw_install updates |

### 9.4 Software Discovery / ADM

| Property | Default | Effect |
|----------|---------|--------|
| `glide.discovery.discover_software` | `true` | Software package discovery |
| `glide.discovery.software_sccm_managed` | `false` | True = Discovery won't write for SCCM-managed |
| `glide.discovery.enable.software_filter` | `true` | Filter list (Language Pack, Hotfix, etc.) |
| `glide.discovery.enable.software_simplify` | `true` | Name/version cleanup (disable → dup software rows) |
| `glide.discovery.enable_file_tracking` | `false` | Pattern file tracking |
| `glide.discovery.file_tracking.max_files_per_ci` | `50` | (NOT 4 — that's change_limit_count) |
| `glide.discovery.file_tracking.change_limit_count` | `4` | Change limit count |
| `glide.discovery.enable_adme` | `false` | Enhanced ADM probe |

### 9.5 IRE Engine Properties

| Property | Default | Effect |
|----------|---------|--------|
| `glide.identification_engine.skip_duplicates` | `true` | Auto-pick oldest duplicate < threshold |
| `glide.identification_engine.skip_duplicates.threshold` | `5` | Safety bound |
| `glide.identification_engine.enable_identifier_optional_condition` | `false` | Advanced conditions on regular entries |
| `glide.identification_engine.skip_sys_object_source_matching` | `false` | Prefer IRE matching over source_native_key |
| `glide.identification_engine.dynamic_ire_enabled` | `false` | Use Dynamic IRE (CMDB 360) |
| `glide.reconciliation.override.null` | `true` | Lower-priority may fill empty field |
| `glide.identification_engine.lookup_match.create_duplicate_task_ci.enabled` | `false` | Dedup tasks for lookup duplicates |
| `glide.identification_engine.granular_insert_locking` | `true` | Multiple granular vs single global lock |
| `glide.identification_engine.batch_update_last_discovered` | `true` | Batch update last_discovered |

---

## 10. VERIFICATION & OBSERVABILITY

| Signal | Where | What to Look For |
|--------|-------|------------------|
| Discovery Status | `Discovery > Discovery Status` (related list on schedule) | State flow, Completed vs Started, `Scan N of M`, cancel drops Ready jobs |
| Discovery Timeline | Show Discovery Timeline per device run | Queueing vs processing time + ECC records per step |
| ECC Queue | `Discovery > ECC Queue` | Raw payloads/XML in/out |
| Discovery Log | `Discovery > Logs` | Warnings/errors by probe/device; `log_message_length=200` truncates |
| Discovery Home | `Discovery > Home` | Tiles: Schedules / Discovered Devices / Cloud Resources / Errors |
| Discovery Admin Workspace | Errors + anomaly detection | ML-based anomaly detection (20% thresholds) |
| Identification Logs | `Configuration > Identification Logs` | IRE decisions per CI (cap 1000 via `glide.identification_logs.max_run_ids`) |
| Identification Simulation | `Configuration > Identification/Reconciliation` | Dry-run w/ zero CMDB commit; inspect execution log |
| CMDB Health | CMDB Workspace / Health dashboard | Completeness / Correctness / Compliance; dup metric narrowness |
| CMDB 360 | Multisource CMDB | Required for Dynamic IRE; compares source values |

**Debug-only properties (bounded windows, revert after):**
- `glide.discovery.debug.ci_identification`
- `glide.discovery.log_debug`
- `glide.discovery.log_debug_info`
- `glide.cmdb.logger.source.identification_engine=debug|debugVerbose`
- `mid.probe.collect_debug_info=true`

---

## 11. ANTI-PATTERNS (25 CONFIRMED)

| # | Anti-Pattern | Why It Hurts | Correct Move |
|---|--------------|--------------|--------------|
| 1 | Name-only identification rules | Renames/dup hostnames create new CIs | Add serial/UUID/MAC; strong independent key |
| 2 | More identifier entries "for safety" | Each adds matching cost; weak entries match wrong CI | One strong entry; extra only with evidence |
| 3 | Lookup identifier entries | Performance cost; dup lookup rows = ambiguous matches | Redesign to independent attrs; monitor if unavoidable |
| 4 | `enforce_unique_ips` as identification control | Erases VIPs/shared IPs; not a dup control | Use only as opt-in IP-invariant guard |
| 5 | `skip_duplicates=false` everywhere | Small duplicate sets fail identification | Keep `true` with deliberate threshold; investigate cause |
| 6 | Raising threshold without fixing rules | Masks duplicates instead of preventing | Fix rules, then re-tune threshold |
| 7 | One giant schedule for everything | Long runs, stacked invocations, hard to isolate | Split by network/domain/credential; use behaviors + chaining |
| 8 | Untrusted source allowed to insert | Low-quality CIs and duplicates | Add **IRE Data Source Rule** to block insert |
| 9 | No reconciliation owner | Sources overwrite each other | **Reconciliation Rules** + **Data Refresh Rules** |
| 10 | Deleting CIs to "clean up" | Breaks relationships/history; recreated next run | Use de-dup remediation + deletion strategies |
| 11 | Changing serial-number syntax | Breaks asset tracking and matching | Preserve raw serial numbers |
| 12 | Ignoring `max run time`/`max idle` | Stuck runs pile up | Set both; monitor status |
| 13 | Inclusion rule class-scoped on parent | Children invisible to IRE → new CI each run | Scope inclusion rules to specific class |
| 14 | Two ID strategies for one table | Class identifier + parent lookup = duplicates | One strategy per class |
| 15 | Custom identifier with default Order | Never runs (collides with base rule) | Use unique Order values |
| 16 | Renaming NIC labels/adapters | Breaks match on bonded hosts | Never rename NIC labels |
| 17 | Editing `duplicate_of` by hand | Breaks remediation chain | Use Remediator wizard |
| 18 | Overlapping schedules over same ranges | Duplicate discoveries | Use behaviors + range sets |
| 19 | Multi-page patterns + `multi_page_serial_mode=false` | Parallel payloads = duplicates | Set `true` for pattern-heavy estates |
| 20 | No reconciliation rule for authorized source | Write freeze or free-for-all | Define static/dynamic recon per source+attr |
| 21 | `Update with Null` on sensitive attrs | Lower-priority nulls populated fields | Only list attrs that SHOULD be nullable |
| 22 | Exclusion list >500k entries | Cancels runs | Prune exclusions |
| 23 | Windows account lacking local admin | Most WMI "couldn't classify" | Use proper credentials |
| 24 | Dynamic IRE on with no recon plan | DSRs/refresh silently dead | Use `cmdb_dynamic_ire_skip_class` deliberately |
| 25 | Assuming default rule beats attr-specific | Inverted — attr-specific ALWAYS wins | Specific-attribute > all-attributes (always) |

---

## 12. COVERAGE GAPS & UNEXPLORED SOURCES

### 12.1 Agent Coverage Summary

| Agent | Model | Status | Topics Covered | Topics Missing |
|-------|-------|--------|----------------|----------------|
| deepseek-v4.1-flash-fast (buffy) | DeepSeek V4.1 Flash Fast | ✅ PASS | All 8/8 + 4 IRE families | — |
| deepseek-v4-flash (hermes) | DeepSeek V4 Flash | ✅ PASS | All 8/8 | — |
| inkling-2-small | OpenRouter inkling-2-small | ✅ PASS | All 8/8 + 17 Australia sources | — |
| qwen3-30b-a3b | Ollama qwen3-30b-a3b | ⚠️ PASS* | 7/8 | mid_server |
| qwen2.5-7b | Ollama qwen2.5-7b | ⚠️ PASS* | 6/8 | reconciliation, mid_server |
| openrouter-free | OpenRouter free | ⚠️ PASS* | 7/8 | mid_server (partial) |
| llama3.1-8b | Ollama llama3.1-8b | ❌ PARTIAL | 0/8 | ALL — NO SOURCES REACHED |
| qwen2.5-coder-7b (alt) | Ollama qwen2.5-coder | Worker | Duplicate prevention only | — |
| particle-1 (alt) | particle-ai/particle-1 | Worker | CI Class Manager only | — |
| qwen3.5-4b (alt) | Ollama qwen3.5-4b | Worker | Config options + order only | — |
| kilo-ernie-5.5-flash (WT1-5) | Baidu ERNIE 5.5 Flash | ✅ Lead | All via 5 worktrees | — |
| deepseek-v4-pro (results) | Kilo deepseek-v4-pro | ✅ | IRE Matrix (39 perms) + Gap Analysis | — |

### 12.2 Known Gaps (from Coverage Gap Analysis)

| Gap | Details | Priority |
|-----|---------|----------|
| **CI Class Manager navigation** | Not in Discovery guide; only in CMDB guide | HIGH |
| **IRE Data Source Rules** | 0 hits in guides; only in Brazil docs | HIGH |
| **Data Refresh Rules** | 0 hits in guides; "staleness" only in KPI context | HIGH |
| **Insert-vs-update nuance** | `sys_updated_on` no-write, `install_status` not auto-reactivated | HIGH |
| **Pattern authoring** | Deliberately out of scope | MEDIUM |
| **Schedule auto-start/priority behavior** | Not fully documented | MEDIUM |
| **Australia vs Brazil property diff** | ~110 properties; only defaults flagged where docs contradict | MEDIUM |
| **Dynamic IRE production behavior** | All sources default `false`; untested | LOW |
| **Non-CMDB IRE procedures** | Not covered | LOW |

### 12.3 Unexplored / Unverified Sources

| Source Type | Examples | Status |
|-------------|----------|--------|
| **Now Support KBs (auth-gated)** | KB0869861, KB0755747, KB0750382/83/86, KB3104470 | Cited but not directly verified |
| **ServiceNow FluidTopics API** | khub search across Brazil/Australia maps | Used by deepseek-flash & inkling-2-small |
| **Community forums** | servicenow.com/community (ITOM, CMDB, Developer) | Corroboration only |
| **Instance UI paths** | Menu labels vary by release/patch | **UNVERIFIED** — flagged throughout |
| **Pattern debugger / horizontal patterns** | NDL operations, step parameters | Not explored |
| **CMDB 360 / Dynamic IRE** | Requires license; no test instance | **UNVERIFIED** |

### 12.4 Recommendations for Complete Coverage

1. **Add CI Class Manager + 4 IRE Families** to Discovery guide (or CMDB guide)
2. **Verify Australia property defaults** against live instance
3. **Test Dynamic IRE** with CMDB 360 in non-prod
4. **Validate Identification Simulation** workflows end-to-end
5. **Document pattern authoring** for horizontal patterns
6. **Map domain-separated rule behavior** in multi-domain instances

---

## 📌 APPENDIX: AGENT CONTRIBUTIONS LEDGER

| Agent | Key Contributions |
|-------|-------------------|
| `inkling-2-small__openrouter__kilo` | 17 Australia docs, property catalog §8, merge analysis, conflict validation |
| `deepseek-flash__openrouter__kilo-cli` | Brazil 68 topics, patterns/FBD/console/behaviors/timeline/deletion strategies |
| `deepseek-v4.1-flash-fast__freebuff__buffy` | Evidence digest 28 sources, Status states, Shazzam batch rules, three-stale-mechanisms table |
| `deepseek-v4-pro__deepseek__kilocode` | **IRE_RULE_APPLICABILITY_MATRIX.md (39 perms)**, KB-backed behavior, COVERAGE_GAP_ANALYSIS |
| `deepseek-v4-flash__deepseek__hermes` | 4-phase writeup, WMI KB, ire_err_exclusion_list, reconciliation ordering caveat |
| `kilo-ernie-5.5-flash__baidu__kilo` | WT1-5 synthesis, insertion-blocked downstream, property conflict resolution |
| `openrouter-free__openrouter__kilo` | KB0869861 checklist, retired-status BR, multi_page_serial_mode corroboration |
| `particle-1__openrouter__alt-swarm` | CI Class Manager role matrix, wizard order, field constraints, pre-flight checklist |
| `qwen2.5-coder-7b__ollama__alt-swarm` | Duplicate prevention checklist, skip thresholds table |
| `qwen3.5-4b__ollama__alt-swarm` | Config options inventory, canonical order of operations |
| `qwen3-30b-a3b__ollama__hermes`, `qwen2.5-7b__ollama__hermes`, `llama3.1-8b__ollama__hermes` | Corroboration of defaults; llama3.1-8b failed to reach sources |

---

*End of Consolidated Master Reference*