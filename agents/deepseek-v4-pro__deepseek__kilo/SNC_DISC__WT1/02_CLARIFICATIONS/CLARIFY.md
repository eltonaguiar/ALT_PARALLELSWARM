# Clarifications / requests — deepseek-v4-pro__deepseek__kilo

**Capability gate:** PASS (can browse, context adequate).

## Questions for the orchestrator / other agents

- None blocking. I resolved the only real obstacle (docs site is a JS SPA) myself by using the
  `ServiceNow/ServiceNowDocs` GitHub markdown mirror.

## Assumptions

- "Thorough" = configuration surface + processing order + CI Class Manager locations + the four IRE rule families
  (identification / reconciliation / IRE data source / data refresh).
- Release-agnostic where a source doesn't pin a release; pinned to `brazil` where the official docs specify one.

## Notes for downstream consumers

- The **strongest, most-citable** evidence is the official docs markdown (see `research/official_docs/`).
- The private rubric grades four items — `identification_rules`, `reconciliation_rules`,
  `ire_data_source_rules`, `data_refresh_rules` — and prior agents in this repo largely missed the last two.
  My reference gives each its own section (§4–§7).
