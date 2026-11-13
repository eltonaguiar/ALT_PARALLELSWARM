# ServiceNow Discovery — Configuration Reference (Australia)

Agent: `inkling-2-small__openrouter__kilo` · Model `openrouter/thinkingmachines/inkling-2-small:free` · Provider **OpenRouter** · Harness **Kilo**
Release pin: **Australia** ("Release version: Australia", docs updated 2026-03-12). Property names are stable back to Geneva/Madrid where noted.
All sources retrieved 2026-11-13 via the servicenow.com docs khub API — see `research/EVIDENCE_DIGEST.md` (sources [1]–[17]). This document is the synthesis; §11 lists what is UNVERIFIED.

---

## 1. Order of operations — standing Discovery up from zero

The Configuring Discovery page [3] and the horizontal process flow [2] give the real order. Discovery does **not** need every procedure done; defaults are sane for most discoveries, and the ITOM Configuration Console is the fast path. The dependency order is:

1. **MID Server** up + validated + attached (out of scope here; required before anything returns data).
2. **Credentials** (WMI/SSH/SNMP/SNMPv3/HTTP) for the ranges you will scan. HTTP classification is *lowest* priority — used only when Shazzam sees 80/443 open and WMI/SSH/SNMP fail [4].
3. **MID↔ECC queue** — schedules place Shazzam/port probes in the ECC queue; MID polls it [2].
4. **Discovery schedule** — IP ranges (or Quick Discovery / Discover now) + which credentials. Schedule properties constrain width: `glide.discovery.schedule_ipv4_limit`, `glide.discovery.schedule_ipv6_limit`, `glide.discovery.max_concurrent_invocations_per_schedule` [1].
5. **Scan (Shazzam + port probes)** → open-port fingerprint → *machine type guess* [2].
6. **Classify** — exactly one classification probe per device; result sets CI class [2][4].
7. **Identify** — identifier rules / pattern identifier operations decide **match → update existing CI** vs **no match → create CI** [2][5][6]. This is where duplicates are prevented.
8. **Explore** — exploration probes/patterns from the classifier's Triggers Probes related list; sensors update the CMDB [2].
9. **CMDB write** via IRE — identification → reconciliation → commit. Insert ≠ update paths (see §6) [7][8][10].
10. **Verify** — Discovery Home, ECC queue, Identification Logs (`Configuration > Identification Logs`, `glide.identification_logs.max_run_ids`) [10].

Runtime flow (one IP, probes path): Shazzam → port probes → port-probe record → classification probe → classifier (criteria: parameter/operator/value, case-sensitive for process classifiers) → identification trigger probe → identifier rules → exploration probes → sensors → CMDB [2][4].

Patterns path: no identity probe; the **Horizontal Pattern probe** runs pattern operations which call identifier rules for both identify and explore [2][6].

## 2. Discovery configuration options / properties (the ones that change CMDB outcomes)

Set via `sys_properties.list` (table System Properties [sys_properties]) or the linked CMDB Properties modules. All from [1] unless noted.

### 2.1 IP / network
| property | default | effect |
|---|---|---|
| `glide.discovery.exclude_ip_sync_classes` | `cmdb_ci_lb` | classes whose IP is not substituted from scan data (uses mgmt IP as returned) |
| `glide.discovery.enforce_unique_ips` | `false` | when true, clears `ip_address` on every other CI sharing an IP after each valid discovery — strong duplicate guard; side effect: shared/NAT addresses get cleared |
| `glide.discovery.discoverable.network.max.netmask.bits` | (default exists) | caps discovery to regular netmasks |
| `glide.discovery.shazzam_simplify_ranges` / `glide.discovery.shazzam_ranges_json` | — | simplify large IP range handling |
| `glide.discovery.discover_software` | — | software instance population |
| `glide.discovery.enable_mac_address_verification` | — | MAC/IP cross-check; helps identification hygiene |
| `glide.discovery.allow_loopback_adapters` | — | include loopbacks as NICs (usually leave false) |
| `glide.discovery.virtual_interface_types` / `physical_interface_types` / `switch_interface_types` | — | interface typing used by net discovery |
| `glide.discovery.bgp_router_disable` | `true` | skip BGP exploration (large tables); set false only for small-network BGP edge |
| `glide.discovery.schedule_monitoring.stale_check_seconds` / `.dry_run` / `.schedule_types_to_monitor` | — | discovery run monitoring |
| `glide.discovery.schedule.autogenerate.group` / `.debug` | — | schedule auto-generation |
| `glide.discovery.max_concurrent_invocations_per_schedule` | — | per-schedule concurrency |
| `glide.discovery.retire_stale_accounts` | — | stale account retirement |
| `glide.discovery.mark_esx_servers_as_absent` | — | absent marking for ESX |

