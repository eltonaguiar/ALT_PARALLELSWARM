# FINAL — ServiceNow Discovery Configuration Reference (Merged, Validated)

**Compiled by:** `deepseek-flash` · provider `deepseek` · harness Kilo CLI · worktree `nvidia-v4`
**Compiled:** 2026-11-13
**Scope:** all ServiceNow Discovery research on `ALT_PARALLELSWARM` `main`, merged and
cross-validated.
**Primary basis:** ServiceNow Zurich docs (59 topics captured by this author) plus the
Brazil/Australia docs and KB articles captured by sibling agents.

> This file deliberately merges every agent's unique findings. Where two agents disagree,
> the conflict is listed in §12 with the resolution and the evidence used. Release labels
> are preserved: Zurich, Brazil, Australia, Xanadu, Washington DC, Yokohama.

---

## 0. Agents merged, and the ambiguity problem

| Agent folder | Model | Provider | Harness | Release basis | Contribution |
|---|---|---|---|---|---|
| `deepseek-flash__deepseek__nvidia-v4` (this author) | `deepseek-flash` | `deepseek` | Kilo CLI | Zurich | 59 primary topics; IRE/duplicate deep dive; swarm harness |
| `deepseek-flash__openrouter__kilo-cli` | `deepseek/deepseek-flash` | OpenRouter | Kilo CLI | Brazil | 68 topics; four-rule-family audit; FBD/Configuration Console |
| `deepseek-v4.1-flash-fast__freebuff__buffy` | DeepSeek V4.1 Flash Fast | Freebuff / Codebuff | Buffy native | Brazil/Zurich/Xanadu/Washington | 28 sources; KB-cited duplicate/remediation mechanics |
| `deepseek-v4-flash__deepseek__hermes` | `deepseek-v4-flash` | DeepSeek API | Hermes CLI | Community/KB | Four phases; WMI firewall; behavior pitfalls |
| `inkling-2-small__openrouter__kilo` | `openrouter/thinkingmachines/inkling-2-small:free` | OpenRouter | Kilo | Australia | IRE property catalog; reclassification; HTTP classification |
| `openrouter-free__openrouter__kilo` | `openrouter.free` | OpenRouter | Kilo | KB/community | Retired-CI status; inclusion-rule pitfalls; duplicate troubleshooting |
| `particle-1__openrouter__alt-swarm` | `particle-ai/particle-1:free` | OpenRouter | ALT swarm | Brazil | CI Class Manager breadcrumbs/roles |
| `qwen2.5-coder-7b__ollama__alt-swarm` | `qwen2.5-coder:7b` | Ollama | ALT swarm | Brazil | Duplicate decision table |
| `qwen3.5-4b__ollama__alt-swarm` | `qwen3.5:4b` | Ollama | ALT swarm | Brazil | Property inventory |
| `qwen2.5-7b__ollama__hermes` / `qwen3-30b-a3b__ollama__hermes` / `llama3.1-8b__ollama__hermes` | local Ollama | Ollama | Hermes | Brazil/Zurich | Thin drafts; no unique config beyond the above |
| `kilo-ernie-5.5-flash__baidu__kilo` | Ernie 5.5 Flash | Baidu | Kilo | — | Process report only; no Discovery config |

**The ambiguous keys:** two agents report model `deepseek-flash` via Kilo —
`deepseek-flash__openrouter__kilo-cli` (provider **OpenRouter**) and
`deepseek-flash__deepseek__nvidia-v4` (provider **DeepSeek**). A third uses
`deepseek-v4-flash` via DeepSeek. They are **different runs**; do not merge their folders.
This final is authored by the **DeepSeek-provider** run.

---

## 1. Mental model

Discovery is two pipelines that meet at the CMDB:

```
Network / devices
      │  horizontal discovery
      ▼
Shazzam scan → classification → identification → exploration
      │                              │
      │ probes + sensors             │ patterns (NDL)
      ▼                              ▼
Discovery identifier ──────► CMDB IRE identification rules
      │                              │
      └──────────► IRE ◄─────────────┘
                     │
          reconcile → insert / update / no-op
                     │
                     ▼
                    CMDB
```

Three consequences that explain most misconfiguration:

1. **Discovery identifiers and CMDB IRE Identification Rules are not the same object.**
   Probe-based discovery uses Discovery identifiers; pattern-based discovery uses IRE
   Identification Rules. In current releases both are routed through IRE
   (`glide.discovery.use_cmdb_identifiers=true`); Service Mapping always uses IRE
   identifiers regardless of the property.
2. **Duplicate prevention is not one checkbox.** It is four distinct controls plus repair:
   - **Identification Rule** — matches the right CI (prevents duplicates);
   - **IRE Data Source Rule** — insert gate for untrusted sources;
   - **Reconciliation Rule + Data Refresh Rule** — update authority and staleness;
   - **de-duplication tasks** — repair when duplicates still occur.
3. **Reconciliation never blocks an insert.** When IRE inserts a new CI, reconciliation is
   not applied. A missing attribute after Discovery is a reconciliation problem; an extra
   CI is an identification (or inclusion/ACL) problem.
4. **IRE only runs for the `Configuration items` scan type.** An `IP addresses` scan
   creates device history and never writes CIs, so it cannot create a duplicate CI.

---

## 2. Order of operations

### 2.1 Setup order (blank instance → trustworthy CMDB writes)

| # | Step | Why it is here | Exit check |
|---|---|---|---|
| 0 | Confirm subscription/plugin; assign `discovery_admin` | Discovery is a separate subscription; the role grants access to Discovery tables | Role present; plugin active |
| 1 | Install **at least two** MID Servers; assign **Discovery** or **ALL** | MID Servers execute probes/patterns and initiate all communication | `Discovery > MID Servers` shows Up/Validated |
| 2 | Configure and **test** credentials (Windows/SSH/SNMP/vCenter/cloud) | Bad credentials are the leading cause of failed discoveries | Credential test succeeds per protocol/device class |
| 3 | Define IP ranges / range sets; add exclusions and global exclusions | Discovery scans only what you authorize | Ranges resolve; excluded networks absent |
| 4 | Review classifiers (and patterns) for expected device classes | Classifiers select the probes/pattern for identification/exploration | A test device classifies into the expected CI class |
| 5 | Create a Discovery schedule (type **Configuration items**) | The schedule is the control point: when, where, which MID Server, which behavior | Schedule saved; `Discover now` works |
| 6 | Run and watch the four phases | Scanning → classification → identification → exploration | Discovery Status reaches a terminal state |
| 7 | Validate via ECC queue XML, Discovery Log, device history, Home page | Proves what was collected and written | Expected CIs created/updated; no credential errors |
| 8 | Tune properties/classifiers/behaviors | Only after evidence from step 7 | Re-run improves coverage without new duplicates |
| 9 | Configure CMDB governance: Identification Rules, IRE Data Source Rules, Reconciliation Rules, Data Refresh Rules, inclusion, de-dup | Discovery writes through IRE; governance decides who may insert vs update and how duplicates are repaired | Identification simulation passes; duplicate metric stable |
| 10 | Operate: schedules, CMDB Health, Data Manager, CMDB 360 | Keeps the CMDB accurate over time | Health/duplicate KPIs trending correctly |

**Critical ordering rule:** design the **CI class + identification rule** before enabling a
broad schedule. A schedule that discovers 10,000 devices against a weak name-only
identifier is how duplicate floods are created. Do not tune reconciliation first — you
cannot judge which source should own `name` until you have seen what each source writes.

### 2.2 Runtime order (per device, and the state you will see)

| # | Phase | What runs | Discovery Status device state |
|---|---|---|---|
| 1 | **Scanning** | Shazzam probe (port scan) then protocol port probes (WMI/SSH/SNMP/HTTP); results return via the ECC queue | `Alive, not active, not classified`; `Active` |
| 2 | **Classification** | Exactly one classification probe per device; determines CI class; first phase that uses credentials | `Classified`; `Active, couldn't classify` |
| 3 | **Identification** | Identity probe/pattern collects serial, name, IP, MAC → identifier rules decide update vs create → IRE writes the CMDB | `Identified CI`; new CI; `Identified, ignored extra IP` |
| 4 | **Exploration** | Exploration probes/patterns from the classifier's *Triggers Probes* enrich the CI | `Updated CI` |

Failure signatures: `Active, couldn't classify` = credential/protocol/port problem at step
2; a device that classifies but never reaches `Identified CI` = identity probe or IRE
problem at step 3.

**Pattern variant:** the trigger probe can be the **Horizontal Pattern probe**; pattern
operations cover **both** identification and exploration, and probes/sensors are not used.

---

## 3. Configuration surfaces

### 3.1 Subscription, roles, and entry points

- Discovery requires a separate subscription; the plugin must be requested/activated.
- `discovery_admin` grants configuration/execution access. `admin` also works for most
  procedures. IRE rule work needs `itil_admin`; class creation also uses
  `personalize_dictionary`; identification simulation and some class operations need
  `admin`; CI Class Manager full access is `sn_cmdb_admin`, read-only `sn_cmdb_editor`.
- Entry points (release labels vary):
  - `All > Discovery > Discovery Schedules`
  - `All > Discovery > Discovery Log`
  - `All > Discovery > MID Servers`
  - `All > Discovery > Discovery Definition > Properties`
  - `All > Configuration > CI Class Manager`
  - `All > Configuration > Identification/Reconciliation > Identification Simulation`
  - `All > Configuration > Identification/Reconciliation > IRE Data Source Rule`
  - `All > Configuration > CMDB Properties > Identification/Reconciliation Properties`
  - `All > Configuration > Identification Logs`
- Navigator-label variance: the Discovery learning guide uses
  `All > Discovery > Discovery Definition > Schedules`, `All > Discovery > Credentials`,
  and `All > Discovery > Properties` / `discovery_private_properties.list`; Brazil product
  docs use `Discovery Schedules` and `Discovery Definition > Properties`. Both are
  documented; use the path your release displays. The underlying object is the same.

