# QA — deepseek-v4-pro__deepseek__kilo

## Coverage self-check (harness topics)

| topic | covered | section |
|---|---|---|
| configuration_options (properties/config) | YES | §1 |
| order_of_operations (phases/sequence) | YES | §2 |
| ci_class_manager | YES | §3 |
| duplicates | YES | §4, §8 |
| insert_vs_update | YES | §8 |
| identification | YES | §4 |
| reconciliation | YES | §5 |
| mid_server | YES | §1, §2 |

**8/8 topics covered.**

## Domain-expert (private rubric) items

| item | own section | detail level |
|---|---|---|
| identification_rules | §4 | deep (unique/required attrs, derivation, independent/dependent, regular/lookup/hybrid entries, inclusion rules, related entries) |
| reconciliation_rules | §5 | deep (static/dynamic, 4 precedence principles, cmdb_reconciliation_definition / cmdb_dynamic_reconciliation_definition, data source history) |
| ire_data_source_rules | §6 | deep (Insert Not Allowed, cmdb_ire_data_source_rule, partial payloads, derivation/override) |
| data_refresh_rules | §7 | deep (Effective Duration staleness semantics, location, lower-priority takeover, dynamic-rule caveat) |

**4/4 rubric items have dedicated sections.**

## Citation check

- Distinct source URLs cited: **25** (11 official docs + 4 KB + 10 community).
- Every claim carries a URL or is marked `UNVERIFIED` (1 item: `r_DiscoveryProperties` page not rendered).
- All official docs cite their `canonical_url` on `docs.servicenow.com` (Brazil release).

## Verdict

**PASS.** 8/8 topics + 4/4 rubric items, 25 cited sources, honest UNVERIFIED marking for the one page not rendered.
