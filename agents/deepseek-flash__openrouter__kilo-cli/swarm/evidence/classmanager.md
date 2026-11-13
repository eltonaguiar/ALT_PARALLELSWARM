

[S1] CI Class Manager
SOURCE: ServiceNow docs Brazil / ci-class-manager

CI Class Manager
Release version: Brazil
Updated September 10, 2026
1 minute to read
Use the CI Class Manager to centrally view, create, or edit basic class definitions, class settings for Identification and Reconciliation Engine (IRE), CMDB
Health, and manage some Service Mapping definitions.
Note: CI Class Manager doesn't support working with non-CMDB tables. For more details, see
IRE support for non-CMDB tables .
To access the CI Class Manager, navigate to All > Configuration > CI Class Manager . In general, the sn_cmdb_admin role has full access to all sections of the CI Class Manager and the sn_cmdb_editor user role has read access only.
Class basics
Create a class
View class basic information
View and edit class definitions and metadata
Add a suggested relationship
Show all CIs for a class
Create or modify Dependency Views map icons
Delete CIs
Update the list of classes in the Principal Class filter
CMDB Health
Create a compliance audit
Create a certification template
Create a CMDB Health orphan rule
Create a CMDB Health staleness rule
Set a CI field to be recommended
Set a CI attribute to be mandatory
Create health inclusion rule
IRE
Identification:
Create a CI identification rule
Create an identification inclusion rule
Reconciliation:
Create a CI reconciliation rule
Create a data refresh rule
Dependencies:
Create a dependent relationship rule for a CMDB class (hosting and containment)
Service Mapping
Entry point types for Service Mapping
CI types for Service Mapping and Discovery

[S2] Create a CI class
SOURCE: ServiceNow docs Brazil / create-ci-class

Create a CI class
Release version: Brazil
Updated September 10, 2026
3 minutes to read
Create a CI class (table) that is an extension of an existing CI class. Then create
identification and reconciliation rules for the new class.
Before you begin
The class that is being extended must have its
Is_Extendable field checked, indicating that the class is
extendable.
Role required:
sn_cmdb_admin or Itil_admin, and personalize_dictionary: Required for editing the dictionary table
sn_cmdb_admin or admin: Full access
About this task
The CI Class Manager is a centralized location for managing CMDB tables and for
creating a class that is derived from another CMDB class. Creating a class requires
basic details such as a label and a name. Identification and reconciliation rules
are also required to ensure that the class can be successfully identified by the
identification engine.
For more information about extending a class and how attributes are derived from a parent class in that process, see Table extension and classes .
Procedure
Navigate to All > Configuration > CI Class Manager .
Click Hierarchy to expand the CI Classes list.
Select the class that the new class is extended from.
Click Add Child Class .
The Add Child Class option appears only if the selected
class is extendable.
On the Provide Basic Info tab, fill out the information
and then click Next .
[TABLE]
Field |
Description |
Display name |
A unique label for the class (such as Laptops or Thin Clients). The label appears on list and form views for the class. Updating the Label field also updates the label record in the
language file for the current language. See Field Labels in Data dictionary tables . Maximum string length is 80 characters.
|
Table name |
Automatically populated based on the table label and the
prefix string
'u_cmdb_ci'.
You cannot modify the prefix; however, you can modify the
rest of the table name. The name can contain only
lowercase, alphanumeric ASCII characters and underscores
(_).
Maximum string length is 80 characters.
|
Description |
Explanation of the use purpose of the class. |
Icon |
The icon associated with the class. |
Extensible |
Indicator of whether this class can be extended. |
Principal Class |
Denotes whether this class is included in the Principal Class filter. If this class is included in the Principal Class filter, then CIs from this class appear in CI list views when the Principal Class filter is applied. |
[/TABLE]
On the Add Attributes tab, click the + sign and enter details for each new class column.
Click Next .
For description of the different columns in the list view, see Dictionary entry form . To designate an attribute as a CI identifier for class identification, double-click the attribute's Identification Rule column and set it to
true .
On the Set Identification Rule tab, examine the Derived identification rule and its Identifier Entries .
You can click Replace to replace the derived rule with a new identification rule and new identifier entries specific to the new class. See Identification rules for details about identification rules and identifier entries.
On the Dependencies tab, click Add
dependency to add dependent rules .
The Dependencies tab appears only if there are
dependent identification rules for the selected class.
On the Add Reconciliation Rules tab, click
Add to create the following rules:
Reconciliation Rules
Data Refresh
Rules
On the Add Suggested Relationships tab, review the diagram of the class derived suggested relationships.
Use the filter to display only inbound, outbound, or specific relationship types.
To add a suggested relationship for the class:
Click New .
In the Add Suggested Relationship dialog box, select a Relationship and a Target Class for the relationship. This Class and the Target
Class become parent or child in the suggested relationship, based on your selection of the Relationship .
Click Save .
When building relationships for the class in the Query Builder, the list of suggested relati

