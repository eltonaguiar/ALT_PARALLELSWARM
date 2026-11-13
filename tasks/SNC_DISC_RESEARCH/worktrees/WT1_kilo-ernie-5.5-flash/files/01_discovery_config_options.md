# 01 — ServiceNow Discovery: Configuration Options

Source: ServiceNow Docs (ITOM Visibility / Discovery), current GA line. Items marked
**[verify on instance]** vary by release or are instance-dependent.

## 1. Where Discovery configuration lives (bread-crumbs)

| What | Navigation path |
|------|-----------------|
| Discovery schedules | `All > IT Operations Management > Discovery > Discovery Schedules` |
| Discovery schedules (classic) | `All > ITOM > Discovery > Discovery Schedules` |
| Discovery status / results | `All > ITOM > Discovery > Discovery Status` |
| Discovery log | `All > ITOM > Discovery > Discovery Log` |
| IP networks (Network Discovery) | `All > ITOM > Discovery > IP Networks` |
| Behaviors | `All > ITOM > Discovery > Discovery Behaviors` |
| Classifiers | `All > ITOM > Discovery > CI Classifiers` |
| Probes | `All > ITOM > Discovery > Probes` |
| Patterns | `All > ITOM > Discovery > Patterns` (Pattern Designer) |
| Discovery properties | `All > ITOM > Discovery > Properties` or `System Properties > All Properties` |
| CI Class Manager | `All > Configuration > CI Class Manager` |
| Identification rules | via CI Class Manager, or `All > Configuration > System > ... Identification Rules` |
| Reconciliation rules | `cmdb_reconciliation_definition` / `cmdb_dynamic_reconciliation_definition` tables |
| MID Servers | `All > ITOM > MID Servers` / `MID Server dashboard` |
| ECC queue | `All > ITOM > ECC > ECC Queue` (records: `ECC Queue [ecc_queue]`) |

> Menu wording has shifted between releases (e.g. `ITOM` vs `IT Operations Management`).
> Prefer the table-name target if a menu label is missing: `discovery_schedule_list.do`,
> `discovery_status_list.do`, `cmdb_ci_class_manager.do`, `ecc_queue_list.do`.

## 2. Discovery Schedule options (the main control surface)

The Discovery Schedule is the control point for a run: when it runs, which MID Server(s),
what type of discovery, and which IP ranges.

| Field | Options / default | Effect |
|-------|-------------------|--------|
| **Name** | free text | Unique descriptive name. |
| **Discover** | Configuration items / IP addresses / Networks / Service / Serverless / Cloud application / Cloud resources / Certificates | **Configuration items** = normal credentialed discovery using CI identifiers (updates CMDB). **IP addresses** = credential-less port/banner scan, creates device history but **does not update CMDB**. Networks, Service (Service Mapping), Cloud, Certificates are specialized. |
| **MID Server selection method** | Auto-Select / Specific MID Cluster / Specific MID Server / Use Behavior | Auto-Select matches MID Server IP ranges + app (Discovery or ALL). Specific cluster/server pins it. Behavior enables multi-MID, multi-domain, load-balancing scans. |
| **MID Server / Cluster / Behavior** | conditional | Set by the selection method above. |
| **Active** | true/false | Inactive schedules can still run manually. |
| **Location** | location ref | Assigned to discovered CIs. |
| **Max run time** | duration | Cancels remaining tasks when elapsed (protects system load). |
| **Max Idle time** | duration (column hidden by default) | Cancels stalled runs (no ECC input processed, nothing in processing). Measured from last ECC Queue change; fixed at run start. |
| **Run** | Daily/Weekly/Monthly/Once/On demand | Schedule frequency (system time zone). |
| **Log state changes** | true/false | Log each state change (e.g. Active → Classifying) on Discovery Status. |
| **Shazzam batch size** | default **1000**, min 256 | IPs per Shazzam probe; smaller = earlier classification, more probes. Cannot exceed Shazzam max range size. |
| **Shazzam cluster support** | true/false | Distribute Shazzam across MID Servers in a cluster. |
| **Use SNMP Version** | ALL / v1 / v2c / v3 | SNMP version for the scan. |
| **Quick ranges** | comma string (network/range/list) | Inline IP targets. |
| **IP Ranges** (related list) | ranges | Primary targets for a simple CI scan. |
| **Discovery Range Sets** (related list) | range sets | One range set per Shazzam probe. |
| **Discovery Status** (related list) | — | Current + past run results. |

