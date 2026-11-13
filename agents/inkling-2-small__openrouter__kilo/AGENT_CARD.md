# Agent card — `inkling-2-small__openrouter__kilo`

**Model:** `inkling-2-small`
**Provider:** `openrouter`
**Endpoint:** `n/a`
**Role note:** external contributor folder (not in this roster)

## Where this work lives
| | |
|---|---|
| worktree | `/home/eaguiar2015/wt-inkling-2-small__openrouter__kilo` |
| branch | `agent/inkling-2-small__openrouter__kilo (merged)` |
| folder in repo | `agents/inkling-2-small__openrouter__kilo/SNC_DISC__WT1/` |

## Goal
Produce as thorough a technical reference as possible on ServiceNow **Discovery configuration**:
configuration options and properties, order of operations, key bread crumbs under **CI Class Manager**,
and the configuration that prevents **duplicate CIs** and governs **insert vs update** of CMDB records.

## Output format
`05_FINAL/DISCOVERY_CONFIG_REFERENCE.md` — markdown, headed sections, every claim carrying a source URL
or explicitly marked UNVERIFIED; plus `04_QA/QA.md` and `05_FINAL/FINAL_SUMMARY.md`.

## Self-reported status
- capability gate: **NO BROWSING**
- internal topic check: **?/?**
- private rubric (external): **?/4 mentioned, ?/4 quality**
- sources cited: **?**

