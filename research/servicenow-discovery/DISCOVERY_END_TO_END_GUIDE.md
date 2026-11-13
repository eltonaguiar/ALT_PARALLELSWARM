# ServiceNow Discovery — End-to-End Configuration Guide (Australia)

Agent: `inkling-2-small__openrouter__kilo` · Model `openrouter/thinkingmachines/inkling-2-small:free` · Provider **OpenRouter** (free tier) · Harness Kilo
Release pin: **Australia**. Property names/defaults transcribed from the Australia docs fetched 2026-11-13 (see §16 source index, [n] tags). Docs pages move; verify on your instance via `sys_properties.list` before changing anything.

Scope: horizontal (IP-scan) Discovery — MID Server → schedules → Shazzam/port probes → classification → identification → exploration → CMDB write. Cloud patterns, ACC, Service Mapping, and OT Discovery are referenced only where they intersect the same mechanisms.

---

## 1. The moving parts

- **MID Server** — host application on the network that polls the instance ECC queue, executes probes/patterns/sensors against targets, and returns results over the network firewall to the instance. Required; the instance never touches target devices directly. [2][21]
- **ECC queue** — the hand-off table. Work is placed there by the instance (or MID); both sides poll it.
- **Sensors / probes / patterns** — probes gather; sensors process returned data; patterns (structured, reusable logic incl. identification ops) are an alternative to probe+sensor stacks.
- **IRE (Identification and Reconciliation Engine)** — decides if a discovered item matches an existing CI (update) or is new (insert), and which source may write which attribute. All writes to the CMDB from Discovery go through IRE. [7][8]

Runtime flow of one IP across **five phases** [2]:

```
 schedule/quick-discovery
        │
  1 SCAN ─ Shazzam + port probes (ECC queue → MID) ── open ports → machine type
        │
  2 CLASSIFY ─ one classification probe per device ── OS/type → CI class
        │
  3 IDENTIFY ─ identifier rules (or pattern identifier ops)
        │        match?→ update / no match?→ create   ←── IRE lives here
        │
  4 EXPLORE ─ exploration probes/patterns from the classifier's
        │        Triggers Probes list; sensors update CMDB/update records
        │
  5 COMMIT ─ IRE: identification → reconciliation → insert/update in CMDB
```

Patterns: the identity probe is **not used**; pattern operations + identifier rules perform identify and explore together [6].

## 2. Zero → first successful Discovery (order of operations)

0. **Roles.** `discovery_admin` for setup (schedules, credentials), `sn_cmdb_admin`/`admin` for IRE/CMDB Properties, `itil_admin` for IRE rules edits. (Least-privilege varies per org; verify on instance.)
1. **MID Server(s).** Install on a supported host in the target network segment. Prepare outbound HTTPS to the instance; download site for the MID package. After install, **Validate** from the instance; encryption of `config.xml` parameter values; auto-upgrade from `install.service-now.com`; MID cluster for scale/HA [21][22][23].
2. **Network prep.** IP ranges to scan; SNMP community strings; WMI/SSH service accounts; firewall ACLs from MID host to targets on 135/445 (WMI), 22 (SSH), 161/162 (SNMP), 80/443 (HTTP/HTTPS).
3. **Credentials + credential affinity.** Instance tries all credentials until one works, then pins the pair in `dscy_credentials_affinity`. Changing creds triggers a re-try cycle. With Orchestration+Discovery and credential aliases enabled, lowest-order affinity wins [19][20].
4. **ITOM Configuration Console (optional fast path).** Single-place wizard for assigning admins, deploying/validating MIDs, credentials, schedules, diagnostics; task guidance v28.3.1+ [18].
5. **Discovery schedule.** `Discovery > Discovery Definition > Schedules` (IP) or the Cloud Discovery Workspace form [15]. Fields (IP schedule): name, MID selection type (auto/specific MID or MID cluster), behavior, IP ranges (CIDRs or IPs), run frequency, credentials to use, **Discover** attribute = `CIs` (drives schedule-monitoring types). Auto-select chooses an appropriate MID; clusters distribute jobs equally [15].
6. **Shazzam/port probes** fire per schedule; results queue back [2].
7. **Classification** → class chosen; **identification** → update/create into CMDB via IRE; **exploration** → detail attributes [2][4][5].
8. **Verify**: Discovery Home (`Discovery > Home`) tiles: Schedules, Discovered Devices, Cloud Resources, Errors [24]; **Discovery Admin Workspace** for errors/anomalies [25]; Identification Logs (`Configuration > Identification Logs`) [10]; Discovery log (`Discovery > Logs`).
9. **Tune duplicates** before scaling out (sections 6–9).
10. **Promote to prod** after one clean schedule run + CMDB spot-checks.

## 3. Scan phase — Shazzam & port probes

Shazzam sends port probes per the scan range; the port-probe record that got a response selects the classification probe. Protocol priority is fixed: WMI/SSH/SNMP first; HTTP 80/443 last — HTTP only classifies if Shazzam saw 80/443 open **and** the higher-priority probes failed [2][4]. If you see devices classified over HTTP, it usually means WMI/SSH/SNMP credentials are wrong — fix creds, don't tune HTTP.

