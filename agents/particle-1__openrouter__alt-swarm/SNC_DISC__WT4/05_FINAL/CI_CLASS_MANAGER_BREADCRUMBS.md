# Worker report — particle-1__openrouter__alt-swarm

**Task:** SNC_DISC_RESEARCH
**Model (primary):** `particle-ai/particle-1:free`
**Model (used):** `particle-ai/particle-1:free`
**Provider:** `openrouter`
**Harness:** ALT_PARALLELSWARM `swarm/agent_runner.py`
**Generated:** 2026-11-13T09:03:27+00:00
**Evidence:** `classmanager.md` (pre-fetched; worker has no browser)
**Assigned section:** Produce the CI Class Manager breadcrumb and workflow section. Give the exact navigation path, role requirements, the class hierarchy navigation, every tab used for class definitions / identification / reconciliation / dependencies / health, the child-class wizard order, and the related screens outside the tool (identification simulation, IRE data source rule, properties). Add a short pre-flight checklist for configuring a new class.

> This is an independent worker draft. It is evidence-constrained, not independently
> web-verified. The orchestrator's primary reference is the authoritative synthesis.

---

## CI Class Manager breadcrumb and workflow

The CI Class Manager is the centralized UI for viewing, creating, and editing basic class definitions and class settings for IRE, CMDB Health, and some Service Mapping definitions. It does not support working with non-CMDB tables. [S1]

### Breadcrumb and entry point

The exact entry path is `All > Configuration > CI Class Manager`. For child-class creation, the working breadcrumb is `All > Configuration > CI Class Manager > Hierarchy > <selected parent class> > Add Child Class`; `Hierarchy` expands the CI Classes list, and `Add Child Class` is available only when the selected class is extendable. [S1][S2]

### Role requirements

| Task / area | Required role(s) and access | Source |
|---|---|---|
| General CI Class Manager access | `sn_cmdb_admin` has full access to all sections; `sn_cmdb_editor` has read access only. | [S1] |
| Create a CI class | `sn_cmdb_admin` or `Itil_admin`, and `personalize_dictionary` is required for editing the dictionary table; `sn_cmdb_admin` or `admin` provides full access. | [S2] |
| Create a dependent relationship rule | `sn_cmdb_editor` and `itil` have read access; `sn_cmdb_admin` and `itil_admin` have full access. | [S3] |
| Identification simulation | `sn_cmdb_admin` or `admin`. | [S4] |

### Class hierarchy navigation

In CI Class Manager, click `Hier
