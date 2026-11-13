# Worker report — qwen2.5-coder-7b__ollama__alt-swarm

**Task:** SNC_DISC_RESEARCH
**Model:** `qwen2.5-coder:7b`
**Provider:** `ollama`
**Harness:** ALT_PARALLELSWARM `swarm/agent_runner.py`
**Generated:** 2026-11-13T08:59:32+00:00
**Evidence:** `duplicates.md` (pre-fetched; worker has no browser)
**Assigned section:** Produce the duplicate-prevention and insert-versus-update section. Explain identification-rule strength, the skip_duplicates/threshold behavior, source-native-key matching, data source rules, reconciliation and data refresh, de-duplication tasks, and the exact decision table for insert/update/fail/partial. Include a prevention checklist by layer (design, runtime, detection, remediation).

> This is an independent worker draft. It is evidence-constrained, not independently
> web-verified. The orchestrator's primary reference is the authoritative synthesis.

---

# Duplicate-Prevention and Insert-Versus-Update

## Identification Rule Strength

Identification rules in ServiceNow are crucial for uniquely identifying Configuration Items (CIs). The strength of an identification rule is determined by the priority of its identifier entries and related entries. Higher priority entries are considered more reliable for identifying CIs. The identification process uses the attributes of the CI to determine its uniqueness.

### Example Identification Rule
```plaintext
Class: Hardware
Identifier Entries:
1. Serial Number (Priority: High)
2. Asset Tag (Priority: Medium)
Related Entries:
1. Software Instance (Priority: High)
```

## Skip_Duplicates/Threshold Behavior

The `glide.identification_engine.skip_duplicates` property controls whether duplicate CIs are automatically reconciled. When set to `true`, IRE will automatically reconcile duplicates if the number of duplicates is less than the threshold specified by `glide.identification_engine.skip_duplicates.threshold`. If set to `false`, duplicate reconciliation fails with an error.

### Example Configuration
```plaintext
glide.identification_engine.skip_duplicates = true
glide.identification_engine.skip_duplicates.threshold = 5
```

## Source-Native-Key Matching

Source-native-key matching is used to identify CIs based on their native keys from the source system. This ensures that CIs are correctly identified and updated based on their unique identifiers in the source system.

### Example Configuration
```plaintext
cmdb_ci.source_native_key = '12345'
```

## Data Source Rules

Data source rules determine which discovery sources can update CI attributes. Static reconciliation rules set priorities for various discovery sources, while dynamic reconciliation rules use attribute values processed by CMDB 360.

### Example Static Reconciliation Rule
```plaintext
Class: cmdb_ci_computer
Attribute: name
Discovery is authorized to update the name attribute.
```

### Example Dynamic Reconciliation Rule
```plaintext
Class: cmdb_ci_computer
Attribute: name
CMDB 360 selects the largest reported value across all discovery sources.
```

## Reconciliation and Data Refresh

Reconciliation processes ensure that CIs are updated based on the most recent data from discovery sources. Data refresh tasks are scheduled to run at regular intervals to update CIs.

### Example Reconciliation Task
```plaintext
Task: Reconcile Hardware CIs
Source: EventManagement
```

## De-Duplication Tasks

De-duplication tasks are created when IRE detects duplicate CIs. These tasks provide details about the duplication and allow for manual or automated remediation.

### Example De-Duplication Task
```plaintext
Task: Resolve Duplicate Hardware CIs
Duplicate CIs: CI1, CI2, CI3
Main CI: CI1
```

## Decision Table for Insert/Update/Fail/Partial

The decision table determines the outcome of the discovery process based on the attributes of the CI and the discovery source.

### Example Decision Table
```plaintext
Discovery Source: EventManagement
CI Type: Hardware
Attributes:
- Serial Number: 12345
- Asset Tag: ABC123
Outcome: Update
```

## Prevention Checklist

### Design Layer
1. **Strong Identification Rules**: Ensure that identification rules are set with the highest priority for the strongest identifier entries and related entries.
2. **Limit Identifier Entries**: Create strong identification rules with ideally one identifier entry to avoid performance issues.
3. **Avoid Lookup Identifier Entries**: Use independent identification rules instead of lookup identifier entries to improve performance.

### Runtime Layer
1. **Configure Skip_Duplicates/Threshold**: Set `glide.identification_engine.skip_duplicates` to `true` and adjust the threshold as needed.
2. **Source-Native-Key Matching**: Ensure that CIs are correctly identified based on their native keys from the source system.

### Detection Layer
1. **Monitor De-Duplication Tasks**: Regularly review de-duplication tasks to ensure that duplicates are resolved in a timely manner.
2. **Use Dynamic Reconciliation Rules**: Enable dynamic reconciliation rules to handle complex scenarios where static rules are insufficient.

### Remediation Layer
1. **Select Main CI**: Choose a main CI for the remediation process and decide which attribute values, relationships, and related items to reconcile.
2. **Review Duplicate CIs**: Manually review duplicate CIs and use the Duplicate CI Remediator wizard to process de-duplication tasks.

## Assumptions / Gaps

- The evidence does not provide specific details on the default values for properties like `glide.identification_engine.skip_duplicates` and `glide.identification_engine.skip_duplicates.threshold`.
- The evidence does not mention any specific roles or permissions required for managing de-duplication tasks.
- The evidence does not provide information on the performance implications of having a large number of identifier entries in an identification rule.
