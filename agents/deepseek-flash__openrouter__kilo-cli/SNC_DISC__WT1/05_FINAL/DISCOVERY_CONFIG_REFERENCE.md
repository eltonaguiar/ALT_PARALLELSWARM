# ServiceNow Discovery — Configuration Reference

**Release basis:** ServiceNow **Brazil** documentation, as served on 2026-11-13.
**Task:** `SNC_DISC_RESEARCH`.
**Author agent:** `deepseek-flash__openrouter__kilo-cli` — model `deepseek/deepseek-flash`,
provider OpenRouter (inferred), harness Kilo CLI. See `00_MODEL/MODEL_PROVIDER.md`.
**Method:** 68 ServiceNow documentation topics retrieved from the docs FluidTopics API
(`/api/khub/...`), cleaned, and cross-checked. Every section ends with the canonical pages.
**Confidence:** High for property names/defaults and documented behavior. Medium for
UI wording, because ServiceNow relabels navigation between releases.

---

## 1. The mental model you need before touching a setting

Discovery is **two pipelines that meet at the CMDB**:

```
Network / devices
      │
      │  horizontal discovery (this document)
      ▼
Shazzam scan → classification → identification → exploration
      │                              │
      │ probes + sensors             │ patterns (NDL)
      │ identity probe/sensor        │ pattern operations
      ▼                              ▼
Discovery identifier  ───────►  CMDB IRE identification rules
      │                              │
      └──────────► IRE ◄─────────────┘
                     │
          reconcile → insert / update / no-op
                     │
                     ▼
                    CMDB
```

There are two important consequences:

1. **"Discovery identifiers" and "CMDB identification rules" are not the same object.**
   Probe-based discovery uses Discovery identifiers; pattern-based discovery uses the
   CMDB Identification and Reconciliation Engine (IRE) rules. In Brazil, Discovery is
   configured to use the CMDB API by default (`glide.discovery.use_cmdb_identifiers =
   true`), but the conceptual paths remain distinct in the documentation.
2. **Duplicate prevention is not one checkbox.** It is the combination of:
   strong identification rules (design), authoritative reconciliation and data-source
   rules (runtime writes), and de-duplication tasks (repair). Tuning one layer while
   ignoring the other two produces either duplicates or silent overwrites.