[S3] Create dependent relationship rules
SOURCE: ServiceNow docs Brazil / dependent-relationship-rules

Create dependent relationship rules
Release version: Brazil
Updated September 10, 2026
4 minutes to read
Create
hosting and containment rules (dependent relationship rules) for CI classes to help with correctly
identifying dependent CIs during the business discovery process and service mapping. Discovery calls the identification API that
applies dependent relationship rules.
You can create a basic hosting or containment rule in the CI Class Manager. Or, use the
Metadata Editor to create groups of hosting and containment rules, and inbound or outbound
endpoints in containment rules. The CI Class Manager and the Metadata Editor are synchronized,
and you can use each of those tools to display and edit a dependent rule.
Create a dependent relationship rule for a CMDB class
Use the CI Class Manager to create a basic dependent relationship rule (hosting or
containment relationship rule) for a CMDB class.
Before you begin
Role required: sn_cmdb_editor and itil have read access, sn_cmdb_admin and itil_admin have full access.
About this task
The class for which you create dependent relationship
rule, must have a dependent
identification rule .
Procedure
Navigate to All > Configuration > CI Class Manager .
Click Hierarchy to display the CI Classes list, and
select the class for which you want to create a hosting or a containment
rule.
In the class navigation bar, click Dependent
Relationships .
In the Dependent Relationships view, click Add
dependency .
Fill out the details in the Add Dependent Relationship Rule dialog box.
[TABLE]
Field |
Description |
Rule Type |
Designation of whether this rule is a hosting rule or a
containment rule. |
This Class |
The class that the rule applies to. |
Relationship |
The relationship type for the rule. |
Target Class |
The target class for the dependent relationship rule. The
designation of this class as a child or parent class, is
based on the specified
Relationship . |
[/TABLE]
Click Save .
What to do next
You can click Reset to derived and then confirm the operation to delete all dependent relationship rules that were added specifically for the selected class. Only dependent
relationships that are derived from a parent class, remain.
For more information about child and parent classes, see Table extension and classes .
Create or edit a collection of containment rules
Create containment rule for CIs to help with
correctly identifying dependent CIs during the business discovery process and service
mapping. Discovery calls the identification API that applies dependent relationship
rules.
Before you begin
Role required: sn_cmdb_admin or admin
About this task
A containment rule is a dependent relationship rule
which defines a relationship between two CIs, structured as: CIType1
RelationshipType CIType2. The first CI type that you add becomes the top level CI of
a containment rules group which is a chain of containment rules. The entire set of
containment rules is organized as groups according to top-level CIs.
To
create a containment rules group for a new CI type, you need to first add the CI
Type1 of the relationship. To add a child containment rule for a CI type that
exists, you need to select that CI type, and define the second portion of the
relationship rule which is the relationship type and CI Type2.
To each rule within a containment rules group you can add
inbound or outbound endpoints, which are noted by

[S4] Using identification simulation
SOURCE: ServiceNow docs Brazil / identification-simulation

