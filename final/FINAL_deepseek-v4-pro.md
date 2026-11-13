# FINAL — ServiceNow Discovery & CMDB Configuration (Merged Reference)

- **Compiled by:** `deepseek-v4-pro` / provider **DeepSeek** / harness **Kilo** (`deepseek-v4-pro__deepseek__kilo`)
- **Date:** 2026-11-13
- **Purpose:** Exhaustive merged summary of every agent's findings in `eltonaguiar/ALT_PARALLELSWARM`, with duplicates cross-validated and reconciled against the official ServiceNow docs.
- **Release basis:** Official `docs.servicenow.com` **Brazil** release (2026-09-10+), with notes where a source pinned a different release.

---

## 0. Provenance & method

| Agent | Model / provider / harness | Primary doc |
|---|---|---|
| DSF | `deepseek-flash` / OpenRouter / Kilo CLI | 59 KB reference + `swarm/evidence/duplicates.md` |
| DV4 | `deepseek-v4.1-flash-fast` / Freebuff (Buffy) | 42 KB reference |
| INK | `inkling-2-small` / OpenRouter / Kilo | 26 KB reference + 10 raw official docs |
| WT1 | `deepseek-v4-flash` / DeepSeek / Hermes | 22 KB reference (8/8 QA, 26 sources) |
| WT5 | `openrouter-free` / OpenRouter / Kilo | 8 KB reference |
| WT4 | `qwen3-30b-a3b` / Ollama / Hermes | 5 KB reference |
| WT2 | `qwen2.5-7b` / Ollama / Hermes | 2 KB reference |
| WT3 | `llama3.1-8b` / Ollama / Hermes | 0.5 KB (empty — unusable) |
| A | `kilo-ernie-5.5-flash` / Baidu / Kilo | discovery config options, duplicate avoidance |
| F | `particle-1` / OpenRouter / alt-swarm | CI Class Manager breadcrumbs |
| G | `qwen2.5-coder-7b` / Ollama / alt-swarm | duplicate prevention |
| H | `qwen3.5-4b` / Ollama / alt-swarm | config options & order |
| **Kilo (me)** | `deepseek-v4-pro` / DeepSeek / Kilo | 25-source reference + IRE applicability matrix |

**Validation method:** every fact that appeared in 2+ agents was checked against the official docs (`c_DiscoProcessFlows`, `c_IdentificationRules`, `r_ReconciliationRulesPrinciples`, `create-reconciliation-rule`, `create-ire-data-source-rule`, `create-datasource-staleness-rule`, `id-detect-dup-ci`, `properties-id-reconciliation`, `ci-class-manager-landing-page`, `discovery-identifiers`, `discovery-classifiers`, `best-practices-id-reconcile`, plus `discovery_properties.txt` / `ire_properties.txt` raw). Conflicts and their resolutions are logged in §9.

---

## 1. Discovery configuration surface

### 1.1 Subscription, roles, entry points
- Discovery requires a **separate subscription / plugin activation** (DSF, DV4, H).
- Roles: **`discovery_admin`** (or `admin`) to configure/execute; MID Server service account needs **`mid_server`** (DSF, DV4, H).
- Entry points (release-dependent wording):
  - `All > Discovery > Discovery Schedules` (Brazil) / `All > ITOM > Discovery > Discovery Schedules` (classic) (DSF, A, H)
  - `All > Discovery > Discovery Status`, `> Discovery Log`, `> Discovery Definition > Properties`, `> MID Servers`, `> Credentials`, `> CI Classifiers`, `> Behaviors`, `> Probes`, `> Patterns`
  - Direct table URLs: `discovery_schedule_list.do`, `discovery_status_list.do`, `cmdb_ci_class_manager.do`, `ecc_queue_list.do` (A)
  - `All > Configuration > CI Class Manager`; `All > Configuration > Identification/Reconciliation` (Identification, CI Identifiers, Inclusion Rules, Reconciliation Definitions, IRE Data Source Rule, Identification Simulation, Identification Log) (DSF, A, F)
  - `All > Configuration > CMDB Properties > Identification/Reconciliation Properties` (DSF)

### 1.2 MID Server
- Polls the instance for work; executes probes/patterns; returns results; retains no discovery data. All traffic is **outbound SOAP/HTTPS** (no inbound firewall rule / VPN) (DSF).
- Firewall: allow outbound to the instance on **443** (DV4).
- Install **two or more** MID Servers on different schedules/ranges (DSF, DV4, H).
- MID Server must be assigned the **Discovery** application or **ALL**; mandatory since **Istanbul** (DSF, DV4, H).
- **Auto-Select** sequence: 1) MID with Discovery/ALL app + matching IP range; 2) first `Up` (random if several); 3) default MID Server for Discovery, then ALL; 4) `Paused`/`Upgrading` fallback. **Not supported for IPv6** (DSF, DV4, H). Selecting a specific MID auto-adds the Discovery app (DV4).
- **Cluster selection** prefers the lowest `Order` value that is `Up`, falls back to `Paused`/`Upgrading`, **ignores default-MID settings**, and a MID belongs to **one cluster only** (DV4).
- Port-scan (Shazzam) work is spread across batch size × MIDs (DV4).
- **Behaviors** (not one giant MID) are the tool for load balancing, multi-domain, ACL-protected SNMP, and dual-protocol devices (DSF, DV4, A).

### 1.3 Credentials
- Types: **SSH** (user/password/key), **WMI** (Windows), **SNMP** (v1/v2c/v3), **IPMI**, **vCenter** (A, H).
- Windows/WMI credentials come from the MID Server service login (needs local admin on targets); SSH/SNMP/vCenter are stored in `discoverycredentials` and decrypted on the MID (DSF, DV4).
- Credential **order**, **affinity** (per schedule / per IP range), and **aliases** control which credential is tried where (DV4, A).
- Windows MID Server must be **domain-joined**; SNMP ACLs must allow the MID Server host (A).

