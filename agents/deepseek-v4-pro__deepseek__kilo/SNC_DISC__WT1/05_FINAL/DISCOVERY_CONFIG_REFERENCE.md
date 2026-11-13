# ServiceNow Discovery — Configuration Reference (SNC_DISC_RESEARCH)

*Authored by `deepseek-v4-pro__deepseek__kilo` (model **`deepseek-v4-pro`**, provider **DeepSeek**, harness **Kilo**).
Worktree `SNC_DISC__WT1`. Release target: **Brazil** (docs reflect `docs.servicenow.com` Brazil / 2026-09-10+).*

> Every factual claim below carries a source URL, or is explicitly marked `UNVERIFIED`.
> Verify against your instance release before production use. "Discovery" here means
> ServiceNow **horizontal Discovery** (on-prem/cloud ITOM Visibility).

---

## Key links (all verified live — HTTP 200, checked 2026-11-13)

**Official docs (`docs.servicenow.com`, Brazil release):**

- IRE overview — https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/c_CMDBIdentifyandReconcile.html
- Identification rules — https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/c_IdentificationRules.html
- Reconciliation rules — https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/r_ReconciliationRulesPrinciples.html
- IRE data source rule — https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/create-ire-data-source-rule.html
- Data refresh rule — https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/create-datasource-staleness-rule.html
- CI Class Manager — https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/ci-class-manager-landing-page.html
- Identification best practices — https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/best-practices-id-reconcile.html
- Discovery process flow (phases) — https://www.servicenow.com/docs/r/it-operations-management/discovery/c_DiscoProcessFlows.html
- Configuring Discovery — https://www.servicenow.com/docs/r/it-operations-management/discovery/c_DiscoveryConfiguration.html
- Discovery behaviors — https://www.servicenow.com/docs/r/it-operations-management/discovery/c_DiscoveryBehaviors.html
- How Discovery identifiers work — https://www.servicenow.com/docs/r/it-operations-management/discovery/c_HowDiscoveryIdentifiersWork.html

**Knowledge base (`support.servicenow.com`):**

- KB1064718 — IRE fundamentals — https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB1064718
- KB2558192 — duplicate CI tasks vs retired CIs — https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB2558192
- KB3222102 — `sys_updated_on` refresh behavior — https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB3222102
- KB0756709 — data precedence rules — https://support.servicenow.com/kb_view_customer.do?sysparm_article=KB0756709

**Community (corroborating):**

- CI Class Manager & IRE deep dive — https://www.servicenow.com/community/cmdb-forum/a-deep-dive-into-ci-class-manager-and-ire-servicenow-cmdb/m-p/3486406
- Understanding IRE reconciliation rules — https://www.servicenow.com/community/cmdb-articles/understanding-ire-reconciliation-rules/ta-p/3289239
- Avoid duplicate CI creation — https://www.servicenow.com/community/cmdb-forum/how-to-avoid-duplicate-ci-creation/m-p/3498456
- Discovery overview — https://www.servicenow.com/community/itom-articles/servicenow-discovery-overview/ta-p/2321453

---

## Applicability at a glance (corrected)

The four IRE controls are **not** uniformly "per class, on insert and update". Each has its own
scope and insert-vs-update behaviour — see `IRE_RULE_APPLICABILITY_MATRIX.md` for the full
permutation list (39 worked examples) and the controlling fields/system properties.

| Rule family | INSERT? | UPDATE? |
|---|---|---|
| Identification rules | yes — no match → create | yes — match → update |
| Reconciliation rules (static/dynamic) | no | yes |
| IRE data source rules | **yes — blocks insert** | no |
| Data refresh rules | no | yes — stale → lower-priority source may update |

---

## 1. Discovery configuration options (the "what can I configure?" surface)

Discovery is driven by these configuration elements (`c_DiscoveryConfiguration`):

- **IP address ranges / schedules** — what to scan and when. Schedules specify one or more
  IP addresses or ranges, and can run on a regular schedule or be launched on demand
  (Discover now / Quick Discovery).
  <https://www.servicenow.com/docs/r/it-operations-management/discovery/c_DiscoProcessFlows.html>
