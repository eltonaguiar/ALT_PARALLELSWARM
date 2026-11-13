# ServiceNow Discovery — Configuration Reference

**Release basis:** ServiceNow Zurich (family release), English docs, captured 2026-11-13.
**Author:** `deepseek-flash` via provider `deepseek`, Kilo CLI harness, worktree `nvidia-v4`.
**Audience:** Discovery admins, CMDB/IRE admins, platform architects.

> **How to read this**
> - Facts are taken from the ServiceNow Zurich documentation listed in §10.
> - Statements marked **[practitioner]** are operational judgement, not product documentation.
> - Defaults are quoted as documented. New (zBooted) Zurich instances sometimes differ from
>   upgraded instances — those cases are called out explicitly.
> - This reference is deliberately opinionated about *order*: doing IRE work before
>   classification/identification works is the most common cause of duplicate CIs.

---

## 0. Executive summary

Discovery is an **agentless pipeline**: a MID Server scans targets, the instance
classifies devices, identifies them against the CMDB, then explores them. The CMDB write
is not done by Discovery directly — Discovery hands a payload to the **Identification and
Reconciliation Engine (IRE)**, which applies identification, reconciliation, and data-source
rules before insert/update.

The five control planes you must configure, in dependency order:

1. **Reachability** — MID Server(s), IP ranges, credentials.
2. **Classification** — Shazzam port scan → classifier → CI class.
3. **Identification** — identity probe/sensor → identifier rule → existing CI or new CI.
4. **Reconciliation & data-source authority** — which source may write which attribute,
   and which source may create CIs at all.
5. **Hygiene** — duplicate thresholds, deletion strategies, data refresh, monitoring.

If you only remember one thing: **duplicate prevention is an identification-rule design
problem first, and a duplicate-cleanup problem second.** Remediation tools clean up the
symptoms; weak identification rules keep manufacturing duplicates.

---

## 1. Architecture and data flow

### 1.1 Horizontal vs top-down discovery

| Type | Purpose | Output |
|---|---|---|
| **Horizontal discovery** | Scan the network, find devices and applications, populate CIs and direct relationships ("application runs on server"). | CMDB CIs + relationships; no business-service context. |
| **Top-down discovery** (Service Mapping) | Map CIs that belong to a business service and their dependencies. | Service-level dependency maps. |

Normal sequence: horizontal discovery first, then top-down Service Mapping. Both feed the
same CMDB and the same IRE.

### 1.2 The four horizontal phases

| Phase | What happens | Key configuration |
|---|---|---|
| **1. Scanning** | Shazzam probe + port probes are placed on the ECC queue; MID Server scans common ports (WMI, SSH, SNMP, HTTP) and reports which responded. | Discovery schedule IP ranges, MID Server/behavior, Shazzam batch size, SNMP version. |
| **2. Classification** | The successful port probe selects a **classifier**; a classification probe determines OS/device type. Exactly one classification probe per device. | Classifiers, classification criteria, order, trigger probe. |
| **3. Identification** | Identity probes/sensors collect serial number, name, IP, MAC; **identifiers** decide whether to update an existing CI or create one. | Identity probes/sensors, identifier rules, IRE identification rules, `source_name`/`source_native_key`. |
| **4. Exploration** | Additional probes or a **pattern** collect attributes, software, applications and relationships. | Probes/sensors or patterns; applicative credentials; pattern operations. |

With **patterns**, phases 3 and 4 are unified: the pattern's operations perform both
identification and exploration, and only the **Horizontal Discovery Sensor** is used.
Patterns need both host credentials and **applicative credentials** to see applications.

### 1.3 Components

| Component | Role | Where configured |
|---|---|---|
| **MID Server** | Agentless worker inside the firewall; polls the ECC queue, runs probes/patterns, returns XML. Starts all communication outbound (SOAP over HTTPS). | `Discovery > MID Servers`; MID Server `config.xml`; application/capability assignment. |
| **Shazzam probe** | Port scanner that discovers live devices and hints at type. | Probe record; schedule batch size; `glide.discovery.shazzam_*` properties. |
| **Classifier** | Maps a responding device/probe result to a CI class and triggers further probes/patterns. | `Discovery Definition > Classifiers` (CI and process classifications). |
| **Probe / sensor** | JavaScript collector / parser pair. | Probe and sensor records; ECC queue. |
| **Pattern** | NDL operation sequence used in identification/exploration; preferred modern approach. | Pattern Designer; Horizontal Pattern probe; `sa_ci_to_pattern` for related-CI deletion. |
| **Identifier** | Discovery-era rule that matches a device to an existing CI. | `cmdb_identifier`, `cmdb_identifier_entry`; CI Class Manager in current releases. |
| **IRE** | Central CMDB write gate: identification, reconciliation, data-source rules, dedup. | CI Class Manager; `Identification/Reconciliation` module; IRE APIs. |
| **CMDB 360 / Multisource CMDB** | Stores per-source attribute values and enables dynamic reconciliation. | CMDB 360 configuration; required for dynamic reconciliation rules. |
| **Discovery Admin Workspace** | Operational console for schedules, IP inventory, diagnostics, tuning, content. | `Discovery Admin Workspace`. |

### 1.4 Where the CMDB write actually happens

1. Discovery builds a payload (`items`, `relations`, `values`, optional
   `sys_object_source_info`).
2. IRE validates the payload and computes identifier keys.
3. IRE matches: `sys_id` → source key (`source_name` + `source_native_key`) →
   identification-rule criteria (dependent CIs first).
4. IRE reconciles attribute conflicts using static or dynamic reconciliation rules.
5. IRE commits inserts/updates, or stores **partial/incomplete** items for later.
6. Discovery updates `last_discovered` / `discovery_source` even when no other attribute
   changed.

---

## 2. Order of operations (greenfield)

This is the sequence that minimizes rework. Each stage has an exit check.

### Stage 0 — Entitlement, plugin, roles

- Confirm ITOM Visibility/Discovery entitlement and install the Discovery application
  (Guided Setup or ITOM Configuration Console). Zurich Patch 8+ prefers the **ITOM
  Configuration Console**; the older **ITOM Discovery Guided Setup** still exists at
  `All > ITOM Guided Setup > ITOM Discovery Guided Setup` and is organized as
  **Learn → Crawl → Walk → Run**.
- Grant `discovery_admin` to Discovery operators. IRE rule work needs `itil_admin`;
  identification simulation and some class operations need `admin`; class creation also
  uses `personalize_dictionary`.
- Decide **domain separation** before creating schedules/credentials if you will use it.

**Exit check:** a user with `discovery_admin` can open `Discovery > Discovery Schedules`
and `Discovery > MID Servers`.

### Stage 1 — MID Server

- Install at least **two** MID Servers on physical/virtual hosts; assign the **Discovery**
  application (or **ALL**). Place them so they can reach the target ranges.
- Validate connectivity: `Discovery > MID Servers`; check the MID Server log on the host
  (`agent\logs\agent0.log0`) and the instance-side log.
- If using a cluster, decide cluster membership now; a MID Server cannot belong to a
  load-balancing cluster and a failover cluster at the same time.

**Exit check:** MID Servers show **Up/Validated** and their IP ranges cover the pilot
subnet.

### Stage 2 — Credentials

- **Windows/WMI:** the login configured for the MID Server service is used; no separate
  WMI credential is required for the MID host's own domain context. For multi-domain
  Windows, use PowerShell and/or behaviors with criteria.
- **UNIX/Linux:** SSH credential on the instance (user, key/password, privilege
  escalation as required).
- **SNMP:** v1/v2c community or v3 credential on the instance.
- **vCenter / cloud:** platform-specific credentials; cloud discovery also needs service
  accounts and, for some paths, a MID Server with cloud access.
- Prefer **credential aliases** over duplicating secrets; external credential storage is
  enabled by `com.snc.use_external_credentials=true` (default true).
- Discovery auto-selects which credential works per device; it does not need one
  credential per host.

**Exit check:** a Quick Discovery against one host succeeds and the Discovery log shows
the credential used.

### Stage 3 — IP ranges / range sets

- Define exactly what Discovery may scan. Nothing outside these ranges is touched.
- Use **Quick ranges** for simple comma-separated IPs/CIDRs/ranges, or **Discovery Range
  Sets** for reusable ranges across schedules.