Using identification simulation
Release version: Brazil
Updated September 10, 2026
6 minutes to read
Identification simulation is a central location for automatically constructing a payload that is guaranteed to be complete and valid. You can then simulate the processing of the payload by the Identification and Reconciliation
Engine (IRE) and examine the results before actually submitting it for execution by IRE.
Use identification simulation to construct an input payload, and simulate processing of the
payload by IRE. You can then examine the results, adjust identification rules if needed, and
re-run the simulation of the updated payload.
Use the identification simulation to:
Automatically construct input payload that is based on existing identification rules,
hosting and containment rules.
Simulate execution of a payload (automatically constructed by identification simulation, or
manually created).
Browse payload output and execution log messages for a simulated run.
Note:
Identification simulation does not commit any updates to the CMDB.
Identification simulation supports simulation of processing payloads that are provided and
which contain non-CMDB tables, but doesn't support the generation of such payloads.
Automatically generate payload
Use identification simulation to automatically construct an input payload for a
specified class. The constructed payload is complete with any required dependent CIs,
correctly structured, and syntactically valid for processing by the identification and
reconciliation engine (IRE).
Before you begin
Role required: sn_cmdb_admin or admin
About this task
The payload that is constructed during identification simulation is for the specified
class. For a dependent CI class, you will be prompted for information about all
dependencies. After you provide the required details, identification simulation
constructs the payload based on your input.
Note: Automatically generating payloads that contain non-CMDB tables, isn't
supported.
Procedure
Navigate to All > Configuration > Identification/Reconciliation , and click Identification
Simulation .
In the Start with CI Class box click
Start .
On the Payload Information form, in the Data
source field, select the data source that is associated with
this class update.
For the ServiceNow Discovery data source, select
ServiceNow .
Select the Class in the payload.
In the Criterion Attributes area select the CI
identifier attributes and then specify the values that uniquely identify
a CI.
In the Additional Attributes area specify
attributes and values that matching CIs will be updated with.
For dependent CIs associated with dependent identification rules, fill out the
Criterion Attributes and Additional
Attributes sections in all Container
level sections that display.
Click Generate Script .
If any errors indicate that there are missing fields, fill in the missing fields and then click Generate Script again.
What to do next
Click Run Simulation to simulate processing of the
payload by IRE.
Examine the results of the simulation, fine-tune the payload as needed, and
combine with other payloads for other classes as desired. After finalizing the
payload, use the createOrUpdateCI() API to execute the payload by
IRE which will result in actual updates to the CMDB.
Click Copy Script to copy the JSON script into the
clipboard. You can then paste that script into a third party softw

[S5] Components and process of IRE
SOURCE: ServiceNow docs Brazil / ire-components-process

Components and process of Identification and Reconciliation
Release version: Brazil
Updated September 10, 2026
3 minutes to read
The CMDB Identification and Reconciliation functionality is supported by the Identification and Reconciliation engine (IRE), rules, and tasks. Identification rules, reconciliation rules, IRE data
source rules, de-duplication tasks, and reclassification tasks determine how IRE identifies and reconciles CI.
Concepts and Components of Identification and Reconciliation
Identification
Process of uniquely identifying CIs, to determine if a CI already exists in the CMDB or if it is a newly discovered CI that must be added to the CMDB. Identification processes rely on identification rules , or on unique IDs for CIs that data sources can provide.
Reconciliation
Process of reconciling CIs and CI attributes by allowing only designated authoritative data sources to write to the CMDB at the CI table and attribute level. The CMDB is updated in real time as records are being processed. There is no staging area to verify the reconciliation activities before they are committed. Reconciliation processes
rely on reconciliation rules and IRE data source rules .
Reconciliation is required only for update operations, when the identification process identifies a CI in the CMDB that matches an incoming CI in the payload. When IRE inserts a new CI, reconciliation is not applied.
De-duplication tasks
If the instance encounters duplicate CIs during the Identification and Reconciliation
process, it groups each set of duplicate CIs into a de-duplication task . Review the
info