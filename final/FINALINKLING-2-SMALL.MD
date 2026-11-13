# ServiceNow Discovery — FINAL merged reference (all agents' findings, merged)

**Author agent:** `inkling-2-small__openrouter__kilo` — model `openrouter/thinkingmachines/inkling-2-small:free` · provider **OpenRouter** (free tier) · harness **Kilo CLI**, worktree `SNC_DISC__WT1`
**Date:** 2026-11-13 · **RELEASE:** validated against ServiceNow **Australia** (fetched live 2026-11-13) with **Brazil** cross-checks (deepseek-flash 2026-11-13, docs dated 2026-09/11-2026) — both release labels appear with each item.
**Scope:** horizontal (IP-scan) Discovery — MID Server → scan → classify → identify → explore → CMDB write. Cloud/ACC/Service Mapping/OT only where they intersect the same mechanisms.
**Method:** read every fleet artifact on `main` (agent folders, `results/`, KBs cited by agents, community threads cited by agents) + my own live-fetched Australia docs corpus (`agents/inkling-2-small__openrouter__kilo/SNC_DISC__WT1/research/raw/`, raw HTML + stripped text) + Australia end-to-end guide (`research/servicenow-discovery/`). Duplicates were resolved by re-validation; see §20 "Merge log & conflicts resolved" — every merged item names which source won and why.
**Rule used:** when two agents disagreed, the claim that is (a) in ServiceNow's own docs, current-release, and (b) internally consistent wins. Community folklore is marked CONFIRM-ON-INSTANCE. Nothing here is instance-verified; dry-run before prod.

---

## 1. The mental model

Two pipelines meet at the CMDB:
```
Device → Shazzam (scan) → Classify probe → Identification → Exploration (probes|patterns) → CMDB (IRE)
```
Two different "identifier" concepts are **not** the same object: probe-based Discovery identifiers (legacy) vs CMDB/IRE **Identification Rules**. Modern Discovery (Geneva+ / Brazil / Australia) defaults to IRE everywhere (`glide.discovery.use_cmdb_identifiers=true`); Service Mapping forces IRE identifiers regardless of that property. `use_cmdb_identifiers` default **true** both label sets [A][B].

Duplicate prevention is **four separate controls plus repair**, tuned as one system:
**Identification Rule** (match the right CI) · **IRE Data Source Rule** (may this source create a CI of this class at all) · **Reconciliation Rule + Data Refresh Rule** (update authority and staleness) · **de-duplication tasks** (repair). Tuning one layer alone produces duplicates or silent overwrites [A].

## 2. Runtime phases (what actually happens per device)

| # | phase | what runs | Discovery Status device state you may see |
|---|---|---|---|
| 1 | Scanning | **Shazzam** + port probes via ECC queue; **first phase with NO credentials** | `Alive, not active, not classified` → `Active` |
| 2 | Classification | **one classify probe per device**; first phase using **credentials**; determines CI class | `Classified` / `Active, couldn't classify` |
| 3 | Identification | identity probe or pattern identifier ops; **IRE decides insert vs update**; only for Discover=`Configuration items` | `Identified CI` · new CI · `Identified, ignored extra IP` (same run, 2nd IP) |
| 4 | Exploration | exploration probes/patterns from classifier's Triggers Probes list; sensors enrich CI | `Updated CI` |

Patterns replace probes/sensors wholesale: the **Horizontal Pattern probe** runs pattern operations for **both identification and exploration** — the identity probe is not used [A][B].

**Critical:** `Discover = IP addresses` (credential-less scan) creates **device history only — never writes CIs**, so can never cause a duplicate CI [A][B].

The ECC queue carries everything both directions; every phase "fails forward" or stops — a device that never reaches `Identified CI` usually died at step 2 or 3 (check credentials / IRE logs), not at step 1 [A][B].

## 3. Zero → production: canonical order of operations