- **Credentials** — Discovery needs per-range credentials to connect and run probes
  (WMI, SSH, SNMP, PowerShell, HTTP).
  <https://www.servicenow.com/docs/r/it-operations-management/discovery/c_DiscoveryConfiguration.html>
- **MID Server** — the agent that runs probes/sensors against hosts and returns results via the
  External Communication Channel (ECC) queue. Discovery follows a documented sequence to select a MID Server.
  <https://www.servicenow.com/docs/r/it-operations-management/discovery/c_DiscoProcessFlows.html>
- **Discovery behaviors** — determine which probes **Shazzam** launches and **from which MID Servers**.
  A behavior holds one or more **functionalities** (protocol definitions + MID Server list + phase number +
  functionality criteria). Used for load-balancing, multi-domain WMI, ACL-protected SNMP, and dual-protocol devices.
  <https://www.servicenow.com/docs/r/it-operations-management/discovery/c_DiscoveryBehaviors.html>
- **Classifiers** — per-device-class records that specify which probes run in the identification and
  exploration phases.
  <https://www.servicenow.com/docs/r/it-operations-management/discovery/c_DiscoProcessFlows.html>
- **Probes vs Patterns** — probes/sensors are JavaScript-based; **Patterns** are written in Neebula
  Discovery Language (NDL) and can cover the identification + exploration phases via the
  **Horizontal Pattern probe**. Server-side (Jakarta+) horizontal discovery defaults to patterns where available.
  <https://www.servicenow.com/community/itom-articles/servicenow-discovery-overview/ta-p/2321453>
- **Discovery properties** — `r_DiscoveryProperties` lists system properties that tune Discovery.
  <https://www.servicenow.com/docs/r/it-operations-management/discovery/r_DiscoveryProperties.html> *(UNVERIFIED — page not rendered; exists per docs index)*
- **ITOM Configuration Console** — faster guided install/config (interactive pages, task assignment, ServiceNow Otto).
  <https://www.servicenow.com/docs/r/it-operations-management/discovery/c_DiscoveryConfigurationConsole.html>

## 2. Order of operations (the 4 Discovery phases)

Horizontal Discovery passes through **four phases**, orchestrated through the **ECC queue** and the **MID Server**
(`c_DiscoProcessFlows`):

1. **Scanning (Shazzam)** — the Shazzam probe + port probes go into the ECC queue; the MID Server runs them,
   scanning common ports (WMI 135, HTTP, SSH 22, SNMP 161). Open ports are reported back and identify the machine type.
2. **Classification** — one classification probe per device determines the precise device class
   (e.g., OS version → the CI class). It also determines which classifier/probes run next.
3. **Identification** — an **identification trigger probe** (or the **Horizontal Pattern probe** for patterns)
   collects identity data; sensors process it; Discovery runs CI identifiers against the CMDB and
   **updates an existing CI or creates a new one**.
