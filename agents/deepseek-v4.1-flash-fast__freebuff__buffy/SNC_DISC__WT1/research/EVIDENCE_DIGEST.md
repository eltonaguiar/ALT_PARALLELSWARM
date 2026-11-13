# Evidence digest — SNC_DISC__WT1

Raw, quoted evidence collected **before** synthesis, so the reference can be audited line by line.
Quotes are verbatim from the fetched page unless shown in brackets.

---

## [S1] Discovery identifiers
URL: https://www.servicenow.com/docs/r/it-operations-management/discovery/c_DiscoveryIdentifiers.html
Release label: Brazil · updated 2026-09-10

> "After Discovery classifies a configuration item (CI), it uses identifiers to determine if the
> device already exists in the Configuration Management Database (CMDB)."

> "This identification step only takes place for the Configuration item type of discovery, not for
> the other types of discovery."

> "If the identifier finds a matching CI, the identifier either updates that CI or does nothing. If
> the identifier cannot find a matching CI, it either creates a new CI or does nothing."

> "Serial numbers are necessary for accurate asset tracking. … do not configure sensors or patterns
> to modify the serial number syntax, such as adding a custom prefix."

Tables: Identifier [`cmdb_identifier`] stores all identifier rules; Identifier Entry
[`cmdb_identifier_entry`] stores all the identifier attributes.

Rules table: ESX Server (`correlation_id`); Hardware (`serial_number`, `serial_number_type`, `name`,
`ip_address`, `mac_address`, + Serial Number `cmdb_serial_number`, Network Adapter
`cmdb_ci_network_adapter`); Storage Server (`cim_object_path`, name, serial, MAC, IP + lookups);
WBEM Service (`cim_object_path`).

> "The `sys_class_name` cannot be an attribute for independent rules, such as `cmdb_ci_hardware`."

> "If you create an identifier with the name attribute, avoid changing adapter names. Discovery will
> be unable to resolve existing CIs for renamed adapters. Discovery labels the Install Status of that
> CI as 'Absent' and creates another CI."

> "Custom identifiers must have different Order values than those of the default identifiers."

> "Use the `glide.identification_engine.skip_duplicates` and
> `glide.identification_engine.skip_duplicates.threshold` properties."

> "`glide.discovery.use_cmdb_identifiers` … If you upgraded from a pre-Geneva version, you must
> manually add this property and set it to true." / "When Service Mapping is active, the new
> identifiers … are always used regardless of the property value."

---

## [S2] Identification rules
URL: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/c_IdentificationRules.html
Release label: Brazil · 2026-09-10

> "An identification rule applies to a CI class and consists of a single CI identifier and one or
> more identifier entries and related entries, each with a different priority."

> "If no identification rule is explicitly defined for a child class, then the child class derives
> its identification rule … Later, an own identification rule can be explicitly defined for the child
> class. In that case … the Hardware class identification rule, including its associated related entry
> for the Software Instance table, is no longer in effect for the Computer class."

Entry types: Regular / Lookup / Hybrid (hybrid example: two cloud VMs with identical serials).

> "Do not create conflicting identification rules especially for lookup-based rule. Example: In a CI
> Identifier for the Hardware class, you specify a lookup-based rule for the Network Adapter class and
> you also define a CI Identifier for the Network Adapter class. Duplicates might potentially be
> created in the Network Adapter table."

> "It is preferable to enforce exact count match … for a stronger identification rule."

> "Related entries are not used to directly identify CIs."

---

## [S3] Reconciliation rules
URL: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/r_ReconciliationRulesPrinciples.html
Release label: Brazil · 2026-09-10

> "Reconciliation rules determine which discovery sources can update CI attributes."

Static rules stored in Reconciliation Definition [`cmdb_reconciliation_definition`]; dynamic rules in
Dynamic Reconciliation Definitions [`cmdb_dynamic_reconciliation_definition`].

> "When both, static and dynamic reconciliation rules exist for the same CI attribute, the dynamic
> reconciliation rule takes precedence over the static reconciliation rule."

