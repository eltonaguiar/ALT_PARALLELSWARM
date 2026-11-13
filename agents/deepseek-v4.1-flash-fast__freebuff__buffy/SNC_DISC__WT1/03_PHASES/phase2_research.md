# Phase 2 — research

2026-11-13

Capability gate: **PASS** (native `web_search` + `read_url`; no Playwright needed; docs pages
extract as full text).

Research passes, in this order:

1. **Discovery runtime + identifiers** → `docs …/discovery/c_DiscoveryIdentifiers`,
   `c_DiscoProcessFlows`, `r_DiscoveryStatusDevices`, KB0535236 / KB0535234.
2. **Schedule + setup order + IP ranges** → `discovery-schedule-form`, `t_ConfigureDiscovery`,
   `discovery-ip-address-configuration`, `exclude-ip-ranges`, KB0748222.
3. **IRE: identification vs reconciliation** → `c_IdentificationRules`,
   `t_CreateCIIdentificationRule`, `r_ReconciliationRulesPrinciples`, KB0756709, KB1064718,
   KB3037828 (rule-precedence surprise).
4. **Duplicate repair + health** → KB0869861, `de-duplication-tasks`, KB0726425, CMDB Health KPIs.
5. **CI Class Manager surface** → `t_ViewTableDefinitions`, `create-dependent-relationship`,
   `c_ServiceRulesMetadata`.
6. **Properties** → `r_DiscoveryProperties`, `r_AvailableSystemProperties`.

Evidence notes written to `research/EVIDENCE_DIGEST.md` (quoted lines + URLs) before synthesis,
so the reference is assembled from evidence rather than from memory.

Notable finding that reshaped section 13: **reconciliation rules never block an *insert*** — they
only gate *updates* [S9]. So "why did I get a duplicate?" and "why did my attribute not change?"
are different rule sets, and conflating them sends people to the wrong screen.
