# Duplicate CIs remediation

- Source: https://www.servicenow.com/docs/r/zurich/servicenow-platform/configuration-management-database-cmdb/de-duplication-tasks.html
- Release: Zurich
- Map: platcap

---

# Duplicate CIs remediation

Summarize Summarized using AI This content was generated using new OpenAI-powered functionality. Results are provided on an as is basis and are not guaranteed to be accurate or complete. Summary of Duplicate CIs remediation Duplicate Configuration Items (CIs) in the ServiceNow CMDB can degrade performance and data integrity. Regular detection and remediation of duplicates are essential to maintain a reliable CMDB. The Identification and Reconciliation Engine (IRE) detects duplicate CIs and groups them into de-duplication tasks for review and remediation. Users can also manually create de-duplication tasks when automatic detection does not occur. Show full answer Show less De-duplication Tasks and Remediation Options De-duplication Tasks: Contain details of duplicate sets including the list of duplicate CIs. These tasks enable review and selection of a main CI to retain. Bulk Remediation: Use the De-duplication dashboard and Template Library in CMDB Workspace to review and remediate multiple tasks consistently using preconfigured templates. Single Task Remediation: Use the Duplicate CI Remediator wizard to manually reconcile a single task by selecting a main CI and deciding how to merge attributes, relationships, and related items. Main CI and Attribute Management The main CI is the active CI retained after remediation, into which duplicate CIs are consolidated. The duplicateof attribute tracks references from duplicate CIs to the main CI. After remediation, all duplicates reference the main CI, whose own duplicateof attribute is empty. Users can choose which data from duplicates is merged or retain the main CI unchanged. Asset-related attributes are not merged as they are excluded from the default related items list. Tools and Dashboards De-duplication Dashboard: Enables bulk remediation with templates, providing operational insights and consistent application of remediation settings. De-duplication Template Library: Stores preconfigured remediation templates by CI class to apply consistent settings across multiple tasks. Duplicate CI Remediator: Wizard-driven tool for manual, detailed remediation of individual de-duplication tasks, supporting attribute and relationship reconciliation. Impact on Related Tables and Processes Change Requests linked to CIs in a state other than New have their Configuration Item field cleared if the CI is deleted during remediation. Change Requests in New state automatically update the CI to the main CI during remediation. Problem and incident tasks referencing duplicate CIs remain valid as the system merges the main CI. Special Scenarios and Limitations Large Duplicate Sets: Remediation options are limited for sets exceeding 1,000 but capped at 5,000 duplicates. Only recommended main CI selection is available, and reconciliation is restricted. Duplicate Serial Numbers: De-duplication tasks may appear for duplicate serial numbers, but relationship merges do not apply. Large Related Items Sets: Remediation may timeout; a restricted mode can be enabled via system property to continue processing by limiting related items. Attribute Restrictions: The duplicateof field is system-managed with enforced rules to prevent data integrity issues, such as preventing chains of duplicates or cross-domain references. Main CI Deletion: A main CI cannot be deleted without first disassociating or deleting all its duplicates. Configuration and Management Users can manage the default list of related items globally used during remediation to control what associated records are merged. System properties control how duplicates are processed during CMDB identification and remediation. CMDB Workspace provides a comprehensive experience to create templates, review tasks, and manage remediation efficiently. Practical Benefits for ServiceNow Customers By leveraging these tools and processes, ServiceNow customers can: Maintain CMDB integrity and performance by regularly identifying and consolidating duplicate CIs. Streamline remediation using bulk operations and templates for consistent results across their organization. Ensure related ITSM processes like change, incident, and problem management remain accurate and functional during CI consolidation. Handle large and complex duplicate scenarios with configurable thresholds and restricted remediation modes. Manage and customize remediation scope through default related items and property settings.
Duplicate CIs in the CMDB unnecessarily overload the system and interfere with the CMDB's integrity and reliability. It is therefore important to regularly use CMDB tools that detect and remediate duplicate CIs.

## De-duplication tasks

When Identification and Reconciliation Engine (IRE) processes detect duplicate CIs, IRE groups each set of duplicate CIs into a de-duplication task for review and remediation. De-duplication tasks provide details about the
 duplication, including a list of all the duplicate CIs in the set. Review the details of each duplicate CI in the task and the data that was used to determine that the CI is a duplicate. For more information about IRE processes
 that detect duplicate CIs and generate de-duplication tasks, see
Detecting duplicate CIs
.

Under some circumstances, IRE doesn't automatically generate de-duplication tasks for duplicate CIs. To still remediate the duplication in such case, you must create the de-duplication task manually. For information about when
 this happens and how to manually create a task, see
Manually create a de-duplication task
.

Remediation of a de-duplication task consolidates its set of duplicate CIs into a single CI, eliminating the duplication.

