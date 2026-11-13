# Worker report — particle-1__openrouter__alt-swarm

**Task:** SNC_DISC_RESEARCH
**Model (primary):** `particle-ai/particle-1:free`
**Model (used):** `particle-ai/particle-1:free`
**Provider:** `openrouter`
**Harness:** ALT_PARALLELSWARM `swarm/agent_runner.py`
**Generated:** 2026-11-13T09:02:14+00:00
**Evidence:** `classmanager.md` (pre-fetched; worker has no browser)
**Assigned section:** Produce the CI Class Manager breadcrumb and workflow section. Give the exact navigation path, role requirements, the class hierarchy navigation, every tab used for class definitions / identification / reconciliation / dependencies / health, the child-class wizard order, and the related screens outside the tool (identification simulation, IRE data source rule, properties). Add a short pre-flight checklist for configuring a new class.

> This is an independent worker draft. It is evidence-constrained, not independently
> web-verified. The orchestrator's primary reference is the authoritative synthesis.

---

# CI Class Manager: Breadcrumb, Navigation, and Class Workflow

## Navigation and access

The CI Class Manager is the central location for viewing, creating, and editing basic class definitions, IRE class settings, CMDB Health settings, and some Service Mapping definitions. It does not support working with non-CMDB tables. The exact breadcrumb is **All > Configuration > CI Class Manager** [S1].

Role requirements differ by task and are stated inconsistently across the supplied sources, so they are reproduced verbatim below rather than reconciled.

| Task / scope | Role requirement (as stated) | Source |
|---|---|---|
| General access to CI Class Manager | `sn_cmdb_admin` has full access to all sections; `sn_cmdb_editor` has read access only | [S1] |
| Creating a CI class | `sn_cmdb_admin` or `Itil_admin`, and `personalize_dictionary` (required for editing the dictionary table); `sn_cmdb_admin` or `admin` for full access | [S2] |
| Dependent relationship rule (basic, in CI Class Manager) | `sn_cmdb_editor` and `itil` have read access; `sn_cmdb_admin` and `itil_admin` have full access | [S3] |
| Containment rules group | `sn_cmdb_admin` or `admin` | [S3] |
| Identification simulation | `sn_cmdb_admin` or `admin` | [S4] |

[S1][S2][S3][S4]

## Class hierarchy navigation

Click **Hierarchy** to expand the CI Classes list, then select the class you want to work with. For class creation, select the class the new class is extended from; the **Add Child Class** option appears only if the selected class is extendable. For dependent relationship rules, the same **Hierarchy** step is used to display the CI Classes list and select the target class [S2][S3].

## Tabs and views used for class definitions

The wizard tabs below appear in the order listed during child-class creation. The **Dependent Relationships** view is reached from the class navigation bar rather than the wizard.

| Tab / view | What it is used for | Source |
|---|---|---|
| **Provide Basic Info** | `Display name`, `Table name`, `Description`, `Icon`, `Extensible`, `Principal Class` | [S2] |