### 1.4 Schedules
- Fields: **Name**, **Discover** (Configuration items / IP addresses / Networks / Service / Serverless / Cloud application / Cloud resources / Certificates), **MID selection method** (Auto-Select / Specific MID Cluster / Specific MID Server / Use Behavior), **Active**, **Location**, **Max run time**, **Max Idle time** (hidden column; measured from last ECC Queue change), **Run** (Daily/Weekly/Monthly/Once/On demand/Periodically/After Discovery), **Log state changes**, **Shazzam batch size**, **Shazzam cluster support**, **Use SNMP Version** (ALL/v1/v2c/v3), **Quick ranges**, **IP Ranges** (related list), **Discovery Range Sets**, **Discovery Status** (A, H, DSF, DV4).
- **`Discover` semantics:** *Configuration items* = credentialed scan that writes CIs; *IP addresses* = credential-less scan creating **device history only, never CIs** (DSF, DV4, A).
- **Shazzam batch size** default **1000**; minimum effective **256** (UI converts lower to 0) (DSF, DV4).
- **Run after = After Discovery** is chainable, with "Even if canceled" (DSF).
- **`glide.discovery.max_concurrent_invocations_per_schedule`** default **3** caps stacked runs of the same schedule; 0/negative disables (DSF, A, H).
- **Range sets** are reusable groups of ranges; a schedule scans only its attached ranges (DSF, DV4).
- IP range methods: address list, range, CIDR network (CIDR auto-excludes network/broadcast); per-range excludes + a global exclusion list; **>500,000 excluded addresses cancels the discovery** (DV4).
- **IPv6** is not supported for range/network definitions (IPv6 address-list scans are available); auto-select unsupported for IPv6 (DV4, DSF).

### 1.5 Behaviors / functionalities
- A **Behavior** holds one or more **Discovery functionalities**; a functionality links a functionality definition (protocol list), the MID Servers, a **phase** (integer — same-phase functionalities run in one Shazzam probe, phases run numerically), and optional functionality criteria (`mid_server`, `win_domain`, `mid_win_domain`) (A).
- A Behavior **must have at least one functionality** or it does not work properly (WT1).
- Quick Discovery is "free" to test **all** credentials; a Behavior tests only the defined port probes (WT1).
- Common functionalities: Windows only (WMI), Windows/DNS/WINS, SNMP only, All except SNMP, All except Windows (A).

### 1.6 Classifiers
- Three types: **device**, **process**, **IP address (IP scan)** (INK).
- Device classification identifies Windows/UNIX/Linux, routers, switches, load balancers; triggers active-processes probe. **HTTP classification** (since Madrid) is **lowest priority** — used only if Shazzam sees 80/443 open and WMI/SSH/SNMP fail (INK).
- Process classification classifies applications from running processes during **exploration**, creates child CIs with **Runs on::Runs** relationships; process-handler scripts strip inconsistent parameters **before** classification → prevents duplicate application CIs (INK).
- IP-address classification is credential-less, uses open ports/banners, updates the CI when criteria are met, then launches exploration probes (INK).
- Criteria = **parameter / operator / value**; process-classifier conditions are **case-sensitive** (INK).
- A **Horizontal Pattern probe** can be attached to a classifier to launch patterns instead of probes (INK).
- Debug: `glide.discovery.debug.classification` = `false` (INK).

### 1.7 Probes, patterns, Configuration Console
- Probes/sensors are JavaScript-based; **Patterns** are written in Neebula Discovery Language (NDL) and cover identification + exploration via the Horizontal Pattern probe (DSF).
- **ITOM Configuration Console** is the fast path (install/update apps, interactive pages, task assignment, automated implementation by ServiceNow Otto); it manages specific CI types, details (OS info), ARP data, software packages, and File-Based Discovery, but shows only *some* supported applications (INK, H, WT4).
- Discovery returns **all** data to the instance before console settings are applied; the instance ignores excluded data when updating the CMDB (H).

### 1.8 Modes
- Horizontal discovery (bottom-up), Service Mapping (top-down), IP Scan (credential-less, no CIs), Cloud Discovery (A).

---

## 2. Order of operations

### 2.1 Canonical runtime order — the 4 phases
Confirmed by official `c_DiscoProcessFlows`, and by DSF, DV4, WT1 (majority):

1. **Scanning (Shazzam)** — port probes (WMI 135, SSH 22, SNMP 161, HTTP 80/443) find live IPs and open ports; results appear in the Shazzam probe's *input*.
2. **Classification** — one classification probe per device decides the CI class (OS version, device type); **first phase that uses credentials**; uses the **Port Probe table** to pick the Classify probe. Supported protocols: **SSH, WMI, SNMP, CIM**.
3. **Identification** — the identification trigger probe (or the **Horizontal Pattern probe** for patterns) collects identity data; sensors process it; IRE matches against the CMDB → **update existing or create new**. **Only phase that writes the CMDB** (and only for Configuration-item schedules).
4. **Exploration** — trigger probes collect in-depth info (OS, CPU, memory, processes, software, relationships); **File-Based Discovery runs here**.

- Each phase follows the previous only on a positive result ("dominos" — WT1).
- The **ECC queue** exposes the four phases as two Queue values and four State values (WT1).
- With **patterns**, the Horizontal Pattern probe covers both Identification and Exploration; probes/sensors are not used (DSF, WT1).
- Validation method: run Quick Discovery from the schedule (IP + MID Server), then check `cmdb_ci` (WT1).

### 2.2 Alternative framings (from other agents — not canonical)
- **WT5 (openrouter-free):** 6 steps — Launch → Network Discovery → Pattern Matching → CMDB Identification → Reconciliation → Insert/Update.
- **WT2 (qwen2.5-7b):** 4 steps — Probe Execution → Data Collection → Data Parsing → CMDB Update.
- **H (qwen3.5):** 6-step *setup* order — Role Assignment → MID Provisioning → Credential Configuration → Schedule Definition → Configuration Console Application → CMDB Update.
- These are partial/simplified taxonomies; the 4-phase model is authoritative. See §9 (conflict C-B1).

### 2.3 Setup / governance order (DSF, DV4)
roles → scope design → MID install/verify → credentials + test → ranges/exclusions → **fix identification/dependent rules before scale** → schedule → narrow pilot → then tune reconciliation / data-source rules. Design the CI class + identification rule **before** enabling broad schedules; name-only identifiers cause duplicate floods.

---

## 3. CI Class Manager