### 3.2 MID Server

- The MID Server **polls the instance** for work, executes probes/patterns, and returns
  results. It does not retain discovery data.
- All communication is initiated from inside the firewall over SOAP/HTTPS; no inbound
  firewall rule or VPN is required.
- Install **two or more** initially, on different schedules/ranges.
- Assign the **Discovery** application or **ALL** (mandatory since Istanbul).
- **Auto-Select selection sequence:** 1) MID with Discovery app + matching IP range; 2)
  MID with ALL + matching range; 3) if several, first `Up` (random among Up); 4) default
  MID Server for Discovery, then ALL; 5) `Paused`/`Upgrading` candidates. Auto-Select is
  **not supported with IPv6**.
- Cluster selection prefers the lowest `Order` value that is `Up`, falling back to
  `Paused`/`Upgrading`; cluster selection ignores default MID Server settings.
- A MID Server can belong to **one** cluster only (not one load-balancing + one failover).
- For load balancing, multiple domains, ACL-protected SNMP, or devices exposing two
  protocols, use **Discovery behaviors**.
- WMI caveat: traffic starts on port 135 but Windows negotiates unused high ports; a
  firewall that allows 135 but blocks high ports breaks identification/exploration of
  Windows devices.

### 3.3 Credentials

| Target | Credential location | Notes |
|---|---|---|
| Windows (WMI) | MID Server **service** account on a Windows host | Give it at least local administrator rights on targets. For multiple domains prefer PowerShell. |
| UNIX/Linux (SSH) | Instance credential record (`discoverycredentials`) | Key or password; privilege escalation if needed. |
| SNMP | Instance credential record | v1/v2c community or v3. |
| VMware vCenter | Instance credential record | Required for vCenter exploration. |
| Cloud | Instance/cloud account config | Service principals, roles, or SSM; see cloud-specific docs. |
| External vault | Credential alias / external storage | `com.snc.use_external_credentials=true` by default. |

- Credentials are stored in `discoverycredentials`; the MID decrypts with its own private
  key.
- **Order** matters (which credential is tried first); **affinity** prevents a credential
  being sprayed at unrelated devices; **aliases** filter which credentials a schedule may
  use.
- Discovery automatically determines which credential works for a device.
- Test before every broad run.

### 3.4 IP address space, range sets, exclusions

- A schedule scans only the ranges attached to it; a **range set** is a reusable group.
- Methods: IP address list, IP range, IP network in CIDR. **CIDR networks auto-exclude
  network and broadcast addresses.**
- **IPv6 is not supported for range or network definitions**, while an IPv6 address-list
  scan *is* available for Configuration-item schedules. That asymmetry surprises people.
- Excludes are per range-set; **global exclusions** apply across all schedules (CI, IP,
  network scans).
- **>500,000 excluded addresses cancels the discovery** and logs an error — on huge
  estates express scope as a small include set rather than "everything minus a lot."
- **IP service affinity** remembers which protocol/port succeeded for an address
  (`ip_service_affinity`), so subsequent runs try the working protocol first.
- `glide.discovery.enforce_unique_ips` controls whether an IP is cleared from other
  devices when reused. It is **not** a CI de-duplication control; default `false`.
- `glide.discovery.exclude_ip_sync_classes` (default `cmdb_ci_lb`) keeps the management
  IP of load balancers instead of substituting a NIC IP.
- **IPAM integration** can auto-create schedules; `glide.discovery.schedule_ipv4_limit`
  (default 65,536) and `glide.discovery.schedule_ipv6_limit` (default 20,000) bound
  auto-generated schedules.

### 3.5 Discovery schedule

| Field / control | What it does | Practical guidance |
|---|---|---|
| **Discover** | `Configuration items`, `IP addresses`, `Networks`, `Service`, `Serverless`, `Cloud application`, `Cloud resources`, `Certificates` | For CMDB CI population use **Configuration items**. IP-address scans do **not** update the CMDB. |
| **MID Server selection method** | Auto-Select, Specific MID Cluster, Specific MID Server, Use Behavior | Start with Auto-Select; use Behavior for multi-domain/load balancing. |
| **Max run time** | Cancels remaining tasks at the limit | Set a window matching change/ops constraints. |
| **Max Idle time** | Cancels stalled runs when no ECC records are processing | Hidden by default; add the column to `discovery_schedule` to use it. |
| **Shazzam batch size** | IPs per Shazzam probe; default 1000 | Minimum effective 256; larger batches reduce overhead but delay classification. |
| **Shazzam cluster support** | Distributes Shazzam across cluster members | Works with batch size; probes run sequentially per MID Server. |
| **Use SNMP Version** | ALL / v1 / v2c / v3 | Pin the version when the network requires it. |
| **Quick ranges** | Inline IP/range/list entry | Good for pilots; move to range sets for reuse. |
| **Active** | Enables the schedule | Inactive schedules can still be run manually. |
| **Location** | Assigns location to discovered CIs | Empty = no location. |
| **Log state changes** | Logs every device state transition | Useful during tuning, noisy in steady state. |
| **Discovery Agent** | MID / AWS MID | Only appears when `glide.discovery.enable_ssm` is on and Discover = Configuration items following a Cloud Resources schedule. |

**Run options:** On Demand (default), Daily, Weekly, Monthly, Periodically, Once,
Weekdays, Weekends, Month Last Day, Calendar Quarter End, **After Discovery**.
`After Discovery` chains schedules; `Even if canceled` decouples the chain from the
upstream result.

**Concurrency guard:** `glide.discovery.max_concurrent_invocations_per_schedule`
(default **3**) prevents a slow schedule from stacking unbounded runs. `0` or negative
disables the guard; it does not apply to "Run after = Even if canceled".

Related lists: **IP Ranges**, **Discovery Range Sets**, **Discovery Status**, **Global IP
Exclusion**, **Discovery Attributes** (per-schedule/range CI field values, e.g. location).

### 3.6 Behaviors (multi-MID orchestration)

A behavior assigns **functionalities** (protocol sets) to MID Servers, grouped by a
numeric **phase**. Use it for:

- load balancing across MID Servers;
- multiple Windows domains;
- SNMP devices protected by an ACL that only some MID Server hosts satisfy;
- devices that expose both SSH and SNMP, where you want to force one protocol.

A functionality record links: functionality definition (protocols), MID Servers, phase,
and optional criteria (`mid_server`, `win_domain`, `mid_win_domain`). Criteria are
required only for Windows MID Servers in multi-domain scenarios.

Common functionality definitions: **Windows only (WMI)**, **Windows, DNS, and WINS**,
**SNMP only**, **All except SNMP**, **All except Windows (no WMI)**.

A behavior **must have at least one functionality**, otherwise it does not work properly.
Quick Discovery checks all credentials; a behavior checks only the defined port probes.

### 3.7 Configuration Console and File-Based Discovery (FBD)

The **Discovery Configuration Console** (`All > Discovery > Discovery Definition >
Configuration Console`; role `admin`) is the toggle-based front end for which CI types and
information Discovery collects, including **File-Based Discovery (FBD)**.

FBD is a Discovery feature, **not one of the four IRE rule families**. It runs during the
**Exploration** phase and records software found on disk:

| Object | Purpose |
|---|---|
| `cmdb_file_information` | Files FBD kept: name, size, version, path, CI reference |
| `samp_file_name` | Vendor-maintained allow-list of file names (synced from Content Data Service) |
| `samp_custom_file_name` | Your additions for software the vendor list does not know |
| `cmdb_sam_sw_install` | Software installation records, including FBD-sourced installs |
| `cmdb_unidentified_file_set` | Files kept but matched no known product |
| `cmdb_swid_tag` | SWID tags, when enabled in the console |

Key properties: `glide.discovery.file_discovery.wildcard.windows` (additive extensions)
and `glide.discovery.file_discovery.blacklist.windows` (hard filter). Default FBD
frequency is **Monthly**; FBD does not run until the initial Content Data Service sync
(about 24 hours) completes. Plugin: `com.snc.discovery.file_based_discovery`.

### 3.8 Classifiers, patterns, probes, sensors

- A **classifier** tells Discovery which probe(s) to run for identification and
  exploration, or which Horizontal Pattern probe to launch. Classification happens after
  the Shazzam scan and before identification/exploration.
- Three classification types:
  - **Device** — Windows/UNIX/Linux computers, routers, switches, load balancers; triggers
    identification/exploration probes; can use HTTP classification as a lower-priority
    fallback.
  - **Process** — applications based on running processes; runs during exploration;
    creates child CIs with `Runs on::Runs`; process handlers filter inconsistent
    parameters to avoid duplicate application CIs.
  - **IP address (IP scan)** — credential-less scan by open ports/banners; updates CIs
    without identifiers.
- Classifier **criteria** are `parameter operator value`; process-classifier condition
  filters are case-sensitive.
- **HTTP classification fallback (Madrid+):** activates only if Shazzam sees 80/443 open
  and higher-priority WMI/SSH/SNMP probes fail.
- **Patterns** are NDL operations that collect/process data and update the CMDB. When a
  pattern is used, Discovery does **not** use the identity probe; it uses the identifier
  rule for the CI type specified by the pattern.
- Keep out-of-the-box classifiers unless adding a CI type Discovery does not classify.
  Debug with `glide.discovery.debug.classification=true` (add to `sys_properties`).
- Prefer patterns for new work; they unify identification + exploration. Patterns need
  both host credentials and **applicative credentials** to see applications.

### 3.9 Discovery properties (comprehensive)

Location: **`Discovery Definition > Properties`**, or **`sys_properties`** for properties
not shown there. Defaults are quoted as documented; new-vs-upgraded instances sometimes
differ (noted).

#### Identity, IP, and hostname