- For large estates, run **Network Discovery** first to learn IP networks, then convert
  them into range sets.
- Exclude sensitive/irrelevant networks deliberately (security and performance).

**Exit check:** the pilot range is represented once, with no overlapping duplicate ranges
inside the same schedule.

### Stage 4 — Discovery schedule

Create the schedule at `Discovery > Discovery Schedules` (or the Discovery Admin
Workspace) and configure:

| Setting | Guidance |
|---|---|
| **Discover** | `Configuration items` for normal CI discovery (uses identifiers and updates CMDB). `IP addresses` scans without credentials and does **not** update the CMDB. `Networks` populates IP networks. `Service` is Service Mapping. `Serverless`, `Cloud application`, `Cloud resources`, `Certificates` are specialized. |
| **MID Server selection method** | Auto-Select (based on ranges; not supported for IPv6), Specific MID Cluster, Specific MID Server, or Use Behavior. |
| **Behavior** | Required for multiple domains/protocols, load balancing, ACL-protected SNMP, or avoiding double scans. |
| **Run** | Frequency/time; system time zone applies. |
| **Max run time** | Hard stop; remaining tasks cancel. |
| **Max idle time** | Cancels stalled runs; hidden by default — add the column to `discovery_schedule` to use it. |
| **Shazzam batch size** | Default 1000; minimum enforced 256. Smaller batches start classification sooner. |
| **Shazzam cluster support** | Distributes Shazzam across cluster members. |
| **SNMP version** | `ALL` by default; restrict to v1/v2c/v3 when required. |
| **Location** | Assigned to discovered CIs; empty means none. |
| **Log state changes** | Useful during pilot; noisy at scale. |

**Exit check:** schedule is **Active**, ranges are correct, and **Discover now** produces a
Discovery Status with devices in `Active/Classifying/...` states.

### Stage 5 — Classifiers

- Review CI classifiers and process classifiers before the first production run.
- A classifier maps probe results to a CI class and specifies the trigger probe/pattern.
- Classification criteria and **order** matter; the first matching classifier wins.
- For patterns, the classifier specifies the **Horizontal Pattern probe**, which launches
  the pattern.
- Only one classification probe runs per device; if classification is wrong, exploration
  will be wrong too.

**Exit check:** pilot devices land in the intended classes (e.g. `cmdb_ci_linux_server`,
`cmdb_ci_win_server`, `cmdb_ci_netgear`) rather than generic fallbacks.

### Stage 6 — Identification (Discovery layer)

- Verify identity probes/sensors are active and returning serial number, name, IP, MAC.
- Review identifier rules; they are evaluated in `Order` sequence (low to high).
- Ensure serial numbers are not modified by custom probes/sensors/patterns. Do not add
  prefixes or reformat them.
- If you upgrade from a pre-Geneva release, `glide.discovery.use_cmdb_identifiers=true`
  moves identification to the IRE framework; convert legacy custom identifiers first.
- In current releases this property is true by default and Service Mapping always uses the
  IRE framework.

**Exit check:** a re-run of the same host updates the same CI `sys_id`; no new CI is
created.

### Stage 7 — IRE rules (CI Class Manager)

Do this **after** you know the real classes and identifiers, and **before** connecting
noisy third-party sources.

1. Identification rules per class (prefer independent; one strong identifier entry).
2. Identification inclusion rules if you need to narrow scope for performance.
3. Reconciliation rules (static source precedence; or dynamic with CMDB 360).
4. Data refresh rules (staleness per source).
5. IRE data source rules (block untrusted sources from inserting).
6. Dependent relationship rules (hosting/containment) for dependent classes.
7. Optional: Dynamic IRE simulation for Hardware and descendants.

**Exit check:** Identification Simulation for a representative payload returns the intended
match/insert outcome and no unexpected errors.

### Stage 8 — Pilot, validate, then scale

- Start with a small range and a short interval.
- Validate using **Discovery Status**, **timelines**, **device history**, **ECC queue**,
  **Discovery log**, and **Discovery Admin Workspace > Diagnostics**.
- Only after a clean pilot: expand ranges, add behaviors/clusters, enable software
  discovery, and connect SCCM/other sources.
- Configure deletion strategies for pattern-discovered related CIs before the second run.
- Establish a duplicate review cadence (see §6.6).

### Stage 9 — Post-clone

Re-check instance-specific values after cloning: MID Server URLs/credentials, schedules,
capability assignments, cloud accounts, and any property overrides. Discovery docs include
a dedicated **Post-clone Discovery configuration** topic; treat cloning as a configuration
migration, not a copy.

---

## 3. Configuration surfaces in detail

### 3.1 Discovery setup entry points

| Entry point | Path | Use |
|---|---|---|
| ITOM Configuration Console | ITOM Guided Setup → console task (Zurich Patch 8+) | Fastest install/config path; task assignment, Otto automation. |
| ITOM Discovery Guided Setup | `All > ITOM Guided Setup > ITOM Discovery Guided Setup` | Learn/Crawl/Walk/Run structured setup. |
| Manual setup | `Discovery > Discovery Schedules`, `Discovery > MID Servers`, etc. | Full control; required when not using Guided Setup. |
| Discovery Admin Workspace | `Discovery Admin Workspace` | Home, Schedules, IP inventory, Status details, Diagnostics, Content 360, Insights, Tuning, Settings. |
| Classic modules | `Discovery Definition > Properties`, `Classifiers`, `Probes`, `Identifier` | Low-level tuning. |

### 3.2 MID Server selection and behaviors

**Selection methods**

| Method | When to use | Constraint |
|---|---|---|
| **Auto-Select MID Server** | Simple deployments; MID Server IP ranges cover the schedule ranges. | Not supported with IPv6. Requires Discovery or ALL application on the MID Server. |
| **Specific MID Cluster** | Load balancing/failover across MID Servers. | A MID Server cannot be in two clusters. |
| **Specific MID Server** | One worker, small scope, or IP/network/Service scans. | No cluster use; application is added automatically. |
| **Use Behavior** | Multiple domains, multiple protocols, ACL-protected SNMP, large estates. | MID Server field is replaced by Behavior. |

**Behaviors** decide which probes Shazzam launches and from which MID Servers. Each
behavior contains one or more **Discovery functionality** records:

- **Functionality definition** — protocol set (e.g. Windows only (WMI), SNMP only, All
  except SNMP, All except Windows).
- **MID Servers** — one or more; load is balanced across them.
- **Phase** — integer; functionalities in the same phase run in one Shazzam probe, phases
  run in numerical order.
- **Functionality criteria** — `mid_server`, `win_domain`, `mid_win_domain`; required only
  for Windows MID Servers in multi-domain scenarios.

Behavior use cases: load balancing; two Windows domains; SNMP devices behind an ACL;
devices that answer both SSH and SNMP (exclude the protocol you do not want explored).

### 3.3 Credentials

| Target | Credential location | Notes |
|---|---|---|
| Windows (WMI) | MID Server service login | For multiple domains prefer PowerShell; use behavior criteria. |
| UNIX/Linux (SSH) | Instance credential record | Key or password; privilege escalation if needed. |
| SNMP | Instance credential record | v1/v2c community or v3. |
| VMware vCenter | Instance credential record | Required for vCenter exploration. |
| Cloud (AWS/Azure/GCP/IBM/OCI/OpenStack) | Instance/cloud account config | May use service principals, roles, or SSM; see cloud-specific docs. |
| External vault | Credential alias / external storage | `com.snc.use_external_credentials=true` by default. |

Credential design rules:

- Use least privilege; one account per platform/domain where practical.
- Do not reuse a human admin account for discovery.
- Use aliases so credential rotation does not require editing every schedule.
- Applicative credentials are separate from host credentials; patterns need both.

### 3.4 Discovery properties (high-value catalog)

Path: **`Discovery Definition > Properties`**, or **System Properties `[sys_properties]`**
for properties not shown there. Type/default are as documented for Zurich.

#### 3.4.1 Identity, hostname, and duplicate behaviour