- Path: **`All > Configuration > CI Class Manager`** (`cmdb_ci_class_manager.do`). Manages the CMDB class hierarchy; does **not** manage non-CMDB tables (DSF, A, B, F, D, E).
- Roles: **`sn_cmdb_admin`** full; **`sn_cmdb_editor`** / **`itil`** read (B, F). Per-task: creating a class needs `sn_cmdb_admin`/`itil_admin` + `personalize_dictionary`; dependent-relationship read = `sn_cmdb_editor` + `itil`; identification simulation = `sn_cmdb_admin`/`admin` (F).

### 3.1 Tabs (per class)
| Tab | Purpose |
|---|---|
| **Class Info → Basic Info** | display name (≤80 chars, unique), table name (`u_cmdb_ci_*`, lowercase/underscore, ≤80), description, icon, **Extensible**, **Principal Class** |
| **Attributes** | view/add/edit attributes; set **`Identification = true`** to make an attribute an identifier |
| **Identification and Reconciliation** | create/delete **identification rules**, **identification inclusion rules**, **reconciliation rules**, **data refresh rules** |
| **Dependent Relationships** | hosting/containment rules required for dependent identification |
| **Suggested Relationships** | relationships suggested in Query Builder (`Base class`, `Relationship`, `Dependent class`) |
| **All Relationship Rules** | combined suggested + dependent relationships |
| **Health** | compliance audit, certification template, orphan rule, **staleness rule**, recommended/mandatory attributes, health inclusion rules |
| **CI List** | list/create/delete CIs of this class |

### 3.2 IRE sub-sections (under Class Info)
- **Identification** — CI identification rules; identification inclusion rules
- **Reconciliation** — CI reconciliation rules; **Data Refresh Rules**
- **Dependencies** — dependent relationship rules (hosting/containment)

### 3.3 Create-child-class flow
Hierarchy → pick an **Extensible** parent → **Add Child Class** → Basic Info → Add Attributes (mark identifier) → **Set Identification Rule** (review the *Derived* rule + entries; optionally **Replace**) → Dependencies → **Add Reconciliation Rules** (+ **Data Refresh Rules**) → Suggested Relationships → Done (DSF, A, B, F).

### 3.4 Related screens
- **Identification Simulation** — `Configuration > Identification/Reconciliation > Identification Simulation`; simulate payloads without committing (uses `createOrUpdateCI()` for final execution) (DSF, F).
- **Identification Log** — `Configuration > Identification and Reconciliation > Identification Log`; troubleshoot IRE (WT1, DSF).
- **IRE Data Source Rule** — `All > Configuration > Identification/Reconciliation > IRE Data Source Rule` (**not** a CI Class Manager tab) (DSF, DV4, INK).

---

## 4. The four IRE rule families

> The four controls are **not** uniformly "per class, on insert and update." Each has its own scope and insert-vs-update behaviour.

### 4.1 Applicability matrix (insert vs update)

| Rule family | Scope | INSERT? | UPDATE? |
|---|---|---|---|
| **Identification rules** | one rule per CI class (descendants derive; child overrides) | **YES** — no match → create | **YES** — match → update |
| **Reconciliation rules** (static/dynamic) | per class + per source + per attribute (or "Apply to all attributes") | **NO** | **YES** |
| **IRE data source rules** | per class + per source | **YES — blocks insert** | **NO** (update still allowed) |
| **Data refresh rules** | per class + per source | **NO** | **YES** — stale → lower-priority source may update |

Plus: **Identification inclusion rules** (class-level row filter) and **Exclude classes from Dynamic IRE** (`cmdb_dynamic_ire_skip_class`).

### 4.2 Identification rules
- Answer **"does this CI already exist?"**; run on **both** insert and update (C, D, E, F).
- **Matching order:** 1) `source_name` + `source_native_key` (from `sys_object_source_info` / `Source [sys_object_source]`) — fastest; `glide.identification_engine.skip_sys_object_source_matching` (default `false`) forces rule-based matching even when source keys exist; 2) identification rules / identifier entries; 3) `sysId` — if the payload provides the CI's `sysId`, IRE locates it directly (C, D, G).
- **Rule structure:** one identifier per rule; one or more **identifier entries** with distinct **priorities**; optional **related entries**. Entry types:
  - **Regular** — the CI's own attributes (preferred; e.g. `name` + `serial_number`)
  - **Lookup** — a related table that references the CI (e.g. `cmdb_serial_number`); join cost; prefer **Enforce exact count match**
  - **Hybrid** — regular + lookup
- **Best practices:** prefer **independent** rules; minimize **dependent** rules (max two dependency levels); avoid lookup entries (performance); limit entries (ideally **1**); strongest entries get **highest priority**; define the rule at the correct class level (C, D, G).
- Attributes used in an identifier must be flagged **`Identification = true`** on the class (B, D, F).
- **Child classes derive** the parent's rule (including related entries) unless they define their own; defining one **replaces** the derived rule entirely — re-add needed related entries (DSF, DV4).
- `sys_class_name` cannot be an identification attribute of an **independent** rule (DSF, DV4).
- **Never** define a parent lookup entry and a child class identifier for the same table — the contradiction produces duplicates (DV4, DSF).
- **Default shipped rules:** Hardware Rule (`cmdb_ci_hardware`: serial_number, serial_number_type, name, ip_address, mac_address + lookups), ESX Server Rule (`correlation_id`), Storage Server Rule (`cim_object_path`, name, serial fields, MAC, IP + lookups), WBEM Service Rule (`cim_object_path`) (DSF, DV4, INK).
- `glide.discovery.debug.ci_identification = true` → **CI Identification Log** (A, C, D).

