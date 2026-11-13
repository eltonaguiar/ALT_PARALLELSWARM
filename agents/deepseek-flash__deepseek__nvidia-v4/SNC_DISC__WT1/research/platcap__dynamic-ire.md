# Dynamic IRE

- Source: https://www.servicenow.com/docs/r/zurich/servicenow-platform/configuration-management-database-cmdb/dynamic-ire.html
- Release: Zurich
- Map: platcap

---

# Dynamic IRE

Summarize Summarized using AI This content was generated using new OpenAI-powered functionality. Results are provided on an as is basis and are not guaranteed to be accurate or complete. Summary of Dynamic IRE The Dynamic Identification and Reconciliation Engine (Dynamic IRE) is an advanced ServiceNow engine designed to improve the accuracy and efficiency of Configuration Item (CI) identification. Unlike the legacy Static IRE, which relies on manually created and maintained rules, Dynamic IRE uses automated algorithms that run in parallel to score and match CIs across multiple data sources. It is specifically applicable to the Hardware [cmdbcihardware] class and its descendants, with options to exclude certain subclasses when necessary. Show full answer Show less Key Features Automated Identification: Dynamic IRE automatically updates identification rules during data ingestion, eliminating the need for manual rule creation and maintenance. Improved Matching Accuracy: By evaluating a larger combination of CI attributes simultaneously, it reduces duplicate CIs and increases match precision compared to Static IRE. Modes of Operation: Simulation Mode: Runs Dynamic IRE alongside Static IRE to compare results and performance without impacting production data. Committed Mode: Dynamic IRE exclusively performs identification, fully replacing Static IRE. Class Exclusion: Administrators can exclude specific hardware subclasses from Dynamic IRE, allowing Static IRE to handle those when custom attributes or rules are required. Switching Flexibility: Customers can switch between Dynamic and Static IRE via system properties or the CI Class Manager, ensuring ease of transition and rollback if needed. Getting Started and Usage Recommendations Dynamic IRE is enabled by default on Zurich Patch 11 or later instances. For upgraded instances still using Static IRE, it is recommended to: Start in simulation mode on a non-production instance to test and compare performance and outcomes. Use the CI Class Manager to enable simulation, review comparison metrics like parity scores and CI operation differences, and examine detailed record-level comparisons. Once satisfied with simulation results, commit to Dynamic IRE in production for the Hardware class and its descendants. Use the system property glide.identificationengine.dynamicireenabled to toggle Dynamic IRE on or off as needed. Benefits for ServiceNow Customers Reduced Manual Effort: No need to maintain complex manual identification rules, saving time and reducing errors. Higher CI Data Quality: Enhanced CI matching accuracy reduces duplicates and improves CMDB integrity. Safe Transition: Simulation mode and easy rollback allow testing without risk to production environments. Visibility and Control: Detailed comparison data enables informed decisions about adopting Dynamic IRE.
Dynamic Identification and Reconciliation Engine (IRE) processes CI identification for maximum accuracy and efficiency and eliminates the need to manually create or maintain rules. Actually, you can't alter any of the algorithms
 or operations of Dynamic IRE.

When necessary to differentiate, the legacy, manually-driven IRE, is referred to as
Static IRE
.

Dynamic IRE
is a new engine that you can choose to use instead of
Static IRE
. Dynamic IRE identifies CIs using an improved identification dynamic process and automatically updates its IRE identification rules
 during ingestion of data payloads.

Dynamic IRE evaluates various conditions within the payload simultaneously by running algorithms in parallel to
 score potential matches and to accurately determine CI identity across multiple data sources. Compared to Static IRE, on average, Dynamic IRE matches CIs using a larger combination of the CI attributes to improve the chances of
 finding an optimal match, and by so, reducing the chances for duplicate CIs.

Dynamic IRE is applicable only to the Hardware [cmdb_ci_hardware] class and its descending classes. However, you can configure the system to exclude from Dynamic IRE specific classes descending from the Hardware class.

Key benefits of Dynamic IRE are:
- Usually identifies CIs more accurately resulting in a reduction of duplicate CIs.
- Eliminates manual configuration and continuous maintenance of IRE process rules.

## Getting started with Dynamic IRE

Dynamic IRE is enabled by default on zBooted instances running
Zurich
Patch 11 or a later release. In this state the system property
glide.identification_engine.dynamic_ire_enabled
is set to
true
and Dynamic IRE is considered to be in
 a 'committed mode'.