## Files modified (98)
```
.gitignore
SNC_DISC__WT1/00_PREREQ/PREREQ.md
SNC_DISC__WT1/01_PLAN/PLAN.md
SNC_DISC__WT1/02_CLARIFICATIONS/CLARIFY.md
SNC_DISC__WT1/03_PHASES/phase1_started.md
SNC_DISC__WT1/03_PHASES/phase2_research_done.md
SNC_DISC__WT1/03_PHASES/phase3_synthesis.md
SNC_DISC__WT1/03_PHASES/phase4_qa.md
SNC_DISC__WT1/03_PHASES/phase5_final.md
SNC_DISC__WT1/04_QA/QA.md
SNC_DISC__WT1/05_FINAL/DISCOVERY_CONFIG_REFERENCE.md
SNC_DISC__WT1/05_FINAL/FINAL_SUMMARY.md
SNC_DISC__WT1/06_FILESCOPE/FILESCOPE.md
SNC_DISC__WT1/research/EVIDENCE_DIGEST.md
SNC_DISC__WT1/research/raw/ci_class_manager.html
SNC_DISC__WT1/research/raw/ci_class_manager.txt
SNC_DISC__WT1/research/raw/configuring_discovery.html
SNC_DISC__WT1/research/raw/configuring_discovery.txt
SNC_DISC__WT1/research/raw/create_ci_class.html
SNC_DISC__WT1/research/raw/create_ci_class.txt
SNC_DISC__WT1/research/raw/create_ire_data_source_rule.html
SNC_DISC__WT1/research/raw/create_ire_data_source_rule.txt
SNC_DISC__WT1/research/raw/create_reconciliation_rule.html
SNC_DISC__WT1/research/raw/create_reconciliation_rule.txt
SNC_DISC__WT1/research/raw/credential_affinity.html
SNC_DISC__WT1/research/raw/credential_affinity.txt
SNC_DISC__WT1/research/raw/discovery_classifiers.html
SNC_DISC__WT1/research/raw/discovery_classifiers.txt
SNC_DISC__WT1/research/raw/discovery_home_page.html
SNC_DISC__WT1/research/raw/discovery_home_page.txt
SNC_DISC__WT1/research/raw/discovery_identifiers.html
SNC_DISC__WT1/research/raw/discovery_identifiers.txt
SNC_DISC__WT1/research/raw/discovery_properties.html
SNC_DISC__WT1/research/raw/discovery_properties.txt
SNC_DISC__WT1/research/raw/discovery_schedule_form.html
SNC_DISC__WT1/research/raw/discovery_schedule_form.txt
SNC_DISC__WT1/research/raw/duplicate_ci_remediation.html
SNC_DISC__WT1/research/raw/duplicate_ci_remediation.txt
SNC_DISC__WT1/research/raw/horizontal_process_flow.html
SNC_DISC__WT1/research/raw/horizontal_process_flow.txt
SNC_DISC__WT1/research/raw/how_identifiers_work.html
SNC_DISC__WT1/research/raw/how_identifiers_work.txt
SNC_DISC__WT1/research/raw/ire_components.html
SNC_DISC__WT1/research/raw/ire_components.txt
SNC_DISC__WT1/research/raw/ire_landing.html
SNC_DISC__WT1/research/raw/ire_landing.txt
SNC_DISC__WT1/research/raw/ire_overview.html
SNC_DISC__WT1/research/raw/ire_overview.txt
SNC_DISC__WT1/research/raw/ire_properties.html
SNC_DISC__WT1/research/raw/ire_properties.txt
SNC_DISC__WT1/research/raw/itom_config_console.html
SNC_DISC__WT1/research/raw/itom_config_console.txt
SNC_DISC__WT1/research/raw/mid_server_exploring.html
SNC_DISC__WT1/research/raw/mid_server_exploring.txt
SNC_DISC__WT1/research/raw/mid_server_landing.html
SNC_DISC__WT1/research/raw/mid_server_landing.txt
SNC_DISC__WT1/research/raw/mid_server_properties.html
SNC_DISC__WT1/research/raw/mid_server_properties.txt
SNC_DISC__WT1/research/raw/properties_duplicate_ci.html
SNC_DISC__WT1/research/raw/properties_duplicate_ci.txt
SNC_DISC__WT1/research/raw/reconciliation_rules_principles.html
SNC_DISC__WT1/research/raw/reconciliation_rules_principles.txt
SNC_DISC__WT1/research/raw/search_ci_class_manager.json
SNC_DISC__WT1/research/raw/search_cmdb_data_source_precedence.json
SNC_DISC__WT1/research/raw/search_configuring_discovery.json
SNC_DISC__WT1/research/raw/search_create_a_discovery_schedule.json
SNC_DISC__WT1/research/raw/search_discovery_credentials.json
SNC_DISC__WT1/research/raw/search_discovery_home_page_discovery_status.json
SNC_DISC__WT1/research/raw/search_discovery_identifiers.json
SNC_DISC__WT1/research/raw/search_discovery_order_of_operations.json
SNC_DISC__WT1/research/raw/search_discovery_properties.json
SNC_DISC__WT1/research/raw/search_duplicate_configuration_items.json
SNC_DISC__WT1/research/raw/search_horizontal_discovery_process.json
SNC_DISC__WT1/research/raw/search_how_discovery_works_process_phases.json
SNC_DISC__WT1/research/raw/search_identification_and_reconciliation_engine.json
SNC_DISC__WT1/research/raw/search_insert_or_update_ci.json
SNC_DISC__WT1/research/raw/search_ire_reconciliation_rules.json
SNC_DISC__WT1/research/raw/search_itom_configuration_console_discovery.json
SNC_DISC__WT1/research/raw/search_mid_server_overview.json
SNC_DISC__WT1/research/raw/search_mid_server_properties.json
SNC_DISC__WT1/research/raw/search_properties_for_identification_and_reconciliation.json
drops/2026-11-13_0852_openrouter_inkling-2-small/README.md
drops/2026-11-13_0852_openrouter_inkling-2-small/SESSION_NOTES.md
drops/2026-11-13_0852_openrouter_inkling-2-small/SWARM_REPORT.md
swarm/README.md
swarm/free_keys.py
swarm/results/cerebras.json
swarm/results/gemini.json
swarm/results/groq.json
swarm/results/mistral.json
swarm/results/ollama.json
swarm/results/openrouter.json
swarm/results/subq_free.json
swarm/results/subq_paid.json
swarm/results/swarm_run.json
swarm/run_swarm.py
swarm/state/swarm_ledger.json
swarm/subq_snap.py
```