### 4.3 Reconciliation rules
- Answer **"which data source may write which attribute?"**; run **only on update** — **not applied on insert** (C, D, E, F).
- **Static rules** (`cmdb_reconciliation_definition`): per class/attribute, priority-ordered; lower number = higher authority; child overrides parent; an attribute-specific rule **beats** an "Apply to all attributes" rule regardless of priority; overlapping rules for different sources **coexist** (IRE uses Data Source History to prevent overwrites); empty attribute list = whole class (C, D).
- **Dynamic rules** (`cmdb_dynamic_reconciliation_definition`): CMDB 360 chooses the **largest / most-reported** value; one rule per class+attribute; requires CMDB 360; **dynamic beats static** for the same attribute (C, D).
- **Per-rule fields:** `Active`, `Discovery source`, `Priority`, **`Apply to all attributes` vs explicit `Attributes`**, **`Update with Null`**, **`Filter Condition`** (e.g. `[Department] [is] [Finance]`) (DSF, A).
- **Cannot** target system fields or IRE fields (`discovery_source`); rules cannot be dot-walked through reference fields (DSF).
- `glide.reconciliation.override.null` (default `true`) lets a lower-priority source fill an **empty** field (DSF, DV4, A).
- `glide.identification_engine.enable_reconciliation_filter_before_update` (default `false`) controls filter timing (DSF, A).
- **Data Source Precedence Rules** (`cmdb_datasource_last_update`) resolve "flipping" when reconciliation alone is insufficient (WT1, KB0756709).
- With **Domain Separation**, reconciliation rules are domain-scoped; parent-domain rules apply to child domains unless overridden (DV4).
- **Reclassification flags** (payload `settings`): `updateWithoutUpgrade`, `updateWithoutDowngrade`, `updateWithoutSwitch` — override `glide.class.*`; evaluated during **Exploration**; stored in `cmdb_ci.reclassification_flag` (C, E, DSF).

### 4.4 IRE data source rules
- **Create-only gate:** prevents a specific source from **inserting** new CIs of a class; still permits **updates** (DSF, DV4, C, F).
- Table `cmdb_ire_data_source_rule`; fields: **`Active`**, **`Applies to`** (class + children), **`Data source`**, **`Insert Not Allowed`** (DSF, DV4, INK).
- Evaluated **only** when identification finds no match and IRE is about to insert (DSF, DV4).
- Child classes inherit; a child rule overrides the parent; **one active rule per class/source pair** (DSF, DV4).
- Does **not** apply to lookup/related items (DSF, DV4).
- Blocked insert → error `INSERT_NOT_ALLOWED_FOR_SOURCE`; with **`CreateOrUpdateCIEnhanced()`** the item is stored as a **partial payload**; with **`createOrUpdateCI()`** the whole payload fails (no partial commits) (DSF, DV4).
- A later permitted source's insert **merges** the stored partial payload, deletes it, and then the previously-blocked source may update that CI (DSF, DV4).
- **No impact when dynamic reconciliation rules are in effect** (DSF, DV4, INK).

### 4.5 Data refresh / staleness rules
- Mark a CI **stale** for a specific source so a **lower-priority** authorized source may update it; **update-only** (DSF, DV4, C, D, E).
- Location: CI Class Manager → Hierarchy → class → Class Info → **Reconciliation Rules → Data Refresh Rules → Add** (DSF, DV4).
- Fields: **`Discovery source`**, **`Effective Duration`**, **`Active`** (DSF, DV4).
- **`Effective Duration = 0`** (default) → immediately stale → lower-priority source always authorized (DSF).
- Refresh can only write fields the source is authorized to update by static reconciliation (DSF).
- **No effect when dynamic reconciliation is in effect** (DSF, DV4).
- Staleness is evaluated against **Data Source History** (`cmdb_datasource_last_update`), not just `sys_updated_on` (DV4).
- **Non-CMDB tables** use `Data Source Staleness Definitions` (`cmdb_datasource_staleness`) with Applies to / Data source / Effective Duration (DV4).
- CMDB Health **staleness rule is reporting-only** (correctness KPI); Discovery's stale-setting takes precedence (DV4).
- Avoid **ping-pong**: strict priority for identity fields; staleness-aware refresh only for non-identifying attributes (DSF).

### 4.6 Identification inclusion rules
- Narrow **which rows of a class** participate in identification ("Inclusion Rule (Advanced)" → an **`Active record condition`**, e.g. only `install_status = Installed`) (DSF, DV4, A, WT5, WT2).
- **No predefined rules OOTB** → all CIs participate; they affect anything that calls IRE (Discovery, Service Mapping, import sets) (DSF, DV4).
- **Critical rule:** never scope an inclusion rule by **class** (e.g. on `cmdb_ci_hardware`) — child classes not included are not found, producing duplicates; filter on attributes/status instead (WT5, WT2, DV4).

### 4.7 Dynamic IRE (CMDB 360) & class exclusion
- `glide.identification_engine.dynamic_ire_enabled` (default `false`) switches to Dynamic IRE (Static off) (INK, DSf, DSF).
- When Dynamic IRE is in effect: dynamic beats static; **IRE data source rules and data refresh rules have no impact**; `cmdb_dynamic_ire_skip_class` can carve classes back out so Static IRE (and those two rules) keep applying (INK, DSF).
- `glide.identification_engine.dynamic_ire.auto_compare` (default `true`) compares Dynamic vs Static outputs (INK).

---

## 5. Duplicate CI prevention

### 5.1 Mechanisms
1. **Identification rules** (uniqueness) + inclusion rules (scope).
2. **IRE data source rules** (block untrusted inserts).
3. **Reconciliation + data refresh rules** (prevent overwrite flapping).
4. **`glide.identification_engine.skip_duplicates`** (auto-resolve small duplicate sets).
5. **De-duplication tasks** (review/remediation) + templates + Duplicate CI Remediator wizard.

### 5.2 `skip_duplicates` behaviour (official `id-detect-dup-ci`)
- `glide.identification_engine.skip_duplicates` default **`true`**; `glide.identification_engine.skip_duplicates.threshold` default **`5`** (C, D, E, G, INK, DSF).
- If `skip_duplicates = true` **and the number of duplicate CIs is *less than* the threshold** → the **oldest** duplicate is picked as the match and updated; it becomes the **main CI**; the rest are tagged `duplicate_of = <main>`; IRE filters out tagged CIs during matching (official doc).
- If `skip_duplicates = false` → matching **fails with an error**; **none** of the duplicates are updated (official doc).
- **In either case, de-duplication tasks are always created** (official doc, line 26) — see §9 conflict C-C2.
- Edge case: if IRE updates any attribute **other than** `duplicate_of` on a duplicate CI, it is **no longer considered a duplicate** and `duplicate_of` is cleared (official doc).
- `glide.duplicate_ci_remediator.max.cis` (default **1000**, ≤5000) bounds large remediation sets (C, D, E, INK, DSF).
- `glide.identification_engine.lookup_match.create_duplicate_task_ci.enabled` (default **`false`**) — for duplicate **lookup/related** items: `false` selects the older CI without a task; `true` also creates a task (C, D, INK, DSF). By default IRE does **not** create tasks for duplicate lookup (`cmdb_serial_number`) / related (`cmdb_software_instance`) items unless listed in `cmdb_duplicate_lookup_related_allowed_class` (INK, official).

