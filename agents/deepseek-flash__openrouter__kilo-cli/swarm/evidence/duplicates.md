

[S1] Identification rules
SOURCE: ServiceNow docs Brazil / identification-rules

Identification rules
Release version: Brazil
Updated September 10, 2026
6 minutes to read
The CMDB identification process relies on identification rules to uniquely identify CIs.
An identification rule applies to a CI class and consists of a single CI
identifier and one or more identifier entries and related
entries , each with a different priority. Each identifier entry defines a unique
attribute set with a specific priority and each related entry defines rules for identifying
related items. Create strong identification rules that are set with the highest priority for
the strongest identifier entries and related entries.
The identification process and identification rules use the CI's attributes for identification:
Unique attributes
Designated sets of criterion attribute values of a CI that can be used to uniquely identify the CI. Unique attributes can be from the same table or from derived tables.
Required attributes
Designated attributes of a CI that cannot be empty.
Derivation across the CMDB hierarchy
If no identification rule is explicitly defined for a child class, then the child class
derives its identification rule, including any associated identification entries and related
entries, from its parent class. Later, an own identification rule can be explicitly defined
for the child class. In that case, the identification rule that was initially derived from
the parent class, including any associated identification entries and related entries, is no
longer in effect at the child class. Also, you must explicitly add identification entries
and related entries in the newly created identification rule at the child class.
For example: The Hardware class identification rule has a related
entry for the Software Instance table. This identification rule,
including its associated related entry for the Software Instance table,
is derived by the Computer class. If you then create a new
identification rule for the Computer class, it overwrites the
identification rule that was derived from the Hardware class.
Therefore, the Hardware class identification rule, including its
associated related entry for the Software Instance table, is no longer
in effect for the Computer class. If the same related entry is needed,
you must explicitly add a related entry for the Software Instance table
in the newly created identification rule for the Computer class.
Identification rule types
CI dependency is specified in the CI Class Manager by the dependent relationship rules for the
CI's class:
Independent CIs
CIs, such as Server CIs, which exist on their own and are not dependent on any other
CIs.
Dependent CIs
CIs which depend on a relationship to another CI and can't exist on their own in the
absence of the dependent relationship. For example:
Network Adapter CIs can't exist meaningfully without the
Hardware CIs that contain them.
Application CIs can't exist on their own without the
Server CI they are hosted on.
The steps for identifying dependent CIs can be different from the steps for identifying
independent CIs. This difference is reflected in the differences between dependent
identification rules and independent identification rules:
Independent identification rule
A rule that identifies a CI based on the CI's own attributes, independently of other
CIs or relationship.
Dependent identification rule
A rule in which identifying a CI requires identifying a depe

[S2] Detecting duplicate CIs
SOURCE: ServiceNow docs Brazil / detect-duplicate-ci