| Property | Type | Default | Effect / when to change |
|---|---|---|---|
| `glide.discovery.use_cmdb_identifiers` | true/false | `true` | Routes identification/reconciliation through CMDB IRE. Keep true unless documented legacy reason. |
| `glide.discovery.enforce_unique_ips` | true/false | `false` | Clears an IP from other devices when reused. Enable only if IP uniqueness is a hard invariant; can erase legitimate shared/VIP data. |
| `glide.discovery.exclude_ip_sync_classes` | string | `cmdb_ci_lb` | Classes whose IP is not substituted by a NIC IP. |
| `glide.discovery.ip_service_affinity` | true/false | `false`; new Zurich/Brazil `true` | Remembers the successful protocol/port per IP. Enable for mixed SSH/SNMP environments. |
| `glide.discovery.hostname.always_update` | true/false | `true` | Updates host name with the newest trusted value; can overwrite hand-entered values. Probe-based only. |
| `glide.discovery.hostname.case` | choice | `Lower case` | Upper/No change also available. |
| `glide.discovery.hostname.dns_nbt_trusted` | true/false | `true` | Trusts DNS/NetBIOS names. Do not use DNS names for Linux/AIX/Solaris patterns. |
| `glide.discovery.hostname.include_domain` | true/false | `false` | Include domain in hostname. Same Linux/AIX/Solaris caveat. |
| `glide.discovery.hostname.snmp_trusted` | true/false | `false`; new Zurich/Brazil `true` | Trusts SNMP names. |
| `glide.discovery.hostname.ssh_trusted` | true/false | `false`; new Zurich/Brazil `true` | Trusts SSH names. |
| `glide.discovery.hostname.wmi_trusted` | true/false | `false`; new Zurich/Brazil `true` | Trusts WMI names. |
| `glide.discovery.domain.name.nbt` | true/false | `true` | Windows domain from NBT vs WMI. |
| `glide.discovery.fqdn.regex` | string | `^([^.]+)\.((?:[^.]+\.)+[^.]+)$` | FQDN host/domain parsing regex. |
| `glide.discovery.enable_mac_address_verification` | true/false | `false` | Stops processing an IP if the device's MAC changed mid-run. |
| `glide.discovery.source_name` | string | `ServiceNow` | Source written to `sys_object_source` / `discovery_source`. Change only for coexistence/migration. |
| `glide.discovery.debug.ci_identification` | true/false | `false` | Writes CI identification debug to the CI Identification Log. Time-box it. |

#### Network discovery and scanning

| Property | Type | Default | Effect |
|---|---|---|---|
| `glide.discovery.bgp_router_disable` | true/false | `true` | Skips BGP routing exploration (large tables, OOM risk). |
| `glide.discovery.debug.network_discovery` | true/false | `true` | Verbose network discovery logging. |
| `glide.discovery.discoverable.network.max.netmask.bits` | integer | `28` | Ignores very small regular networks; 1–32 valid. |
| `glide.discovery.network_owner_method` | choice | `Most Networks` | Chooses which router owns an IP network. |
| `glide.discovery.physical_interface_types` | string | `6,117,9,71,209` | Interface types treated as physical. |
| `glide.discovery.switch_interface_types` | string | `7,8,9,26,53,62,69,71,78,115,117,209` | Interface types treated as switch ports. |
| `glide.discovery.virtual_interface_types` | integer/string | `53` | Interface types considered virtual. |
| `glide.discovery.L3_mapping` | true/false | `true` | Maps servers/network gear to routers and L3 switches. |
| `glide.discovery.network_discovery.functionality` | string | `SNMP only` | Functionality used for network discovery. |
| `glide.discovery.shazzam_simplify_ranges` | true/false | `true` | Removes duplicate IPs across ranges in a single-behavior schedule. |
| `glide.discovery.shazzam_ranges_json` | true/false | `true` | JSON-encodes Shazzam ranges to reduce payload size. |
| `glide.discovery.allow_loopback_adapters` | true/false | `false` | Discovers loopback adapters on SNMP devices. |

#### Scheduling, sensors, and throughput

| Property | Type | Default | Effect |
|---|---|---|---|
| `glide.discovery.max_concurrent_invocations_per_schedule` | integer | `3` | Caps stacked runs of the same schedule. |
| `glide.discovery.schedule_ipv4_limit` | integer | `65,536` | Max IPv4 addresses in an auto-generated schedule. |
| `glide.discovery.schedule_ipv6_limit` | integer | `20,000` | Max IPv6 addresses; older releases cap at 5,000. |
| `glide.discovery.schedule.autogenerate.group` | string | empty | Groups auto-generated IPAM schedules by tag/attribute. |
| `glide.discovery.schedule.autogenerate.debug` | true/false | `false` | Detailed IPAM schedule logging. |
| `glide.discovery.schedule_monitoring.stale_check_seconds` | integer | `1200` | Seconds without update before a status is stale. |
| `glide.discovery.schedule_monitoring.dry_run` | true/false | `false` | Log monitoring decisions without changing state. |
| `glide.discovery.schedule_monitoring.schedule_types_to_monitor` | string | `CIs` | Which schedule types to monitor. |
| `discovery.use.event.processing` | true/false | `false` | Uses Event Framework for sensor/cloud jobs. |
| `discovery.event.separate.cloud.events` | true/false | `true` | Separates cloud and IP sensor queues when event processing is on. |
| `discovery.event.pin.jobs` | true/false | `false` | Pins event processors to nodes; `false` can increase throughput. |
| `com.glide.queue.discovery.sensors.processing_jobs.priority` | integer | `100` | Lower value = higher priority. Also seen as `glide.queue.discovery.sensors.processing_jobs.priority`. |
| `com.glide.queue.discovery.cloud.sensors.processing_jobs.priority` | integer | `100` | Same, cloud path. |
| `glide.discovery.sensors.save_attachments` | true/false | `true` | Keeps ECC attachments for inspection. |
| `glide.discovery.use_probe_results_cache` | true/false | `false` | Skips sensor processing when probe results are unchanged. |
| `glide.discovery.active_processes_filter` | true/false | `false` | Filters running processes to those matching process classifications. |
| `glide.discovery.perf.metrics.enable_collection` | true/false | `true` | Collects Discovery performance metrics. |
| `glide.discovery.perf.metrics.rollup_by_build` | true/false | `true` | Roll-up grouping. |
| `glide.discovery.perf.metrics.rollup_by_status` | true/false | `true` | Roll-up grouping. |
| `glide.discovery.perf.metrics.rollup_by_target` | true/false | `true` | Roll-up grouping. |
| `glide.eccprobe.max_queued_probes_per_run` | integer | `20` | Caps probes a node picks up per run. |
| `glide.eccprobe.awsrestprobe.max_retries` | integer | `4` | Exponential backoff for AWS rate limits (max 10). |
| `glide.eccprobe.awsrestprobe.max_wait` | integer | `30` | Max retry wait (max 2046 s). |
| `glide.codesigning.tracking.unsupported_script_tracking.enabled` | true/false | `true` | If true and code signing is on, unsupported scripts are not notarized and Cloud Discovery can fail; set false to enable Cloud Discovery on code-signed instances. |
| `glide.discovery.log_message_length` | integer | `200` | Discovery Log message cap; `0`/negative disables. Also seen as `glide.discovery.log_message_chars`. |
| `glide.discovery.log_debug_info` | true/false | `false` | Adds ECC-derived debug to the Discovery log. |
| `glide.discovery.save_pattern_log` | string | `true` | Saves pattern logs; false reduces DB writes, but failures always save. |

#### Exploration, software, events, cloud

| Property | Type | Default | Effect |
|---|---|---|---|
| `glide.discovery.application_mapping` | true/false | `true` | Enables ADM; disabling stops relationship creation, not probes/classification. |
| `glide.discovery.enable_adme` | true/false | `false` | Enhanced ADM probe with fallback. |
| `glide.discovery.adm.update.applications` | true/false | `true` (Tokyo+ new installs) | Marks application CIs absent/installed based on running process. Must be added manually after upgrade. |
| `glide.discovery.discover_software` | true/false | `true` | Enables software package discovery. |
| `glide.discovery.enable.software_filter` | true/false | `true` | Windows software filtering. |
| `glide.discovery.software_filter_keys` | string | `Language Pack, Hotfix Security Update` | Names containing these are filtered. |
| `glide.discovery.enable.software_simplify` | true/false | `true` | Normalises names/versions; disabling can create duplicate software records. |
| `glide.discovery.enable.software_simplify_sccm` | true/false | `false` | Aligns software names with SCCM. |
| `glide.discovery.software_sccm_managed` | true/false | `false` | Suppresses software for SCCM-managed computers. |
| `glide.discovery.populate_software_instance_table` | true/false | `false` | Legacy SAM table population. |
| `glide.discovery.sam_batch_update_size` | integer | `100` | Batches `cmdb_sam_sw_install` updates where only `last_scanned` changed. |
| `glide.discovery.enable_file_tracking` | true/false | `true` | Tracks configuration files found by patterns. |
| `glide.discovery.file_tracking.max_file_size` | integer | `500000` | Per-file cap. |
| `glide.discovery.file_tracking.max_files_per_ci` | integer | `50` | Per-CI cap. |
| `glide.discovery.file_tracking.change_limit_count` | integer | `4` | Changes allowed per window. |
| `glide.discovery.file_tracking.change_limit_days` | integer | `7` | Window length. |
| `glide.discovery.file_discovery.wildcard.windows` | string | — | Additive FBD extensions. |
| `glide.discovery.file_discovery.blacklist.windows` | string | — | Hard FBD file filter. |
| `glide.discovery.mark_esx_servers_as_absent` | true/false | `false` | Absent instead of retired when missing from payload. |
| `glide.discovery.retire_stale_accounts` | true/false | `false` | Cleans stale cloud service account references. |
| `glide.discovery.warn_minor_version` | true/false | `false` | Warn on minor version mismatch. |
| `glide.discovery.roundingInterval.cpu` | integer | `1` MHz | CPU speed rounding. |
| `glide.discovery.roundingInterval.ram` | integer | `1` MB | RAM rounding. |
| `glide.discovery.discover_aws_ec2_host_metadata` | true/false | `true` | AWS metadata probes during IP discovery. |
| `glide.discovery.discover_azure_host_metadata` | true/false | `true` | Azure metadata probes. |
| `glide.discovery.sensors.fire_ssh_probe` | true/false | `true` | SSH probe fallback when LB VIPs are missing from SNMP payload. |
| `glide.discovery.enable_ssm` | true/false | `false` | AWS SSM-based discovery. |
| `glide.discovery.ssm.enable_windows` | true/false | `false` | SSM on Windows. |
| `glide.discovery.multi_page_serial_mode` | true/false | `false` | Processes multi-page pattern payloads serially; documented fix for duplicates from multi-page payloads. |
| `com.snc.use_external_credentials` | true/false | `true` | External credential storage. |
| `glide.discovery.certs.*` | various | — | Certificate Inventory and Management: renewal tasks, incidents, Slack channel, CSR generation. |

