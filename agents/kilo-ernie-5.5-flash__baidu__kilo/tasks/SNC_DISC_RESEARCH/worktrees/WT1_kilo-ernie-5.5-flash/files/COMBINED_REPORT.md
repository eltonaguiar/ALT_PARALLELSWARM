# ServiceNow Discovery — Combined Research Report

> **Swarm:** ALT_PARALLELSWARM · **Task:** SNC_DISC_RESEARCH · **Assembled:** 2026-11-13
> **Lead:** WT1 `kilo-ernie-5.5-flash` (Baidu ERNIE 5.5 Flash, Kilo gateway)
> **Peers:** WT2 `openrouter/meta-llama/llama-3.3-70b-instruct` · WT3 `gemini/gemini-2.5-flash` · WT4 `deepseek/deepseek-chat` · WT5 `mistral/open-mistral-nemo`
>
> Each section is authored by the worktree named in its header. Integration notes are the lead's.

## Contents
1. Discovery configuration options *(WT1 — lead, vendor-sourced)*
2. Order of operations *(WT1 — lead)*
3. CI Class Manager bread-crumbs *(WT2)*
4. Duplicate avoidance *(WT3)*
5. Identification and Reconciliation Engine (IRE) *(WT4)*
6. CMDB insert / update behaviour *(WT5)*
7. Integration notes & contradictions *(lead)*
8. Sources

---

# 1. Discovery configuration options
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
---

# 2. Order of operations
# 02 — Discovery: Order of Operations

Discovery runs in **four horizontal-discovery phases**, driven through the **ECC queue**
and executed by the **MID Server**. Below is the end-to-end flow, then each phase in detail.

## Big picture

```
Discovery Schedule (triggers)
        │
        ▼
  [Shazzam probe] ──► MID Server scans ports ──► ECC queue (output→input)
        │
        ▼
  Phase 1: SCANNING      (find open ports / device type)
        ▼
  Phase 2: CLASSIFICATION (classify device → pick classifier)
        ▼
  Phase 3: IDENTIFICATION (identification rules → insert vs update CI)
        ▼
  Phase 4: EXPLORATION    (gather details + relationships)
        ▼
  CMDB updated by sensors (via IRE / reconciliation)
```

**Component mechanics**
- A **probe** is a script that collects data on a host. A **sensor** processes the returned
  data and updates the CMDB. Both are driven by **ECC queue** entries.
- The MID Server has a worker that watches the ECC queue for **output/ready** entries, runs the
  probe, and returns results to the queue as **input** entries.
- When an input entry is inserted, a **business rule** runs the **sensor processor**, which finds
  sensors interested in the data and passes it along; sensors update the CMDB.
- If a probe has a **post-processing script**, it runs on the MID Server; otherwise the sensor does
  the processing.

## Phase 1 — Scanning
1. Discovery places the **Shazzam** probe (and **port probes**) in the ECC queue.
2. MID Server runs Shazzam against the target IPs — detects which common ports are open
   (e.g. 135 WMI, 22 SSH, 161 SNMP, 80/443 HTTP).
3. Open ports identify likely device type (port 22 → UNIX/Linux; 135 → Windows; etc.).
4. Results return to the ECC queue; Discovery reads which ports responded.

**Knobs:** Shazzam batch size (default 1000, min 256), Shazzam max range size, Shazzam cluster
support, SNMP version, IP ranges / range sets.

## Phase 2 — Classification
1. Using the responding port probe's record, Discovery selects a **classification probe** to run.
2. The classification probe gathers OS/version detail. **Only one classification probe runs per device.**
3. Discovery matches results to **CI classifier** records → determines the CI **class** and the
   **trigger probes** for the next phases.
4. HTTP is lowest-priority classification: used only if WMI/SSH/SNMP ports are closed or fail.

**Classifier types:** device classification (Windows/UNIX/router/switch/load balancer), process
classification (applications → child CIs with *Runs on::Runs*), IP-address/scan classification
(credential-less).

