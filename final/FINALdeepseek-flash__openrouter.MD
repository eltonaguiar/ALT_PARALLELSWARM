# FINAL — ServiceNow Discovery Configuration Reference

**Merged final deliverable** · `SNC_DISC_RESEARCH`
**Author:** `deepseek-flash__openrouter__kilo-cli` — model `deepseek/deepseek-flash`, provider OpenRouter (inferred), harness Kilo CLI
**Date:** 2026-11-13
**Release basis:** ServiceNow **Brazil** and **Australia** documentation, cross-checked against the CMDB and Discovery learning guides
**Method:** all findings from every agent worktree under `ALT_PARALLELSWARM` were read, de-duplicated, and validated against official docs / raw fetched sources. Conflicts are listed in §11.

> **Read this first.** This is a configuration reference, not a customer runbook. Every property name and default below is traceable to a source in §12. Where two agents disagreed, the conflict is resolved or explicitly flagged. Verify UI labels and defaults on your own release before changing production.

---

## 0. Contributor ledger

| Agent / folder | Model · Provider | What it contributed |
|---|---|---|
| `deepseek-flash__openrouter__kilo-cli` | `deepseek/deepseek-flash` · OpenRouter | 68-topic Brazil corpus; primary reference; full Discovery/IRE/duplicate analysis; swarm harness |
| `deepseek-v4-pro__deepseek__kilocode` (results) | `deepseek-v4-pro` · DeepSeek | Independent Brazil reference; 39-permutation IRE applicability matrix; KB links; insert/update nuance |
| `deepseek-v4.1-flash-fast__freebuff__buffy` | `deepseek-v4.1-flash-fast` · freebuff | 28-source ledger; full property lists; schedule/MID/CCM detail; duplicate causes |
| `deepseek-v4-flash__deepseek__hermes` | `deepseek-v4-flash` · DeepSeek | Community/KB corroboration; `L3_mapping`, `ire_err_exclusion_list`, CCM tabs |
| `inkling-2-small__openrouter__kilo` | `inkling-2-small:free` · OpenRouter | Australia end-to-end guide; full Discovery property catalog; MID properties; troubleshooting matrix; runbook |
| `openrouter-free__openrouter__kilo` | OpenRouter free models | KB0869861 duplicates; retired CI behavior; multi-page serial mode |
| `kilo-ernie-5.5-flash__baidu__kilo` | ERNIE 5.5 flash · Baidu | Five-worktree swarm; schedule fields, CCM tabs, duplicate flow, reconciliation caveats |
| `qwen3-30b-a3b__ollama__hermes`, `qwen2.5-7b__ollama__hermes`, `llama3.1-8b__ollama__hermes` | local Ollama | Additional drafts; corroboration of phases and duplicate basics |
| `qwen3.5-4b__ollama__alt-swarm`, `qwen2.5-coder-7b__ollama__alt-swarm`, `particle-1__openrouter__alt-swarm` | local Ollama / OpenRouter free | Dispatched worker drafts (options, duplicates, CI Class Manager) |

---

## 1. Mental model

Discovery is **two pipelines that meet at the CMDB**:

```
Network / devices
      │  horizontal Discovery (this document)
      ▼
Shazzam scan → classification → identification → exploration
      │                              │
      │ probes + sensors             │ patterns (NDL)
      │ identity probe / sensor      │ pattern operations
      ▼                              ▼
Discovery identifier  ───────►  CMDB IRE Identification Rules
      │                              │
      └──────────► IRE ◄─────────────┘
                     │
          identify → reconcile → insert / update / no-op
                     │
                     ▼
                    CMDB
```

**Four IRE rule families — canonical terminology and insert/update applicability:**

| Mechanism | Exact name | Question it answers | Insert | Update | Configuration level |
|---|---|---|---|---|---|
| **Identification Rule** | Identification Rule (IRE identifier) | "Does this CI already exist?" | **YES** — no match creates | **YES** — match updates | Class → identifier entry → attributes |
| **IRE Data Source Rule** | IRE Data Source Rule (short: Data Source Rule) | "Can this source create a new CI of this class?" | **YES — gate** (may block) | **NO** — cannot block updates | Class + source; not attribute-level |
| **Reconciliation Rule** | Reconciliation Rule | "Which source may update this attribute?" | **NO** | **YES** — after match | Class + source + attribute |
| **Data Refresh Rule** | Data Refresh Rule (staleness rule) | "Has the higher-priority source's data gone stale?" | **NO** | **YES** — after reconciliation | Class + source + refresh criteria |

**Order of application:**

1. **Identification** runs first on every payload item.
2. If a CI **matches** → **Reconciliation** decides which source may update each attribute; **Data Refresh** can then let a lower-priority source refresh a stale field.
3. If **no match** → **IRE Data Source Rule** decides whether the source may insert. Reconciliation and Data Refresh are skipped.

**Two boundaries that are easy to get wrong:**

- An **IRE Data Source Rule** is a **create-only** gate. It cannot restrict which attributes an allowed source updates, and it cannot block updates to an existing CI.
- **Reconciliation** and **Data Refresh** are **update-only**. They are not applied when IRE inserts a new CI.

**Adjacent mechanisms — not one of the four families:**

| Mechanism | What it does |
|---|---|
| **Identification Inclusion Rule** | Narrows which CIs participate in identification and in the duplicate Health metric |
| **Reclassification** | Upgrades/downgrades/switches a matched CI's class; can produce a reclassification task |
| **De-duplication Task** | Groups duplicate CIs for remediation; output of duplicate detection, not a rule |
| **Dynamic IRE / dynamic reconciliation** | Value-based reconciliation via CMDB 360; an extension of the Reconciliation family |
| **Partial / incomplete payloads** | Error handling for payloads that cannot be uniquely identified or committed |

---

## 2. Release and terminology notes

### 2.1 Release comparison (validated)

The **Brazil** `r_DiscoveryProperties` page contains **114 properties**; the **Australia** page contains **112**. Brazil adds two `sn_disco_certmgmt.*` properties (`find_and_attach_root_certificate`, `mark_self_signed_for_incomplete_chain`). Of the 112 common properties, 110 have documented defaults and two (`glide.discovery.sensors.netapp_native_7mode`, `glide.discovery.sensors.netapp_native_cluster_mode`) are listed as unset. A programmatic comparison found only four default-value differences, and all four are the same semantic change with a different release name:

| Property | Brazil default | Australia default |
|---|---|---|
| `glide.discovery.hostname.snmp_trusted` | `false` (new Brazil customers: `true`) | `false` (new Australia customers: `true`) |
| `glide.discovery.hostname.ssh_trusted` | `false` (new Brazil customers: `true`) | `false` (new Australia customers: `true`) |
| `glide.discovery.hostname.wmi_trusted` | `false` (new Brazil customers: `true`) | `false` (new Australia customers: `true`) |
| `glide.discovery.ip_service_affinity` | `false` (new Brazil customers: `true`) | `false` (new Australia customers: `true`) |

**Conclusion:** property names and defaults are stable across these releases. UI labels and navigator paths vary more than properties.

### 2.2 Aliases

| Alias seen in docs/UI | Canonical term |
|---|---|
| CMDB identifier, IRE identifier, CI identifier | **Identification Rule** |
| Data Source Rule, Data Sources (navigator) | **IRE Data Source Rule** |
| CI reconciliation rule, static/dynamic reconciliation | **Reconciliation Rule** |
| Staleness rule, Refreshable + Stale threshold | **Data Refresh Rule** |
| Discovery Behaviour (guide) | **Discovery Behavior** (ServiceNow docs) |

### 2.3 Known documentation typos / conflicts

| Item | Status |
|---|---|
| `cmdbreconciliationdefinition` | Docs typo. Real table is `cmdb_reconciliation_definition`. Verify with `.list`. |
| `glide.identificationengine.skipduplicates` | Docs typo in a properties summary. Real property is `glide.identification_engine.skip_duplicates`. |
| `glide.discovery.log_message_chars` vs `glide.discovery.log_message_length` | Both appear in agent sources with default `200`. Treat as the same setting; verify the exact name in `sys_properties`. |
| `glide.discovery.enforce_ip_sync` | Appears in one source; not in the official 97-property catalog. Likely a typo for `glide.discovery.enforce_unique_ips` or a release-specific property. Verify. |
| `glide.discovery.multi_page_serial_mode` default | One source says `false` with a direct quote ("false sets the pages to process in parallel and true sets the pages to process serially"); another says `true`. **Resolved to `false`** per the quoted source; verify on instance. |
| Correlation ID duplicate behavior | One source says two Windows servers with the same Correlation ID are not treated as duplicates; another says the same Correlation ID triggers duplicates unless domain-separated. **Unresolved** — Correlation ID is documented as the ESX Server Rule identifier, not a general duplicate trigger. Verify before relying on it. |

### 2.4 Properties not present in the fetched Discovery Properties page

These appear in `r_AvailableSystemProperties`, KB sources, or feature-specific docs, not in the 97-property `r_DiscoveryProperties` page fetched on 2026-11-13. Verify on the instance before use:

- `glide.discovery.multi_page_serial_mode` (default `false` per quoted source)
- `glide.discovery.log_debug_info` (default `false`)
- `glide.discovery.log_message_chars` (default `200`)
- `glide.discovery.sam_batch_update_size` (default `100`)
- `glide.discovery.source_name` (default `ServiceNow`; documented in *Change the Discovery source name*)
- `glide.discovery.debug.classification` (default `false`; documented in *Discovery classifiers*)
- `glide.discovery.ire_err_exclusion_list` (default includes `ABANDONED, INSERT_FAILED, UPDATE_FAILED, NO_IDENTIFIER_KEYS_GENERATED`)

### 2.5 Release-specific behavior notes

- **Dynamic IRE:** `glide.identification_engine.dynamic_ire_enabled` default `false`; `glide.identification_engine.dynamic_ire.auto_compare` default `true` compares Static IRE and Dynamic IRE for all payloads without switching. Class exemptions are stored in `cmdb_dynamic_ire_skip_class`.
- **ADM updates:** `glide.discovery.adm.update.applications` default `true` on instances where Discovery was first activated beginning with the Tokyo release; older instances must add it manually.
- **Probe-to-pattern migration:** `glide.discovery.ip_based.active` default `true` on migrated instances; Discovery does not attempt extra IP-address detection.
- **IPv6 schedule cap:** `glide.discovery.schedule_ipv6_limit` default `20000`; on instances below ZP3/YP9 the maximum is `5,000`, which is also the default in Yokohama and earlier.
- **HTTP classification:** from Madrid onward, the HTTP fallback runs last and only when Shazzam saw ports 80/443 open and WMI/SSH/SNMP failed.
- **File-Based Discovery:** plugin `com.snc.discovery.file_based_discovery`; default frequency **Monthly**; does not run before the initial Content Data Service sync (~24 hours).
- **Navigation repackaging:** IRE is repackaged under `Configuration > Identification/Reconciliation`; the classic `All > Discovery > Discovery Definition > {Schedules, Properties}` paths remain.

---

## 3. Canonical order of operations

### 3.1 Setup (before the first broad scan)

| # | Step | Why | Exit check |
|---|---|---|---|
| 0 | Confirm subscription/plugins; assign `discovery_admin` | Discovery is a separate subscription; the role grants access to Discovery tables | Role present; plugin active |
| 1 | Install **at least two** MID Servers; assign **Discovery** or **ALL** | The MID Server executes probes/patterns and initiates all communication | MID Servers appear under `Discovery > MID Servers`; status **Up** and **Validated** |
| 2 | Configure and **test** credentials (WMI, SSH, SNMP, SNMPv3, HTTP, vCenter, IPMI) | Bad credentials are the leading cause of failed discovery | Credential test succeeds per protocol/device class |
| 3 | Define IP ranges / range sets; add global IP exclusions | Discovery scans only what you authorize | Ranges resolve; excluded networks absent |
| 4 | Review **Identification Rules** and **Dependent Relationship Rules** before the first broad scan | Weak identifiers are the leading cause of duplicate CIs | A test device matches the expected CI class and identifier |
| 5 | Create a Discovery schedule (**Discover = Configuration items**) | The schedule is the control point: when, where, which MID Server, which behavior | Schedule saved; `Discover now` works |
| 6 | Run a narrow pilot (one range, one credential) | Fail fast before scaling | Discovery Status reaches a terminal state |
| 7 | Validate via ECC Queue XML, Discovery Log, device history, Home page | Proves what was actually collected and written | Expected CIs created/updated; no credential errors |
| 8 | Tune properties/classifiers/behaviors | Only after evidence from step 7 | Re-run improves coverage without new duplicates |
| 9 | Configure CMDB governance: Identification Rules, IRE Data Source Rules, Reconciliation Rules, Data Refresh Rules, inclusion, de-dup | Discovery writes through IRE; governance decides who may insert vs. update | Identification simulation passes; duplicate metric stable |
| 10 | Operate: schedules, CMDB Health, Data Manager, CMDB 360 | Keeps the CMDB accurate over time | Health/duplicate KPIs trending correctly |