4. **Exploration** — exploration trigger probes (from the classifier's Trigger Probes related list) gather
   in-depth info and populate CI attributes/relationships.

> With **patterns**, the Horizontal Pattern probe covers both identification and exploration; probes/sensors are not used.
> <https://www.servicenow.com/docs/r/it-operations-management/discovery/c_DiscoProcessFlows.html>

The **ECC queue** exposes the four phases as queue/state values: Port Scanning (Shazzam), Classify, Identify, Exploration.
<https://www.servicenow.com/community/itom-articles/servicenow-discovery-overview/ta-p/2321453>

**Identity probe behavior** (`c_HowDiscoveryIdentifiersWork`): the identity probe asks for serial numbers, name, network id;
the identity sensor passes results to the identifier; the identifier then:
**find match → update (or nothing)** / **no match → create (or nothing)**, then (if configured to continue) launches exploration probes.
<https://www.servicenow.com/docs/r/it-operations-management/discovery/c_HowDiscoveryIdentifiersWork.html>

## 3. CI Class Manager — key bread crumbs

Access: **All → Configuration → CI Class Manager**. `sn_cmdb_admin` has full access; `sn_cmdb_editor` read-only.
The CI Class Manager centrally manages class definitions, **IRE settings**, **CMDB Health**, and some Service Mapping defs.
<https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/ci-class-manager-landing-page.html>

Under the **IRE** section of a selected CI class you configure:

| Area | What you create | Official link |
|---|---|---|
| **Identification** | CI identification rule; identification **inclusion** rule | `t_CreateCIIdentificationRule`, `create-id-inclusion-rule` |
| **Reconciliation** | CI reconciliation rule (static/dynamic); **data refresh rule** | `create-reconciliation-rule`, `create-datasource-staleness-rule` |
| **Dependencies** | Dependent relationship rule (hosting / containment) | `create-dependent-relationship` |

The same identification rules are reachable from the app navigator:
**All → Configuration → Identification/Reconciliation → CI Identifiers**.
<https://www.servicenow.com/community/cmdb-forum/identification-and-reconciliation-rule/td-p/3142427>

**IRE data source rules** are a separate module:
**All → Configuration → Identification/Reconciliation → IRE Data Source Rule** (stored in `cmdb_ire_data_source_rule`).
<https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/create-ire-data-source-rule.html>

## 4. Identification rules (how a CI is uniquely recognized → duplicate prevention)

The CMDB identification process relies on **identification rules** to uniquely identify CIs. A rule applies to a **CI class**
and consists of a single **CI identifier** plus one or more **identifier entries** and **related entries**, each with a priority.
<https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/c_IdentificationRules.html>

Key concepts:

- **Unique attributes** — criterion attribute value sets that uniquely identify the CI (same or derived table).
- **Required attributes** — attributes that cannot be empty.
- **Hierarchy derivation** — a child class without its own rule **derives** the parent's rule (incl. entries); defining a
  child rule **overwrites** the derived one, so entries must be re-added explicitly.
- **Rule types**:
  - **Independent identification rule** — identifies by the CI's own attributes (always preferred).
  - **Dependent identification rule** — requires identifying a dependent CI first (max 2 dependency levels; minimize use).
- **Identifier entries**:
  - **Regular** — CI's own attributes.
  - **Lookup** — uses a related/lookup table (e.g. Serial Numbers, Network Adapters) that references `cmdb_ci`.
  - **Hybrid** — regular + lookup combined.
- **Inclusion rules ("Inclusion Rule (Advanced)")** — narrow the CI scope IRE considers during identification
  (e.g. only `Operational status = Operational`).
- **Related entries** — create/update records on related tables (not used to identify).

Best practices (order of importance): prefer **independent** rules; **avoid lookup entries**; **limit identifier entries to 1**;
set strongest entries at highest priority.
<https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/best-practices-id-reconcile.html>

> **Duplicate prevention hinges on identification rules.** IRE checks identification rules per class to decide
> "new CI" vs "existing CI". If a match is found → **update**; else → **create**. Rules are evaluated **per class**,
> so identical attribute values in *different classes* can still produce separate CIs — the common "Discovery created a
> new CI even though one with the same name exists" failure is almost always a weak/class-mismatched identifier, not a bug.
> <https://www.servicenow.com/community/developer-forum/servicenow-discovery-creating-a-new-ci-even-though-an-existing/m-p/3590971>
> <https://www.servicenow.com/community/cmdb-forum/how-to-avoid-duplicate-ci-creation/m-p/3498456>

When IRE detects duplicate CIs it groups each set into a **de-duplication task** for review/remediation; a large duplicate
count usually means weak identification rules. IRE also evaluates **retired CIs** by default and raises a **Duplicate CI task**
when an active CI shares identifying attributes with a retired one.
<https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/c_CMDBIdentifyandReconcile.html>
<https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB2558192>

## 5. Reconciliation rules (which source may update which field → insert/update control)

Reconciliation rules determine **which discovery sources can update which CI attributes**; without them, sources overwrite
each other. Two types:
<https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/r_ReconciliationRulesPrinciples.html>

- **Static** — legacy; set priority/precedence per discovery source per attribute.
  Stored in **Reconciliation Definition** `cmdb_reconciliation_definition`.
- **Dynamic** — based on CMDB 360 (largest / most-reported value), not source priority; requires CMDB 360.
  Stored in **Dynamic Reconciliation Definitions** `cmdb_dynamic_reconciliation_definition`.

Precedence principles:

1. **Dynamic beats static** when both exist for the same attribute.
2. **Attribute-specific rules beat "all attributes" rules** — a rule listing specific attributes overrides a blank-`Attributes`
   rule that grants the whole class. *(Best practice: always list the exact attributes a source may update; leave `Attributes`
   empty only when you truly mean "all".)*
   <https://www.servicenow.com/community/itom-forum/attributes-field-in-reconciliation-rules-in-ire-does-it-actually/m-p/1025487>
3. **Child-class rules override parent-class rules** for the overridden attribute.
4. **Overlapping static rules coexist** — two sources may both be authorized for the same attribute; reconciliation then
   prevents them overwriting each other.

Data precedence (which source's value wins when several may update a field) is tracked in the
**Data Source History** `cmdb_datasource_last_update` table; the **data precedence rules** KB is `KB0756709`.
<https://www.servicenow.com/community/itom-forum/attributes-field-in-reconciliation-rules-in-ire-does-it-actually/m-p/1025487>
<https://support.servicenow.com/kb_view_customer.do?sysparm_article=KB0756709>

## 6. IRE data source rules (block a source from *inserting*, but let it *update*)

An **IRE data source rule** prevents a specific discovery source from **inserting new CIs** of a specific class while still
letting it **update existing ones** (e.g. an IP scanner that shouldn't fabricate server CIs). Stored in
**IRE Data Source Rule** `cmdb_ire_data_source_rule`. Fields: `Active`, `Applies to` (class), `Data source`, `Insert Not Allowed`.
<https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/create-ire-data-source-rule.html>

- Child classes **derive** the parent's data source rules; child rules **override** parent rules.
- When a prohibited **insert** is attempted: `CreateOrUpdateCIEnhanced()` stores the failed payload in
  **CMDB IRE Partial Payloads** `cmdb_ire_partial_payloads`; plain `createOrUpdateCI()` fails the whole payload (no partial commits).
- A later permitted source's insert merges the stored partial payload, deletes it, and then the previously-prohibited
  source may update that CI.
- Data source rules **do not apply** to lookup/related items; only **one active rule per class/source pair**.
- **No impact when dynamic reconciliation rules are in effect.**

## 7. Data refresh rules (staleness — when a lower-priority source may take over)

**Data refresh rules** determine **whether a CI is stale for a given discovery source**, used together with static
reconciliation rules to decide if/when/by-which-source a CI may be updated.
<https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/create-datasource-staleness-rule.html>

- Location: **CI Class Manager → select class → Class Info → Reconciliation Rules → Data Refresh Rules → Add**.
- Fields: **Discovery source** (whose staleness is evaluated), **Effective Duration** (staleness window), **Active**.
- Semantics: if the fields in the class's static reconciliation rule weren't updated by that source within **Effective Duration**,
  the CI is **stale** and a **lower-priority** authorized source may update it. `Effective Duration = 0` ⇒ stale immediately
  (lower-priority source always allowed).
- **No impact when dynamic reconciliation rules are in effect.** Precedence order of reconciliation rules is unchanged by data refresh rules.

## 8. Insert vs update — what actually gets written to the CMDB

- Identification and the field-update are **separate steps**. Identification matches the device to an existing CI using
  identifier rules (regardless of the CI's `install_status`); IRE then reconciles **only the attributes present in the payload**
  for that class.
  <https://www.servicenow.com/community/cmdb-forum/rediscovered-ci-remains-retired-why-doesn-t-ootb-discovery/m-p/3575543>
- **No data change → no write.** If Discovery collects values that already equal the CI's attributes, no update occurs and
  `sys_updated_on` is **not** refreshed (distinguishes "still collecting but unchanged" from "not collecting at all").
  <https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB3222102>
- IRE always updates **`last_discovered`** and **`discovery_source`** during payload processing even when nothing else changes
  ("Timestamps in key attributes").
  <https://www.servicenow.com/community/servicenow-ai-platform-forum/when-does-ire-update-the-discovery-source-field-of-a-ci/m-p/1111012>
- Lifecycle fields such as **`install_status`** are typically **not** in the OOTB Discovery payload, so a rediscovered
  "Retired" CI is **not** auto-flipped back to "Installed" — that is expected behavior, not a bug.
  <https://www.servicenow.com/community/cmdb-forum/rediscovered-ci-remains-retired-why-doesn-t-ootb-discovery/m-p/3575543>

## 9. IRE at a glance

The **Identification and Reconciliation Engine (IRE)** is a centralized framework that processes payloads to maintain the
CMDB (and some non-CMDB tables): it **creates new CIs** and **updates existing CIs**. Applications such as Service Mapping,
horizontal Discovery, and pattern Discovery apply IRE via APIs; import sets and third-party sources use REST / scriptable IRE APIs.
Processing order: **identification rules** find CIs → **inclusion rules** decide which may be used → **reconciliation rules**
decide which source updates which field (with **data source rules** and **data refresh rules** further shaping inserts/updates).
<https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/c_CMDBIdentifyandReconcile.html>
<https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB1064718>

---

## Source map (all URLs cited above)

Official docs (Brazil release, `docs.servicenow.com`):

- Identification rules — <https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/c_IdentificationRules.html>
- Reconciliation rules — <https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/r_ReconciliationRulesPrinciples.html>
- IRE data source rule — <https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/create-ire-data-source-rule.html>
- Data refresh rule — <https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/create-datasource-staleness-rule.html>
- IRE overview — <https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/c_CMDBIdentifyandReconcile.html>
- CI Class Manager — <https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/ci-class-manager-landing-page.html>
- Identification best practices — <https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/best-practices-id-reconcile.html>
- Discovery process flow — <https://www.servicenow.com/docs/r/it-operations-management/discovery/c_DiscoProcessFlows.html>
- Configuring Discovery — <https://www.servicenow.com/docs/r/it-operations-management/discovery/c_DiscoveryConfiguration.html>
- Discovery behaviors — <https://www.servicenow.com/docs/r/it-operations-management/discovery/c_DiscoveryBehaviors.html>
- How Discovery identifiers work — <https://www.servicenow.com/docs/r/it-operations-management/discovery/c_HowDiscoveryIdentifiersWork.html>

Knowledge base:

- IRE fundamentals — <https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB1064718>
- Duplicate CI tasks vs retired CIs — <https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB2558192>
- `sys_updated_on` refresh behavior — <https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB3222102>
- Data precedence rules — <https://support.servicenow.com/kb_view_customer.do?sysparm_article=KB0756709>

Community (corroborating):

- CI Class Manager & IRE deep dive — <https://www.servicenow.com/community/cmdb-forum/a-deep-dive-into-ci-class-manager-and-ire-servicenow-cmdb/m-p/3486406>
- Understanding IRE reconciliation rules — <https://www.servicenow.com/community/cmdb-articles/understanding-ire-reconciliation-rules/ta-p/3289239>
- Identification vs reconciliation rules — <https://www.servicenow.com/community/cmdb-articles/cmdb-understanding-identification-and-reconciliation-rules-and/ta-p/3520826>
- Avoid duplicate CI creation — <https://www.servicenow.com/community/cmdb-forum/how-to-avoid-duplicate-ci-creation/m-p/3498456>
- Discovery overview — <https://www.servicenow.com/community/itom-articles/servicenow-discovery-overview/ta-p/2321453>

> Raw evidence transcripts are in this worktree's `research/` folder (search digests + `research/official_docs/*.md`).