### 2.2 HTTP classification fallback (Madrid+)
HTTP classification activates only if Shazzam sees 80/443 open and higher-priority WMI/SSH/SNMP probes fail. Property hook: `glide.discovery.debug.network_discovery` (logs) [1][4].

### 2.3 Identification-relevant Discovery properties
| property | default | effect |
|---|---|---|
| `glide.discovery.use_cmdb_identifiers` | (present on Geneva+ instances) | switch to CMDB Identification & Reconciliation identifiers; required post-Geneva upgrades; **always on when Service Mapping is active** regardless of value [5] |
| `glide.discovery.hostname.always_update` | — | force hostname update even if identical (watch for churn) |
| `glide.discovery.hostname.case` | — | case handling for name matching |
| `glide.discovery.hostname.include_domain` | — | include domain in name comparison |
| `glide.discovery.hostname.{wmi,ssh,snmp,dns_nbt}_trusted` | — | which protocol wins for hostname |
| `glide.discovery.fqdn.regex` | — | FQDN validation |
| `glide.discovery.network_owner_method` | — | how network ownership resolves |
| `glide.discovery.debug.ci_identification` | — | verbose identification logs |
| `glide.discovery.use_probe_results_cache` | — | cache probe results |
| `glide.discovery.application_mapping` / `glide.discovery.enable_adme` / `glide.discovery.adme.*` | — | application mapping to dependency map (ADME) |
| `glide.discovery.enable_file_tracking` / `glide.discovery.file_tracking.max_files_per_ci` / `.max_file_size` / `.change_limit_count` / `.change_limit_days` | — | file-based discovery limits |
| `glide.discovery.certs.*` | — | cert inventory & renewal task creation |
| `glide.discovery.software_sccm_managed`, `glide.discovery.enable.software_filter`, `glide.discovery.software_filter_keys`, `glide.discovery.enable.software_simplify[_sccm]` | — | SCCM/software simplification |

## 3. IRE properties that govern duplicates and update behaviour [10]

Set at **Configuration > CMDB Properties > Identification/Reconciliation Properties** (or sys_properties for the rest). Role: `sn_cmdb_admin` or `admin`.