On upgraded instances running
Zurich
Patch 11 or a later release, that are using Static IRE, you can switch into using Dynamic IRE as described in this topic. For more information, see the respective release notes for the family release of your
 instance.

## Modes of operation

Dynamic IRE provides two modes of operation:
Simulation mode
In simulation mode, Dynamic IRE and Static IRE run in parallel so you can experience and compare Dynamic IRE to Static IRE.

In simulation mode, both Static IRE and Dynamic IRE process the payloads, and any differences in processing and outcome are stored in the CMDB IRE Output Comparison Items [cmdb_ire_output_comparison_item] table. Also, after some
 time of simulations, you can compare the performance of Dynamic IRE to Static IRE.

Committed mode
In committed mode, only Dynamic IRE performs IRE processes and Static IRE is turned off. Once in a committed mode, you can switch back to Static IRE without implications.
Typically, you should start with the simulation mode on a non-production instance to test effectiveness and performance, examine the outcome, and then commit to full usage of Dynamic IRE on your production instance.

## Exclude classes from Dynamic IRE

There might be reasons for configuring child classes descending from the Hardware class, to be excluded from Dynamic IRE. For example, you might want to exclude a custom class with custom attributes, for which there are IRE rules that
 are based on those custom attributes. In this situation, it might not be beneficial to apply Dynamic IRE for that class and its descendants. So if Dynamic IRE is enabled, Static IRE is still being used for those excluded classes.

For more information, see
Exclude classes from Dynamic IRE
.

## Simulate and commit to Dynamic IRE

To start using Dynamic IRE exclusively, a general guideline is to test it first by simulation on a non-production instance:
- Ensure that you meet the user role requirement: sn_cmdb_user.
- On a non-production instance, navigate to the CI Class Manager.
- In CI Class Manager, select Hierarchy and then select the Hardware class.
- In the Hardware navigation panel, select Identification Rule .
- In the Dynamic IRE section, select Simulate Dynamic IRE .
- Carefully review the Simulate Dynamic IRE tile: If you're ready to start a simulation to test Dynamic IRE on a non-production instance, select Simulate Dynamic IRE . The simulation runs IRE processes on the Hardware and any descending classes, and then
 shows a comparison in terms of effectiveness and performance, between Dynamic and Static IRE. Carefully examine this comparison, which can help you determine whether to commit to using Dynamic IRE. If you have already completed a simulation, reviewed the results, and are ready to fully use Dynamic IRE with the Hardware class, on a production instance select the agreement and then select Commit to Dynamic
 IRE .
Alternatively, you can use the
glide.identification_engine.dynamic_ire_enabled
system property to enable or disable Dynamic IRE, and by so, switching between Dynamic and Static IRE. For more information about this
 property, see
Properties
.

## Switch back to Static IRE

When the system is using Dynamic IRE, you can switch back to Static IRE:
- In CI Class Manager, select Hierarchy and then select the Hardware class.
- In the Hardware navigation panel, select Identification Rule .
- In the Dynamic IRE section, select Change to IRE .

## Comparison of the results of Dynamic IRE and Static IRE

In simulation mode, you can see a comparison of the activities and outcome between Dynamic IRE and Static IRE, at a high level and at a record level. Examine the details in this comparison carefully, to help you evaluate the
 effectiveness of Dynamic IRE in your environment before committing to using it.

This comparison calculates a
parity score
, which is the percentage of identical results between Dynamic IRE and Static IRE.
Note:
For a mature Static IRE implementation (with manually-created rules), the parity score is
 expected to be high. This indicates that Dynamic IRE is capable of producing similar results to Static IRE without requiring any manually-created rules or validations for accuracy.

Bar charts show the difference in CI operations of inserting CIs, updating CIs, and CIs found to be incomplete, between the two methods. Select a bar to show the list of comparison records from the CMDB IRE Output Comparison Items
 [cmdb_ire_output_comparison_item] table, for the selected bar chart. Those records contain the details about CIs that were processed differently between Dynamic IRE and Static IRE. Select a record to open it and to review the comparison
 details (in JSON format).

On a record form, you can select
Summarize
to show an
 organized and more user friendly presentation of the comparison results, generated by the
ServiceNow Otto
for CMDB IRE comparison record summarization skill.