### 5.3 Other duplicate guards
- `glide.discovery.enforce_unique_ips` (default `false`) clears a reused IP from other devices (DSF, INK) — **not** a CI dedup control.
- `glide.discovery.enable_mac_address_verification` (default `false`) detects IP/MAC change mid-discovery and stops that IP (DSF, INK).
- `glide.discovery.multi_page_serial_mode` (`false`; `true` serializes multi-page pattern payloads) — documented fix for duplicate CIs from parallel payload processing (DV4, DSF).
- Domain separation: servers in different domains with the same Correlation ID are **unique**, not duplicates (WT5).
- Custom query business rules on `cmdb_ci` tables can hide CIs from IRE → check and disable (WT5).
- ACLs on `cmdb_ci` can prevent IRE from finding existing CIs (WT5).
- Bonded/teamed NICs share IP/MAC; renaming an adapter makes Discovery mark the old CI `Install Status = Absent` and create a new one — use a `name`-based rule (DV4, INK).
- **Serial numbers are integrity-critical:** never reformat/prefix them in patterns or sensors (DSF, DV4, INK).
- **Correlation ID:** two CIs sharing a Correlation ID are treated as the **same CI** (duplicate) — unless domain separation applies (WT5; see §9 conflict C-B2).

### 5.4 Remediation
- **De-duplication tasks** are auto-created for duplicate sets; review in **CMDB Workspace → De-duplication Dashboard**; remediate in bulk with **templates** (CMDB Workspace → Template Library) or the **Duplicate CI Remediator** wizard (select main CI, merge attributes/relationships/related items) (WT1, INK, G).
- Gotchas: templates are **not retroactive**; the "Condition to filter CIs from the template class" is evaluated at the **CI level**, not the task level (WT1).
- Remediation roles: `itil` read; `itil_admin` / `cmdb_dedup_admin` write (DV4, INK).
- Troubleshooting checklist (KB0869861): identification rules → inclusion rules → business rules → ACLs → domain separation → `duplicate_of` → `discovery_source` → `IdentificationEngineScriptableApi` → identification simulation (WT5).
- `glide.discovery.debug.ci_identification = true` → CI Identification Log (A, C, D).

---

## 6. Insert vs update — decision summary

| Situation | Result |
|---|---|
| Exactly one identifier match | **UPDATE** the CI; reconciliation decides which attributes the source may write |
| No match + insert allowed | **INSERT** a new CI; reconciliation/data refresh **not applied** |
| No match + insert blocked by IRE data source rule | `INSERT_NOT_ALLOWED_FOR_SOURCE`; Enhanced API stores a partial payload |
| Multiple matches, `skip_duplicates=true`, < threshold | update the **oldest**, tag others `duplicate_of`, create a de-dup task |
| Multiple matches, ≥ threshold (or `skip_duplicates=false`) | identification **fails**; de-dup task created; no update |
| Matched but class change would help | **reclassification** (upgrade/downgrade/switch); payload flags override `glide.class.*` |
| Retired CI rediscovered | Discovery does **not** un-retire it (no OOTB behaviour); a custom Business Rule is required |
| Under-supplied payload | **partial item** (stored in `cmdb_ire_partial_payloads`, recoverable) or **incomplete item** (dead, `cmdb_ire_incomplete_payloads`) |

- Partial-item errors: `MISSING_MATCHING_ATTRIBUTES`, `REQUIRED_ATTRIBUTE_EMPTY`, `MISSING_DEPENDENCY`, `INSERT_NOT_ALLOWED_FOR_SOURCE` (INK).
- `createOrUpdateCI()` = no partial commits; any failing item fails the whole payload. `CreateOrUpdateCIEnhanced()` = `partial_commits` (default true) commits good items and parks bad ones (INK, DSF, DV4).
- Partial payload lifecycle: stored in `cmdb_ire_partial_payloads` (+ `_index`), merged on the next matching payload, **≤90-day** retention, **1000-item** cap, fetch limits **2000/5000** (DSF, DV4, INK).
- Dependent CIs are identified **after** their independent host.
- `first_discovered` / `last_discovered` are always stamped; the payload wins only if newer (`glide.identification_engine.skip_updating_source_last_discovered_if_older` default `true`) (INK, DSF).

---

## 7. Property reference