| Property | Type | Default | Why it matters |
|---|---|---|---|
| `glide.discovery.use_cmdb_identifiers` | true/false | `true` | Routes identification through the CMDB IRE framework. Set true after converting legacy custom identifiers. |
| `glide.discovery.enforce_unique_ips` | true/false | `false` | If true, clears an IP on other devices sharing it. Can mask legitimate NAT/load-balancer cases. |
| `glide.discovery.exclude_ip_sync_classes` | string | `cmdb_ci_lb` | Classes whose management IP is not replaced by a NIC IP. |
| `glide.discovery.hostname.always_update` | true/false | `true` | Always updates hostname from the trusted source; can overwrite hand-entered names. Probe-based only. |
| `glide.discovery.hostname.case` | choice | `Lower case` | Upper/No change also available. |
| `glide.discovery.hostname.dns_nbt_trusted` | true/false | `true` | Trust DNS/NetBIOS names. Docs warn not to use DNS name as hostname for Linux/AIX/Solaris patterns. |
| `glide.discovery.hostname.include_domain` | true/false | `false` | Include domain in hostname. Same Linux/AIX/Solaris caveat. |
| `glide.discovery.hostname.snmp_trusted` | true/false | `false` (new Zurich: `true`) | Trust SNMP name over reverse DNS. |
| `glide.discovery.hostname.ssh_trusted` | true/false | `false` (new Zurich: `true`) | Trust SSH name. |
| `glide.discovery.hostname.wmi_trusted` | true/false | `false` (new Zurich: `true`) | Trust WMI name. |
| `glide.discovery.domain.name.nbt` | true/false | `true` | Windows domain from NBT vs WMI. |
| `glide.discovery.enable_mac_address_verification` | true/false | `false` | Stops processing an IP if the device's MAC changed mid-run. |
| `glide.discovery.ip_service_affinity` | true/false | `false` (new Zurich: `true`) | Remembers the successful protocol per IP; important with non-standard SSH ports. |

#### 3.4.2 Scanning, scheduling, performance

| Property | Type | Default | Why it matters |
|---|---|---|---|
| `glide.discovery.max_concurrent_invocations_per_schedule` | integer | `3` | Prevents a slow schedule from stacking runs. `0`/negative disables. Does not apply to "Run after = Even if canceled". |
| `glide.discovery.shazzam_simplify_ranges` | true/false | `true` | Removes duplicate IPs across ranges, but only for single-behavior schedules. |
| `glide.discovery.shazzam_ranges_json` | true/false | `true` | Shrinks Shazzam payload. |
| `glide.discovery.schedule_ipv4_limit` | integer | `65536` | Max IPv4 addresses per auto-generated IPAM schedule. |
| `glide.discovery.schedule_ipv6_limit` | integer | `20000` | Max IPv6 addresses; older releases cap at 5,000. |
| `glide.discovery.discoverable.network.max.netmask.bits` | integer | `28` | Ignores very small regular networks during Network Discovery. |
| `glide.discovery.network_owner_method` | choice | `Most Networks` | Which router owns an IP network. |
| `glide.discovery.physical_interface_types` | string | `6,117,9,71,209` | Interface types considered physical for L2 topology. |
| `glide.discovery.switch_interface_types` | string | `7,8,9,26,53,62,69,71,78,115,117,209` | Interface types considered switch ports. |
| `glide.discovery.virtual_interface_types` | integer/string | `53` | Interface types considered virtual. |
| `glide.discovery.L3_mapping` | true/false | `true` | Maps servers/network gear to routers and L3 switches. |
| `glide.discovery.bgp_router_disable` | true/false | `true` | Skips BGP exploration (large tables, OOM risk). |
| `glide.discovery.debug.network_discovery` | true/false | `true` | Verbose network discovery logging. |
| `glide.discovery.log_message_length` | integer | `200` | Discovery Log message cap; `0`/negative disables. |
| `glide.discovery.save_pattern_log` | string | `true` | Saves pattern logs; false reduces DB writes, but failures always save. |
| `glide.discovery.perf.metrics.enable_collection` | true/false | `true` | Collects performance metrics. |
| `glide.discovery.perf.metrics.rollup_by_build` | true/false | `true` | Roll-up grouping. |
| `glide.discovery.perf.metrics.rollup_by_status` | true/false | `true` | Roll-up grouping. |
| `glide.discovery.perf.metrics.rollup_by_target` | true/false | `true` | Roll-up grouping. |
| `glide.discovery.sensors.save_attachments` | true/false | `true` | Keeps ECC attachments for inspection; false saves space. |
| `glide.discovery.use_probe_results_cache` | true/false | `false` | Skips sensor processing when probe results did not change. |
| `glide.eccprobe.max_queued_probes_per_run` | integer | `20` | Caps probes a node picks up per run. |
| `glide.eccprobe.awsrestprobe.max_retries` | integer | `4` | Exponential backoff for AWS rate limits (max 10). |
| `glide.eccprobe.awsrestprobe.max_wait` | integer | `30` | Max retry wait (max 2046 s). |

#### 3.4.3 Exploration, software, events

| Property | Type | Default | Why it matters |
|---|---|---|---|
| `glide.discovery.application_mapping` | true/false | `true` | Enables ADM; disabling stops relationship creation, not probes/classification. |
| `glide.discovery.active_processes_filter` | true/false | `false` | Limits ADM to processes present in Process Classification. |
| `glide.discovery.enable_adme` | true/false | `false` | Enhanced ADM probe with fallback. |
| `glide.discovery.adm.update.applications` | true/false | `true` (Tokyo+ new installs) | Marks application CIs absent/installed based on running process. Must be added manually after upgrade. |
| `glide.discovery.discover_software` | true/false | `true` | Enables software package discovery. |
| `glide.discovery.enable.software_filter` | true/false | `true` | Windows software filtering. |
| `glide.discovery.software_filter_keys` | string | `Language Pack, Hotfix Security Update` | Names containing these are filtered. |
| `glide.discovery.enable.software_simplify` | true/false | `true` | Normalises names/versions; disabling can create duplicate software records. |
| `glide.discovery.enable.software_simplify_sccm` | true/false | `false` | Aligns software names with SCCM. |
| `glide.discovery.software_sccm_managed` | true/false | `false` | Suppresses software for SCCM-managed computers. |
| `glide.discovery.populate_software_instance_table` | true/false | `false` | Legacy SAM table population. |
| `glide.discovery.enable_file_tracking` | true/false | `true` | Tracks configuration files found by patterns. |
| `glide.discovery.file_tracking.max_file_size` | integer | `500000` | Per-file cap. |
| `glide.discovery.file_tracking.max_files_per_ci` | integer | `50` | Per-CI cap. |
| `glide.discovery.file_tracking.change_limit_count` | integer | `4` | Changes allowed per window. |
| `glide.discovery.file_tracking.change_limit_days` | integer | `7` | Window length. |
| `discovery.use.event.processing` | true/false | `false` | Uses Event Framework for sensor processing. |
| `discovery.event.pin.jobs` | true/false | `false` | Node pinning; false may improve throughput. |
| `discovery.event.separate.cloud.events` | true/false | `true` | Separates cloud and IP sensor queues. |
| `com.glide.queue.discovery.sensors.processing_jobs.priority` | integer | `100` | Lower value = higher priority. |
| `com.glide.queue.discovery.cloud.sensors.processing_jobs.priority` | integer | `100` | Same, cloud path. |
| `com.snc.use_external_credentials` | true/false | `true` | External credential storage. |
| `glide.discovery.allow_loopback_adapters` | true/false | `false` | Discovers loopback adapters on SNMP devices. |
| `glide.discovery.mark_esx_servers_as_absent` | true/false | `false` | Absent instead of retired when missing from payload. |
| `glide.discovery.retire_stale_accounts` | true/false | `false` | Cleans stale cloud service account references. |
| `glide.discovery.debug.ci_identification` | true/false | `false` | Debug CI identification log. |
| `glide.discovery.warn_minor_version` | true/false | `false` | Warn on minor version mismatch. |
| `glide.discovery.roundingInterval.cpu` | integer | `1` MHz | CPU speed rounding. |
| `glide.discovery.roundingInterval.ram` | integer | `1` MB | RAM rounding. |
| `glide.discovery.discover_aws_ec2_host_metadata` | true/false | `true` | AWS metadata probes during IP discovery. |
| `glide.discovery.discover_azure_host_metadata` | true/false | `true` | Azure metadata probes. |
| `glide.discovery.sensors.fire_ssh_probe` | true/false | `true` | SSH probe fallback when LB VIPs are missing from SNMP payload. |
| `glide.discovery.enable_ssm` | true/false | `false` | AWS SSM-based discovery. |
| `glide.discovery.ssm.enable_windows` | true/false | `false` | SSM on Windows. |