Detecting duplicate CIs
Release version: Brazil
Updated September 10, 2026
7 minutes to read
When IRE identification process detects duplicate CIs, it groups each set of duplicate CIs into a de-duplication task for review and remediation. A large number of duplicate CIs might be due to weak identification rules. You
can configure the identification engine to reconcile duplicate CIs.
During Identification and Reconciliation Engine (IRE) processes, handling of duplicate CIs is determined by the properties glide.identification_engine.skip_duplicates (set to true by default) and
glide.identification_engine.skip_duplicates.threshold (set to 5 by default), and on the number of duplicate CIs that are detected. You can configure these properties so that duplicate CIs are
automatically reconciled, skipping duplication.
If glide.identification_engine.skip_duplicates is true, and the number of duplicate CIs is less than the threshold specified by
glide.identification_engine.skip_duplicates.threshold , then the oldest of the duplicate CIs is picked as a match and gets updated. That oldest duplicate CI also becomes the main CI for
that set of duplicate CIs. The rest of the duplicate CIs are tagged as duplicates by setting their duplicate_of attribute to the appropriate main CI. During matching, IRE filters out any CI that is
tagged as duplicate of any CI.
If glide.identification_engine.skip_duplicates is false, then matching
of duplicate CIs fails with an error, and none of the duplicate CIs are updated.
Also, the glide.duplicate_ci_remediator.max.cis property determines de-duplication processing for a large number of duplicate CIs. For more information, see the 'Large number of duplicate CIs' section in the Duplicate CIs remediation topic.
In either case, de-duplication tasks are always created.
Note: For a duplicate CI, if any of the CI's attributes, other than
duplicate_of , is updated by IRE processing, then the CI is no longer
considered a duplicate CI. In that situation, the value of duplicate_of is
cleared in the CI.
For more information about these properties, see Properties for Identification and Reconciliation .
Detecting duplicate CIs in related and lookup tables
During CI identification, IRE might detect duplicate lookup items (Serial Number [cmdb_serial_number] table), or duplicate related items (Software Instance [cmdb_software_instance] table). By default, IRE doesn't create
de-duplication tasks for these duplicate items. However, you can modify this default behavior by configuring IRE to generate de-duplication tasks for specific lookup or related tables, allowing you to then remediate any
duplications.
Add entries in the CMDB Deduplication Task Lookup or Related item allowed classes [cmdb_duplicate_lookup_related_allowed_class] configuration table for each table for which you want IRE to generate de-duplication tasks during identification:
Add an entry for any lookup table in an identifier entry in the respective identification rule.
Add an entry for any related table in a related entry in the respective identification rule.
In the base system, this configuration table has no records, in which case IRE doesn’t generate de-duplication tasks for any duplications in lookup or related tables from the identification rule. When detecting duplication
in related or lookup tables, IRE will generate de-duplication tasks only for those tables with an active entry in the configuration table:
Ensure that you have the required role for the cmdb_duplicate_lookup_related_allowed_class table.
To add or update records: sn_cmdb_admin, cmdb_dedup_admin, or itil_admin
To read or create reports: sn_cmdb_editor, sn_cmdb_admin, itil, itil_admin, cmdb_dedup_admin
In the navigation filter, enter cmdb_duplicate_lookup_related_allowed_class.list .
Select New and fill out the CMDB Deduplication Task Lookup or Related item allowed classes table form.
[TABLE]
Field |
Description |
Active |
Is the entry active. |
Lookup or related item class |
The lookup table (such as Serial Number [cmdb_serial_number]) or related table (such as Software Instance [cmdb_software_instance]) for which you want IRE to create de-duplication tasks when detecting
duplicate

[S3] Duplicate CIs remediation
SOURCE: ServiceNow docs Brazil / dedup-remediation

Duplicate CIs remediation
Release version: Brazil
Updated September 10, 2026
10 minutes to read
Duplicate CIs in the CMDB unnecessarily overload the system and interfere with the CMDB's integrity and reliability. It is therefore important to regularly use CMDB tools that detect and remediate duplicate CIs.
De-duplication tasks
When Identification and Reconciliation Engine (IRE) processes detect duplicate CIs, IRE groups each set of duplicate CIs into a de-duplication task for review and remediation. De-duplication tasks provide details
about the duplication, including a list of all the duplicate CIs in the set. Review the details of each duplicate CI in the task and the data that was used to determine that the CI is a duplicate. For more information about IRE
processes that detect duplicate CIs and generate de-duplication tasks, see Detecting duplicate CIs .
Under some circumstances, IRE doesn't automatically generate de-duplication tasks for duplicate CIs. To still remediate the duplication in such case, you must create the de-duplication task manually. For information about when
this happens and how to manually create a task, see Manually create a de-duplication task .
Remediation of a de-duplication task consolidates its set of duplicate CIs into a single CI, eliminating the duplication.
To process de-duplication tasks (automatically-generated by IRE or manually created) to remediate duplicate CIs:
In bulk: Use the De-duplication Dashboard, De-duplication Template Library, and the entire CI de-duplication experience in CMDB Workspace to:
Create de-duplication templates that process similar de-duplication tasks in bulk
Review de-duplication tasks
Process de-duplication tasks in bulk by using de-duplication templates
Gain insights into de-duplication counts and status in your organization
A single task: Review de-duplication tasks (manual) and use the Duplicate CI Remediator wizard to process a single de-duplication task.
Main CI
The main CI plays a key role in the remediation of duplicate CIs. The main CI is one of the duplicate CIs that you want to retain as an active CI after reconciling the rest of the duplicate CIs into that main
CI. You can then potentially retire or delete the rest of the duplicate CIs, or assign custom values to their attributes.
The first step during remediation is to select a main CI for the remediation process.
During remediation, you choose which attribute values, relationships, and related items from the duplicate CIs to reconcile into the main CI. Alternatively, you can choose not to consolidate any data and retain the main
CI as it is.
The duplicate_of attribute in duplicate CIs, is used to store a reference to the main CI. For duplicate CIs which existed in an instance that was upgraded to the New York release or later, the main CI is unknown. After upgrade, duplicate_of for those duplicate CIs is set to 'Unknown', indicating that the CI is a duplicate but the main CI is
unknown.
Before remediation, the CIs in a duplicate CIs set are all duplicates of each other. After remediation, a set of duplicate CIs consists of one main CI, and any number of CIs, each considered a duplicate of the main CI. The
duplicate_of attribute of the main CI is empty. The duplicate_of attribute for all the rest of the duplicate CIs in the set, is a reference to the main CI of the set.
Default related items list
A list of related items that is used globally in the remediation of duplicate CIs, with all de-duplication tasks. During remediation, all items from the default related items list are selected by default to be merged