**Community-reported, not in the primary property reference (verify before use):**
`glide.discovery.ire_err_exclusion_list` (suppresses IRE errors in the pattern log; OOB
list includes `ABANDONED, INSERT_FAILED, UPDATE_FAILED, NO_IDENTIFIER_KEYS_GENERATED` —
`NO_IDENTIFIER_KEYS_GENERATED` masks silent CI creation failures).

### 3.10 Deletion strategy (patterns only)

When a pattern finds the main CI but not a related CI, the related CI's deletion strategy
in **Related CI Types `[sa_ci_to_pattern]`** applies:

| Strategy | Behavior |
|---|---|
| **Keep** (default) | Preserve the record; no changes. |
| **Delete** | Delete the related CI and its relationship. |
| **Mark as absent** | Set `install_status=Absent`; does not delete. Exception: `cmdb_ci_network_adapter` and `cmdb_ci_ip_address` are deleted when marked absent. |
| **Delete relations** | Delete only the relationships. |
| **Mark as retired** | Set `install_status=Retired`; does not delete. |

Limits: not available for probes/sensors; cannot set a strategy on the **main CI** for
Infrastructure pattern types; main CIs can be deleted only for Application or Cloud
Resource patterns; does not apply to **related entries**.

### 3.11 Domain separation, retired CIs, post-clone

- Discovery schedules enforce domain separation; MID Servers available to a schedule are
  limited to the schedule owner's domain.
- Reconciliation rules can be scoped by domain; child domains inherit parent rules unless
  overridden.
- **Domain separation and duplicates:** servers in different domains with the same
  Correlation ID are considered unique, not duplicates (by design).
- **Retired CI status (KB0755747):** Discovery does not override the Retired status and
  restore a CI to Operational when rediscovered. To auto-update, create a Business Rule on
  `cmdb_ci`: `before` / `update` / condition "Most recent discovery changes" AND
  "Operational Status is Retired" / script sets `operational_status` to Operational.
  Warning: setting Operational also sets Status/Hardware Status to Installed.
- After a clone, revalidate MID Server URLs, credentials, capability assignments, cloud
  accounts, and schedules. Treat the clone as a new deployment.

---

## 4. CI Class Manager — breadcrumbs and tab map

**Primary navigation:** `All > Configuration > CI Class Manager`.
(Some topics say `All > CI Class Manager`; both land on the same module.)

CI Class Manager is the central place to view/create/edit class definitions and the
settings for **identification, reconciliation, dependencies, and CMDB Health**. It does
**not** support non-CMDB tables.

### 4.1 Screen map

| Bread crumb | What you configure |
|---|---|
| **CI Class Manager → Hierarchy** | Expand the CI class tree; select the class to edit. |
| **Class Info** | Basic info, attributes, suggested relationships, CIs of the class, dependency-view icons, delete CIs, principal-class filter. |
| **Class Info → Identification Rule** | Identifier entries, priorities, inclusion rules, Dynamic IRE. |
| **Class Info → Reconciliation** | Static reconciliation rules, data refresh rules, reconciliation definitions. |
| **Class Info → Dependencies** | Dependent relationship rules (hosting/containment). |
| **Class Info → Health** | Compliance audits, certification templates, orphan/staleness rules, recommended/mandatory attributes, health inclusion rules. |
| **Class Info → Suggested Relationships** | Relationship suggestions used by Query Builder. |
| **Class Info → Service Mapping** | Entry point types and CI types for Service Mapping/Discovery. |

**IRE Data Source Rules are not a CI Class Manager tab.** They are class-level and live
outside the tool at `All > Configuration > Identification/Reconciliation > IRE Data Source
Rule` (the CMDB learning guide calls the navigator entry **Data Sources**).

### 4.2 Roles (per task, as documented)

| Task / scope | Role requirement |
|---|---|
| General access to CI Class Manager | `sn_cmdb_admin` full; `sn_cmdb_editor` read-only |
| Creating a CI class | `sn_cmdb_admin` or `itil_admin`, plus `personalize_dictionary` |
| Creating a CI class (full access) | `sn_cmdb_admin` or `admin` |
| Dependent relationship rules (read) | `sn_cmdb_editor` and `itil` |
| Dependent relationship rules (full) | `sn_cmdb_admin` and `itil_admin` |
| Containment rule groups | `sn_cmdb_admin` or `admin` |
| Identification simulation | `sn_cmdb_admin` or `admin` |

### 4.3 Creating a child class (wizard order)

1. **Provide Basic Info** — display name (≤80 chars, unique), table name (auto-prefixed
   `u_cmdb_ci`; lowercase alphanumeric + underscore; ≤80 chars), description, icon,
   extensible, principal class.
2. **Add Attributes** — add columns; double-click the attribute's **Identification Rule**
   cell and set it to `true` to designate a CI identifier.
3. **Set Identification Rule** — review the **Derived identification rule** and its
   identifier entries; click **Replace** to define class-specific entries.
4. **Dependencies** — add dependent rules (tab appears only when dependent identification
   rules exist).
5. **Add Reconciliation Rules** — add Reconciliation Rules and Data Refresh Rules. If
   skipped, no source is authorized to update the class.
6. **Add Suggested Relationships** — review/add relationship type + target class.
7. **Done**.

Precondition: the parent class must have **Is Extendable** checked. Metadata Editor and
CI Class Manager are synchronised for dependent rules.

### 4.4 Related screens outside the tool

| Task | Path |
|---|---|
| Identification simulation | `All > Configuration > Identification/Reconciliation > Identification Simulation` |
| IRE Data Source Rules (insert gate) | `All > Configuration > Identification/Reconciliation > IRE Data Source Rule` |
| Identification inclusion rules list | `All > Configuration > Identification/Reconciliation > Identification Inclusion Rules` |
| CMDB IRE properties | `All > Configuration > CMDB Properties > Identification/Reconciliation Properties` |
| Discovery properties | `All > Discovery > Discovery Definition > Properties` |
| Metadata Editor (hosting/containment groups) | `All > Configuration > Metadata Editor` |
| Reconciliation definitions list | `All > Configuration > Identification/Reconciliation > Reconciliation Definitions` |
| Duplicate CI Remediator properties | `Configuration > CMDB Properties > Duplicate CI Remediator Properties` |

---

## 5. IRE deep dive

### 5.1 The pipeline

```
payload item
   │
   ├─ (fast path) source_name + source_native_key in sys_object_source_info
   │        OR
   ├─ identification rule matching on criterion attributes
   ▼
identified? ── no ──► insert (if allowed by IRE data source rule)
   │ yes
   ▼
reconciliation (update only)
   ├─ static rules: source priority per class/attribute
   ├─ dynamic rules: value-based via CMDB 360 (takes precedence)
   └─ data refresh: staleness allows a lower-priority source to write
   ▼
commit to CMDB
```

**IRE only reconciles updates.** When it inserts a new CI, reconciliation is not applied.
A blocked insert logs `INSERT_NOT_ALLOWED_FOR_SOURCE`.

### 5.2 The four rule families — canonical terminology

| Mechanism | Exact name | Question it answers | Insert | Update | Configuration level |
|---|---|---|---|---|---|
| **Identification Rule** | Identification Rule (IRE identifier) | "Does this CI already exist?" | **YES** — no match creates | **YES** — match updates | Class → identifier entry → attributes |
| **IRE Data Source Rule** | IRE Data Source Rule | "Can this source create a new CI of this class?" | **YES — gate** (may block) | **NO** — cannot block updates | Class + source; not attribute-level |
| **Reconciliation Rule** | Reconciliation Rule | "Which source may update this attribute?" | **NO** | **YES** — after match | Class + source + attribute |
| **Data Refresh Rule** | Data Refresh Rule (staleness rule) | "Has the higher-priority source's data gone stale?" | **NO** | **YES** — after reconciliation | Class + source + refresh criteria |

**Order of application:** 1) Identification; 2) if match → Reconciliation, then Data Refresh
can let a lower-priority source refresh a stale field; 3) if no match → IRE Data Source Rule
decides whether the source may insert. Reconciliation and Data Refresh are skipped entirely
on insert.

**Boundaries:** an IRE Data Source Rule is a **create-only** gate; it cannot restrict which
attributes an allowed source updates, and cannot block updates to an existing CI.
Reconciliation and Data Refresh are **update-only**.

**Adjacent mechanisms — not one of the four families:** Identification Inclusion Rule
(scoping filter), Reclassification (class-change control), De-duplication Task (output of
duplicate detection), Dynamic IRE / dynamic reconciliation (extension of Reconciliation),
Partial/incomplete payloads (processing outcome).

**Do not conflate** an IRE Data Source Rule with the CI field `discovery_source` /
`sys_object_source`. The rule gates inserts; the field records which source last wrote the
CI. A blocked source can still be the `discovery_source` of an update.