**Advanced**: for multi-MID load balancing, multi-domain, ACL-restricted SNMP, or dual-protocol
devices, use **Discovery behaviors** (functionalities → MID Servers → phases).

## 3. MID Server selection & behaviors

- **Auto-Select**: 1) MID Server with matching IP range + Discovery/ALL app; 2) first Up; 3) random if multiple up; 4) default MID Server for Discovery/ALL; 5) Paused/Upgrading fallback. **Not supported with IPv6.**
- **Behavior** = one or more **Discovery functionality** records. A functionality links: a functionality definition (protocol list), the MID Servers, a **phase** (integer; same-phase functionalities run in one Shazzam probe, phases run numerically), and optional **functionality criteria** (mid_server / win_domain / mid_win_domain) for Windows.
- Common functionalities: *Windows only (WMI)*, *Windows/DNS/WINS*, *SNMP only*, *All except SNMP*, *All except Windows (no WMI)*.

## 4. Discovery properties (`glide.discovery.*`)

Set under `System Properties > All Properties` (or `All > ITOM > Discovery > Properties`).

| Property | Default | Effect |
|----------|---------|--------|
| `glide.discovery.log_debug` | false | Verbose Discovery debug logging. |
| `glide.discovery.log_debug_info` | false | Write ECC debug info into Discovery log. |
| `glide.discovery.debug.ci_identification` | false | Debug logging to the **CI Identification Log** (key for IRE troubleshooting). |
| `glide.discovery.sensors.save_attachments` | true | Keep ECC attachments after sensor processing (set true to inspect raw probe data). |
| `glide.discovery.max_concurrent_invocations_per_schedule` | 3 | Cap concurrent invocations of the same schedule (prevents overlap storms). |
| `glide.discovery.hostname.always_update` | true | Always update hostname from most recent **trusted** source (can overwrite manual values). |
| `glide.discovery.hostname.case` | Lower case | Hostname casing normalization. |
| `glide.discovery.hostname.dns_nbt_trusted` | (varies) | Trust DNS/NetBIOS hostname source. |
| `glide.discovery.enable_mac_address_verification` | false | Verify MAC to detect IP change mid-discovery; stops that IP with a warning. |
| `glide.discovery.enable_file_tracking` | true | Pattern-based config file tracking. |
| `glide.discovery.file_tracking.max_files_per_ci` | 4 | Max tracked config files per CI. |
| `glide.discovery.save_pattern_log` | true | Persist pattern logs (set false to reduce DB load; failures always saved). |
| `glide.discovery.log_message_length` | 200 | Truncate Discovery log messages. |
| `glide.discovery.enable.software_filter` | true | Windows software filtering. |
| `glide.discovery.shazzam_ranges_json` | true | JSON-encode Shazzam IP ranges (smaller payload). |
| `glide.eccprobe.max_queued_probes_per_run` | 20 | Max probes a node picks up per run. |
| `glide.discovery.mark_esx_servers_as_absent` | false | Mark missing ESX servers absent vs retired. |

## 5. Protocol & credential configuration (prerequisites)

Discovery needs **credentials** for the protocols it will use, and the MID Server must be able to reach the targets.

| Area | Navigation | Notes |
|------|-----------|-------|
| Discovery credentials | `All > ITOM > Discovery > Credentials` | SSH (username/password/key), WMI (Windows), SNMP (v1/v2c/v3 community/credentials), IPMI, vCenter, etc. Order/priority matters. |
| Credential affinity | per schedule / per IP range | Windows MID Server must be domain-joined; SNMP ACLs must allow the MID Server host. |
| MID Server setup | `All > ITOM > MID Servers` | Install/validate; assign Discovery/ALL application; configure IP ranges. |
| Ports / firewall | — | MID Server must reach WMI 135 + dynamic RPC, SSH 22, SNMP 161/udp, HTTP 80/443. **[verify on instance]** |

## 6. Discovery modes recap

- **Horizontal discovery** (bottom-up, this doc): scans IP ranges, classifies, identifies, explores.
- **Service Mapping** (top-down): maps application services from entry points downward.
- **IP Scan** (`Discover = IP addresses`): credential-less; **no CMDB CI updates**, only device history.
- **Cloud Discovery**: discovers cloud resources via cloud accounts/patterns.

## Sources
- Discovery schedule form reference — servicenow.com/docs (discovery-schedule-form)
- Discovery properties — servicenow.com/docs (r_DiscoveryProperties)
- Discovery behaviors — servicenow.com/docs (c_DiscoveryBehaviors)
- MID Server selection sequence — servicenow.com/docs (c-MIDServerSelectionSequence)