[S4] Reconciliation rules
SOURCE: ServiceNow docs Brazil / reconciliation-rules

Reconciliation rules
Release version: Brazil
Updated September 10, 2026
5 minutes to read
Reconciliation rules determine which discovery
sources can update CI attributes.
Discovery sources, such as EventManagement, ImportSet, ManualEntry, and Tivoli, are used
with the createOrUpdateCI() API to simulate manual updates to CIs.
Without reconciliation rules, discovery sources can overwrite each other's updates to
attribute values.
There are two types of reconciliation rules:
Static reconciliation rules
Static reconciliation rules are the legacy reconciliation rules that set priorities
for the various discovery sources for updating CI attributes. Static reconciliation
rules specify which discovery sources can update class attributes, and the
precedence order among these discovery sources.
When creating static reconciliation rules, ensure that there is a reconciliation
rule for each discovery source that is authorized to update an attribute.
Reconciliation rules can be defined at the parent and the child class level.
Static reconciliation rules are stored in the Reconciliation Definition
[cmdb_reconciliation_definition] table.
Dynamic reconciliation rules
Dynamic reconciliation rules are based on attribute values processed by CMDB 360 rather than on discovery source
priority. First, CMDB 360 processes the current payload data into the CMDB 360 data
store. Then, applying a dynamic reconciliation rule, IRE selects the largest or most
reported value, for example, across all discovery sources. Because dynamic
reconciliation rules leverage CMDB 360, you must enable that feature to use dynamic
reconciliation rules.
Creating dynamic reconciliation rules can be useful, for example, if it becomes
difficult to set priority order for multiple discovery sources. Only a single
dynamic reconciliation rule can exist per class attribute.
Dynamic reconciliation rules are stored in the Dynamic Reconciliation Definitions
[cmdb_dynamic_reconciliation_definition] table.
Examples of static reconciliation rules
The following sample static reconciliation rules are created for the
cmdb_ci_computer class and its
cmdb_ci_linux_server child class:
Discovery is exclusively authorized to update the name attribute
in the cmdb_ci_computer class. Because reconciliation rules are
derived by child classes from parent classes, this rule also authorizes Discovery to
update the name attribute in any child classes for the
cmdb_ci_computer class.
ServiceWatch is exclusively authorized to update the name
attribute in the cmdb_ci_linux_server class.
ServiceWatch is exclusively authorized to update all

[S5] General guidelines for using CMDB Identification
SOURCE: ServiceNow docs Brazil / id-best-practices

General guidelines for using CMDB Identification
Release version: Brazil
Updated September 10, 2026
3 minutes to read
Review the following general guidelines for using CMDB Identification effectively.
Identification rules
An independent identification rule identifies a CI based on the CI's attributes,
independently of other CIs.
A dependent identification rule identifies a CI by its dependent CIs and
the relationships of the identified CI with those dependent CIs. Identification with
a dependent identification rule is based on the dependent CIs and the relationships
and qualifiers between the identified CI and its dependent CIs. Identification then
requires more time than with an independent identification rule and is prone to some
identification errors. Usage of dependent rules should therefore be minimized.
CI modeling determines which type of identification rules are required for proper CI
identification.
Create identification rules using the following order of importance:
Independent identification rules — It is always preferable to create
independent identification rules rather than dependent identification rules.
When you model a CI, define the CI with a complete set of attributes that
lend themselves to independent identification, eliminating the need to use
additional CIs for identification.
Dependent identification rules — If it is necessary to create dependent
identification rules, then define a single level of dependency. Two is the
maximum number of dependency levels that is supported.
Avoid creating lookup identifier entries. The use of lookup identifier entry
is highly discouraged as it can reduce performance. If unavoidable, ensure
to first review class definitions and consider updates that allow usage of
independent identification rules.
Limit the number of identifier entries within an identification rule,
ideally to 1. A second identifier entry can further reduce performance, as
will each additional identifier entry.
Create strong identification rules in which the strongest identifier entries
and related entries are set with the highest priority.
Ensure that the identification rule is at the class level that it needs to
be.
Payload
Create the pa