#### 3.4.4 A note on default drift

Several hostname-trust and IP-affinity defaults changed for **new Zurich installs** but are
not retroactively changed on upgraded instances (`snmp_trusted`, `ssh_trusted`,
`wmi_trusted`, `ip_service_affinity`). Always read the property value on the instance
rather than assuming the doc's new-install default. **[practitioner]**

### 3.5 Classifiers and classification

- **CI classification** maps discovered data to a CI class; **process classification**
  maps running processes to application/process CIs.
- A classifier specifies criteria and a trigger probe (or, for patterns, the Horizontal
  Pattern probe).
- Classification criteria are evaluated in order; keep the most specific classes first.
- Wrong classification is the root cause of many "duplicate" reports: the same host lands
  in two classes, so two independent identification rules can never match each other.
- If you add custom classes, create them in **CI Class Manager** (not the raw dictionary)
  so identification/reconciliation tabs are available.

### 3.6 Discovery identifiers

After classification, Discovery launches **identity probes** that gather serial number,
name, IP, and MAC. The **identity sensor** passes results to identifiers. An identifier:

1. Searches the CMDB for a match using its configured attributes.
2. If found: update the CI (subject to IRE reconciliation) or do nothing.
3. If not found: insert a CI or do nothing.
4. Then launches exploration probes/patterns if configured to continue.

**Identifier tables**

| Table | Contents |
|---|---|
| `cmdb_identifier` | Identifier rule headers (applies-to table, order, active). |
| `cmdb_identifier_entry` | Attribute entries/priorities for each rule. |

**Default rules (examples)**

| Rule | Applies to | Match attributes |
|---|---|---|
| Hardware Rule | `cmdb_ci_hardware` | serial number/type, name, IP, MAC; serial-number and network-adapter related tables. |
| ESX Server Rule | `cmdb_ci_esx_server` | `correlation_id`. |
| Storage Server Rule | `cmdb_ci_storage_server` | CIM object path, name, serial, MAC, IP, serial/adapter lookups. |
| WBEM Service Rule | `cmdb_ci_wbem_service` | `cim_object_path`. |

**Evaluation order:** low `Order` number to high. Custom identifiers must use different
order values. Disable a rule with **Active = false** rather than deleting it.

**NIC bonding caveat:** if interfaces are bonded/teamed, name + IP + MAC may be needed to
distinguish interfaces. If you add `name` to an identifier, do not rename adapters later —
Discovery will not resolve the renamed adapter, marks the old CI Absent, and creates a new
one.

**Serial-number caveat:** do not modify baseline probes/sensors/patterns to add prefixes or
change serial-number syntax. This breaks asset tracking and identification.

**Legacy vs IRE:** current releases use the IRE framework
(`glide.discovery.use_cmdb_identifiers=true`). Upgrades from pre-Geneva may still carry
legacy identifiers; convert custom ones before enabling. Service Mapping always uses the
new framework.

### 3.7 Patterns, probes, and sensors

| Aspect | Probes/sensors | Patterns |
|---|---|---|
| Language | JavaScript | NDL (Neebula Discovery Language) |
| Used in | All phases, including exploration | Identification + exploration |
| CMDB write | Sensor scripts | Horizontal Discovery Sensor |
| Credentials | Host credentials | Host + applicative credentials |
| Deletion strategy | Not available | Available for related CIs (`sa_ci_to_pattern`) |
| Customisation | Probe/sensor records | Pattern Designer |

Operational guidance:

- Prefer patterns for new work; they are the modern path and unify identification +
  exploration.
- Validate pattern commands with the Command Validation task before scaling.
- Pattern logs are saved according to `glide.discovery.save_pattern_log`; failures always
  save.
- Pattern discovery is required for **CI deletion strategies**.

### 3.8 CI deletion strategies (pattern discovery only)

When a pattern finds the main CI but no longer finds a related CI, the related CI's record
in **Related CI Types `[sa_ci_to_pattern]`** decides what happens:

| Strategy | Effect |
|---|---|
| **Keep** | Default; record unchanged. |
| **Delete** | Deletes the related CI and its relationship to the main CI. |
| **Mark as absent** | Sets `install_status=Absent`; does not delete. Exception: network adapters and IP addresses **are deleted**. |
| **Delete relations** | Removes only the relationship. |
| **Mark as retired** | Sets `install_status=Retired`; does not delete. |

Limits:

- Not available for probes/sensors.
- Cannot set a strategy on the **main CI** for Infrastructure pattern types.
- Main CIs can be deleted only for Application or Cloud Resource patterns.
- Does not apply to **related entries** (IRE rules based on related CIs).

### 3.9 SCCM coexistence

- Discovery and SCCM can both write hardware/software data.
- Use `glide.discovery.software_sccm_managed=true` to suppress software from SCCM-managed
  computers, and `glide.discovery.enable.software_simplify_sccm=true` to align names.
- Use `sys_object_source_info` (`source_name=SCCM`, `source_native_key`) for stable
  cross-source identification.
- Use reconciliation/data-source rules so the less authoritative source cannot overwrite
  or insert blindly.

### 3.10 Domain separation and post-clone

- Discovery schedules enforce domain separation; the MID Servers available to a schedule
  are limited to the schedule owner's domain.
- Reconciliation rules can be scoped by domain; child domains inherit parent rules unless
  overridden.
- After a clone, revalidate MID Server URLs, credentials, capability assignments, cloud
  accounts, and schedules. Treat the clone as a new deployment.

---

## 4. CI Class Manager — exact bread crumbs

**Primary navigation:** `All > Configuration > CI Class Manager`.
(Some older topics say `All > CI Class Manager`; both land on the same module.)

CI Class Manager is the central place to view/create/edit class definitions and the
settings for **identification, reconciliation, and CMDB Health**. It does **not** support
non-CMDB tables; use the IRE non-CMDB flow for those.

### 4.1 Screen map

| Bread crumb | What you configure |
|---|---|
| **CI Class Manager → Hierarchy** | Expand the CI class tree; select the class to edit. |
| **Class panel → Class Info** | Basic info, class columns, suggested relationships, CIs of the class, dependency-view icons, delete CIs, principal-class filter. |
| **Class Info → Identification Rule** | Identifier entries, priorities, inclusion rules, and (for Hardware) **Dynamic IRE**. |
| **Class Info → Reconciliation** | Static reconciliation rules, data refresh rules, reconciliation definitions. |
| **Class Info → Dependencies** | Dependent relationship rules (hosting/containment). |
| **Class Info → Health** | Compliance audits, certification templates, orphan/staleness rules, recommended/mandatory attributes, health inclusion rules. |
| **Class Info → Suggested Relationships** | Relationship suggestions used by Query Builder. |
| **Class Info → Service Mapping** | Entry point types and CI types for Service Mapping/Discovery. |

### 4.2 Creating a class (exact flow)

1. `All > Configuration > CI Class Manager`.
2. Click **Hierarchy** to expand the class list.
3. Select the parent class. It must have **Is Extendable** checked.
4. Click **Add Child Class**.
5. **Provide Basic Info:** display name, table name (auto-prefixed `u_cmdb_ci`; lowercase
   alphanumeric + underscore), description, icon, extensible, principal class. Click
   **Next**.
6. **Add Attributes:** add columns. To make an attribute an identifier, double-click its
   **Identification Rule** cell and set it to true. Click **Next**.
7. **Set Identification Rule:** review the derived rule and identifier entries; click
   **Replace** to define a class-specific rule. Click **Next**.
8. **Dependencies:** add dependent rules if the class depends on another CI. This tab only
   appears when dependent identification rules exist. Click **Next**.
9. **Add Reconciliation Rules:** add reconciliation and data refresh rules. Click **Next**.
10. **Add Suggested Relationships:** review/add relationships. Click **Done**.

