# Worker report — qwen2.5-coder-7b__ollama__alt-swarm

**Task:** SNC_DISC_RESEARCH
**Model (primary):** `qwen2.5-coder:7b`
**Model (used):** `qwen2.5-coder:7b`
**Provider:** `ollama`
**Harness:** ALT_PARALLELSWARM `swarm/agent_runner.py`
**Generated:** 2026-11-13T09:04:47+00:00
**Evidence:** `duplicates.md` (pre-fetched; worker has no browser)
**Assigned section:** Produce the duplicate-prevention and insert-versus-update section. Explain identification-rule strength, the skip_duplicates/threshold behavior, source-native-key matching, data source rules, reconciliation and data refresh, de-duplication tasks, and the exact decision table for insert/update/fail/partial. Include a prevention checklist by layer (design, runtime, detection, remediation).

> This is an independent worker draft. It is evidence-constrained, not independently
> web-verified. The orchestrator's primary reference is the authoritative synthesis.

---

## Duplicate-Prevention and Insert-Versus-Update

### Identification Rule Strength

Identification rules in ServiceNow are crucial for uniquely identifying Configuration Items (CIs). The strength of an identification rule is determined by the priority of its identifier entries and related entries. Higher priority entries are considered more reliable for identifying CIs. It is essential to design strong identification rules by setting the highest priority for the strongest identifier entries and related entries [S1].

### Skip_Duplicates/Threshold Behavior

The `glide.identification_engine.skip_duplicates` property controls whether duplicate CIs are automatically reconciled. When set to `true`, IRE will automatically reconcile duplicate CIs if the number of duplicates is less than the threshold specified by `glide.identification_engine.skip_duplicates.threshold` (default is 5). If set to `false`, matching of duplicate CIs will fail with an error [S2].

### Source-Native-Key Matching

Source-native-key matching is a method used to identify and reconcile CIs based on their native keys from the source system. This ensures that CIs are correctly identified and updated based on their unique keys from the source [S1].

### Data Source Rules

Data source rules determine which discovery sources can update CI attributes. There are two types of reconciliation rules: static and dynamic. Static reconciliation rules set priorities for discovery sources, while dynamic reconciliation rules are based on attribute values processed by CMDB 360. Static reconciliation rules are stored in the `Reconciliation Definition` [cmdb_reconciliation_definition] table, and dynamic rules are stored in the `Dynamic Reconciliation Definitions` [cmdb_dynamic_reconciliation_definition] table [S4].

### Reconciliation and Data Refresh

Reconciliation is the process of updating CI attributes based on data from discovery sources. When a discovery source updates a CI, the reconciliation rules determine which source's data should be used. Data refresh involves updating the CMDB with the latest data from discovery sources. This ensures that the CMDB remains up-to-date and accurate [S4].

### De-Duplication Tasks

De-duplication tasks are created when IRE detects duplicate CIs. These tasks provide details about the duplication, including a list of all duplicate CIs. Reviewing and processing these tasks is essential for maintaining the integrity and reliability of the CMDB [S2].

### Decision Table for Insert/Update/Fail/Partial

The decision table for insert/update/fail/partial is used to determine the action to take when IRE detects duplicate CIs. The table is based on the number of duplicates and the value of the `glide.identification_engine.skip_duplicates` property. The table is as follows:

| glide.identification_engine.skip_duplicates | Number of Duplicates | Action |
|--------------------------------------------|------------------------|--------|
| true                                       | < threshold            | Update the oldest duplicate CI and tag others as duplicates. |
| true                                       | >= threshold           | Create a de-duplication task. |
| false                                      | Any number             | Fail the matching process. |

### Prevention Checklist

#### Design

- **Strong Identification Rules**: Create strong identification rules with the highest priority for the strongest identifier entries and related entries.
- **Limit Identifier Entries**: Limit the number of identifier entries within an identification rule to 1.
- **Avoid Lookup Identifier Entries**: Avoid using lookup identifier entries as they can reduce performance.

#### Runtime

- **Configure Skip_Duplicates/Threshold**: Configure the `glide.identification_engine.skip_duplicates` and `glide.identification_engine.skip_duplicates.threshold` properties based on the organization's requirements.
- **Enable Dynamic Reconciliation Rules**: Enable dynamic reconciliation rules if needed to handle complex scenarios.

#### Detection

- **Review De-Duplication Tasks**: Regularly review and process de-duplication tasks to ensure the integrity and reliability of the CMDB.
- **Monitor Duplicate CIs**: Monitor for duplicate CIs and take appropriate action based on the decision table.

#### Remediation

- **Select Main CI**: Select a main CI for the remediation process and choose which attribute values, relationships, and related items to reconcile into the main CI.
- **Process De-Duplication Tasks**: Process de-duplication tasks in bulk using de-duplication templates or manually using the Duplicate CI Remediator wizard.

### Assumptions / Gaps

- The evidence does not provide specific details on the impact of different attribute values on the decision table for insert/update/fail/partial.
- The evidence does not provide specific details on the role requirements for managing the CMDB Deduplication Task Lookup or Related item allowed classes [cmdb_duplicate_lookup_related_allowed_class].
- The evidence does not provide specific details on the performance implications of using lookup identifier entries in identification rules.
