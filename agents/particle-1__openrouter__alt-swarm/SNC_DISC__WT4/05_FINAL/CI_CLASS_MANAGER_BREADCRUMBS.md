# Worker report — particle-1__openrouter__alt-swarm

**Task:** SNC_DISC_RESEARCH
**Model (primary):** `particle-ai/particle-1:free`
**Model (used):** `particle-ai/particle-1:free`
**Provider:** `openrouter`
**Harness:** ALT_PARALLELSWARM `swarm/agent_runner.py`
**Generated:** 2026-11-13T09:04:57+00:00
**Evidence:** `classmanager.md` (pre-fetched; worker has no browser)
**Assigned section:** Produce the CI Class Manager breadcrumb and workflow section. Give the exact navigation path, role requirements, the class hierarchy navigation, every tab used for class definitions / identification / reconciliation / dependencies / health, the child-class wizard order, and the related screens outside the tool (identification simulation, IRE data source rule, properties). Add a short pre-flight checklist for configuring a new class.

> This is an independent worker draft. It is evidence-constrained, not independently
> web-verified. The orchestrator's primary reference is the authoritative synthesis.

---

## CI Class Manager: Breadcrumb and Workflow

### Navigation and roles

The CI Class Manager is reached from the application breadcrumb `All > Configuration > CI Class Manager`. The same path is given for creating a class, for creating dependent relationship rules, and for the tool generally, so a single breadcrumb serves all class-definition work described in the evidence [S1][S2][S3].

The tool is described as a centralized location for viewing, creating, and editing basic class definitions and class settings for the Identification and Reconciliation Engine (IRE), CMDB Health, and some Service Mapping definitions. It does not support working with non-CMDB tables [S1].

Role requirements are stated per task rather than as one consolidated matrix. The table reproduces each statement exactly as written in the evidence.

| Task / scope | Role requirement | Source |
|---|---|---|
| General access to CI Class Manager | `sn_cmdb_admin` has full access to all sections; `sn_cmdb_editor` has read access only | [S1] |
| Creating a CI class | `sn_cmdb_admin` or `Itil_admin`, and `personalize_dictionary` (required for editing the dictionary table) | [S2] |
| Creating a CI class (full access) | `sn_cmdb_admin` or `admin` | [S2] |
| Dependent relationship rules (read) | `sn_cmdb_editor` and `itil` | [S3] |
| Dependent relationship rules (full) | `sn_cmdb_admin` and `itil_admin` | [S3] |
| Containment rule groups | `sn_cmdb_admin` or `admin` | [S3] |
| Identification simulation | `sn_cmdb_admin` or `admin` | [S4] |

The evidence does not reconcile these per-task statements into a single role model; treat each row as scoped to the task named in that row [S1][S2][S3][S4].

### Class hierarchy navigation

Click `Hierarchy` to expand the CI Classes list, then select the class from which the new class is extended. The `Add Child Class` option appears only if the selected class is extendable [S2]. The precondition is that the class being extended has its `Is_Extendable` field checked, indicating the class is extendable [S2].

For dependent relationship rules the entry point differs slightly: click `Hierarchy` to display the CI Classes list, select the class, and then, in the class navigation bar, click `Dependent Relationships` [S3]. The class for which a dependent relationship rule is created must have a dependent identification rule [S3].

### Tabs used for class definitions, identification, reconciliation, dependencies, and health

| Tab | Purpose | Notes from evidence |
|---|---|---|
| `Provide Basic Info` | First wizard step; captures label, table name, description, icon, extensibility, Principal Class | Fields: `Display name`, `Table name`, `Description`, `Icon`, `Extensible`, `Principal Class` [S2] |
| `Add Attributes` | Adds new class columns | Click the `+` sign per column; double-click the attribute's `Identification Rule` column and set it to `true` to designate a CI identifier [S2] |
| `Set Identification Rule` | Reviews the `Derived identification rule` and its `Identifier Entries` | `Replace` substitutes a new identification rule and new identifier entries specific to the new class [S2] |
| `Dependencies` | Adds dependent rules via `Add dependency` | Appears only if there are dependent identification rules for the selected class [S2] |
| `Add Reconciliation Rules` | Click `Add` to create `Reconciliation Rules` and `Data Refresh` rules | [S2] |
| `Add Suggested Relationships` | Reviews the diagram of derived suggested relationships; filter by inbound, outbound, or specific relationship types | `New` opens the `Add Suggested Relationship` dialog; select a `Relationship` and a `Target Class`, then `Save` [S2] |
| `Dependent Relationships` | Class navigation bar tab for hosting and containment rules | `Add dependency` opens the `Add Dependent Relationship Rule` dialog with `Rule Type`, `This Class`, `Relationship`, `Target Class`; `Save` commits [S3] |

