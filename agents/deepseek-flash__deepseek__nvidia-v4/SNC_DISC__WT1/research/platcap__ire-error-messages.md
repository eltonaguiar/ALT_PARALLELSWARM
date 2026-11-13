# IRE error messages

- Source: https://www.servicenow.com/docs/r/zurich/servicenow-platform/configuration-management-database-cmdb/id-engine-error-messages.html
- Release: Zurich
- Map: platcap

---

# IRE error messages

Summarize Summarized using AI This content was generated using new OpenAI-powered functionality. Results are provided on an as is basis and are not guaranteed to be accurate or complete. Summary of IRE Error Messages The Identification and Reconciliation Engine (IRE) generates various error messages that assist users in troubleshooting issues related to configuration item (CI) identification. These messages can appear in the Identification Logging pane and system logs, helping users identify and resolve problems during data processing. Show full answer Show less Key Features Key error messages include: IDENTIFICATIONRULEMISSING: Indicates a missing identification rule for a specified table. Ensure the rule is active. MISSINGMATCHINGATTRIBUTES: Missing required values in the payload; add necessary attributes for identification. INVALIDINPUTDATA: References invalid sysid in the payload. Validate and correct the sysid. DUPLICATEPAYLOADRECORDS: Identifies duplicate items in the payload. Remove duplicates to proceed. LOCKTIMEOUT: Indicates a failure to acquire a synchronization lock; consider adjusting the mutex expiration time. REQUIREDATTRIBUTEEMPTY: Missing mandatory fields in the payload. Ensure all required fields are populated. Key Outcomes By addressing these error messages, ServiceNow customers can: Ensure accurate identification and reconciliation of configuration items. Resolve data conflicts and inconsistencies that may hinder processing. Maintain system integrity by preventing duplicate records and invalid references. Enhance system efficiency through proper configuration and adherence to identification rules. It is essential to regularly review error messages and take corrective actions to optimize the performance of the IRE and ensure seamless data processing.
The Identification and Reconciliation Engine (IRE) generates the following errors and
 messages. Depending on settings, these messages appear in the Identification Logging pane and in
 the system logs.

For information about lookup-based CI identification and
 qualifier chains, see
Create a CI identification rule
.
Note:
IRE performs an initial verification of a payload before processing identification
 rules. If IRE detects any duplicate CIs based on any class identifiers, the payload is
 rejected and processing stops.
For information about CMDB Identification Payload error: "FAILED TRYING TO EXECUTE ON
 CONNECTION", see
CMDB Identification Payload error - "Insertion failed with error Error
 during insert of cmdb_ci...", where node logs show "FAILED TRYING TO EXECUTE ON
 CONNECTION" "Duplicate entry 'XXX' for key 'XXX'"
knowledge base
 article.

## Error- IDENTIFICATION_RULE_MISSING

Message Description and Resolution
Identity Rule Missing for table [ xyz ] Description: Identification rule is missing for a class. Resolution: Ensure that there is an identification rule for table [ xyz ],
 and that the rule is active.

## MISSING_MATCHING_ATTRIBUTES

Message Description and Resolution
In payload missing minimum set of input values for criterion (matching)
 attributes from identify rule for table [ xyz ]. Add these input values
 in payload item ' abc ' Description: Missing minimum set of values for criterion attributes for an identification
 rule. Resolution: In the payload, add minimum set of values for criterion attributes for CI Identifier for table [ xyz ]. Open the CI Class Manager , click Hierarchy and select the [ xyz ] class. Check the identification rule and the identifier entries for
 table [ xyz ].

## Error- NO_CLASS_NAME_FOR_INDEPENDENT_CI

Message Description and Resolution
Cannot have 'sys_class_name' as a key field in an Independent Identity Rule on
 ' xyz ' Description: The class attribute was added to the CI identifier which is not
 supported. Resolution: Remove the class attribute from CI Identifier for table
 [ xyz ].

## Error- IDENTIFICATION_RULE_FOR_LOOKUP_MISSING

Message Description and Resolution
Identity Rule for table [ xyz ] missing Lookup Rule for class
 [ abc ] Description: The payload has a lookup class name, but the corresponding lookup rule is missing. Resolution: Add lookup identifier entry with [Search on table] as [ abc ] for CI Identifier for table [ xyz ]. For more information about this error message, see Identification error "Identity Rule for table [cmdb_ci_table_name] missing Lookup Rule for class [table_name]" [KB0786444] .

