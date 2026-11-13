# ServiceNow Discovery — Configuration Reference

*Worktree `SNC_DISC__WT1` · agent `deepseek-v4.1-flash-fast__freebuff__buffy` ·
model `DeepSeek V4.1 Flash Fast` · provider Freebuff / Codebuff (Buffy runtime) · 2026-11-13*

Evidence-backed. Every non-obvious claim carries `[S<n>]`, resolved in §18. Claims I could not
source are marked **UNVERIFIED** and collected in §17. Nothing here is instance-tested — see §0.

---

## 0. Evidence policy and scope

- Sources are ServiceNow's own docs (`docs.servicenow.com`) and Now Support KB
  (`support.servicenow.com`). Community posts are used only to corroborate, never alone.
- ServiceNow docs are **release-labelled**. The pages used here span *Brazil*, *Zurich*, *Xanadu*,
  *Washington DC*. Where a statement is release-specific the label is quoted; where the behaviour is
  long-standing it is stated without a label.
- I have **no ServiceNow instance**, so every UI path is doc-sourced, not clicked. Menu labels drift
  between releases — treat §10 as "go here, the label may be singular/plural on your release".

## 1. Mental model (get this right and the rest follows)

Horizontal Discovery has **four runtime phases per device** — Scanning, Classification,
Identification, Exploration `[S7]`. The Identification phase is where Discovery calls the CMDB
**Identification and Reconciliation Engine (IRE)** `[S7][S10]`.

Three different rule sets are involved, and mixing them up is the most common reason people
misconfigure their way into duplicates:

| question | engine / rule set | where configured |
|---|---|---|
| "Is this the same CI I already have?" | **identification rules** (IRE) | CI Class Manager → class → Identifiers `[S2]` |
| "Which data source is allowed to change this attribute?" | **reconciliation rules** (static/dynamic, IRE) | CI Class Manager → class → Reconciliation Rules `[S3]` |
| "Has this source gone quiet, so a lower-priority source may take over?" | **data refresh rules** (IRE, static reconciliation only) | CI Class Manager → class → Reconciliation Rules → **Data Refresh Rules** `[S23]` |
| "May this source create a CI of this class at all?" | **IRE data source rules** | `Configuration → Identification/Reconciliation → IRE Data Source Rule` `[S24]` |
| "Is this device config actually a server?" | classification + patterns | Discovery Definition → classifiers/patterns `[S16]` |

Two consequences worth stating plainly:

1. **Reconciliation never blocks an insert.** "When a CI is created through the IRE, the system
   creates the CI regardless of reconciliation rules because it is a new record." `[S9]`
   So a missing attribute after Discovery is a *reconciliation* problem, while an extra CI is an
   *identification* (or inclusion/ACL) problem.
2. **IRE only runs for the CI scan type.** "This identification step only takes place for the
   Configuration item type of discovery, not for the other types of discovery." `[S1]`
   An `IP addresses` scan creates device history and never writes CIs, so it can never be the cause
   of a duplicate CI `[S4]`.

## 2. Data model you will actually touch

| table | holds | source |
|---|---|---|
| `cmdb_identifier` | identifier (identification) rules, one per class | `[S1]` |
| `cmdb_identifier_entry` | the attribute sets ("identifier entries") and their priorities | `[S1]` |
| `cmdb_reconciliation_definition` | **static** reconciliation rules | `[S3]` |
| `cmdb_dynamic_reconciliation_definition` | **dynamic** reconciliation rules (needs CMDB 360) | `[S3]` |
| `cmdb_datasource_last_update` | Data Source History — which source last wrote which attribute | `[S9]` |
| `cmdb_ci*` (`cmdb_ci_server`, `cmdb_ci_linux_server`, …) | the CIs themselves | `[S1]` |
| `cmdb_ci_network_adapter`, `cmdb_serial_number` | lookup tables the default Hardware rule searches on | `[S1]` |
| `discovery_schedule` | schedules; also where you add the hidden **Max Idle time** column | `[S4]` |
| `discovery_device_history` | per-device phase/state record behind Discovery Status | `[S6]` |
| `discoverycredentials` (Discovery → Credentials) | credentials the MID Server uses | `[S22]` |
| `sys_properties` | the `glide.*` switches in §9 | `[S12]` |
| `reconcile_duplicate_task` | de-duplication tasks | `[S11][S18]` |
| `cmdb_health_orphan_rule` | orphan rules feeding the correctness KPI | `[S15]` |

`duplicate_of` is a field, not a table: it links a duplicate CI to its **main CI** `[S11]`.

## 3. Configuration surface, grouped by *where you set it*

- **A. Platform prerequisites** — Discovery plugin; `discovery_admin` (or `admin`) role for
  configuring/running; a MID Server user with the `mid_server` role; Basic Authentication available
  if you use user/password MID auth `[S5]`.
- **B. Host + network** — MID Server host(s) meeting system requirements, assigned the **Discovery
  application (or ALL)**. Starting with Istanbul this assignment is mandatory `[S5]`. Firewall must
  allow outbound to the instance; port 443 (SSL) and proxy issues are the classic failure `[S5]`.
- **C. Credentials** — Windows (service account with ≥ local admin), SSH (Linux/UNIX), SNMP v1/v2c/v3
  (network gear). Stored in `discoverycredentials`, decrypted on the MID Server with its private
  key `[S22]`.
