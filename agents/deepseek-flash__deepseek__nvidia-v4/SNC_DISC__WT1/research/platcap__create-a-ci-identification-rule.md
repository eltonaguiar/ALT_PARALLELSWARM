# Create a CI identification rule

- Source: https://www.servicenow.com/docs/r/zurich/servicenow-platform/configuration-management-database-cmdb/t_CreateCIIdentificationRule.html
- Release: Zurich
- Map: platcap

---

# Create a CI identification rule

Identification rules are used to uniquely identify CIs in the CMDB, as part of Identification and Reconciliation (IRE) processes.
Each CMDB class can be associated with a single identification rule.

## Before you begin

You can update a CI identification rule only at the class level that the rule is defined for. You can't update a derived rule.

Role required: itil has read access, itil_admin (on top of itil) has full access.

## About this task

In a CI identification rule, specify a CI identifier, and identifier entries and related entries that uniquely identify the CI.

Review the following before creating identification rules:
- Identification rules
- General guidelines for using CMDB Identification
- Explore predefined identification rules: Navigate to All > CI Class Manager . Select Hierarchy and then search and select, for example, the Hardware class. In the Hardware bar, expand Class Info and select Identification Rule . Examine all the sections and tiles with the settings of the Hardware class identification rule.

## Procedure

- Navigate to All > Configuration > CI Class Manager .
- Select Hierarchy to show the CI Classes list and then select the class for which to create an identification rule.
- In the class navigation bar, expand Class Info and then select Identification Rule .
- Select Edit , Add , or Replace (for a class that has derived the CI identification rule), in the Identification Rule section to create one.
- Fill out the form, and then select Save . Field Description Independent/Dependent Designation of whether the CI identifier can identify the CI independently of other CIs, or not. Note: To set the rule as Dependent , you must specify dependent relationship rules for the selected class. Name Name of CI identifier. Description Description of the CI identifier.
- In the Identifier Entries section, select an existing identifier entry to edit, or select Add to create one.
- In the Identifier Entry dialog box, choose an option and then select Next . Continue with one of the following three steps according to the option you selected: Option Description Use attributes from main table <table> Lets you select attributes from the currently selected table (regular identifier entry). Use attributes from another table (Lookup table) Lets you select attributes from any related table, other than the currently selected table (lookup identifier entry). Use attributes from main and another table (Hybrid) Lets you select attributes from both the currently selected table, and from another table (hybrid identifier entry).
- Use attributes from main table <'table'> option: Set the options on the form and then select Save . Search On Table is preset to the currently selected table in the CI Classes list. Field Description Active Check box that specifies the identifier entry is active. At least one identifier entry in an identification rule must be active for the rule to apply. Priority Priority of the identifier entry. Identifier entries are applied based on priority. Rules with lower priority numbers are given higher priority. Identifier entries of identical priorities are applied
 randomly. You can keep gaps between the priority numbers, so you can assign the unused priority numbers to new entries without modifying the existing priority order. Criterion Attributes Set of attributes that uniquely identify the CI. Attributes can belong to the current class, or to a parent class. Note: It is possible to add reference fields as a criterion attribute. However, such
 fields might not always be effective: Reference fields store sys_id s that point to a record in another table, and thus is considered a weak criterion attribute (in terms of uniqueness) for the current table. The system detects and then replaces invalid values in a reference field with 'Unknown'. For example, an invalid Model ID value is replaced with the value 'Unknown'. Also, if
 several CIs end up having that same reference field set to 'Unknown', then these CIs become duplicate CIs. Allow null attribute When selected, then if at least one criterion attribute is not null, attempt matching with an identifier entry even if there are criterion attributes that are null. Otherwise, all criterion attributes must have values to attempt matching with an identifier entry. Allow fallback to parent's rules Allows the identification rules of the CI's parent to be used if a match is not found for this identification rule. Applies only for dependent identification rules. Advanced Options A filter to narrow the set of records that will be searched for a matching CI. Available only if the glide.identification_engine.enable_identifier_optional_condition system property is set to true ( false by default).
 In the base system, identifier entries of various classes are pre-configured with advanced options conditions. All these pre-configured conditions in regular identifier entries will automatically apply
 when you set this property to true . Therefore, to prevent unexpected behavior, review those predefined conditions in regular identifier entries before setting this property to true . For more details about this property, see Properties . Note: If criterion attributes have only two attributes and sys_class_name is one of them (for example [name, sys_class_name], [ip_address, sys_class_name]), then the other attribute cannot be NULL, even
 if Allow null attribute is enabled. This restriction is due to sys_class_name being considered a special system matching attribute.
- Use attributes from another table (Lookup table) option: Set Search On Table to a table other than the currently selected table in the CI Classes list. The Search On Table must have a reference field to cmdb_ci , otherwise the identifier entry is considered invalid. Set the rest of the fields as described in the previous step. Optional: Select Advanced options and enter the information for a lookup identifier (scroll down if necessary). Advanced Option Description All of these conditions must be met A filter to narrow the set of records that will be searched for a matching CI. Enforce exact count match For lookup identification, match a CI only on exact lookup records count match. When enforced, all lookup items for a CI in the payload must have matching records in the lookup table, that reference
 the same CI: Only matches CIs that have all the lookup items from the input payload referencing the CI in CMDB. If there are multiple matches, selects the oldest created CI as the final match. When not enforced, one lookup item for a CI in the payload matching a record in the lookup table, is sufficient to consider a match: Matches any CI that has at least one of the lookup items from the input payload referencing the CI in CMDB. If there are multiple matches, selects the CIs with the max number of lookup items from the input payload referencing the CI in CMDB. If there are still multiple matches, selects the oldest created CI as the final match. Select Save .
