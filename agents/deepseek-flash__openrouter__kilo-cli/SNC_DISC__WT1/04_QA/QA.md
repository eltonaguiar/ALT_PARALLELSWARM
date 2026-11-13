# QA — SNC_DISC_RESEARCH

**Agent:** `deepseek-flash__openrouter__kilo-cli`
**Model:** `deepseek/deepseek-flash` · **Provider:** OpenRouter (inferred) · **Harness:** Kilo CLI
**Checked:** 2026-11-13T09:10Z

## Success criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| SC1 | Coverage of Discovery options | **PASS** | 12 sections; 30+ named properties across identity/IP, network, scheduling, sensors, IRE, duplicates, deletion |
| SC2 | Correct order of operations | **PASS** | §2 has a 10-step ordered table with exit checks and a "design rules before broad schedules" rule |
| SC3 | CI Class Manager breadcrumbs | **PASS** | §8 gives `All > Configuration > CI Class Manager`, roles, Hierarchy, tab map, wizard order, related screens |
| SC4 | Duplicate prevention + insert/update control | **PASS** | §7 has a decision table, root causes, 4-layer controls, detection, remediation |
| SC5 | Traceability | **PASS** | Each section has canonical docs links; 68 topics indexed in `research/SOURCES.md` |
| SC6 | No fabricated property names/URLs | **PASS (spot-check)** | 20 property names/defaults checked against fetched text; see table below |
| SC7 | Honest limitations | **PASS** | `02_CLARIFICATIONS/CLARIFY.md`, `00_MODEL/MODEL_PROVIDER.md`, §11 |
| SC8 | Parallel orchestration demonstrated | **PASS** | 3 workers, 3 worktrees, 3 branches, all QA PASS; `swarm/ORCHESTRATION.md` |
| SC9 | Safe free-tier usage | **PASS** | Ledger enforces inflight/daily calls/daily tokens; cost recorded; free run cost `$0.00` |

## Property/default spot-check

| Property | Value in reference | Source file |
|---|---|---|
| `glide.discovery.use_cmdb_identifiers` | `true` | `discovery-properties` |
| `glide.discovery.enforce_unique_ips` | `false` | `discovery-properties` |
| `glide.discovery.exclude_ip_sync_classes` | `cmdb_ci_lb` | `discovery-properties` |
| `glide.discovery.ip_service_affinity` | `false`; new Brazil `true` | `discovery-properties` |
| `glide.discovery.hostname.always_update` | `true` | `discovery-properties` |
| `glide.discovery.hostname.dns_nbt_trusted` | `true` | `discovery-properties` |
| `glide.discovery.hostname.snmp_trusted` | `false`; new Brazil `true` | `discovery-properties` |
| `glide.discovery.hostname.ssh_trusted` | `false`; new Brazil `true` | `discovery-properties` |
| `glide.discovery.hostname.wmi_trusted` | `false`; new Brazil `true` | `discovery-properties` |
| `glide.discovery.max_concurrent_invocations_per_schedule` | `3` | `discovery-properties` |
| `glide.discovery.schedule_ipv4_limit` | `65,536` | `discovery-properties` |
| `glide.discovery.schedule_ipv6_limit` | `20,000` | `discovery-properties` |
| `glide.discovery.shazzam_simplify_ranges` | `true` | `discovery-properties` |
| `glide.discovery.shazzam_ranges_json` | `true` | `discovery-properties` |
| `discovery.use.event.processing` | `false` | `discovery-properties` |
| `glide.discovery.sensors.save_attachments` | `true` | `discovery-properties` |
| `glide.discovery.use_probe_results_cache` | `false` | `discovery-properties` |
| `glide.identification_engine.skip_duplicates` | `true` | `ire-properties` |
| `glide.identification_engine.skip_duplicates.threshold` | `5` | `ire-properties` |
| `glide.reconciliation.override.null` | `true` | `ire-properties` |
| `glide.identification_engine.dynamic_ire_enabled` | `false` | `ire-properties` |
| `glide.identification_engine.partial_payload_items_max_size` | `1000` | `ire-properties` |

## Worker QA

| Worker | Automated QA | Caveat |
|---|---|---|
| `qwen3.5-4b__ollama__alt-swarm` | PASS (1266 words) | Good option tables; its order-of-operations list is faithful to the digest |
| `qwen2.5-coder-7b__ollama__alt-swarm` | PASS (671 words) | **Known imprecision:** it says "data source rules determine which discovery sources can update CI attributes"; in the source, data-source rules govern **insert permission**, while reconciliation governs update authority. Do not rely on that draft without the primary reference. |
| `particle-1__openrouter__alt-swarm` | PASS (1328 words) | Strong on navigation and roles; correctly declares evidence gaps (e.g., Health tab label) |

The automated worker gate checks length, headings, citations, and structure — **not truth**.
All three worker drafts are marked as independent drafts in their own headers.

## Things a reviewer should still verify

1. UI labels in the target release (Brazil vs. the customer's version).
2. Whether the customer uses probe-based or pattern-based discovery; the reference
   explains both but a customer runbook must pick one.
3. The customer's actual authoritative-source priority before applying any
   reconciliation recommendation.
4. Free-tier caps in `swarm/registry.json` are operator guards, not vendor facts.

## Verdict

**PASS**, with the coder-draft caveat above. The primary reference is the artifact to
use; worker drafts are supporting evidence of the orchestration design.