- **D. Scan scope** — IP address lists / ranges / CIDR networks, reusable **range sets**, per-range
  **excludes**, and a global exclusion list `[S17]`.
- **E. Schedule** — the control point that decides *when*, *what type*, *which MID Server*, and
  *how much* (§5) `[S4]`.
- **F. Classification / patterns** — classifiers choose the CI class; patterns/probes gather
  identity + exploration data and feed IRE `[S16][S7]`. *(Pattern authoring: out of scope, §17.)*
- **G. CMDB rules** — identification, reconciliation, data source rules, dependent (hosting /
  containment) relationships `[S2][S3][S14]`.
- **H. Properties** — `Discovery Definition → Properties` and `sys_properties` (§9) `[S12]`.
- **I. Health + remediation** — CMDB Health KPIs, duplicate metric, de-duplication dashboard and
  templates (§14–§15) `[S15][S11]`.

## 4. Order of operations

### 4A. Setup order (blank instance → trustworthy CMDB writes)

1. **Roles**: grant `discovery_admin` to the humans who configure/run Discovery `[S5]`.
2. **Design the scope**: which IP ranges, which credential per range, who owns the CMDB classes.
   Decide this *before* installing, because ranges + credentials determine MID placement `[S5]`.
3. **Install the MID Server** on a host that can reach those ranges; assign it the Discovery
   application (or ALL) `[S5]`.
4. **Verify the MID Server**: `Discovery → MID Servers`; status must be *Up* and validated; check
   the MID log if not `[S5]`.
5. **Create credentials** (`Discovery → Credentials`), then **test them**. Bad credentials are "a
   leading cause of failed discoveries" `[S5]`. Set **credential order** and **affinity** so a
   credential is not sprayed at every device `[S22]`.
6. **Create ranges / range sets and exclusions** — including the global exclusion list for
   (management subnets, iLO/DRAC, OT, anything you must not touch) `[S17]`.
7. **(For identification quality) fix the rules before the first big scan**: review identifier rules
   for each class you will write, and dependent relationship rules if you will discover dependent
   CIs (VMs, app servers) `[S2][S14]`.
8. **Create the schedule** (§5): Discover = *Configuration items*, MID selection method, run window,
   `Max run time`, `Shazzam batch size` `[S4]`.
9. **Run a narrow pilot first** (one range, one credential), then read **Discovery Status** per device
   (§15) `[S6]`. Only then widen to production ranges.
10. **Then** tune reconciliation and data source rules — deliberately last, because you cannot judge
    "which source should own `name`" until you have seen what each source actually writes `[S3][S9]`.

> Why this order: every step's output is the next step's input. Credentials before schedule, ranges
> before schedule, MID validated before schedule, and *rules* before scale. Doing CMDB rules first
> means tuning blind.

### 4B. Runtime order (what happens per device, and the state you will see)

| # | phase | what runs | Discovery Status device state you may see |
|---|---|---|---|
| 1 | Scanning | **Shazzam** probe (port scan) then protocol port probes; results return via ECC queue `[S7]` | `Alive, not active, not classified` (responding, no scannable open port); `Active` (open WMI/SSH/SNMP port) `[S6]` |
| 2 | Classification | one **classify probe per device**; determines the CI class (e.g. Windows vs Linux vs switch); **first phase that uses credentials** `[S16]` | `Classified`; `Active, couldn't classify` (often with a reason) `[S6]` |
| 3 | Identification | identity probe/pattern collects serial, name, IP, MAC → **identifier rules** decide update vs create → **IRE writes the CMDB** `[S1][S7]` | `Identified CI` (existing match), new CI, `Identified, ignored extra IP` (same device already seen under another IP in this run) `[S6]` |
| 4 | Exploration | exploration probes/patterns from the classifier's *Triggers Probes* enrich the CI `[S7]` | `Updated CI` (existing CI enriched) `[S6]` |

Failure signatures to recognise: `Active, couldn't classify` = credential/protocol/port problem at
step 2 `[S16]`; a device that classifies but never reaches `Identified CI` = identity probe or IRE
problem at step 3 `[S1][S8]`.

## 5. Discovery Schedule form — the fields that change behaviour

`Discovery → Discovery Schedules → New` (or `Workspaces → Discovery Admin Workspace → Schedules`)
`[S4][S21]`.