## Error- IDENTIFICATION_RULE_FOR_RELATED_ITEM_MISSING

Message Description and Resolution
Identity Rule for table [ xyz ] missing Related Rule for class
 [ abc ] Description: The payload has a related class name, but the corresponding related rule is
 missing. Resolution: Add related entry with [Related table] as [ abc ] within CI
 Identifier for table [ xyz ].

## Error- NO_LOOKUP_RULES_FOR_DEPENDENT_CI

Message Description and Resolution
Cannot have Lookup Rule for a Dependent Identity Rule on
 ' xyz ' Description: Cannot have Lookup Rule for a Dependent Identity Rule. Resolution: Remove lookup identifier entry from dependent CI Identifier for table
 [ xyz ].

## Error- INVALID_INPUT_DATA

Message Description and Resolution
Found invalid sys_id in payload. No record with sys_id [ xyz ] exist in table [ abc ] or is a duplicate record with [duplicate_of] field set to a main CI Description: The payload has a reference to an invalid sys_id. Resolution: Remove the referenced sys_id, or provide a valid sys_id. In payload no data source exist. You need to provide choice value from choice
 field [discovery_source] in table [cmdb_ci] Description: In payload no data source exists. Resolution: In the payload, provide a valid choice value from choice field
 [discovery_source] from table [cmdb_ci]. In payload invalid data source [ xyz ] exist. You need to provide a
 valid choice value from field [discovery_source] in table [cmdb_ci] Description: The payload contains an invalid data source. Resolution: In the payload, provide a valid choice value from choice field
 [discovery_source] from table [cmdb_ci]. No such relationship with name [ xyz ] exist in table
 [cmdb_rel_type]. If out-of-box relationship for [ xyz ] has been removed
 or renamed, it should be restored Description: The payload is referencing a relationship that does not exist in the
 [cmdb_rel_type] table. Resolution: Verify that the reference to the relationship is accurate. Or, if it is a
 new relationship, add it to the [cmdb_rel_type] table. Or, If out-of-box
 relationship for [ xyz ] has been removed or renamed, restore
 it. Payload relations ' xyz ' has invalid parent record index:
 [ 0 ] Description: Payload references invalid parent indexes. Resolution: Check payload indexes and ensure that they are all valid. Payload relations ' xyz ' has invalid child record index:
 [ 0 ] Description: Payload references invalid child indexes. Resolution: Check payload indexes and ensure that they are all valid.

## Error- DUPLICATE_RELATIONSHIP_TYPES

Message Description and Resolution
Duplicate relationship type records exists with name [ xyz ] in
 table [cmdb_rel_type] having sys_ids: [ abc ] Description: There are duplicate records in the [rel_ci_type] table for the
 relationship. Resolution: Remove the duplicate records.

## Error- DUPLICATE_PAYLOAD_RECORDS

Message Description and Resolution
Found duplicate items in the payload (index 0 and 1 ),
 using className [ xyz ] and fields [ abc ]. Remove duplicate
 items from payload Description: The payload contains two items whose criterion attributes have identical
 values. Resolution: Remove one of the duplicate items.

## Error- LOCK_TIMEOUT

Message Description and Resolution
Failed to acquire synchronization lock for xyz Description: Failed to acquire the system mutex lock. Resolution: Increase the mutex expiration time by adding the system property glide.identification_engine.mutex_expiration_time and
 setting to an integer value that is greater than the default value (15
 min).

## Error- MULTIPLE_DUPLICATE_RECORDS

Message Description and Resolution
Found duplicate records in table [ xyz ] using fields
 [ abc ] Description: Found duplicate records in the specified table. Resolution: Fix the duplicate records found by the identification engine. Check
 de-duplication tasks for information about all duplicates.

## Error- REQUIRED_ATTRIBUTE_EMPTY

Message Description and Resolution
Missing mandatory field [ xyz ] in table [ abc ]. Add
 input value for mandatory field in payload Description: A required attribute is missing in the payload. Resolution: In the payload, add input value for mandatory field [ xyz ] in
 table [ abc ].

## Error- MISSING_DEPENDENCY

Message Description and Resolution
In payload no relations defined for dependent class [ xyz ] that
 matches any containment/hosting rules: [ abc ]. Add appropriate relations
 in payload for ' def ' Description: No relations defined for the dependent class that matches any of its
 metadata rules. Resolution: In payload add appropriate relations for dependent class [ xyz ]
 that matches any containment/hosting rules: [ abc ].