To process de-duplication tasks (automatically-generated by IRE or manually created) to remediate duplicate CIs:
- In bulk: Use the De-duplication dashboard and the De-duplication Template Library in CMDB Workspace to: Review de-duplication tasks Remediate de-duplication tasks in bulk by using de-duplication templates Gain insights into de-duplication counts and status in your organization Access the CI de-duplication experience in CMDB Workspace to create de-duplication templates that remediate similar de-duplication tasks in bulk.
- A single task: Review de-duplication tasks (manual) and use the Duplicate CI Remediator wizard to process a single de-duplication task.

## Main CI

The
main CI
plays a key role in the remediation of duplicate CIs.
The main CI is one of the duplicate CIs that you want to retain as an active CI after reconciling the rest of the duplicate CIs into that main
 CI. You can then potentially retire or delete the rest of the duplicate CIs, or assign custom values to their attributes.
The first step during remediation is to select a main CI for the remediation process.
During remediation, you choose which attribute values, relationships, and related items from the duplicate CIs to reconcile into the main CI.
Alternatively, you can choose not to consolidate any data and retain the main
 CI as it is.

The
duplicate_of
attribute in duplicate CIs, is used to store a reference to the main CI. For duplicate CIs which existed in an instance that was upgraded to the
New York
release or later, the main CI is unknown. After upgrade,
duplicate_of
for those duplicate CIs is set to 'Unknown', indicating that the CI is a duplicate but the main CI is
 unknown.

Before remediation, the CIs in a duplicate CIs set are all duplicates of each other. After remediation, a set of duplicate CIs consists of one main CI, and any number of CIs, each considered a duplicate of the main CI. The
duplicate_of
attribute of the main CI is empty. The
duplicate_of
attribute for all the rest of the duplicate CIs in the set, is a reference to the main CI of the set.

## Default related items list

A list of related items that is used globally in the remediation of duplicate CIs, with all de-duplication tasks. During remediation, all items from the default related items list are selected by default to be merged to the main
 CI. During remediation, adding or removing related items to be merged doesn't affect the default related items list. See
Manage default related items list
for more information.
Note:
- Merging of attributes and related items that are associated with assets is not supported. Asset related tables are not included in the default related items list and therefore they are not available for merge.
- If a scenario involves an inactive change request, the Configuration item field on the Change Request form is cleared. If the current value is a duplicate CI, then it isnât merged with the main
 CI.

## De-duplication dashboard

CMDB Workspace
and
provide a de-duplication remediation solution letting you remediate de-duplication tasks, in bulk. The De-duplication dashboard, and the de-duplication templates and libraries, let you
 remediate multiple de-duplication tasks, consistently, in a single operation. The De-duplication Template Library in CMDB Workspace lets you create a preconfigured de-duplication template with the remediation settings for a
 class. The De-duplication dashboard in CMDB Workspace lets you then run the preconfigured template on multiple de-duplication tasks for the class that is set in the template. The remediation settings in the template, are then
 consistently applied to the duplicate CIs of the de-duplication tasks, to remediate CI duplication.

For more information about remediating duplicate CIs in CMDB Workspace, see
CI de-duplication experience in CMDB Workspace
.

## Duplicate CI Remediator

A de-duplication remediation tool, that is wizard-like and that lets you reconcile a set of duplicate CIs associated with a single de-duplication task. You can choose one of the duplicate CIs to retain as an active CI, and then
 decide how to process the rest of the duplicate CIs. The Duplicate CI Remediator lets you set reconciliation options for attributes, relationships, and related items.

If
ServiceNow Otto
for CMDB is installed on the instance, then the Duplicate CI Remediator provides a remediation option that uses the De-duplication task resolution assistant skill. For information about
 setting up
ServiceNow Otto
, see
ServiceNow Otto for Configuration Management Database (CMDB)
.

For information about using the Duplicate CI Remediator, see
Remediate a de-duplication task (manual)
.

## Effects on related tables (such as change requests)

Remediation can potentially have the following effects on change requests:
- When a CI is associated with a change request whose state isnât New , then when duplicate CI remediation processes delete the CI, the CI is removed from the change request.
- When a CI is associated with a change request whose state is New , then when duplicate CI remediation processes delete the CI, the CI in the change request is updated to the main CI.
The business rule
Ready only CI when not New
prevents change requests that aren't in the New state, from getting updated. This behavior ensures the validity and the continued processing of a change
 request when change request CIs are affected by duplicate remediation processing.
When a CI is associated with a problem or an incident task, those tasks remain valid after duplicate CI
 remediation processes run as the system merges the main CI in those tasks even if the remediation processes deleted the associated CI.

## Properties that affect processing of duplicate CIs