| field | options | why it matters |
|---|---|---|
| **Discover** | Configuration items / IP addresses / Networks / Service / Serverless / Cloud application / Cloud resources / Certificates | **Only "Configuration items" runs identification and writes CIs** `[S1][S4]`. IP-address scans create device history only `[S4]`. |
| **MID Server selection method** | Auto-Select / Specific MID Cluster / Specific MID Server / **Use Behavior** | Auto-select needs the MID to have the Discovery (or ALL) app *and* a matching IP range; **auto-select is not supported for IPv6** `[S4]`. Selecting a specific MID auto-adds the Discovery app `[S4]`. |
| **Behavior** | preconfigured behavior | Use when one schedule needs multiple Windows credentials, multiple protocols across MIDs, large-scale load balancing, or multiple domains `[S4]`. |
| **Location** | location | Assigns location to discovered CIs; empty = no location `[S4]`. |
| **Max run time** | duration | Hard stop: remaining tasks cancel even if the scan is incomplete `[S4]`. |
| **Max Idle time** | duration | Cancels *stalled* runs (no ECC movement). **Hidden by default** — add the column to the `discovery_schedule` table to use it `[S4]`. |
| **Log state changes** | bool | Per-state log entries (Active → Classifying …), visible in the Devices related list `[S4]`. |
| **Shazzam batch size** | int, default **1000** | Splits IPs into sequential batches so classification starts earlier. UI policy enforces a **minimum of 256** and converts anything lower to **0** `[S4]`. |
| **Shazzam cluster support** | bool | Distributes Shazzam batches across cluster MIDs; works together with batch size `[S4]`. |
| **Use SNMP Version** | **ALL** (default) / v1 / v2c / v3 | Pin it if your gear mishandles v3 probing `[S4]`. |
| **Active** | bool | Inactive schedules can still be run manually `[S4]`. |
| **Discovery Agent** | MID / AWS MID | Only appears when `glide.discovery.enable_ssm` is on and Discover = Configuration items following a Cloud Resources schedule `[S4]`. |

Related lists: **IP Ranges**, **Discovery Range Sets**, **Discovery Status**, **Global IP Exclusion**,
**Discovery Attributes** (per-schedule/range CI field values, e.g. location) `[S4]`.

## 6. IP ranges, range sets and exclusions

- Methods, combinable: IP **address list** (individual IPs/hostnames), IP **range**, IP **network**
  in CIDR `[S17]`.
- **CIDR networks auto-exclude network and broadcast addresses**, avoiding junk results `[S17]`.
- **IPv6 is not supported for range or network definitions** `[S17]` — while an IPv6 address-list
  scan *is* available for Configuration-item schedules `[S4]`. That asymmetry surprises people.
- Excludes are per range-set: type `IP Address List`, `IP Address Range`, or `IP Network` `[S17]`.
- **>500,000 excluded addresses cancels the discovery** and logs an error `[S17]` — on huge estates,
  express scope as a small include set rather than "everything minus a lot".
- Global exclusions apply across **all** schedules (CI, IP, network scans) `[S4][S17]`.
- Quick ranges accept network/range/list in one comma-delimited string, for pilot runs `[S4]`.

## 7. MID Server selection and scaling

- Selection sequence differs per phase: the **port scan (Shazzam)** is spread across batch size ×
  MIDs, while cluster selection prefers the **lowest `Order` value that is `Up`**, falling back to
  `Paused`/`Upgrading` when nothing is Up `[S4]`.
- Cluster selection **ignores default MID Server settings** `[S4]`.
- A MID can belong to **one** cluster only (not one load-balancing + one failover) `[S4]`.
- Install **at least two** MIDs and split schedules/ranges between them; it is the fastest
  throughput win available `[S5]`.
- Behaviour is the escape hatch when a single schedule needs *different* MIDs for different
  credentials/protocols/domains `[S4]`.

## 8. Credentials

- Stored in `discoverycredentials`; the MID decrypts with its own private key `[S22]`.
- Default Windows path: the MID Server **service** account is used to reach Windows devices — give it
  at least local administrator rights on targets `[S22]`.
- Linux/UNIX and network devices use the SSH/SNMP credentials defined in `Discovery → Credentials` `[S22]`.
- **Order** matters (which credential is tried first) and **affinity** prevents a credential being
  applied to unrelated devices. Credential **aliases** filter which credentials a schedule may use `[S22]`.
- Test before scheduling; every troubleshooting guide starts with bad credentials `[S5]`.

## 9. Properties that change Discovery / IRE behaviour

Set at **Discovery Definition → Properties**, or in **`sys_properties`** `[S12]`.

| property | default | effect | source |
|---|---|---|---|
| `glide.identification_engine.skip_duplicates` | — | Controls how Discovery handles duplicate CIs found during identification | `[S1]` |
| `glide.identification_engine.skip_duplicates.threshold` | — | Threshold used with the skip-duplicates logic | `[S1]` |
| `glide.discovery.use_cmdb_identifiers` | `true` on Geneva+ | Use CMDB IRE identifiers instead of legacy identifiers; pre-Geneva upgrades may need it added manually. **Service Mapping always uses IRE identifiers regardless** | `[S1][S20]` |
| `glide.discovery.multi_page_serial_mode` | `false` | `true` processes multi-page pattern payloads **serially**; the documented fix for duplicates created from multi-page payloads | `[S8][S12]` |
| `glide.reconciliation.override.null` | — | Whether a lower-priority source may write into an **empty** field | `[S9]` |
| `glide.discovery.log_debug_info` | `false` | Adds debug info to the Discovery log from ECC input | `[S12]` |
| `glide.discovery.log_message_chars` | `200` | Log preview length | `[S12]` |
| `glide.discovery.application_mapping` | `true` | Enables ADM | `[S12]` |
| `glide.discovery.sam_batch_update_size` | `100` | Batches `cmdb_sam_sw_install` updates where only `last_scanned` changed | `[S12]` |
| `glide.discovery.enable.software_filter` | `true` | Windows software filtering | `[S12]` |
| `glide.discovery.L3_mapping` | — | Map servers/gear to routers and L3 switches | `[S12]` |
| `glide.discovery.roundingInterval.cpu` | — | CPU speed rounding | `[S12]` |
| `glide.discovery.retire_stale_accounts` | — | Removes stale service-account references in Discovery Config | `[S12]` |
| `glide.discovery.enable_ssm` | — | Gates the AWS-SSM (Agent) option on schedules | `[S4]` |