> "A rule that grants access to specific attributes in a class overrides other static reconciliation
> rules with an empty attribute list that grants access to the entire class."

> "Any reconciliation rules defined for a child class override the rules defined for its parent class."

> "Static reconciliation rules that authorize different discovery sources for the same attributes of
> the same class can coexist and do not exclude each other. … Any reconciliation rules are enforced to
> prevent the discovery sources from overwriting each other's updates."

Dynamic rules: "CMDB 360 processes the current payload data … applying a dynamic reconciliation rule,
IRE selects the largest or most reported value" + "you must enable that feature".

---

## [S4] Discovery Schedule form reference
URL: https://www.servicenow.com/docs/r/it-operations-management/discovery/discovery-schedule-form.html
Release label: Brazil · updated 2026-11-05

Discover options: Configuration items / IP addresses / Networks / Service / Serverless / Cloud
application / Cloud resources / Certificates.

> "IP addresses: Scans devices without the use of credentials. These scans discover all the active IP
> addresses in the specified range and create device history records, but don't update the CMDB."

> "Auto-Select MID Server: … you must configure MID Servers to use: The Discovery application, or ALL
> applications … The IP range that includes the ranges you configure on the discovery schedule." /
> "MID Server auto-select isn't supported with IPv6."

> "Use Behavior: … Scans requiring multiple Windows credentials. … more than one MID Server. … Load
> balancing for large discoveries … Scanning multiple domains."

> "Max run time … the remaining tasks for the discovery are canceled, even if the scan isn't complete."

> "By default, the Max Idle time field doesn't display in the Discovery Schedule form. To include this
> parameter, open the Discovery Schedules [discovery_schedule] table, add the column…"

> "Shazzam batch size … By default, the batch size is 1000. A UI policy enforces a minimum batch size
> of 256 because batch sizes below 256 IP addresses don't benefit from clustering. The policy converts
> any value below 256 to a value of zero."

> "Shazzam cluster support … These probes are run in sequence and not concurrently."

> "Use SNMP Version … The default value is ALL."

> "Discovery Agent … available only when the system property glide.discovery.enable_ssm is enabled…"

Related lists: IP Ranges, Discovery Range Sets, Discovery Status, Global IP Exclusion, Discovery
Attributes, Certificate URLs.

---

## [S5] Set up Discovery without Guided Setup
URL: https://www.servicenow.com/docs/r/it-operations-management/discovery/t_ConfigureDiscovery.html

> "Grant Discovery role: Confirm that users who are expected to configure and execute Discovery in
> your network have the discovery_admin role."

> "Install at least two MID Servers at first and assign them to different schedules and IP ranges to
> help complete discoveries quicker. Starting with the Istanbul release, you must make sure that the
> MID Server is assigned the Discovery application or the ALL application."

> "The MID Server might not have outbound access on port 443 (SSL) or a proxy server might be
> preventing TCP…" / "If Basic Authentication is enabled, a user name and password must be provided."

Scheduling step: "Make sure to test your credentials before you run a schedule. Bad credentials are a
leading cause of failed discoveries." (from companion scheduling page, same doc set)

---

## [S6] Discovery device history
URL: https://www.servicenow.com/docs/r/it-operations-management/discovery/r_DiscoveryStatusDevices.html

Per-device Completed activity values:
- "Alive, not active, not classified | After Shazzam | Device is responding, but it does not have any open (active) ports…"
- "Active | After Shazzam | Device has open (active) ports…"
- "Classified | After Classification Probe | We were able to classify the device type and will be proceeding to the Identification stage."
- "Active, couldn't classify | After Classification Probe …"
- "Identified CI | After Identification Probe/Pattern | Existing CI has been found based on identification results."
- "Identified, ignored extra IP | … Device has already been discovered via a different IP in same Discovery status."
- "Updated CI | After certain Exploration Probes/Patterns … CI has been updated with additional information."

> "This number does not include the universal probes, Shazzam and Ping, that run initially."
> "Scan status | … For example, Scan 17 of 19."