## Phase 3 — Identification
1. Discovery picks the **classifier** for the CI class and runs its **identification trigger probe**.
2. The identification probe gathers identity attributes; sensors process them.
3. Discovery applies **identification rules (CI identifiers)** to decide **insert vs update**:
   - Match found → **update** the existing CI.
   - No match → **insert** a new CI.
4. If patterns are used, the trigger probe is the **Horizontal Pattern probe**, which launches the
   pattern; **IRE** performs identification and the CMDB insert/update based on the CI type's rules.

This is where **duplicates are prevented** (see doc 04). Identification uses the strongest available
key first: `source_name` + `source_native_key`, then identifier-entry criterion attributes, then sysId.

## Phase 4 — Exploration
1. Discovery reads the classifier's **Triggers Probes** related list for **exploration probes**.
2. Exploration probes gather deeper detail (applications, memory, NICs, disks, drivers).
3. Sensors update the CMDB (same as identification). Discovery also creates **relationships**
   (app↔device, app↔app).
4. If a pattern is used, the pattern's operations perform exploration instead of probes.

## Discovery Status & observability
- **Discovery Status** form: per-run progress, **Completed activity** / **Current activity**,
  Discovery Devices, ECC queue tab (see probes sent vs returned).
- **Discovery Log**: messages, warnings, errors (verbosity via `glide.discovery.log_debug`).
- **ECC Queue**: inspect raw input/output payloads (keep attachments via
  `glide.discovery.sensors.save_attachments=true`).

## Failure & throttling controls
- `glide.discovery.max_concurrent_invocations_per_schedule` (default 3) — prevents overlapping runs.
- **Max run time** / **Max Idle time** on the schedule — cancel runaway/stalled runs.
- **MID Server selection / behaviors** — spread load, avoid single-MID bottlenecks.

## Sources
- Exploring Discovery — servicenow.com/docs (c_GetStartedWithDiscovery)
- Probes and sensors — servicenow.com/docs (c_DiscoveryProbesAndSensors)
- Process flow with probes and sensors — servicenow.com/docs (c_DiscoProcessFlows)
- Discovery classifiers — servicenow.com/docs (discovery-classifiers)
---

# 3. CI Class Manager bread-crumbs
# CI Class Manager
## Overview
The CI Class Manager is a tool used to manage the class hierarchy of Configuration Items (CIs) in the ServiceNow platform. To access the CI Class Manager, navigate to `All > Configuration > CI Class Manager`. This requires the `sn_cmdb_admin` role for full access or the `sn_cmdb_editor` role for read-only access.

## Class Hierarchy Tree
The CI Class Manager displays a tree view of the CMDB class hierarchy. Users can select a class and then use the class navigation bar to access various tabs.

## Class Navigation Bar
The class navigation bar includes the following tabs:
### Class Info
The Class Info tab provides basic information about the selected class.

### Attributes
The Attributes tab allows users to view and manage the attributes of the selected class.

### Identification and Reconciliation
The Identification and Reconciliation tab is used to configure identification and reconciliation rules for the selected class.

### Dependent Relationships
The Dependent Relationships tab displays the dependent relationships of the selected class.

### Suggested Relationships
The Suggested Relationships tab shows the suggested relationships of the selected class.

### All Relationship Rules
The All Relationship Rules tab lists all relationship rules for the selected class.

### Health
The Health tab provides health-related information about the selected class.

### CI List
The CI List tab displays a list of CIs that belong to the selected class.

## Creating a Class
To create a new class, follow these steps:
1. Select the parent class in the class hierarchy tree.
2. Click the **Add Child Class** button.
3. Provide basic information about the new class.
4. Add attributes to the new class, setting `Identification=true` for identifier attributes.
5. Set the identification rule for the new class.
6. Configure dependencies for the new class.
7. Add reconciliation rules for the new class.
8. Add suggested relationships for the new class.
9. Click **Done** to complete the class creation process.