Key MID-side scan knobs (mid.* properties, set on the MID Server `config.xml` or MID Server Properties) [26]:
`mid.shazzam.threads`, `mid.shazzam.max_scanners_per_thread`, `mid.shazzam.regulator.interval_ms`, `mid.shazzam.regulator.packets_per_interval` — tune when you hit packet-loss detection or scan too fast on sensitive gear (regulate gently). `mid.eccq.max_payload_size`, `mid.discovery.max_payload_size` (payload caps), `mid.discovery.max_total_items_size_per_page`, `mid.discovery.max_related_count_per_page`, `mid.discovery.max_relation_count_per_page`, `mid.discovery.multiprobe.skip_others_on_error`, `mid.probe.use_legacy_reverse_dns`/`use_legacy_forward_dns`, `mid.probe.collect_debug_info` [26].

Instance-side: `glide.discovery.shazzam_simplify_ranges=true` (default) de-dupes overlapping ranges of a single-behavior schedule; multiple behaviors keep duplicates [1]. `glide.discovery.shazzam_ranges_json=true` (default) — JSON-encodes ranges (much smaller payloads) [1].

## 4. Classification — which probe, which class

Classifier decides probes/patterns for identification + exploration. Three classification types [4]:

- **Device classification** — OS/network gear types (Windows/Linux/router/switch/...). Madrid+ can classify over HTTP as fallback.
- **Process classification** — classifies applications during exploration; creates child CIs (`Runs on::Runs on` relationships); process handler scripts strip unstable params so the same app doesn't get duplicated. Process classifier conditions are case-sensitive.
- **IP address (IP scan) classification** — credential-less; uses open ports + banners.

Criteria = parameter + operator + value. Classifier specifies **Triggers Probes** (related list). Pattern alternative: `Horizontal Pattern` probe on the classifier → pattern runs for identify+explore; classifier criteria decide pattern match [2][4].

Debug: `glide.discovery.debug.classification=true` → logs which classifier ran + criteria names/values [4].

## 5. Identification — identifiers & IRE

### 5.1 Classic identifier rules (what Discovery queries first) [5][6]
`Identifier [cmdb_identifier]` + `Identifier Entry [cmdb_identifier_entry]`.
Defaults shipped: Hardware [cmdb_ci_hardware] (serial_number, serial_number_type, name, ip_address, mac_address + *Search on* Serial Number and Network Adapter tables), ESX Server (correlation_id), Storage Server, WBEM Service. A class-specific rule (e.g. `cmdb_ci_linux_server`) beats overloading Hardware; for NIC-bonded hosts add `name` to distinguish bonded interfaces (and **never rename those adapters**).
- Independent classes can't use `sys_class_name` as an entry.
- Rules parse **low Order → high Order**; entries likewise; custom rules need distinct Order; deactivate (Active=false) to turn off — don't delete.
- *Optional condition* on entries narrows match scope (requires `glide.identification_engine.enable_identifier_optional_condition=true`; review pre-configured entries first) [10].
- CMDB identifiers (IRE framework) are the default since Geneva; `glide.discovery.use_cmdb_identifiers=true` (default true) — Service Mapping forces on regardless [5][1].
- Source-side fast path: payload `sys_object_source_info` with `source_name`+`source_native_key` matches directly — no rules consulted. `glide.identification_engine.skip_sys_object_source_matching=true` forces rules anyway [7][10].

### 5.2 IRE end-to-end [7][8][10]
Payload enters → validate → build identifier keys → match existing CIs via rules/source keys → **reconcile** (only if updating; inserts skip reconciliation) → commit. Enhanced APIs: `CreateOrUpdateCIEnhanced()` defaults on: `partial_payloads`, `partial_commits`, `deduplicate_payloads`; `generate_summary` off. Plain `createOrUpdateCI()` = no partial commits — **one bad item fails the whole batch**.
- **Partial** items (recoverable): stored `cmdb_ire_partial_payloads` (+`cmdb_ire_partial_payloads_index`), merged in on later matching payloads; ≤90 days; `glide.identification_engine.partial_payload_items_max_size=1000`; fetch limits 2000/5000.
- **Incomplete** items: logged to `cmdb_ire_incomplete_payloads`, never processed (diagnostic only).
- **Reclassification**: class change blocked by `settings` flags (`updateWithoutUpgrade|Downgrade|Switch`, flags win over properties) or properties `glide.class.{upgrade,downgrade,switch}.enabled` (default true) / `glide.identification_engine.update_without_{upgrade,downgrade,switch}_enabled` (default false; latter take precedence and process update but skip the class move). Blocked → reclassification task for review (enable `glide.identification_engine.reclassification_restriction_rules_enabled`, default true) [10].
- Reconciliation **is real-time and has no staging area**; test with `identifyCIEnhanced`/`identifyCI` (dry-run) or Identification simulation UI before live use [8].
- Dependencies force identification order: dependent CI identified **after** its independent host (Tomcat after the Windows Server) [7].
- Timestamps override payload staleness: IRE stamps `last_discovered`/`discovery_source` always; payload wins only if newer (`glide.identification_engine.skip_updating_source_last_discovered_if_older=true` default) [7][10].
- Serial numbers → `cmdb_serial_number` (with type). Non-standard formats break asset tracking + matching [5].

## 6. Reconciliation — source precedence (who may write what)