**Critical ordering rule:** design the **CI class + identification rule** before enabling a broad schedule. A schedule that discovers 10,000 devices against a weak name-only identifier is how duplicate floods are created.

### 3.2 Runtime phases (per device)

```
Schedule / Quick Discovery
   │
   1 SCAN       Shazzam + port probes (ECC queue → MID) → open ports → machine type
   2 CLASSIFY   one classification probe per device → OS/type → CI class
   3 IDENTIFY   identifier rules / pattern identifier ops → match? update : create
   4 EXPLORE    exploration probes/patterns → attributes + relationships
   5 COMMIT     IRE: identification → reconciliation → insert/update in CMDB
```

**Per-device state chain (Brazil docs):**

```
Alive, not active, not classified
  → Active
  → Classified  /  Active, couldn't classify
  → Identified CI  /  Identified, ignored extra IP
  → Updated CI
```

- `Active, couldn't classify` = credential/protocol/port problem at classification.
- Classifies but never reaches `Identified CI` = identity probe or IRE problem at identification.
- `Identified, ignored extra IP` = the device was seen under a second IP in the same run; no second CI is created.

After identification, the `discovery.device.complete` event triggers the `IPAddressFixup` script include.

**Patterns path:** when a pattern is used, the **Horizontal Pattern probe** covers identification and exploration together; the identity probe is not used. Pattern operations call the identifier rules for the CI type specified by the pattern.

---

## 4. Configuration surface

### 4.1 Roles and entry points

| Area | Role | Notes |
|---|---|---|
| Discovery configuration/run | `discovery_admin` (or `admin`) | Schedules, credentials, MID Servers, Discovery properties |
| MID Server service account | `mid_server` | Instance side; local/domain credentials on the target side |
| CI Class Manager / IRE | `sn_cmdb_admin` full; `sn_cmdb_editor` read | `itil` may have read access to some IRE logs |
| De-duplication tasks | `itil` read; `itil_admin` or `cmdb_dedup_admin` write | |
| Discovery properties | `admin` / `discovery_admin` | |

**Entry points:**

| Destination | Breadcrumb |
|---|---|
| Discovery dashboard / home | `All > Discovery > Dashboard` / `Discovery > Home` |
| Discovery Configuration Console | `All > Discovery > Discovery Definition > Configuration Console` |
| Discovery schedules | `All > Discovery > Discovery Schedules` (Brazil docs) / `Discovery > Discovery Definition > Schedules` (guide) |
| Discovery status | `All > Discovery > Status` |
| Discovery log | `All > Discovery > Discovery Log` |
| MID Servers | `All > Discovery > MID Servers` |
| Credentials | `All > Discovery > Credentials` |
| Probes and patterns | `All > Discovery > Discovery Definition > Probes · Patterns` |
| Discovery properties | `All > Discovery > Discovery Definition > Properties` / `All > Discovery > Properties` / `discovery_private_properties.list` |
| CI Class Manager | `All > Configuration > CI Class Manager` |
| IRE rules | `All > Configuration > Identification/Reconciliation > {Identification Rules, Reconciliation Rules, Data Refresh Rules, IRE Data Source Rule, Identification Inclusion Rules}` |
| CMDB properties | `All > Configuration > CMDB Properties > {Identification/Reconciliation Properties, Duplicate CI Remediator Properties}` |
| Identification Logs | `All > Configuration > Identification Logs` |
| ECC Queue | `% ecc_queue` in the navigator filter |
| Discovery Admin Workspace | errors, anomalies, ML detection |

### 4.2 MID Server

- The MID Server **polls the instance** for work, executes probes/patterns, and returns results. It does not retain discovery data.
- All communication is initiated from inside the firewall over SOAP/HTTPS; no inbound firewall rule or VPN is required.
- Install **two or more** initially, on different schedules/ranges, to finish faster and to avoid a single point of failure.
- The MID Server must be assigned the **Discovery** application or **ALL**.
- A MID Server can belong to **one cluster** only; cluster selection prefers the lowest `Order` value that is `Up`, falling back to `Paused`/`Upgrading`, and ignores default MID Server settings.

**Auto-Select MID sequence:**

1. a MID Server with the Discovery app (or ALL) and a matching IP range;
2. otherwise a MID Server with ALL and a matching IP range;
3. if several are Up, choose randomly among them;
4. otherwise the default MID Server for Discovery, then for ALL;
5. otherwise `Paused`/`Upgrading` candidates.

**Caveat:** Auto-Select is **not supported with IPv6** (reported by one source; verify on your release).

**Ports:** WMI `135` + dynamic RPC high ports, SSH `22`, SNMP `161`/udp, HTTP `80`/`443`. A firewall that allows 135 but blocks the dynamic high ports will break Windows identification/exploration.

**MID Server properties** are set in `config.xml` or MID Server Properties. Full catalog in §4.9.

### 4.3 Credentials

- Windows/WMI credentials come from the **MID Server service login** on a Windows host.
- UNIX/SSH, vCenter, SNMP, IPMI, and HTTP credentials are configured **on the instance** (`All > Discovery > Credentials`).
- Discovery automatically determines which credential works for a device and pins the pair in `dscy_credentials_affinity`. Changing credentials triggers a re-try cycle.
- With Orchestration + Discovery and credential aliases enabled, the lowest-order affinity wins.
- `mid.discovery.multiprobe.skip_others_on_error` (default `true`) stops a multi-probe from iterating through remaining credentials when another member probe has already failed or timed out.
- With Orchestration + Discovery and credential aliases enabled, the lowest-order affinity wins.
- External credential storage is controlled by `com.snc.use_external_credentials` (default `true`).
- Test credentials before every broad run; bad credentials are the leading cause of failed discovery.
- For multiple Windows domains, prefer **PowerShell** (one MID Server can authenticate across domains with instance-stored credentials), or use behaviors.

### 4.4 IP address space

- A schedule scans only the IP ranges attached to it; a **range set** is a reusable group of ranges.
- Range methods can be combined: IP **address list**, IP **range**, IP **network** (CIDR). CIDR networks auto-exclude network and broadcast addresses.
- **IPv6** is not supported for range or network definitions in all releases; IPv6 address-list scans may be available for Configuration-item schedules.
- **Global IP exclusions** prevent scanning specified addresses across all schedules that discover CIs, IPs, or networks.
- **IP service affinity** remembers which protocol/port succeeded for an address (`ip_service_affinity`), so subsequent runs try the working protocol first.
- `glide.discovery.enforce_unique_ips` controls whether an IP is cleared from other devices when reused. It is **not** a CI de-duplication control; default `false`.
- `glide.discovery.exclude_ip_sync_classes` (default `cmdb_ci_lb`) keeps the management IP of load balancers instead of substituting a NIC IP.
- **IPAM integration** can auto-create schedules; `glide.discovery.schedule_ipv4_limit` (default 65,536) and `glide.discovery.schedule_ipv6_limit` (default 20,000) bound auto-generated schedules.
- More than 500,000 excluded addresses cancels the discovery and logs an error.

### 4.5 Discovery schedule

| Field / control | Options / default | Effect |
|---|---|---|
| **Name** | free text | Unique descriptive name |
| **Discover** | `Configuration items`, `IP addresses`, `Networks`, `Service`, `Serverless`, `Cloud application`, `Cloud resources`, `Certificates` | For CMDB CI population use **Configuration items**. IP-address scans create device history only and do **not** update the CMDB. |
| **MID Server selection method** | `Auto-Select`, `Specific MID Cluster`, `Specific MID Server`, `Use Behavior` | Auto-Select matches MID IP ranges + app; Behavior is for multi-MID/multi-domain/load balancing. |
| **Behavior** | preconfigured behavior | Multiple Windows credentials, multiple protocols across MIDs, large-scale load balancing, multiple domains |
| **Location** | location reference | Assigned to discovered CIs; empty = no location |
| **Max run time** | duration | Hard stop; remaining tasks cancel even if the scan is incomplete |
| **Max Idle time** | duration | Cancels stalled runs (no ECC movement); **hidden by default** — add the column to `discovery_schedule` |
| **Run** | `On Demand` (default), `Daily`, `Weekly`, `Monthly`, `Once`, `Periodically`, `Weekdays`, `Weekends`, `Month Last Day`, `Calendar Quarter End`, `After Discovery` | Schedule frequency; `After Discovery` chains schedules; `Even if canceled` decouples the chain |
| **Active** | `true` / `false` | Inactive schedules can still be run manually |
| **Log state changes** | `true` / `false` | Logs each state transition on Discovery Status |
| **Shazzam batch size** | default `1000`; UI minimum `256` | IPs per Shazzam probe; smaller batches classify earlier but create more probes |
| **Shazzam cluster support** | `true` / `false` | Distributes Shazzam batches across cluster MID Servers |
| **Use SNMP Version** | `ALL` (default), `v1`, `v2c`, `v3` | SNMP version for the scan |
| **Quick ranges** | comma-delimited network/range/list | Inline IP targets; good for pilots |
| **IP Ranges** | ranges | Primary targets for a simple CI scan |
| **Discovery Range Sets** | range sets | One range set per Shazzam probe |
| **Global IP Exclusion** | related list | Exclusions across all schedules |
| **Discovery Attributes** | related list | Additional attributes |
| **Discovery Status** | related list | Per-run status |

**Concurrency guard:** `glide.discovery.max_concurrent_invocations_per_schedule` (default **3**) prevents a slow schedule from stacking unbounded runs. `0` or negative disables the guard. It does not apply to schedules with `Run after = Even if canceled`.

### 4.6 Behaviors and functionality definitions

A **behavior** assigns **functionalities** (protocol sets) to MID Servers, grouped by a numeric **phase**. Use it for:

- load balancing across MID Servers;
- multiple Windows domains;
- SNMP devices protected by an ACL that only some MID Server hosts satisfy;
- devices that expose both SSH and SNMP, where you want to force one protocol.

A functionality record links: functionality definition (protocols), MID Servers, phase, and optional criteria. Criteria are required only for Windows MID Servers in multi-domain scenarios.

- Criteria fields: `mid_server`, `win_domain`, `mid_win_domain`.
- Common functionalities: `Windows only (WMI)`, `Windows/DNS/WINS`, `SNMP only`, `All except SNMP`, `All except Windows (no WMI)`.
- A behavior must have at least one Discovery functionality defined, otherwise it does not work properly.
- Phases run numerically; same-phase functionalities run in one Shazzam probe.

### 4.7 Classifiers and patterns

A **classifier** tells Discovery which probe(s) to run for identification and exploration, or which Horizontal Pattern probe to launch. Classification happens after the Shazzam scan and before identification/exploration.

| Type | What it classifies | Notes |
|---|---|---|
| **Device** | Windows/UNIX/Linux computers, routers, switches, load balancers | Triggers identification and exploration probes; HTTP classification is the lowest-priority fallback (used only if WMI/SSH/SNMP fail). From Madrid onward, the HTTP fallback runs last and only when Shazzam saw ports 80/443 open. |
| **Process** | Applications, based on running processes | Runs during exploration; creates child CIs with `Runs on::Runs`; process handler scripts strip unstable parameters (paths with PIDs, ports) to prevent duplicate application CIs; process classifier conditions are case-sensitive |
| **IP address (IP scan)** | Credential-less scan by open ports/banners | Updates CIs without identifiers; used for discovery of devices at the edge |

- Classifier **criteria** are `parameter operator value` and are based on what the classify probe returned.
- **Patterns** are NDL operations that collect/process data and update the CMDB. When a pattern is used, Discovery does **not** use the identity probe; it uses the identifier rule for the CI type specified by the pattern.
- Keep out-of-the-box classifiers unless you are adding a CI type Discovery does not already classify. Debug with `glide.discovery.debug.classification = true`.
- Shazzam port probes watch WMI, SSH, and SNMP; `OPEN` on any advances to the next phase.

### 4.8 Configuration Console and File-Based Discovery (FBD)

The **Discovery Configuration Console** (`All > Discovery > Discovery Definition > Configuration Console`; role `admin`) is the toggle-based front end for which CI types and information Discovery collects, including **File-Based Discovery (FBD)**. It does not display all supported applications.

FBD is a Discovery feature, **not one of the four IRE rule families**. It runs during the **Exploration** phase and records software found on disk:

| Object | Purpose |
|---|---|
| `cmdb_file_information` | The files FBD kept, including name, size, version, path, and CI reference |
| `samp_file_name` | Vendor-maintained allow-list of file names (synced from Content Data Service) |
| `samp_custom_file_name` | Your additions for software the vendor list does not know |
| `cmdb_sam_sw_install` | Software installation records, including FBD-sourced installs |
| `cmdb_unidentified_file_set` | Files that were kept but matched no known product |
| `cmdb_swid_tag` | SWID tags, when enabled in the console |