### 7.1 Discovery properties (`glide.discovery.*`)
| Property | Default | Effect |
|---|---|---|
| `exclude_ip_sync_classes` | `cmdb_ci_lb` | CI classes excluded from IP substitution (keep mgmt IP) |
| `enforce_unique_ips` | `false` | Clear a reused IP from other CIs |
| `bgp_router_disable` | `true` | Skip SNMP BGP routing probe/pattern |
| `debug.network_discovery` | `true` | Extensive network-discovery logging |
| `discoverable.network.max.netmask.bits` | `28` | Max regular netmask |
| `network_owner_method` | `Most Networks` | Router pick: First/Last/Most/Least Networks |
| `physical_interface_types` | `6,117,9,71,209` | Physical ifType list |
| `switch_interface_types` | `7,8,9,26,53,62,69,71,78,115,117,209` | Switch ifType list |
| `virtual_interface_types` | `53` | Virtual ifType list |
| `L3_mapping` | `true` | Map devices to routers/L3 switches |
| `network_discovery.functionality` | `SNMP only` | Network discovery method |
| `hostname.always_update` | `true` | Always update name from most recent trusted source |
| `hostname.case` | `Lower case` | Hostname casing |
| `hostname.dns_nbt_trusted` | `true` | Trust DNS/NetBIOS name |
| `hostname.snmp_trusted` / `.ssh_trusted` / `.wmi_trusted` | `false` (new Aus. `true`) | Trusted name sources |
| `hostname.include_domain` | `false` | Include domain in name |
| `fqdn.regex` | `^([^.]+)\.((?:[^.]+\.)+[^.]+)$` | FQDN parsing |
| `domain.name.nbt` | `true` | Windows domain via NBT |
| `max_concurrent_invocations_per_schedule` | `3` | Concurrency cap per schedule (0/neg disables) |
| `schedule_ipv4_limit` / `schedule_ipv6_limit` | `65536` / `20000` | Auto-schedule IP caps |
| `schedule_monitoring.stale_check_seconds` | `1200` | Run-monitoring staleness check |
| `retire_stale_accounts` | `false` | Remove stale cloud service accounts |
| `mark_esx_servers_as_absent` | `false` | ESX absent vs retired |
| `ip_based.active` | `true` | Scan all IPs of a device in one schedule |
| `ip_service_affinity` | `false` (new Aus. `true`) | Remember last discovered port |
| `sensors.fire_ssh_probe` | `true` | SSH probe when VIPs absent from SNMP |
| `sensors.save_attachments` | `true` | Keep ECC attachments after sensors |
| `shazzam_ranges_json` / `shazzam_simplify_ranges` | `true` / `true` | JSON ranges / dedupe IPs |
| `save_pattern_log` | `true` | Save pattern logs (always on failure) |
| `use_probe_results_cache` | `false` | Process changed probe results only |
| `log_debug` / `log_debug_info` | `false` | Debug logging / ECC debug info |
| `log_message_length` | `200` | Log message cap |
| `multi_page_serial_mode` | `false` | Serialize multi-page pattern payloads (dup fix) |
| `use_cmdb_identifiers` | `true` | Route through CMDB IRE vs legacy identifiers |
| `discover_software` | `true` | Software discovery |
| `populate_software_instance_table` | `false` | Populate software-instance tables |
| `enable.software_filter` | `true` | Windows software filtering |
| `enable.software_simplify` | `true` | Name/version cleanup |
| `software_sccm_managed` | `false` | Skip software for SCCM-managed CIs |
| `enable_file_tracking` | `true` | Pattern-based config-file tracking |
| `file_tracking.max_file_size` | `500000` | File-tracking size cap |
| `file_tracking.max_files_per_ci` | `50` | Files tracked per CI |
| `file_tracking.change_limit_count` / `.days` | `4` / `7` | Change limits |
| `enable_adme` | `false` | Enhanced ADM probe |
| `adm.update.applications` | `true` | Update app CIs from running-process status |
| `application_mapping` | `true` | Application mapping (relationships only) |
| `active_processes_filter` | `false` | Filter processes to classification matches |
| `discover_aws_ec2_host_metadata` / `discover_azure_host_metadata` | `true` / `true` | Cloud metadata probes |
| `enable_ssm` | `false` | AWS SSM discovery |
| `allow_loopback_adapters` | `false` | Discover SNMP loopback adapters |
| `enable_mac_address_verification` | `false` | MAC/IP change detection |
| `debug.ci_identification` | `false` | CI Identification Log |
| `debug.classification` | `false` | Classifier execution logging |
| `count.use_optimized_counter` | `true` | Optimized `discovery_status` counters |
| `warn_minor_version` | `false` | Warn on minor_version mismatch |
| `roundingInterval.cpu` / `.ram` | `1` / `1` | MHz/MB rounding |
| `use.event.processing` | `false` | Event-Framework processing |
| `event.separate.cloud.events` | `true` | Separate cloud events |
| `event.pin.jobs` | `false` | Pin event jobs |
| `certs.days_before_expiration_to_create_renewal_task` | `60` | Cert renewal task lead time |
| `certs.enable_renewal_task_creation_for_discovered_certificates` | `true` | Cert renewal tasks |

Other namespaces on the same page: `com.snc.use_external_credentials=true`; `com.glide.codesigning.tracking.unsupported_script_tracking.enabled=true`; `com.glide.queue.discovery.{cloud.,}sensors.processing_jobs.priority=100`; `mid.powershell.target_base_dir=admin$\temp`; `glide.ecc_agent.validated.override=false`; `glide.eccprobe.max_queued_probes_per_run=20`; `glide.eccprobe.awsrestprobe.max_retries=4`; `glide.eccprobe.awsrestprobe.max_wait=30`; `sn_disco_firewall.*`; `sn_disco_certmgmt.enable_csr_generation=false`, `.private_key_size=2048`; `sn_disco_workspace.*` (ML-based).

### 7.2 IRE / reconciliation properties
| Property | Default | Effect |
|---|---|---|
| `glide.identification_engine.skip_duplicates` | `true` | Auto-resolve small duplicate sets |
| `glide.identification_engine.skip_duplicates.threshold` | `5` | Above this, behaves as `skip_duplicates=false` |
| `glide.identification_engine.skip_sys_object_source_matching` | `false` | `false` = prefer source-native-key match; `true` = force IRE rules |
| `glide.identification_engine.lookup_match.create_duplicate_task_ci.enabled` | `false` | Create de-dup tasks for duplicate lookup/related items |
| `glide.identification_engine.non_dependency_relation.duplicate_detection` | `false` | Detect duplicate non-dependent relationships |
| `glide.identification_engine.dynamic_ire_enabled` | `false` | Use Dynamic IRE (Static off) |
| `glide.identification_engine.dynamic_ire.auto_compare` | `true` | Compare Dynamic vs Static outputs |
| `glide.class.upgrade.enabled` / `.downgrade.enabled` / `.switch.enabled` | `true` | Allow IRE reclassification (false = reject + task) |
| `glide.identification_engine.update_without_upgrade_enabled` / `.downgrade_` / `.switch_` | `false` | Process update but skip that reclassification |
| `glide.identification_engine.reclassification_restriction_rules_enabled` | `true` | Apply reclassification restriction rules |
| `glide.reconciliation.override.null` | `true` | Lower-priority source may fill an empty field |
| `glide.required.attribute.enabled` | `true` | Required attributes cannot be null |
| `glide.identification_engine.enable_reconciliation_filter_before_update` | `false` | Apply reconciliation filter before value change |
| `glide.identification_engine.enable_identifier_optional_condition` | `false` | Advanced conditions on regular identifier entries |
| `glide.identification_engine.partial_payload_items_max_size` | `1000` | Max items per partial payload |
| `glide.identification_engine.partial_items_process_limit` | `2000` | Max partial items fetched per call |
| `glide.identification_engine.partial_items_process_absolute_limit` | `5000` | Absolute fetch stop |
| `glide.identification_engine.skip_updating_source_last_discovered_if_older` | `true` | Don't back-date `last_discovered`/`discovery_source` |
| `glide.identification_engine.skip_updating_last_scan_if_older` | `true` | Don't back-date `sys_object_source.last_scan` |
| `glide.identification_engine.batch_update_last_discovered` | `true` | Batch `last_discovered` updates |
| `glide.identification_engine.batch_update_last_discovered.use_execute_lazy` | `true` | Defer batched updates |
| `glide.identification_engine.granular_insert_locking` | `true` | Granular insert locks |
| `glide.identification_engine.platform_domain_separation_enabled` | `false` | Domain-separation mode |
| `glide.cache.size.service_cache` | `20` MB | IRE relation cache (LRU) |
| `glide.identification_engine.related_items_local_cache_count` | `15000` | Related/lookup cache (0 disables) |
| `glide.identification_engine.dependent_items_local_cache_count` | `10000` | Dependent CI cache |
| `glide.identification_engine.independent_items_local_cache_count` | `100000` | Independent CI cache |
| `glide.identification_logs.max_run_ids` | `1000` | Max runs in Identification Logs |
| `glide.cmdb.logger.source.identification_engine` | — | IRE log level (info/warn/error/debug/debugVerbose) |
| `glide.duplicate_ci_remediator.max.cis` | `1000` (≤5000) | Bound large remediation sets |
| `glide.duplicate_ci_remediator.dry_run` | `false` | Safe rehearsal |