During CMDB Identification, processing of sets of duplicate CIs is determined by:
- Property glide.identification_engine.skip_duplicates (true by default).
- Property glide.identification_engine.skip_duplicates.threshold (5 by default).
- Number of duplicate CIs in a set.
For information about how these properties affect the management of duplicate CIs, see
Detecting duplicate CIs
.

## Special remediation scenarios

There are a few special remediation scenarios in which the remediation of duplicate CIs behaves differently:

Large number of duplicate CIs
Support for reconciliation of duplicate CIs is limited when the number of duplicate CIs exceeds a certain threshold. This threshold is based on the value of the
glide.duplicate_ci_remediator.max.cis
property, which is 1,000 by default. You can update this property to increase the threshold. However, this threshold never exceeds 5,000, even if you set
 the property to a value greater than 5,000.

When the number of duplicate CIs for a de-duplication task exceeds the threshold, the options available in the wizard are limited:
- On the Select Main CI tab, only the Recommended list of main CIs appears, and only the Use Main CI option is available.
- Recommendations are based only on the oldest created, newest updated, and most recently discovered CIs.
- Reconciliation of attribute conflicts and CI relationships is not supported, and only default related items are reconciled.
Duplicate serial numbers
Duplicate CI remediation is usually applied to duplicate CMDB CIs. However, in some situations de-duplication tasks might be created for duplicate serial numbers. When remediation is applied to duplicate serial
 numbers, the merge of relationships from duplicate records, is not referenced and is not applied.
Large number of related items
A de-duplication task might be associated with a large number of related items which might block the remediation process as loading the task times out. To continue the remediation process in this case, you can try
 running remediation in a restricted mode. Add the
glide.duplicate_ci_remediator.enable_restricted_mode
system property, and set its value to
true
to show the
Use
 the Duplicate CI Remediator (Restricted Mode)
option in the Remediate dialog box. For more information about using this option to restrict the use of related items in de-duplication remediation and allow
 remediation to proceed, see
Using restricted mode within the Duplicate CI Remediator [KB1542272]
.

## Restrictions

IRE uses the
duplicate_of
field internally by populating it as part of the skip duplicate mechanism, and you should restrict manual updates of that field. For more details, see
Detecting duplicate CIs
.

If you do attempt to modify the value of
duplicate_of
directly on a CI form or by using a script, the following restrictions are enforced to ensure data integrity:
- A CI cannot be its own main CI (you cannot set a CI as a duplicate of itself).
- A CI and its main CI cannot be from different domains.
- The duplicate_of attribute of the main CI cannot reference any CI as its main CI (you cannot set a CI as a duplicate of another duplicate CI to create a chain of duplicate CIs). If you attempt to set a CI as a duplicate of another duplicate CI, then the CI is set as a duplicate of the main CI of the duplicate CI you are trying to set. If the main CI of the duplicate CI you are trying to
 set is 'Unknown', the operation fails. Table 1. Example: Attempt to set a CI as duplicate of another duplicate CI CIs Attempted setting Result (System enforced) CI1: duplicate_of = empty CI2: duplicate_of = CI3 CI3: Main CI CI1: duplicate_of = CI2 CI1: duplicate_of = CI3 CI2: duplicate_of = CI3 CI3: Main CI If CI2 is a duplicate of 'Unknown', the operation fails. If a main CI becomes a duplicate of another CI, then it can no longer be a main CI. All CIs that were duplicates of that main CI are set as duplicates of the new main CI. Table 2. Example: Attempt to set a main CI as duplicate of another CI CIs Attempted setting Result (System enforced) CI1: duplicate_of = CI4 CI2: duplicate_of = CI4 CI3: duplicate_of = CI4 CI4: Main CI CI5: duplicate_of = empty CI4: duplicate_of = CI5 CI1: duplicate_of = CI5 CI2: duplicate_of = CI5 CI3: duplicate_of = CI5 CI4: duplicate_of = CI5 CI5: Main CI If a main CI becomes a duplicate of a CI within the same duplicate CI set, then the selected duplicate becomes the main CI in the duplicate CI set. The rest of the duplicate CIs in the set are set as duplicates of
 the new main CI. Table 3. Example: Attempt to set a main CI as duplicate of a CI within the duplicate CIs set CIs Attempted setting Result (System enforced) CI1: duplicate_of = CI4 CI2: duplicate_of = CI4 CI3: duplicate_of = CI4 CI4: Main CI CI4: duplicate_of = CI1 CI1: Main CI CI2: duplicate_of = CI1 CI3: duplicate_of = CI1 CI4: duplicate_of = CI1
- You can't delete a CI that is the main CI for a set of duplicate CIs. To delete a main CI, you must first disassociate that main CI with all of its duplicate CIs. Either delete all duplicate CIs that are associated with
 that main CI, or remove the reference to that main CI from all duplicate_of attributes in any duplicate CIs that have it.