CMDB Health settings are managed in the CI Class Manager, and the evidence enumerates the capabilities available there: create a compliance audit, create a certification template, create a CMDB Health orphan rule, create a CMDB Health staleness rule, set a CI field to be recommended, set a CI attribute to be mandatory, and create a health inclusion rule. The evidence does not state the tab label under which these appear [S1].

### Child-class wizard order

The wizard steps appear in the following order in the evidence [S2]:

1. `Provide Basic Info` — fill out the information, then click `Next`.
2. `Add Attributes` — click the `+` sign and enter details for each new class column, then click `Next`.
3. `Set Identification Rule` — examine the `Derived identification rule` and its `Identifier Entries`; optionally click `Replace`.
4. `Dependencies` — click `Add dependency` to add dependent rules (conditional tab).
5. `Add Reconciliation Rules` — click `Add` to create reconciliation and data refresh rules.
6. `Add Suggested Relationships` — review the derived relationship diagram and add relationships as needed.

The evidence presents these as sequential steps but does not state whether any step can be skipped or revisited [S2].

Basic info field constraints are as follows [S2]:

| Field | Constraint |
|---|---|
| `Display name` | Unique label; appears on list and form views; updating it also updates the label record in the language file for the current language; maximum 80 characters |
| `Table name` | Auto-populated from the table label with the prefix string `u_cmdb_ci`; prefix not modifiable; remainder editable; lowercase alphanumeric ASCII characters and underscores (`_`) only; maximum 80 characters |
| `Description` | Explanation of the use purpose of the class |
| `Icon` | Icon associated with the class |
| `Extensible` | Whether this class can be extended |
| `Principal Class` | Whether the class is included in the Principal Class filter; if included, CIs from this class appear in CI list views when the filter is applied |

### Related screens outside the tool

**Identification simulation.** Navigate to `All > Configuration > Identification/Reconciliation` and click `Identification Simulation`. In the `Start with CI Class` box click `Start`. On the `Payload Information` form, select the data source in the `Data source` field — for the ServiceNow Discovery data source, select `ServiceNow` — then select the `Class` in the payload, choose CI identifier attributes and values in `Criterion Attributes`, and specify update values in `Additional Attributes`. For dependent CIs associated with dependent identification rules, complete the `Criterion Attributes` and `Additional Attributes` sections in all container-level sections that display. Click `Generate Script`, then `Run Simulation`; `Copy Script` copies the JSON. Simulation does not commit any updates to the CMDB, and final execution uses the `createOrUpdateCI()` API [S4].

**IRE data source rules.** Reconciliation relies on reconciliation rules and IRE data source rules, and is required only for update operations — when identification matches an incoming CI to an existing CI. When IRE inserts a new CI, reconciliation is not applied [S5].

**Properties.** The evidence supplied does not describe any system properties screen or property names related to CI Class Manager; this is not stated in the supplied evidence [S1][S2][S3][S4][S5].

### Pre-flight checklist for configuring a new class

| # | Check | Evidence |
|---|---|---|
| 1 | Confirm the parent class has `Is_Extendable` checked | [S2] |
| 2 | Confirm the operator holds `sn_cmdb_admin` or `Itil_admin`, plus `personalize_dictionary` if the dictionary table will be edited | [S2] |
| 3 | Agree the `Display name` (≤80 characters) and the `Table name` remainder after the fixed `u_cmdb_ci` prefix | [S2] |
| 4 | Decide `Principal Class` inclusion, since it controls appearance in CI list views under the filter | [S2] |
| 5 | Prepare attributes and mark identifier attributes via the `Identification Rule` column | [S2] |
| 6 | Decide whether to keep the derived identification rule or `Replace` it | [S2] |
| 7 | Confirm a dependent identification rule exists if dependent relationships are required | [S3] |
| 8 | Prepare reconciliation rules and data refresh rules | [S2] |
| 9 | Prepare suggested relationships (relationship type and target class) | [S2] |
| 10 | Plan an identification simulation run before committing payloads | [S4] |

### Assumptions / gaps

- Role requirements are recorded per task in the evidence and are not consolidated into a single authoritative matrix; the table above preserves each statement without harmonizing them [S1][S2][S3][S4].
- The tab label for CMDB Health settings is not stated in the supplied evidence, although the capabilities available under CMDB Health are enumerated [S1].
- No system properties, property names, or defaults for CI Class Manager are present in the supplied evidence [S1][S2][S3][S4][S5].
- Whether wizard steps are mandatory, skippable, or revisitable is not stated [S2].
- Service Mapping entry point types and CI types for Service Mapping and Discovery are listed as in-scope for the tool, but no procedure or screen detail is supplied [S1].
- The evidence notes that CI Class Manager does not support non-CMDB tables and that identification simulation can process but not generate payloads containing non-CMDB tables [S1][S4].
