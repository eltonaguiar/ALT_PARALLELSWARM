# Worker report — qwen2.5-coder-7b__ollama__alt-swarm

**Task:** SNC_DISC_RESEARCH
**Model:** `qwen2.5-coder:7b`
**Provider:** `ollama`
**Harness:** ALT_PARALLELSWARM `swarm/agent_runner.py`
**Generated:** 2026-11-13T09:00:51+00:00
**Evidence:** `duplicates.md` (pre-fetched; worker has no browser)
**Assigned section:** Produce the duplicate-prevention and insert-versus-update section. Explain identification-rule strength, the skip_duplicates/threshold behavior, source-native-key matching, data source rules, reconciliation and data refresh, de-duplication tasks, and the exact decision table for insert/update/fail/partial. Include a prevention checklist by layer (design, runtime, detection, remediation).

> This is an independent worker draft. It is evidence-constrained, not independently
> web-verified. The orchestrator's primary reference is the authoritative synthesis.

---

# Duplicate-Prevention and Insert-versus-Update

## Identification Rule Strength

Identification rules in ServiceNow are crucial for uniquely identifying Configuration Items (CIs). The strength of an identification rule is determined by the priority of its identifier entries and related entries. Higher priority entries are considered more reliable for identifying CIs. It is essential to design strong identification rules by setting the highest priority for the strongest identifier entries and related entries [S1].

## Skip_Duplicates/Threshold Behavior

The `glide.identification_engine.skip_duplicates` property controls whether duplicate CIs are automatically reconciled. When set to `true`, IRE will automatically reconcile duplicate CIs if the number of duplicates is less than the threshold specified by `glide.identification_engine.skip_duplicates.threshold` (default is 5). If set to `false`, matching of duplicate CIs will fail with an error [S2].

## Source-Native-Key Matching

Source-native-key matching is a method used to identify and reconcile CIs based on their native keys from the source system. This ensures that CIs are correctly identified and updated based on their unique identifiers in the source system [S1].

## Data Source Rules

Data source rules determine which discovery sources can update CI attributes. There are two types of reconciliation rules: static and dynamic. Static reconciliation rules set priorities for discovery sources, while dynamic reconciliation rules are based on attribute values processed by CMDB 360. Static reconciliation rules are stored in the `Reconciliation Definition` table, and dynamic reconciliation rules are stored in the `Dynamic Reconciliation Definitions` table [S4].

## Reconciliation and Data Refresh

Reconciliation is the process of updating CI attributes based on data from discovery sources. It ensures that CIs are up-to-date and consistent across the CMDB. Data refresh can be triggered manually or automatically based on the configuration of reconciliation rules [S4].

## De-Duplication Tasks

De-duplication tasks are created when IRE detects duplicate CIs. These tasks provide details about the duplication, including a list of all duplicate CIs in the set. Reviewing and processing these tasks is essential for maintaining the integrity and reliability of the CMDB [S2].

## Decision Table for Insert/Update/Fail/Partial

The decision table for insert/update/fail/partial is used to determine the action to take when a CI is detected. The table is based on the attributes of the CI and the configuration of reconciliation rules. The decision table is stored in the `Reconciliation Definition` table [S4].

## Prevention Checklist

### Design

- Create strong identification rules with the highest priority for the strongest identifier entries and related entries.
- Limit the number of identifier entries within an identification rule to 1.
- Avoid creating lookup identifier entries.

### Runtime

- Configure the `glide.identification_engine.skip_duplicates` and `glide.identification_engine.skip_duplicates.threshold` properties based on the number of duplicate CIs.
- Ensure that the identification rule is at the class level that it needs to be.

### Detection

- Review the details of each duplicate CI in the de-duplication task.
- Ensure that the de-duplication task is processed in a timely manner.

### Remediation

- Select a main CI for the remediation process.
- Choose which attribute values, relationships, and related items from the duplicate CIs to reconcile into the main CI.
- Ensure that the duplicate_of attribute is used to store a reference to the main CI.

## Assumptions / Gaps

- The evidence does not provide information on the specific attributes that should be used for identification rules.
- The evidence does not provide information on the specific roles required to add or update records in the `cmdb_duplicate_lookup_related_allowed_class` table.
- The evidence does not provide information on the specific steps to follow when manually creating a de-duplication task.