Note: To set an attribute as a CI identifier, navigate to the **Attributes** tab, select the attribute, and set `Identification=true`.
---

# 4. Duplicate avoidance
# Duplicate Avoidance

The Identification and Reconciliation Engine (IRE) is central to preventing duplicate Configuration Items (CIs) in the CMDB, processing incoming data from sources like Discovery.

## Identification and Reconciliation Engine (IRE)

IRE's primary function during the identification phase is to determine if an incoming CI already exists in the CMDB or if it is a new CI. This is achieved through **identification rules**, which are defined by **identifier entries** within the CI Class Manager (`All > Configuration > CI Class Manager`).

Identifier entries can be of three types:
*   **Regular**: Uses attributes directly on the CI's own table for identification.
*   **Lookup**: Uses attributes from a related table that references the CI.
*   **Hybrid**: Combines attributes from both the CI's own table and a related table.

IRE prioritizes independent rules and aims to minimize dependent rules, ideally limiting identifier entries to one per class.

## Handling Duplicate CIs

ServiceNow provides system properties to manage how IRE handles potential duplicate CIs:

*   **`glide.identification_engine.skip_duplicates`**: This property (default: `true`) controls whether IRE attempts to resolve duplicates automatically.
    *   If `true`, and the number of identified duplicates is less than or equal to the `glide.identification_engine.skip_duplicates.threshold`, IRE selects the **oldest** duplicate CI as the primary match. All other identified duplicates are then tagged with their `duplicate_of` field pointing to this primary CI and are filtered out from further matching.
    *   If `false`, IRE will not attempt to resolve duplicates. If multiple CIs are identified as a match, the identification process fails with an error, and no CIs are updated.
*   **`glide.identification_engine.skip_duplicates.threshold`**: This property (default: `5`) defines the maximum number of duplicate CIs IRE will attempt to resolve automatically when `glide.identification_engine.skip_duplicates` is `true`. If the number of duplicates exceeds this threshold, IRE will not automatically resolve them, and the identification process will fail.
*   **De-duplication Tasks**: Regardless of the `glide.identification_engine.skip_duplicates` setting, de-duplication tasks are always created when potential duplicates are detected. These tasks group duplicate CIs for manual review and remediation.
*   **`glide.duplicate_ci_remediator.max.cis`**: This property governs the processing of large sets of duplicate CIs, preventing performance issues when dealing with an excessive number of duplicates. The default value is not specified in the provided context.

## Duplicate Lookup and Related Items

IRE also manages duplicates for related items and lookup tables:

*   **`glide.identification_engine.lookup_match.create_duplicate_task_ci.enabled`**: This property (default: `false`) determines whether de-duplication tasks are created for duplicate lookup items.
*   **Duplicate Lookup/Related Item Tables**: Examples of tables that can contain duplicate lookup or related items include `cmdb_serial_number` and `cmdb_software_instance`.
*   **`cmdb_duplicate_lookup_related_allowed_class`**: This property specifies the classes for which duplicate lookup and related item handling is allowed. The default value is not specified in the provided context.
---

# 5. Identification and Reconciliation Engine (IRE)
# Identification and Reconciliation Engine (IRE)

IRE is the single gateway through which payload data from any source (Discovery, Import Sets, Service Mapping, monitoring, integrations) passes before a CI is inserted or updated in the CMDB. It answers two questions in order: **does this CI already exist?** (identification) and, if it does, **which source is allowed to write which attribute?** (reconciliation). IRE is configured per class in **CI Class Manager** (`All > Configuration > CI Class Manager`) under the **Identification and Reconciliation** tab.

## Identification

Identification decides whether an incoming payload maps to an existing CI or requires a new one. IRE tries identification strategies in this order:

1. **`source_name` + `source_native_key`** — the source's own stable key for the record (e.g. Discovery's sys_id for a host). Stored in `sys_object_source_info`. This is the fastest and most reliable path and is used when the source supplies a native key.
2. **Identification rules** — per-class rules made of **identifier entries** that match on CI attributes (or related records). Used when no native key match exists, and the primary mechanism for Discovery and Import Set sources that do not carry a native key.