Static rules (legacy, `cmdbreconciliationdefinition` per Australia docs — verify `cmdb_reconciliation_definition.list`): per class + attribute + priority; one rule required per authorized source per attribute; child class overrides parent; an empty Attribute list authorizes the whole class; multiple sources may co-authorize the same attribute (coexist, no exclusion) [11].

Dynamic rules (`cmdb_dynamic_reconciliation_definition`): pick largest/most-reported value across CMDB 360 history; needs CMDB 360; one dynamic rule per class+attribute; dynamic wins over static at the same class level [11].

Data refresh rules: mark a CI **stale for a specific source** → unblocks lower-priority authorized sources to update. Create from the CI Class Manager [11][16].

Rules of the road [10][11]:
- No rules = `Discovery`/`ImportSet`/`ManualEntry` etc. **overwrite each other freely**. Always create rules for every source you trust to write.
- Authorization is attribute-scoped; override by child rules.
- Lower-priority source **can** fill an empty field (`glide.reconciliation.override.null=true` default).
- Reference sources in rules by their `discovery_source` value (e.g., `Discovery`, `SCCM`, `ManualEntry`, `EventManagement`).
- Domain-separated rules apply to child domains unless overridden [10][11].

### Worked example
`cmdb_ci_computer`: Discovery authorized to update `name` on the class + children.
`cmdb_ci_linux_server`: ServiceWatch authorized to update `name` **and all other attributes** (empty Attributes) — child rule; Discovery no longer writes `name` on Linux servers, but keeps it on every other computer subclass [11].

## 7. IRE data source rules — "is this source allowed to insert?"

`IRE Data Source Rule [cmdb_ire_data_source_rule]` (`Configuration > Identification/Reconciliation > IRE Data Source Rule`): forbid a source×class **insert** while still letting it **update** [13].
- Use case: IP scan tool legitimately discovers network gear but must not create half-empty server CIs.
- Child classes derive rules; child rule overrides parent; one active rule per source×class; doesn't apply to lookup/related items; no effect when dynamic reconciliation rules govern the attribute [13].
- Blocked insert → `INSERT_NOT_ALLOWED_FOR_SOURCE` error; under `CreateOrUpdateCIEnhanced()` the item parks in partial payloads (recoverable later); under plain `createOrUpdateCI()` the **whole payload fails** [13].
- When a permitted source later inserts the same CI, IRE merges with the parked partial payload, deletes it, and re-permits updates by the previously-blocked source [13].

## 8. Preventing duplicates — every layer

| layer | knob | default | note |
|---|---|---|---|
| identification rules | serial/name/mac/ip entries, Order [5] | tuned per class | weak rules = #1 cause of dupes |
| identifier *Optional condition* | `glide.identification_engine.enable_identifier_optional_condition` | false | enable only after reviewing pre-configured entries [10] |
| source native keys | `sys_object_source_info` in payload | n/a | fastest, zero-rule path [7] |
| force rules over keys | `glide.identification_engine.skip_sys_object_source_matching` | false | use true when keys stable + attributes churn [10] |
| duplicate pick at match time | `glide.identification_engine.skip_duplicates` + `.threshold=5` | true/5 | oldest becomes main; others get `duplicate_of`→main; above 5, identification errors instead [10] |
| IP uniqueness | `glide.discovery.enforce_unique_ips` | false | clears IP on other CIs when a valid IP re-appears — strong but will wipe NAT/shared IPs; size blast radius [1] |
| MAC verification | `glide.discovery.enable_mac_address_verification` | false | stops IP-change dupes; enable for DHCP'd fleets [1] |
| unique per-IP class list | `glide.discovery.exclude_ip_sync_classes` | `cmdb_ci_lb` | keep LB mgmt IPs unsubstituted [1] |
| hostname match hygiene | `glide.discovery.hostname.{include_domain,case,hostname.{snmp,ssh,wmi,dns_nbt}_trusted}` | see §10 tables | Australia flips snmp/ssh/wmi_trusted + ip_service_affinity to **true for new customers** [1] |
| host name stability | adapter renames → Absent + new CI | n/a | don't rename bonded NIC labels [5] |
| serials | `cmdb_serial_number`, forbid custom prefixes/sn syntax edits | n/a | base truth for asset IDs [5] |
| process classifier handlers | strip volatile params (paths w/ pids, ports) | n/a | prevents app-CI dupes [4] |
| CMDB Health | staleness/orphan/compliance rules, sync complete rules per class | per env | finds dupes as they happen [16] |
| de-dup remediation | de-dup dashboard/templates + Duplicate CI Remediator | n/a | see §9 |
| Discovery vs SCCM | `glide.discovery.software_sccm_managed=true`; simplify props | false | stop double-sourcing software rows [1] |