Required roles: `itil_admin` + `personalize_dictionary` for dictionary edits; `admin` for
full access.

### 4.3 Identification rule editing (CI Class Manager)

- `CI Class Manager > Hierarchy > <class> > Class Info > Identification Rule`.
- Review **identifier entries** in priority order. The strongest entry should have the
  highest priority (lowest order value, per the UI).
- **Independent** rules match on the CI's own attributes. **Dependent** rules require the
  parent/dependent CI to be identified first and use relationship qualifiers.
- Entry types: **regular** (own attributes), **lookup** (related table referencing
  `cmdb_ci`), **hybrid** (regular + lookup).
- **Related entries** create/update related records but do **not** identify the CI.
- Child classes inherit the parent rule unless they define their own; when they do, the
  inherited entries/related entries are no longer in effect and must be re-added.

### 4.4 Reconciliation and data refresh (CI Class Manager)

- `Class Info > Reconciliation` → add/edit reconciliation rules.
- Reconciliation rules can be defined at parent and child levels; child rules override
  parent rules for the attributes they cover.
- **Data refresh rules** declare when data from a source is stale, allowing a
  lower-priority source to update it.
- List views: `All > Configuration > Identification/Reconciliation > Reconciliation
  Definitions` shows all reconciliation definitions.

### 4.5 Dynamic IRE (Hardware only)

- `CI Class Manager > Hierarchy > Hardware > Class Info > Identification Rule >
  Dynamic IRE`.
- **Simulate Dynamic IRE** runs Static and Dynamic IRE in parallel and stores differences
  in `cmdb_ire_output_comparison_item`.
- **Commit to Dynamic IRE** makes Dynamic IRE the only identifier for Hardware and its
  descendants.
- **Change to IRE** switches back to Static IRE.
- Property: `glide.identification_engine.dynamic_ire_enabled`.
- Default: enabled/committed on zBooted Zurich Patch 11+ instances; upgraded instances may
  still be Static. Always check.
- Exclude custom Hardware subclasses when their custom attributes require static rules.

### 4.6 CI Class Manager limitations

- No non-CMDB tables.
- Dynamic IRE applies only to `cmdb_ci_hardware` and descendants.
- Some tabs appear only when the class has the relevant configuration (e.g. Dependencies
  only with dependent identification rules).
- Changes to identification rules are high-impact; use **Identification Simulation**
  before production.

---

## 5. IRE deep dive

### 5.1 What IRE is

IRE is the centralized framework that processes incoming CI data from Discovery, Service
Mapping, import sets, and third-party sources. It applies:

- **identification rules** — decide which CI is the same CI;
- **reconciliation rules** — decide which source may write which attribute;
- **IRE data source rules** — decide which source may create CIs of a class;
- **data refresh rules** — decide when source data is stale.

It prevents duplicates and prevents non-authoritative sources from overwriting good data.

### 5.2 Payload and identifier keys

Minimal item:

```json
{
  "items": [{
    "className": "cmdb_ci_win_server",
    "values": { "name": "SAMLABVM52" },
    "sys_object_source_info": {
      "source_native_key": "16777219",
      "source_name": "SCCM",
      "source_feed": "SCCM Computer Identity",
      "source_recency_timestamp": "2019-08-26 13:00:00"
    }
  }]
}
```

IRE computes an identifier key from either:

1. `source_name` + `source_native_key` from `sys_object_source_info`, or
2. the identification criterion attributes.

The fast path is the source key; identification-rule matching is slower. The property
`glide.identification_engine.skip_sys_object_source_matching` controls whether IRE skips
that fast path and prioritises rules.

### 5.3 Identification rules

An identification rule applies to one CI class and contains:

- one **CI identifier** (the class the rule applies to);
- one or more **identifier entries** (priority-ordered);
- optional **related entries** (create/update related records; not identification).

Entry types:

| Type | Match basis | Risk |
|---|---|---|
| **Regular** | CI's own attributes | Preferred; fast and predictable. |
| **Lookup** | A related table with a reference to `cmdb_ci` | Slower; can conflict with a direct identifier rule and create duplicates. |
| **Hybrid** | Regular + lookup | Useful when attributes alone are not unique (e.g. duplicate VM serials); still costly. |

**Independent vs dependent**

- **Independent** — CI exists on its own (e.g. Server); rule uses its own attributes.
- **Dependent** — CI cannot exist without a parent (e.g. Network Adapter inside Hardware,
  Application hosted on Server); the parent must be identified first, and relationship
  qualifiers participate in matching.
- A dependent CI can have only **one parent** with dependency. Support is limited to **two
  dependency levels**; prefer one.
- Qualifier chains: if the payload's qualifier chain differs from the DB, IRE updates the
  DB qualifier chain to match.

**Inheritance**

- Child class with no rule inherits the parent's rule, entries, and related entries.
- Child class with its own rule replaces the inherited rule entirely; re-add any needed
  entries/related entries explicitly.

**Design rules (from ServiceNow guidance)**

1. Prefer independent rules.
2. Minimise dependent levels (max 2).
3. Avoid lookup identifier entries.
4. Ideally **one identifier entry per rule**; each extra entry reduces performance.
5. Put the strongest identifier entry at the highest priority.
6. Ensure the rule is at the correct class level.
7. Never create a lookup-based rule for a class that also has its own direct identifier
   rule — contradictory matching can create duplicates.

**Lookup-table rules**

- The lookup table must reference `cmdb_ci`.
- Prefer **Enforce exact count match (Lookup)** for stronger matching.
- Missing lookup records are inserted by IRE during identification.

### 5.4 Reconciliation

Reconciliation decides **which source can write an attribute**, not **which CI it is**.

**Static rules**

- Legacy priority model: list authorized sources and their precedence per class/attribute.
- Stored in `cmdb_reconciliation_definition`.
- Define a rule for every source authorized to update an attribute.
- Parent/child inheritance applies; child rules override parent rules for the covered
  attributes.
- An empty attribute list authorizes **all attributes** of the class.
- Overlapping static rules for different sources can coexist; enforcement prevents
  overwrites.
- Domain separation: rules can be scoped by domain; child domains inherit unless
  overridden.

**Dynamic rules**

- Based on **CMDB 360 / Multisource CMDB** values, not source priority.
- IRE selects the **largest or most reported** value across sources.
- Requires CMDB 360.
- Only one dynamic rule per class attribute.
- Stored in `cmdb_dynamic_reconciliation_definition`.
- Dynamic takes precedence over static for the same attribute at the same class level.
- A child class static rule can still override a parent dynamic rule for that attribute.

**Data refresh rules**

- Declare staleness per source so a lower-priority source can refresh stale data.
- Stored/edited via CI Class Manager; also available for non-CMDB tables.

### 5.5 IRE data source rules

Purpose: let a source **update** CIs but not **create** them.

- Navigation: `All > Configuration > Identification/Reconciliation > IRE Data Source
  Rule`.
- Fields: **Active**, **Applies to** (class + children), **Data source**, **Insert Not
  Allowed**.
- Stored in `cmdb_ire_data_source_rule`.
- Child rules override parent rules.
- Only one active rule per class/source pair.
- Does not apply to lookup or related items.
- Does not apply when dynamic reconciliation is in effect.
- On a blocked insert: error `INSERT_NOT_ALLOWED_FOR_SOURCE`; with
  `CreateOrUpdateCIEnhanced()` the item is stored as a partial payload. With
  `createOrUpdateCI()` the whole payload fails (no partial commits).
- If a permitted source later inserts the CI, IRE merges the partial payload, deletes the
  partial record, and the previously blocked source can update the CI thereafter.

### 5.6 Partial and incomplete items (enhanced API)

`CreateOrUpdateCIEnhanced()` / `identifyCIEnhanced` support:

| Feature | API option | Default | Effect |
|---|---|---|---|
| Partial payloads | `partial_payloads` | on | Stores unmatched items in `cmdb_ire_partial_payloads` for later merge. Enabling it forces partial commits + dedup. |
| Partial commits | `partial_commits` | on | Commits valid items even when others fail. |
| Deduplicate payload | `deduplicate_payloads` | on | Merges duplicate items inside one payload. |
| Summary | `generate_summary` | off | Adds per-class processing counts. |