Also: for IP-address scans "there is no CMDB activity … displays only the classification status."

---

## [S7] Horizontal discovery process flow with probes and sensors
URL: https://www.servicenow.com/docs/r/it-operations-management/discovery/c_DiscoProcessFlows.html

> "Scanning phase: The Shazzam probe and port probes are executed via the MID Server to detect open
> ports … Results are returned to the instance through the External Communication Channel (ECC) queue."

> "Classification phase: … Discovery sends a classification probe … Only one classification probe runs
> per device."

> "Identification phase: Discovery selects the appropriate classifier based on the CI class to run
> identification trigger probes that apply identification rules. These rules decide whether to insert
> or update CIs in the CMDB."

> "Exploration phase: Exploration probes specified in the classifier's Triggers Probes related list run
> to collect additional data and enrich the CI information."

---

## [S8] KB0869861 — How to troubleshoot duplicate CMDB CI records
URL: https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB0869861

> "A duplicate record, as defined by the IRE, is a record created when a CI should have been updated
> instead based on the identification rules."

> "Duplicates may be created when any of the following factors prevent the identification engine from
> finding an existing CI: Inclusion rules; Query business rules; Access control lists (ACLs)."

> "…depending on the release, the IRE does not identify CIs when: The `duplicate_of` field is not
> empty. The `discovery_source` field is set to `Duplicate`."

> "This can occur when discovering the same CI in separate discoveries at the same time, or when
> payloads in the same discovery contain the same dependent CI in more than one payload."

> "Set the `glide.discovery.multi_page_serial_mode` property to true so that multipage payloads are
> processed in serial. This prevents the creation of duplicate CIs by Discovery."

> "Warning: Creating an inclusion rule for a parent class such as `cmdb_ci_hardware` with conditions
> that include 'Class' can cause duplicate CIs. The inclusion rule applies to all child classes, so
> any child class passed to the IRE that is not included in the condition is not found by the engine."

Also: "In the pattern, add a step to remove duplicates before they are sent back to the instance."

---

## [S9] KB0756709 — How CMDB reconciliation and data precedence rules work
URL: https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB0756709

> "Each time a CI is inserted or updated, the IRE records the attribute-level changes in the Data
> Source History [cmdb_datasource_last_update] table, including the source name."

> "When a CI is created through the IRE, the system creates the CI regardless of reconciliation rules
> because it is a new record."

> "If the source is allowed, the IRE checks whether a higher-priority data source has previously
> updated the same attributes. If so, the IRE skips the update for those attributes."

> "The `glide.reconciliation.override.null` property controls whether a lower-priority data source can
> update an empty field on a CI."

> "Data precedence rules were merged with reconciliation rules beginning with the Paris release."

---

## [S10] KB1064718 — CMDB IRE fundamentals
URL: https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB1064718

> "The IRE uses identification rules to find CIs in the CMDB." / "The IRE first applies the
> identification rules to find CIs in the CMDB, and then applies the inclusion rules to determine if
> those CIs can be used."

> "To open CI Class Manager, go to Configuration > CI Class Manager."

Independent vs dependent CIs; dependent relationship rules live in CI Class Manager.

---

## [S11] Duplicate CIs remediation
URL: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/de-duplication-tasks.html

> "After remediation, a set of duplicate CIs consists of one main CI, and any number of CIs, each
> considered a duplicate of the main CI. The duplicate_of attribute of the main CI is empty."

> "Role required: itil to read, itil_admin or cmdb_dedup_admin to write" (legacy remediator page)

> "Set attributes to custom values (recommended): Retain all duplicate CIs. Mark the duplicate CIs as
> invalid by setting a specific Attribute to a specific Value … The duplicate_of attribute of the
> duplicate CIs is automatically set to the appropriate main CI."

> "Use CMDB Workspace to create de-duplication templates for consistent bulk remediation of duplicates."

Restrictions: main CI cannot reference a CI as its main; if a main CI becomes a duplicate, its
duplicates re-point; duplicate of 'Unknown' blocks the operation.

---