> **Documented naming inconsistency — do not silently "fix" it.** ServiceNow's own pages render this
> family two ways: `glide.identification_engine.skip_duplicates` `[S1]` and
> `glide.identificationengine.skipduplicates` `[S12]`. Check `sys_properties` on your instance before
> setting either; do not assume which spelling your release ships.

## 10. CI Class Manager — the bread crumbs

Everything CMDB-write-related lives behind one entry point: **All → Configuration → CI Class Manager**
`[S2][S13]`. Inside, pick a class in **Hierarchy**, then use the class navigation bar `[S13]`.

| path | what lives there | why it matters for Discovery |
|---|---|---|
| `CI Class Manager → Hierarchy → <class>` | the class tree (`cmdb_ci_linux_server`, …) | the class you pick is the scope of every rule below `[S13]` |
| `… → Class Info → Basic Info` | display name, **table name**, description, icon | confirms the real table (`cmdb_ci_*`) you will query `[S13]` |
| `… → Dependent Relationships` | hosting/containment rules | **Required before an identification rule can be `Dependent`**; also drives dependent CI identification for VMs/apps `[S14][S2]` |
| `… → Identifiers` (Identification) | the class's single identification rule: identifier entries, related entries, priorities | the insert-vs-match decision (§11) `[S2]` |
| `… → Class Info → Reconciliation Rules` | static reconciliation rules per discovery source / attribute | which source may update an attribute (§12) `[S3]` |
| `… → Class Info → Reconciliation Rules → Data Refresh Rules` | per-source **Effective Duration** staleness rules | lets a lower-priority source take over when the priority source stops reporting (§12B) `[S23]` |
| `Configuration → Identification/Reconciliation → IRE Data Source Rule` | `cmdb_ire_data_source_rule` records (**not** inside CI Class Manager) | block a source from *inserting* a class while still allowing updates (§12A) `[S24]` |
| `… → Health` | CMDB Health properties, scorecards, rules **at class level**; orphan scorecard | tune completeness/correctness for this class `[S13][S15]` |
| `CMDB Health dashboard` | aggregated **completeness / correctness / compliance** KPIs | the duplicate metric that tells you if you are losing `[S15]` |
| `CMDB Workspace → De-duplication dashboard` | duplicate sets, **de-duplication templates** for bulk fixes | remediation at scale `[S11]` |
| `De-duplication tasks` list | `reconcile_duplicate_task` records | per-duplicate work queue `[S11][S18]` |
| `Duplicate CI Remediator` (legacy Core UI wizard) | guided single-task remediation: pick **main CI**, merge attributes/relationships/related items | manual fix path `[S11]` |

Notes:

- **Metadata Editor and CI Class Manager are synchronised** for dependent rules — editing in one shows
  in the other `[S14]`.
- The CI Health widget can say *"not applicable"*: duplicate scoring needs identification rules on
  the class or an ancestor, and orphan scoring needs orphan rules and health inclusion rules `[S15]`.
- **UNVERIFIED**: whether your release exposes an identifier *simulation* action from the class form.
  Look for it — it is the cheapest way to test a rule change without waiting for a scan — but I could
  not confirm it from an instance (§17).

## 11. Identification rules (the insert-vs-match decision)

**Shape.** "An identification rule applies to a CI class and consists of a single CI identifier and
one or more identifier entries and related entries, each with a different priority." `[S2]`
Each class is associated with a **single** identification rule `[S20]`.

**Entry types** `[S2]`:

- **Regular** — the CI's own attributes.
- **Lookup** — attributes on a related table that references `cmdb_ci` (e.g. `cmdb_serial_number`,
  `cmdb_ci_network_adapter`).
- **Hybrid** — both, for cases where a lookup alone is not unique (two cloud VMs sharing serials).

**Related entries** create/update records on other tables; they are **not** used to identify the CI `[S2]`.

**Inheritance trap.** A child class **derives** the parent's rule — including its related entries —
unless you create a rule at the child. Creating one **replaces the derived rule entirely**, so you
must re-add any related entries you still need `[S2]`.

**Default Discovery identifiers** (base system) `[S1]`:

| rule | class | identifies on |
|---|---|---|
| Hardware Rule | `cmdb_ci_hardware` | `serial_number`, `serial_number_type`, `name`, `ip_address`, `mac_address` + lookup on `cmdb_serial_number` and `cmdb_ci_network_adapter` |
| ESX Server Rule | `cmdb_ci_esx_server` | `correlation_id` |
| Storage Server Rule | `cmdb_ci_storage_server` | `cim_object_path`, `name`, serial fields, `mac_address`, `ip_address` + lookups |
| WBEM Service Rule | `cmdb_ci_wbem_service` | `cim_object_path` |

**Operational rules** `[S1]`:

- Custom identifiers must use **different `Order` values** from the defaults; Discovery parses low →
  high. Disable a rule with its `Active` checkbox rather than guessing order.
- `sys_class_name` **cannot** be an identification attribute of an independent rule — to identify by
  class, create one rule per class and name the class in *Applies to* `[S1]`.