- **Partial** = not enough data to identify, or one of `MISSING_MATCHING_ATTRIBUTES`,
  `REQUIRED_ATTRIBUTE_EMPTY`, `MISSING_DEPENDENCY`, `INSERT_NOT_ALLOWED_FOR_SOURCE`.
- **Incomplete** = stored for logging only.
- Partial payloads are deleted after **90 days**.
- Identifier keys are stored in `cmdb_ire_partial_payloads_index` to match later payloads.

### 5.7 Timestamps and recency

- `last_discovered` + `discovery_source`: IRE always updates these; a payload timestamp
  only applies if newer than the CMDB value.
- `first_discovered`: set on first insert; on update, only changed if provided.
- `source_recency_timestamp` can update `last_scan` on `sys_object_source`; controlled by
  `glide.identification_engine.skip_updating_last_scan_if_older` and
  `..._ire_message_listener_skip_updating_last_scan_to_now`.
- Related toggles exist for `last_discovered`.

### 5.8 Reclassification

IRE can reclassify a CI when the payload's class differs. Reclassification can be
configured/limited; use it deliberately. Uncontrolled reclassification plus multiple
sources is a common source of "vanishing" CIs and duplicate classes. **[practitioner]**

### 5.9 Identification Simulation

- `All > Configuration > Identification/Reconciliation > Identification Simulation`.
- Build a payload from a CI class (it auto-adds required dependencies and valid
  structure) or paste an existing payload.
- Choose the **data source** (ServiceNow Discovery = `ServiceNow`).
- Optionally use **Enhanced Identification** (`identifyCIEnhanced`).
- **Run Simulation** → inspect Input / Logs / Output; adjust rules; rerun.
- Simulation **does not commit** to the CMDB.
- Use the IE/service-cache log levels to control verbosity.

This is the safest way to test identification-rule changes before production.

---

## 6. Duplicate prevention and insert-vs-update

### 6.1 The decision path (what IRE does, in order)

```
payload item
  │
  ├─ sys_id supplied? ──yes──► direct match → update
  │
  ├─ sys_object_source_info.source_name + source_native_key? ──yes──► key match → update
  │        (unless glide.identification_engine.skip_sys_object_source_matching prioritises rules)
  │
  ├─ identification rule matching
  │     ├─ dependent CI? → identify parent/dependency first, then match with qualifiers
  │     ├─ identifier entries in priority order (regular → lookup → hybrid)
  │     └─ match count:
  │           0 → INSERT (subject to IRE data source rule)
  │           1 → UPDATE
  │           >1 → duplicate set → skip_duplicates logic (below)
  │
  ├─ reconciliation: is this source allowed to write the attribute?
  │     ├─ static: source precedence
  │     └─ dynamic: CMDB 360 largest/most-reported value
  │
  ├─ data source rule: may this source INSERT this class?
  │     └─ no → INSERT_NOT_ALLOWED_FOR_SOURCE → partial payload (enhanced API)
  │
  └─ commit (or partial/incomplete)
```

### 6.2 Duplicate handling at match time

Controlled by:

- `glide.identification_engine.skip_duplicates` (default **true**)
- `glide.identification_engine.skip_duplicates.threshold` (default **5**)
- the number of duplicates found

Behaviour:

| Condition | Result |
|---|---|
| `skip_duplicates=true` and duplicates < threshold | Oldest duplicate is chosen as the match/main CI and updated; the rest get `duplicate_of` set to it. IRE filters `duplicate_of` CIs during matching. |
| `skip_duplicates=false` | Matching fails with an error; none of the duplicates are updated. |
| Duplicates ≥ threshold | See the large-duplicate handling in remediation; `glide.duplicate_ci_remediator.max.cis` applies. |

De-duplication tasks are **always** created when duplicates are detected. The
`skip_duplicates` property changes *which* duplicate is used for the update and whether
matching proceeds; it does not suppress task creation.

`duplicate_of` is cleared automatically if any other attribute of the duplicate is updated
by IRE — at that point it is no longer treated as a duplicate.

### 6.3 Duplicate detection and remediation

- IRE groups each duplicate set into a **de-duplication task**.
- Choose a **main CI** to retain; duplicates reference it via `duplicate_of`.
- Bulk: **CMDB Workspace → De-duplication dashboard + Template Library**.
- Single: **Duplicate CI Remediator** wizard (attributes, relationships, related items).
- The main CI's `duplicate_of` must be empty; a main CI cannot be deleted until its
  duplicates are disassociated or deleted.
- Asset-related attributes/relationships are not merged (excluded from the default related
  items list).
- Change requests: if the CI is deleted and the change is not `New`, the CI field is
  cleared; if `New`, it is updated to the main CI. Problems/incidents remain valid because
  the main CI is merged in.
- Large sets: >1,000 duplicates restrict remediation; hard cap 5,000. Only recommended
  main-CI selection is available and reconciliation is limited.
- Duplicate serial numbers can create tasks, but relationship merging does not apply.
- Large related-item sets may time out; restricted mode
  (`glide.duplicate_ci_remediator.enable_restricted_mode=true`) limits related items and
  lets remediation proceed.

**Remediation properties**

| Property | Default | Purpose |
|---|---|---|
| `glide.duplicate_ci_remediator.max.field_length` | `4000` | Excludes/truncates long attributes in remediation. |
| `glide.duplicate_ci_remediator.related_items_blacklist` | `cert_task.cmdb_ci,cert_audit_result.configuration_item,discovery_log.cmdb_ci,alm_hardware.ci,alm_asset.ci,fm_expense_line.ci` | Related tables excluded from merge. |
| `glide.duplicate_ci_remediator.max.cis` | `1000` (cap 5000) | Large-set threshold. |
| `glide.duplicate_ci_remediator.dry_run` | `false` | Test remediation without writing. |
| `glide.duplicate_ci_remediator.enable_restricted_mode` | `false` | Allows blocked remediation to proceed with limited related items. |

Path for these: `Configuration > CMDB Properties > Duplicate CI Remediator Properties`
(or `sys_properties`).

### 6.4 Duplicate prevention design checklist

**Model**

- [ ] Every discovered class has a deliberate identification rule.
- [ ] Prefer independent rules; ≤1 identifier entry where possible.
- [ ] No lookup-based rule on a class that also has a direct identifier rule.
- [ ] Dependent rules limited to ≤2 levels, with correct dependent relationship rules.
- [ ] Child classes that override a parent rule re-add needed entries/related entries.
- [ ] Custom classes created through CI Class Manager with identifiers and reconciliation.

**Data**

- [ ] Serial numbers are discovered unchanged (no prefixes/reformatting).
- [ ] `source_name` + `source_native_key` supplied by integrations when available.
- [ ] Stable, unique source keys; do not recycle keys across devices.
- [ ] Payload ≤500 CIs; no duplicate items; no `sys_*` metadata; minimum criterion
      attributes.
- [ ] Dependent inserts against the same parent are serialized, not fired concurrently.
- [ ] `sys_id` used for known updates.

**Authority**

- [ ] Reconciliation rules exist for every source that may update each attribute.
- [ ] Untrusted sources blocked from inserting via IRE data source rules.
- [ ] Data refresh rules defined for stale sources.
- [ ] Dynamic reconciliation only where CMDB 360 is enabled and understood.
- [ ] Domain separation scoped correctly.

**Hygiene**

- [ ] Deletion strategies chosen for pattern-discovered related CIs.
- [ ] `skip_duplicates`/threshold reviewed against expected data quality.
- [ ] Duplicate dashboard reviewed on a cadence.
- [ ] Discovery pilot re-run yields stable `sys_id`s (no new CIs).
- [ ] CMDB Health orphan/staleness/duplicate KPIs monitored.

### 6.5 Insert vs update — worked examples

**Example A — known update with `sys_id`**

```json
{"items":[{"className":"cmdb_ci_linux_server",
           "values":{"sys_id":"194876usytrr65378098","ram":"2048"}}]}
```

IRE locates the CI directly; criterion attributes are not needed. This is the fastest and
least ambiguous update.

**Example B — source-key match**