- Use attributes from main and another table (Hybrid) option: Set the options on the General Settings tab as described in previous steps, and then select Next . On the Main Table Settings tab, select the attributes to use from the currently selected table, and then select Next . Search On Table is preset to the currently selected table in the CI Classes list. On the Lookup Table Settings tab, select a Search On Table and then in Criterion Attributes select attributes from the specified table. Search On Table must have a reference field to cmdb_ci , otherwise the identifier entry is considered invalid. You can select Advanced options and enter the information for a lookup identifier as described in the previous step (scroll down if necessary). Select Save . Note: The Allow null attribute option in the hybrid option, is set to false . Therefore, all of the selected criterion attributes from both the currently selected table and the
 lookup table, must have a value. Also, setting optional conditions is available only for the lookup table, and is not available for the main table.
- Optional: On the Related Entries section select an existing related entry to edit, or select Add to create one. Update the Related Entry form and then select Save . Table 1. Related Entry form Field Description Active Check box that specifies that the related entry is
 active. Related table A related table that references the CI that is being
 matched. Referenced field A referenced field in Related table that should store the referenced CI. This field always
 references the cmdb_ci table, or a descendent of the cmdb_ci
 table. Priority Priority of the related entry for the specified Related table . Rules with lower
 priority numbers are given higher priority while matching a
 related item for specific related table. Related entries for the
 specified related table with identical priorities are applied
 randomly. You can keep gaps between the priority numbers,
 so you can assign the unused priority numbers to new entries
 without modifying the existing priority order. Criterion attributes The set of attributes to uniquely identify the related item. Attributes can belong to the current class, or to a parent class. Note: It is possible to add reference fields as a criterion attribute. However,
 such fields might not always be effective: Reference fields store sys_id s that point to a record in another table, and thus is considered a weak criterion attribute (in terms of uniqueness) for the current table. The system detects and then replaces invalid values in a reference field with 'Unknown'. For example, an invalid Model ID value is replaced with the value 'Unknown'. Also, if several
 CIs end up having that same reference field set to 'Unknown', then these CIs become duplicate CIs. Select the lock icon to view, add, or remove attributes from the identification rule. Allow null attribute If at least one criterion attribute in the related table is not null, matching with an identifier entry is attempted even when other criterion attributes are null. Filter conditions Add conditions to construct a filter to narrow the set of
 records that will be searched for a matching related
 item. Note: If criterion attributes have only two attributes and sys_class_name is one of them (for example [name, sys_class_name], [ip_address, sys_class_name]), then the other attribute cannot be
 NULL, even if Allow null attribute is enabled. This restriction is due to sys_class_name being considered a special system matching attribute.

## Example

For example, the pre-defined
Hardware Rule
applies to the Hardware [cmdb_ci_hardware] table. It has an identifier entry with the criterion attribute
Serial Number, Serial Number Type
and its
Search on table
field is set to
Serial Number
.

The following payload snippet adds a CI to the
cmdb_ci_linux_server
class, that is a child of the
Hardware
class. It also shows how you can add related items in the payload for which you
 should create
Related Entries
on the CI Identifier page for the Hardware [cmdb_ci_hardware] table:

{
 "items": [
 {
 "className": "cmdb_ci_linux_server",
 "lookup": [
 {
 "className": "cmdb_serial_number",
 "values": {
 "serial_number": "VMware-42 21 e3 da 44 14 5a a6-56 48 2b 0a 28 53 42 4c",
 "serial_number_type": "system",
 "valid": "true"
 }
 },
 {
 "className": "cmdb_serial_number",
 "values": {
 "serial_number": "4221E3DA-4414-5AA6-5648-2B0A2853424C",
 "serial_number_type": "uuid",
 "valid": "true"
 }
 }, }
 ],

 ârelated": [
 {
 "className": "cmdb_ci_ucs_chassis",
 "values": {
 âname": âchassis1",
 âcategory": âcategory1",
 âshort_description": âMy Chassis 1"
 }
 },
 {
 "className": "cmdb_ci_ucs_chassis",
 "values": {
 âname": "chassis2",
 "category": "category2",
 "short_description": "My Chassis 2"
 }
 }, }
 ],

 "values": {
 ......
 "name": "xpolog2.lab3",
 "os_name": "Linux",
 "output": "Linux xpolog2.lab3 2.6.32-431.el6.x86_64 #1 SMP Fri Nov 22 03:15:09 UTC 2013 x86_64 x86_64 x86_64 GNU/Linux",
 "serial_number": "VMware-42 21 e3 da 44 14 5a a6-56 48 2b 0a 28 53 42 4c",
 "sys_class_name": "cmdb_ci_linux_server"
 }
 }
 ]
}
When the
Hardware Rule
is applied, the Serial Number [cmdb_serial_number] table is searched for a match with the values specified within the
lookup
key. Unless
Enforce exact
 count match (Lookup)
is checked, it is not necessary for every lookup key to return a match, as long as there is at least one match. If all matches reference the same CI, then that CI is considered to be the
 existing CI record. If no match is found, then the identification search continues to the next rule entry. If after all the rules are exhausted without finding a match, a new CI record is created in the database.

## What to do next

You can optionally
create an inclusion rule
to narrow the scope of CIs that are included in identification.