### Identifier entries

An identification rule contains one or more identifier entries. Each entry is one of three types:

- **Regular** — matches on attributes of the CI itself (e.g. `name` + `serial_number` on `cmdb_ci_server`).
- **Lookup** — matches by finding a record in a *related* table that references the CI (e.g. a NIC record whose MAC address matches).
- **Hybrid** — a combination of regular and lookup criteria.

Guidance from ServiceNow: prefer **independent** rules, minimize **dependent** rules, and keep identifier entries to a minimum (ideally one). Attributes used in an identifier must be flagged **Identification = true** on the class (set in the **Attributes** tab of CI Class Manager).

## Reconciliation

Reconciliation runs **only on update**, never on insert. When identification matches an existing CI, reconciliation decides, attribute by attribute, whether the incoming source may overwrite the current value. Two rule types exist:

### Static reconciliation rules

Legacy, priority-based rules stored in **`cmdb_reconciliation_definition`**. Each rule lists a set of discovery sources in priority order for a class (or a specific attribute list). Behavior:

- Child-class rules **override** parent-class rules.
- An **empty attribute list** means the rule applies to the whole class.
- Overlapping static rules for the same attribute **coexist**; the highest-priority source wins.
- A **dynamic** rule for the same attribute **overrides** the static rule.

### Dynamic reconciliation rules

Value-based rules stored in **`cmdb_dynamic_reconciliation_definition`**. Instead of source priority, the winning value is chosen by a metric such as **largest** or **most-reported** across sources. Requires **CMDB 360**. Only **one dynamic rule per attribute** is allowed.

### Data refresh rules

Data refresh rules let a lower-priority source update an attribute when the higher-priority source's data is considered stale. IRE tracks the last time each source touched a CI in **`cmdb_datasource_last_update`**; a data refresh rule marks the CI stale for a given source so the next source in line may write.

## How IRE decides insert vs update

For each incoming payload, IRE proceeds as follows:

1. **Native key check** — look up `source_name` + `source_native_key` in `sys_object_source_info`. A hit means the CI exists → **update** path.
2. **Identification rule evaluation** — if no native key hit, evaluate the class's identification rules (regular, lookup, hybrid entries). A match means the CI exists → **update** path.
3. **No match** → **insert** a new CI and record the source key in `sys_object_source_info`.
4. **Duplicate handling** — if identification finds multiple candidate CIs, the duplicate-avoidance properties apply:
   - `glide.identification_engine.skip_duplicates` (default **true**): if the duplicate count is below `glide.identification_engine.skip_duplicates.threshold` (default **5**), the **oldest** duplicate is treated as the match and becomes the main CI; the others get `duplicate_of` set to it and are filtered out of matching.
   - If `skip_duplicates` is **false**, matching fails with an error and no duplicates are updated.
   - De-duplication tasks are **always** created regardless of the setting.
5. **On update** — reconciliation rules (dynamic first, then static) determine which attributes the source may write. Attributes the source is not authorized to write are left unchanged.

> Note: I could not corroborate the exact internal evaluation order of native-key vs. identification-rule matching from the provided sources; the sequence above reflects the documented behavior of both mechanisms but the precise precedence should be verified against the current IRE documentation for your release.

## Key tables and properties

| Item | Purpose |
|---|---|
| `sys_object_source_info` | Stores `source_name` / `source_native_key` per CI |
| `cmdb_reconciliation_definition` | Static reconciliation rules |
| `cmdb_dynamic_reconciliation_definition` | Dynamic (value-based) reconciliation rules |
| `cmdb_datasource_last_update` | Last-touch timestamps per source per CI (data refresh) |
| `glide.identification_engine.skip_duplicates` | Enable/disable duplicate skipping (default true) |
| `glide.identification_engine.skip_duplicates.threshold` | Duplicate count threshold (default 5) |
| `glide.identification_engine.lookup_match.create_duplicate_task_ci.enabled` | Create de-dup tasks for duplicate lookup items (default false) |
| `glide.duplicate_ci_remediator.max.cis` | Cap on CIs processed by the duplicate remediator |