### 8.1 De-duplication remediation flow [14][15]
IRE groups dupes into **de-duplication tasks** (auto-generated; manual creation supported). Review → pick **Main CI** → merge selected attribute values/relationship/related items into Main → dupes get `duplicate_of` reference (no chains; `duplicate_of` of a Main cannot reference another dup) [14].
Execution paths: **De-duplication Dashboard / Template Library** in CMDB Workspace/Service Graph Workspace (bulk); **Duplicate CI Remediator** wizard (single).
Properties (`Configuration > CMDB Properties > Duplicate CI Remediator Properties`, role `sn_cmdb_admin`/`admin`) [15]:
`glide.duplicate_ci_remediator.dry_run` (default false — **run with true first**), `.max.cis` (1000, ≤5000), `.max.field_length` (4000), `.related_items_blacklist` (default blocks cert_task.cmdb_ci, cert_audit_result.configuration_item, discovery_log.cmdb_ci, alm_hardware.ci, alm_asset.ci, fm_expense_line.ci), `.merge_related_items_enhanced=true` (skip BRs/errors), `.enable_restricted_mode` (false; complex states only).

### 8.2 Detection signals
- De-dup task volume rising = weak identification rules, not bad luck. Strengthen rules before mass-remediating [9][14].
- Discovery Home Errors tile + Identification Logs + `glide.identification_logs.max_run_ids=1000` [10][24].
- Dynamic IRE comparison: `glide.identification_engine.dynamic_ire.auto_compare=true` (default) compares Dynamic vs Static outputs without switching [10].

## 9. Insert vs update — decision matrix

| situation | IRE behavior | knob |
|---|---|---|
| Matched CI, this source may write attribute X | update (or skip) | static/dynamic reconciliation rule [11] |
| Matched CI, source may update class but not attr X | attribute skipped; others committed | attribute-scoped rule [11] |
| Insert prohibited for this source×class | payload item fails; parked partial (Enhanced) / whole payload fails (createOrUpdateCI) | IRE data source rule [13] |
| Matched, insufficient attrs (partial) | parked partial (90d) | `partial_payloads` default on [7] |
| Matched, class move available, allowed | reclassify (upgrade/downgrade/switch) | `glide.class.*` / `update_without_*` / payload flags [7][10] |
| Matched, class move blocked | reclassification task | `reclassification_restriction_rules_enabled` [10] |
| Duplicate set ≤ threshold (5) at match | oldest = Main; others `duplicate_of` | `skip_duplicates` [10] |
| Duplicate set > threshold | identification error (skip_duplicates forced false) | `skip_duplicates.threshold` [10] |
| Source is lower priority, field already filled by higher | attribute skipped | static precedence ordering [11] |
| Field empty, lower priority exists | filled (override-null) | `glide.reconciliation.override.null=true` [10] |
| Stale source tries to back-write last_discovered | skipped if older | `glide.identification_engine.skip_updating_source_last_discovered_if_older` [7][10] |

## 10. Discovery properties — full catalog (Australia)

Editable at **Discovery Definition > Properties** (or `sys_properties.list`), salvo noted. Grouped by the sections on the Australia page [1]. ✓ = duplicate/CMDB-write relevant.

### 10.1 IP properties
| property | default | notes |
|---|---|---|
| ✓ `glide.discovery.exclude_ip_sync_classes` | `cmdb_ci_lb` | classes whose IPs stay as-discovered (mgmt IP kept on LBs) |
| ✓ `glide.discovery.enforce_unique_ips` | `false` | clears shared IP from sibling CIs; see §8 |

### 10.2 Network properties
| property | default | notes |
|---|---|---|
| `glide.discovery.bgp_router_disable` | `true` | skip BGP exploration; false → OOM risk on MID |
| `glide.discovery.debug.network_discovery` | `true` | extensive NetDisc logging |
| `glide.discovery.discoverable.network.max.netmask.bits` | `28` | regular networks ≤/28 not discovered; anything else discovers everything |
| `glide.discovery.network_owner_method` | `Most Networks` | router↔network association (also First/Last/Least Networks) |
| `glide.discovery.physical_interface_types` | `6,117,9,71,209` | ifType MIB-2 list |
| `glide.discovery.switch_interface_types` | `7,8,9,26,53,62,69,71,78,115,117,209` | not matching → router if routed |
| `glide.discovery.virtual_interface_types` | `53` | virtual ifType |
| `glide.discovery.L3_mapping` | `true` | map servers/network devices to L3 routers |
| `glide.discovery.network_discovery.functionality` | `SNMP only` | usually correct |
| `glide.discovery.allow_loopback_adapters` | `false` | loopbacks as NICs |
| `glide.discovery.mark_esx_servers_as_absent` | `false` | absent not retire |
| `glide.discovery.sensors.fire_ssh_probe` | `true` | SSH if LB/VIP missing in SNMP |
| `glide.discovery.sensors.netapp_native_7mode` / `.netapp_native_cluster_mode` | unset | native NetApp vs SMI-S |
| `glide.discovery.sensors.save_attachments` | `true` | keep ECC attachments post-processing |

### 10.3 Host name identity (huge for dupes) ✓
| property | default |
|---|---|
| `glide.discovery.hostname.always_update` | `true` |
| `glide.discovery.hostname.case` | `Lower case` (also Upper/No change) |
| `glide.discovery.hostname.include_domain` | `false` |
| `glide.discovery.hostname.dns_nbt_trusted` | `true` |
| `glide.discovery.hostname.snmp_trusted` | `false` → **true for new Australia customers** [1] |
| `glide.discovery.hostname.ssh_trusted` | `false` → **true new AU customers** [1] |
| `glide.discovery.hostname.wmi_trusted` | `false` → **true new AU customers** [1] |
| `glide.discovery.domain.name.nbt` | `true` (Windows domain from NBT; else WMI) |
| `glide.discovery.fqdn.regex` | `^([^.]+)\.((?:[^.]+\.)+[^.]+)$` |
| `glide.discovery.ip_service_affinity` | `false` → **true new AU customers** [1] |
| `glide.discovery.ip_based.active` | `true` (probe→pattern migrations) |
| ✓ `glide.discovery.enable_mac_address_verification` | `false` |
| ✓ `glide.discovery.use_cmdb_identifiers` | `true` |