| property | default | duplicate/insert-update effect |
|---|---|---|
| `glide.identification_engine.skip_duplicates` | **true** | If duplicates < threshold: oldest CI is picked as match target **and becomes main CI**; other duplicates get `duplicate_of` → main CI. If false: matching fails and error is logged |
| `glide.identification_engine.skip_duplicates.threshold` | **5** | Above this, identification treats duplicates as if skip_duplicates=false |
| `glide.class.upgrade.enabled` / `glide.class.downgrade.enabled` / `glide.class.switch.enabled` | **true** | Allow IRE reclassification (up/down/switch) during identification |
| `glide.identification_engine.update_without_upgrade_enabled` / `.update_without_downgrade_enabled` / `.update_without_switch_enabled` | **false** | When true: process the CI update but **skip the reclassification** for that direction. Precedence over `glide.class.*.enabled` |
| `glide.identification_engine.reclassification_restriction_rules_enabled` | **true** | Apply active reclassification restriction rules |
| `glide.reconciliation.override.null` | **true** | Lower-priority source may update an empty field |
| `glide.required.attribute.enabled` | **true** | Required attributes may not be null during I&R |
| `glide.identification_engine.skip_sys_object_source_matching` | **false** | false (default) prefers `sys_object_source` native-key match over identification rules — **faster unique path**; true forces IRE identification rules even when source keys exist. Set true when source attributes churn but native keys are stable → avoids dupes from unstable identifiers |
| `glide.identification_engine.skip_updating_source_last_discovered_if_older` | **true** | Stale source payloads don't roll back `last_discovered`/`discovery_source` |
| `glide.identification_engine.skip_updating_last_scan_if_older` / `.ire_message_listener_skip_*` | **true / false** | Same for Source table `last_scan` |
| `glide.identification_engine.partial_payload_items_max_size` | **1000** | Cap items per partial payload; splits beyond this |
| `glide.identification_engine.partial_items_process_limit` / `.partial_items_process_absolute_limit` | **2000 / 5000** | Partial payload fetch limits per IRE call |
| `glide.identification_engine.granular_insert_locking` | **true** | multiple granular insert locks vs one global lock (set false on lock contention) |
| `glide.identification_engine.batch_update_last_discovered` / `.batch_update_last_discovered.use_execute_lazy` | **true / true** | batch last_discovered updates; set both false for immediate consistency / deletion-race workarounds |
| `glide.cache.size.service_cache` | **20 MB** | identification engine relation cache |
| `glide.identification_engine.*_local_cache_count` | **15000 / 10000 / 100000** | related / dependent / independent item caches; 0 disables |
| `glide.identification_engine.enable_identifier_optional_condition` | **false** | enables Optional condition advanced filter on regular identifier entries (applies pre-configured conditions) |
| `glide.identification_engine.enable_reconciliation_filter_before_update` | **false** | apply reconciliation filter conditions before (not after) value change |
| `glide.identification_engine.dynamic_ire.enabled` / `.dynamic_ire.auto_compare` | **false / true** | Dynamic IRE switch + comparison mode |
| `glide.identification_engine.non_dependency_relation.duplicate_detection` | **false** | detect duplicate non-dependent relations in payload |
| `glide.identification_engine.lookup_match.create_duplicate_task_ci.enabled` | **false** | create de-dup tasks for duplicate lookup-table related items |
| `glide.cmdb.logger.source.identification_engine` | — | `info|warn|error|debug|debugVerbose` — heavy; scope narrowly |
| `glide.identification_logs.max_run_ids` | **1000** | max log runs in `Configuration > Identification Logs` |

## 4. CI Class Manager — key breadcrumbs

Navigation: **All > Configuration > CI Class Manager** [16][17]. Organized tabs:

| area | breadcrumb / contents | why it matters |
|---|---|---|
| **Class basics** | Hierarchy → select class → Add Child Class; per class: display name, table name (`u_cmdb_ci_*`), **Extensible** flag, Principal Class flag, icon | new class names must extend an existing extendable class; only extended classes get derived identifier rules [17] |
| **Identification (IRE)** | Class → IRE → **Identification: CI identification rules**, Identification inclusion rules | per-class identifier rules you will tune to kill duplicates; double-click attribute → set Identification Rule = true on class columns tab [17] |
| **Reconciliation (IRE)** | Class → IRE → **Reconciliation: CI reconciliation rules**, **Data refresh rules** | who may write what attribute; data refresh rules mark CI stale for a source so lower-priority sources can update |
| **Dependencies** | Class → IRE → **Dependent relationship rules (hosting and containment)** | dependent CIs (e.g. Tomcat on Windows Server) are identified *in the context of their host* — required for dependent-class unique ID |
| **CMDB Health** | Class → CMDB Health → staleness rules, orphan rule, compliance audit, certification template, Health inclusion rules, mandatory/recommended attributes | CMDB quality; recommended/mandatory fields surface bad Discovery data |
| **Service Mapping** | Entry point types, CI types | pattern triggers for application CIs |
| **Class columns** | Class → Columns | set identifier attributes here; per-column Identification Rule flag [17] |
| **Suggested relationships / list with CIs / dependency map icons / delete CIs / Principal Class filter** | Class → misc tabs | suggested relationships refresh Query Builder; Delete CIs from here |

Create-class flow (what the identification engine will actually use afterwards) [17]:
Hierarchy → pick parent (must be Extensible) → Add Child Class → Provide Basic Info (label ≤80 chars, table `u_cmdb_ci_<name>`, lowercase/underscore, Extensible, Principal Class) → Add Attributes (per column; double-click Identification Rule column to true for identifiers) → **Set Identification Rule** (review Derived identification rule + entries; optionally Replace with a new rule) → Dependencies (add dependent rules if the class has them) → **Add Reconciliation Rules** (create Reconciliation + **Data Refresh Rules** — if skipped, no source is authorized to update the class and weak identification sneaks dupes in silently) → Suggested Relationships → Done.

## 5. Avoiding duplicates — the configuration that actually works