### 5.3 Identification Rules (IRE identifiers)

**Anatomy:** one CI identifier per rule; one or more identifier entries (unique attribute
sets) with different priorities; optional related entries; `Applies to` class; required
attributes cannot be empty; criterion attributes are the unique attribute sets used for
matching.

**Types:**

| Type | Meaning | Guidance |
|---|---|---|
| **Independent** | Identifies a CI from its own attributes | Prefer this. Model CIs with a complete independent key. |
| **Dependent** | Requires identifying a parent/dependent CI and the relationship first | Use only when the CI cannot exist alone (NIC, app on host). Minimize; two dependency levels is the maximum supported. |

**Identifier entry types:**

| Entry type | Matching fields come from | Guidance |
|---|---|---|
| **Regular** | The CI's own table (or inherited `cmdb_ci` fields) | Preferred; cheapest and least ambiguous. |
| **Lookup** | A related table that references the CI (e.g. `cmdb_ci_network_adapter` for MAC) | Costs a join; use only when the identifying attribute genuinely lives on the related table. If lookup records don't exist, IRE inserts them. |
| **Hybrid** | Both the CI table and a related table | Use when neither source alone is unique (e.g. duplicate VM serials). |

A single rule can mix Regular, Lookup, and Hybrid entries, each with its own priority.
Lookup entries can impact performance and are explicitly discouraged when a Regular entry
is sufficient. Prefer **Enforce exact count match (Lookup)** for stronger matching.

**Priority rules:** lowest `Order` runs first; custom identifiers must use a different
order from defaults; put the **strongest** identifier entry first; limit entries ideally to
**one**; disable a rule rather than deleting it; ensure the rule is at the correct class
level.

**Default rules in the base system:**

| Rule | Applies to | Attributes |
|---|---|---|
| Hardware Rule | `cmdb_ci_hardware` | `serial_number`, `serial_number_type`, `name`, `ip_address`, `mac_address`; plus Serial Number and Network Adapter lookup tables |
| ESX Server Rule | `cmdb_ci_esx_server` | `correlation_id` |
| Storage Server Rule | `cmdb_ci_storage_server` | `cim_object_path`, `name`, serial fields, `mac_address`, `ip_address`; plus lookups |
| WBEM Service Rule | `cmdb_ci_wbem_service` | `cim_object_path` |

Do not add `sys_class_name` as an attribute for an independent rule such as Hardware. If
matching depends on class, create a rule per class and set `Applies to`.

**Inheritance trap:** a child class **derives** the parent's rule — including related
entries — unless you create a rule at the child. Creating one **replaces the derived rule
entirely**, so re-add any related entries you still need.

**Operational rules:**
- Custom identifiers must use different `Order` values from defaults; Discovery parses
  low → high. Disable with `Active=false` rather than deleting.
- Bonded/teamed NICs share IP and MAC; adding `name` distinguishes interfaces — but
  **renaming an adapter breaks matching**: Discovery marks the old CI `Install Status =
  Absent` and creates a new one.
- **Serial numbers are integrity-critical.** Verify custom probes/sensors/patterns still
  return serials and never reformat them (no custom prefixes).
- **Never** define a lookup-based identifier for a child table in a parent's rule *and* a
  class-level identifier for that child — the two contradict and produce duplicates.

**Identification Inclusion Rules** narrow which existing CIs participate in identification
and in the CMDB Health duplicate metric. They affect every script that calls IRE, so apply
them narrowly. **Critical pitfall:** do not use "Class" as a condition on a parent class
table like `cmdb_ci_hardware` — child classes not named are not found by IRE, causing
duplicates. Filter on attributes/status instead. Base system has none.

### 5.4 Reconciliation Rules (update-only)

**Purpose:** after Identification matches an existing CI, decide **which source may update
which attribute**. Reconciliation is **update-only**; it is not applied when IRE inserts.

| Type | Basis | Precedence | Requirements |
|---|---|---|---|
| **Static** | Source priority per class/attribute | Lower than dynamic for the same attribute | A rule per authorized source/attribute; stored in `cmdb_reconciliation_definition` |
| **Dynamic** | Attribute values processed by CMDB 360 (largest/most-reported) | **Wins** over static for the same attribute | CMDB 360 must be enabled; one dynamic rule per class attribute; stored in `cmdb_dynamic_reconciliation_definition` |

**Precedence, in the order that actually bites:**
1. **Dynamic beats static** for the same attribute.
2. **A rule that lists specific attributes beats a rule with an empty Attributes field
   ("all attributes") — regardless of discovery-source priority.** A lower-priority source
   with an explicit attribute list can block a higher-priority source.
3. **Child-class rules beat parent-class rules** (including derived rules).
4. Between two rules for the same attribute at the same class level, **priority** decides.
5. Rules authorising different sources for the same attribute **coexist**; IRE prevents
   overwrites using Data Source History (`cmdb_datasource_last_update`).
6. Empty-field updates are governed by `glide.reconciliation.override.null` (default `true`).
7. **Insert is not gated by reconciliation**; use IRE Data Source Rules for that.
8. With Domain Separation, rules are domain-scoped; parent-domain rules apply to child
   domains unless overridden.
9. **Reconciliation is evaluated against the class in the input payload**, not the class
   the CI currently lives in. A missing reconciliation rule for the payload class can cause
   an unintended class downgrade and attribute update.
10. IRE checks `cmdb_datasource_last_update` during reconciliation — a common reason rules
    "don't seem to work."

Per-rule fields: `Active`, `Discovery source`, `Priority`, `Apply to all attributes` vs an
explicit `Attributes` list, `Update with Null`, and `Filter Condition`. A rule with
`Update with Null` can set listed attributes to null; without it, a source cannot null out
a populated field. `Filter Condition` scopes the rule to a row subset;
`glide.identification_engine.enable_reconciliation_filter_before_update` (default `false`)
controls whether the filter runs before or after values change. You cannot create a
reconciliation rule for system fields or IRE-specific fields such as `discovery_source`,
and rules cannot be dot-walked through reference fields.

Practical guidance: **always list attributes explicitly** rather than leaving Attributes
empty, so a rule does what you meant when someone later adds a specific-attribute rule.

### 5.5 IRE Data Source Rules (insert-only)

**Purpose:** prevent a specific discovery/data source from **creating** new CIs of a class.
It is a **create-only gate**, not an attribute-level update restriction, and it does not
block updates to CIs that already exist.

- Stored in `cmdb_ire_data_source_rule`.
- Configuration: `All > Configuration > Identification/Reconciliation > IRE Data Source
  Rule` (guide shortens to **Data Sources**).
- Fields: **Active**, **Applies to** (CI class and children), **Data source**, **Insert Not
  Allowed**.
- Child classes inherit the rule; a child-class rule overrides the parent.
- Evaluated **only when identification found no match** and IRE is about to insert.
- Has no effect on updates. A source blocked from inserting can still update an existing
  CI, subject to Reconciliation Rules.
- Has no impact once **dynamic reconciliation** is in effect.
- A blocked insert logs `INSERT_NOT_ALLOWED_FOR_SOURCE`. With `CreateOrUpdateCIEnhanced()`
  the item is stored as a partial payload; `createOrUpdateCI()` does not allow partial
  commits, so the whole payload can fail.
- Does not apply to lookup or related items; only one rule can be active for a given
  class/source pair.

**Example:** an IP-scan tool that discovers network gear but creates thin server CIs. Block
that source from inserting `cmdb_ci_server`; it can still update server CIs Discovery
already created.

### 5.6 Data Refresh Rules (update-only, staleness)

**Purpose:** let a lower-priority source refresh a field when the higher-priority source's
data has gone **stale**. Data Refresh is **update-only**; it never applies to a new insert.

- Where: `All > Configuration > CI Class Manager > Hierarchy > <class> > Class Info >
  Reconciliation Rules > Data Refresh Rules > Add`, with fields: **Discovery source**,
  **Effective Duration**, **Active**. (The learning guide describes the same behavior as
  **Refreshable** + **Stale threshold** on a reconciliation rule.)
- **Effective Duration / Stale threshold = 0** (default) means the CI is immediately stale
  for that source, so a lower-priority source is always authorized to refresh.
- The refresh can only write fields the lower-priority source is authorized to update by
  Reconciliation Rules.
- Data Refresh has **no effect** when dynamic reconciliation rules are in effect.
- Field-specific rules are safer than "Apply to all": staleness on `name` should not block
  a refresh of `serial_number`.
- Avoid ping-pong between two sources alternately refreshing each other. Use strict
  priority for identity fields and staleness-aware refresh only for non-identifying
  attributes.
- Non-CMDB tables: the same concept is configured in `cmdb_datasource_staleness.list` with
  `Applies to`, `Data source`, `Effective Duration`.
- Staleness is evaluated against Data Source History (`cmdb_datasource_last_update`), not
  just `sys_updated_on`.

**Three different "stale" mechanisms — do not mix them up:**

| mechanism | question it answers | where | effect |
|---|---|---|---|
| **Data refresh rule** | has *this discovery source* stopped refreshing this CI? | CI Class Manager → Reconciliation Rules → Data Refresh Rules | allows lower-priority sources to update (static reconciliation only) |
| **CMDB Health staleness rule** | what % of this class is stale (correctness KPI)? | CI Class Manager → Health → Correctness → Staleness Rule | reporting only; changes no data |
| **CMDB Data Manager policy** | should this CI be retired/archived/deleted? | CMDB Workspace → Data Manager | lifecycle action on the CI |

The health staleness rule's Effective Duration is based on `sys_updated_on`; "the Discovery
setting of certain types of CIs as stale takes precedence over a CMDB Health staleness
rule" — so a CI can look stale in health reporting while Discovery is actually refreshing
it (unchanged data means no write, so `sys_updated_on` does not move).

### 5.7 Reclassification

IRE can upgrade, downgrade, or switch a CI's class when a match is found. Controls:

