# Worker report — particle-1__openrouter__alt-swarm

**Task:** SNC_DISC_RESEARCH
**Model (primary):** `particle-ai/particle-1:free`
**Model (used):** `particle-ai/particle-1:free`
**Provider:** `openrouter`
**Harness:** ALT_PARALLELSWARM `swarm/agent_runner.py`
**Generated:** 2026-11-13T09:02:42+00:00
**Evidence:** `classmanager.md` (pre-fetched; worker has no browser)
**Assigned section:** Produce the CI Class Manager breadcrumb and workflow section. Give the exact navigation path, role requirements, the class hierarchy navigation, every tab used for class definitions / identification / reconciliation / dependencies / health, the child-class wizard order, and the related screens outside the tool (identification simulation, IRE data source rule, properties). Add a short pre-flight checklist for configuring a new class.

> This is an independent worker draft. It is evidence-constrained, not independently
> web-verified. The orchestrator's primary reference is the authoritative synthesis.

---

# CI Class Manager: Breadcrumb and Workflow

## Navigation and role requirements

The CI Class Manager is reached from the application breadcrumb `All > Configuration > CI Class Manager` [S1][S2][S3]. It is the centralized location for viewing, creating, and editing basic class definitions and class settings for the Identification and Reconciliation Engine (IRE), CMDB Health, and some Service Mapping definitions [S1]. It does not support working with non-CMDB tables [S1].

| Role | Granted access | Source |
|---|---|---|
| `sn_cmdb_admin` | Full access to all sections of the CI Class Manager; full access for class creation; full access for dependent relationship rules; required (or `admin`) for identification simulation | [S1][S2][S3][S4] |
| `sn_cmdb_editor` | Read access only to CI Class Manager sections; read access (with `itil`) for dependent relationship rules | [S1][S3] |
| `Itil_admin` | Listed alongside `sn_cmdb_admin` as a required role for class creation, with `personalize_dictionary` required for editing the dictionary table | [S2] |
| `admin` | Full access for class creation; required (or `sn_cmdb_admin`) for identification simulation | [S2][S4] |

The evidence states the class-creation role requirement as "`sn_cmdb_admin` or `Itil_admin`, and `personalize_dictionary`: Required for editing the dictionary table" and separately "`sn_cmdb_admin` or `admin`: Full access" [S2]. It does not state which of these applies to which wizard step [S2].

## Class hierarchy navigation

Within the CI Class Manager, click `Hierarchy` to expand the CI Classes list, then select the class from which the new class is extended [S2]. The `Add Child Class` option appears only if the selected class is extendable [S2]. Before you begin, the class being extended must have its `Is_Extendable` field checked, indicating that the class is extendable [S2]. For dependent relationship rules, the same `Hierarchy` navigation is used to display the CI Classes list and select the target class [S3].

## Tab inventory

The tabs below are the ones the evidence names for class definitions, identification, reconciliation, dependencies, and health.

| Tab / view | Where it appears | Purpose | Source |
|---|---|---|---|
| `Provide Basic Info` | Add Child Class wizard | Capture label, table name, description, icon, extensibility, Principal Class | [S2] |
| `Add Attributes` | Add Child Class wizard | Add new class columns via the `+` sign; set an attribute as a CI identifier by double-clicking its `Identification Rule` column and setting it to `true` | [S2] |
| `Set Identification Rule` | Add Child Class wizard | Examine the `Derived identification rule` and its `Identifier Entries`; `Replace` swaps in a new rule and identifier entries specific to the new class | [S2] |
| `Dependencies` | Add Child Class wizard | `Add dependency` to add dependent rules; the tab appears only if there are dependent identification rules for the selected class | [S2] |
| `Add Reconciliation Rules` | Add Child Class wizard | `Add` to create Reconciliation Rules and Data Refresh Rules | [S2] |
| `Add Suggested Relationships` | Add Child Class wizard | Review the derived suggested-relationship diagram; filter inbound, outbound, or specific relationship types; `New` opens the Add Suggested Relationship dialog | [S2] |
| `Dependent Relationships` | Class navigation bar (after creation) | `Add dependency` to create hosting or containment rules | [S3] |

The wizard tab is named `Dependencies` [S2], while the post-creation class navigation bar view is named `Dependent Relationships` [S3]; the evidence does not state whether these are the same screen.