Duplicate prevention is layered; every layer matters:

**A. Identification rules (match phase).** `Identifier [cmdb_identifier]` + `Identifier Entry [cmdb_identifier_entry]`. Defaults shipped: Hardware [cmdb_ci_hardware] → serial_number(+type), name, ip_address, mac_address — plus Serial Number, Network Adapter, ESX, Storage Server, WBEM rules, with *Search on* tables `cmdb_serial_number` and `cmdb_ci_network_adapter` [5].
- Create per-class rules (e.g. cmdb_ci_linux_server) instead of overloading Hardware for NIC-bonded nets; include `name` there [5].
- Entries marked **Optional condition** narrow candidate sets (requires `glide.identification_engine.enable_identifier_optional_condition=true`; review pre-configured entries first) [10].
- **Evaluation order**: rules and entries parse low→high Order. Custom rules must use different Order values; disable rules with Active=false rather than delete [5].
- **Contain CIs**: avoid name-based rules where names get renamed — renamed adapter → unresolvable CI marked Absent + duplicate new CI [5].
- **Serial numbers** drive asset tracking; any non-standard serial format (custom prefixes) breaks matching → dupes. Never alter serial number syntax in sensors/patterns [5].
- Mark serial numbers as identifiers; they're stored in `cmdb_serial_number` [5].