```json
{"items":[{"className":"cmdb_ci_win_server",
           "values":{"name":"SAMLABVM52"},
           "sys_object_source_info":{"source_name":"SCCM",
             "source_native_key":"16777219",
             "source_recency_timestamp":"2019-08-26 13:00:00"}}]}
```

If the source key matches, IRE updates without running the slower rule matcher (unless the
skip property changes that). If it does not match, IRE falls back to identification rules.

**Example C — dependent insert**

Tomcat WAR depends on Tomcat, which depends on a Linux server. Supply all three items and
`relations` with indices; supply `sys_id`s for known parents. IRE must identify the parent
chain before it can resolve the child.

**Example D — blocked insert**

An IP scanner that should never create server CIs: add an IRE data source rule for the
scanner + `cmdb_ci_*server`, `Insert Not Allowed=true`. Inserts fail with
`INSERT_NOT_ALLOWED_FOR_SOURCE`; with the enhanced API the item is kept as a partial
payload. If Discovery later creates the server, the partial is merged and the scanner can
update it subsequently.

### 6.6 Anti-patterns that manufacture duplicates

| Anti-pattern | Why it duplicates | Fix |
|---|---|---|
| Two classes for the same device (bad classifier) | Separate identification rules can never match across classes. | Fix classification first; merge/retire classes. |
| Lookup rule + direct rule on the same class | Contradictory match basis. | Keep one independent rule; remove lookup. |
| Multiple identifier entries with weak attributes | Ambiguous matches; performance drop. | One strong entry; move weaker data to exploration. |
| Dependent rules deeper than 2 levels | Parent chain fails or is slow. | Flatten model; use independent identifiers. |
| Renaming NICs when `name` is an identifier | Old CI marked Absent; new CI created. | Freeze adapter names or stop using name alone. |
| Serial-number rewriting in custom probes | Every run produces a "new" device. | Preserve raw serial; normalise downstream. |
| No reconciliation rules | Sources overwrite each other. | Define per-source authority. |
| No data source rules | Noisy scanners create skeleton CIs. | Block insert for untrusted sources. |
| Duplicate entries in one payload | Identification failure/odd matches. | Deduplicate before sending. |
| >500 CIs per payload | Timeouts/partial failures. | Batch. |
| Concurrent dependent inserts | Congestion and partial failures. | Serialize per parent. |
| Dynamic IRE without CMDB 360 | Rules cannot work. | Enable CMDB 360 or stay static. |
| Deleting CIs manually | Breaks relationships/tasks; duplicates return next run. | Use deletion strategies and remediation. |

### 6.7 IRE error codes worth memorising

| Code | Meaning | First response |
|---|---|---|
| `MISSING_MATCHING_ATTRIBUTES` | Item lacks the criterion attributes for at least one identifier entry. | Check payload vs rule; add attributes or `sys_object_source_info`. |
| `REQUIRED_ATTRIBUTE_EMPTY` | A required attribute is missing. | Fix source data/model. |
| `MISSING_DEPENDENCY` | Dependent CI lacks the declared dependency. | Send parent + relation; check dependent rules. |
| `INSERT_NOT_ALLOWED_FOR_SOURCE` | Data source rule blocks insert. | Confirm intent; adjust rule only if source is trusted. |
| Duplicate-match error (when `skip_duplicates=false`) | Multiple matches; updates refused. | Remediate or enable skip_duplicates. |
| Partial payload stored | Item incomplete. | Inspect `cmdb_ire_partial_payloads`; wait for completing source. |

See `IRE error messages` and `Discovery error messages` for the full lists.

---

## 7. Verification and troubleshooting

### 7.1 Run-level checks

| Surface | What to look for |
|---|---|
| **Discovery Status** | State, counts, errors, per-device progress; cancel a stuck run here. |
| **Discovery timelines** | Phase-by-phase timing; where the run stalled. |
| **Discovery device history** | What happened to a device across runs. |
| **ECC queue** | Raw probe/pattern XML payloads and processing state. |
| **Discovery log** | Credential, classification, identification, exploration errors. |
| **Discovery Admin Workspace > Diagnostics** | Built-in diagnostics and support tools. |
| **Discovery Admin Workspace > Tuning** | Performance tuning. |
| **Discovery Admin Workspace > Content 360** | Pattern/content coverage. |
| **Performance metrics** | `glide.discovery.perf.metrics.*`; rollups by build/status/target. |

### 7.2 CMDB-level checks

| Surface | What to look for |
|---|---|
| **Identification Simulation** | Match/insert outcome without writing. |
| **CI Identification Log** | Enable `glide.discovery.debug.ci_identification`. |
| **`cmdb_ire_partial_payloads`** | Held items; 90-day retention. |
| **`cmdb_ire_partial_payloads_index`** | Identifier keys used to complete partials. |
| **De-duplication dashboard** | Duplicate sets and trends. |
| **CMDB Health** | Orphans, staleness, duplicates, compliance. |
| **CMDB 360** | Per-source attribute values for dynamic reconciliation. |

### 7.3 Fast triage table

| Symptom | Likely cause | Check |
|---|---|---|
| Same host appears twice | Classifier sends it to two classes, or identifier too weak | Device history, class, identifier rule |
| CI never updates | Reconciliation rule excludes the source, or payload older than `last_discovered` | Reconciliation definitions, payload timestamp |
| New CI every run | Serial/name changes each run, or `sys_object_source_info` key unstable | Probe output, source key, identifier |
| Insert silently missing | IRE data source rule blocked it, partial payload stored | `INSERT_NOT_ALLOWED_FOR_SOURCE`, partial payloads table |
| Run never finishes | Max run/idle not set; MID Server/credential issue | Status, ECC, MID logs |
| Discovery finds nothing | Wrong range, MID Server not validated, firewall | Schedule ranges, MID Server dashboard |
| Devices classified generic | Classifier order/criteria | Classifiers, probe results |
| Applications missing | No applicative credential, ADM disabled | `application_mapping`, pattern credentials |
| Duplicate software records | `software_simplify=false` | Software properties |
| Discovery load too high | Concurrency, batch size, event processing | `max_concurrent_invocations_per_schedule`, Shazzam batch, Event Framework |

---

## 8. Operational runbooks

### 8.1 First 10 working days (pilot)

1. Day 0: roles, MID Server(s), pilot ranges, one credential per platform.
2. Day 1: Quick Discovery on 5–20 hosts; confirm classification.
3. Day 2: re-run and confirm stable `sys_id`s; inspect identity data.
4. Day 3: review identifier rules for the pilot classes; fix weak attributes.
5. Day 4: create reconciliation rules for every source that will write the pilot classes.
6. Day 5: add IRE data source rules for any untrusted source; test blocked insert.
7. Day 6: Identification Simulation for a representative payload.
8. Day 7: enable deletion strategies for pattern related CIs; second run.
9. Day 8: duplicate dashboard review; remediate any pilot duplicates.
10. Day 9–10: document decisions, then expand ranges in waves.

### 8.2 Weekly / monthly cadence

- Weekly: Discovery Status failures, Error messages, MID Server health, schedule overruns.
- Weekly: new de-duplication tasks; trend count.
- Monthly: identification-rule review for new classes; reconciliation coverage.
- Monthly: partial payloads older than 90 days (should be auto-deleted), orphan/stale KPIs.
- Quarterly: Dynamic IRE simulation (if not committed), pattern/content updates, credential
  rotation.

### 8.3 Change-control rules

- Identification/reconciliation rule changes: test in sub-production with Identification
  Simulation; peer review; change record.
- Property changes affecting identity (`hostname.*`, `use_cmdb_identifiers`,
  `skip_duplicates`, `enforce_unique_ips`): treat as high risk; they can rewrite CMDB
  identity at scale.
- Deletion-strategy changes: high risk; can delete network adapter/IP records.
- Dynamic IRE commit: high risk; simulate first, record parity results.

---

## 9. Decision matrix