### 10.4 Software discovery
| property | default |
|---|---|
| `glide.discovery.discover_software` | `true` |
| `glide.discovery.populate_software_instance_table` | `false` (pre-Jakarta SAM only) |
| `glide.discovery.software_sccm_managed` | `false` — true stops Discovery from writing software for SCCM-managed computers |
| `glide.discovery.software_filter_keys` | `Language Pack, Hotfix Security Update` |
| `glide.discovery.enable.software_filter` | `true` |
| `glide.discovery.enable.software_simplify` | `true` (strips version cruft; off → dup software rows) |
| `glide.discovery.enable.software_simplify_sccm` | `false` |
| `glide.discovery.active_processes_filter` | `false` (perf optimization for ADM) |

### 10.5 Process/Application dependency mapping (ADME)
| property | default |
|---|---|
| `glide.discovery.application_mapping` | `true` |
| `glide.discovery.enable_adme` | `false` |
| `glide.discovery.adme.sampling_interval` | `120` s (min 5) |
| `glide.discovery.adme.aggregation_interval` | `3600` s |
| `glide.discovery.adme.rolling_window_size` | `24` chunks |
| `glide.discovery.adme.max_total_samples` | `100` |
| `glide.discovery.adme.base_dir_unix` | `false` (path expected when set) |
| `mid.powershell.target_base_dir` | `admin$\temp` |
| `glide.discovery.adm.update.applications` | `true` (Tokyo+; absent→install_status=absent) |

### 10.6 Event Framework & perf
| property | default |
|---|---|
| `discovery.use.event.processing` | `false` |
| `discovery.event.separate.cloud.events` | `true` |
| `discovery.event.pin.jobs` | `false` |
| `com.glide.queue.discovery.sensors.processing_jobs.priority` | `100` |
| `com.glide.queue.discovery.cloud.sensors.processing_jobs.priority` | `100` |
| `glide.discovery.count.use_optimized_counter` | `true` |
| `glide.discovery.perf.metrics.enable_collection` | `true` |
| `glide.discovery.perf.metrics.rollup_by_{build,status,target}` | all `true` |
| `glide.discovery.log_debug` | `false` |
| `glide.discovery.log_message_length` | `200` (0/neg disables limit) |
| `glide.discovery.debug.ci_identification` | `false` |
| `glide.discovery.save_pattern_log` | `true` (false ⇒ save only on failure) |
| `glide.discovery.use_probe_results_cache` | `false` |
| `glide.discovery.warn_minor_version` | `false` |

### 10.7 Scheduling & monitoring
| property | default |
|---|---|
| `glide.discovery.max_concurrent_invocations_per_schedule` | `3` (0/neg disables) |
| `glide.discovery.schedule_ipv4_limit` | `65,536` |
| `glide.discovery.schedule_ipv6_limit` | `20,000` (≤5,000 pre-ZP3/YP9) |
| `glide.discovery.schedule.autogenerate.group` / `.debug` | empty / false |
| `glide.discovery.schedule_monitoring.dry_run` | `false` |
| `glide.discovery.schedule_monitoring.schedule_types_to_monitor` | `CIs` |
| `glide.discovery.schedule_monitoring.stale_check_seconds` | `1200` (2× job interval fallback) |
| `glide.discovery.retire_stale_accounts` | `false` |
| `sn_disco_workspace.discovery_schedule_anomaly_detection_disabled` | `false` |
| `sn_disco_workspace.discovery_schedule_anomaly_detection_method` | `ML-based` |
| `sn_disco_workspace.discovery_schedule_anomaly_discover_type` | `CIs, Cloud Resources` |
| `sn_disco_workspace.discovery_schedule_anomaly_ml_model_sensitivity` | `low` |
| `sn_disco_workspace.discovery_schedule_{cis_discovered,error,runtime}_anomaly_threshold` | `20`% each |
| `sn_disco_workspace.discovery_stats_time_scale` | `7` |
| `sn_disco_workspace.enable_auto_create_schedules` | `false` (IPAM-driven) |
| `sn_disco_workspace.enable_error_framework` | `true` |
| `sn_disco_workspace.visibility_diagnostic_utility.enabled` | `false` |
| `glide.discovery.roundingInterval.cpu` / `.ram` | `1` MHz / `1` MB |
| `glide.discovery.count.use_optimized_counter` | `true` |

