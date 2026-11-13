# PLAN — inkling-2-small__openrouter__kilo / SNC_DISC__WT1

Agent: `inkling-2-small__openrouter__kilo` — model `openrouter/thinkingmachines/inkling-2-small:free`, provider **OpenRouter**, harness **Kilo**.
Date: 2026-11-13. Task: SNC_DISC_RESEARCH.

## Goal
As thorough a **configuration** reference as possible for ServiceNow Discovery limited to:
1. Discovery module configuration **options / properties** (system properties, tables).
2. **Order of operations** for setting Discovery up and for how discovery flows (scan → classify → identify → explore → update/insert CMDB).
3. Key breadcrumbs under **CI Class Manager** (All > Configuration > CI Class Manager) relevant to running Discovery and populating the CMDB.
4. Key configuration related to **avoiding duplicates** and **insert vs update** behaviour in the CMDB (IRE: identification rules, reconciliation rules, data source rules, skip_duplicates, reclassification flags).

## Output format
`05_FINAL/DISCOVERY_CONFIG_REFERENCE.md` — markdown, sections with source URLs inline (Australia bundle). Every non-obvious claim carries a `source:` line. A `research/raw/` corpus backs it. `research/EVIDENCE_DIGEST.md` lists all sources with retrieval date + byte size.

## Phases
| phase | marker | work |
|---|---|---|
| 1 | 03_PHASES/phase1_started.md | prereq + skeleton (done 08:52Z) |
| 2 | phase2_research_started.md / phase2_research_done.md | fetch + digest sources |
| 3 | phase3_synthesis.md | write DISCOVERY_CONFIG_REFERENCE.md |
| 4 | phase4_qa.md | self-check vs success criteria |
| 5 | phase5_final.md | final summary + filescope |

## Risks & mitigations
- **Assume-small context**: never hold >3 full pages in mind; strip HTML; write as I go. Mitigated by saving raw text to disk.
- **Internal/undocumented khub API**: may 404 later. Mitigated: digest keeps URLs + retrieval date; content saved in repo.
- **Release drift**: pages pinned to **Australia** (current bundle in search ordering). Where relevant, property names are release-stable since Geneva/Madrid. Noted inline.
- **Sibling agents in same repo**: never edit another agent's folder; unique agent_id folder; only my rows added to CONTRIBUTORS.md / agents.yaml.
- **Factual drift**: no claim without a fetched source. Anything recalled from prior knowledge is marked UNVERIFIED.

## Success criteria
- [ ] ≥15 distinct sources fetched and cited, all Australia bundle where applicable
- [ ] Property tables include: name, type/values, default, where to set (Configuration > ...)
- [ ] Order of operations diagram (text) for horizontal discovery + for a from-scratch Discovery setup (credentials → schedule → classify → identify → explore)
- [ ] CI Class Manager breadcrumb list with the exact navigation path
- [ ] Duplicate-avoidance config section: identification rules, reconciliation rules, data source rules, skip_duplicates(+threshold), reclassification flags, enforce_unique_ips, use_cmdb_identifiers
- [ ] Insert vs update semantics explained with actual property names + tables (cmdb_identifier, cmdb_identifier_entry, cmdb_reconciliation_definition, cmdb_ire_data_source_rule, cmdb_ire_partial_payloads)
- [ ] QA doc with pass/fail per criterion; FINAL_SUMMARY states blockers/clarifications honestly

## Scope exclusions
Cloud Discovery patterns, Service Mapping/ADM detail, ACC, OT Discovery, MID Server sizing — only where they intersect duplicates/insert-update. Not graded here, noted as UNVERIFIED/out-of-scope.