- `glide.class.upgrade.enabled` / `glide.class.downgrade.enabled` /
  `glide.class.switch.enabled` (default `true`)
- `glide.identification_engine.update_without_upgrade_enabled` /
  `...update_without_downgrade_enabled` / `...update_without_switch_enabled` (default
  `false`) — when true, process the update but skip reclassification for that direction;
  these take precedence over `glide.class.*.enabled`.
- `glide.identification_engine.reclassification_restriction_rules_enabled` (default
  `true`) — apply active reclassification restriction rules.
- Payload `settings` flags `updateWithoutUpgrade`, `updateWithoutDowngrade`,
  `updateWithoutSwitch` take precedence over system settings.
- Automatic reclassification can be disabled, producing a **reclassification task**;
  review these — they batch silently otherwise.

### 5.8 Partial and incomplete payloads

- **Partial item:** lacks enough data for unique identification *but* has
  `source_name`/`source_native_key` or enough identifying context; stored in
  `cmdb_ire_partial_payloads` and retried when a later payload completes it. Identifier
  keys are stored in `cmdb_ire_partial_payloads_index`.
- **Incomplete item:** lacks unique identification and has a non-partial error; stored in
  `cmdb_ire_incomplete_payloads` for logging and never retried.
- Partial payloads older than **90 days** are deleted.
- `glide.identification_engine.partial_payload_items_max_size` (default **1000**) bounds
  one partial payload; larger payloads are split.
- `glide.identification_engine.partial_items_process_limit` /
  `...partial_items_process_absolute_limit` (default **2000 / 5000**) bound partial
  payload fetch per IRE call.
- `CreateOrUpdateCIEnhanced()` enables partial payloads, partial commits, payload
  de-duplication, and optional summaries. `createOrUpdateCI()` does not allow partial
  commits: one blocked insert can fail the whole payload.
- IRE errors for a partial item: `MISSING_MATCHING_ATTRIBUTES`,
  `REQUIRED_ATTRIBUTE_EMPTY`, `MISSING_DEPENDENCY`, `INSERT_NOT_ALLOWED_FOR_SOURCE`.

### 5.9 IRE properties

| Property | Default | Effect |
|---|---|---|
| `glide.identification_engine.skip_duplicates` | `true` | If duplicates < threshold: oldest is picked as match/main CI; others get `duplicate_of`. If false: matching fails with an error. |
| `glide.identification_engine.skip_duplicates.threshold` | `5` | Above this, identification treats duplicates as if skip were false. |
| `glide.identification_engine.skip_sys_object_source_matching` | not consistently documented (likely `false`) | False prefers the `sys_object_source` native-key fast path; true forces IRE identification rules. Set true when source attributes churn but native keys are stable. |
| `glide.identification_engine.skip_updating_source_last_discovered_if_older` | `true` | Stale source payloads don't roll back `last_discovered`/`discovery_source`. |
| `glide.identification_engine.skip_updating_last_scan_if_older` / `.ire_message_listener_skip_*` | `true / false` | Same for Source table `last_scan`. |
| `glide.identification_engine.lookup_match.create_duplicate_task_ci.enabled` | `false` | Create de-dup tasks for duplicate lookup-table related items. |
| `glide.identification_engine.non_dependency_relation.duplicate_detection` | `false` | Detect duplicate non-dependent relations in payload. |
| `glide.identification_engine.enable_identifier_optional_condition` | `false` | Enables Optional condition advanced filter on regular identifier entries. |
| `glide.identification_engine.enable_reconciliation_filter_before_update` | `false` | Apply reconciliation filter conditions before (not after) value change. |
| `glide.identification_engine.granular_insert_locking` | `true` | Multiple granular insert locks vs one global lock; set false on lock contention. |
| `glide.identification_engine.batch_update_last_discovered` / `.batch_update_last_discovered.use_execute_lazy` | `true / true` | Batch `last_discovered` updates; set both false for immediate consistency / deletion-race workarounds. |
| `glide.identification_engine.partial_payload_items_max_size` | `1000` | Cap items per partial payload. |
| `glide.identification_engine.partial_items_process_limit` / `.partial_items_process_absolute_limit` | `2000 / 5000` | Partial payload fetch limits. |
| `glide.identification_engine.reclassification_restriction_rules_enabled` | `true` | Apply reclassification restriction rules. |
| `glide.identification_engine.update_without_upgrade_enabled` / `...downgrade...` / `...switch...` | `false` | Skip reclassification for that direction. |
| `glide.identification_engine.dynamic_ire_enabled` | `true` on zBooted Zurich Patch 11+; upgraded may differ | Enables Dynamic IRE for Hardware and descendants. Variant spelling seen: `glide.identification_engine.dynamic_ire.enabled`. |
| `glide.identification_engine.dynamic_ire.auto_compare` | `true` | Comparison mode for Dynamic IRE. |
| `glide.cache.size.service_cache` | `20 MB` | Identification engine relation cache. |
| `glide.identification_engine.*_local_cache_count` | `15000 / 10000 / 100000` | Related / dependent / independent item caches; 0 disables. |
| `glide.cmdb.logger.source.identification_engine` | — | `info|warn|error|debug|debugVerbose`; heavy — scope narrowly. |
| `glide.identification_logs.max_run_ids` | `1000` | Max log runs in `Configuration > Identification Logs`. |
| `glide.required.attribute.enabled` | `true` | Required attributes may not be null during I&R. |
| `glide.reconciliation.override.null` | `true` | Lower-priority source may update an empty field. |
| `glide.duplicate_ci_remediator.dry_run` | `false` | Test remediation without writing. |
| `glide.duplicate_ci_remediator.max.cis` | `1000` (cap 5000) | Large-set threshold. |
| `glide.duplicate_ci_remediator.max.field_length` | `4000` | Excludes/truncates long attributes in remediation. |
| `glide.duplicate_ci_remediator.related_items_blacklist` | `cert_task.cmdb_ci,cert_audit_result.configuration_item,discovery_log.cmdb_ci,alm_hardware.ci,alm_asset.ci,fm_expense_line.ci` | Related tables excluded from merge. |
| `glide.duplicate_ci_remediator.merge_related_items_enhanced` | — | Ignore DB errors / skip workflows on related tables so remediation completes. |
| `glide.duplicate_ci_remediator.enable_restricted_mode` | `false` | Allows blocked remediation to proceed with limited related items. |

**Documented naming inconsistency — do not silently "fix" it.** ServiceNow's own pages
render the skip-duplicates family two ways: `glide.identification_engine.skip_duplicates`
and `glide.identificationengine.skipduplicates`. Check `sys_properties` on your instance
before setting either.

### 5.10 Identification Simulation

- `All > Configuration > Identification/Reconciliation > Identification Simulation`.
- Build a payload from a CI class (auto-adds required dependencies and valid structure) or
  paste an existing payload.
- Choose the **data source** (ServiceNow Discovery = `ServiceNow`).
- Optionally use **Enhanced Identification** (`identifyCIEnhanced`).
- **Run Simulation** → inspect Input / Logs / Output; adjust rules; rerun.
- Simulation **does not commit** to the CMDB.
- Use the IE/service-cache log levels to control verbosity.
- `Copy Script` copies the JSON; final execution uses `createOrUpdateCI()`.

### 5.11 Dynamic IRE

- `CI Class Manager > Hierarchy > Hardware > Class Info > Identification Rule > Dynamic IRE`.
- **Simulate Dynamic IRE** runs Static and Dynamic IRE in parallel and stores differences
  in `cmdb_ire_output_comparison_item`.
- **Commit to Dynamic IRE** makes Dynamic IRE the only identifier for Hardware and its
  descendants.
- **Change to IRE** switches back to Static IRE.
- Property: `glide.identification_engine.dynamic_ire_enabled`.
- Default: enabled/committed on zBooted Zurich Patch 11+ instances; upgraded instances may
  still be Static. Always check.
- Exclude custom Hardware subclasses when their custom attributes require static rules.
- Applicable only to `cmdb_ci_hardware` and descendants.

---

## 6. Duplicate prevention and insert-vs-update

### 6.1 The insert/update decision table

| Condition | IRE action | What you see |
|---|---|---|
| Identifier matches exactly one CI | **Update** | Attributes reconciled; `last_discovered`/`discovery_source` updated |
| No identifier match and the **IRE Data Source Rule** permits insert | **Insert** | New CI; Reconciliation and Data Refresh are not applied |
| No match but the **IRE Data Source Rule** blocks insert | **Blocked** | `INSERT_NOT_ALLOWED_FOR_SOURCE`; Enhanced API stores a partial payload |
| Insufficient identifying data | **Partial / incomplete** | Partial stored for later merge, or incomplete logged and never retried |
| Multiple matches, count < threshold, `skip_duplicates=true` | **Update oldest**, mark others | Oldest becomes main CI; others get `duplicate_of`; de-dup task created |
| Multiple matches, count ≥ threshold, or `skip_duplicates=false` | **Identification fails** | Error logged; de-dup task created; no update |
| Duplicate items inside one payload | **Deduplicated** before processing | One payload item processed |
| Matched CI requires class change | **Reclassify / task** | Automatic if allowed; otherwise reclassification task |
| Device seen under a second IP in the same run | No second CI | `Identified, ignored extra IP` |
| Scan type is `IP addresses` | No CI at all | Schedule type |

**Rule of thumb:** identification answers "new or existing"; reconciliation answers "whose
value wins". If you find yourself editing reconciliation to stop duplicates, you are on the
wrong screen.

### 6.2 Root causes of duplicate CIs

1. **Weak identification rules** — matching on `name` alone, or on a lookup entry that is
   not unique.
2. **Unstable identifying attributes** — adapter renames, hostname churn, serial-number
   rewriting, or a changed native key under a stable source.
3. **IP reuse / DHCP** — two devices share an address over time; MAC/NIC bonding complicates
   this further.