### 7.3 Deletion strategies (pattern-related CIs)
Keep (default) / Delete / Mark as absent / Delete relations / Mark as retired. Exception: **network adapter and IP address are deleted** when marked absent (DSF).

### 7.4 File-Based Discovery (FBD)
- Plugin `com.snc.discovery.file_based_discovery`; default frequency **Monthly**; requires initial Content Data Service sync (~24 h) (DSF).
- Properties: `file_discovery.wildcard.windows` (additive), `file_discovery.blacklist.windows` (hard filter) (DSF).

---

## 8. Key tables

- **IRE:** `cmdb_identifier`, `cmdb_identifier_entry`, `cmdb_reconciliation_definition`, `cmdb_dynamic_reconciliation_definition`, `cmdb_ire_data_source_rule`, `cmdb_datasource_last_update`, `cmdb_datasource_staleness`, `cmdb_ire_partial_payloads` (+ `_index`), `cmdb_ire_incomplete_payloads`, `cmdb_duplicate_lookup_related_allowed_class`, `cmdb_dynamic_ire_skip_class`, `sys_object_source_info`, `sys_object_source`, `sys_properties`.
- **Discovery:** `discovery_schedule`, `discovery_device_history`, `discoverycredentials`, `ecc_queue`, `discovery_status`, `reconcile_duplicate_task`.
- **CMDB Health:** `cmdb_health_orphan_rule`, health staleness/staleness rules.
- **Default lookup tables:** `cmdb_serial_number`, `cmdb_ci_network_adapter`.
- **FBD:** `cmdb_file_information`, `samp_file_name`, `samp_custom_file_name`, `cmdb_sam_sw_install`, `cmdb_unidentified_file_set`, `cmdb_swid_tag`.

---

## 9. Conflict resolution log (duplicates validated & merged)

| ID | Discrepancy | Resolution (validated) |
|---|---|---|
| **C-B1** | **Order of operations** — WT1: 4 phases (Port Scanning→Classification→Identification→Exploration); WT5: 6 steps; WT2: 4 steps (Probe Execution→Data Collection→Data Parsing→CMDB Update); H: 6-step setup | **4 phases is canonical** (official `c_DiscoProcessFlows`; DSF/DV4/WT1 agree). The others are partial/alternative framings. |
| **C-B2** | **Correlation ID** — WT5: same Correlation ID = duplicate; WT4: same Correlation ID = **not** duplicate | **WT5 correct.** The shipped ESX Server Rule uses `correlation_id` as the identifier (INK), so identical Correlation IDs match the same CI → duplicate. WT4 (qwen3-30b) is a misreading. |
| **C-C1** | **500-CI limit** — A: `max_concurrent_invocations_per_schedule` default 3 = concurrency cap; E: "≤500 CIs per batch by default (this property)" | **A correct.** `max_concurrent_invocations_per_schedule` (default 3) is a concurrency cap. The **500-CI payload limit** is a separate best practice (`best-practices-id-reconcile.md`: "Limit the number of CIs per payload to 500"). E misattributes. |
| **C-C2** | **De-dup tasks "always created"?** — C/D/E: always created; G: only when `skip_duplicates=true` **and** ≥ threshold | **C/D/E correct.** Official `id-detect-dup-ci.md` line 26: "In either case, de-duplication tasks are always created." G's decision table is a simplification and is wrong on conditionality. |
| **C-C3** | **Threshold boundary** — C: "≤ threshold"; D/G: "< threshold" | **"< threshold" (strictly less than)** — official doc wording. C's "≤" is slightly off. |
| **C-C4** | **Reclassification flag names** — C: `updateWithoutUpgrade/Downgrade/Switch`; E: `updateWithoutUpgrade/Downgrade/Switch` (missing `updateWithout` prefix on two) | **C correct.** Payload flags are `updateWithoutUpgrade`, `updateWithoutDowngrade`, `updateWithoutSwitch` (matching `glide.identification_engine.update_without_*_enabled`). |
| **C-C5** | **Health tab label** — B names a "Health" tab; F's evidence didn't state it | **B correct.** `ci-class-manager-landing-page.md` confirms a CMDB Health section/tab. Evidence gap only. |
| **C-C6** | **Role granularity** — B: general (`sn_cmdb_editor`/`itil` read); F: per-task roles | **Both valid.** F is more granular; use F's per-task matrix. |
| **C-C7** | **`skip_duplicates` framing** — E: unconditional oldest-retention; C/D/G: threshold-conditioned | **C/D/G correct** (threshold-conditioned, per official doc). |
| **C-C8** | **IRE matching precedence** — C: source-key first; D: unverified | **C correct.** `skip_sys_object_source_matching` default `false` means `source_native_key` match is preferred (documented). |
| **C-A1** | **MID selection fallback** — DSF: Auto-Select falls back to default MID then Paused/Upgrading; DV4: cluster selection ignores default-MID settings | **Both valid** — different selection mechanisms (Auto-Select vs cluster selection). |
| **C-A2** | **IRE data source rule fields** — DSF includes `Active`; DV4 omits it | **DSF correct** (official doc has `Active`). |
| **C-A3** | **Shazzam batch minimum** — DSF: "minimum effective 256"; DV4: "UI converts below 256 to 0" | **Both true** (min effective 256; UI floors lower values to 0). |
| **C-A4** | **`skip_duplicates` spelling** — DV4 flags two documented spellings | Use the official `glide.identification_engine.skip_duplicates`. |
| **C-A5** | **Identification Simulation UI** — DSF: exists; DV4: UNVERIFIED | **DSF correct** (official `identification-simulation` doc exists). |