Key properties: `glide.discovery.file_discovery.wildcard.windows` (additive extensions) and `glide.discovery.file_discovery.blacklist.windows` (hard filter). Default FBD frequency is **Monthly**; FBD does not run until the initial Content Data Service sync (about 24 hours) completes. The plugin is `com.snc.discovery.file_based_discovery`.

### 4.8.1 Deletion strategies (patterns only)

Deletion strategies apply **only to patterns**, not probes/sensors. They are configured on the **Related CI Types [sa_ci_to_pattern]** table and apply when a pattern finds the main CI but not a related CI:

| Strategy | Behavior |
|---|---|
| **Keep** (default) | Preserve the record; no changes. |
| **Delete** | Delete the related CI and its relationship. |
| **Mark as absent** | Set `install_status = Absent`; does not delete. Exception: `cmdb_ci_network_adapter` and `cmdb_ci_ip_address` are deleted when marked absent. |
| **Delete relations** | Delete only the relationships. |
| **Mark as retired** | Set `install_status = Retired`; does not delete. |

### 4.9 Property catalogs — Discovery, IRE, MID, remediation, Health

**Discovery properties — full catalog.** The Brazil `r_DiscoveryProperties` page has **114 properties**; Australia has **112**. Of the 112 common properties, 110 have documented defaults and two NetApp native-mode properties are unset. Brazil adds two `sn_disco_certmgmt.*` properties. Seven additional properties appear in `r_AvailableSystemProperties` / KB / feature docs and are marked **[extra]**. All values below are the documented defaults; verify on your release.

**IP and identity**

| Property | Default | Effect |
|---|---|---|
| `glide.discovery.debug.ci_identification` | `false` | CI identification debugging: If set to true , enables debug logging (into the CI Identification Log) for CI Identification. |
| `glide.discovery.domain.name.nbt` | `true` | Set OS domain name by NBT or WMI. |
| `glide.discovery.enable_mac_address_verification` | `false` | Enables MAC address verification to determine if a device has changed its IP address during a discovery. |
| `glide.discovery.enforce_unique_ips` | `false` | Enforce unique IP addresses: Ignores the IP address after Discovery encounters subsequent devices that use the same IP address. |
| `glide.discovery.exclude_ip_sync_classes` | `cmdb_ci_lb` | Defines CI classes whose IP addresses shouldn’t be substituted if the address returned by Discovery doesn’t match one of the devices' NICs. |
| `glide.discovery.fqdn.regex` | `^([^.]+)\.((?:[^.]+\.)+[^.]+)$` | DNS Host Name And Domain Name Regex: The default parsing of FQDN (Fully Qualified Domain Name) is to pick the first name separated by dots as the host name and the rest of the n... |
| `glide.discovery.hostname.always_update` | `true` | Always update host name. |
| `glide.discovery.hostname.case` | `Lower case` | Host name case. |
| `glide.discovery.hostname.dns_nbt_trusted` | `true` | DNS or NetBIOS is trusted host name source: If set to true , trust the device name discovered via DNS or NetBIOS. |
| `glide.discovery.hostname.include_domain` | `false` | Includes domain name in host name: If set to true , include the domain name as part of the host name. |
| `glide.discovery.hostname.snmp_trusted` | `false (For new Discovery customers starting in Brazil , default value is true.)` | SNMP is trusted host name source: If set to true , trust the device name discovered via SNMP. |
| `glide.discovery.hostname.ssh_trusted` | `false (For new Discovery customers starting in Brazil , default value is true.)` | SSH is trusted host name source: If set to true , trust the device name discovered via SSH. |
| `glide.discovery.hostname.wmi_trusted` | `false (For new Discovery customers starting in Brazil , default value is true.)` | WMI is trusted host name source: If set to true , trust the device name discovered via WMI. |
| `glide.discovery.ip_based.active` | `true (For probe-to-pattern migrated instances.)` | This allows scans on all IP Address of the same device in the same Discovery schedule to go through full cycle. |
| `glide.discovery.ip_service_affinity` | `false (For new Discovery customers starting in Brazil , default value is true.)` | IP service affinity: If set to true , IP service affinity is enabled. |
| `glide.discovery.use_cmdb_identifiers` | `true` | CMDB Identifiers: If set to true , identification and reconciliation will be handled by the CMDB API instead of through the old Discovery implementation. |

**Network discovery**

| Property | Default | Effect |
|---|---|---|
| `glide.discovery.L3_mapping` | `true` | Map servers and network devices to routers and layer-3 switches If the "L3 mapping" property is enabled, it maps servers and network gears to its associated routers and layer-3 ... |
| `glide.discovery.allow_loopback_adapters` | `false` | Loopback adapter filter: Allows network loopback adapters on SNMP devices to be discovered instead of being filtered out during Discovery. |
| `glide.discovery.bgp_router_disable` | `true` | BGP router exploration disable: Disables running the SNMP – Routing probe or pattern when discovering a router running the BGP protocol. |
| `glide.discovery.debug.network_discovery` | `true` | Network discovery debugging: Enables extensive logging of all Network Discovery activities on the instance. |
| `glide.discovery.discoverable.network.max.netmask.bits` | `28` | Maximum netmask size for discoverable networks (bits): The maximum number of bits in a regular netmask for networks that are discovered by Network Discovery . |
| `glide.discovery.mark_esx_servers_as_absent` | `false` | If this property is set to true, the ESX Servers are marked as absent instead of retired if the ESX server isn’t found in the payload. |
| `glide.discovery.network_discovery.functionality` | `SNMP only` | Networks discovery functionality: The Functionality used to discover networks. |
| `glide.discovery.network_owner_method` | `Most Networks` | Network router selection method: This property controls the method used to decide (during Network Discovery ) which router should be selected as the router to be associated with... |
| `glide.discovery.physical_interface_types` | `6,117,9,71,209` | Physical interface types: A comma-separated list of interface types that are considered physical for the purposes of network discovery. |
| `glide.discovery.sensors.fire_ssh_probe` | `true` | In case the VIPs (Load Balancer Virtual Services) didn’t return as part of the SNMP Probe payload, fire the SSH Probe. |
| `glide.discovery.sensors.save_attachments` | `true` | Determines whether discovery sensors save ECC queue attachments after successful sensor processing. |
| `glide.discovery.switch_interface_types` | `7,8,9,26,53,62,69,71,78,115,117,209` | Switch interface types: A comma-separated list of interface types that are considered. |
| `glide.discovery.virtual_interface_types` | `53` | Virtual interface types: List of interface types (comma-separated) that can be considered "virtual" for the purposes of network discovery. |

**Software discovery**

| Property | Default | Effect |
|---|---|---|
| `glide.discovery.active_processes_filter` | `false` | Active Processes Filter: Optimization for application dependency mapping. |
| `glide.discovery.discover_software` | `true` | Discover software packages: Enable the discovery of software packages. |
| `glide.discovery.enable.software_filter` | `true` | Windows software filter: Enable Windows software filtering for Discovery . |
| `glide.discovery.enable.software_simplify` | `true` | Enables cleanup for software’s name and version. |
| `glide.discovery.enable.software_simplify_sccm` | `false` | Enables cleanup for SCCM software. |
| `glide.discovery.populate_software_instance_table` | `false` | If set to true , Discovery populates these tables for software discovery: cmdb_software_instance and cmdb_sam_sw_install |
| `glide.discovery.software_filter_keys` | `Language Pack, Hotfix Security Update` | Windows software filters: If Windows software filtering is enabled, when the name of a discovered software contains any of the comma-separated values, it’s filtered out. |
| `glide.discovery.software_sccm_managed` | `false` | Windows software is SCCM managed: If set to true , Discovery won’t populate software for computer CIs also managed by SCCM. |

**Application dependency mapping (ADME/ADM)**

| Property | Default | Effect |
|---|---|---|
| `glide.discovery.adm.update.applications` | `true, on instances where Discovery is first activated beginning with the Tokyo release.` | Controls if application CIs should be updated based on running process status. |
| `glide.discovery.adme.aggregation_interval` | `3600` | ADME - Aggregation interval (sec): How often to aggregate instantaneous data into chunks in seconds. |
| `glide.discovery.adme.base_dir_unix` | `false` | ADME - Unix Base Dir: An existing directory on the target UNIX machines to be used as a workspace. |
| `glide.discovery.adme.max_total_samples` | `100` | ADME - Max total samples: The limit of samples being taken by the script. |
| `glide.discovery.adme.rolling_window_size` | `24` | ADME - Rolling window size: How many recently aggregated chunks to keep. |
| `glide.discovery.adme.sampling_interval` | `120` | ADME - Sampling interval (sec): How often to sample process and connection data in seconds. |
| `glide.discovery.application_mapping` | `true` | Application mapping: Enables the application mapping portion of Discovery classification. |
| `glide.discovery.enable_adme` | `false` | ADME: Enable enhanced ADM probe. |
| `mid.powershell.target_base_dir` | `admin$\temp` | Powershell - Target Base Dir: A network share on the target Windows machines to be used as a workspace. |

**Event framework and performance**

| Property | Default | Effect |
|---|---|---|
| `com.glide.queue.discovery.cloud.sensors.processing_jobs.priority` | `100` | Manages the background job's worker priority for Cloud-based Discovery jobs when using Event Framework. |
| `com.glide.queue.discovery.sensors.processing_jobs.priority` | `100` | Manages the background job's worker priority for IP-based Discovery jobs when using Event Framework. |
| `discovery.event.pin.jobs` | `false` | Enables event processors to execute on specific nodes. |
| `discovery.event.separate.cloud.events` | `true` | Reduces processing time by separating the discovery.sensor and discovery.cloud.sensor event queues for cloud and IP-based discoveries. |
| `discovery.use.event.processing` | `false` | Enables Discovery to use the Event Framework when processing jobs. |
| `glide.discovery.count.use_optimized_counter` | `true` | Executes optimized code for updating discovery_status.started and discovery_status.completed counts. |
| `glide.discovery.log_debug` | `false` | Controls debug logging for Discovery . |
| `glide.discovery.log_message_length` | `200` | Limits the maximum message length that is displayed in Discovery Log table. |
| `glide.discovery.perf.metrics.enable_collection` | `true` | Whether to collect Discovery performance metrics. |
| `glide.discovery.perf.metrics.rollup_by_build` | `true` | Whether to aggregate individual Discovery performance metrics into a roll-up table that groups by discovery build. |
| `glide.discovery.perf.metrics.rollup_by_status` | `true` | Whether to aggregate individual Discovery performance metrics into a roll-up table that groups by discovery status. |
| `glide.discovery.perf.metrics.rollup_by_target` | `true` | Whether to aggregate individual Discovery performance metrics into a roll-up table that groups by target IP address. |
| `glide.discovery.save_pattern_log` | `true` | Controls whether pattern logs are saved during discovery execution. |
| `glide.discovery.use_probe_results_cache` | `false` | Use probe results cache: If set to true , the cache is checked to see if the results of the probe must be processed by a sensor. |
| `glide.discovery.warn_minor_version` | `false` | Warn on Minor Version Mismatch: If set to true , warnings are logged when minor_version mismatches are detected during Discovery sensor processing. |

**Scheduling and monitoring**

| Property | Default | Effect |
|---|---|---|
| `glide.discovery.max_concurrent_invocations_per_schedule` | `3` | Maximum concurrent invocations per schedule: Prevents an unbounded number of invocations from inundating the system when a schedule takes longer than the time between invocations. |
| `glide.discovery.retire_stale_accounts` | `false` | When set to true , Discovery automatically removes stale service account references from the Discovery Config - Logical Datacenters [cmp_discovery_ldc_config] table when previou... |
| `glide.discovery.schedule.autogenerate.debug` | `false` | Enables detailed logging for troubleshooting. |
| `glide.discovery.schedule.autogenerate.group` | `empty` | Groups auto-generated IPAM Discovery schedules by a specific tag or attribute. |
| `glide.discovery.schedule_ipv4_limit` | `65,536` | Defines the maximum number of IPv4 addresses that can be included in a single auto-generated IPv4 Discovery schedule. |
| `glide.discovery.schedule_ipv6_limit` | `20000` | Defines the maximum number of IP6 addresses that can be included in a single auto-generated IPv6 Discovery schedule. |
| `glide.discovery.schedule_monitoring.dry_run` | `false` | Determines whether the job will run in "dry run" mode. |
| `glide.discovery.schedule_monitoring.schedule_types_to_monitor` | `CIs` | Determines the type of statuses to track. |
| `glide.discovery.schedule_monitoring.stale_check_seconds` | `1200 (20mins). If nothing is configured, the default is 2x the interval of the job.` | Determines the number in seconds in which a status is considered stale. |

**Certificates, firewall, and Discovery Admin Workspace**