> Source: [Exploring Discovery](https://www.servicenow.com/docs/r/it-operations-management/discovery/c_GetStartedWithDiscovery.html),
> [Discovery identifiers](https://www.servicenow.com/docs/r/it-operations-management/discovery/c_DiscoveryIdentifiers.html),
> [IRE](https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/ire.html).

---

## 2. Canonical order of operations

This is the order that avoids rework. Each step has an exit check; do not move on until
it passes.

| # | Step | Why it is here | Exit check |
|---|---|---|---|
| 0 | Confirm subscription/plugin; assign `discovery_admin` | Discovery is a separate subscription; the role grants access to Discovery tables | Role present; plugin active |
| 1 | Install **at least two** MID Servers, assign the **Discovery** or **ALL** application | A MID Server executes probes/patterns and initiates all communication | MID Servers appear under `Discovery > MID Servers`; status Up/Validated |
| 2 | Configure and **test** credentials | Bad credentials are the leading cause of failed discoveries | Credential test succeeds per protocol/device class |
| 3 | Define IP ranges / range sets; add global IP exclusions | Discovery scans only what you authorize | Ranges resolve; excluded networks absent |
| 4 | Review classifiers (and patterns) for the device classes you expect | Classifiers select the probes/pattern for identification and exploration | A test device classifies into the expected CI class |
| 5 | Create a Discovery schedule (type **Configuration items**) | The schedule is the control point: when, where, which MID Server, which behavior | Schedule saved; `Discover now` works |
| 6 | Run and watch the four phases | Scanning → classification → identification → exploration | Discovery Status reaches a terminal state |
| 7 | Validate via ECC queue XML, Discovery Log, device history, Home page | Proves what was actually collected and written | Expected CIs created/updated; no credential errors |
| 8 | Tune properties/classifiers/behaviors | Only after evidence from step 7 | Re-run improves coverage without new duplicates |
| 9 | Configure CMDB governance: IRE identification, reconciliation, data refresh, inclusion, de-dup | Discovery writes through IRE; governance decides authority and duplicates | Identification simulation passes; duplicate metric stable |
| 10 | Operate: schedules, CMDB Health, Data Manager, CMDB 360 | Keeps the CMDB accurate over time | Health/duplicate KPIs trending correctly |

**Critical ordering rule:** design the **CI class + identification rule** before you
enable a broad schedule. A schedule that discovers 10,000 devices against a weak
name-only identifier is how duplicate floods are created.

> Sources: [Set up Discovery without Guided Setup](https://www.servicenow.com/docs/r/it-operations-management/discovery/t_ConfigureDiscovery.html),
> [Discovery setup](https://www.servicenow.com/docs/r/it-operations-management/discovery/discovery-setup.html),
> [Schedule a horizontal discovery](https://www.servicenow.com/docs/r/it-operations-management/discovery/t_CreateADiscoverySchedule.html).

---

## 3. Configuration surface (what exists, and what it controls)

### 3.1 Subscription, roles, and entry points

- Discovery requires a **separate subscription**; the plugin must be requested/activated.
- `discovery_admin` grants configuration and execution access. `admin` also works for
  most procedures.
- Main UI entry points used in this document:
  - `All > Discovery > Discovery Schedules`
  - `All > Discovery > Discovery Log`
  - `All > Discovery > MID Servers`
  - `All > Discovery > Discovery Definition > Properties`
  - `All > Configuration > CI Class Manager`
  - `All > Configuration > Identification/Reconciliation > Identification Simulation`
  - `All > Configuration > Identification/Reconciliation > IRE Data Source Rule`
  - `All > Configuration > CMDB Properties > Identification/Reconciliation Properties`

### 3.2 MID Server

- The MID Server **polls the instance** for work, executes probes/patterns, and returns
  results. It does not retain discovery data.
- All communication is initiated from inside the firewall over SOAP/HTTPS; no inbound
  firewall rule or VPN is required.
- Install **two or more** initially, on different schedules/ranges, to finish faster.
- The MID Server must be assigned the **Discovery** application or **ALL**.
- MID selection sequence (Auto-Select):
  1. a MID Server with the Discovery app and a matching IP range;
  2. otherwise a MID Server with ALL and a matching IP range;
  3. if several, first `Up` (random among Up);
  4. otherwise the default MID Server for Discovery, then for ALL;
  5. otherwise `Paused`/`Upgrading` candidates.
- For load balancing, multiple domains, ACL-protected SNMP, or devices exposing two
  protocols, use **Discovery behaviors** rather than one MID Server.

> Source: [Set up without Guided Setup](https://www.servicenow.com/docs/r/it-operations-management/discovery/t_ConfigureDiscovery.html),
> [Discovery behaviors](https://www.servicenow.com/docs/r/it-operations-management/discovery/c_DiscoveryBehaviors.html).

### 3.3 Credentials

- Windows/WMI credentials come from the **MID Server service login** on a Windows host.
- UNIX/SSH, vCenter, and SNMP credentials are configured **on the instance**.
- Discovery automatically determines which credential works for a device.
- Test credentials before every broad run; the docs call bad credentials a leading
  cause of failed discovery.
- For multiple Windows domains, prefer **PowerShell** (one MID Server can authenticate
  across domains with instance-stored credentials), or use behaviors.

### 3.4 IP address space

- A schedule scans only the IP ranges attached to it; a **range set** is a reusable
  group of ranges.
- **Global IP exclusions** prevent scanning specified addresses across all schedules
  that discover CIs, IPs, or networks.
- **IP service affinity** remembers which protocol/port succeeded for an address
  (`ip_service_affinity`), so subsequent runs try the working protocol first. Useful
  when a device exposes both SSH and SNMP and SSH fails.
- `glide.discovery.enforce_unique_ips` controls whether an IP is cleared from other
  devices when reused. It is **not** a CI de-duplication control; default `false`.
- `glide.discovery.exclude_ip_sync_classes` (default `cmdb_ci_lb`) keeps the management
  IP of load balancers instead of substituting a NIC IP.
- **IPAM integration** can auto-create schedules; `glide.discovery.schedule_ipv4_limit`
  (default 65,536) and `glide.discovery.schedule_ipv6_limit` (default 20,000) bound
  auto-generated schedules.

> Source: [Discovery IP address configuration](https://www.servicenow.com/docs/r/it-operations-management/discovery/discovery-ip-address-configuration.html),
> [IP address selection properties](https://www.servicenow.com/docs/r/it-operations-management/discovery/r_CIIPAddressSelection.html),
> [Discovery properties](https://www.servicenow.com/docs/r/it-operations-management/discovery/r_DiscoveryProperties.html).

### 3.5 Discovery schedule

A schedule answers: **what** to discover, **when**, with **which MID Server**, and with
what **limits**.

| Field / control | What it does | Practical guidance |
|---|---|---|
| **Discover** | `Configuration items`, `IP addresses`, `Networks`, `Service`, `Serverless`, `Cloud application`, `Cloud resources`, `Certificates` | For CMDB CI population, use **Configuration items**. IP-address scans do **not** update the CMDB. |
| **MID Server selection method** | Auto-Select, Specific MID Cluster, Specific MID Server, Use Behavior | Start with Auto-Select; use Behavior for multi-domain/load balancing. |
| **Max run time** | Cancels remaining tasks at the limit | Set a window that matches your change/ops constraints. |
| **Max Idle time** | Cancels stalled runs when no ECC records are processing | Hidden by default; add the column if needed. |
| **Shazzam batch size** | IPs per Shazzam probe; default 1000 | Minimum effective 256; larger batches reduce overhead but delay classification. |
| **Shazzam cluster support** | Distributes Shazzam across cluster members | Use with batch size; probes run sequentially per MID Server. |
| **Use SNMP Version** | ALL / v1 / v2c / v3 | Pin the version when the network requires it. |
| **Quick ranges** | Inline IP/range/list entry | Good for pilots; move to range sets for reuse. |
| **Active** | Enables the schedule | Inactive schedules can still be run manually. |
| **Log state changes** | Logs every device state transition | Useful during tuning, noisy in steady state. |

**Run options:** On Demand (default), Daily, Weekly, Monthly, Periodically, Once,
Weekdays, Weekends, Month Last Day, Calendar Quarter End, **After Discovery**.
`After Discovery` lets you chain schedules; `Even if canceled` decouples the chain from
the upstream result.

**Concurrency guard:** `glide.discovery.max_concurrent_invocations_per_schedule`
(default **3**) prevents a slow schedule from stacking unbounded runs. `0` or negative
disables the guard.

> Sources: [Discovery Schedule form reference](https://www.servicenow.com/docs/r/it-operations-management/discovery/discovery-schedule-form.html),
> [Run options for discovery schedules](https://www.servicenow.com/docs/api/khub/maps/bsp_DjPRMilbWYHwwVa4zQ/topics/D2ETmHBsu4mAXXuvjkdEZw/content?target=DESIGNED_READER).

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

> Source: [Discovery behaviors](https://www.servicenow.com/docs/r/it-operations-management/discovery/c_DiscoveryBehaviors.html).

---

## 4. Classifiers and patterns

A **classifier** tells Discovery which probe(s) to run for identification and
exploration, or which Horizontal Pattern probe to launch. Classification happens after
the Shazzam scan and before identification/exploration.

Three classification types:

| Type | What it classifies | Notes |
|---|---|---|
| **Device** | Windows/UNIX/Linux computers, routers, switches, load balancers | Triggers identification and exploration probes; can use HTTP classification as a lower-priority fallback. |
| **Process** | Applications, based on running processes | Runs during exploration; creates child CIs with `Runs on::Runs`; process handlers filter inconsistent parameters to avoid duplicate application CIs. |
| **IP address (IP scan)** | Credential-less scan by open ports/banners | Updates CIs without identifiers; used for discovery of devices at the edge. |

- Classifier **criteria** are `parameter operator value` and are based on what the
  classify probe returned. Process-classifier condition filters are case-sensitive.
- **Patterns** are NDL operations that collect/process data and update the CMDB. When a
  pattern is used, Discovery does **not** use the identity probe; it uses the identifier
  rule for the CI type specified by the pattern.
- Keep out-of-the-box classifiers unless you are adding a CI type Discovery does not
  already classify. Debug with `glide.discovery.debug.classification = true` (add to
  `sys_properties`).

> Sources: [Discovery classifiers](https://www.servicenow.com/docs/r/it-operations-management/discovery/discovery-classifiers.html),
> [Create a Discovery CI classification](https://www.servicenow.com/docs/r/it-operations-management/discovery/create-discovery-ci-classification.html),
> [Horizontal flow with patterns](https://www.servicenow.com/docs/r/it-operations-management/discovery/disco-process-flow-patterns.html).

---

## 5. Discovery properties that matter most

Location: `All > Discovery > Discovery Definition > Properties`.
The full reference is 26+ minutes of reading; the table below is the operational subset.

### 5.1 Identity, IP, and hostname

| Property | Default | Effect / when to change |
|---|---|---|
| `glide.discovery.use_cmdb_identifiers` | `true` | Routes identification/reconciliation through CMDB IRE instead of the legacy Discovery implementation. Keep `true` unless you have a documented legacy reason. |
| `glide.discovery.enforce_unique_ips` | `false` | Clears an IP from other devices when reused. Enable only if IP uniqueness is a hard invariant; otherwise it can erase legitimate shared/VIP data. |
| `glide.discovery.exclude_ip_sync_classes` | `cmdb_ci_lb` | Classes whose IP is not substituted by a NIC IP. Extend for other virtual IP classes. |
| `glide.discovery.ip_service_affinity` | `false`; **new Brazil customers `true`** | Remembers the successful protocol/port per IP. Enable for mixed SSH/SNMP environments. |
| `glide.discovery.hostname.always_update` | `true` | Updates host name with the newest trusted value; can overwrite hand-entered values. Probe-based discovery only. |
| `glide.discovery.hostname.dns_nbt_trusted` | `true` | Trusts DNS/NetBIOS names. Do not use DNS names for Linux/AIX/Solaris patterns. |
| `glide.discovery.hostname.snmp_trusted` | `false`; new Brazil `true` | Trusts SNMP names. |
| `glide.discovery.hostname.ssh_trusted` | `false`; new Brazil `true` | Trusts SSH names. |
| `glide.discovery.hostname.wmi_trusted` | `false`; new Brazil `true` | Trusts WMI names. |
| `glide.discovery.source_name` | `ServiceNow` | Source written to `sys_object_source` / `discovery_source`. Change only for coexistence/migration scenarios. |
| `glide.discovery.debug.ci_identification` | `false` | Writes CI identification debug to the CI Identification Log. Turn on for a bounded troubleshooting window. |

### 5.2 Network discovery and scanning

| Property | Default | Effect |
|---|---|---|
| `glide.discovery.bgp_router_disable` | `true` | Skips BGP routing exploration (large tables, OOM risk). |
| `glide.discovery.discoverable.network.max.netmask.bits` | `28` | Ignores very small regular networks; 1–32 valid. |
| `glide.discovery.network_owner_method` | `Most Networks` | Chooses which router owns an IP network. |
| `glide.discovery.physical_interface_types` | `6,117,9,71,209` | Interface types treated as physical. |
| `glide.discovery.switch_interface_types` | `7,8,9,26,53,62,69,71,78,115,117,209` | Interface types treated as switch ports. |
| `glide.discovery.shazzam_simplify_ranges` | `true` | Removes duplicate IPs across ranges in a single-behavior schedule. |
| `glide.discovery.shazzam_ranges_json` | `true` | JSON-encodes Shazzam ranges to reduce payload size. |
| `glide.discovery.network_discovery.functionality` | `SNMP only` | Functionality used for network discovery. |

### 5.3 Scheduling, sensors, and throughput

| Property | Default | Effect |
|---|---|---|
| `glide.discovery.max_concurrent_invocations_per_schedule` | `3` | Caps stacked runs of the same schedule. |
| `glide.discovery.schedule_ipv4_limit` | `65,536` | Max IPv4 addresses in an auto-generated schedule. |
| `glide.discovery.schedule_ipv6_limit` | `20,000` | Max IPv6 addresses in an auto-generated schedule. |
| `discovery.use.event.processing` | `false` | Uses the Event Framework for sensor/cloud jobs. Enable for scale, then tune queue priorities. |
| `discovery.event.separate.cloud.events` | `true` | Separates cloud and IP sensor queues when event processing is on. |
| `discovery.event.pin.jobs` | `false` | Pins event processors to nodes; `false` can increase throughput. |
| `glide.discovery.sensors.save_attachments` | `true` | Keeps ECC attachments for inspection. Set `false` in steady state if storage is a concern. |
| `glide.discovery.use_probe_results_cache` | `false` | Skips sensor processing when probe results are unchanged. |
| `glide.discovery.active_processes_filter` | `false` | Filters running processes to those matching process classifications. |
| `glide.discovery.perf.metrics.enable_collection` | `true` | Collects Discovery performance metrics. |

### 5.4 Deletion strategy (patterns only)

When a pattern finds the main CI but not a related CI, the related CI's deletion
strategy in the `Related CI Types [sa_ci_to_pattern]` table applies:

| Strategy | Behavior |
|---|---|
| **Keep** (default) | Preserve the record; no changes. |
| **Delete** | Delete the related CI and its relationship. |
| **Mark as absent** | Set `install_status = Absent`; does not delete. Exception: `cmdb_ci_network_adapter` and `cmdb_ci_ip_address` are deleted when marked absent. |
| **Delete relations** | Delete only the relationships. |
| **Mark as retired** | Set `install_status = Retired`; does not delete. |

> Source: [Discovery properties](https://www.servicenow.com/docs/r/it-operations-management/discovery/r_DiscoveryProperties.html),
> [CI deletion strategies](https://www.servicenow.com/docs/r/it-operations-management/discovery/deletion-strategy.html).

---

## 6. Identification and reconciliation (IRE)

### 6.1 The pipeline

```
payload item
   │
   ├─ (fast path) source_name + source_native_key in sys_object_source_info
   │        OR
   ├─ identification rule matching on criterion attributes
   ▼
identified? ── no ──► insert (if allowed by data source rule)
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

### 6.2 Identification rules

Anatomy:

- one CI **identifier** per rule;
- one or more **identifier entries** (unique attribute sets) with different priorities;
- optional **related entries** for related/lookup items;
- `Applies to` class; rules are inherited by child classes unless the child defines its
  own rule (then the parent's rule and entries no longer apply to the child);
- **required attributes** cannot be empty;
- **criterion attributes** are the unique attribute sets used for matching.

Types:

| Type | Meaning | Guidance |
|---|---|---|
| **Independent** | Identifies a CI from its own attributes | Prefer this. Model CIs with a complete independent key. |
| **Dependent** | Requires identifying a parent/dependent CI and the relationship first | Use only when the CI cannot exist alone (NIC, app on host). Minimize; docs state two dependency levels is the maximum supported. |

Priority rules:

- Lowest `Order` runs first; custom identifiers must use a different order from defaults.
- Put the **strongest** identifier entry first.
- Limit entries, ideally to **one**; each extra entry costs performance.
- Avoid **lookup** identifier entries; they are explicitly discouraged for performance.
- Disable a rule rather than deleting it if you need to stop it temporarily.

Default rules in the base system:

| Rule | Applies to | Attributes |
|---|---|---|
| Hardware Rule | `cmdb_ci_hardware` | `serial_number`, `serial_number_type`, `name`, `ip_address`, `mac_address`; plus Serial Number and Network Adapter lookup tables |
| ESX Server Rule | `cmdb_ci_esx_server` | `correlation_id` |
| Storage Server Rule | `cmdb_ci_storage_server` | `cim_object_path`, `name`, `serial_number`, `serial_number_type`, `mac_address`, `ip_address`; plus Serial Number and Network Adapter |
| WBEM Service Rule | `cmdb_ci_wbem_service` | `cim_object_path` |

> Do not add `sys_class_name` as an attribute for an independent rule such as Hardware.
> If matching depends on class, create a rule per class and set `Applies to`.

**Inclusion rules** narrow which existing CIs participate in identification and in the
CMDB Health duplicate metric. They affect every script that calls IRE, so apply them
narrowly. Base system has none.

**Data source rules** block a source from **inserting** new CIs of a class while still
allowing it to update existing CIs. Stored in `cmdb_ire_data_source_rule`; child classes
inherit, child rules override. A blocked insert produces
`INSERT_NOT_ALLOWED_FOR_SOURCE`; with `CreateOrUpdateCIEnhanced()` the item is stored as
a partial payload.

### 6.3 Reconciliation rules

| Type | Basis | Precedence | Requirements |
|---|---|---|---|
| **Static** | Source priority per class/attribute | Lower than dynamic for the same attribute | A rule per authorized source/attribute; stored in `cmdb_reconciliation_definition` |
| **Dynamic** | Attribute values processed by CMDB 360 (e.g., largest/most-reported) | **Wins** over static for the same attribute | CMDB 360 must be enabled; one dynamic rule per class attribute; stored in `cmdb_dynamic_reconciliation_definition` |

Key behaviors:

- Child-class rules override parent-class rules.
- A rule with an empty attribute list authorizes all attributes in the class; specific
  attribute rules override broader rules.
- Overlapping static rules for the same attribute can coexist; IRE enforces them so
  sources do not overwrite each other.
- **Data refresh rules** complement static rules: after an effective duration with no
  update, the CI is treated as stale for that source and a lower-priority source may
  write. Duration `0` (default) means immediately stale. Data refresh has no effect when
  dynamic reconciliation is in effect.
- `glide.reconciliation.override.null` (default `true`) allows a lower-priority source to
  fill an empty field.

### 6.4 Reclassification

IRE can upgrade, downgrade, or switch a CI's class when a match is found. Controls:

- `glide.identification_engine.update_without_upgrade_enabled` (default `false`)
- `...update_without_downgrade_enabled`
- `...update_without_switch_enabled`
- reclassification restriction rules (`...reclassification_restriction_rules_enabled`,
  default `true`)
- payload `settings` flags `updateWithoutUpgrade`, `updateWithoutDowngrade`,
  `updateWithoutSwitch` take precedence over system settings
- automatic reclassification can be disabled, producing a **reclassification task**

### 6.5 Partial and incomplete payloads

- **Partial item:** lacks enough data for unique identification *but* has
  `source_name`/`source_native_key` or enough identifying context; stored in
  `cmdb_ire_partial_payloads` and retried when a later payload completes it.
- **Incomplete item:** lacks unique identification and has a non-partial error; stored in
  `cmdb_ire_incomplete_payloads` for logging and never retried.
- Partial payloads older than **90 days** are deleted.
- `glide.identification_engine.partial_payload_items_max_size` (default **1000**) bounds
  one partial payload; larger payloads are split.
- `CreateOrUpdateCIEnhanced()` enables partial payloads, partial commits, payload
  de-duplication, and optional summaries. `createOrUpdateCI()` does not allow partial
  commits: one blocked insert can fail the whole payload.

### 6.6 IRE performance guardrails (documented best practices)

- Limit each payload to **500 CIs**.
- Do not send duplicate items in one payload.
- Do not send system fields (`sys_domain`, `sys_updated_on`, `sys_mod_count`, etc.).
- Send only the criterion attributes required by the identification rule.
- Use `sys_id` when available; IRE can locate the CI directly.
- When inserting many CIs that depend on the same parent, **serialize** API calls to
  avoid clogging the system.

> Sources: [IRE](https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/ire.html),
> [Components and process](https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/c_CompsandProcessIDandReconcil.html),
> [Identification rules](https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/c_IdentificationRules.html),
> [Reconciliation rules](https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/r_ReconciliationRulesPrinciples.html),
> [Identification guidelines](https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/best-practices-id-reconcile.html),
> [IRE properties](https://www.servicenow.com/docs/api/khub/maps/zf4CFrQ4oaR8UN3GV4kT5g/topics/rjKNaLRC6pTLNgUV3Yq9wA/content?target=DESIGNED_READER).

---

## 7. Duplicate prevention and insert-vs-update control

### 7.1 The insert/update decision table

| Condition | IRE action | What you see |
|---|---|---|
| Identifier matches exactly one CI | **Update** | Attributes reconciled; `last_discovered`/`discovery_source` updated |
| No identifier match and inserts allowed | **Insert** | New CI; reconciliation not applied |
| No match but data source rule blocks insert | **Blocked** | `INSERT_NOT_ALLOWED_FOR_SOURCE`; Enhanced API stores a partial payload |
| Insufficient identifying data | **Partial / incomplete** | Partial stored for later merge, or incomplete logged and never retried |
| Multiple matches, count < threshold, `skip_duplicates=true` | **Update oldest**, mark others | Oldest becomes main CI; others get `duplicate_of`; de-dup task created |
| Multiple matches, count ≥ threshold, or `skip_duplicates=false` | **Identification fails** | Error logged; de-dup task created; no update |
| Duplicate items inside one payload | **Deduplicated** before processing | One payload item processed |
| Matched CI requires class change | **Reclassify / task** | Automatic if allowed; otherwise reclassification task |

### 7.2 Root causes of duplicate CIs

1. **Weak identification rules** — matching on `name` alone, or on a lookup entry that
   is not unique.
2. **Unstable identifying attributes** — adapter renames, hostname churn, serial-number
   rewriting, or a changed native key under a stable source.
3. **IP reuse / DHCP** — two devices share an address over time; MAC/NIC bonding
   complicates this further.
4. **Multiple sources with no authority model** — discovery, SCCM, monitoring, and
   manual entry all insert without reconciliation/data-source rules.
5. **Lookup-table duplication** — duplicate serial-number records pointing at different
   CIs; IRE selects the older referenced CI unless configured to create de-dup tasks.
6. **Over-broad schedules** — scanning the same device through multiple ranges or
   behaviors; Shazzam range simplification only helps single-behavior schedules.
7. **Payload hygiene** — duplicate items in a payload, or missing criterion attributes
   that force partial/incomplete handling.

### 7.3 Prevention controls, by layer

**Design-time (CI Class Manager):**

- Model each class with a **complete independent identifier**; prefer independent rules.
- Put the strongest identifier entry at the **highest priority**; keep one entry where
  possible; avoid lookup entries.
- Add **required attributes** and **identification inclusion rules** where appropriate.
- Define **dependent relationship rules** (hosting/containment) only for genuinely
  dependent CIs; keep dependency depth ≤ 2.
- Create the rule at the correct class level; remember child rules override parent rules.

**Runtime (properties and IRE):**

- `glide.identification_engine.skip_duplicates = true` lets IRE pick the oldest match
  for small duplicate sets instead of failing.
- `glide.identification_engine.skip_duplicates.threshold = 5` is the safety bound; above
  it, identification fails as if skip were false.
- `glide.identification_engine.skip_sys_object_source_matching = true` prioritizes
  identification-rule matching over the `sys_object_source` shortcut. Use when the source
  native key is stable but identifying attributes change, which can otherwise create
  duplicates.
- `glide.identification_engine.lookup_match.create_duplicate_task_ci.enabled = false`
  (default) selects the older CI for lookup matches without a de-dup task; set `true`
  when such lookup duplication must be remediated.
- Use **IRE data source rules** to stop untrusted sources from inserting a class; allow
  them to update only.
- Use **reconciliation + data refresh** so only the authoritative source writes, and
  stale data can be refreshed.
- Enable **dynamic reconciliation** only with CMDB 360; it wins over static rules.
- Set `glide.duplicate_ci_remediator.max.cis` deliberately for large duplicate sets.

**Detection:**

- IRE always creates **de-duplication tasks** when it detects duplicate sets.
- `duplicate_of` references the main CI; the main CI has an empty `duplicate_of`.
- **CMDB Health** duplicate metrics and the **Identification Log** expose trends.
- **Identification simulation** (`All > Configuration > Identification/Reconciliation >
  Identification Simulation`) lets you test a payload without committing; use it before
  changing rules.

**Remediation:**

- **Bulk:** CMDB Workspace De-duplication Dashboard + Template Library; create templates
  per class, review tasks, run templates in bulk.
- **Single task:** Duplicate CI Remediator wizard; choose the main CI, then merge
  attributes, relationships, and related items (or retain the main CI as-is).
- Asset-related tables are **not** merged; inactive change requests referencing a
  duplicate CI have the CI field cleared rather than merged.
- Related-table workflows can be disabled during remediation via
  `glide.duplicate_ci_remediator.merge_related_items_enhanced` plus an entry in
  `reconcile_duplicate_related_table_config`; base system does this for `change_request`
  and `task_ci`.

> Sources: [Detecting duplicate CIs](https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/id-detect-dup-ci.html),
> [Duplicate CIs remediation](https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/de-duplication-tasks.html),
> [Duplicate CI properties](https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/properties-duplicate-ci.html),
> [Identification simulation](https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/identification-simulation.html).

---

## 8. CI Class Manager — breadcrumbs and tab map

### 8.1 Access

```
All > Configuration > CI Class Manager
```

- `sn_cmdb_admin` — full access to all sections.
- `sn_cmdb_editor` — read-only access.
- CI Class Manager **does not support non-CMDB tables**; use the non-CMDB IRE procedures
  for those.

### 8.2 Navigation inside the tool

```
CI Class Manager
└── Hierarchy (CI Classes list)
    └── <select a class>
        ├── Class Info
        │   ├── Basic information / definitions / metadata
        │   ├── Attributes
        │   └── Suggested relationships
        ├── Identification
        │   ├── Identification rule (identifier entries, priorities)
        │   └── Inclusion rule (advanced)
        ├── Reconciliation Rules
        │   ├── Static reconciliation rules
        │   └── Data refresh rules
        ├── Dependencies
        │   └── Hosting / containment dependent relationship rules
        └── Health
            ├── Compliance audit
            ├── Certification template
            ├── Orphan rule
            ├── Staleness rule
            ├── Recommended/mandatory attributes
            └── Health inclusion rule
```

### 8.3 Creating a child class — wizard order

1. **Provide Basic Info** — display name, table name (`u_cmdb_ci…` prefix is fixed),
   description, icon, extensible, principal class.
2. **Add Attributes** — add columns; mark an attribute as an identifier by setting its
   **Identification Rule** column to `true`.
3. **Set Identification Rule** — inspect the derived rule; **Replace** it to define
   class-specific identifier entries.
4. **Dependencies** — add dependent rules (only shown when dependent identification
   rules exist).
5. **Add Reconciliation Rules** — add static reconciliation rules and data refresh
   rules.
6. **Add Suggested Relationships** — review/add relationship targets.

### 8.4 Related screens outside the tool

| Task | Path |
|---|---|
| Identification simulation | `All > Configuration > Identification/Reconciliation > Identification Simulation` |
| IRE data source rules | `All > Configuration > Identification/Reconciliation > IRE Data Source Rule` |
| Identification inclusion rules list | `All > Configuration > Identification/Reconciliation > Identification Inclusion Rules` |
| CMDB IRE properties | `All > Configuration > CMDB Properties > Identification/Reconciliation Properties` |
| Discovery properties | `All > Discovery > Discovery Definition > Properties` |
| Metadata Editor (hosting/containment groups) | `All > Configuration > Metadata Editor` |

> Sources: [CI Class Manager](https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/ci-class-manager-landing-page.html),
> [Create a CI class](https://www.servicenow.com/docs/api/khub/maps/zf4CFrQ4oaR8UN3GV4kT5g/topics/hIFyNjLNGj9RmtXizqEOyw/content?target=DESIGNED_READER),
> [Create dependent relationship rules](https://www.servicenow.com/docs/api/khub/maps/zf4CFrQ4oaR8UN3GV4kT5g/topics/XHZYKW~Jnu8UYCdUN0xRXg/content?target=DESIGNED_READER),
> [Create an inclusion rule](https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/create-id-inclusion-rule.html),
> [Create a data refresh rule](https://www.servicenow.com/docs/api/khub/maps/zf4CFrQ4oaR8UN3GV4kT5g/topics/ZWHWQE_uf8LNI2g9a0mcPw/content?target=DESIGNED_READER).

---

## 9. Validation and observability

| What | Where | What to look for |
|---|---|---|
| Discovery Status | `Discovery > Discovery Status` (also related list on the schedule) | State progression, completed/current activity, device history |
| ECC Queue | `Discovery > ECC Queue` | Raw probe/pattern XML payloads; proves what was returned |
| Discovery Log | `Discovery > Discovery Log` | Debug/Info/Warning/Error by probe, device, CI, ECC input |
| Discovery Home | `Discovery > Home` | Schedule summaries, cloud resources, error details and remediation hints |
| CI Identification Log | `Configuration > Identification Logs` | Identification decisions; enable with `glide.discovery.debug.ci_identification` |
| Identification simulation | `Configuration > Identification/Reconciliation` | Payload output and execution log **without** committing |
| CMDB Health | CMDB Workspace / Health dashboard | Duplicate, orphan, staleness, compliance KPIs |

Canceling an active discovery: started sensor jobs are terminated immediately; jobs in
`Ready` that have not started are deleted.

> Sources: [Schedule a horizontal discovery](https://www.servicenow.com/docs/r/it-operations-management/discovery/t_CreateADiscoverySchedule.html),
> [Discovery status](https://www.servicenow.com/docs/r/it-operations-management/discovery/c_DiscoveryStatus.html),
> [Discovery logs](https://www.servicenow.com/docs/r/it-operations-management/discovery/r_DiscoveryLog.html).

---

## 10. Risks and anti-patterns

| Anti-pattern | Why it hurts | Correct move |
|---|---|---|
| Name-only identification | Renames and duplicate hostnames create new CIs | Add serial/UUID/MAC; use a strong independent key |
| More identifier entries "for safety" | Each entry adds matching cost; weak entries can match the wrong CI | One strong entry; extra entries only with evidence |
| Lookup identifier entries | Performance cost; duplicate lookup rows cause ambiguous matches | Redesign to independent attributes; if unavoidable, monitor lookup duplicates |
| `skip_duplicates=false` everywhere | Any small duplicate set fails identification | Keep `true` with a deliberate threshold; investigate the cause |
| Raising the threshold without fixing rules | Masks duplicates instead of preventing them | Fix rules, then re-tune threshold |
| One giant schedule for everything | Long runs, stacked invocations, hard to isolate failures | Split by network/domain/credential; use behaviors and chaining |
| Untrusted source allowed to insert | Low-quality CIs and duplicates | IRE data-source rule: update-only |
| No reconciliation owner | Sources overwrite each other | Static priority + data refresh, or dynamic with CMDB 360 |
| Deleting CIs to "clean up" | Breaks relationships/history; may be recreated next run | Use de-dup remediation and deletion strategies |
| Changing serial-number syntax | Breaks asset tracking and matching | Preserve raw serial numbers |
| Ignoring `max run time`/`max idle` | Stuck runs pile up | Set both; monitor status |

---

## 11. Clarifications / open questions

These do **not** block the reference, but they block customer-specific tuning:

1. **Release and patch level** — this reference is Brazil (docs dated 2026-11-05/10).
   Older releases differ in UI labels and some defaults (noted where known).
2. **Probe-based, pattern-based, or both?** The identification path and deletion
   behavior differ. Most modern deployments use patterns, but the docs still support
   probes/sensors.
3. **Authoritative sources** — which systems may write which attributes? That determines
   static reconciliation, data refresh, and data-source rules.
4. **CMDB 360 / dynamic IRE licensed and enabled?** Dynamic reconciliation requires it.
5. **Definition of duplicate** — CI records only, or lookup/related items too? The latter
   needs `cmdb_duplicate_lookup_related_allowed_class` entries.
6. **Domain separation** — rules and schedules are domain-scoped; confirm the target
   domain before designing.
7. **Scale** — number of IPs, devices, and MID Servers determines batch size, behaviors,
   and whether event processing is warranted.

---

## 12. Source map

All sources were retrieved from the ServiceNow docs **Brazil** maps on 2026-11-13:

- ITOM map: `bsp_DjPRMilbWYHwwVa4zQ`
- Platform capabilities map: `zf4CFrQ4oaR8UN3GV4kT5g`

The complete topic list with content IDs and API URLs is in
[`../../research/SOURCES.md`](../../research/SOURCES.md). Primary canonical pages:

| Topic | URL |
|---|---|
| Discovery overview | https://www.servicenow.com/docs/r/it-operations-management/discovery/r-discovery.html |
| Exploring Discovery | https://www.servicenow.com/docs/r/it-operations-management/discovery/c_GetStartedWithDiscovery.html |
| Configuring Discovery | https://www.servicenow.com/docs/r/it-operations-management/discovery/c_DiscoveryConfiguration.html |
| Set up without Guided Setup | https://www.servicenow.com/docs/r/it-operations-management/discovery/t_ConfigureDiscovery.html |
| Discovery properties | https://www.servicenow.com/docs/r/it-operations-management/discovery/r_DiscoveryProperties.html |
| Discovery schedule form | https://www.servicenow.com/docs/r/it-operations-management/discovery/discovery-schedule-form.html |
| Discovery classifiers | https://www.servicenow.com/docs/r/it-operations-management/discovery/discovery-classifiers.html |
| Discovery identifiers | https://www.servicenow.com/docs/r/it-operations-management/discovery/c_DiscoveryIdentifiers.html |
| Discovery behaviors | https://www.servicenow.com/docs/r/it-operations-management/discovery/c_DiscoveryBehaviors.html |
| Deletion strategies | https://www.servicenow.com/docs/r/it-operations-management/discovery/deletion-strategy.html |
| CI Class Manager | https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/ci-class-manager-landing-page.html |
| CMDB IRE | https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/c_CMDBIdentifyandReconcile.html |
| IRE engine | https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/ire.html |
| Identification rules | https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/c_IdentificationRules.html |
| Reconciliation rules | https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/r_ReconciliationRulesPrinciples.html |
| Detecting duplicate CIs | https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/id-detect-dup-ci.html |
| Duplicate CIs remediation | https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/de-duplication-tasks.html |
| Identification simulation | https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/identification-simulation.html |
| CMDB 360 | https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/multisource-cmdb.html |
| CMDB Health | https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/c_CMDBHealth.html |