**Consensus facts (2+ agents agree):** CI Class Manager path & tabs; IRE as the single gateway; identification on insert+update, reconciliation update-only; reconciliation never blocks inserts; identifier entry types Regular/Lookup/Hybrid; prefer independent rules; static/dynamic reconciliation tables; child-overrides-parent; dynamic beats static; `skip_duplicates` default true / threshold 5; oldest duplicate becomes main CI + `duplicate_of`; `duplicate_of`/`discovery_source=Duplicate` skipped; MID selection methods; Auto-Select IPv6 limitation; Discovery/ALL app requirement; scan-type list; credential types; `cmdb_datasource_last_update`; `cmdb_duplicate_lookup_related_allowed_class`; child-class wizard order; suggested-relationship removal caveat.

---

## 10. Source map (all URLs cited across agents)

**Official docs (`docs.servicenow.com`):**
- Discovery: `c_GetStartedWithDiscovery`, `c_DiscoveryIdentifiers`, `t_ConfigureDiscovery`, `discovery-setup`, `t_CreateADiscoverySchedule`, `discovery-schedule-form`, `discovery-classifiers`, `create-discovery-ci-classification`, `disco-process-flow-patterns` / `c_DiscoProcessFlows`, `c_DiscoveryBehaviors`, `discovery-ip-address-configuration`, `r_CIIPAddressSelection`, `r_DiscoveryProperties`, `deletion-strategy`, `c_DiscoveryStatus`, `r_DiscoveryLog`, `r-discovery`, `c_DiscoveryConfiguration`, `c_DiscoveryConfigurationConsole`, `exclude-ip-ranges`, `r_AvailableSystemProperties`, `r_DiscoveryStatusDevices`, `discovery-properties`
- CMDB/IRE: `ire`, `c_CompsandProcessIDandReconcil`, `c_IdentificationRules`, `r_ReconciliationRulesPrinciples`, `best-practices-id-reconcile`, `ci-class-manager-landing-page`, `create-id-inclusion-rule`, `id-detect-dup-ci`, `de-duplication-tasks`, `properties-duplicate-ci`, `identification-simulation`, `c_CMDBIdentifyandReconcile`, `multisource-cmdb`, `c_CMDBHealth`, `create-ire-data-source-rule`, `create-datasource-staleness-rule`, `create-reconciliation-rule`, `create-reconciliation-rule-non-cmdb`, `create-non-cmdb-data-refresh-rule`, `t_CreateCMDBHealthStaleRule`, `r_CMDBHealthMetrics`, `t_ViewCIHealth`, `t_CreateCIIdentificationRule`, `create-dependent-relationship`, `c_ServiceRulesMetadata`, `ire-reference`, `properties-id-reconciliation`, `configuring-ire`, `dynamic-ire-exclude-class`, `domain-separation-identification-reconciliation`

**Knowledge base (`support.servicenow.com`):**
- KB1064718 (IRE fundamentals), KB2558192 (duplicate tasks vs retired CIs), KB3222102 (`sys_updated_on` refresh), KB0756709 (data precedence), KB0869861 (troubleshoot duplicate CIs), KB0755747 (retired CI rediscovery), KB0535236 (WMI firewall), KB0748325 / KB0748222 (Configuration Console), KB1380611 (trusted hostname), KB2184482 (AWS discovery), KB0726425, KB3037828, KB0750382/0383/0386 (IRE debug logs), KB1542272, KB0820379

**Community / other:**
- `community/itom-articles/servicenow-discovery-overview/ta-p/2321453`
- `community/itom-articles/understand-phases-of-discovery/ta-p/3116984`
- `community/cmdb-articles/cmdb-identification-reconciliation/ta-p/2301712`
- `community/cmdb-forum/a-deep-dive-into-ci-class-manager-and-ire-servicenow-cmdb/m-p/3486406`
- `community/cmdb-articles/understanding-ire-reconciliation-rules/ta-p/3289239`
- `community/cmdb-articles/cmdb-understanding-identification-and-reconciliation-rules-and/ta-p/3520826`
- `community/cmdb-forum/how-to-avoid-duplicate-ci-creation/m-p/3498456`
- `community/cmdb-forum/identification-and-reconciliation-rule/td-p/3142427`
- `community/cmdb-forum/deduplication-template-doesn-t-correctly-picking-up-the/td-p/3466047`
- `community/itom-forum/how-to-set-unique-key-for-a-ci-in-discovery/m-p/911760`
- `community/developer-forum/servicenow-discovery-creating-a-new-ci-even-though-an-existing/m-p/3590971`
- `community/itom-forum/deeper-understanding-of-the-discovery-processes/m-p/913596`
- `servicenowwithrunjay.com/cmdb-ci-class-manager/`, `servicenowguru.com/...ire/`

---

## 11. Notable gaps / caveats
- **WT3 (`llama3.1-8b`)** produced no usable content (empty reference).
- **Release drift:** sources span Australia / Brazil / Geneva / Xanadu / Washington DC; UI labels and some defaults differ by release. Prefer Brazil for current defaults.
- **`glide.discovery.use_cmdb_identifiers`** — present Geneva+; pre-Geneva upgrades must add it manually (`true`); Service Mapping always uses IRE identifiers (DV4, INK).
- **Identification Simulation** and several menu labels are release/UI dependent (DSF/DV4 disagreement noted).
- **`duplicate_of`** is a **field**, not a table (DV4).
- **CMDB Health duplicate metric** is narrow: only CIs with identification rules that have an empty discovery source or an active de-dup task (DV4).