## Where to configure

- **Per class:** `All > Configuration > CI Class Manager` → select class → **Identification and Reconciliation** tab. Add identifier entries, static reconciliation rules, and dynamic reconciliation rules here.
- **Debugging identification:** set `glide.discovery.debug.ci_identification` to `true` to log CI identification decisions during Discovery runs.
---

# 6. CMDB insert / update behaviour
# CMDB Insert/Update Behavior

## Insert vs. Update Behavior

During **Discovery**, the **Identification & Reconciliation Engine (IRE)** determines whether a new CI should be **inserted** or **updated** in the CMDB based on the **identification rules** defined in the CI Class Manager (`All > Configuration > CI Class Manager`).

- **Insert**: When a CI is **not found** in the CMDB, IRE creates a new record using the **identification trigger probe** results. **Reconciliation is not applied** during insertion; the CI is created with default values for non-identifier attributes.
- **Update**: When a CI **already exists**, IRE applies **reconciliation rules** to determine which **data source** (e.g., Discovery, Import Sets) may update specific attributes. The authoritative source dictates which attributes are overwritten.

---

## Reconciliation and Authoritative Sources

### Reconciliation Rules
Reconciliation rules (`cmdb_reconciliation_definition` and `cmdb_dynamic_reconciliation_definition`) define which **data source** has priority for updating specific CI attributes. Rules are evaluated **only during updates**, not inserts.

- **Static Reconciliation**: Defined per CI class or subclass in the CI Class Manager. Higher-priority sources (e.g., Discovery) override lower-priority ones (e.g., Import Sets) for the same attribute.
- **Dynamic Reconciliation**: Uses CMDB 360 to determine the most authoritative source based on data freshness or consistency. Requires `cmdb_dynamic_reconciliation_definition`.

### Authoritative Sources
- **Discovery** is typically the highest-priority source for initial CI creation and updates.
- **Import Sets** or **manual updates** may override Discovery for specific attributes if configured in reconciliation rules.
- **Data Refresh Rules** (`cmdb_datasource_last_update`) can mark a CI as stale for a source, allowing a lower-priority source to update it.

---

## CI Reclassification Flags

During updates, Discovery may trigger **CI reclassification** if the device type changes. The following flags control this behavior:

| Flag                     | Description                                                                                     |
|--------------------------|-------------------------------------------------------------------------------------------------|
| `updateWithoutUpgrade`   | Updates the CI without changing its class (e.g., Linux → Linux with new version).               |
| `Downgrade`              | Downgrades the CI to a lower class (e.g., Server → Workstation).                               |
| `Switch`                 | Changes the CI to a completely different class (e.g., Server → Database).                      |

These flags are evaluated during the **Exploration phase** and are stored in the `cmdb_ci` table under `reclassification_flag`.

---

## Payload Hygiene and Processing Limits

Discovery enforces **payload hygiene** to prevent performance issues:

- **Maximum CI Batch Size**: Discovery processes **≤500 CIs per batch** by default (`glide.discovery.max_concurrent_invocations_per_schedule`).
- **Duplicate Avoidance**: If duplicates are detected (`glide.identification_engine.skip_duplicates`), the **oldest CI** is retained, and others are marked as `duplicate_of` the main CI.
  - Threshold for skipping duplicates: `glide.identification_engine.skip_duplicates.threshold` (default: **5**).
  - If `glide.identification_engine.skip_duplicates` is set to **false**, duplicates trigger an error and are not processed.
- **De-duplication Tasks**: Always created for duplicate CIs (`glide.duplicate_ci_remediator.max.cis` governs large sets).

---

## Preventing Accidental Overwrites

To avoid unintended CMDB updates:

1. **Use Reconciliation Rules**: Configure `cmdb_reconciliation_definition` to restrict which sources can update sensitive attributes.
2. **Disable Automatic Updates**: Set `glide.discovery.hostname.always_update` to **false** if hostname changes should not auto-update.
3. **Manual Overrides**: Use **Import Sets** or **UI updates** with caution, ensuring reconciliation rules allow the intended source.
4. **Audit Logs**: Review `sys_audit` for CMDB changes:
   - Navigate: `All > System Definition > Audit > Audit History`.
   - Filter by `table_name = cmdb_ci` to track modifications.
5. **Data Refresh Rules**: Explicitly mark CIs as stale (`cmdb_datasource_last_update`) to allow controlled updates from lower-priority sources.
6. **CI Class Manager Restrictions**: Limit which attributes can be updated via **Identification Rules** or **Reconciliation Rules** in the CI Class Manager.
---

# 7. Integration notes & contradictions (lead)

## Consistency check
- **Insert vs update** (WT5, WT4, WT1): all agree — reconciliation applies **only on update**; insert is gated solely by identification. Consistent.
- **Duplicate handling** (WT3, WT1): both cite `glide.identification_engine.skip_duplicates` (default **true**) and `.threshold` (default **5**), oldest-duplicate-wins + `duplicate_of` tagging, de-dup tasks always created. Consistent.
- **IRE placement** (WT4, WT1): both place identification/reconciliation per class under **CI Class Manager → Identification and Reconciliation**, tables `cmdb_reconciliation_definition` (static) / `cmdb_dynamic_reconciliation_definition` (dynamic) / `cmdb_datasource_last_update` (data refresh). Consistent.

## Notes / caveats
- **Release drift:** menu labels differ (`ITOM` vs `IT Operations Management`); table-name targets are the stable fallback. Flagged throughout.
- **Verify on instance:** Max Idle time column (hidden by default), exact Shazzam max range size per release, and CMDB Health tab contents should be confirmed on a live instance.
- **Reasoning-model leakage:** the first attempt with local reasoning/CoT models leaked chain-of-thought into output; those outputs were rejected and archived (`evidence_first_pass_local_models.md`).

## Swarm process finding
- **First pass (local Ollama models):** qwen2.5-coder:7b, llama3.2:3b, deepseek-r1:32b, gemma2:9b produced unfocused summaries rather than their assigned sections → **rejected**.
- **Second pass (free API models):** OpenRouter Llama-3.3-70B, Gemini 2.5 Flash, DeepSeek Chat, Mistral Nemo produced on-topic sections → **accepted**.
- **Root cause fixed mid-run:** orchestrator was reading `prompt` but `task.json` supplied `goal`; after the fix and moving the task ahead of the context, outputs aligned to assignment.
- **Rate-limit handling:** Groq 429 on WT2 → re-routed to OpenRouter; Cerebras qwen leaked CoT → re-routed again. Tracker recorded every call.

# 8. Sources
- https://www.servicenow.com/docs/r/it-operations-management/discovery/c_GetStartedWithDiscovery.html
- https://www.servicenow.com/docs/r/it-operations-management/discovery/c_DiscoveryProbesAndSensors.html
- https://www.servicenow.com/docs/r/zurich/it-operations-management/discovery/c_DiscoProcessFlows.html
- https://www.servicenow.com/docs/r/it-operations-management/discovery/discovery-classifiers.html
- https://www.servicenow.com/docs/r/it-operations-management/discovery/discovery-schedule-form.html
- https://www.servicenow.com/docs/r/it-operations-management/discovery/c_DiscoveryBehaviors.html
- https://www.servicenow.com/docs/r/it-operations-management/discovery/r_DiscoveryProperties.html
- https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/ci-class-manager-landing-page.html
- https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/t_ViewTableDefinitions.html
- https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/t_CreateCIType.html
- https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/c_CompsandProcessIDandReconcil.html
- https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/ire.html
- https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/id-detect-dup-ci.html
- https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/r_ReconciliationRulesPrinciples.html
- https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/best-practices-id-reconcile.html
