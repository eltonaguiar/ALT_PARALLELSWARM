# ServiceNow Discovery Configuration Reference

## 1. Configuration Options & Properties

| Property | Purpose |
|---|---|
| `glide.discovery.multi_page_serial_mode` | When `true`, multipage payloads are processed in serial — prevents duplicate CIs from Discovery [KB0869861]. |
| Discovery Schedules | Control how often Discovery scans run; configure in `Service Administration > Discovery Schedules`. |
| Shazzam Probe List | Defines what probes run and in what order. Shazzam is the discovery framework. |
| Pattern Collection | Patterns define how CI attributes are discovered from actual infrastructure (Windows, Linux, Network). |
| Active Directory / LDAP configs | Lightweight directory protocol configurations for discovering directory objects. |
| MID Server | The proxy that runs discovery probes on the network; can be dedicated per Discovery schedule. |
| CMDB Identification Rules | Per-class identification criteria; set in `Configuration > CI Class Manager`. |

## 2. Order of Operations

Discovery runs in a sequential flow:

1. **Launch** — a Discovery schedule triggers the run.
2. **Network Discovery** — shazzam probe pings IP ranges, checks open ports, identifies active hosts.
3. **Pattern Matching** — for each discovered host, the appropriate pattern (Windows, Linux, etc.) determines what CI data to collect.
4. **CMDB Identification** — the IRE processes the CI payload and attempts to match it against existing CIs.
5. **Reconciliation** — if the CI is found, the IRE checks if the current discovery source is allowed to update the CI.
6. **Insert or Update** — if no match is found, a new CI is created. If a match is found and reconciliation permits, the CI is updated.

## 3. CI Class Manager Bread Crumbs

Access to per-class identification rules:

- **CI Class Manager**: `Configuration > CI Class Manager`
  - Shows each CI class (e.g. Windows Server, Linux Server, Database, Network Switch)
  - Displays the **Identification Rules** applied to that class
  - Shows whether a class **derives** its identifier from a parent class
  - Shows **Dependent Relationship Rules** (hosting rules) for dependent CIs

- **Identification Rules** define:
  - **Derived** — Inherited from a parent class (e.g. `cmdb_ci_hardware`)
  - **Independent** — Does not depend on relationships to other CIs (e.g. serial number only)
  - **Correlation ID** — First matching criteria — the same CI found via different identifiers

- **Inclusion Rules**: `Configuration > Identification/Reconciliation > Identification Inclusion Rules`
  - Filters which CIs are considered for identification
  - **Critical rule**: Do NOT use "Class" as a condition on a parent class table like `cmdb_ci_hardware` — this causes child classes to be treated as duplicates.

## 4. Duplicate CI Prevention

The IRE prevents duplicates using:

| Mechanism | What it does |
|---|---|
| Identification rules | Defines what makes a CI unique. If two servers have the same Correlation ID, they are duplicates (unless domain separation applies). |
| Inclusion rules | Restricts which CIs are considered. A CI not included in the rule is skipped — it can't be matched, so a new CI is created. |
| Reconciliation rules | Determine if a data source is allowed to update a CI. Without proper reconciliation, a source may be blocked from updating, causing duplicate creation. |
| Domain separation | Servers in different domains with the same Correlation ID are considered unique, not duplicates. |
| Query business rules | Custom query business rules on `cmdb_ci` tables can affect IRE queries — check and disable if causing duplicates. |
| ACLs | Access control lists on `cmdb_ci` tables can prevent IRE from finding existing CIs — check if IRE is querying as a restricted user. |
| `glide.discovery.multi_page_serial_mode` | Setting this to `true` prevents concurrent payload processing, eliminating race conditions that create duplicates from slow business rules. |

## 5. Insert vs Update Behavior

The IRE follows a precise decision tree:

```
Payload received
  → Validate payload CIs and relationships
    → If invalid: log errors and stop
    → If valid: continue
      → Loop through identification rules
        → Query CMDB
          → CI found?
            → Is CI active given inclusion rules for this class?
              → Yes: Do reconciliation rules allow this source to update?
                → Yes: Update CI fields
                → No: Do not update CI
              → No: Update CI fields
            → No: Are there more identification rules to attempt?
              → Yes: Continue to next rule
              → No: Create new CI
```

Key points:

- **CI not found** → New CI is created (INSERT).
- **CI found, active, reconciliation allows update** → CI fields are updated (UPDATE).
- **CI found, but not active (inclusion rules exclude it)** → CI is updated regardless of reconciliation rules.
- **CI found, but reconciliation disallows update** → CI is NOT updated; no duplicate is created (existing CI remains untouched).
- **Retired CI rediscovered** → Discovery does NOT un-retire the CI. The operational status remains Retired. A custom Business Rule on `cmdb_ci` with the condition "Most recent discovery changes" is needed to auto-update status.

## 6. Retired CI Status (KB0755747)

- Discovery does not include logic to override the Retired status and restore a CI to Operational when rediscovered.
- To auto-update retired CIs, create a Business Rule on `cmdb_ci`:
  - Table: `cmdb_ci`
  - When: `before`
  - Update: selected
  - Conditions: "Most recent discovery changes" AND "Operational Status is Retired"
  - Script: Update `operational_status` to the correct value (check via Show Choice List)
  - **Warning**: Updating Operational Status to Operational also sets Status/Hardware Status to Installed.

## 7. CMDB Identification and Reconciliation Engine (IRE)

The IRE is a centralized framework that:

- Receives CI payloads from Discovery, integrations, and external sources
- Identifies existing CIs by matching against identification rules
- Reconciles updates by checking if the current data source is authorized to update
- Creates new CIs when no match is found
- Prevents duplicates by properly matching against all applicable rules

### Dependent CIs

- Dependent CIs also use identification rules, but require at least one **hosting rule** to be satisfied.
- Example: A Kubernetes Pod is uniquely identified by its UID AND its "Contained by" relationship to a specific Kubernetes cluster.
- The same UID with different cluster containment = different CIs.

## 8. IRE Troubleshooting Checklist (from KB0869861)

1. **Check identification rules** in CI Class Manager — confirm the CI should be considered a duplicate.
2. **Check inclusion rules** — ensure the CI class is included and not excluded by a parent table condition.
3. **Debug business rules** — disable custom query business rules to see if they prevent CI matching.
4. **Debug ACLs** — ensure IRE is querying without restrictive access controls.
5. **Check domain separation** — if applicable, same Correlation ID in different domains = different CIs (by design).
6. **Check `duplicate_of` field** — IRE skips CIs where `duplicate_of` is populated.
7. **Check `discovery_source` field** — IRE skips CIs with `discovery_source = Duplicate`.
8. **Use IRE API** — test payloads via the `IdentificationEngineScriptableApi` in a background script.
9. **Run identification simulation** — use the built-in simulation tool to test matching without actually updating CMDB.

## Sources

- KB0869861: How to troubleshoot duplicate CMDB CI records (support.servicenow.com)
- KB0755747: Discovery does not update operational status of retired CIs when rediscovered (support.servicenow.com)
- KB1064718: CMDB Identification and Reconciliation Engine fundamentals (support.servicenow.com) [partial]
- developer.servicenow.com: Discovery configuration and CI Class Manager docs [assumed context]

---

**Document generated:** 2026-11-13T08:52Z
**Agent:** openrouter-free__openrouter__kilo
**Model:** openrouter.free / openrouter
**Worktree:** agents/openrouter-free__openrouter__kilo/SNC_DISC__WT5