| Property | Default | Effect |
|---|---|---|
| `glide.discovery.certs.cert_admin_user_id` | `Certificate Administrator` | Certificate Inventory and Management : Holds the user ID of the user who will be referenced in the certificate task and incident, created via Scheduled Job. |
| `glide.discovery.certs.days_before_expiration_to_create_renewal_task` | `60` | Certificate Inventory and Management : Number of days before certificate expiration that a renewal task should be created. |
| `glide.discovery.certs.enable_incident_creation_for_expired_certificates` | `false` | Certificate Inventory and Management : Enables the Scheduled Job to create the incidents for expired certificates, for example, certificates whose validity is past current syste... |
| `glide.discovery.certs.enable_renewal_task_creation_for_discovered_certificates` | `true` | Certificate Inventory and Management : Enables renewal task creation for all discovered certificates. |
| `glide.discovery.certs.slack_channel_id` | `empty` | Certificate Inventory and Management : Indicates the Slack channel ID where certificate notifications are sent. |
| `glide.discovery.discover_aws_ec2_host_metadata` | `true` | When doing IP-based discovery against a given host, also run probes that retrieve AWS EC2 metadata. |
| `glide.discovery.discover_azure_host_metadata` | `true` | When doing IP-based discovery against a given host, also run probes that retrieve Azure metadata. |
| `glide.discovery.enable_ssm` | `false` | Enables AWS SSM-based discovery. |
| `glide.discovery.ssm.enable_windows` | `false` | Enables AWS SSM-based discovery on Windows machines as a high-level system user that can run any command. |
| `sn_disco_certmgmt.enable_csr_generation` | `false` | Enables automatic CSR generation on the Certificate Inventory and Management Request New Certificate and Request New Ceriticate (Automated) forms. |
| `sn_disco_certmgmt.find_and_attach_root_certificate` | `false` | Certificate Inventory and Management Finds the root certificate by its subject common name and links it to the certificate chain during discovery. |
| `sn_disco_certmgmt.mark_self_signed_for_incomplete_chain` | `true (if the property doesn't exist)` | Certificate Inventory and Management When discovery captures an incomplete certificate chain, sets the last captured certificate as its own root issuer and issuer. |
| `sn_disco_certmgmt.private_key_size` | `2048` | Changes the private key size when using automatic CSR generation on the Certificate Inventory and Management Request New Certificate and Request New Ceriticate (Automated) forms. |
| `sn_disco_firewall.default.rule.task.approval.group` | `Approval Group Name` | Firewall Audits and Reporting : Indicates the name of the approval group that is used to approve the firewall rule tasks. |
| `sn_disco_firewall.default.rule.task.policy.owner.group` | `Task Owner Group Name` | Firewall Audits and Reporting : Indicates the name of the assignment group that owns or is assigned to firewall rule tasks |
| `sn_disco_workspace.discovery_schedule_anomaly_detection_disabled` | `false` | Discovery Admin Workspace : Disables the anomaly detection feature. |
| `sn_disco_workspace.discovery_schedule_anomaly_detection_method` | `ML-based` | Discovery Admin Workspace : Determines the approach used for anomaly detection in Discovery schedules. |
| `sn_disco_workspace.discovery_schedule_anomaly_discover_type` | `CIs, Cloud Resources` | Discovery Admin Workspace : Determines the type of Discovery schedules for which anomaly detection is enabled, IP-based (CIs) and/or Cloud Discovery (Cloud Resources). |
| `sn_disco_workspace.discovery_schedule_anomaly_ml_model_sensitivity` | `low` | Discovery Admin Workspace : Adjusts the sensitivity for ML-based Discovery schedule anomaly detection. |
| `sn_disco_workspace.discovery_schedule_cis_discovered_anomaly_threshold` | `20` | Discovery Admin Workspace : Sets the threshold percentage for detecting anomalies in the number of configuration items (CIs) discovered during a Discovery schedule execution. |
| `sn_disco_workspace.discovery_schedule_error_anomaly_threshold` | `20` | Discovery Admin Workspace : Sets the threshold percentage for detecting anomalies in Discovery schedule error counts. |
| `sn_disco_workspace.discovery_schedule_runtime_anomaly_threshold` | `20` | Discovery Admin Workspace : Sets the threshold percentage for detecting anomalies in Discovery schedule execution time. |
| `sn_disco_workspace.discovery_stats_time_scale` | `7` | Discovery Admin Workspace : Configures the time scale for all relevant charts in Discovery Admin Workspace . |
| `sn_disco_workspace.enable_auto_create_schedules` | `false` | Discovery Admin Workspace : Enables automatic creation and management of Discovery schedules based on IPv6 network infrastructure data in IPAM. |
| `sn_disco_workspace.enable_error_framework` | `true` | Discovery Admin Workspace : Controls whether the Error Framework is active for Discovery . |
| `sn_disco_workspace.visibility_diagnostic_utility.enabled` | `false` | Discovery Admin Workspace : Enables a Virtual Agent to retrieve diagnostic information for troubleshooting issues with Discovery . |

**ECC queue and platform**

| Property | Default | Effect |
|---|---|---|
| `com.glide.codesigning.tracking.unsupported_script_tracking.enabled` | `true` | Controls script tracking for code signing on Cloud Discovery . |
| `com.snc.use_external_credentials` | `true` | Allows the use of external storage of credentials. |
| `glide.ecc_agent.validated.override` | `false` | An override for the ecc_agent validated field: If set to true, ecc_agent records will always be treated as valid. |
| `glide.eccprobe.awsrestprobe.max_retries` | `4` | Set the maximum number of times the AWS request will be retried if a rate limit exceeded error occurs. |
| `glide.eccprobe.awsrestprobe.max_wait` | `30` | Set the maximum total amount of time (seconds) the AWS request attempts to retry. |
| `glide.eccprobe.max_queued_probes_per_run` | `20` | Set the maximum number of probes a node can pick up during a run. |
| `glide.eccprobe.node_agent_id` | `NODE_AGENT` | ECC queue entries with "mid.server.${VALUE}" will be picked up and processed by the nodes. |

**Other Discovery properties**

| Property | Default | Effect |
|---|---|---|
| `glide.discovery.enable_file_tracking` | `true` | Enable configuration file tracking as part of the Pattern based Horizontal Discovery . |
| `glide.discovery.file_tracking.change_limit_count` | `4` | File Tracking: Number of changes allowed on a tracked configuration file in the defined time window. |
| `glide.discovery.file_tracking.change_limit_days` | `7` | File Tracking: Time window (in days) that limits the number of changes on a tracked configuration file. |
| `glide.discovery.file_tracking.max_file_size` | `500000` | File Tracking: The maximum file size for tracked configuration file content. |
| `glide.discovery.file_tracking.max_files_per_ci` | `50` | File Tracking: The maximum number of tracked configuration files per CI. |
| `glide.discovery.roundingInterval.cpu` | `1` | CPU speed rounding: Enter the number to round the CPU speed to. |
| `glide.discovery.roundingInterval.ram` | `1` | Memory rounding: Enter the number to round the computer RAM to. |
| `glide.discovery.shazzam_ranges_json` | `true` | Use JSON for IP ranges in Shazzam: If set to true , Discovery encodes Shazzam's IP ranges as JSON, dramatically reducing the payload size. |
| `glide.discovery.shazzam_simplify_ranges` | `true` | If set to true , Shazzam detects IPs included in multiple ranges of the same Discovery schedule and removes duplicates from all but one range. |
| `glide.discovery.sensors.netapp_native_7mode` | unset | For 7-Mode NetApp storage servers, use native discovery instead of SMI-S. |
| `glide.discovery.sensors.netapp_native_cluster_mode` | unset | For Cluster Mode NetApp storage servers, use native discovery instead of SMI-S. |

**Additional properties from Available System Properties / KB (not in the fetched Discovery Properties page)**

| Property | Default | Effect |
|---|---|---|
| `glide.discovery.debug.classification` | `false` | Logs which classifier ran and the criteria names/values. |
| `glide.discovery.ire_err_exclusion_list` | `ABANDONED, INSERT_FAILED, UPDATE_FAILED, NO_IDENTIFIER_KEYS_GENERATED` | Suppresses IRE errors from the pattern log. |
| `glide.discovery.log_debug_info` | `false` | Add ECC-derived debug information to the Discovery log. |
| `glide.discovery.log_message_chars` | `200` | Log preview/message length. |
| `glide.discovery.multi_page_serial_mode` | `false` | Process multi-page pattern payloads serially instead of in parallel; prevents duplicate CIs from concurrent multi-page payloads. |
| `glide.discovery.sam_batch_update_size` | `100` | Batch size for cmdb_sam_sw_install updates where only last_scanned changed. |
| `glide.discovery.source_name` | `ServiceNow` | Source written to sys_object_source / discovery_source. |

**IRE properties — `Configuration > CMDB Properties > Identification/Reconciliation Properties`**

| Property | Default | Effect |
|---|---|---|
| `glide.cache.size.service_cache` | `20` | Maximum cache size (in MB) that is used by the identification engine for inbound and outbound relations. |
| `glide.class.downgrade.enabled` | `true` | Allows IRE to reclassify a matched CI to a child class (downgrade). |
| `glide.class.switch.enabled` | `true` | Allows IRE to switch a matched CI to a different class. |
| `glide.class.upgrade.enabled` | `true` | Allows IRE to reclassify a matched CI to a parent class (upgrade). |
| `glide.identification_engine.batch_update_last_discovered` | `true` | Controls batch update of last_discovered field in CIs that are being processed by the identification engine. |
| `glide.identification_engine.batch_update_last_discovered.use_execute_lazy` | `true` | Sets IRE mode for processing batch updates of the discovery timestamp fields first_discovered and last_discovered . |
| `glide.identification_engine.dependent_items_local_cache_count` | `10000` | For optimization, a custom number of locally cached query result entries of dependent CIs. |
| `glide.identification_engine.dynamic_ire.auto_compare.sampling.enabled` | `true` | are true , then the system runs a comparison between Static IRE and Dynamic IRE for all payloads. |
| `glide.identification_engine.dynamic_ire_enabled` | `false` | Switches between using Dynamic IRE or Static IRE. |
| `glide.identification_engine.enable_identifier_optional_condition` | `false` | Enables advanced options for regular identifier entries in identification rules. |
| `glide.identification_engine.enable_reconciliation_filter_before_update` | `false` | Determines whether filter conditions of a reconciliation rule are applied before a value change during payload processing, or after. |
| `glide.identification_engine.granular_insert_locking` | `true` | Determines whether to use multiple granular insert locks or single global insert lock. |
| `glide.identification_engine.independent_items_local_cache_count` | `100000` | For optimization, a custom number of locally cached query result entries of independent CIs. |
| `glide.identification_engine.ire_message_listener_skip_updating_last_scan_to_now` | `false` | If RTE does not pass the ire.skip_updating_last_scan_to_now custom property on the Robust Import Set Transformer form , IRE uses the value of this property for the ire.skip_upda... |
| `glide.identification_engine.ire_message_listener_skip_updating_source_last_discovered_to_now` | `false` | If Robust Transform Engine (RTE) does not pass the ire.skip_updating_last_scan_to_now custom property on the Robust Import Set Transformer form , IRE uses the value of this prop... |
| `glide.identification_engine.lookup_match.create_duplicate_task_ci.enabled` | `false` | Enables IRE behavior of creating de-duplication tasks for duplicate related items in a lookup table detected during a lookup-based identification. |
| `glide.identification_engine.non_dependency_relation.duplicate_detection` | `false` | Sets IRE behavior when the payload contains duplicate non-dependent relationships (identical parent/child relationship type). |
| `glide.identification_engine.partial_items_process_absolute_limit` | `5000` | Absolute limit of the number of partial items for IRE to fetch, after which, IRE stops fetching partial payloads from the CMDB IRE Partial Payloads [cmdb_ire_partial_payloads] t... |
| `glide.identification_engine.partial_items_process_limit` | `2000` | Maximum number of partial items to be fetched in a single IRE call. |
| `glide.identification_engine.partial_payload_items_max_size` | `1000` | Maximum number of items allowed when creating a partial payload. |
| `glide.identification_engine.platform_domain_separation_enabled` | `false` | Toggles domain separation support mode during IRE processing. |
| `glide.identification_engine.reclassification_restriction_rules_enabled` | `true` | Globally enable or disable the application of active reclassification restriction rules. |
| `glide.identification_engine.related_items_local_cache_count` | `15000` | For optimization, a custom number of locally cached query result entries of related/lookup items. |
| `glide.identification_engine.skip_duplicates` | `true` | When true and the duplicate count is below the threshold, IRE picks the oldest CI as the match and tags the others with duplicate_of; de-duplication tasks are always created. |
| `glide.identification_engine.skip_duplicates.threshold` | `5` | If the number of duplicate CIs exceeds the threshold, then identification processes the duplicate CIs as if glide.identification_engine.skip_duplicates is set to false. |
| `glide.identification_engine.skip_sys_object_source_matching` | `false` | Determines whether IRE identification processes have the priority in being used to uniquely identify CIs in a payload, over the use of sys_object_source lookup. |
| `glide.identification_engine.skip_updating_last_scan_if_older` | `true` | Determines how IRE uses the source_recency_timestamp value in a payload to determine whether to update the last_scan attribute in the Source [sys_object_source] table. |
| `glide.identification_engine.skip_updating_source_last_discovered_if_older` | `true` | Determines how IRE updates the last_discovered and the discovery_source attributes in the CMDB. |
| `glide.identification_engine.update_without_downgrade_enabled` | `false` | Enable IRE to process CI updates with downgrade reclassification updates. |
| `glide.identification_engine.update_without_switch_enabled` | `false` | Enable IRE to process CI updates with switch reclassification updates. |
| `glide.identification_engine.update_without_upgrade_enabled` | `false` | Enable IRE to process CI updates with upgrade reclassification updates. |
| `glide.identification_logs.max_run_ids` | `1000` | Maximum number of run IDs retained in Configuration > Identification Logs. |
| `glide.reconciliation.override.null` | `true` | When true, a lower-priority source may update an empty field. |
| `glide.required.attribute.enabled` | `true` | When true, required attributes may not be null during identification and reconciliation. |