4. **Multiple sources with no authority model** — discovery, SCCM, monitoring, and manual
   entry all insert without Reconciliation Rules or IRE Data Source Rules.
5. **Lookup-table duplication** — duplicate serial-number records pointing at different CIs;
   IRE selects the older referenced CI unless configured to create de-dup tasks.
6. **Over-broad schedules** — scanning the same device through multiple ranges or behaviors;
   Shazzam range simplification only helps single-behavior schedules.
7. **Payload hygiene** — duplicate items in a payload, or missing criterion attributes that
   force partial/incomplete handling.
8. **Inclusion rules scoped by class** — child classes not named are not found by IRE, so a
   new CI is created.
9. **ACLs or query business rules** hiding the existing CI from IRE.
10. **Existing CI already has `duplicate_of` set, or `discovery_source = Duplicate`** — IRE
    refuses to identify it; remediate the duplicate set before re-scanning.
11. **Same CI discovered concurrently** by two discoveries, or the same dependent CI inside
    multiple payloads of one discovery.
12. **Multi-page payloads processed in parallel** — `glide.discovery.multi_page_serial_mode`
    processes them serially.
13. **Manually created CIs** with an empty discovery source that never get reconciled.
14. **Reconciliation blocks the update**, so a human "fixes" it by creating a manual CI.
15. **A high-priority source went silent**; its old values keep winning, and someone
    imports/manual-enters the "real" data → a second CI. Add a data refresh rule.
16. **An untrusted source** (e.g. an IP-scan tool) creates detail-less CIs of a class it
    cannot really discover → IRE Data Source Rule with Insert Not Allowed.

### 6.3 Prevention controls, by layer

**Design-time (CI Class Manager):**
- Model each class with a **complete independent identifier**; prefer independent rules.
- Put the strongest identifier entry at the highest priority; keep one entry where possible;
  avoid lookup entries.
- Add required attributes and identification inclusion rules where appropriate; never scope
  inclusion by class on a parent table.
- Define dependent relationship rules only for genuinely dependent CIs; keep dependency
  depth ≤ 2.
- Create the rule at the correct class level; child rules override parent rules.

**Runtime (properties and IRE):**
- `glide.identification_engine.skip_duplicates=true` lets IRE pick the oldest match for
  small duplicate sets instead of failing.
- `glide.identification_engine.skip_duplicates.threshold=5` is the safety bound; above it,
  identification fails as if skip were false.
- `glide.identification_engine.skip_sys_object_source_matching=true` prioritizes
  identification-rule matching over the `sys_object_source` shortcut. Use when the source
  native key is stable but identifying attributes change.
- `glide.identification_engine.lookup_match.create_duplicate_task_ci.enabled=true` when
  lookup duplication must be remediated.
- Use IRE Data Source Rules to stop untrusted sources from inserting; they can still update
  subject to Reconciliation Rules.
- Use Reconciliation Rules + Data Refresh Rules so only the authoritative source writes,
  and stale data can be refreshed.
- Enable dynamic reconciliation only with CMDB 360; it wins over static rules.
- Set `glide.duplicate_ci_remediator.max.cis` deliberately for large duplicate sets.

**Detection:**
- IRE always creates de-duplication tasks when it detects duplicate sets (even when
  `skip_duplicates` picks a main CI for the match).
- `duplicate_of` references the main CI; the main CI has an empty `duplicate_of`.
- CMDB Health duplicate metrics and the Identification Log expose trends.
- Identification Simulation lets you test a payload without committing.

**Remediation:**
- Bulk: CMDB Workspace De-duplication Dashboard + Template Library; create templates per
  class, review tasks, run templates in bulk.
- Single task: Duplicate CI Remediator wizard; choose the main CI, then merge attributes,
  relationships, and related items (or retain the main CI as-is).
- Asset-related tables are not merged; inactive change requests referencing a duplicate CI
  have the CI field cleared rather than merged.
- Related-table workflows can be disabled during remediation via
  `glide.duplicate_ci_remediator.merge_related_items_enhanced` plus an entry in
  `reconcile_duplicate_related_table_config`; base system does this for `change_request`
  and `task_ci`.
- Templates are **not retroactive** — they do not update already-created de-duplication
  tasks.
- The **"Condition to filter CIs from the template class"** is evaluated at the CI level,
  not at the de-duplication task level, which explains templates appearing to "not pick up"
  the intended task.

### 6.4 Duplicate detection and remediation properties

| Property | Default | Purpose |
|---|---|---|
| `glide.duplicate_ci_remediator.dry_run` | `false` | Test remediation without writing. |
| `glide.duplicate_ci_remediator.max.cis` | `1000` (cap 5000) | Large-set threshold; above it, remediation is limited. |
| `glide.duplicate_ci_remediator.max.field_length` | `4000` | Excludes/truncates long attributes. |
| `glide.duplicate_ci_remediator.related_items_blacklist` | see §5.9 | Related tables excluded from merge. |
| `glide.duplicate_ci_remediator.merge_related_items_enhanced` | — | Skip workflows / ignore DB errors on related tables. |
| `glide.duplicate_ci_remediator.enable_restricted_mode` | `false` | Allows blocked remediation to proceed with limited related items. |

Remediation rules: do not set `duplicate_of` by hand; the system enforces constraints (main
CI cannot itself be a duplicate; a duplicate of `Unknown` blocks the operation). Roles:
`itil` to read, `itil_admin` or `cmdb_dedup_admin` to write. After remediation, ensure
inclusion rules / skip-duplicates are configured so the same pair is not re-created.

### 6.5 Duplicate-CI troubleshooting checklist (KB0869861)

1. Check identification rules in CI Class Manager — confirm the CI should be considered a
   duplicate.
2. Check inclusion rules — ensure the CI class is included and not excluded by a parent
   table condition.
3. Debug business rules — disable custom query business rules to see if they prevent CI
   matching.
4. Debug ACLs — ensure IRE is querying without restrictive access controls.
5. Check domain separation — same Correlation ID in different domains = different CIs (by
   design).
6. Check `duplicate_of` — IRE skips CIs where `duplicate_of` is populated.
7. Check `discovery_source` — IRE skips CIs with `discovery_source = Duplicate`.
8. Use the IRE API — test payloads via `IdentificationEngineScriptableApi` in a background
   script.
9. Run identification simulation — test matching without updating the CMDB.

### 6.6 Anti-patterns

| Anti-pattern | Why it hurts | Correct move |
|---|---|---|
| Name-only identification | Renames and duplicate hostnames create new CIs | Add serial/UUID/MAC; use a strong independent key |
| More identifier entries "for safety" | Each entry adds matching cost; weak entries can match the wrong CI | One strong entry; extra entries only with evidence |
| Lookup identifier entries | Performance cost; duplicate lookup rows cause ambiguous matches | Redesign to independent attributes; if unavoidable, monitor lookup duplicates |
| `skip_duplicates=false` everywhere | Any small duplicate set fails identification | Keep true with a deliberate threshold; investigate the cause |
| Raising the threshold without fixing rules | Masks duplicates instead of preventing them | Fix rules, then re-tune threshold |
| One giant schedule for everything | Long runs, stacked invocations, hard to isolate failures | Split by network/domain/credential; use behaviors and chaining |
| Untrusted source allowed to insert | Low-quality CIs and duplicates | Add an IRE Data Source Rule; the source can still update |
| No reconciliation owner | Sources overwrite each other | Reconciliation Rules + Data Refresh Rules |
| Deleting CIs to "clean up" | Breaks relationships/history; may be recreated next run | Use de-dup remediation and deletion strategies |
| Changing serial-number syntax | Breaks asset tracking and matching | Preserve raw serial numbers |
| Ignoring `max run time`/`max idle` | Stuck runs pile up | Set both; monitor status |
| Inclusion rule scoped by class on a parent table | Child classes not found → duplicates | Filter on attributes/status instead |
| Custom identifiers sharing `Order` values with base rules | Rules may not run as intended | Give unique Order; confirm Active |
| Editing `duplicate_of` by hand | Breaks system constraints | Use Remediator |
| Treating CMDB Health duplicate = 0 as proof | The metric has narrow conditions (see §7) | Use de-dup tasks + Identification Log trends |

---

## 7. Verification and observability

| What | Where | What to look for |
|---|---|---|
| Discovery Status | `Discovery > Discovery Status` (also related list on the schedule) | State progression, completed/current activity, device history, scan status |
| Discovery timelines | `Show Discovery Timeline` | Every probe/sensor/pattern with queueing vs processing time and ECC records |
| ECC Queue | `Discovery > ECC Queue` | Raw probe/pattern XML payloads; proves what was returned |
| Discovery Log | `Discovery > Discovery Log` | Debug/Info/Warning/Error by probe, device, CI, ECC input |
| Discovery Home | `Discovery > Home` | Schedule summaries, cloud resources, error details and remediation hints |
| CI Identification Log | `Configuration > Identification Logs` | Identification decisions; enable with `glide.discovery.debug.ci_identification` |
| Identification simulation | `Configuration > Identification/Reconciliation` | Payload output and execution log **without** committing |
| CMDB Health | CMDB Workspace / Health dashboard | Duplicate, orphan, staleness, compliance KPIs |
| Partial payloads | `cmdb_ire_partial_payloads`, `cmdb_ire_partial_payloads_index`, `cmdb_ire_incomplete_payloads` | Held/recoverable items, key index, dead items |
| De-duplication dashboard | CMDB Workspace | Duplicate sets and trends |

Canceling an active discovery: started sensor jobs are terminated immediately; jobs in
`Ready` that have not started are deleted.

**Per-device states:** `Alive, not active, not classified` → `Active` → `Classified` /
`Active, couldn't classify` → `Identified CI` / `Identified, ignored extra IP` → `Updated
CI`.