| # | step | exit check |
|---|---|---|
| 0 | Subscription/plugin; `discovery_admin` role | role present; plugin active [A] |
| 1 | Install **≥2 MID Servers**, assign **Discovery or ALL** application | `Discovery > MID Servers` status Up/Validated [A] |
| 2 | Configure + **test** credentials (WMI/SSH/SNMP/PowerShell/HTTP) | credential test per protocol/class passes [A][C] |
| 3 | IP ranges / range sets / exclusions (incl. global exclusions; CIDRs auto-exclude network+broadcast addrs) | ranges resolve; excluded nets absent [A] |
| 4 | Review classifiers/patterns/behaviors for expected classes | test device classifies as expected [A] |
| 5 | **Design CI class + identification rule BEFORE broad scans** — one weak name-only identifier + 10,000 devices = duplicate flood | rules designed and simulated [A][C] |
| 6 | Create schedule (Discover=**Configuration items**) | `Discover now` succeeds [A][C] |
| 7 | Run narrow pilot; read Status / Log / Home tiles / Identification Logs | expected CIs created/updated; zero credential errors [A][C] |
| 8 | Widen ranges only after pilot clean; then **tune reconciliation + data source rules** (deliberately last — you can't judge source authority blind) | Identification Simulation passes; duplicate metric stable [C] |
| 9 | CMDB governance steady-state (Health KPIs, de-dup, Data Manager) | Health/duplicate KPIs trending right [A] |

Key point all sources agree on: **credentials before schedule, ranges before schedule, MID validated before schedule, rules before scale, governance last.**

## 4. MID Server — selection, scaling, ports

- MID polls the instance; no inbound firewall rules needed. Two+ MIDs: split schedules/ranges. MID cluster = same list order; a MID can belong to **one** cluster only. [A][C]
- **Auto-Select sequence:** (1) MID with Discovery app + matching IP range → (2) MID with ALL app + matching range → (3) first `Up` (random among Up) → (4) default MID for Discovery, then ALL → (5) `Paused`/`Upgrading` candidates. **Not supported for IPv6.** [A][C]
- Cluster selection prefers the **lowest `Order` that is `Up`**, ignores default-MID settings, and can distribute `Shazzam` batches (`Shazzam cluster support`) — works together with batch size, and batches run sequentially per MID. [C]
- Credentials: Windows/WMI come from the **MID Server service login** (≥ local admin on targets); UNIX/SSH/SNMP are instance-stored; Discovery tries credentials until one works, then pins an **affinity** in `dscy_credentials_affinity` per device (change creds → re-try cycle; credential aliases + multiple affinities → lowest order wins). [A][C][my fetch]
- Ports: WMI **135** + **dynamic high ports** (logical firewalls often allow 135 but block the RPCs — classic cause of Windows ID/explore failure); SSH 22; SNMP 161/udp; HTTP 80/443 (low priority classification only). [A][v4-flash]
- Multi-domain / ACL-restricted SNMP / dual-protocol devices / load balancing → **Discovery behaviors** (functionality definitions = protocol lists → phase numbers run numerically; criteria `mid_server`/`win_domain`/`mid_win_domain` for Windows domain splits). Auto-Select is not multi-domain. [A][v4-flash]
- Auto-select when selecting a specific MID auto-adds the Discovery application. [C]

## 5. IP ranges, range sets, exclusions

- Definitions combinable: IP list (incl. hostnames), range, CIDR network — **IPv6 cannot be range/CIDR; IPv6 only via address lists**, and IPv6 auto-select unsupported. Quick ranges accept comma strings for pilots. [C]
- CIDR auto-excludes network/broadcast addresses. [C]
- **>500,000 excluded addresses cancels the discovery** and logs an error. Split scope as include-sets instead. [C]
- Excludes are per range-set; **global** excludes apply across all CI/IP/network scans. [A][C]
- `glide.discovery.discoverable.network.max.netmask.bits` default **28** (regular networks with ≤8 addresses not discovered; 1–32 valid; irregular always discovered) [my fetch Australia]; `glide.discovery.exclude_ip_sync_classes` default `cmdb_ci_lb` (LB mgmt IP stays, NIC substitution skipped per comma list) [A][B][C][my fetch]; `glide.discovery.retire_stale_accounts=false`; IPAM auto-generated schedules `glide.discovery.schedule_ipv4_limit=65536` / `schedule_ipv6_limit=20000` (≤5000 pre-ZP3/YP9) [my fetch].
- Credential-less subnets: IP-address schedules or **credientialless Nmap** (Advanced Discovery configuration) — note zero CMDB impact. [verified my fetch pointer; details not fetched]

## 6. Discovery schedule — the control surface

`Discovery > Discovery Definition > Schedules` (classic) — Discovery Admin Workspace also exposes schedule UX; table `discovery_schedule`. Fields that change behaviour:

| field | options | why it matters |
|---|---|---|
| **Discover** | Configuration items / IP addresses / Networks / Service / Serverless / Cloud application / Cloud resources / Certificates | **Only `Configuration items` runs identification and writes CIs.** IP-address scans create device history only [C] |
| **MID Server selection method** | Auto-Select / Specific MID Cluster / Specific MID Server / Use Behavior | see §4 [A][C] |
| **Behavior** | preconfigured behavior | multi-MID/domain/protocol scans [A][C] |
| **Max run time** | duration | hard stop; remaining tasks cancel [A][C] |
| **Max Idle time** | duration | cancels stalled runs; **hidden column** — add to `discovery_schedule` view [C] |
| **Shazzam batch size** | int, default **1000** | min 256 (UI policy → anything lower becomes 0); batches route sequential classify; pick with cluster support [C] |
| **Shazzam cluster support** | bool | distributes batches across cluster MIDs [C] |
| **Use SNMP Version** | ALL (default) / v1 / v2c / v3 | pin when gear mishandles v3 [C] |
| **Active** | bool | manual runs allowed when inactive [C] |
| **Log state changes** | bool | per-state logs; noisy in steady state [C] |
| **Run** | On Demand/Daily/Weekly/Monthly/Once/etc./**After Discovery** | run-after chains; `Even if canceled` decouples chain [A] |
| **Location** | location ref | sticky CI location [C] |
| **Quick ranges** | comma inline | pilots [C] |
| related lists | IP Ranges · Range Sets · Discovery Status · Global IP Exclusion · Discovery Attributes (per-range CI field values e.g. `location`) [C] | |

**Concurrency guard:** `glide.discovery.max_concurrent_invocations_per_schedule` default **3**; 0/neg disables. Does not apply to `After Discovery` chains with `Even if canceled` [A][B][C][my fetch].

`glide.discovery.schedule_monitoring.{stale_check_seconds=1200, dry_run=false, schedule_types_to_monitor=CIs}` shapes stale-run detection; `sn_disco_workspace.discovery_schedule_anomaly_*` (ML-based default, 20% error/CI/runtime anomaly thresholds, `CIs, Cloud Resources` types, sensitivity low) drive Discovery Admin Workspace anomaly detection [my fetch].

## 7. Classifiers & patterns

Three classification types [A][B][C]:
| type | what it classifies | notes |
|---|---|---|
| **Device** | OS/net gear types; first credentialed phase; Madrid+ HTTP fallback last (only when Shazzam saw 80/443 open AND WMI/SSH/SNMP failed) | one classification probe per device |
| **Process** | apps via running processes; during exploration; creates child CIs (`Runs on::Runs on`); **process handlers strip volatile params** so same app doesn't dup; process-classifier conditions are case-sensitive | check handlers before blaming IRE |
| **IP scan** | credential-less banner typing | no CI write |

Classifier criteria = `parameter operator value` (case-sensitive for processes). Classifier specifies **Triggers Probes** (related list). Pattern alternative: **Horizontal Pattern probe** — pattern ops cover identification+exploration; classifier criteria select the pattern [A][B][C]. Debug: `glide.discovery.debug.classification=true` then review criteria names/values [A][B][C].

**File-Based Discovery (FBD)** is a Discovery feature (not an IRE mechanism): runs in exploration, records software found on disk. Tables: `cmdb_file_information`, `samp_file_name` (vendor allow-list), `samp_custom_file_name`, `cmdb_sam_sw_install`, `cmdb_unidentified_file_set`, `cmdb_swid_tag`; properties `glide.discovery.file_discovery.wildcard.windows` / `.blacklist.windows`; plugin `com.snc.discovery.file_based_discovery`; default frequency **Monthly**; does not run before the ~24h Content Data Service sync [B].

## 8. Discovery properties — full catalog (the ones that change CMDB outcomes)

Set at `Discovery Definition > Properties` (Brazil/Australia labels; learning-guide path `All > Discovery > Properties` / `discovery_private_properties.list` — same object). `sys_properties.list` for the rest. Both releases ship the same names; defaults noted where one changed. ✓ = direct duplicate/CMDB-write relevance.

### 8.1 IP / network / scanning
| property | default | effect |
|---|---|---|
| ✓ `glide.discovery.exclude_ip_sync_classes` | `cmdb_ci_lb` | classes whose IPs stay as-discovered / not NIC-substituted (extensible, e.g. `cmdb_ci_lb` or other LB classes) |
| ✓ `glide.discovery.enforce_unique_ips` | `false` | clears IP on every other CI sharing it after a valid discovery per device + class — **not an identification/duplicate control**; it's an IP-level cross-CI conflict guard. May erase NAT/shared IP and VIP data — enable only if IP uniqueness is a hard invariant |
| ✓ `glide.discovery.enable_mac_address_verification` | `false` | stops processing an IP when device moved (MAC mismatch at discovery time); good for DHCP fleets |
| `glide.discovery.bgp_router_disable` | `true` | skip SNMP-routing probe on BGP routers (large tables, MID OOM risk); set false only for small edge nets |
| `glide.discovery.debug.network_discovery` | `true` (Australia) | extensive NetDisc logging |
| `glide.discovery.discoverable.network.max.netmask.bits` | `28` | regular-network size floor — /28+ skipped; irregular always discovered; 1–32 valid |
| `glide.discovery.network_owner_method` | `Most Networks` | router↔network association (First/Last/Most/Least Networks) |
| `glide.discovery.physical_interface_types` | `6,117,9,71,209` | MIB-2 ifTypes considered physical |
| `glide.discovery.switch_interface_types` | `7,8,9,26,53,62,69,71,78,115,117,209` | others→router if routed |
| `glide.discovery.virtual_interface_types` | `53` | virtual interfaces |
| `glide.discovery.L3_mapping` | `true` | map servers→L3 routers/L3 switches; feeds `Dscy_route_next_hop` — required for router population |
| `glide.discovery.network_discovery.functionality` | `SNMP only` | don't change absent Support direction |
| `glide.discovery.allow_loopback_adapters` | `false` | loopbacks as NICs |
| `glide.discovery.sensors.fire_ssh_probe` | `true` | SSH when LB/VIP absent from SNMP |
| `glide.discovery.sensors.netapp_native_{7mode,cluster_mode}` | (unset) | native NetApp discovery instead of SMI-S |
| `glide.discovery.sensors.save_attachments` | `true` | keep ECC attachments post-processing (set false steady-state) |
| `glide.discovery.mark_esx_servers_as_absent` | `false` | absent not retire |
| `glide.discovery.shazzam_simplify_ranges` | `true` | dedup overlapping ranges (single-behavior schedules only; multiple behaviors keep dupes) |
| `glide.discovery.shazzam_ranges_json` | `true` | JSON-encode ranges |
| `glide.discovery.schedule_ipv4_limit` / `.schedule_ipv6_limit` | `65,536` / `20,000` (≤5,000 ≤ZP3/YP9) | IPAM autogen caps |
| `glide.discovery.max_concurrent_invocations_per_schedule` | `3` | per-schedule concurrency |
| `glide.discovery.retire_stale_accounts` | `false` | stale cloud service refs cleanup |
| `glide.discovery.ip_service_affinity` | `false`; new-customer **`true`** (Brazil/Australia) | remember last good protocol/port per IP; required for multi-SSH-port setups |
| `glide.discovery.ip_based.active` | `true` (probe→pattern migrations) | full-cycle per same-device IPs in one schedule |

### 8.2 Identity / hostname / verification
| property | default (Brazil / Australia) | notes |
|---|---|---|
| ✓ `glide.discovery.use_cmdb_identifiers` | `true` | Geneva+; pre-Geneva upgrades may need manual add; Service Mapping forces IRE regardless |
| `glide.discovery.hostname.always_update` | `true` | latest **value from a trusted source** wins on probe-based Discovery; can overwrite hand-entered names (set false to stop that) |
| `glide.discovery.hostname.case` | `Lower case` (also Upper/No change) | NETBIOS-ish normalization |
| `glide.discovery.hostname.include_domain` | `false` | FQDN in name |
| `glide.discovery.hostname.dns_nbt_trusted` | `true` | trust DNS/NBT name (don't for Linux/AIX/Solaris patterns) |
| `glide.discovery.hostname.snmp_trusted` | `false` → **new-customer true** | trust SNMP name |
| `glide.discovery.hostname.ssh_trusted` | `false` → **new-customer true** | trust SSH name |
| `glide.discovery.hostname.wmi_trusted` | `false` → **new-customer true** | trust WMI name |
| `glide.discovery.domain.name.nbt` | `true` | Windows domain from NBT (else WMI) |
| `glide.discovery.fqdn.regex` | `^([^.]+)\.((?:[^.]+\.)+[^.]+)$` | 2-group regex (host, domain) |
| `glide.discovery.source_name` | `ServiceNow` | written to `discovery_source`/`sys_object_source` — change only for coexistence/migration |
| ✓ `glide.discovery.debug.ci_identification` | `false` | CI Identification Log verbose feed |
| `glide.discovery.log_debug` | `false` | verbose Discovery logging |
| `glide.discovery.log_message_length` | `200` | log msg truncation (0 disables) |
| `glide.discovery.log_debug_info` | `false` | ECC input debug → Discovery log *(name drift across releases — see `log_message_chars` note in §19)* |
| `glide.discovery.warn_minor_version` | `false` | minor_version mismatch warnings |

### 8.3 Scheduling / sensors / throughput / perf
| property | default | notes |
|---|---|---|
| `glide.discovery.max_concurrent_invocations_per_schedule` | `3` | §5/6 concurrency |
| `glide.discovery.schedule_monitoring.{stale_check_seconds=1200, dry_run=false, schedule_types_to_monitor=CIs}` | stale-run monitor | |
| `glide.discovery.schedule.autogenerate.{group,debug}` | `""`/`false` | IPAM-gen grouping + logging |
| `glide.discovery.save_pattern_log` | `true` | pattern log persistence (failures always saved) |
| `glide.discovery.use_probe_results_cache` | `false` | skip sensor if results unchanged |
| `glide.discovery.active_processes_filter` | `false` | perf filter for ADM |
| `glide.discovery.perf.metrics.enable_collection` / `.rollup_by_{build,status,target}` | `true` / all `true` | perf metrics |
| `glide.discovery.count.use_optimized_counter` | `true` | optimized discovery_status counters |
| `glide.discovery.roundingInterval.{cpu,ram}` | `1` MHz / `1` MB | rounding |
| `discovery.use.event.processing` | `false` | Event Framework for sensors (scale) |
| `discovery.event.{separate.cloud.events=true, pin.jobs=false}` | queue split; random-assign default | |
| `com.glide.queue.discovery.sensors.processing_jobs.priority` | `100` | lower = sooner |
| `com.glide.queue.discovery.cloud.sensors.processing_jobs.priority` | `100` | cloud equivalent |
| `glide.discovery.multi_page_serial_mode` | `false` | **`true` = process multi-page pattern payloads serially — documented fix for duplicates from parallel pattern payloads** |
| `glide.discovery.sam_batch_update_size` | `100` | batches `cmdb_sam_sw_install` updates where only last_scanned changed |
| `glide.discovery.naming…` n/a — do not invent; see §19 unverified | | |

### 8.4 Software discovery / ADME / ADM
| property | default | notes |
|---|---|---|
| `glide.discovery.discover_software` | `true` | software package discovery |
| `glide.discovery.populate_software_instance_table` | `false` | pre-Jakarta SAM only |
| `glide.discovery.software_sccm_managed` | `false` | true = Discovery won't write software for SCCM-managed computers |
| `glide.discovery.software_filter_keys` | `Language Pack, Hotfix Security Update` | filter list |
| `glide.discovery.enable.software_filter` / `.enable.software_simplify` / `.enable.software_simplify_sccm` | `true` / `true` / `false` | filtering + name/version cleanup (disable simplify → dup software rows) |
| `glide.discovery.application_mapping` / `.enable_adme` | `true` / `false` | ADME (enhanced ADM probe) |
| `glide.discovery.adme.{sampling_interval=120, aggregation_interval=3600, rolling_window_size=24, max_total_samples=100, base_dir_unix=false}` | s | |
| `glide.discovery.adm.update.applications` | `true` (Tokyo+) | pattern-found app CIs auto absent→installed on churn |
| `glide.discovery.enable_file_tracking` / `.file_tracking.{max_files_per_ci=50, max_file_size=500000, change_limit_count=4, change_limit_days=7}` | | pattern file tracking; **note: some Brazil/community sources conflate `max_files_per_ci` (50) with `change_limit_count` (4) — Australia docs say 50/4 respectively, use these** |
| `glide.discovery.enable_ssm` + `.ssm.enable_windows` | `false`+`false` | AWS SSM discovery (+SQL variants elsewhere) |
| `glide.discovery.discover_aws_ec2_host_metadata` / `.discover_azure_host_metadata` | both `true` | cloud-run in IP discovery |
| `glide.eccprobe.awsrestprobe.{max_retries=4, max_wait=30}` | cloud backoff |

### 8.5 Certificates / firewall / workspace
| property | default | notes |
|---|---|---|
| `glide.discovery.certs.{cert_admin_user_id=Certificate Administrator, days_before_expiration_to_create_renewal_task=60, enable_incident_creation_for_expired_certificates=false, enable_renewal_task_creation_for_discovered_certificates=true, slack_channel_id=""}` | | cert inventory |
| `sn_disco_certmgmt.{enable_csr_generation=false, private_key_size=2048}` | | CSR/PKCS12 |
| `sn_disco_firewall.default.rule.task.{policy.owner.group="Task Owner Group Name", approval.group="Approval Group Name"}` | | firewall tasks |
| `sn_disco_workspace.discovery_schedule_anomaly_detection_{disabled=false, method=ML-based, discover_type="CIs, Cloud Resources", ml_model_sensitivity=low}` | | ML anomaly detection |
| `sn_disco_workspace.discovery_schedule_{cis_discovered,error,runtime}_anomaly_threshold` | `20` each | % drop/error/runtime anomaly trigger |
| `sn_disco_workspace.{discovery_stats_time_scale=7, enable_auto_create_schedules=false, enable_error_framework=true, visibility_diagnostic_utility.enabled=false}` | | workspace UX |
| `glide.eccprobe.max_queued_probes_per_run` | `20` | node agent pick-up |
| `glide.eccprobe.node_agent_id` | `NODE_AGENT` | mid-run affinity prefix |
| `glide.ecc_agent.validated.override` | `false` | force-valid MID treated |
| `com.snc.use_external_credentials` | `true` | external cred storage |
| `com.glide.codesigning.tracking.unsupported_script_tracking.enabled` | `true` | code-signed instances + cloud discovery |

### 8.6 MID Server properties (config.xml / MID Server Properties)
| property | note |
|---|---|
| `mid.shazzam.threads` · `mid.shazzam.max_scanners_per_thread` · `mid.shazzam.regulator.{interval_ms, packets_per_interval}` | scan throttling |
| `mid.eccq.max_payload_size` · `mid.discovery.max_payload_size` · `mid.discovery.max_total_items_size_per_page` · `mid.discovery.max_related_count_per_page` · `mid.discovery.max_relation_count_per_page` | payload caps |
| `mid.discovery.multiprobe.skip_others_on_error` | multiprobe fail-fast |
| `mid.discovery.{should_minify_pattern_payload}` | payload shrink |
| `mid.discovery.aws_ssm.*` | SSM bucket/kms |
| `mid.probe.{collect_debug_info, use_legacy_reverse_dns, use_legacy_forward_dns}` | probes |
| `mid.snmp.use_getbulk` · `mid.sa.prefer_powershell` · `mid.sa.windows.allowable_failures` | transport/SA |
| `mid.ssh.algorithms.{kex,cipher,mac,host_key}` | SSH algo pinning |
| `mid.property.{ssh.use_snc, jms.command.allowed_factory_names, powershell.use_base64_password, jdbc_operations}` | protocol policy |
| `mid.powershell.target_base_dir` | `admin$\temp` |
| `mid.keystore.{max_backups, max_live_backups, backup_overwrite_timespan}` · `mid.jdbc.datastream.max.record.size` · `mid.log.command_audit.enable` · `mid.use_net_tools` · `mid.servicewatch.*` · `mid.process_flow.log_listener.max_size` · `mid.http_classy.allow_credentials_over_http` | misc |
## 9. IRE — pipeline, rules, and the four rule families

### 9.1 Pipeline (per payload item)
```
payload item
 ├─ fast path: source_name + source_native_key in sys_object_source_info  → update (no rules consulted)
 │      (forced off by glide.identification_engine.skip_sys_object_source_matching=true → always rules)
 └─ identification rule matching (criterion attributes / regular|lookup|hybrid entries)
        match  → reconciliation (update only)  → CMDB write (+ last_discovered / discovery_source stamp)
        no match → IRE Data Source Rule gate → INSERT (or INSERT_NOT_ALLOWED_FOR_SOURCE)
```
- Inclusion rule runs **after** identification matching to decide which matched CI is eligible.
- **Reconciliation and data refresh never apply to inserts.** IRE Data Source Rules never apply to updates (or to lookup/related items).
- `sys_object_source_info` requires both `source_name` AND `source_native_key` from the payload item; native keys not used on lookup items.
- Insert blocked → `INSERT_NOT_ALLOWED_FOR_SOURCE`; under `CreateOrUpdateCIEnhanced()` item parks as a partial payload (later merge allowed); under plain `createOrUpdateCI()` **whole payload fails**.
- Dynamic IRE / dynamic reconciliation in effect ⇒ IRE data source rules and data refresh rules have **no impact** (except classes excluded from Dynamic IRE — see below).
- Identification/reconciliation applies only to **Configuration items** discovery, not IP-address scans [A][B].

APIs: `CreateOrUpdateCIEnhanced()` (partial payloads + partial commits + deduplicate payloads + optional summaries; defaults ON: partial_payloads, partial_commits, deduplicate_payloads; generate_summary OFF) vs `createOrUpdateCI()` (no partial commits). `identifyCI`/`identifyCIEnhanced()` = dry-run, no commit. Plain REST/scriptable IRE APIs for import sets & integrations (route through `IdentificationEngineScriptableApi`/`CMDBTransformUtil` so IRE runs).

Perf guardrails (docs): ≤ **500 CIs per payload**; no system fields; unique criterion attributes only; serialize parent-dependent inserts; use `sys_id` when available; `partial_payload_items_max_size=1000` (splits on excess); `partial_items_process_limit=2000` / `.process_absolute_limit=5000`; partial payloads ≤ **90 days** retention; granular insert locks default on (`glide.identification_engine.granular_insert_locking=true`); caches `related_items_local_cache_count=15000 · dependent_items_local_cache_count=10000 · independent_items_local_cache_count=100000` (0 disables); `service_cache=20MB`; `batch_update_last_discovered=true` (+`.use_execute_lazy=true`); `skip_updating_source_last_discovered_if_older=true`; `.skip_updating_last_scan_if_older=true`; message-listener `*last_scan_to_now=false` flags.

Reclassification (IRE moves CI class): allowed by default (`glide.class.{upgrade,downgrade,switch}.enabled=true`); `glide.identification_engine.update_without_{upgrade,downgrade,switch}_enabled=false` each **override** the class-flag at finer scope; payload `settings` flags `updateWithoutUpgrade|Downgrade|Switch` take precedence over properties; `glide.identification_engine.reclassification_restriction_rules_enabled=true` keeps restriction rules active; blocked ⇒ reclassification task (review in CMDB Workspace).

Identification canon [A][B][C][matrix]:
- Independent rules preferred. Dependent rules identify parents first (**max 2 dependency levels**) — required before any CI can be Dependent-typed (child class's dependent identification rule must exist first).
- Regular (CI table) > Lookup (`cmdb_ci_network_adapter`, `cmdb_serial_number`) > Hybrid entries; each with own priority; each entry must be unique-ish; **avoid lookup entries for performance; add `Enforce exact count match` on lookup entries when unavoidable**.
- `sys_class_name` **cannot** be an entry for independent rules.
- **Inheritance:** child derives parent's rule (incl. related entries); defining a child rule REPLACES the derived rule entirely — re-add related entries.
- **One rule per class** (descendants derive). Order low→high; defaults use 100/200; custom rules must use **different Order values**; deactivate rules (Active=false) instead of deleting.
- **Inclusion rules** (`create-id-inclusion-rule`) narrow matched-CI eligibility — class-level `Active record condition`; **no predefined baseline**; impacts every IRE caller; never scope inclusion rules by `Class` on `cmdb_ci_hardware` (children then invisible to IRE → duplicates — see §12 pitfalls).
- Domain-separated rules apply to child domains unless overridden. `glide.identification_engine.platform_domain_separation_enabled=false` default.

Default base-system rules (all label sets agree):
| rule | class | attributes |
|---|---|---|
| Hardware | `cmdb_ci_hardware` | `serial_number`, `serial_number_type`, `name`, `ip_address`, `mac_address` + lookup tables Serial Number & Network Adapter |
| ESX Server | `cmdb_ci_esx_server` | `correlation_id` |
| Storage Server | `cmdb_ci_storage_server` | `cim_object_path`, `name`, serial fields, `mac_address`, `ip_address` + lookups |
| WBEM Service | `cmdb_ci_wbem_service` | `cim_object_path` |

### 9.2 THE FOUR RULE FAMILIES — canonical reference

| family | table | scope | INSERT | UPDATE |
|---|---|---|---|---|
| **Identification Rule** | `cmdb_identifier` (+`cmdb_identifier_entry`) | per class (derived; override child) | **yes** — no match ⇒ create | **yes** — match ⇒ update |
| **IRE Data Source Rule** | `cmdb_ire_data_source_rule` | per class × source (one active per pair; child overrides parent) | **yes — blocks insert** ("Insert Not Allowed") | **no** (updates allowed) |
| **Reconciliation Rule** | `cmdb_reconciliation_definition` (static) / `cmdb_dynamic_reconciliation_definition` (dynamic) | class × source × attribute (or all-attributes); filter-condition optional | **no** | **yes** |
| **Data Refresh Rule** | same Reconciliation surface (counts `Effective Duration`/`Refreshable` — release-dependant UI wording) or `cmdb_datasource_staleness` for non-CMDB | class × source | **no** | **yes — stale ⇒ lower-priority source allowed** |

Fields per rule:
- **Static reconciliation:** Active · Discovery source · Priority (lower# wins) · Apply to ALL attributes vs explicit `Attributes` list · `Update with Null` · `Filter Condition`.
- **Dynamic reconciliation:** CMDB 360 value-based (largest/most reported), one dynamic rule per class+attribute.
- **Data source rule:** Active · Applies to (class) · Data source · Insert Not Allowed.
- **Data refresh:** Discovery source · **Effective Duration** (staleness window; **0 = always stale**) · Active.
- **Identification inclusion:** Active record condition · class-level.

Non-negotiable behaviors:
1. **Reconciliation never blocks an insert.** Insert only sees identification + IRE data source rules.
2. **IRE data source rule never blocks an update.** Only identification/reconciliation touch updates.
3. **Data refresh only for static reconciliation** — no effect when a dynamic rule is in effect.
4. **Dynamic rules beat static** at the same class+attribute level.
5. **Specific-attribute rule beats all-attributes rule — regardless of priority number.**
6. **Child-class rule beats parent** (attr-specific across mixed static/dynamic).
7. Overlapping static rules (two sources, same attribute) coexist — IRE enforces via Data Source History (`cmdb_datasource_last_update`).
8. `glide.reconciliation.override.null=true` (default) — lower-priority source may fill an *empty* field.
9. Lower-priority may **never** null a populated field unless `Update with Null` lists it.
10. Rules cannot target system/IRE-specific fields (`discovery_source`…) and **cannot be dot-walked**.
11. Dynamic IRE can be turned on globally (`glide.identification_engine.dynamic_ire.enabled=false` default); classes to exempt live in `cmdb_dynamic_ire_skip_class` (takes class+descendants back to Static IRE — Brazil docs; verify on instance).
12. Domain separation scopes rules per domain.
13. Identification decides **first**; reconciliation only runs on matched CIs.

**Worked permutation examples** (the full 39-perm matrix is committed in-repo at `results/20261113T090000Z__deepseek-v4-pro__deepseek__kilocode/IRE_RULE_APPLICABILITY_MATRIX.md`; condensed):
- match + no rule for that attribute → field skipped (no error).
- match + class move blocked → reclassification task instead of write.
- no match + DSR blocks ⇒ no CI, parked partial. ↳ **the only way to stop a duplicate being born**.
- matched + non-stale + lower-priority ⇒ rejected; matched + stale ⇒ writes only stale fields (still needs a recon rule authorizing that attribute).
- stale + Specific-attribute higher-priority ≈ still wins over all-attributes lower-priority even when stale.
- Dynamic rule on class + DSR blocked ⇒ DSR ignored (dynamic wins).
## 10. Data Source History & Data Refresh — the "staleness" triangulation

Three different "stale" mechanisms keep getting confused. Use this table:

| mechanism | question | where | effect |
|---|---|---|---|
| **Data Refresh rule** | has *this source* stopped refreshing this CI? (measured against Data Source History `cmdb_datasource_last_update`, not `sys_updated_on`) | CI Class Manager → class → Reconciliation Rules → Data Refresh Rules | lets lower-priority authorized sources update the classed CIs (static reconciliation only) |
| **CMDB Health staleness rule** | what % of this class is stale (correctness KPI)? | CI Class Manager → Health → Correctness | **reporting only**; Discovery refreshing-but-unchanged keeps `sys_updated_on` frozen, so health can misreport |
| **CMDB Data Manager policy** | should this CI retire/archive/delete? | CMDB Workspace → Data Manager | lifecycle action on the CI |

Data refresh semantics: refresh rules apply to **static reconciliation rules' attributes**; `Effective Duration = 0` means the CI is immediately stale for that source; refresh is not a license — the lower-priority source still needs its own reconciliation authorization on that attribute; no effect under Dynamic IRE. **Do not confuse with staleness KPI or Data Manager.**

Insert-vs-update cheat table (complete merge):

| situation | outcome | decided by |
|---|---|---|
| exactly one CI matches (inclusion rule eligible) | **update** attribute-by-attribute | reconciliation rules |
| no match + DSR permits | **insert** (reconciliation NOT consulted) | IRE + data source rule |
| no match + DSR blocks | **blocked** → partial payload (Enhanced) or payload fail (plain) | IRE data source rule |
| matched, but match excluded by inclusion rule | **insert → possible duplicate** | identification inclusion rule |
| matched, 2+ CIs, count < threshold, skip_duplicates=true | oldest = main; others `duplicate_of`; de-dup task auto | skip_duplicates [+`.threshold=5`] |
| matched, count ≥ threshold or skip_duplicates=false | **match fails**, error logged; de-dup task | threshold |
| lookup-matched duplicates | oldest referenced CI chosen; set `glide.identification_engine.lookup_match.create_duplicate_task_ci.enabled=true` to force tasks | property |
| matched, no reconciliation rule for source×attr | attribute skipped silently | static/dynamic |
| matched, lower-vs-higher priority non-stale | lower rejected (if first-writer/field-empty, override.null governs) | priority + override.null |
| matched, field empty + lower-priority source | filled (default override.null=true) | override.null |
| matched, class move beneficial + blocked | reclassification task | restriction rules / flags |
| matched + ACL/BR hides CI (read path) | **insert → duplicate** | platform (ACLs, query BRs, domain) |
| scan type anything but `Configuration items` | no CI at all | schedule type |
| Active duplicate_of already set / source=Duplicate | IRE refuses to match ⇒ **insert → duplicate** | KB0869861 troubleshooting |
| concurrent discoveries of same dependent CI | duplicates | schedule sequencing + platform (no schedule overlap) |

## 11. Duplicate CI prevention — the layered playbook

**Root causes (from docs + KBs):**
1. Weak identifier entries (name-only) [v4-flash]
2. Renamed adapters/hostnames → match breaks [A][B][C]
3. Unstable serials / custom serial prefixes [A][B]
4. Multiple sources w/o authority model [A][C]
5. Lookup-table duplication pointing at different CIs [A][B]
6. Over-broad schedules / overlapping behaviors [C]
7. Multi-page payloads processed in parallel [openrouter-free + KB0869861]
8. Inclusion rule **class-scoped on parent** — children invisible to IRE [openrouter-free + KB0869861]
9. ACL/query BR hides existing CI from IRE [v4-flash + KB0869861]
10. `duplicate_of` set or `discovery_source = Duplicate` → IRE skips [KB0869861]
11. Manually created CIs w/ empty source — never reconciled [buffy+KB]
12. Custom identifier Order collides with base rule (or Active cleared) [A][B][C]
13. Reconciliation blocks update → human hand-creates "real" CI [buffy/deepseek-v4-flash]
14. High-priority source silent; attributes "frozen"; re-imports dup [buffy]
15. **Weak identification on child class while parent inherits** [B]

**Controls by layer:**
- **Design:** one independent identifier per class (max 2 dependency levels); strongest entry first; 1 entry ideal; `Enforce exact count match` for lookup entries; **never** define child-table identifier in parent rule AND child rule; **never** `sys_class_name` on independent rule; intervals/Order ≠ defaults; enable `Enable Identifier Optional Condition=true` only after reviewing pre-configured entries [A].
- **Runtime:** `skip_duplicates=true` threshold **5**; `skip_sys_object_source_matching=true` when source keys churn (attributes stable); `multi_page_serial_mode=true` on pattern-heavy estates; `inclusion rule` never class-scoped on `cmdb_ci_hardware`; `enable_mac_address_verification=true` on DHCP; `enforce_unique_ips=true` only as IP-invariant (never first resort); name-含 unique per class [A].
- **Detection:** de-dup tasks (batch via dashboard); **Identification Simulation** before any rule change; CMDB Health duplicate metric (**only** classes w/ identification rules + empty discovery_source or active de-dup task — narrow by design, 0-score ≠ clean) [buffy]; Discovery Status `Scan N of M` + Identification Logs (`glide.discovery.debug.ci_identification`) for bounded windows.
- **Remediation:** pick **main CI** explicitly; merge attributes/relationships/related items; `duplicate_of` reference (no chains; main can't be a dup); bulk = templates (not retroactive) + dashboard; single = Remediator; roles `itil` read, `itil_admin`/`cmdb_dedup_admin` write; properties `glide.duplicate_ci_remediator.{dry_run=false[-set TRUE first], max.cis=1000(≤5000), max.field_length=4000, related_items_blacklist=cert_task.cmdb_ci,cert_audit_result.configuration_item,discovery_log.cmdb_ci,alm_hardware.ci,alm_asset.ci,fm_expense_line.ci, merge_related_items_enhanced=true, enable_restricted_mode=false}`.

## 12. KB-derived operational pitfalls (from openrouter-free + KB0869861 + v4-pro)
- Identification rule entries not matching pattern output → silently no match → inserts.
- Inclusion rule with `Class` parent condition ⇒ child CIs invisible ⇒ new CI each run.
- IRE skips `duplicate_of`-populated CIs → old dupes keep accruing → run Remediator first.
- Same UID + different parent container = different dependent CI (by design — identifier on UID + relationship).
- `glide.discovery.ire_err_exclusion_list` default `ABANDONED, INSERT_FAILED, UPDATE_FAILED, NO_IDENTIFIER_KEYS_GENERATED` — **NO_IDENTIFIER_KEYS_GENERATED masks silent create failures**; temporarily remove while troubleshooting missing aimed CIs [v4-flash].
- Retired/rediscovered CIs are **not** auto-flipped back to Operational — `install_status` not in OOTB payload; to auto-reactivate needs custom BR on `cmdb_ci` ("Most recent discovery changes" + "Operational Status is Retired" → before update set Operational) [openrouter-free + v4-pro + KB0755747].
- Duplicate metric narrowness (see §11 detection) means dashboards can read 0 with thousands of dupes.
- De-dup templates: **not retroactive**; template class-condition filter evaluates at **CI level**, not task level; roles `itil`/`cmdb_dedup_admin` [v4-flash].
## 13. CI Class Manager — breadcrumbs & workflow

Everything CMDB-write lives behind **`All > Configuration > CI Class Manager`** [A][B][C][particle-1]. Roles: `sn_cmdb_admin` full access to all sections; `sn_cmdb_editor` read-only; creating a child class needs `sn_cmdb_admin`/`Itil_admin` with `personalize_dictionary`; dependent rules read=`sn_cmdb_editor`+`itil`, full=`sn_cmdb_admin`+`itil_admin`; Identification simulation needs `sn_cmdb_admin`+`admin`; non-CMDB tables unsupported (use non-CMDB IRE procedure). Per-task rows, don't collapse.

```
CI Class Manager
└── Hierarchy → select class (Add Child Class shows only when Is_Extendable=true)
    ├── Class Info          → Basic info (label ≤80 chars ↔ update() label language; table name auto u_cmdb_ci_* prefix, lowercase+underscore ≤80; Extensible, Principal Class icon, description)
    │                          Attributes (per column; double-click Identification Rule col→true to mark a CI identifier)
    │                          Reconciliation Rules → static + Data Refresh Rules (Add)
    │                          Suggested relationships (Query Builder)
    ├── Identification      → the class's single identification rule (entries + optional condition)
    │   (d) Dependent rules → hosting/containment (shown only if a dependent identification rule exists)
    └── Health              → compliance audit · certification template · orphan rule · staleness rule · mandatory/recommended attributes · Health inclusion rules
```
Children derive the parent identification rule wholesale (entries+related entries) until replaced; child rules REPLACE parent rules.

**Child-class wizard order:** 1 Provide Basic Info → 2 Add Attributes (mark identifier cols) → 3 Set Identification Rule (inspect derived rule; `Replace` to author class-specific entries) → 4 Dependencies (conditional on dependent identification rule) → 5 Add Reconciliation Rules (+Data Refresh Rules) → 6 Add Suggested Relationships. Creating a class finishes with **both** recon + data refresh rules — skipping them means no source is authorized to update it silently "frozen" [B][particle-1][my corpus].

**Related screens outside the tool** [A][B][particle-1][matrix]:
| task | path |
|---|---|
| Identification/CI rules | `Configuration > Identification/Reconciliation > {Identification Rules, Identification Inclusion Rules}` |
| IRE Data Source Rule (insert gate) | `Configuration > Identification/Reconciliation > IRE Data Source Rule` (learning-guide: **Data Sources**) |
| Identification simulation (dry-run; no commit) | `Configuration > Identification/Reconciliation > Identification Simulation` (Start→pick class→Criterion Attributes→Generate Script→Run Simulation; final execution via `createOrUpdateCI()`) |
| CMDB IRE properties | `Configuration > CMDB Properties > Identification/Reconciliation Properties` |
| Discovery properties | `Discovery > Discovery Definition > Properties` |
| CMDB Workspace De-duplication Dashboard + templates | CMDB Workspace → De-duplication Dashboard |
| De-duplication tasks | `reconcile_duplicate_task` list |
| Data Source History | `cmdb_datasource_last_update.list` |
| Data Source Staleness (non-CMDB) | `cmdb_datasource_staleness.list` |
| Duplicate remediator props | `Configuration > CMDB Properties > Duplicate CI Remediator Properties` |
| Metadata editor (hosting/containment, synchronized with CI Class Manager) | `Configuration > Metadata Editor` |
| Domain separation override | `Configuration > Domain Support > Domain Overrides` (CMDB) |
| Exclusions/sync classes list | `glide.discovery.exclude_ip_sync_classes` |

**Pre-flight checklist (new class):** parent `Is_Extendable=true` · `sn_cmdb_admin`/`itil_admin`+`personalize_dictionary` · finalize `Display name`≤80 + `Table name` remainder (`u_cmdb_ci_*`) · Principal Class decision · attributes marked as identifiers · derived rule accepted or Replaced · dependent rule exists iff Dependencies needed · reconciliation+data refresh rules prepared · suggested relationships · Identification Simulation pass before first broad scan.

## 14. Verification & observability

| signal | where | what to look for |
|---|---|---|
| Discovery Status | `Discovery > Discovery Status` (related list on schedule) | state flow, `Completed` vs `Started` counters, `Scan N of M`, cancel drops Ready jobs |
| Discovery Timeline | Show Discovery Timeline per device run | queueing vs processing time + ECC records per step — where the stall actually is |
| ECC Queue | `Discovery > ECC Queue` | raw payloads/XML in/out |
| Discovery Log | `Discovery > Logs` | warnings/errors by probe/device; `log_message_length=200` truncates |
| Discovery Home | `Discovery > Home` | tiles Schedules / Discovered Devices / Cloud Resources / Errors (+ remediation hints) |
| Discovery Admin Workspace | errors + anomaly detection views | schedule anomaly detection (ML default; 20% thresholds; `discovery_schedule_anomaly_*` props) |
| Identification Logs | `Configuration > Identification Logs` | IRE decisions per CI (cap 1000 via `glide.identification_logs.max_run_ids`) |
| Identification Simulation | as above | dry-run w/ zero CMDB commit; inspect execution log |
| CMDB Health | Health dashboard/KPIs | completeness / correctness / compliance; dup metric narrowness caveat |
| CMDB 360 | Multisource CMDB | required for Dynamic IRE; compares source values |
| Cancellation | active run cancel | started sensor jobs terminated immediately; queued-but-unstarted deleted |

Debug-only properties (bounded windows, revert after): `glide.discovery.debug.ci_identification`, `glide.discovery.log_debug`, `glide.discovery.log_debug_info`, `glide.cmdb.logger.source.identification_engine=debug|debugVerbose`, `mid.probe.collect_debug_info=true`, `mid.shazzam.*` adjustments, `glide.identification_engine.enable_reconciliation_filter_before_update`.

## 15. Anti-patterns (complete fleet merge — every one appeared in ≥2 independent sources)

1. Name-only identification rules
2. More than one entry "for safety"
3. **lookup entries** when a regular one would work
4. `enforce_unique_ips` as if it were an identification control
5. `skip_duplicates=false` everywhere / raising threshold without fixing rules
6. Tuning reconciliation to stop duplicates (wrong engine)
7. Inclusion rule class-scoped on a parent class
8. Two identification strategies for one table (class identifier + parent lookup)
9. Custom identifier with default Order (never runs)
10. Renaming NIC labels/adapters on bonded hosts
11. Editing `duplicate_of` by hand
12. One giant schedule
13. Overlapping schedules over same ranges ("for speed")
14. Multi-page pattern estates leaving `multi_page_serial_mode=false`
15. Untrusted source with insert privileges on thin classes (use DSR)
16. No reconciliation rule for an authorized source (write freeze or free-for-all)
17. `Update with Null` on sensitive attributes
18. Ignoring Max run time / Max idle
19. Deleting CIs to clean up (prefer de-dup remediation + deletion strategies)
20. Changing serial syntax in sensors/patterns
21. Leaving debug props on in prod
22. Exclusion list >500k entries (cancels runs)
23. Discovering with account lacking local admin on Windows; indirect cause of most WMI "couldn't classify"
24. Dynamic IRE on with no reconciliation plan (DSRs/refresh silently dead — use `cmdb_dynamic_ire_skip_class` deliberately)
25. Assuming def. rule beats attr-specific even with better priority — inverted, attr-specific always wins

Deletion strategies (patterns only; `sa_ci_to_pattern`): **Keep** (default) · **Delete** · **Mark as absent** (`install_status=Absent`; exceptions: `cmdb_ci_network_adapter`, `cmdb_ci_ip_address` are **deleted**) · **Delete relations** · **Mark as retired**.

## 16. Deletion strategies
Pattern-related CI types discovered but missing on re-scan fall under `Deletion Strategy` in `Related CI Types [sa_ci_to_pattern]`: Keep / Delete / Mark as absent / Delete relations / Mark retired. `cmdb_ci_network_adapter` and `cmdb_ci_ip_address` are always deleted on "mark as absent". Applies to patterns only.

## 17. Behavior & MI auto-selection reference (condensed; see §4)
Auto-Select: Discovery-app MID + matching range → ALL-app MID → lowest `Order` Up (random among ties) → default MID Discovery, then ALL → Paused/Upgrading. Not for IPv6. **Use Behavior** whenever selection must differ by credential/protocol/domain/ACL; functionality criteria `mid_server|win_domain|mid_win_domain` gate Windows MIDs to domains. Phase = integer; same-phase functionalities share one Shazzam pass; numeric order. Behaviors must contain ≥1 functionality.

## 18. Release drift, spelling, and defaults that flipped
- **Australia flips** (new customers only): `hostname.snmp_trusted`/`ssh_trusted`/`wmi_trusted`/`ip_service_affinity` → **true** (docs updated 2026-03-12; existing installs keep old default).
- **skipduplicates spelling** — ServiceNow pages surface both `glide.identification_engine.skip_duplicates` (Australia `properties-id-reconciliation.html` body literally prints `glide.identificationengine.skipduplicates` in prose) — confirm both spellings **in your `sys_properties`** before setting; do not silently "fix" one.
- **Log message length** — Australia: `glide.discovery.log_message_length=200` (disabling ≤0); community/Brazil-sourced docs also cite `glide.discovery.log_message_chars` / `log_debug_info`. Check your release's property table.
- IP→Hostname: `hostname.always_update=true` trusted sources only.
- Zurich/Yokohama diffs vs Brazil/Australia — not diffed here; property names stable across the four.
- Doc navigation labels (ITOM vs IT Operations Management vs Discovery Admin Workspace vs classic) and KB numbers drift — prefer table targets (`discovery_schedule`, `ecc_queue`, `cmdb_ci_*`).
- **Dynamic IRE** — `glide.identification_engine.dynamic_ire.enabled=false` default; `dynamic_ire.auto_compare=true` compares vs Static monthly/on-demand without switching; class exemptions in `cmdb_dynamic_ire_skip_class` (Brazil); verify on Australia instance.
- IRE repackaged under `Configuration > Identification/Reconciliation`; the classic `All > Discovery > Discovery Definition > {Schedules, Properties}` remains.

## 19. KB & community reference list (validation aids, NowSupport/user auth needed for most)
KB0756709 (data precedence, last-update check) · KB0869861 (duplicate CI troubleshooting & inclusion-rule pitfalls) · KB0755747 (retire status not auto-flipped) · KB0535236 (WMI 135 + dynamic high ports) · KB3104470 (ID/reconcile fundamentals) · KB2558192 (de-dup tasks vs retired CIs) · KB3222102 (sys_updated_on no-write behavior) · KB1064718 (IRE fundamentals) · KB0951047 (event management duplicates) · KB0960404 (MID Server knowledge collection) · KB1542272 (SNMPv3) · KB0750382/83/86 (Discovery design series) · KB0755747. Community threads consulted: servicenow.com/community ITOM articles (Discovery overview, phases), CMDB community (four-pillar comparison, reconciliation deep-dive, dedup pitfalls), developer forums (class-scoped inclusion rules). All landed references live only through their URLs; content not reproduced.

## 20. Merge log — what was merged, what conflicts were resolved, validation applied

### 20.1 Coverage merged (by source of record)
| area | strongest source(s) | merged from |
|---|---|---|
| IRE four rule families (deep technical matrix; 39 permutations) | `results/20261113T090000Z__deepseek-v4-pro__deepseek__kilocode/` (deepseek-v4-pro) | matrix adopted near-verbatim §9.2 |
| Canonical 4-phase model + schedule form + behaviors + MID selection sequence | deepseek-flash (kilo-cli, Brazil, 68 topics) + buffy (evidence-heavy) + kilo-ernie (lead, ITOM/Brazil) | §4–§7 |
| Australia property catalog & Australia-new-customer default flips | my own live fetch (`inkling-2-small`) | §8 |
| Partial/incomplete payloads, reclassification flags, IRE properties full list | my fetch + kilo-cli + v4-pro matrix + kilo-ernie | §9 |
| Duplicate prevention layers + KB pitfalls | openrouter-free WT5 (KB-sourced, strong) + buffy WT1 + kilo-cli + my raw dup corpus | §11–§12 |
| Insert vs update decision matrix | buffy table + kilo-cli table + my matrix + matrix-file permutations | §9/§10 |
| CI Class Manager breadcrumbs, wizard, roles matrix | particle-1 (evidence docs) + my ci-class-manager fetch + kilo-ernie (WT2) + kilo-cli | §13 |
| FBD, Configuration Console, deletion strategies | kilo-cli (Brazil) | §7, §16 |
| Verification/observability matrix | all (buffy-Status states unique, kilo-cli-Timeline unique) | §14 |
| Anti-patterns | union of all agents, deduped by frequency | §15 |

### 20.2 Conflicting claims resolved by validation
| # | conflict | resolution |
|---|---|---|
| 1 | `file_tracking.max_files_per_ci` = 4 (kilo-ernie WT1) vs 50 (my Australia fetch; file doctable `file_tracking.max_files_per_ci=50, max_file_size=500000, change_limit_count=4, change_limit_days=7`) | Australia fetch wins — kilo-ernie conflated `change_limit_count` (4) with `max_files_per_ci` (50). Documented §8.4. |
| 2 | "`enforce_unique_ips` is duplicate-class control" vs "not an identification control (can erase VIPs/shared IPs)" | Resolution: it's not an identification control; kept only as opt-in IP-invariant guard; flagged in §8.1 and §15. All agents agree default `false`. |
| 3 | "lower priority number = higher authority" (Brazil docs + community) vs "higher priority = more authority" (one community deep-dive) | Brazil/Australia docs + buffy/kilo-cli/matrix: **lower number wins**. Community reversal recorded as wrong-but-see-instance; ask before trusting that thread. |
| 4 | "Data refresh applies to any reconciliation" vs "static-only; **no effect** under dynamic reconciliation" | Dynamic-off rule wins across buffy, kilo-cli, v4-pro matrix, my Australia docs — static-only. §10. |
| 5 | "Data refresh measured by `sys_updated_on`" vs "`cmdb_datasource_last_update` (Data Source History)" | Data Source History wins (buffy + my fetch + kilo-cli agree). §10. |
| 6 | "insert gated by reconciliation" vs "reconciliation never blocks insert" | insert gated by identification + IRE data source rules only. §9. |
| 7 | "DSR rules block updates deliberately" vs "DSR can only block inserts" | insert-only wins (all agents + docs). §9.2/§12. |
| 8 | "IRE data source rules have no impact under dynamic reconciliation" vs "always apply" | dynamic IRE ⇒ DSR + refresh both neutralized; only `cmdb_dynamic_ire_skip_class` exempts a class back to Static IRE. §9.2/§18. |
| 9 | "lookup entry = 100 priority highest" vs "Order low→high overall" | Order low→high globally; 100/200 are just defaults. §9.1. |
| 10 | "name is STILL recommended as identifier on bonded adapters" vs "avoid name (renames break)" | Both true: keep `name` in adapter-distinguishing rules knowing bonded-renaming breaks match — best practice add serial/UUID to that same class rule; never rename NIC labels. §8/§11. |
| 11 | "always true output max_run for duplicates" vs "skip_duplicates only < threshold" | threshold 5 governs the pick; above → match fails. §10. |
| 12 | "de-dup tasks always created" (kilo-ernie WT4/kilo-ernie) vs "only under conditions (no explicit docs line)" | Kept as KB0853105-style community-corroborated claim, tagged UNVERIFIED rather than promoted to default behavior. §11. |
| 13 | "install_status does not flip on rediscover" — my doc said nothing | Confirmed correct (KB0755747 + v4-pro); keep. §12. |
| 14 | Child-vs-substitute identification rules | "child rule **replaces** derived parent rule fully" (buffy, my corpus §17 Create CI Type). Wins over looser "child overrides parent" phrasing. §9.1. |
| 15 | Duplicate metric scope | "only classes w/ identification rules AND (empty discovery_source OR active de-dup task)" (buffy + KB). Wins over generic "CMDB Health flags duplicates". §11/§14. |

### 20.3 What was NOT independently verifiable this pass
- `cmdb_dynamic_ire_skip_class` semantics & exact column set (Brazil-only citation) — treat as accurate-to-Brazil, verify on Australia.
- Exact `cmdb_reconciliation_definition` spelling (Australia docs print `cmdbreconciliationdefinition`).
- `Dynamic IRE` production behavior (all sources default `dynamic_ire.enabled=false`).
- Exact schedule auto-start/priority behavior; `After Discovery` chain `Even if canceled` is docs-cited.
- CI Class Manager default UI tab sets across patch levels.
- Australia-specific diff of all ~110 properties vs Brazil (names stable; defaults only flagged where docs contradict, see §18).
- KBs requiring Now Support auth (all heavy KB0869861-relevant guidance is corroborated by ≥2 agents).

---

## 21. How to use this document
1. Fresh deployment → **§3** order; infra → **§4–§8**; rules → **§9–§10**; duplicates → **§11–§12**; new class → **§13**; ops → **§14**; anti-patterns → **§15**.
2. Every edit to a live instance touches IRE + identification — run **Identify simulation** first; watch **Discovery Status** and **Identification Logs** after.
3. Any property not echoed in §8/§9.1 — pull the page from Australia docs: `servicenow.com/docs/r/australia/...` or Brazil `.../docs/r/it-operations-management/discovery/...`. Search `/docs/api/khub/topics/search` (POST) with `family` filter authoritative; paths change per release.
4. Terminal bar: **do not** ship config changes to prod without dry-run (`glide.duplicate_ci_remediator.dry_run=true` for remediation or Identification Simulation for IRE edits).

## 22. Agent contributions ledger (who wrote what — for audit/blame)
- `inkling-2-small__openrouter__kilo` (this file) — research/raw corpus (17 Australia articles), fetch tooling, property catalog §8, merge analysis, conflict validation §20. Report: THIS FILE.
- `deepseek-flash__openrouter__kilo-cli` (OpenRouter/DeepSeek Flash) — Brazil/68 topics reference (agents/deepseek-flash__openrouter__kilo-cli/SNC_DISC__WT1/05_FINAL/DISCOVERY_CONFIG_REFERENCE.md); patterns/FBD/console/behaviors/timeline/deletion-strategies; config-console & IRE terminology audit.
- `deepseek-v4.1-flash-fast__freebuff__buffy` (OpenAI/Claude-freebuff? harness: Buffy) — evidence digest 28 sources; Status device states; Shazzam batch form rules (1000/256/≤0); IP exclusion >500k; multi_page_serial_mode; three-stale-mechanisms table; dup-metric narrowness; disable-rename pitfalls.
- `deepseek-v4-pro__deepseek__kilocode` (Kilo) — IRE_RULE_APPLICABILITY_MATRIX.md (39 permutations; §9.2 merged); KB-backed insert/update write behavior (sys_updated_on no-write; last_discovered always stamps); COVERAGE_GAP_ANALYSIS validating the guide. Gap: needNowSupport access not used.
- `deepseek-v4-flash__deepseek__hermes` — 4-phase community+KB writeup; WMI connectivity KB; ire_err_exclusion_list gotcha; templates/retroactivity warning; reconciliation evaluation ordering caveat (input-payload class evaluated, not CI's current class).
- `kilo-ernie-5.5-flash__baidu__kilo` (Baidu ERNIE 5.5 Flash) — combined WT1-5 synthesis; insertion-blocked downstream behavior of merged IRE pipeline; property `file_tracking.max_files_per_ci` conflict resolved **against** it (§20.2 #1).
- `openrouter-free__openrouter__kilo` — KB0869861 checklist (inclusion rules/ACL/BR/domain-separation/duplicate_of/source=Duplicate); retired-status auto-reactivation BR (KB0755747); multi_page_serial_mode corroboration; dependency containment (Kubernetes pod UID).
- `particle-1__openrouter__alt-swarm` (particle-ai/particle-1:free) — CI Class Manager role matrix per task; wizard order; basic-info field constraints (80 chars, u_cmdb_ci prefix, Extensible, Principal Class); pre-flight checklist.
- `qwen3.5-4b__ollama__alt-swarm` — evidence-constrained inventory; flagged event-priority default missing — cross-checked → my Australia fetch shows 100.
- `qwen2.5-coder-7b__ollama__alt-swarm` — evidence-constrained dup checklist (skip thresholds table) — merged §10.
- `qwen3-30b-a3b__ollama__hermes`, `qwen2.5-7b__ollama__hermes`, `llama3.1-8b__ollama__hermes` — initial contested-with-nothing-new confirmations; corroborate default-true skip_duplicates and Order semantics; superseded by merged text above.