### 10.8 Certificates & cloud/AWS SSM
| property | default |
|---|---|
| `glide.discovery.certs.cert_admin_user_id` | `Certificate Administrator` |
| `glide.discovery.certs.days_before_expiration_to_create_renewal_task` | `60` |
| `glide.discovery.certs.enable_incident_creation_for_expired_certificates` | `false` |
| `glide.discovery.certs.enable_renewal_task_creation_for_discovered_certificates` | `true` |
| `glide.discovery.certs.slack_channel_id` | `empty` |
| `sn_disco_certmgmt.enable_csr_generation` | `false` |
| `sn_disco_certmgmt.private_key_size` | `2048` (512/1024/2048/4096) |
| `glide.discovery.enable_ssm` | `false` (AWS SSM discovery) |
| `glide.discovery.ssm.enable_windows` | `false` |
| `glide.discovery.discover_aws_ec2_host_metadata` | `true` |
| `glide.discovery.discover_azure_host_metadata` | `true` |
| `glide.eccprobe.awsrestprobe.max_retries` | `4` |
| `glide.eccprobe.awsrestprobe.max_wait` | `30`s |

### 10.9 ECC/queue hygiene
| property | default |
|---|---|
| `glide.eccprobe.max_queued_probes_per_run` | `20` |
| `glide.eccprobe.node_agent_id` | `NODE_AGENT` |
| `glide.ecc_agent.validated.override` | `false` |
| `com.snc.use_external_credentials` | `true` |
| `com.glide.codesigning.tracking.unsupported_script_tracking.enabled` | `true` |
| `sn_disco_firewall.default.rule.task.policy.owner.group` | `Task Owner Group Name` |
| `sn_disco_firewall.default.rule.task.approval.group` | `Approval Group Name` |

### 10.10 MID Server properties (config.xml / MID Server Properties) [26]
| property | default/note |
|---|---|
| `mid.shazzam.threads` | scan threads |
| `mid.shazzam.max_scanners_per_thread` | scanners/thread |
| `mid.shazzam.regulator.interval_ms` / `.packets_per_interval` | regulator cadence/rate |
| `mid.eccq.max_payload_size` | ECC payload cap |
| `mid.discovery.max_payload_size` | discovery payload cap |
| `mid.discovery.max_total_items_size_per_page` | paging cap |
| `mid.discovery.max_related_count_per_page` / `.max_relation_count_per_page` | relations paging |
| `mid.discovery.multiprobe.skip_others_on_error` | bail out whole multiprobe on first error |
| `mid.discovery.aws_ssm.{s3_bucket_name,s3_bucket_region,kms_key_name,kms_key_region}` | SSM integration |
| `mid.discovery.aws_ssm.linux.fallback_root_user` | SSM fallback |
| `mid.discovery.should_minify_pattern_payload` | shrink pattern payloads |
| `mid.probe.collect_debug_info` | probes collect debug info |
| `mid.probe.use_legacy_reverse_dns` / `.use_legacy_forward_dns` | legacy DNS |
| `mid.snmp.use_getbulk` | SNMPv2 bulk |
| `mid.sa.prefer_powershell` | prefer PS over SOAP for Windows |
| `mid.sa.windows.allowable_failures` | SA window failures before mark |
| `mid.ssh.algorithms.{kex,cipher,mac,host_key}` | SSH algorithm pinning |
| `mid.property.ssh.use_snc` / `.jms.command.allowed_factory_names` / `.powershell.use_base64_password` / `.jdbc_operations` | transport/protocol policy |
| `mid.powershell.target_base_dir` | `admin$\temp` |
| `mid.keystore.{max_backups,max_live_backups,backup_overwrite_timespan}` | keystore rotation |
| `mid.jdbc.datastream.max.record.size` / `.fail.when.attachement.limit.exceeded` | JDBC discovery |
| `mid.http_classy.allow_credentials_over_http` | allow HTTP classification creds (unsafe — avoid) |
| `mid.log.command_audit.enable` | command audit logging |
| `mid.use_net_tools` | net tools fallback |
| `mid.servicewatch.*` | process-awareness (netstat/ss paths, max connections) |
| `mid.process_flow.log_listener.max_size` | process flow log cap |

## 11. IRE properties — full list (Australia) [10]
Set at **Configuration > CMDB Properties > Identification/Reconciliation Properties** (role `sn_cmdb_admin`/`admin`) unless noted.
`glide.required.attribute.enabled`=true · `glide.class.upgrade.enabled`=true · `glide.class.downgrade.enabled`=true · `glide.class.switch.enabled`=true · `glide.identification_engine.update_without_upgrade_enabled`=false · `.update_without_downgrade_enabled`=false · `.update_without_switch_enabled`=false (each overrides the corresponding class.* flag) · `glide.identification_engine.reclassification_restriction_rules_enabled`=true · `glide.reconciliation.override.null`=true · `glide.identification_engine.skip_duplicates`=true · `.skip_duplicates.threshold`=5 · `glide.identification_logs.max_run_ids`=1000 · `glide.cache.size.service_cache`=20 (MB) · `glide.identification_engine.granular_insert_locking`=true · `glide.identification_engine.batch_update_last_discovered`=true · `.batch_update_last_discovered.use_execute_lazy`=true · `glide.identification_engine.related_items_local_cache_count`=15000 · `.dependent_items_local_cache_count`=10000 · `.independent_items_local_cache_count`=100000 (0 disables each) · `glide.cmdb.logger.source.identification_engine`=(info/warn/error/debug/debugVerbose; heavy) · `glide.identification_engine.partial_payload_items_max_size`=1000 · `.partial_items_process_limit`=2000 · `.partial_items_process_absolute_limit`=5000 · `.skip_updating_source_last_discovered_if_older`=true · `.skip_updating_last_scan_if_older`=true · `.ire_message_listener_skip_updating_source_last_discovered_to_now`=false · `.ire_message_listener_skip_updating_last_scan_to_now`=false · `.platform_domain_separation_enabled`=false · `.enable_identifier_optional_condition`=false · `.enable_reconciliation_filter_before_update`=false · `.skip_sys_object_source_matching`=false · `.lookup_match.create_duplicate_task_ci.enabled`=false · `.dynamic_ire.enabled`=false · `.dynamic_ire.auto_compare`=true · `.non_dependency_relation.duplicate_detection`=false