For CMDB Health, the evidence lists the capabilities available from the CI Class Manager — create a compliance audit, create a certification template, create a CMDB Health orphan rule, create a CMDB Health staleness rule, set a CI field to be recommended, set a CI attribute to be mandatory, and create a health inclusion rule — but does not name the individual tabs that host them [S1].

## Child-class wizard order

The wizard proceeds in this fixed order [S2]:

1. `Provide Basic Info` — fill out the information, then click `Next` [S2].
2. `Add Attributes` — click the `+` sign, enter details for each new class column, then click `Next` [S2].
3. `Set Identification Rule` — examine the derived rule and identifier entries, optionally `Replace` [S2].
4. `Dependencies` — click `Add dependency` to add dependent rules [S2].
5. `Add Reconciliation Rules` — click `Add` to create reconciliation and data refresh rules [S2].
6. `Add Suggested Relationships` — review the diagram and optionally add relationships [S2].

`Provide Basic Info` fields are inventoried below [S2].

| Field | Behavior |
|---|---|
| `Display name` | Unique label shown on list and form views; maximum 80 characters |
| `Table name` | Auto-populated from the table label and the prefix string `u_cmdb_ci`; prefix is not modifiable; lowercase alphanumeric ASCII and underscores only; maximum 80 characters |
| `Description` | Explanation of the class's use purpose |
| `Icon` | Icon associated with the class |
| `Extensible` | Whether this class can be extended |
| `Principal Class` | Whether the class is included in the Principal Class filter |

## Related screens outside the tool

**Identification simulation.** Navigate to `All > Configuration > Identification/Reconciliation` and click `Identification Simulation` [S4]. Role required is `sn_cmdb_admin` or `admin` [S4]. In the `Start with CI Class` box click `Start`, then on the `Payload Information` form select the data source in the `Data source` field — for the ServiceNow Discovery data source, select `ServiceNow` — select the `Class`, fill `Criterion Attributes` and `Additional Attributes`, complete all `Container` level sections for dependent CIs, and click `Generate Script` [S4]. Then click `Run Simulation`; simulation does not commit any updates to the CMDB [S4]. Final execution uses the `createOrUpdateCI()` API [S4].

**IRE data source rules.** IRE data source rules are named as a component of reconciliation, alongside identification rules, reconciliation rules, de-duplication tasks, and reclassification tasks [S5]. Reconciliation is required only for update operations, when identification matches an incoming CI to an existing CI; when IRE inserts a new CI, reconciliation is not applied [S5]. The navigation path to the IRE data source rule screen is not stated in the supplied evidence.

**Properties.** No properties screen, property name, or default value is stated in the supplied evidence.

## Pre-flight checklist for configuring a new class

| # | Check | Source |
|---|---|---|
| 1 | Confirm the parent class has `Is_Extendable` checked | [S2] |
| 2 | Confirm you hold `sn_cmdb_admin` or `Itil_admin` plus `personalize_dictionary` if editing the dictionary table | [S2] |
| 3 | Confirm the target is a CMDB table, not a non-CMDB table | [S1] |
| 4 | Prepare `Display name` (≤80 chars) and `Table name` (≤80 chars, lowercase/underscore, `u_cmdb_ci` prefix) | [S2] |
| 5 | Decide whether the class belongs in the Principal Class filter | [S2] |
| 6 | Decide which attributes are CI identifiers (`Identification Rule` = `true`) | [S2] |
| 7 | Decide whether to keep the derived identification rule or `Replace` it | [S2] |
| 8 | Confirm a dependent identification rule exists before adding dependent relationships | [S2][S3] |
| 9 | Plan reconciliation and data refresh rules | [S2] |
| 10 | Validate the result in identification simulation before executing via `createOrUpdateCI()` | [S4] |

## Assumptions / gaps

- The exact tab labels for CMDB Health inside the CI Class Manager are not stated in the supplied evidence; only the list of health tasks is provided [S1].
- The navigation path to the IRE data source rule screen is not stated in the supplied evidence [S5].
- No properties screen, property name, or default value appears in the supplied evidence.
- Whether the wizard's `Dependencies` tab and the class navigation bar's `Dependent Relationships` view are the same screen is not stated [S2][S3].
- The evidence does not state which class-creation role applies to which wizard step [S2].
- The Metadata Editor is described as synchronized with the CI Class Manager for dependent rules, but its navigation path is not stated [S3].
