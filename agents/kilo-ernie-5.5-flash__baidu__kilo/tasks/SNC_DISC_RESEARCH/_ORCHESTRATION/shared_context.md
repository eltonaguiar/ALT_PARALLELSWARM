# Shared context — distilled ServiceNow Discovery sources

> Fed to peer worktrees (WT2..WT5) as background. These are paraphrased vendor facts
> with source URLs; peers should treat them as ground truth but flag anything they
> cannot corroborate.

## A. Discovery = horizontal discovery (bottom-up)
Discovery finds CIs on the network and updates the CMDB. It uses:
- **Probes** — scripts that collect info on a host (run via the MID Server).
- **Sensors** — process the data a probe returns and update the CMDB.
- **Patterns** — NDL (Neebula Discovery Language) series of operations; replace probes/sensors
  in the last two phases; built in Pattern Designer. Patterns define which CMDB tables to populate.

Both probes and sensors get instructions from the **ECC queue** (External Communication Channel).
A worker on the MID Server watches the ECC queue; probe results return to the queue as *input*
records; an insert business rule runs the sensor processor, which routes data to sensors that
update the CMDB.

## B. The four phases (order of operations)
1. **Scanning** — Shazzam probe + port probes detect open ports (WMI 135, SSH 22, SNMP 161, HTTP 80/443). Open ports hint at device type (e.g. port 22 → UNIX/Linux).
2. **Classification** — a *classification probe* gathers OS/version detail; **classifiers** decide the device class and which trigger probes run next. Only one classification probe per device. HTTP is lowest priority (used only if WMI/SSH/SNMP fail).
3. **Identification** — the classifier's *identification trigger probe* runs; identification rules (CI identifiers) decide **insert vs update** in the CMDB. If a pattern is used, the Horizontal Pattern probe launches it and IRE does identification.
4. **Exploration** — *exploration trigger probes* gather more detail (apps, memory, NICs, drivers) and create relationships; sensors update the CMDB.

Classifiers: device classification, process classification (creates child CIs with Runs on::Runs), IP-address (credential-less) classification.

## C. Discovery Schedule (control point)
- `All > ITOM > Discovery > Discovery Schedules` (or via Guided Setup). Key fields:
  - **Discover** type: Configuration items / IP addresses / Networks / Service / Serverless / Cloud application / Cloud resources / Certificates.
  - **MID Server selection method**: Auto-Select / Specific MID Cluster / Specific MID Server / Use Behavior.
  - **Shazzam batch size** (default 1000; min 256) — IPs per Shazzam probe.
  - **Max run time / Max Idle time**, **Location**, **Log state changes**, **Use SNMP Version**, **Quick ranges**, **IP Ranges** related list, **Discovery Range Sets**.
- **Behaviors** map functionalities (protocol lists) to MID Servers and phases for load balancing / multi-domain / ACL / dual-protocol control.

## D. CI Class Manager
- Navigate: `All > Configuration > CI Class Manager`. Requires `sn_cmdb_admin` (full) / `sn_cmdb_editor` (read).
- Tree view of the CMDB class hierarchy. Select a class, then use the class navigation bar:
  - **Class Info** (Basic Info), **Attributes**, **Identification and Reconciliation**,
    **Dependent Relationships**, **Suggested Relationships**, **All Relationship Rules**,
    **Health**, **CI List**.
- Create a class: select parent → **Add Child Class** → Provide Basic Info → Add Attributes
  (set Identification=true for identifier attributes) → Set Identification Rule → Dependencies →
  Add Reconciliation Rules → Add Suggested Relationships → Done.

## E. IRE — Identification & Reconciliation Engine
- IRE is the centralized engine that processes incoming data before CMDB insert/update across
  sources (Discovery, Import Sets, Service Mapping, monitoring).
- **Identification**: uniquely identify a CI (does it already exist?). Uses **identification rules**
  (identifier entries) or `source_name` + `source_native_key` (sys_object_source_info).
- **Reconciliation**: only on **update** (not insert); decides which **data source** may write each
  CI attribute. Uses **reconciliation rules** + **IRE data source rules**.
- **Identifier entries**: Regular (CI's own attributes), Lookup (a related table referencing the CI),
  Hybrid (combination). Prefer independent rules; minimize dependent rules; limit identifier entries (ideally 1).
- **De-duplication**: duplicate CIs are grouped into de-duplication tasks.

## F. Duplicate avoidance specifics
- `glide.identification_engine.skip_duplicates` (default **true**): if #duplicates < `glide.identification_engine.skip_duplicates.threshold` (default **5**), the **oldest** duplicate is the match and becomes the main CI; others get `duplicate_of` = main CI and are filtered out during matching. If set **false**, matching fails with an error and no duplicates are updated. De-dup tasks are always created.
- `glide.duplicate_ci_remediator.max.cis` governs processing of large duplicate sets.
- `glide.identification_engine.lookup_match.create_duplicate_task_ci.enabled` (default false): create de-dup tasks for duplicate lookup items.
- Duplicate lookup/related item tables: `cmdb_serial_number`, `cmdb_software_instance`; allowed classes in `cmdb_duplicate_lookup_related_allowed_class`.

## G. Reconciliation rules
- **Static** (legacy): priority order among discovery sources per CI attribute; stored in
  `cmdb_reconciliation_definition`. Child-class rules override parent; empty attribute list = whole class;
  dynamic overrides static for same attribute; overlapping static rules coexist.
- **Dynamic**: value-based (largest/most-reported) using CMDB 360; stored in
  `cmdb_dynamic_reconciliation_definition`; one per attribute; requires CMDB 360.
- **Data Refresh Rules**: mark a CI stale for a source so a lower-priority source may update; last-touch
  timestamps in `cmdb_datasource_last_update`.

## H. Useful properties (glide.discovery.*)
- `glide.discovery.log_debug` (false) — Discovery debug logging.
- `glide.discovery.debug.ci_identification` (false) — CI identification debug log.
- `glide.discovery.sensors.save_attachments` (true) — keep ECC attachments after sensor processing.
- `glide.discovery.max_concurrent_invocations_per_schedule` (3).
- `glide.discovery.hostname.always_update` (true) — always update hostname from most recent trusted source.
- `glide.discovery.enable_mac_address_verification` (false) — detect IP change mid-discovery.
- `glide.discovery.save_pattern_log` (true) — save pattern logs.
- `glide.discovery.log_message_length` (200).

## Sources
- https://www.servicenow.com/docs/r/it-operations-management/discovery/c_GetStartedWithDiscovery.html
- https://www.servicenow.com/docs/r/it-operations-management/discovery/c_DiscoveryProbesAndSensors.html
- https://www.servicenow.com/docs/r/zurich/it-operations-management/discovery/c_DiscoProcessFlows.html
- https://www.servicenow.com/docs/r/it-operations-management/discovery/discovery-classifiers.html
- https://www.servicenow.com/docs/r/it-operations-management/discovery/discovery-schedule-form.html
- https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/ci-class-manager-landing-page.html
- https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/c_CompsandProcessIDandReconcil.html
- https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/ire.html
- https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/id-detect-dup-ci.html
- https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/r_ReconciliationRulesPrinciples.html
- https://www.servicenow.com/docs/r/it-operations-management/discovery/r_DiscoveryProperties.html