## 12. CMDB Health & ongoing hygiene
- Staleness rules per source; orphan rules; compliance audits; certification templates; Health inclusion rules; mandatory/recommended attributes per class [16].
- **Principal Class** flag — keeps default CI lists lean [17].
- Principal-class filter notwithstanding, Discovery touches hardware everywhere — scope your first schedule to one subnet and watch it fail fast.
## 13. Roles, navigation & quick reference

| where | path | purpose |
|---|---|---|
| Schedules (IP) | `Discovery > Discovery Definition > Schedules` | created schedules; Discover attribute = CIs |
| Cloud schedules | Cloud Discovery Workspace | AWS/Azure/GCP/OCI/Alibaba |
| Properties | `Discovery > Discovery Definition > Properties` | sections §10 |
| CI Class Manager | `All > Configuration > CI Class Manager` [16][17] | classes, identification/reconciliation rules, suggested relationships, staleness rules, mandatory attrs, principal class |
| IRE rules | `Configuration > Identification/Reconciliation > {Identification Rules, Reconciliation Rules, Data Refresh Rules, IRE Data Source Rule}` | §6/§7 |
| CMDB Properties | `Configuration > CMDB Properties > {Identification/Reconciliation Properties, Duplicate CI Remediator Properties}` | §11 / §8.1 |
| Identification Logs | `Configuration > Identification Logs` (runs cap 1000) | §8.2 |
| Discovery Home | `Discovery > Home` → tiles Schedules / Discovered Devices / Cloud Resources / Errors [24] | §3 verify |
| Discovery Admin Workspace | errors, anomalies, ML detection [25] | daily ops |
| ECC queue | `% ecc_queue` in nav filter | payload inspection |
| dscy_credentials_affinity | affinity table [19] | see §2 step 3 |
| sys_properties | `sys_properties.list` | every property in §10/§11 |

Roles typically required: `discovery_admin` (Discovery), `sn_cmdb_admin`/`admin` (CMDB/IRE), `mid_server` for MID host service account on target OS, `itil_admin` for IRE rule authoring. Verify on instance.

## 14. Troubleshooting matrix

| symptom | likely cause / first check |
|---|---|
| Device never matched; new CI daily | weak identifier entries → strengthen; check serials; check `use_cmdb_identifiers=true`; read Identification Logs |
| Bonded-NIC host duplicates | name missing from class rule [5] |
| Adapter rename → Absent + re-create | known name-rule behavior [5] |
| CI count flat, errors spike | creds expired → credential affinity stale (`dscy_credentials_affinity`); MID clock/cert; ECC backlog |
| Schedule runs, no probes sent | MID down/not validated; `mid.*` max queued probes; ECC queue processing paused |
| Insert blocked, message `INSERT_NOT_ALLOWED_FOR_SOURCE` | IRE data source rule for source×class [13] |
| Whole payload fails, not partial | plain `createOrUpdateCI()` — switch to `CreateOrUpdateCIEnhanced()` |
| Duplicates from import sets | route through `CMDBTransformUtil` (applies IRE) [8][9] |
| Lower-priority source can't fill empty field | `glide.reconciliation.override.null=true` (default true) [10] |
| stale last_discovered never updates | payload older than CMDB — expected; inspect property [10] |
| Duplicates found weekly | one de-dup task spike = identification rule weakness [9]; remediation: dry_run + templates [15] |
| HTTP-classified Windows boxes | WMI/SSH/SNMP creds broken — fix creds, not classifier [4] |
| CMDB huge / Principal Class empty | filter rule excludes extended classes incorrectly |
| Discovery slow mid-run | raise `mid.shazzam.threads`? NO — first check regulator settings packet rate; check MID CPU; `mid.discovery.multiprobe.skip_others_on_error` |
| Payload dropped on size | `mid.discovery.max_payload_size`, `mid.eccq.max_payload_size` [26] |

Debug properties to use temporarily, then **revert**: `glide.discovery.debug.ci_identification=true`, `glide.discovery.debug.classification=true`, `glide.cmdb.logger.source.identification_engine=debug`, `glide.discovery.log_debug=true`, `mid.probe.collect_debug_info=true`. All are perf killers at scale.

## 15. Runbook: deploy Discovery into a new subnet tomorrow morning