**MID Server properties — `config.xml` / MID Server Properties**

| Property | Default | Effect |
|---|---|---|
| `com.glide.closure_max_rows_per_table` | `200000` | Sets the maximum number of rows allowed in a table. |
| `glide.stored_proc.data_type.validation` | `false` | Stops validation of data types in stored procedure parameters. |
| `mid.aws.sts.assume_role.credential_ttl_minutes` | `60` | Set the number of minutes you want to cache temporary credentials for Cloud Discovery. |
| `mid.aws.sts.assume_role.disable_credential_caching` | `false` | Set this property to true to prevent the caching of temporary credentials for Cloud Discovery. |
| `mid.ca.certificate.api.request.retry.count` | `3` | Indicates how many times the Certificate Import query will retry after the rate limit has occurred. |
| `mid.ca.certificate.api.request.retry.interval` | `30000` | Used to delay Certificate import from CAs when the rate limit has occurred. |
| `mid.cloud.discovery.bypass.proxy` | `none` | This configuration parameter accepts a comma separated list of DNS/IP addresses of proxy servers. |
| `mid.discovery.aws_ssm.kms_key_name` | `none` | Using a dedicated key enhances security by verifying that applicative credentials are encrypted and securely retrieved at runtime, without being exposed in plain text. |
| `mid.discovery.aws_ssm.kms_key_region` | `none` | Using a dedicated key enhances security by verifying that applicative credentials are encrypted and securely retrieved at runtime, without being exposed in plain text. |
| `mid.discovery.aws_ssm.linux.fallback_root_user` | `false` | When the glide.discovery.enable_ssm property is enabled, AWS SSM Discovery on Linux defaults to using the root user for command execution. |
| `mid.discovery.aws_ssm.s3_bucket_name` | `none` | Because the SSM Run Command console has a 24,000-character limit, results that exceed this limit must be stored in and retrieved from an S3 bucket. |
| `mid.discovery.aws_ssm.s3_bucket_region` | `none` | Because the SSM Run Command console has a 24,000-character limit, results that exceed this limit must be stored in and retrieved from an S3 bucket. |
| `mid.discovery.file_transfer_protocol` | `SCP` | Used to determine the file transfer method used for probes or patterns. |
| `mid.discovery.max_ci_count_per_page` | `500` | Sets the maximum number of CIs per ECC queue page during horizontal discovery. |
| `mid.discovery.max_pattern_payload_size` | `50000000` | Defines the maximum overall payload size for the payload of results that come from patterns. |
| `mid.discovery.max_payload_size` | `5000000` | Specifies the maximum string length of Discovery results that the MID Server sends to the instance. |
| `mid.discovery.max_related_count_per_page` | `100` | Sets the maximum number of related items per chunk during horizontal discovery. |
| `mid.discovery.max_relation_count_per_page` | `10000` | Sets the maximum number of relations per ECC queue page during horizontal discovery. |
| `mid.discovery.max_total_items_size_per_page` | `3145728 (3 MB)` | Sets the maximum size limit per ECC queue page during pattern-based discovery. |
| `mid.discovery.multiprobe.skip_others_on_error` | `true` | Prevents probes in a multi-probe from iterating through available credentials when another member probe has already failed or timed out. |
| `mid.discovery.should_minify_pattern_payload` | `false` | Enables JSON minification for pattern payloads. |
| `mid.eccq.max_payload_size` | `20000000` | Specifies the maximum string length of a payload that the MID Server sends to the instance. |
| `mid.http_classy.allow_credentials_over_http` | `false` | Enables the HTTP Classify probe to send credentials over the HTTP protocol during discovery. |
| `mid.install_server.base_uri` | `https://install.service-now.com` | Modifying this system property requires maint privileges. |
| `mid.jdbc.datastream.fail.when.attachement.limit.exceeded` | `true` | Specifies if the data up to 4GB (four attachments, each of size 1GB) can be retrieved from the RDBMS. |
| `mid.jdbc.datastream.max.record.size` | `64` | Specifies the maximum record size in KB. |
| `mid.keystore.backup_overwrite_timespan` | `60` | Specifies the number of seconds from the current backup time to determine if a the most recent backup in that time span should be replaced by the new one instead of creating a n... |
| `mid.keystore.max_backups` | `3` | Specifies the maximum number of backups from manual key store operations through the manage_certificate script. |
| `mid.keystore.max_live_backups` | `2` | Specifies the maximum number of live backups from running MID server. |
| `mid.log.command_audit.enable` | `false` | Enables the MID Server command audit log. |
| `mid.powershell.target_base_dir` | `admin$\temp` | Specifies the location of the target base folder used for Discovery using WMI. |
| `mid.probe.collect_debug_info` | `false` | An optional property to collect debug information. |
| `mid.probe.use_legacy_forward_dns` | `false` | Enables the legacy DNSNameResolver probe and disables the default DNSNameResolver probe. |
| `mid.probe.use_legacy_reverse_dns` | `false` | Enables the legacy DNS probe and disables the default DNS probe. |
| `mid.process_flow.log_listener.max_size` | `10485760` | Sets the maximum size in bytes of memory available to save log messages for Workflow Studio actions running on a MID Server. |
| `mid.property.jdbc_operations` | `:` | Tells the JDBCOrchestrationProbe what JDBC operations it is allowed to execute. |
| `mid.property.jms.command.allowed_factory_names` | `connectionFactory, queueConnectionFactory,` | Comma delimited list of Java Messaging Service (JMS) connection factories that the MID Server requires for a custom JMS activity or action. |
| `mid.property.powershell.use_base64_password` | `false` | If the Credential is set to be specific to certain MID Servers, then the property can also be set to those same MID Servers. |
| `mid.property.ssh.use_snc` | `true` | Enables the use of the SNCSSH client for Discovery and Orchestration. |
| `mid.sa.prefer_powershell` | `true` | Enables MID Server to use PowerShell Remoting.Note: It is not recommended to change this property as it is being deprecated. |
| `mid.sa.ssh.use_sncssh` | `true` | Toggles SSH between non-interactive and interactive modes. |
| `mid.sa.windows.allowable_failures` | `2` | Specifies the number of allowable failures before the MID Server stops executing the pattern. |
| `mid.servicewatch.max_concurrent_connections` | `7` | Defines the maximum number of concurrent tasks sent to an individual host by a single MID Server. |
| `mid.servicewatch.num_paths_linux_netstat_to_check` | `5` | Define the maximum number of installation paths to use during discovery of Linux servers. |
| `mid.servicewatch.num_paths_linux_ss_to_check` | `5` | Define the maximum number of installation paths to use during discovery of Linux servers. |
| `mid.servicewatch.use_full_linux_netstat_path` | `true` | Controls if the netstat command is executed with its full installation path. |
| `mid.servicewatch.use_full_linux_ss_path` | `false` | Controls if the ss command is executed with its full installation path. |
| `mid.shazzam.max_scanners_per_thread` | `100` | Specifies the number of concurrent scanners processed by each Shazzam thread. |
| `mid.shazzam.regulator.interval_ms` | `1` | Sets the interval, in milliseconds, in which Shazzam can launch packets. |
| `mid.shazzam.regulator.packets_per_interval` | `1` | Sets the number of packets that Shazzam can launch in the time interval specified by the mid.shazzam.regulator.interval_ms property. |
| `mid.shazzam.threads` | `5` | Specifies the number of concurrent threads that Shazzam uses. |
| `mid.sm.discolog.max_log_size` | `1000` | Limits the length of the log statements in the Horizontal Discovery Log. |
| `mid.sm.discolog.max_object_size` | `5000` | Limits the length of the object in the Horizontal Discovery Log. |
| `mid.snmp.use_getbulk` | `true` | Specifies whether to use GETBULK to receive a large amount of data in batches. |
| `mid.ssh.algorithms.cipher` | `:` | Modifies the Cipher SSH algorithm priority list. |
| `mid.ssh.algorithms.host_key` | `:` | Modifies the Host Key SSH algorithm priority list. |
| `mid.ssh.algorithms.kex` | `:` | Modifies the Key Exchange SSH algorithm priority list. |
| `mid.ssh.algorithms.mac` | `:` | Modifies the MAC SSH algorithm priority list. |
| `mid.use_net_tools` | `true` | Enables or disables the use of net-tools commands during discovery of devices running on the Linux operating system. |

**Duplicate CI remediation properties — `Configuration > CMDB Properties > Duplicate CI Remediator Properties`**

| Property | Default | Effect |
|---|---|---|
| `glide.duplicate_ci_remediator.dry_run` | `false` | When set to false (default value), updates specified in the wizard are actually performed. |
| `glide.duplicate_ci_remediator.enable_restricted_mode` | `false` | Enables restricted mode remediation in the Duplicate CI Remediator. |
| `glide.duplicate_ci_remediator.max.cis` | `1000` | Maximum number of CIs processed per de-duplication task (<= 5000). |
| `glide.duplicate_ci_remediator.max.field_length` | `4000` | If the max_length for an attribute is equal to the property value, and the size of the data exceeds the property value, then the data is truncated to the property value and the ... |
| `glide.duplicate_ci_remediator.merge_related_items_enhanced` | `true` | Enables the capability to ignore database errors and/or skip ALL business rules (disable workflow) in related tables referencing CIs, during duplicate CI remediation. |
| `glide.duplicate_ci_remediator.related_items_blacklist` | `cert_task.cmdb_ci,cert_audit_result.configuration_item,discovery_log.cmdb_ci,alm_hardware.ci,alm_asset.ci,fm_expense_line.ci` | Related-item tables excluded from merge during remediation. |

**CMDB Health properties**

| Property | Default | Effect |
|---|---|---|
| `glide.cmdb.health.ci_ownership_field` | `managed_by_group` | Attribute in the [cmdb_ci] table that the CMDB Health Dashboard uses to determine CI ownership. |
| `glide.cmdb.health.src.cmdb_health_audit_only` | `false` | When set to true, disables health results from sources other than CMDB Health audit (such as Cloud Discovery). |
| `glide.cmdb.health.staleness_exclude_dependent_cis` | `false` | Exclude dependent CIs for the staleness CMDB Health metric. |
| `glide.cmdb.logger.use_syslog.CMDBHealth` | `error` | A comma-separated list that controls the level of logging of CMDB Health jobs. |
---

## 5. IRE deep dive

### 5.1 Identification Rules (IRE identifiers)

Anatomy:

- one CI **identifier** per rule;
- one or more **identifier entries** (unique attribute sets) with different priorities;
- optional **related entries** for related/lookup items (not used to identify the CI);
- `Applies to` class; rules are inherited by child classes unless the child defines its own rule (then the parent's rule and entries no longer apply to the child);
- **required attributes** cannot be empty (`glide.required.attribute.enabled`, default `true`);
- **criterion attributes** are the unique attribute sets used for matching.

**Identifier entry types:**

| Entry type | Matching fields come from | Guidance |
|---|---|---|
| **Regular** | The CI's own table (or inherited `cmdb_ci` fields) | Preferred; cheapest and least ambiguous |
| **Lookup** | A related table that references the CI (e.g., `cmdb_ci_network_adapter` for MAC, `cmdb_serial_number`) | Costs a join; use only when the identifying attribute genuinely lives on the related table. Prefer `Enforce exact count match`. |
| **Hybrid** | Both the CI table and a related table | Use when neither source alone is unique |

**Priority rules:**

- Lowest `Order` runs first; custom identifiers must use a different order from defaults.
- Put the **strongest** identifier entry first.
- Limit entries, ideally to **one**; each extra entry costs performance.
- Avoid **lookup** identifier entries; they are explicitly discouraged for performance.
- Disable a rule (`Active = false`) rather than deleting it if you need to stop it temporarily.
- Do not add `sys_class_name` as an attribute for an independent rule. If matching depends on class, create a rule per class and set `Applies to`.
- Optional condition on entries narrows the match scope; requires `glide.identification_engine.enable_identifier_optional_condition = true` (default `false`). Review pre-configured entries first.

**Default rules in the base system:**

| Rule | Applies to | Attributes |
|---|---|---|
| Hardware Rule | `cmdb_ci_hardware` | `serial_number`, `serial_number_type`, `name`, `ip_address`, `mac_address`; plus Serial Number and Network Adapter lookup tables |
| ESX Server Rule | `cmdb_ci_esx_server` | `correlation_id` |
| Storage Server Rule | `cmdb_ci_storage_server` | `cim_object_path`, `name`, `serial_number`, `serial_number_type`, `mac_address`, `ip_address`; plus Serial Number and Network Adapter |
| WBEM Service Rule | `cmdb_ci_wbem_service` | `cim_object_path` |

**Source-native-key fast path:** a payload `sys_object_source_info` with `source_name` + `source_native_key` can match directly, without consulting identifier rules. `glide.identification_engine.skip_sys_object_source_matching` (default `false`) forces rule-based matching even when source keys exist — use it when source keys are stable but identifying attributes churn, which can otherwise create duplicates.

**Inclusion rules** narrow which existing CIs participate in identification and in the CMDB Health duplicate metric. They affect every script that calls IRE, so apply them narrowly. Base system has none. Do not use `Class` as a condition on a parent class such as `cmdb_ci_hardware`; the inclusion rule applies to all child classes and can cause child classes not to be found.

### 5.2 IRE Data Source Rule (insert-only)

**Purpose:** prevent a specific discovery/data source from **creating** new CIs of a class. It is a **create-only gate**, not an attribute-level update restriction, and it does not block updates to CIs that already exist.

- Stored in `cmdb_ire_data_source_rule`.
- Configuration: `All > Configuration > Identification/Reconciliation > IRE Data Source Rule` (the CMDB learning guide shortens this to **Data Sources**).
- Fields: **Active**, **Applies to** (CI class and children), **Data source**, **Insert Not Allowed**.
- Child classes inherit the rule; a child-class rule overrides the parent.
- It is evaluated **only when identification found no match** and IRE is about to insert.
- It has no effect on updates. A source blocked from inserting can still update an existing CI, subject to Reconciliation Rules.
- It works independently of **static** reconciliation priority and cannot authorize or deny individual attributes. Official docs state it has no impact once **dynamic reconciliation** is in effect.
- A blocked insert logs `INSERT_NOT_ALLOWED_FOR_SOURCE`. With `CreateOrUpdateCIEnhanced()` the item is stored as a partial payload; `createOrUpdateCI()` does not allow partial commits, so the whole payload can fail.
- IRE Data Source Rules do not apply to lookup or related items, and only one rule can be active for a given class/source pair.
- Later payloads in which the non-permitted source updates the respective CI run successfully; IRE allows the previously blocked source to update the CI once it exists.
- When a permitted source later inserts the same CI, IRE merges the stored partial payload, deletes it, and re-permits updates by the previously-blocked source.

**Example:** an IP-scan tool that discovers network gear but creates thin server CIs. Block that source from inserting `cmdb_ci_server`; it can still update server CIs that Discovery already created.

### 5.3 Reconciliation Rules (update-only)

**Purpose:** after Identification matches an existing CI, decide **which source may update which attribute**. Reconciliation is **update-only**; it is not applied when IRE inserts a new CI.

| Type | Basis | Precedence | Requirements |
|---|---|---|---|
| **Static** | Source priority per class/attribute | Lower than dynamic for the same attribute | A rule per authorized source/attribute; stored in `cmdb_reconciliation_definition` |
| **Dynamic** | Attribute values processed by CMDB 360 (e.g., largest/most-reported) | **Wins** over static for the same attribute | CMDB 360 must be enabled; one dynamic rule per class attribute; stored in `cmdb_dynamic_reconciliation_definition` |

**Key behaviors:**

- **Priority:** lower number = higher priority. But **scope is evaluated first**: an attribute-specific rule beats an "Apply to all attributes" rule even when the attribute-specific rule has a higher (worse) priority number.
- Child-class rules override parent-class rules.
- A rule with an empty attribute list authorizes all attributes in the class; specific attribute rules override broader rules.
- Overlapping static rules for the same attribute can coexist; IRE enforces them so sources do not overwrite each other.
- Per-rule fields: `Active`, `Discovery source`, `Priority`, `Apply to all attributes` vs. an explicit `Attributes` list, `Update with Null`, and `Filter Condition`.
- A rule with `Update with Null` can set the listed attributes to null; without it, a source cannot null out a populated field.
- `Filter Condition` scopes the rule to a row subset (for example, `Department is Finance`). `glide.identification_engine.enable_reconciliation_filter_before_update` (default `false`) controls whether the filter runs before or after values change.
- You **cannot** create a reconciliation rule for system fields or IRE-specific fields such as `discovery_source`, and rules **cannot be dot-walked** through reference fields.
- `glide.reconciliation.override.null` (default `true`) allows a lower-priority source to fill an empty field.
- Data precedence (which source's value wins) is tracked in `cmdb_datasource_last_update`.
- Reconciliation is not a duplicate detector. If duplicate CIs are found, handling is governed by the duplicate properties and de-duplication tasks in §6.

### 5.4 Data Refresh Rules (update-only, staleness)

**Purpose:** let a lower-priority source refresh a field when the higher-priority source's data has gone **stale**. Data Refresh is **update-only**; it never applies to a new insert.

- In the official docs, Data Refresh Rules are created from **CI Class Manager → Hierarchy → select the class → Class Info → Reconciliation Rules → Data Refresh Rules → Add**, with fields: **Discovery source**, **Effective Duration**, and **Active**.
- The CMDB learning guide describes the same behavior as settings on a reconciliation rule: **Refreshable** plus a **Stale threshold** (for example, 90 days). Treat these as the same mechanism with different UI wording across releases.
- **Effective Duration / Stale threshold = 0** (the default) means the CI is immediately stale for that source, so a lower-priority source is always authorized to refresh.
- The refresh can only write fields the lower-priority source is authorized to update by Reconciliation Rules.
- Data Refresh has **no effect** when dynamic reconciliation rules are in effect.
- Field-specific rules are safer than "Apply to all": staleness on `name` should not block a refresh of `serial_number`.
- Avoid ping-pong between two sources alternately refreshing each other. Use strict priority for identity fields (serial number, name) and staleness-aware refresh only for non-identifying attributes.

### 5.5 Reclassification

IRE can upgrade, downgrade, or switch a CI's class when a match is found. Controls:

- `glide.identification_engine.update_without_upgrade_enabled` (default `false`)
- `...update_without_downgrade_enabled` (default `false`)
- `...update_without_switch_enabled` (default `false`)
- `glide.class.upgrade.enabled`, `glide.class.downgrade.enabled`, `glide.class.switch.enabled` (default `true`)
- reclassification restriction rules (`glide.identification_engine.reclassification_restriction_rules_enabled`, default `true`)
- payload `settings` flags `updateWithoutUpgrade`, `updateWithoutDowngrade`, `updateWithoutSwitch` take precedence over system settings
- automatic reclassification can be disabled, producing a **reclassification task**

### 5.6 Partial and incomplete payloads

- **Partial item:** lacks enough data for unique identification *but* has `source_name`/`source_native_key` or enough identifying context; stored in `cmdb_ire_partial_payloads` and retried when a later payload completes it.
- **Incomplete item:** lacks unique identification and has a non-partial error; stored in `cmdb_ire_incomplete_payloads` for logging and never retried.
- Partial payloads older than **90 days** are deleted.
- `glide.identification_engine.partial_payload_items_max_size` (default **1000**) bounds one partial payload; larger payloads are split.
- `glide.identification_engine.partial_items_process_limit` (default **2000**) and `...partial_items_process_absolute_limit` (default **5000**) bound partial-item fetches per IRE call.
- `CreateOrUpdateCIEnhanced()` enables partial payloads, partial commits, payload de-duplication, and optional summaries. `createOrUpdateCI()` does not allow partial commits: one blocked insert can fail the whole payload.

### 5.7 IRE performance guardrails

- Limit each payload to **500 CIs**.
- Do not send duplicate items in one payload.
- Do not send system fields (`sys_domain`, `sys_updated_on`, `sys_mod_count`, etc.).
- Send only the criterion attributes required by the identification rule.
- Use `sys_id` when available; IRE can locate the CI directly.
- When inserting many CIs that depend on the same parent, **serialize** API calls to avoid clogging the system.
- `glide.identification_engine.granular_insert_locking` (default `true`) uses multiple granular insert locks; set `false` if lock contention is observed.
- `glide.identification_engine.batch_update_last_discovered` (default `true`) batches `last_discovered` updates; set both it and `...use_execute_lazy` false for immediate consistency / deletion-race workarounds.

### 5.8 Additional IRE internals and tables

These are documented internals that explain behavior and are useful when debugging:

| Item | Type | Purpose |
|---|---|---|
| `cmdb_datasource_precedence` | table | Ranked source list used by reconciliation on releases that expose it |
| `cmdb_datasource_last_update` | table | Per-attribute record of which source last wrote the value; the first place to check when reconciliation "does not work" |
| `cmdb_datasource_staleness` | table | Non-CMDB Data Source Staleness Definitions (`cmdb_datasource_staleness.list`) |
| `source_recency_timestamp` | payload field | Resolves same-key conflicts; the newer payload wins wholesale, and relationships from the older payload are discarded |
| `cmdb_dynamic_ire_skip_class` | table | Class exemptions that keep a class on static IRE while dynamic IRE is enabled |
| `glide.identification_engine.dynamic_ire.auto_compare` | property | When true, runs a comparison between Static IRE and Dynamic IRE for all payloads without switching |
| `glide.identification_engine.platform_domain_separation_enabled` | property | Toggles domain separation support mode during IRE processing |
| `glide.identification_engine.non_dependency_relation.duplicate_detection` | property | Detects duplicate non-dependent relationships (identical parent/child relationship type) in a payload |
| `glide.identification_engine.skip_updating_source_last_discovered_if_older` | property | Uses `source_recency_timestamp` to avoid rolling back `last_discovered` / `discovery_source` from a stale payload |
| `glide.identification_engine.skip_updating_last_scan_if_older` | property | Same idea for the `last_scan` attribute in `sys_object_source` |
| `glide.identification_engine.ire_message_listener_skip_updating_source_last_discovered_to_now` / `...last_scan_to_now` | properties | RTE fallback controls when the Robust Import Set Transformer does not pass the custom properties |
| `glide.identification_engine.batch_update_last_discovered` / `...use_execute_lazy` | properties | Batch `first_discovered` / `last_discovered` updates; set both false for immediate consistency |
| `glide.identification_engine.granular_insert_locking` | property | Multiple granular insert locks vs. one global lock; set false on lock contention |
| `glide.cache.size.service_cache` | property | Maximum cache size (MB) for inbound/outbound relations (default `20`) |
| `glide.identification_engine.related_items_local_cache_count` / `...dependent_items_local_cache_count` / `...independent_items_local_cache_count` | properties | Local cache entry counts (defaults `15000` / `10000` / `100000`); `0` disables the cache |
| `glide.identification_logs.max_run_ids` | property | Cap on run IDs retained in `Configuration > Identification Logs` (default `1000`) |

---

## 6. Duplicate prevention and insert-vs-update control

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
| No data change | **No write** | `sys_updated_on` is not refreshed; `last_discovered`/`discovery_source` still update |
| Rediscovered Retired CI | **Not auto-un-retired** | Lifecycle fields such as `install_status` are typically not in the OOTB Discovery payload |

### 6.2 Root causes of duplicate CIs

1. **Weak identification rules** — matching on `name` alone, or on a lookup entry that is not unique.
2. **Contradicting identification rules** — a parent lookup entry and a child class-level identifier for the same table.
3. **Inclusion rules scoped by class on a parent** — child classes are not found by IRE.
4. **ACLs or query business rules hiding CIs from IRE** — the CI exists but cannot be read.
5. **Existing CI has `duplicate_of` set or `discovery_source = Duplicate`** — IRE skips it by default.
6. **Same CI discovered concurrently / same dependent CI in multiple payloads** — sequence schedules or de-duplicate in the pattern.
7. **Multi-page payloads processed in parallel** — set `glide.discovery.multi_page_serial_mode = true` on pattern-heavy estates (default documented as `false`).
8. **Identifying attributes empty/null** — keep serials intact; require non-null identifiers.
9. **Patterns/sensors rewriting serial numbers** — remove the transformation.
10. **Manually created CIs with empty discovery source** — populate/retire; let CMDB Health flag them.
11. **Custom identifier never runs** — same `Order` as a default rule, or `Active` cleared.
12. **Reconciliation blocks update** — tune reconciliation; do not hand-create CIs.
13. **High-priority source silent** — add a Data Refresh Rule.
14. **Untrusted source creates detail-less CIs** — add an IRE Data Source Rule with `Insert Not Allowed`.
15. **IP reuse / DHCP** — two devices share an address over time; MAC/NIC bonding complicates this further.
16. **Hostname churn / adapter renames** — a renamed bonded NIC can produce an Absent record plus a new CI.

### 6.3 Prevention controls, by layer

**Design-time (CI Class Manager):**

- Model each class with a **complete independent identifier**; prefer independent rules.
- Put the strongest identifier entry at the **highest priority**; keep one entry where possible; avoid lookup entries.
- Add **required attributes** and **identification inclusion rules** where appropriate.
- Define **dependent relationship rules** (hosting/containment) only for genuinely dependent CIs; keep dependency depth ≤ 2.
- Create the rule at the correct class level; remember child rules override parent rules.
- Do not define a lookup-based identifier for a child table in a parent's rule and a class-level identifier for that child.

**Runtime (properties and IRE):**

- `glide.identification_engine.skip_duplicates = true` lets IRE pick the oldest match for small duplicate sets instead of failing.
- `glide.identification_engine.skip_duplicates.threshold = 5` is the safety bound; above it, identification fails as if skip were false.
- `glide.identification_engine.skip_sys_object_source_matching = true` prioritizes identification-rule matching over the `sys_object_source` shortcut.
- `glide.identification_engine.lookup_match.create_duplicate_task_ci.enabled = false` (default) selects the older CI for lookup matches without a de-dup task; set `true` when such lookup duplication must be remediated.
- Use **IRE Data Source Rules** to stop untrusted sources from inserting a class; they can still update existing CIs.
- Use **Reconciliation Rules + Data Refresh Rules** so only the authoritative source writes, and stale data can be refreshed.
- Enable **dynamic reconciliation** only with CMDB 360; it wins over static rules.
- Set `glide.duplicate_ci_remediator.max.cis` deliberately for large duplicate sets.
- `glide.discovery.enable_mac_address_verification = true` on DHCP fleets.
- `glide.discovery.enforce_unique_ips` only if IP uniqueness is a hard invariant.

**Detection:**

- IRE always creates **de-duplication tasks** when it detects duplicate sets.
- `duplicate_of` references the main CI; the main CI has an empty `duplicate_of`.
- **CMDB Health** duplicate metrics and the **Identification Log** expose trends.
- **Identification simulation** (`All > Configuration > Identification/Reconciliation > Identification Simulation`) lets you test a payload without committing.

**Remediation:**

- **Bulk:** CMDB Workspace De-duplication Dashboard + Template Library; create templates per class, review tasks, run templates in bulk.
- **Single task:** Duplicate CI Remediator wizard; choose the main CI, then merge attributes, relationships, and related items (or retain the main CI as-is).
- Asset-related tables are **not** merged by default; inactive change requests referencing a duplicate CI have the CI field cleared rather than merged.
- Related-table workflows can be disabled during remediation via `glide.duplicate_ci_remediator.merge_related_items_enhanced` plus an entry in `reconcile_duplicate_related_table_config`.
- Templates do not retroactively update already-created de-duplication tasks; the template class condition is evaluated at CI level, not task level.
- Do not set `duplicate_of` by hand: the main CI cannot itself be a duplicate; if the main CI becomes a duplicate, its duplicates re-point; a duplicate of `Unknown` blocks remediation.
- Updating any attribute other than `duplicate_of` on a duplicate CI clears its duplicate status.

### 6.4 De-duplication properties

| Property | Default | Effect |
|---|---|---|
| `glide.duplicate_ci_remediator.dry_run` | `false` | Rehearse remediation without changing data; run with `true` first |
| `glide.duplicate_ci_remediator.max.cis` | `1000` (≤ 5000) | Caps de-duplication processing for large sets |
| `glide.duplicate_ci_remediator.max.field_length` | `4000` | Attributes longer than this are excluded from Select Main/Merge |
| `glide.duplicate_ci_remediator.related_items_blacklist` | `cert_task.cmdb_ci`, `cert_audit_result.configuration_item`, `discovery_log.cmdb_ci`, `alm_hardware.ci`, `alm_asset.ci`, `fm_expense_line.ci` | Related items not merged |
| `glide.duplicate_ci_remediator.merge_related_items_enhanced` | `true` | Ignore DB errors / skip workflows on related tables so remediation completes |
| `glide.duplicate_ci_remediator.enable_restricted_mode` | `false` | Use for complex estates |

---

## 7. CI Class Manager — breadcrumbs and tab map

### 7.1 Access

```
All > Configuration > CI Class Manager
```

- `sn_cmdb_admin` — full access.
- `sn_cmdb_editor` — read-only.
- Child-class creation may also require `personalize_dictionary`; dependent-rule write access may require `itil` / `itil_admin`; Identification Simulation may require `sn_cmdb_admin` + `admin`.
- CI Class Manager **does not support non-CMDB tables**; use the non-CMDB IRE procedures for those.
- It centrally manages class definitions, IRE settings, CMDB Health, and some Service Mapping definitions.

### 7.2 Navigation

```
CI Class Manager
└── Hierarchy (CI Classes list)
    └── <select a class>
        ├── Class Info
        │   ├── Basic Info (display name, table name, description, icon, extensible, principal class)
        │   ├── Attributes (set Identification = true on identifier columns)
        │   └── Suggested Relationships
        ├── Identification
        │   ├── Identification Rule (IRE identifier; identifier entries, priorities)
        │   └── Identification Inclusion Rule (advanced scoping)
        ├── Reconciliation Rules
        │   ├── Reconciliation Rule (static priority; dynamic via CMDB 360)
        │   └── Data Refresh Rule (staleness; Refreshable + Stale threshold)
        ├── Dependencies
        │   └── Hosting / containment dependent relationship rules
        ├── All Relationship Rules
        ├── Health
        │   ├── Compliance audit
        │   ├── Certification template
        │   ├── Orphan rule
        │   ├── Staleness rule
        │   ├── Recommended/mandatory attributes
        │   └── Health inclusion rule
        └── CI List
```

**IRE Data Source Rules are not a CI Class Manager tab.** They are class-level and live outside the tool at `All > Configuration > Identification/Reconciliation > IRE Data Source Rule` (the CMDB learning guide calls the navigator entry **Data Sources**).

### 7.3 Creating a child class — wizard order

1. **Provide Basic Info** — display name, table name (`u_cmdb_ci…` prefix is fixed), description, icon, extensible, principal class.
2. **Add Attributes** — add columns; mark an attribute as an identifier by setting its **Identification** column to `true`.
3. **Set Identification Rule** — inspect the derived rule; **Replace** it to define class-specific identifier entries.
4. **Dependencies** — add dependent rules (only shown when dependent identification rules exist). Hosting rules are stored in `cmdb_metadata_hosting`; containment and reference rules are managed in the **Metadata Editor** (`All > Configuration > Metadata Editor`), which is synchronized with CI Class Manager.
5. **Add Reconciliation Rules** — add Reconciliation Rules and Data Refresh Rules.
6. **Add Suggested Relationships** — review/add relationship targets.
7. **Done.**

### 7.4 Suggested relationships

- Path: CI Class Manager → select class → **Suggested Relationships** → **New** → choose Relationship + Target Class → **Save**; or `All > Configuration > Relationships > Suggested Relationships` → **New**.
- Fields: `Base class`, `Relationship`, `Dependent class`.
- Removing a suggested relationship does not affect relationships already created/updated by Discovery.

### 7.5 Health

- CMDB Health exposes **completeness**, **correctness**, and **compliance** KPIs.
- The duplicate metric only evaluates CIs with identification rules that have empty discovery source or an active de-duplication task; two CIs with identical name+serial and both `discovery_source = ServiceNow` are not reported unless a de-dup task exists.
- Orphan and staleness metrics feed correctness.
- The Health widget shows "not applicable" when duplicate scoring has no identification rules on the class or an ancestor, or orphan scoring has no orphan rules and health inclusion rules.

---

## 8. Validation and observability

| What | Where | What to look for |
|---|---|---|
| Discovery Status | `Discovery > Status` | Per-run state, completed/current activity, Discovery Devices, ECC queue tab |
| Per-device history | `discovery_device_history` | Per-device phase/state outcome per run |
| ECC Queue | `% ecc_queue` | Raw probe/pattern XML payloads; input vs output, ready/processed/error |
| Discovery Log | `Discovery > Discovery Log` | Debug/Info/Warning/Error by probe, device, CI, ECC input |
| Discovery Home | `Discovery > Home` | Tiles: Schedules, Discovered Devices, Cloud Resources, Errors |
| CI Identification Log | `Configuration > Identification Logs` | Identification decisions; enable with `glide.discovery.debug.ci_identification` |
| Identification simulation | `Configuration > Identification/Reconciliation > Identification Simulation` | Payload output and execution log **without** committing |
| CMDB Health | CMDB Workspace / Health dashboard | Duplicate, orphan, staleness, compliance KPIs |
| Discovery timeline | `Show Discovery Timeline` | Every probe/sensor/pattern with queueing vs processing time and ECC records |
| CMDB audit | `All > System Definition > Audit > Audit History` | Filter `table_name = cmdb_ci` |

**Debug properties (use temporarily, then revert):**

- `glide.discovery.debug.ci_identification = true`
- `glide.discovery.debug.classification = true`
- `glide.discovery.log_debug = true` / `glide.discovery.log_debug_info = true`
- `glide.cmdb.logger.source.identification_engine = debug`
- `mid.probe.collect_debug_info = true`

All are performance killers at scale.

---

## 9. Troubleshooting matrix

| Symptom | Likely cause / first check |
|---|---|
| Device never matched; new CI daily | Weak identifier entries; check serials; check `glide.discovery.use_cmdb_identifiers`; read Identification Logs |
| `Active, couldn't classify` | Credential/protocol/port problem at classification; HTTP-classified Windows boxes usually mean WMI/SSH/SNMP credentials are broken |
| Classifies but never `Identified CI` | Identity probe or IRE problem at identification |
| Bonded-NIC host duplicates | `name` missing from the class rule; confirm both adapters differ by `name` and the name is not reused |
| Adapter rename → Absent + re-create | Known name-rule behavior; do not rename bonded NIC labels |
| CI count flat, errors spike | Credentials expired; credential affinity stale (`dscy_credentials_affinity`); MID clock/cert; ECC backlog |
| Schedule runs, no probes sent | MID down/not validated; `mid.*` max queued probes; ECC queue processing paused |
| Insert blocked, `INSERT_NOT_ALLOWED_FOR_SOURCE` | IRE Data Source Rule for source×class |
| Whole payload fails, not partial | Plain `createOrUpdateCI()` — switch to `CreateOrUpdateCIEnhanced()` |
| Duplicates from import sets | Route through `CMDBTransformUtil` / IRE application services |
| Lower-priority source cannot fill empty field | `glide.reconciliation.override.null=true` (default true) |
| Stale `last_discovered` never updates | Payload older than CMDB — expected; inspect `glide.identification_engine.skip_updating_source_last_discovered_if_older` |
| Duplicates found weekly | De-dup task spike = identification rule weakness; remediation: `dry_run` + templates |
| Reconciliation rules seem not to work | Check `cmdb_datasource_last_update`; check child-class overrides; check `Filter Condition` |
| Missing router CIs | Temporarily remove `NO_IDENTIFIER_KEYS_GENERATED` from `glide.discovery.ire_err_exclusion_list` |
| Discovery slow mid-run | Check Shazzam regulator packet rate and MID CPU; check `mid.discovery.multiprobe.skip_others_on_error` |
| Payload dropped on size | `mid.discovery.max_payload_size`, `mid.eccq.max_payload_size` |
| CI listed as Absent then duplicate created | Adapter/host renamed; name-rule mismatch |
| Reclassification silently blocked | Reclassification tasks piling up; inspect `glide.class.*` and `update_without_*` |
| CMDB huge / Principal Class empty | Filter rule excludes extended classes incorrectly |

---

## 10. Runbook — deploy Discovery into a new subnet

1. **MID host:** service account, Java 17+, outbound 443 to `<instance>.service-now.com` + `install.service-now.com`, validate green.
2. **Credentials:** credential set for the subnet (WMI read-only + SSH + SNMPRO/SNMPv3 authPriv), test on one host with Quick Discovery.
3. **Identifiers:** verify identifier rules for Windows/Linux (defaults are usually fine); confirm `glide.discovery.use_cmdb_identifiers=true`; enable `glide.discovery.enable_mac_address_verification=true` on DHCP fleets; leave `enforce_unique_ips=false` until shared IPs are known.
4. **Reconciliation:** create rules for `Discovery` plus any rival sources; at minimum attribute-scope `name`; full-class authorization for trusted sources, attribute-scoped for risky ones.
5. **Data source rules:** add an IRE Data Source Rule only if a low-fidelity source must be blocked from inserting server-class CIs.
6. **Schedule:** name, MID/cluster, ranges, `Discover=CIs`, off-peak window, one replica.
7. **Run once:** check Home tiles + Identification Logs + de-dup task count. If > 3, stop and tune rules, then resume.
8. **Operate:** freeze Discovery credential rotation cadence; document `dscy_credentials_affinity` remediation for on-call; weekly de-dup triage + stale-check review + MID version; monthly property drift audit against the baseline catalogs in §4.9.

---

## 11. Cross-agent consensus, conflicts, and resolutions

### 11.1 Consensus (multiple independent sources)

| Finding | Sources |
|---|---|
| Four IRE rule families; Data Source insert-only; Reconciliation/Data Refresh update-only | deepseek-v4-pro matrix, deepseek-flash reference, CMDB learning guide |
| Four phases: scan → classify → identify → explore | all agents, Discovery learning guide |
| `skip_duplicates=true` + threshold 5: oldest becomes main, others `duplicate_of`; de-dup tasks always created | deepseek-v4-pro, deepseek-v4.1, kilo-ernie, inkling |
| IRE Data Source Rule: class-level, create-only, checked only when no match | deepseek-v4-pro, deepseek-v4.1, kilo-ernie, inkling |
| Data Refresh: `Effective Duration`/staleness, update-only, no effect under dynamic reconciliation | deepseek-v4-pro, inkling, kilo-ernie |
| CI Class Manager nav `All > Configuration > CI Class Manager`; `sn_cmdb_admin` full, `sn_cmdb_editor` read | deepseek-v4-pro, deepseek-v4.1, kilo-ernie, inkling |
| Deletion strategies are pattern-only | deepseek-flash, inkling |
| Default identifier rules (Hardware, ESX, Storage, WBEM) | deepseek-v4-pro, deepseek-v4.1, inkling |
| `glide.discovery.use_cmdb_identifiers` default true; Service Mapping forces it | deepseek-flash, deepseek-v4.1, inkling |
| `glide.discovery.max_concurrent_invocations_per_schedule` default 3 | all |
| `glide.discovery.schedule_ipv4_limit` 65,536 / `schedule_ipv6_limit` 20,000 | deepseek-flash, inkling |
| `glide.discovery.shazzam_simplify_ranges` true; `shazzam_ranges_json` true | deepseek-flash, inkling |
| `glide.reconciliation.override.null` true | deepseek-flash, deepseek-v4-pro, inkling |
| `glide.identification_engine.partial_payload_items_max_size` 1000 | deepseek-flash, deepseek-v4-pro, inkling |
| `glide.duplicate_ci_remediator.max.cis` 1000 | inkling, kilo-ernie |
| `glide.discovery.enable_mac_address_verification` false | inkling, kilo-ernie |
| `glide.discovery.file_tracking.max_files_per_ci` 50 | inkling, kilo-ernie |
| `glide.discovery.certs.*` defaults | inkling, deepseek-v4.1 |
| `cmdb_datasource_last_update` | deepseek-v4-pro, kilo-ernie |
| `sys_object_source_info` fast path | deepseek-v4.1, inkling, kilo-ernie |
| Retired CI rediscovered is not auto-un-retired | deepseek-v4-pro, openrouter-free, kilo-ernie |
| No data change → `sys_updated_on` not refreshed; `last_discovered`/`discovery_source` still update | deepseek-v4-pro |
| Property catalog stability: Brazil 114 / Australia 112; 2 Brazil-only `sn_disco_certmgmt.*`; 4 release-name default differences | deepseek-flash, inkling |
| `cmdb_datasource_precedence`, `cmdb_datasource_last_update`, `source_recency_timestamp` | deepseek-v4-pro, kilo-ernie, inkling |
| `cmdb_dynamic_ire_skip_class`, `dynamic_ire.auto_compare` | inkling, deepseek-v4-pro |
| `dscy_credentials_affinity` | inkling, kilo-ernie |
| `sa_ci_to_pattern` deletion strategies (patterns only) | inkling, deepseek-flash |
| `cmdb_metadata_hosting` / Metadata Editor synchronization | inkling, deepseek-v4.1 |
| `discovery.device.complete` → `IPAddressFixup` | nemotron |

### 11.2 Conflicts and resolutions

| Conflict | Positions | Resolution |
|---|---|---|
| `glide.discovery.multi_page_serial_mode` default | `false` (direct quote from docs/KB) vs `true` (one agent) | **`false`** per the quoted source; verify on instance |
| `glide.discovery.log_message_chars` vs `log_message_length` | Both default `200` | Same setting; verify exact name in `sys_properties` |
| Correlation ID duplicate behavior | "not duplicates" vs "duplicates unless domain-separated" | **Unresolved.** Correlation ID is documented as the ESX Server Rule identifier; do not rely on it as a general duplicate trigger |
| `≤500 CIs per batch` attribution | One agent attributed it to `glide.discovery.max_concurrent_invocations_per_schedule`; others define that as a concurrency cap default 3 | **Misattribution.** Keep the concurrency-cap meaning; the 500-CI payload guardrail is a separate best practice |
| `cmdb_duplicate_lookup_related_allowed_class` | Described as a table in some docs, a property in others | Treat as the **table** of allowed classes for lookup/related de-dup tasks; verify with `.list` |
| `glide.duplicate_ci_remediator.max.cis` default | `1000` (official) vs "varies" | **`1000`** per the official properties page |
| `cmdbreconciliationdefinition` | Docs typo | Use `cmdb_reconciliation_definition` |
| `glide.identificationengine.skipduplicates` | Docs typo | Use `glide.identification_engine.skip_duplicates` |
| Auto-Select IPv6 support | "not supported" vs not mentioned | Treat as **not supported** until verified |
| Menu labels (`ITOM` vs `IT Operations Management`, `Identifiers` vs `Identification`) | Release drift | Use table-name targets (`discovery_schedule_list.do`, `cmdb_ci_class_manager.do`, `ecc_queue_list.do`) as stable fallbacks |
| Release property counts | Earlier comparison said "same 97"; corrected parser says Brazil 114 / Australia 112 | The 97 count missed `sn_disco_*` properties because of a prefix-regex bug. Use the corrected counts; the 4 default differences are unchanged. |
| `glide.discovery.debug.classification` default | One source says `true` (debug); official classifiers doc says `false` | **`false`** per the official *Discovery classifiers* page |
| `glide.discovery.log_debug` vs `glide.discovery.log_debug_info` | Both appear; easy to conflate | `log_debug` controls Discovery debug logging; `log_debug_info` adds ECC-derived debug to the Discovery log. Both default `false`. |
| `glide.discovery.enforce_ip_sync` | Appears in one source; not in the official catalog | Likely a typo for `enforce_unique_ips` or a release-specific property; verify |

---

## 12. Source map and credits

### 12.1 Official docs (Brazil, unless noted)

- Discovery overview / exploring: `https://www.servicenow.com/docs/r/it-operations-management/discovery/r-discovery.html`
- Configuring Discovery: `.../c_DiscoveryConfiguration.html`
- Set up without Guided Setup: `.../t_ConfigureDiscovery.html`
- Discovery properties: `.../r_DiscoveryProperties.html`
- Available system properties: `.../platform-administration/r_AvailableSystemProperties.html`
- Discovery schedule form: `.../discovery-schedule-form.html`
- Discovery classifiers: `.../discovery-classifiers.html`
- Discovery identifiers: `.../c_DiscoveryIdentifiers.html`
- How Discovery identifiers work: `.../c_HowDiscoveryIdentifiersWork.html`
- Discovery behaviors: `.../c_DiscoveryBehaviors.html`
- CI deletion strategies: `.../deletion-strategy.html`
- Discovery IP address configuration: `.../discovery-ip-address-configuration.html`
- MID Server properties: `.../r_MIDServerProperties.html`
- CMDB IRE: `.../configuration-management-database-cmdb/c_CMDBIdentifyandReconcile.html`
- IRE engine: `.../ire.html`
- Identification rules: `.../c_IdentificationRules.html`
- Reconciliation rules: `.../r_ReconciliationRulesPrinciples.html`
- IRE Data Source Rule: `.../create-ire-data-source-rule.html`
- Data refresh rule: `.../create-datasource-staleness-rule.html`
- CI Class Manager: `.../ci-class-manager-landing-page.html`
- Duplicate CIs remediation: `.../de-duplication-tasks.html`
- Duplicate CI properties: `.../properties-duplicate-ci.html`
- Identification simulation: `.../identification-simulation.html`
- CMDB 360: `.../multisource-cmdb.html`
- CMDB Health: `.../c_CMDBHealth.html`

### 12.2 Knowledge base

- KB1064718 — IRE fundamentals
- KB2558192 — duplicate CI tasks vs retired CIs
- KB3222102 — `sys_updated_on` refresh behavior
- KB0756709 — data precedence rules
- KB0869861 — troubleshooting duplicate CMDB CI records
- KB0755747 — retired CI rediscovery
- KB1380611 — trusted hostname source properties
- KB2184482 — AWS Cloud Discovery
- KB0748325 — Configuration Console limitations
- KB0820379 — CI Class Manager display / reconciliation issues
- KB0750382 / KB0750383 / KB0750386 — IRE debug logs (referenced, not opened)
- KB0535236 — WMI port 135 + dynamic high ports
- KB3035161 — same-key merge; newer payload wins
- KB0715237 / KB0723645 — concurrent same-device payloads (Madrid PRB1301835)
- KB3104470 — identification rules
- KB0853105 — de-duplication tasks (referenced, UNVERIFIED)
- KB0951047 / KB0960404 / KB1542272 — SNMPv3
- KB0687602 / KB0965884 — additional IRE/Discovery notes (referenced)

### 12.3 Learning guides (cross-reference)

- CMDB guide: `https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/modules/cmdb/cmdb-guide/`
- Discovery guide: `https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/modules/discovery/discovery-guide/`

### 12.4 Agent artifacts

- `agents/deepseek-flash__openrouter__kilo-cli/SNC_DISC__WT1/05_FINAL/DISCOVERY_CONFIG_REFERENCE.md`
- `results/20261113T090000Z__deepseek-v4-pro__deepseek__kilocode/{DISCOVERY_CONFIG_REFERENCE.md,IRE_RULE_APPLICABILITY_MATRIX.md,COVERAGE_GAP_ANALYSIS.md}`
- `agents/deepseek-v4.1-flash-fast__freebuff__buffy/SNC_DISC__WT1/`
- `agents/deepseek-v4-flash__deepseek__hermes/SNC_DISC__WT1/`
- `agents/inkling-2-small__openrouter__kilo/SNC_DISC__WT1/` and `research/servicenow-discovery/`
- `agents/kilo-ernie-5.5-flash__baidu__kilo/tasks/SNC_DISC_RESEARCH/`
- `agents/openrouter-free__openrouter__kilo/SNC_DISC__WT5/`
- `agents/qwen3-30b-a3b__ollama__hermes/SNC_DISC__WT4/`
- `agents/qwen2.5-7b__ollama__hermes/SNC_DISC__WT2/`
- `agents/llama3.1-8b__ollama__hermes/SNC_DISC__WT3/`
- `agents/nemotron-3-5-super-vl__litellm__opencode/SNC_DISC__WT5/`
- `final/FINAL_deepseek-v4-pro.md`, `final/FINALINKLING-2-SMALL.MD`, `final/FINALdeepseek-flash.MD` (other agents' merged finals)

---

## 13. Gaps and UNVERIFIED

1. No live ServiceNow instance was accessed by any agent; UI labels and defaults are documentation-based.
2. No live IRE payload was executed; behavior is as documented.
3. Release drift (Brazil vs Australia vs older releases) is documented for properties but not exhaustively for UI paths.
4. Correlation ID duplicate behavior is unresolved.
5. `glide.discovery.multi_page_serial_mode` default is resolved to `false` from a direct quote but should be verified on the target instance.
6. `glide.discovery.log_message_chars` vs `log_message_length` naming should be verified.
7. Dynamic IRE production behavior was not exercised (default off).
8. KB articles referenced but not opened: KB0750382/3/6, KB0756709, KB1542272.
9. CMDB Health rule syntax and certification template JSON were not fetched.
10. MID install steps/OS matrix are platform-specific; follow Now Support MID docs for your OS.
11. The exact Shazzam maximum range size property name was not captured by every source; verify in the schedule form.
12. `glide.discovery.enforce_ip_sync` is not in the official catalog; likely a typo for `enforce_unique_ips` or release-specific.
13. `cmdb_dynamic_ire_skip_class` is documented for Brazil; verify on Australia/older releases.
14. `source_recency_timestamp` merge behavior is documented via KB3035161 / KB1064718; the exact payload shape should be validated on the target release.
15. The 114/112 property counts are from the 2026-11-13 fetched pages; re-fetch before relying on them in a later release.