**B. Payload-side source matching (fast lane).** If the payload carries `sys_object_source_info` with `source_name` + `source_native_key`, IRE matches on that directly — no rules needed, no dup risk from attribute drift. `glide.identification_engine.skip_sys_object_source_matching=true` forces rule-based instead (use when attributes churn but keys don't) [7][10].

**C. Classifiers & process handlers.** Process classifiers' handler scripts strip unstable parameters from process command lines before they reach identification — this is what prevents dup application CIs; disabling handlers re-enables dupes [4].

**D. Global uniqueness properties.** `glide.discovery.enforce_unique_ips`, `glide.discovery.enable_mac_address_verification`, `glide.identification_engine.skip_duplicates` (+threshold=5) [1][10]. Caveat on enforce_unique_ips: clears IP everywhere it appears — a NAT/shared management IP will be wiped from siblings; size the blast radius first.

**E. Remediation backstop.** IRE groups duplicates into **de-duplication tasks** (auto-generated when IRE detects dupes; otherwise manual creation). Bulk: CMDB Workspace → De-duplication Dashboard + Template Library. Single: Duplicate CI Remediator wizard (Main CI selection, merge attribute values / relationships / related items) [14]. Remediation properties [15]:
`glide.duplicate_ci_remediator.dry_run=true` (default false) — safe rehearsal; `.max.cis=1000` (≤5000); `.max.field_length=4000` (attributes longer than this are excluded from Select Main/Merge steps); `.related_items_blacklist` (default blocks asset/cert/expense merges: `cert_task.cmdb_ci,cert_audit_result.configuration_item,discovery_log.cmdb_ci,alm_hardware.ci,alm_asset.ci,fm_expense_line.ci`); `.merge_related_items_enhanced=true` (ignore DB errors / skip workflows on related tables so remediation completes); `.enable_restricted_mode` for complex estates. Role `sn_cmdb_admin`/`admin` required [15]. `duplicate_of` on duplicates points at main CI; no chains [14].

**F. Detection signals.** A large number of de-duplication tasks usually means **weak identification rules**, not bad luck — strengthen entries before mass remediation [9][14].

## 6. Insert vs update — how IRE decides, and how to stop the wrong write

Identification outcome → action [7][8][9]:

| match? | action | controlled by |
|---|---|---|
| CI matched | **update** (or no-op) | identification rules / source matching; **reconciliation rules** decide *which attributes this source may write* [11] |
| no match | **create** (insert) | identification rules / source matching; **IRE data source rules** can forbid inserts entirely [13] |
| matched but class change would help | reclassification (up/down/switch) | `glide.class.{upgrade,downgrade,switch}.enabled`, `glide.identification_engine.update_without_*_enabled`; or payload flags `updateWithoutUpgrade|Downgrade|Switch` in `settings` block (flags win over properties) [7][10] |
| matched / no match, under-supplied payload | partial item / incomplete item | `partial_payloads` (default on), `partial_commits` (on), `deduplicate_payloads` (on), `generate_summary` (off) on `CreateOrUpdateCIEnhanced()` [7][8] |
| source inserts prohibited class | payload fails + stored | IRE data source rule `insert_not_allowed=true` → error `INSERT_NOT_ALLOWED_FOR_SOURCE` [13] |

Reconciliation semantics (who wins a write) [11]:
- **Static rules** — legacy; per-class, per-attribute, priority ordered; child overrides parent; overlapping attribute grants coexist (no exclusion). One rule required per authorized source per attribute; empty Attribute list = all class attributes. Stored `cmdbreconciliationdefinition`(docs spelling) / actual table `cmdb_reconciliation_definition` — verify with `cmdb_reconciliation_definition.list` before relying on either spelling.
- **Dynamic rules** — based on CMDB 360 observed values (largest/most reported) across sources; take precedence over static at same class level; one dynamic rule per class+attribute; needs CMDB 360; stored `cmdb_dynamic_reconciliation_definition`.
- **Data refresh rules** — mark a CI stale *for a specific source* so a lower-priority authorized source may then update it.
- Child overrides parent **even for mixed static/dynamic** at the same level; dynamic beats static at the same level [11].
- Null handling: lower-priority source can fill an empty field (`glide.reconciliation.override.null=true` default) [10].
- **Reclassification task** instead of write when class change blocked/disabled — review these; they batch silently otherwise [9][10].
- **Reconciliation is update-only.** Inserts skip reconciliation entirely; inserts are gated only by identification + IRE data source rules [8].
- **createOrUpdateCI()**: no partial commits — **any failing item fails the whole payload**. **CreateOrUpdateCIEnhanced()**: `partial_commits` (default true) commits the good items and parks the bad ones as partial/incomplete payloads; enabling `partial_payloads` implies both [7][8].
- Partial payload lifecycle: stored in `cmdb_ire_partial_payloads` (+`cmdb_ire_partial_payloads_index` for key matching), merged on next matching source payload, ≤90 days retention, `glide.identification_engine.partial_payload_items_max_size=1000` cap, fetch limits 2000/5000 [7][10]. Incomplete payloads never process; diagnostic only (`cmdb_ire_incomplete_payloads`) [7].
- **Reconciliation has no staging area** — updates commit in real time as processed [8]. Test with `identifyCI()` / `identifyCIEnhanced` (no commit) before pointing a new integration at prod [8]. Identification simulation is the UI equivalent [9].
- Ordering inside a payload: dependent CIs are identified **after** their independent host (Tomcat only after Windows Server identified) — dependency classification forces order [7].
- `first_discovered`/`last_discovered` always stamped by IRE; payload wins only if newer (`glide.identification_engine.skip_updating_source_last_discovered_if_older=true`) [7][10].

## 7. Tables at a glance

| table | holds |
|---|---|
| `cmdb_ci*` (e.g. cmdb_ci_hardware, cmdb_ci_linux_server, cmdb_ci_win_server) | the CIs Discovery writes |
| `cmdb_identifier` / `cmdb_identifier_entry` | identifier rules / their attributes (set Identification Rule=true, Order, Optional condition, Active) [5] |
| `cmdb_reconciliation_definition` / `cmdb_dynamic_reconciliation_definition` | static / dynamic reconciliation rules [11] (spelling per docs: "cmdbreconciliationdefinition" — doc artifact) |
| `cmdb_ire_data_source_rule` | insert bans per source×class (child derives/overrides; single active rule per pair; doesn't apply to lookup/related items) [13] |
| `cmdb_ire_partial_payloads` / `cmdb_ire_partial_payloads_index` / `cmdb_ire_incomplete_payloads` | partial (recoverable) / key index / incomplete (dead) payloads [7] |
| `cmdb_serial_number` | serial numbers + type (driving asset tracking) [5] |
| `discovery_log`, `discovery_log` items / ECC queue | run diagnostics; `discovery_log.cmdb_ci` is blacklisted from de-dup merges by default [15] |
| `sys_object_source_info` (payload section) / `sys_object_source` | source name/native key/feed/recency → fast unique match [7] |
| `cmdb_ci_network_adapter` | adapter search (MAC/IP) from hardware/storage rules [5] |
| `cmdb_ire_partial_payloads`… | (see above) |
| `duplicate_of` field on CI | reference to main CI during/after de-dup [14] |

Admin entry points: `Configuration > CI Class Manager`, `Configuration > Identification/Reconciliation > {IRE Data Source Rule, Reconciliation rules, Data refresh rules, Identification rules}`, `Configuration > CMDB Properties > {Identification/Reconciliation Properties, Duplicate CI Remediator Properties}`, `Configuration > Identification Logs`, `All > Discovery Definition > Properties` [1][9][13][15][16].

## 8. Operational runbook (new MID → first scheduled Discovery, no dupes)

1. MID Server + validate + cluster sane.
2. Credentials scoped per subnet; test one host via Quick Discovery.
3. Review/confirm Identifier rules (or create per-OS class rules); confirm `glide.discovery.use_cmdb_identifiers=true` (auto-true with Service Mapping).
4. Enable `glide.discovery.enable_mac_address_verification`; leave `enforce_unique_ips=false` until you know shared IPs; if you turn it on, watch NAT'd devices.
5. Set reconciliation rules for every source that will write (Discovery included), attribute-level for `name` at minimum; empty-attributes for trusted sources. Add Data Refresh rules rather than granting blanket write to anything you don't trust yet.
6. IRE data source rules: forbid low-fidelity sources (e.g. IP scan) from *inserting* server-class CIs; allow updates only [13].
7. Keep `glide.identification_engine.skip_duplicates=true`, threshold=5; watch de-duplication task counts weekly.
8. Increase Order-separated custom identifier rules instead of editing baseline rules; deactivate instead of delete.
9. `glide.discovery.debug.ci_identification=true` + `glide.cmdb.logger.source.identification_engine=debug` for a **time-boxed** window only; revert after.
10. Post-run: check Discovery Home, Identification Logs, de-dup tasks; retire duplicated adapters by name-change policy (never rename NIC labels on bonded channels).

## 9. Failure modes & where to look

| symptom | cause / check |
|---|---|
| New CI created for same host daily | identification too weak → add/strengthen entries, check serial numbers present, check `use_cmdb_identifiers` |
| CPU/RAM swap of two bonded-NIC hosts | name-based rule required; confirm both adapters actually differ by `name` and that name isn't reused |
| Payload rejected entirely | `createOrUpdateCI()` + one bad item → switch to `CreateOrUpdateCIEnhanced()` or fix payload; read error `INSERT_NOT_ALLOWED_FOR_SOURCE` against IRE data source rules |
| Stale `last_discovered` not updating | `glide.identification_engine.skip_updating_source_last_discovered_if_older` semantics [10] |
| CI listed as Absent then duplicate created | adapter/host renamed → name-rule mismatch [5] |
| Rollback needed after bulk remediation | `glide.duplicate_ci_remediator.dry_run=true` first; keep main CI selection explicit [15] |
| Reclassification silently blocked | reclassification tasks piling up → inspect `glide.class.*` and `update_without_*` [10] |
| Duplicates via import sets | route imports through `CMDBTransformUtil`/IRE application services, identification applies there too [8][9] |

## 10. Release pinning & cross-release notes
Australia only above. Zurich & Yokohama publish the same property pages (r/zurich/..., r/yokohama/...) with identical names for the Discovery + IRE property sets referenced here; no deltas were diffed. Madrid+ = HTTP classification floor; Geneva+ = CMDB identifiers available (`use_cmdb_identifiers` required only for pre-Geneva upgrades); Service Mapping forces new identifiers always.

## 11. UNVERIFIED / out of scope
- Sizing numbers for MID Servers, ECC throughput, pattern NLU — out of scope.
- Whether your instance's static rule table is spelled `cmdbreconciliationdefinition` (Australia docs) vs `cmdb_reconciliation_definition` — docs inline the former; verify on the gaming instance with `.list`.
- Exact default for `glide.discovery.discoverable.network.max.netmask.bits` — the docs table shows the property but the raw text capture didn't include the default value; treat as docs-table-only.
- Dynamic IRE production behaviour (`dynamic_ire.enabled=false` default) — documented, not exercised.
- Zurich/Yokonoma property diffs — not diffed; pin re-fetch if the org needs it.
- Table `cmdb_identifier_entry` Optional condition support depends on the base-system pre-configuration noted; review via `cmdb_identifier_entry.list` before enabling.
- KB articles cited by docs (KB0750382/83/86, KB0756709, KB1542272) not opened — NeedNow Support access required.