1. MID host: service account, Java 17+, outbound 443 to `<instance>.service-now.com` + `install.service-now.com`, validate green.
2. Credential set for the subnet (WMI read-only + SSH + SNMPRO/SNMPv3 authPriv), test on one host with Quick Discovery.
3. Verify identifier rules for Windows/Linux (defaults OK); enable `glide.discovery.enable_mac_address_verification=true` on DHCP fleets.
4. Reconciliation rules for `Discovery` + any rival sources: at minimum `name` attribute-scoped; full-class authorization for trusted, attribute-scoped for risky. IRE data source rule: none needed unless blocking an insert source.
5. ITOM Configuration Console tasks (or manual schedule): name, MID/cluster, ranges, `Discover=CIs`, schedule off-peak, 1 replica.
6. Run once; check Home tiles + Identification Logs + de-dup task count = 0 - 3. If >3, stop and tune rules, then resume.
7. Freeze Discovery creds rotation cadence; document `dscy_credentials_affinity` remediation steps for on-call.
8. Weekly: de-dup triage + stale-check review + MID version. Monthly: property drift audit vs §10/§11 baseline.

## 16. Source index

All fetched 2026-11-13 via the Australia docs khub content API. `sources/<slug>.txt|html` is the exact retrieved content.
| # | source (Australia) | file |
|---|---|---|
| 1 | Discovery properties (r_DiscoveryProperties) — IP/network/other catalog, defaults incl. Australia-new-customer flips | discovery_properties |
| 2 | Horizontal discovery process flow with probes and sensors (c_DiscoProcessFlows) | horizontal_process_flow |
| 3 | Configuring Discovery (c_DiscoveryConfiguration) — no canonical order page; order reconstructed from 2,4,5,6 | configuring_discovery |
| 4 | Discovery classifiers (discovery-classifiers) | discovery_classifiers |
| 5 | Discovery identifiers (c_DiscoveryIdentifiers) — default rules table, Order, optional condition note | discovery_identifiers |
| 6 | How Discovery identifiers work (c_HowDiscoveryIdentifiersWork) | how_identifiers_work |
| 7 | Identification and Reconciliation Engine (IRE) (ire) — partial/incomplete, API options, reclassification flags | ire_overview |
| 8 | Components and process of Identification and Reconciliation (c_CompsandProcessIDandReconcil) | ire_components |
| 9 | CMDB Identification and Reconciliation landing (c_CMDBIdentifyandReconcile) | ire_landing |
| 10 | Properties for Identification and Reconciliation (properties-id-reconciliation) — full IRE property list | ire_properties |
| 11 | Reconciliation rules (r_ReconciliationRulesPrinciples) — static/dynamic/precedence/domain | reconciliation_rules_principles |
| 12 | Create a CI reconciliation rule (create-reconciliation-rule) | create_reconciliation_rule |
| 13 | Create an IRE data source rule (create-ire-data-source-rule) | create_ire_data_source_rule |
| 14 | Duplicate CIs remediation (de-duplication-tasks) | duplicate_ci_remediation |
| 15 | Properties related to remediation of duplicate CIs (properties-duplicate-ci) | properties_duplicate_ci |
| 16 | CI Class Manager landing (ci-class-manager-landing-page) | ci_class_manager |
| 17 | Create a CI class (t_CreateCIType) | create_ci_class |
| 18 | ITOM Configuration Console (itom-conf-console) | itom_config_console |
| 19 | Credential affinity (c_CredentialAffinity) | credential_affinity |
| 20 | Credential aliases for Discovery (credential-alias) | credential-alias — not fetched (referenced by 19) |
| 21 | Exploring MID Server (explore-mid-server) | mid_server_exploring |
| 22 | MID Server landing (mid-server-landing) | mid_server_landing |
| 23 | MID Server Workspace — referenced, not fetched; use `Configuration > Mid Servers` | — |
| 24 | Discovery Home page (discovery-home-page) | discovery_home_page |
| 25 | Discovery Admin Workspace — referenced via sn_disco_workspace.* properties (§10.7) | — |
| 26 | MID Server properties (r_MIDServerProperties) — §10.10 | mid_server_properties |
| 27 | Create a new discovery schedule form reference (create-a-new-discovery-schedule-form) — Cloud form; IP schedule fields analogous | discovery_schedule_form |
| 28 | Discovery landings/legal: docs "Summarize" banners (OpenAI) appear on pages 5,7,8,11 etc. — content is ServiceNow's official docs; summaries are AI-generated aids inside the page and are not used here | — |

## 17. Gaps & UNVERIFIED
1. Exact column spelling for static reconciliation rules table: docs print `cmdbreconciliationdefinition` — expected real table `cmdb_reconciliation_definition`; **verify with `.list`** before scripting.
2. `glide.discovery.schedule_ipv6_limit` default 20,000 is documented for current releases; note docs flag ≤5,000 cap pre-ZP3/YP9.
3. MID install steps/OS matrix: not fetched (host prep is platform-specific). Follow NowSupport MID docs for your OS.
4. Dynamic IRE production behavior (default off) — documented, not exercised.
5. Australia vs Yokohama/Zurich diffs — not performed; property names stable, defaults may drift.
6. KB refs (KB0750382/83/86, KB0756709, KB1542272) need Now Support access — not opened.
7. CMDB Health rule syntax and certification template JSON — not fetched; pages are under `CMDB Health` nav.
8. "Order of operations": docs give no single canonical page; §2/§14 are reconstructed from pages 1,2,4,5,6,18,24 — marked as synthesis.