| Scenario | Recommended configuration |
|---|---|
| Single domain, <5k devices | 2 MID Servers, Auto-Select, simple Configuration Items schedule, no behaviors. |
| Multi-domain Windows | PowerShell remoting, behavior with `Windows only (WMI)` + domain criteria, one Windows MID per domain (or PowerShell single MID). |
| Devices answering SSH and SNMP | Behavior that assigns SNMP to a SNMP-only MID and SSH/other to another; or exclude the unwanted protocol. |
| SNMP devices behind ACL | Behavior with `SNMP only` functionality on an ACL-permitted MID Server. |
| Large estate (100k+ IPs) | Clustered MID Servers, Shazzam cluster support, batch 1000–5000, range sets, behaviors for load balancing. |
| Noisy third-party scanner | IRE data source rule (`Insert Not Allowed`), reconciliation limits, data refresh thresholds. |
| Multiple sources with no clear priority | Enable CMDB 360 and use dynamic reconciliation (largest/most reported). |
| Custom class with custom attributes | CI Class Manager child class + independent identification rule + reconciliation; exclude from Dynamic IRE if rules must stay static. |
| Virtual machines with identical serials | Hybrid identifier entry (serial + name) or add a unique attribute; test with simulation. |
| SCCM + Discovery | Stable `source_native_key`, `software_sccm_managed`, simplify alignment, reconciliation authority. |
| Cloud + on-prem overlap | Cloud discovery for cloud resources; reconciliation/data-source rules; avoid duplicate server CIs across sources. |
| Need to prove no duplicates before cutover | Identification Simulation + pilot re-runs + duplicate dashboard baseline. |

---

## 10. Sources, confidence, and gaps

### 10.1 Primary sources (Zurich, en-US)

All captured under `research/` with a machine-readable `source_manifest.json`.

| Area | ServiceNow topic |
|---|---|
| Overview / phases | `Exploring Discovery`; `Horizontal discovery process flow with patterns`; `...with probes and sensors` |
| Setup | `Set up Discovery without Guided Setup`; `Discovery Guided Setup`; `Discovery Quick Start` |
| Schedules | `Discovery Schedule form reference`; `Create a new discovery schedule form reference`; `Schedule a horizontal discovery` |
| Behaviors | `Discovery behaviors` |
| Classifiers | `Discovery classifiers`; `Create a Discovery CI classification`; `Create a Discovery process classification` |
| Identifiers | `Discovery identifiers`; `How Discovery identifiers work`; `Configure Discovery identity probes`; `...sensors` |
| Properties | `Discovery properties`; `Discovery Admin Workspace Settings` |
| Deletion | `CI deletion strategies for pattern discovery` |
| SCCM | `Discovery and SCCM together` |
| CI Class Manager | `CI Class Manager`; `Create a CI class`; `CMDB classifications and class dependency` |
| IRE | `Identification and Reconciliation engine (IRE)`; `CMDB Identification and Reconciliation (IRE)`; `Identification rules`; `Reconciliation rules` |
| IRE authoring | `Create a CI identification rule`; `Create an identification inclusion rule`; `Create a CI reconciliation rule`; `Create a data refresh rule`; `Create an IRE data source rule` |
| Duplicates | `Detecting duplicate CIs`; `Duplicate CIs remediation`; `Properties related to remediation of duplicate CIs` |
| Simulation | `Identification simulation` |
| Dynamic IRE | `Dynamic IRE`; `Configure CI reclassification during IRE processing` |
| Errors | `IRE error messages`; `Discovery error messages` |
| Import sets | `Apply IRE to Import Sets` |

### 10.2 Confidence

| Area | Confidence | Reason |
|---|---|---|
| Horizontal phases, components | High | Multiple consistent primary topics. |
| Schedule/MID/behavior options | High | Direct form reference. |
| Discovery properties + defaults | High, with drift caveat | Direct property reference; new-vs-upgraded defaults differ. |
| CI Class Manager paths | High | Explicit navigation statements. |
| Identification/reconciliation semantics | High | Direct conceptual + procedure topics. |
| Duplicate thresholds/remediation | High | Direct properties + procedure topics. |
| Dynamic IRE applicability | High | Explicit Hardware-only and Patch 11+ statements. |
| Customer-specific tuning | Low | Requires instance data; marked [practitioner]. |

### 10.3 Known gaps / follow-ups

1. **Release-specific UI drift**: this reference is Zurich. Washington/Vancouver/Xanadu
   paths may differ; dynamic IRE availability is patch-dependent.
2. **Exact plugin IDs** for entitlement activation were not captured from the docs; use
   Guided Setup/Configuration Console rather than guessing.
3. **Service Mapping top-down configuration** is intentionally shallow; separate research
   needed for entry points and traffic-based mapping.
4. **Cloud-provider matrices** (AWS/Azure/GCP methods, SSM, service principals) are only
   summarised; each has its own configuration topic.
5. **Non-CMDB IRE** is referenced but not detailed; the CI Class Manager does not support
   non-CMDB tables.
6. **Screen-level field validation** (mandatory fields, role checks per button) was not
   tested on a live instance; docs-based only.

---

## Appendix B — Navigation path index

Exact paths used in this reference (Zurich). UI labels can drift between releases.

| # | Path | Purpose |
|---|---|---|
| 1 | `All > Configuration > CI Class Manager` | Central class/IRE/health console. |
| 2 | `All > CI Class Manager` | Alternate entry used by some docs. |
| 3 | `CI Class Manager > Hierarchy` | Expand the CI class tree. |
| 4 | `CI Class Manager > Hierarchy > <class> > Class Info` | Class overview and settings. |
| 5 | `Class Info > Identification Rule` | Identifier entries, inclusion rules, Dynamic IRE. |
| 6 | `Class Info > Reconciliation` | Static reconciliation + data refresh rules. |
| 7 | `Class Info > Dependencies` | Dependent relationship rules. |
| 8 | `Class Info > Health` | Compliance, certification, orphan/staleness, mandatory attributes. |
| 9 | `Class Info > Suggested Relationships` | Relationship suggestions. |
| 10 | `Class Info > Service Mapping` | Entry point/CI types for Service Mapping. |
| 11 | `All > Configuration > Identification/Reconciliation > IRE Data Source Rule` | Block a source from inserting a class. |
| 12 | `All > Configuration > Identification/Reconciliation > Identification Simulation` | Test a payload without committing. |
| 13 | `All > Configuration > Identification/Reconciliation > Reconciliation Definitions` | List all reconciliation definitions. |
| 14 | `Discovery Definition > Properties` | Discovery property catalog. |
| 15 | `Discovery > MID Servers` | MID Server list/validation. |
| 16 | `Discovery > Discovery Schedules` | Schedule list. |
| 17 | `All > ITOM Guided Setup > ITOM Discovery Guided Setup` | Learn/Crawl/Walk/Run setup. |
| 18 | `All > Discovery > Discovery Definition > Functionality Definitions` | Behavior functionality definitions. |
| 19 | `Configuration > CMDB Properties > Duplicate CI Remediator Properties` | Duplicate remediation properties. |
| 20 | `CMDB Workspace > De-duplication dashboard` | Bulk duplicate review/remediation. |
| 21 | `CMDB Workspace > De-duplication Template Library` | Reusable remediation templates. |
| 22 | `System Properties [sys_properties]` | Properties not exposed in module UI. |
| 23 | `All > Configuration > Identification/Reconciliation` | IRE module landing page. |

## Appendix A — Quick reference card

```
Discovery flow:  Shazzam → Classify → Identify → Explore → IRE → CMDB
Key tables:      cmdb_identifier, cmdb_identifier_entry,
                 cmdb_reconciliation_definition, cmdb_dynamic_reconciliation_definition,
                 cmdb_ire_data_source_rule, cmdb_ire_partial_payloads,
                 cmdb_ire_partial_payloads_index, sa_ci_to_pattern
Key nav:         All > Configuration > CI Class Manager
                 All > Configuration > Identification/Reconciliation > IRE Data Source Rule
                 All > Configuration > Identification/Reconciliation > Identification Simulation
                 Discovery Definition > Properties
Key properties:  glide.discovery.use_cmdb_identifiers (true)
                 glide.identification_engine.skip_duplicates (true)
                 glide.identification_engine.skip_duplicates.threshold (5)
                 glide.discovery.max_concurrent_invocations_per_schedule (3)
                 glide.identification_engine.dynamic_ire_enabled (Zurich P11+ new installs)
                 glide.duplicate_ci_remediator.dry_run (false)
```
