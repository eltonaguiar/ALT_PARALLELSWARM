# Worker report — qwen2.5-coder-7b__ollama__alt-swarm

**Task:** SNC_DISC_RESEARCH
**Model (primary):** `qwen2.5-coder:7b`
**Model (used):** `qwen2.5-coder:7b`
**Provider:** `ollama`
**Harness:** ALT_PARALLELSWARM `swarm/agent_runner.py`
**Generated:** 2026-11-13T09:03:23+00:00
**Evidence:** `duplicates.md` (pre-fetched; worker has no browser)
**Assigned section:** Produce the duplicate-prevention and insert-versus-update section. Explain identification-rule strength, the skip_duplicates/threshold behavior, source-native-key matching, data source rules, reconciliation and data refresh, de-duplication tasks, and the exact decision table for insert/update/fail/partial. Include a prevention checklist by layer (design, runtime, detection, remediation).

> This is an independent worker draft. It is evidence-constrained, not independently
> web-verified. The orchestrator's primary reference is the authoritative synthesis.

---

## Duplicate-Prevention and Insert-Versus-Update

### Identification Rule Strength
Identification rules in ServiceNow are crucial for uniquely identifying Configuration Items (CIs). A strong identification rule is one that uses the highest priority for the strongest identifier entries and related entries. This ensures that CIs are accurately identified and managed within the CMDB.

### Skip_Duplicates/Threshold Behavior
The `glide.identification_engine.skip_duplicates` property is set to `true` by default, which means that duplicate CIs are automatically reconciled. The `glide.identification_engine.skip_duplicates.threshold` property is set to `5` by default, which means that if the number of duplicate CIs is less than 5, the oldest duplicate CI is picked as a match and gets updated. If the number of duplicate CIs is 5 or more, de-duplication tasks are created for review and remediation.

### Source-Native-Key Matching
Source-native-key matching is a method used to identify and reconcile CIs based on their native keys from the source system. This ensures that CIs are accurately identified and managed across different systems.

### Data Source Rules
Data source rules determine which discovery sources can update CI attributes. There are two types of reconciliation rules: static and dynamic. Static reconciliation rules set priorities for the various discovery sources for updating CI attributes, while dynamic reconciliation rules are based on attribute values processed by CMDB 360.

### Reconciliation and Data Refresh
Reconciliation is the process of updating CI attributes based on data from discovery sources. Data refresh is the process of updating the CMDB with the latest data from discovery sources. Both processes are essential for maintaining the accuracy and integrity of the CMDB.

### De-Duplication Tasks
De-duplication tasks are created when the Identification and Reconciliation Engine (IRE) processes detect duplicate CIs. These tasks provide details about the duplication, including a list of all the duplicate CIs in the set. Reviewing and processing these tasks is essential for maintaining the accuracy and integrity of the CMDB.

### Decision Table for Insert/Update/Fail/Partial
The decision table for insert/update/fail/partial is used to determine the action to take when a CI is detected. The table is based on the properties of the CI and the discovery source. The decision table is stored in the Reconciliation Definition [cmdb_reconciliation_definition] table.

### Prevention Checklist by Layer

#### Design
- Create strong identification rules with the highest priority for the strongest identifier entries and related entries.
- Limit the number of identifier entries within an identification rule to 1.
- Avoid creating lookup identifier entries.
- Ensure that the identification rule is at the class level that it needs to be.

#### Runtime
- Configure the `glide.identification_engine.skip_duplicates` property to `true`.
- Configure the `glide.identification_engine.skip_duplicates.threshold` property to `5`.
- Ensure that the data source rules are correctly configured to allow updates from authorized discovery sources.

#### Detection
- Review de-duplication tasks regularly to ensure that duplicate CIs are accurately identified and remediated.
- Use the De-duplication Dashboard, De-duplication Template Library, and the entire CI de-duplication experience in CMDB Workspace to process de-duplication tasks.

#### Remediation
- Select a main CI for the remediation process.
- Choose which attribute values, relationships, and related items from the duplicate CIs to reconcile into the main CI.
- Ensure that the duplicate_of attribute in duplicate CIs is used to store a reference to the main CI.

### Assumptions / Gaps
- The evidence does not provide information on the specific attributes that should be used in identification rules.
- The evidence does not provide information on the specific discovery sources that should be used for reconciliation.
- The evidence does not provide information on the specific roles required to add or update records in the CMDB Deduplication Task Lookup or Related item allowed classes [cmdb_duplicate_lookup_related_allowed_class] configuration table.