- Bonded/teamed NICs share IP and MAC; adding `name` distinguishes interfaces — but **renaming an
  adapter breaks matching**: Discovery marks the old CI `Install Status = Absent` and creates a new
  one `[S1]`.
- **Serial numbers are integrity-critical.** If you customised probes/sensors/patterns, verify they
  still return serials and never reformat them (no custom prefixes) — non-standard serials break
  asset tracking *and* matching `[S1]`.
- Prefer **`Enforce exact count match`** on lookup entries for stronger rules `[S2]`.
- **Never** define a lookup-based identifier for a child table in a parent's rule *and* a class-level
  identifier for that child — the two contradict and produce duplicates in the child table `[S2]`.

## 12. Reconciliation rules (which source wins an update)

**Static** rules (`cmdb_reconciliation_definition`) name the discovery sources authorised to update
class attributes and their precedence `[S3]`. **Dynamic** rules
(`cmdb_dynamic_reconciliation_definition`) decide by **attribute value** using CMDB 360 — the largest
or most-reported value wins — and require CMDB 360 to be enabled; only one dynamic rule per attribute `[S3]`.

Precedence, in the order that actually bites `[S3][S19]`:

1. **Dynamic beats static** for the same attribute `[S3]`.
2. **A rule that lists specific attributes beats a rule with an empty Attributes field ("all
   attributes") — regardless of discovery-source priority.** This is the counter-intuitive one: a
   *lower-priority* source with an explicit attribute list can block a higher-priority source `[S19]`.
3. **Child-class rules beat parent-class rules** (including derived rules) `[S3]`.
4. Between two rules for the same attribute at the same class level, **priority** decides `[S3]`.
5. Rules authorising *different* sources for the same attribute **coexist**; IRE then prevents them
   from overwriting each other using Data Source History `[S3][S9]`.
6. Empty-field updates are governed by `glide.reconciliation.override.null` `[S9]`.
7. **Insert is not gated by reconciliation** `[S9]`; use **data source rules** to stop a source
   creating CIs of a class at all `[S3]`.
8. With Domain Separation, rules are domain-scoped; parent-domain rules apply to child domains unless
   overridden `[S3]`.

Practical guidance that follows from #2: **always list attributes explicitly** rather than leaving
Attributes empty, so a rule does what you meant when someone later adds a specific-attribute rule at
the same class or a child class `[S19]`.

### 12A. IRE data source rules — "you may update, but you may not create"

Separate module from reconciliation, and easy to miss because it is **not** inside CI Class Manager:
`All → Configuration → Identification/Reconciliation → IRE Data Source Rule` `[S24]`.

- Purpose: "prevent a specific discovery (data) source from inserting new CIs for a specific class"
  while still permitting it to update existing CIs `[S24]`.
- Stored in `cmdb_ire_data_source_rule`; **child classes derive these rules from parent classes**, the
  same way identification rules are derived `[S24]`.
- Fields: **Applies to** (the class and its children), **Data source**, **Insert Not Allowed** `[S24]`.
- **Only one rule can be active for any class/discovery-source pair** `[S24]`.
- Does **not** apply to lookup items or related items `[S24]`.
- Blocked inserts fail loudly: `INSERT_NOT_ALLOWED_FOR_SOURCE` — "Insert into [x] is blocked for data
  source [abc] by IRE data source rule" `[S26]`.
- Canonical use case from the docs: an IP-scan tool that sees network gear but not servers, so it
  "creates server CIs without details" — let it update, forbid it to create `[S24]`.

Note the asymmetry that makes this rule family worth knowing: identification decides *match or new*,
reconciliation decides *whose value wins*, and data source rules decide *whether the new record is
allowed to exist at all*. That last one is the only IRE rule that can stop a duplicate being born
when identification legitimately finds no match.

### 12B. Data Refresh Rules — staleness per discovery source

"Specify data refresh rules to determine if a CI is stale for a specific discovery source. Such CIs
can then be updated by a lower-priority authorized discovery source." `[S23]`

- **Where:** `All → Configuration → CI Class Manager → Hierarchy → <class> → Class Info →
  Reconciliation Rules → Data Refresh Rules → Add` `[S23]`. It sits on the reconciliation tab, not in
  a separate module `[S23]`.
- **Fields:** `Discovery source` (whose silence is being measured) and `Effective Duration` (the
  staleness window). If the attributes named in the static reconciliation rule were not updated by
  that source inside the window, the CI is stale **for that source** `[S23]`.
- **What it unlocks:** a lower-priority authorised source may then update the CI. Concretely, updates
  from a lower-priority source are normally rejected *unless* it is the first source to write the
  record, **or the record became stale under the data refresh rule** `[S25]`.
- **Interaction with reconciliation:** data refresh rules "are used in conjunction with static
  reconciliation rules"; the precedence order of reconciliation rules does not change because a data
  refresh rule exists `[S23]`.
- **Critically: they do nothing when a dynamic reconciliation rule is in effect.** "Data refresh rules
  have no impact when dynamic reconciliation rules are in effect" `[S23][S10]`. So on a CMDB 360 /
  Multisource deployment, do not expect data refresh rules to rescue you.
- **Non-CMDB tables:** the same concept is configured in the `Data Source Staleness Definitions` table
  (`cmdb_datasource_staleness.list`) with `Applies to`, `Data source`, `Effective Duration` `[S27]`.
- **Staleness is evaluated against Data Source History**, not just `sys_updated_on`; IRE considers
  `cmdb_datasource_last_update` together with the class's data refresh rules when deciding whether an
  attribute is stale `[S25][S9]`.

#### Three different "stale" mechanisms — do not mix them up

| mechanism | question it answers | where | effect |
|---|---|---|---|
| **Data refresh rule** | has *this discovery source* stopped refreshing this CI? | CI Class Manager → Reconciliation Rules → Data Refresh Rules `[S23]` | allows lower-priority sources to update (static reconciliation only) |
| **CMDB Health staleness rule** | what % of this class is stale (for the correctness KPI)? | CI Class Manager → Health → Correctness → Staleness Rule `[S28]` | **reporting only** — feeds the correctness KPI, changes no data |
| **CMDB Data Manager policy** | should this CI be retired / archived / deleted? | CMDB Workspace → Data Manager `[S17]` scope note | lifecycle action on the CI (out of scope here, §17) |

The health staleness rule's Effective Duration is based on `sys_updated_on`, and "the Discovery
setting of certain types of CIs as stale takes precedence over a CMDB Health staleness rule" `[S28]` —
so a CI can look stale in health reporting while Discovery is actually refreshing it (data unchanged
means no write, so `sys_updated_on` does not move) `[S28]`.

## 13. Duplicate prevention playbook + insert-vs-update decision table

### 13.1 Why duplicates happen (cause → control → where)

| # | cause | control | where |
|---|---|---|---|
| 1 | Contradicting identification rules (parent lookup entry + child class identifier for the same table) | pick **one** identification strategy per table | CI Class Manager → Identifiers `[S2]` |
| 2 | **Inclusion rule scoped by class** on a parent class — child classes not named are not found by IRE | never filter inclusion rules by class; filter on attributes/status instead | IRE / CI Class Manager `[S2][S8]` |
| 3 | ACLs or **query business rules** hiding the existing CI from IRE | make IRE's read path unobstructed; test with a user with no ACL surprises | platform rules `[S8]` |
| 4 | Existing CI already has `duplicate_of` set, or `discovery_source = Duplicate` — IRE then refuses to identify it | remediate the duplicate set (§14) before re-scanning | de-dup `[S8]` |
| 5 | Same CI discovered **concurrently** by two discoveries, or the same dependent CI inside multiple payloads of one discovery | sequence overlapping schedules; de-duplicate dependent CIs in the pattern before returning | scheduling + patterns `[S8]` |
| 6 | Multi-page payloads processed in **parallel** | `glide.discovery.multi_page_serial_mode = true` | `sys_properties` `[S8][S12]` |
| 7 | Identifying attributes come back **empty/null** (no serial, no MAC; bonded NICs; renamed adapters) | keep serials intact; require non-null identifiers; use `name` only knowingly | patterns + Identifiers `[S1]` |
| 8 | Pattern/sensor **rewrites the serial** (prefix, truncation) | remove the transformation | patterns `[S1]` |
| 9 | **Manually created CIs** with an empty discovery source that never gets reconciled | populate or retire manual CIs; let CMDB Health flag them | CMDB Health / de-dup `[S18]` |
| 10 | Custom identifier never runs (same `Order` as a default, or `Active` cleared) | give it a unique Order; confirm Active | Identifiers `[S1]` |
| 11 | Reconciliation blocks the update, so a human "fixes" it by creating a manual CI | tune reconciliation (§12) instead of hand-creating CIs | Reconciliation `[S3][S9]` |
| 12 | A high-priority source went silent. Its old values keep winning, the CMDB freezes, and someone imports/manual-enters the "real" data → a second CI | add a **data refresh rule** so lower-priority sources may take over after Effective Duration | Reconciliation Rules → Data Refresh Rules `[S23][S25]` |
| 13 | An untrusted source (e.g. an IP-scan tool) creates detail-less CIs of a class it cannot really discover | **IRE data source rule** with *Insert Not Allowed* for that class/source pair | IRE Data Source Rule `[S24]` |

### 13.2 Insert vs update — who decides what

| situation | outcome | decided by |
|---|---|---|
| exactly one CI matches the identifier entries | **update** that CI, attribute by attribute | reconciliation rules `[S3]` |
| match exists, but the owning source has been silent past Effective Duration | a lower-priority authorised source may now write | **data refresh rule** + static reconciliation `[S23][S25]` |
| one match but the source is not authorised for an attribute | field is **skipped** (no error) | reconciliation + Data Source History `[S9]` |
| one match, field currently empty, lower-priority source | depends on `glide.reconciliation.override.null` | property `[S9]` |
| **multiple** CIs match | skip-duplicates logic picks one; extra matches become duplicates/tasks | `glide.identification_engine.skip_duplicates` + `.threshold` `[S1][S8]` |
| **no** match | **insert** — reconciliation is not consulted | IRE `[S9]` |
| no match but an **IRE data source rule** forbids insert for that class | no CI created; `INSERT_NOT_ALLOWED_FOR_SOURCE` | IRE data source rule `[S24][S26]` |
| identification cannot run (ACL/inclusion/`duplicate_of`) | **insert → duplicate** | `[S8]` |
| device seen under a second IP in the same run | no second CI; `Identified, ignored extra IP` | Discovery `[S6]` |
| scan type is *IP addresses* | no CI at all | schedule type `[S1][S4]` |

Rule of thumb: **identification answers "new or existing"; reconciliation answers "whose value
wins"**. If you find yourself editing reconciliation to stop duplicates, you are on the wrong screen.

## 14. Remediating duplicates you already have

- A duplicate set = one **main CI** + N CIs whose `duplicate_of` references it. The main CI's
  `duplicate_of` is empty `[S11]`.
- Remediate one at a time with **Duplicate CI Remediator** (pick main CI, choose attributes,
  relationships, related items to merge) or in bulk with **de-duplication templates** in CMDB
  Workspace `[S11]`.
- Options are effectively: **retain duplicates but retire/flag them** (`operational_status = Retired`,
  `duplicate_of` auto-set) or **delete them**; relationships and related items are merged into the
  main CI first `[S11]`.
- **Do not set `duplicate_of` by hand.** The system enforces constraints (main CI cannot itself be a
  duplicate; if a main CI becomes a duplicate, its duplicates re-point to the new main; a duplicate of
  `Unknown` blocks the operation) `[S11]`.
- Roles: `itil` to read, `itil_admin` or `cmdb_dedup_admin` to write `[S11]`.
- After remediation, make sure **inclusion rules / skip-duplicates** are configured so the same pair
  is not re-created on the next scan `[S11][S8]`.

## 15. Verification: how you know it worked

**Discovery Status** (`Discovery → Status`): per-device `Completed activity` / `Current activity`,
plus `Completed` sensor counts and `Scan status` (e.g. `Scan 17 of 19`). Universal probes (Shazzam,
Ping) are excluded from those counts `[S6]`.

**Per-device states** `[S6]`: `Alive, not active, not classified` → `Active` → `Classified` /
`Active, couldn't classify` → `Identified CI` / `Identified, ignored extra IP` → `Updated CI`.

**Timeline**: `Show Discovery Timeline` renders every probe/sensor/pattern with queueing vs
processing time and ECC queue records — the fastest way to see *where* a device stalled `[S15]`.

**Debug**: `glide.discovery.log_debug_info = true` adds ECC-derived debug to the Discovery log `[S12]`.

**CMDB Health**: three KPIs — **correctness**, **completeness**, **compliance** `[S15]`.
The **duplicate metric** is narrower than people expect: it only evaluates CIs that have
identification rules and that either have an **empty discovery source** or have an **active
de-duplication task** `[S18]`. Two CIs with identical name+serial and both `discovery_source =
ServiceNow` are **not** reported unless a de-dup task exists `[S18]`. Orphan and staleness metrics feed
correctness `[S15]`.

Copy-paste checks:

1. `Discovery → Status` → open the run → confirm devices reach `Identified CI`, not
   `Active, couldn't classify` `[S6]`.
2. `CMDB → cmdb_ci_<class>` list → filter `duplicate_of is not empty` for the class you just scanned.
3. CI Class Manager → class → Identifiers: confirm exactly one rule, and that its entries match the
   attributes your pattern actually returns `[S2]`.
4. CI form → CI Health widget: if duplicate score says *not applicable*, you have no identification
   rule at that class or its ancestors `[S15]`.

## 16. Anti-patterns

1. Tuning **reconciliation** to stop duplicates (wrong engine) `[S3][S9]`.
2. Scoping an **inclusion rule by class** `[S2][S8]`.
3. Two identification strategies for one table (class identifier + parent lookup) `[S2]`.
4. Custom identifiers sharing `Order` values with base rules `[S1]`.
5. Rewriting serial numbers in patterns for "cleanliness" `[S1]`.
6. Running overlapping schedules over the same ranges "for speed" `[S8]`.
7. Leaving `glide.discovery.multi_page_serial_mode = false` on pattern-heavy estates `[S8]`.
8. Editing `duplicate_of` by hand instead of using Remediator `[S11]`.
9. Treating CMDB Health duplicate = 0 as proof there are no duplicates (see the metric's narrow
   conditions) `[S18]`.
10. Discovering with an account that lacks local admin on Windows targets, then blaming
    classification `[S22][S5]`.

## 17. Open questions / UNVERIFIED

1. **Identifier simulation UI** — whether your release exposes a simulate action from the class form.
   Not confirmed without an instance.
2. **Exact property spelling** for skip-duplicates (`glide.identification_engine.skip_duplicates` vs
   `glide.identificationengine.skipduplicates`). Both appear in ServiceNow's own material `[S1][S12]`.
   Check `sys_properties`.
3. **Max-range-size property name** for the Shazzam probe — referenced as "the maximum range size
   property for the Shazzam probe" `[S4]`; I did not capture its literal name.
4. **Menu label drift** — "Identifiers" vs "Identification"; "Dependent Relationships" vs "Dependent
   Relationship". Labels differ across the release-labelled pages I read `[S13][S14]`.
5. **Pattern authoring** — deliberately out of scope (clarification C2); proposes `SNC_DISC__WT2`.
6. **CMDB 360 enablement/licensing** specifics for dynamic reconciliation — stated only as "must be
   enabled" `[S3]`.
7. **Reported-but-unconfirmed** claim I removed rather than ship: that Discovery always writes
   `last_discovered`/`first_discovered` on update. IRE documentation references `last_discovered` as
   "the timestamp of when the CI was last discovered" `[S26]`, but I did not capture whether it is
   written on every update or only on change — do not design data refresh windows around it unverified.
8. **CMDB Data Manager lifecycle policies** (retire/archive/delete, attestation) are a separate
   mechanism from data refresh rules. Only named here so nobody confuses them; not covered in depth.

## 18. Source ledger

| id | source | release label |
|---|---|---|
| S1 | Discovery identifiers — `https://www.servicenow.com/docs/r/it-operations-management/discovery/c_DiscoveryIdentifiers.html` | Brazil (updated 2026-09-10) |
| S2 | Identification rules — `…/configuration-management-database-cmdb/c_IdentificationRules.html` | Brazil (2026-09-10) |
| S3 | Reconciliation rules — `…/configuration-management-database-cmdb/r_ReconciliationRulesPrinciples.html` | Brazil (2026-09-10) |
| S4 | Discovery Schedule form reference — `…/discovery/discovery-schedule-form.html` | Brazil (2026-11-05) |
| S5 | Set up Discovery without Guided Setup — `…/discovery/t_ConfigureDiscovery.html` | Brazil/Zurich (2026-09-10 / 2025-09-30) |
| S6 | Discovery device history — `…/discovery/r_DiscoveryStatusDevices.html` | Brazil (2026-09-10) |
| S7 | Horizontal discovery process flow with probes and sensors — `…/discovery/c_DiscoProcessFlows.html` | Brazil (2026-09-10) |
| S8 | KB0869861 — How to troubleshoot duplicate CMDB CI records — `https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB0869861` | KB (2021, updated) |
| S9 | KB0756709 — How CMDB reconciliation and data precedence rules work — `…KB0756709` | KB (updated 2026-08-25) |
| S10 | KB1064718 — CMDB IRE fundamentals — `…KB1064718` | KB (2022) |
| S11 | Duplicate CIs remediation — `…/configuration-management-database-cmdb/de-duplication-tasks.html` | Brazil (2026-09-10) |
| S12 | Discovery properties — `…/discovery/r_DiscoveryProperties.html` + Available system properties — `…/platform-administration/r_AvailableSystemProperties.html` | Brazil/Zurich |
| S13 | View and edit class definitions and metadata — `…/configuration-management-database-cmdb/t_ViewTableDefinitions.html` | Brazil (2026-09-10) |
| S14 | Create dependent relationship rules — `…/create-dependent-relationship.html`; CMDB dependent relationship rules — `…/c_ServiceRulesMetadata.html` | Brazil |
| S15 | CMDB Health KPIs and metrics — `…/configuration-management-database-cmdb/r_CMDBHealthMetrics.html`; View CI health — `…/t_ViewCIHealth.html` | Brazil |
| S16 | KB0535236 — Troubleshooting the Classification phase — `…KB0535236` | KB (updated 2025-05-27) |
| S17 | Discovery IP address configuration — `…/discovery/discovery-ip-address-configuration.html`; Exclude IP ranges — `…/discovery/exclude-ip-ranges.html`; KB0748222 | Brazil/Yokohama |
| S18 | KB0726425 — CMDB Health duplicate metric algorithm — `…KB0726425` | KB (2019) |
| S19 | KB3037828 — lower-priority rule with specific attributes blocks higher-priority rule — `…KB3037828` | KB (2026-05-22) |
| S20 | Create a CI identification rule — `…/configuration-management-database-cmdb/t_CreateCIIdentificationRule.html` | Brazil/Xanadu |
| S21 | Create an IP-based Discovery schedule in Discovery Admin Workspace — `…/discovery/t-dawCreateNewDiscoSchedule.html` | Brazil |
| S22 | Getting started with credentials — `…/platform-security/connections-and-credentials/credentials-getting-started.html` | Yokohama (2025-01-30) |
| S23 | Create a data refresh rule — `…/configuration-management-database-cmdb/create-datasource-staleness-rule.html` | Brazil (2026-10-21) |
| S24 | Create an IRE data source rule — `…/configuration-management-database-cmdb/create-ire-data-source-rule.html` | Brazil (2026-09-10) |
| S25 | Create a reconciliation rule for a non-CMDB table — `…/configuration-management-database-cmdb/create-reconciliation-rule-non-cmdb.html` | Brazil (2026-09-10) |
| S26 | Identification and Reconciliation Engine (IRE) — `…/configuration-management-database-cmdb/ire.html`; IRE error messages — `…/id-engine-error-messages.html` | Brazil (2026-03-12) |
| S27 | Create a data refresh rule for a non-CMDB table — `…/configuration-management-database-cmdb/create-non-cmdb-data-refresh-rule.html` | Washington DC (2024-02-01) |
| S28 | Create a CMDB Health staleness rule — `…/configuration-management-database-cmdb/t_CreateCMDBHealthStaleRule.html` | Brazil (2026-09-10) |

`…` in the ledger = `https://www.servicenow.com/docs/r` (or `https://support.servicenow.com/kb` for
KB rows). Exact URLs are preserved verbatim in `research/EVIDENCE_DIGEST.md`.

---

*Verify against your release before production use. Everything above is documentation-derived; none
of it was executed against a live instance.*