## Error- METADATA_RULE_MISSING

Message Description and Resolution
No containment or hosting rules defined for dependent class [ xyz ].
 Add containment/hosting rules for â abc ' Description: There are no containment or hosting rules defined for dependent class. Resolution: Add containment or hosting rules for dependent class
 [ xyz ].

## Error- MULTIPLE_DEPENDENCIES

Message Description and Resolution
Found multiple dependent relation items [ xyz ] and
 [ abc ] in payload Description: Multiple dependent relation items exist. Resolution: Remove one of the multiple dependent relation items [ xyz ] or
 [ abc ]. Multiple paths leading to the same destination: xyz -> abc Description: Multiple paths leading to the same destination. Resolution: Remove duplicate relationship/qualifier chains that might exists between xyz -> abc .

## Error- ABANDONED

Message Description and Resolution
Abandoning processing payload item ' xyz ', since its depends on
 payload item ' abc ' has errors Description: Dependent payload item has errors, so abandoning processing. Resolution: Resolve the error on the dependent payload item âabc'. Can't find matched record with sys_id [ xyz ] in table
 [ abc ] Description: Matched sys_id does not exist in the corresponding table. Resolution: Check in table [ abc ] whether matched record is a valid record
 based on input payload. Identification engine API got called recursively, aborting... Description: The Identification engine API was called recursively. Resolution: Avoid calling the Identification engine API recursively. Detected error while processing payload from xyz Description: Error occurred during processing payload. Resolution: Resolve all errors mentioned in the output payload from xyz . While processing relations encountered errors in payload item: xyz Description: Payload item has errors. Resolution: Resolve errors in payload item â xyz '. Error occurred during parsing input json payload: xyz Description: Error occurred during parsing JSON payload. Resolution: Ensure that input JSON payload has correct JSON format.

## Error- MULTI_MATCH

Message Description and Resolution
Duplicate dependent records found having relationship [ xyz ] with
 same CI (className:[ abc ], sysId:[ def ]) Description: Found duplicate dependent CIs. Resolution: Check de-duplication tasks for information about all duplicates, and then
 delete duplicate records. Found multiple relations between payload items: ' xyz ' and
 ' abc ' Description: Found multiple relations between payload items. Resolution: Check for duplicate relationship chains and qualifier chains that might
 exist. Found duplicate records in lookup table [ xyz ] using fields
 [ abc ] and reference field [ def ] Description: Found duplicate records in lookup table. Resolution: Check de-duplication tasks for information about all duplicates, and then
 delete duplicate records.

## Error- QUALIFICATION_LOOP

Message Description and Resolution
Qualification chain has loop that contains relation ' xyz ' Description: Qualification chain has a loop. Resolution: Remove the loop from the qualification chain with relation âxyz'.

## Error- TYPE_CONFLICT_IN_QUALIFICATION

Message Description and Resolution
Invalid payload, qualification chain has multiple possible paths for payload
 items: ' xyz ' and ' abc ' Description: Multiple qualification paths found. Resolution: Remove multiple possible qualification paths between items âxyzâ and
 âabc'.

## Error- RECLASSIFICATION_NOT_ALLOWED

Message Description and Resolution
CI Reclassification not allowed from class: [ xyz ] to
 [ abc ] Description: CI reclassification not allowed. Resolution: Check reclassification tasks for information about reclassification, and
 check if reclassification from class: [ xyz ] to [ abc ]
 is valid.

## Error- DUPLICATE_RELATED_PAYLOAD

Message Description and Resolution
Found duplicate Related items (0 and 1) in the payload index 1 using fields
 xyz Description: Duplicate Related items present. Resolution: Remove one of the duplicate related items present in the payload.

## Error- DUPLICATE_LOOKUP_PAYLOAD

Message Description and Resolution
Found duplicate Lookup items (0 and 1) in the payload index 1 using fields xyz Description: Duplicate lookup items present. Resolution: Remove one of the duplicate lookup items present in the payload.

## INSERT_NOT_ALLOWED_FOR_SOURCE

Message Description and Resolution
Insert into [ xyz ] is blocked for data source [ abc ] by
 IRE data source rule Description: An IRE data source
 rule is configured to prevent data source [ abc ] from
 inserting CIs of the [ xyz ] class. Resolution: Delete or update the appropriate IRE data source rule to let data source
 [ abc ] insert CIs of the [ xyz ] class. Or, wait for another permitted data source to create the same CI.