**CMDB Health KPIs:** correctness, completeness, compliance. The **duplicate metric** is
narrower than people expect: it only evaluates CIs that have identification rules and that
either have an **empty discovery source** or have an **active de-duplication task**. Two
CIs with identical name+serial and both `discovery_source = ServiceNow` are **not**
reported unless a de-dup task exists. Orphan and staleness metrics feed correctness. The
CI Health widget can say *"not applicable"*: duplicate scoring needs identification rules on
the class or an ancestor, and orphan scoring needs orphan rules and health inclusion rules.

Copy-paste checks:
1. `Discovery > Status` → open the run → confirm devices reach `Identified CI`, not
   `Active, couldn't classify`.
2. `CMDB > cmdb_ci_<class>` list → filter `duplicate_of is not empty` for the class you
   just scanned.
3. CI Class Manager → class → Identifiers: confirm exactly one rule, and that its entries
   match the attributes your pattern actually returns.
4. CI form → CI Health widget: if duplicate score says *not applicable*, you have no
   identification rule at that class or its ancestors.

---

## 8. Operational runbook

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
  `skip_duplicates`, `enforce_unique_ips`): treat as high risk.
- Deletion-strategy changes: high risk; can delete network adapter/IP records.
- Dynamic IRE commit: high risk; simulate first, record parity results.
- Debug properties (`glide.discovery.debug.ci_identification`,
  `glide.cmdb.logger.source.identification_engine`): time-box and revert.

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
| Pattern-heavy estate | `glide.discovery.multi_page_serial_mode=true`; verify serials; review process handlers. |
| Retired CI rediscovered | Expect no auto-un-retire (KB0755747); add a `cmdb_ci` business rule if auto-restoration is required. |

---

## 10. Conflicts found and how they were resolved

| # | Conflict | Resolution |
|---|---|---|
| 1 | **Release basis differs** — Zurich (this author), Brazil (openrouter deepseek-flash, alt-swarm), Australia (inkling), mixed (buffy). | Not a contradiction. Property names are stable; defaults/UI labels are release-pinned. Every table keeps release labels where known. |
| 2 | **Dynamic IRE property name** — `glide.identification_engine.dynamic_ire_enabled` (Zurich primary) vs `glide.identification_engine.dynamic_ire.enabled` (inkling). | Zurich primary source names `...dynamic_ire_enabled`; use that. The dotted variant is recorded as a spelling risk. |
| 3 | **Duplicate threshold behavior** — qwen2.5-coder table says "true + ≥ threshold → create de-dup task"; primary docs say matching fails and tasks are always created. | Primary wins: at/above threshold identification fails (as if skip=false); de-dup tasks are always created regardless. |
| 4 | **Inclusion-rule exclusion** — openrouter-free says an excluded CI is "updated regardless of reconciliation"; buffy says exclusion causes the CI not to be found → insert/duplicate. | Primary/identification docs: inclusion narrows the CIs processed during identification; an excluded CI is not matched, so the payload can insert a new CI. openrouter-free's "update regardless" is rejected. |
| 5 | **Reconciliation on insert** — openrouter-free decision tree implies reconciliation can be bypassed; openrouter deepseek-flash and buffy say reconciliation is update-only. | Primary wins: reconciliation is not applied on insert. |
| 6 | **Skip-duplicates property spelling** — `glide.identification_engine.skip_duplicates` vs `glide.identificationengine.skipduplicates`. | Both appear in ServiceNow material. Do not assume; check `sys_properties`. |
| 7 | **Log property spelling** — `glide.discovery.log_message_length` (primary) vs `glide.discovery.log_message_chars` (secondary). | Primary name used; variant recorded. |
| 8 | **Queue priority property prefix** — `com.glide.queue.discovery...` (primary) vs `glide.queue.discovery...` (inkling). | Primary prefix used; variant recorded. |
| 9 | **"Always" written on update** — buffy flags `last_discovered`/`first_discovered` as unverified; inkling/openrouter say always stamped. | IRE primary docs describe `last_discovered` update semantics but do not prove every update writes it. Treat as documented behaviour with a caveat; do not build refresh windows on it unverified. |
| 10 | **Retired CI auto-restore** — only openrouter-free (KB0755747). | KB-cited, not primary-doc verified. Included with the KB label and warning. |
| 11 | **`glide.discovery.enforce_ip_sync`** — hermes community only; likely confusion with `enforce_unique_ips`. | Excluded as unverified; `enforce_unique_ips` is the documented property. |
| 12 | **`glide.discovery.duplicate.threshold` / `glide.discovery.delete.*`** — appear in alt-swarm text but not in primary property reference. | Excluded as unverified. |
| 13 | **Identifier simulation UI** — buffy could not confirm a simulate action from the class form; primary docs confirm the Identification Simulation module. | Module path is correct; the class-form action remains unverified. |
| 14 | **CMDB Health duplicate metric** — buffy (KB0726425) says it is narrow; others treat it as a general duplicate count. | KB-cited narrow definition included; do not treat zero as proof of no duplicates. |
| 15 | **FBD / Configuration Console** — openrouter deepseek-flash (learning guide) vs not mentioned by others. | Included as a Discovery feature, not an IRE rule family. |

---

## 11. Open questions / gaps

1. Exact ServiceNow family/patch in scope. Property names are stable; defaults/UI labels drift.
2. CMDB 360 / Multisource CMDB licensed and enabled? Dynamic reconciliation requires it.
3. Dynamic IRE committed? Verify `glide.identification_engine.dynamic_ire_enabled`.
4. Domain separation enabled? Affects schedules, credentials, reconciliation scopes, and
   whether same Correlation ID in different domains is a duplicate.
5. Full list of non-Discovery CMDB sources (SCCM, Intune, cloud, scanners, monitoring).
6. Scale: IPs, devices, MID Servers, schedules, domains.
7. Legacy custom identifiers from a pre-Geneva upgrade?
8. Service Mapping in scope? (Out of scope here except shared IRE/Discovery.)
9. Deletion policy for missing CIs (none vs absent vs retired vs delete).
10. Sub-production instance available for Identification Simulation?
11. Regulatory retention constraints?
12. New vs upgraded instance (four hostname/IP defaults drift)?
13. Whether the identifier simulation action is exposed from the class form.
14. Exact default of `glide.identification_engine.skip_sys_object_source_matching`.
15. Whether `last_discovered` is written on every update or only on change.
16. Pattern authoring depth (deliberately out of scope; a separate worktree is proposed).

---

## 12. Source ledger

### Primary ServiceNow docs (Zurich, captured by this author)

`Exploring Discovery`; `Horizontal discovery process flow with patterns` / `...with probes
and sensors`; `Set up Discovery without Guided Setup`; `Discovery Guided Setup`;
`Discovery Quick Start`; `Discovery Schedule form reference`; `Schedule a horizontal
discovery`; `Discovery behaviors`; `Discovery classifiers`; `Create a Discovery CI
classification`; `Create a Discovery process classification`; `Discovery identifiers`;
`How Discovery identifiers work`; `Configure Discovery identity probes/sensors`;
`Discovery properties`; `Discovery Admin Workspace Settings`; `CI deletion strategies for
pattern discovery`; `Discovery and SCCM together`; `Discovery status`; `Discovery
timelines`; `Discovery device history`; `Discovery error messages`;
`Discovery performance metrics`; `Discovery resource utilization`.

### Primary ServiceNow docs (Brazil/Australia, captured by siblings)

`Exploring Discovery`; `Configuring Discovery`; `Discovery properties`; `Discovery Schedule
form reference`; `Discovery classifiers`; `Discovery identifiers`; `Discovery behaviors`;
`Deletion strategies`; `CI Class Manager`; `CMDB IRE`; `IRE engine`; `Identification rules`;
`Reconciliation rules`; `Detecting duplicate CIs`; `Duplicate CIs remediation`;
`Identification simulation`; `CMDB 360`; `CMDB Health`; `Create a CI class`;
`Create a CI identification rule`; `Create a CI reconciliation rule`;
`Create a data refresh rule`; `Create an IRE data source rule`; `IRE error messages`;
`Create dependent relationship rules`; `Create an inclusion rule`.

### KB articles cited by siblings

| KB | Topic |
|---|---|
| KB0535236 | Troubleshooting the Classification phase; WMI high-port firewall |
| KB0726425 | CMDB Health duplicate metric algorithm (narrow conditions) |
| KB0748222 | IP range exclusions |
| KB0750382/83/86 | IRE payload logging / on-demand identification / IRE steps |
| KB0755747 | Discovery does not update operational status of retired CIs |
| KB0756709 | CMDB reconciliation and data precedence rules |
| KB0869861 | How to troubleshoot duplicate CMDB CI records |
| KB1064718 | CMDB IRE fundamentals |
| KB1542272 | Restricted mode in Duplicate CI Remediator |
| KB3037828 | Lower-priority rule with specific attributes blocks higher-priority rule |
| KB3104470 | Discovery phases / identification keys |

### Secondary cross-reference guides

- CMDB guide — four-pillar rule comparison:
  https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/modules/cmdb/cmdb-guide/
- Discovery guide — four phases, Configuration Console, FBD terms:
  https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/modules/discovery/discovery-guide/

---

## Appendix — Quick reference card

```
Discovery flow:  Shazzam → Classify → Identify → Explore → IRE → CMDB
Four IRE families: Identification Rule (insert+update) · IRE Data Source Rule (insert gate)
                  Reconciliation Rule (update authority) · Data Refresh Rule (staleness)
Key tables:      cmdb_identifier, cmdb_identifier_entry,
                 cmdb_reconciliation_definition, cmdb_dynamic_reconciliation_definition,
                 cmdb_ire_data_source_rule, cmdb_ire_partial_payloads,
                 cmdb_ire_partial_payloads_index, cmdb_ire_incomplete_payloads,
                 cmdb_datasource_last_update, cmdb_datasource_staleness,
                 sa_ci_to_pattern, reconcile_duplicate_task
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
                 glide.reconciliation.override.null (true)
                 glide.discovery.multi_page_serial_mode (false)
```