## [S12] Discovery properties + Available system properties
URLs:
https://www.servicenow.com/docs/r/it-operations-management/discovery/r_DiscoveryProperties.html
https://www.servicenow.com/docs/r/platform-administration/r_AvailableSystemProperties.html

> "Edit the following Discovery properties by navigating to Discovery Definition > Properties."

Entries seen: `glide.discovery.application_mapping` (default true), `glide.discovery.log_debug_info`
(default false), `glide.discovery.log_message_chars` (default 200, location Discovery Definition >
Properties), `glide.discovery.multi_page_serial_mode` (default false; "false sets the pages to process
in parallel and true sets the pages to process serially"), `glide.discovery.sam_batch_update_size`
(default 100), `glide.discovery.enable.software_filter` (default true), `glide.discovery.L3_mapping`,
`glide.discovery.roundingInterval.cpu`, `glide.discovery.retire_stale_accounts`.

Note the further spelling `glide.identificationengine.skipduplicates` appears in the properties
summary ("Properties such as … and glide.identificationengine.skipduplicates manage CMDB data
processing"). Recorded as a discrepancy, not silently normalised.

---

## [S13] View and edit class definitions and metadata (CI Class Manager)
URL: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/t_ViewTableDefinitions.html

> "Navigate to All > Configuration > CI Class Manager. Select Hierarchy to expand the CI Classes list
> and then select a class…"

Nav items: `Class Info` → `Basic Info` (display name, table name, description, class icon),
`Dependent Relationships` (hosting/containment), `All Relationship Rules`, `Health` ("review and
configure CMDB Health-related system properties, scorecards, and rules and settings … at the class
level").

---

## [S14] Dependent relationship rules
URLs:
https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/create-dependent-relationship.html
https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/c_ServiceRulesMetadata.html

> "The class for which you create dependent relationship rule, must have a dependent identification rule."

> "Navigate to All > Configuration > CI Class Manager. … In the class navigation bar, click
> Dependent Relationships."

> "The CI Class Manager and the Metadata Editor are synchronized."

> "Hosting rules represent CIs' placement in a business definition, describing what CIs run on."

---

## [S15] CMDB Health KPIs
URLs:
https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/r_CMDBHealthMetrics.html
https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/t_ViewCIHealth.html

> "CMDB Health calculates an aggregated score for three Key Performance Indicators (KPIs) which are
> correctness, compliance, and completeness."

> Orphan: CI satisfies an orphan rule, or data is missing in its table/parents' table.
> Staleness: default staleness rule applies to the class.

> "Duplicate * If no identification rules ([cmdb_identifier]) are defined for the CI's class or its
> ancestors: A notification to that effect appears. * If only dependent identification rules are
> defined: Not applicable notification appears."

Orphan rules are per class, only one per class, stored in `cmdb_health_orphan_rule`.

---

## [S16] KB0535236 — Troubleshooting the Classification phase
URL: https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB0535236

> "The classification phase of Discovery begins right after the Shazzam port scanner probe … This is
> the first time Discovery uses credentials to query a target."

> "Each classification type then dictates the probes that Discovery runs for the Identification phase
> and Exploration phase."

> "If a classifier probe cannot connect to a device, the Discovery status lists it as Active, couldn't
> Classify."

---

## [S17] IP address configuration / exclusions
URLs:
https://www.servicenow.com/docs/r/it-operations-management/discovery/discovery-ip-address-configuration.html
https://www.servicenow.com/docs/r/it-operations-management/discovery/exclude-ip-ranges.html
https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB0748222

> "IPv6 addresses are not supported for IP range or network definitions in Discovery."

> "IP network: Specifies entire IP networks using CIDR notation … Discovery automatically excludes
> network and broadcast addresses from scans."

> "Exclude IPs is not supported for IPv6 ranges or subnets."

> "Before a Discovery schedule is run, the number of excluded IP addresses is totaled. If there are
> more than 500,000 excluded IP addresses, the Discovery is cancelled and an error is logged."

Exclude types: IP Address List / IP Address Range / IP Network.

---

## [S18] KB0726425 — CMDB Health duplicate metric algorithm
URL: https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB0726425

> "When CMDB Health - Correctness job runs, the Duplicate Metric only checks CIs that have
> Identification Rules defined, and also meet one of below conditions: One of the duplicated CIs has
> empty Discovery Source attribute; There is an active de-duplicate task (reconcile_duplicate_task)
> for the duplicated CI."

Case table: CI01 and CI02 both `Discovery Source: ServiceNow` → "not detected, unless there is a
deduplicate task"; CI01 ServiceNow + CI02 empty → "detected, empty changed to Duplicate, deduplicate
task created".

---

## [S19] KB3037828 — specific-attribute rule blocks higher-priority source
URL: https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB3037828

> "Per CMDB reconciliation rule precedence, a static reconciliation rule that explicitly lists specific
> attributes takes precedence over any rule that uses the 'Applies to all attributes' (empty
> Attributes field) configuration regardless of the relative priority order of the discovery sources
> involved."

In the reported case a *lower-priority* source's explicit attribute rule silently blocked a
higher-priority source's update.

---

## [S20] Create a CI identification rule
URL: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/t_CreateCIIdentificationRule.html

> "Identification rules are used to uniquely identify CIs in the CMDB, as part of Identification and
> Reconciliation (IRE) processes. Each CMDB class can be associated with a single identification rule."

> "You can update a CI identification rule only at the class level that the rule is defined for. You
> can't update a derived rule."

> "If there are still multiple matches, selects the oldest created CI as the final match."

> "Allow null attribute | When selected, then if at least one criterion attribute…"

Field descriptions include Independent/Dependent ("To set the rule as Dependent, you must specify
dependent relationship rules for the selected class").

---

## [S21] Discovery Admin Workspace — create IP-based schedule
URL: https://www.servicenow.com/docs/r/it-operations-management/discovery/t-dawCreateNewDiscoSchedule.html

> "Navigate to Workspaces > Discovery Admin Workspace > Schedules. Select New Discovery … Select
> IP-based discovery … Use existing IP range set (recommended) …"
> "Role required: discovery_admin"

---

## [S22] Getting started with credentials
URL: https://www.servicenow.com/docs/r/yokohama/platform-security/connections-and-credentials/credentials-getting-started.html

> "The MID Server in ServiceNow uses credentials stored in the Credentials [discoverycredentials]
> table to access and manage resources for Discovery, Orchestration, Service Mapping, and Cloud
> Management."

> "By default, Windows MID Servers use the login credentials of the MID Server service on the host
> machine to discover Windows devices in the network. You should Configure Windows MID Server service
> credentials so that they have at least local administrator privileges."

> "For Linux and UNIX machines and network devices, the MID Server uses the SSH and SNMP credentials
> configured in the instance in Discovery > Credentials."

> "The credentials are decrypted on the MID Server with the MID Server's private key."

> "Credential Order and Affinity … For Discovery, aliases help filter credentials, assign multiple
> aliases to schedules, and prevent inappropriate credential affinities."

---

## [S23] Create a data refresh rule
URL: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/create-datasource-staleness-rule.html
Release label: Brazil · updated 2026-10-21

> "Specify data refresh rules to determine if a CI is stale for a specific discovery source. Such CIs
> can then be updated by a lower-priority authorized discovery source."

> "Data refresh rules are used in conjunction with static reconciliation rules to determine
> reconciliation steps for a CI. These rules determine if, when, and by which discovery source a CI
> can be updated. The precedence order of applying reconciliation rules to a class, remains the same
> even when there are data refresh rules for that same class."

> "Data refresh rules have no impact when dynamic reconciliation rules are in effect."

Procedure: `All > Configuration > CI Class Manager` → `Hierarchy` → select class → `Class Info` →
`Reconciliation Rules` → `Data Refresh Rules` section → `Add`.

Fields: `Discovery source` ("Discovery source for which staleness is evaluated"), `Effective Duration`
("The time period that is used for the staleness test. If the fields specified in the static
reconciliation rule for the CI's class weren't updated by Discovery source within the specified
Effective Duration — the CI is determined to be stale for" …).

Role: `sn_cmdb_editor` and `itil` read access; `sn_cmdb_admin` / `itil_admin` full access.

---

## [S24] Create an IRE data source rule
URL: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/create-ire-data-source-rule.html
Release label: Brazil · 2026-09-10

> "When using Identification and Reconciliation Engine (IRE), you can prevent a specific discovery
> (data) source from inserting new CIs for a specific class. Create IRE data source rules for
> discovery sources that you don't trust in creating CIs but continue to trust in updating those CIs
> that exist."

> "IRE data source rules are stored in the IRE Data Source Rule [cmdb_ire_data_source_rule] table."

> "Child classes derive IRE data source rules from parent classes like identification rules do."

> "When IRE processes an insert operation that is prohibited by an IRE data source rule, the insert
> operation fails."

> "IRE data source rules do not apply to lookup and related items, and only a single rule can be
> active for any class/discovery source pair."

Path: `All > Configuration > Identification/Reconciliation > IRE Data Source Rule`. Fields: `Applies to`,
`Data source`, `Insert Not Allowed`. Example given: "an IP scan tool that discovers network gear but
does not discover servers and therefore creates server CIs without details."

---

## [S25] Reconciliation for non-CMDB tables — lower-priority acceptance conditions
URL: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/create-reconciliation-rule-non-cmdb.html
Release label: Brazil · 2026-09-10

> "If multiple data sources are authorized to update the same attributes, assign a priority to each of
> these data sources. …, subsequent updates are accepted only from the same data source or from a data
> source with a higher priority. Updates from a data source with a lower priority are rejected, unless
> these two conditions are met: The lower priority source is the first source updating the record. The
> record became stale based on data refresh rules for the class."

> "During reconciliation, the information in the Data Source History table is considered along with
> the data refresh rules for the CI's class, to determine if a CI attribute is stale. A CI attribute is
> determined to be stale if it was not updated by the latest discovery source to update the CI, within
> a time period."

> "Information about the last discovery source that updates each attribute is stored in the Data Source
> History [cmdb_datasource_last_update] table, but only after enabling the reconciliation rule."

---

## [S26] IRE overview + IRE error messages
URLs:
https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/ire.html
https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/id-engine-error-messages.html

> "IRE uses identification rules, reconciliation rules, and IRE data source rules when processing
> incoming data before inserting that data to the CMDB."

> "Most recent discovery ( last_discovered ) is the timestamp of when the CI was last discovered."

> `INSERT_NOT_ALLOWED_FOR_SOURCE` — "Insert into [ xyz ] is blocked for data source [ abc ] by IRE data
> source rule" (Resolution: delete/update the rule, or wait for a permitted source to create the CI.)

---

## [S27] Data refresh rule for a non-CMDB table
URL: https://www.servicenow.com/docs/r/washingtondc/servicenow-platform/configuration-management-database-cmdb/create-non-cmdb-data-refresh-rule.html
Release label: Washington DC · 2024-02-01

> "enter cmdb_datasource_staleness.list to open the Data Source Staleness Definitions table"
> Fields: `Applies to`, `Data source`, `Effective Duration`. "Data refresh rules have no impact when
> dynamic reconciliation rules are in effect."

---

## [S28] Create a CMDB Health staleness rule
URL: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/t_CreateCMDBHealthStaleRule.html
Release label: Brazil · 2026-09-10

> "If the staleness metric is in effect, then staleness rules are used to determine the percentage of
> stale CIs in the CMDB. This sum is then aggregated into the correctness KPI."

> "The Discovery setting of certain types of CIs as stale takes precedence over a CMDB Health staleness
> rule defined for the CI."

> "Staleness rules are defined per class. If a rule isn't defined for a class, then the parent's rule is
> automatically" …

Path: `All > Configuration > CI Class Manager` → `Hierarchy` → class → `Health` → `Correctness` →
`Staleness Rule` tab. Field: `Effective Duration` (based on `sys_updated_on`).
