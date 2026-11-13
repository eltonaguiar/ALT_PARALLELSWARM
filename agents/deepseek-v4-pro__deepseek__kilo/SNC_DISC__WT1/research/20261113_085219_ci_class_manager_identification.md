# ci_class_manager_identification

query: ServiceNow CI Class Manager identification rules configuration

## Evidence (3 sources)

SOURCE: https://www.servicenow.com/community/cmdb-forum/a-deep-dive-into-ci-class-manager-and-ire-servicenow-cmdb/m-p/3486406
TITLE: ServiceNow
  - A Configuration Management Database (CMDB), in short, is a vital component in successful IT Service Management (ITSM). The main function of a CMDB is to store a thorough catalog of an organization’s IT infrastructure. When working with ServiceNow, properly maintaining its integrity is critical to successfully delivering any business need, including IT operations service management and asset management. The goal of this blog post is to look closer at a few important ServiceNow CMDB concepts, like
  - These are the advanced rules which can restrict the CIs taken into consideration for identification. For example, you might create a rule specifying that you want to process CIs with 'Operational' status. These rules are set under 'Inclusion Rule (Advanced)' tab in CI Class Manager
  - In the CI Class Manager, under the 'Reconciliation Rules' tab, you can add new rules. This involves specifying each 'Discovery source' and its 'Priority'. A higher priority value indicates greater authority. For example, ServiceNow Discovery might have a higher priority than a manual entry .
  - New identification rules can be configured in the CI Class Manager by using the 'Replace' button and then 'Add' under 'Identifier Entries'. You can choose attributes from the main table, a lookup table, or a combination. It's essential to specify the 'Priority' and 'Criterion Attributes' for each entry
  - CI Class Manager: Your Central Hub for Configuration Items CI Class Manager acts as an interface in ServiceNow that allows for unparalleled visibility and control of Configuration Items (CIs). The CI Class Manager enables administrators and sn_cmdb_admin roles to:CI Classes: Define different types of Configuration Items.

SOURCE: https://www.servicenow.com/community/cmdb-articles/elevating-cmdb-data-quality-with-well-defined-ci-identification/ta-p/2857355
TITLE: ServiceNow
  - This is an additional feature available to narrow the scope of CIs that are included in the identification process. When identification inclusion rule is defined for a CI class, ServiceNow’s Identification and Reconciliation Engine (IRE) processes only the Configuration Items (CIs) that meet the criteria set by the identification inclusion rules during the duplication detection of independent CIs. For example, you can create a rule to include solely the CIs whose ‘Operational Status’ is ‘Operati
  - The inclusion rules can also be created from the same ‘Identification rule’ tab of a CI class from the CI class manager. You can find ‘Inclusion Rule (Advanced)’ under the Identifier entries. Click on ‘Add’ and then define the ‘Active record condition’ . For example, the following screenshot shows how to set an inclusion rule for ‘Computer’ CI class with the condition Operation status=Operational.
  - CI Identification Rules are a set of criteria that ServiceNow uses to uniquely identify and differentiate Configuration Items (CIs) within the CMDB. These rules play a vital role in preventing duplication and ensuring the accuracy and integrity of the data stored in the CMDB. They define how a Configuration Item (CI) is identified based on its unique attributes, such as Serial Number, Name, Device ID, Object ID, etc. or any combination of such attributes which act as unique identifiers for a par
  - When a new CI is introduced into the CMDB, ServiceNow's identification and reconciliation engine (IRE) checks the defined CI Identification Rules for a particular CI class to determine whether it is a new CI or if it matches an existing CI. If a match is found based on the identification rules, ServiceNow updates the existing CI record with the new information. However, if no match is found, a new CI record is created within the appropriate CI class. The identification rules for a CI class can b
  - Open the CI class for which you would like to check the identification rules (E.g. Computer, Server, Network Gear etc.)

SOURCE: https://www.servicenow.com/community/cmdb-forum/identification-and-reconciliation-rule/td-p/3142427
TITLE: ServiceNow
  - You can access identification rules in ServiceNow by going to CI class manager and selecting the Identification Rule tab. You can also access them by going to Identification/Reconciliation>CI identifiers from the application navigator.
  - Identification and Reconciliation Rule - ServiceNow Community
  - The IRE uses the identification rules in order of priority to find a CI in the CMDB
  - https://servicenowguru.com/cmdb/servicenow-cmdb-identification-and-reconciliation-engine-ire/
  - Duplicates for a CI class are identified based on the identification rule set for that class. It is possible to automate remediation.

## All search hits

- [ServiceNow](https://www.servicenow.com/community/cmdb-forum/a-deep-dive-into-ci-class-manager-and-ire-servicenow-cmdb/m-p/3486406) score=4
- [ServiceNow](https://www.servicenow.com/community/cmdb-articles/elevating-cmdb-data-quality-with-well-defined-ci-identification/ta-p/2857355) score=4
- [ServiceNow](https://www.servicenow.com/community/cmdb-forum/identification-and-reconciliation-rule/td-p/3142427) score=4
- [ServiceNow](https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/t_CreateCIIdentificationRule.html) score=3
- [ServiceNow](https://www.servicenow.com/docs/r/xanadu/servicenow-platform/configuration-management-database-cmdb/c_IdentificationRules.html?contentId=FrQTNcPP3fEZU_zFLdAvgw) score=3
- [ServiceNow](https://www.servicenow.com/docs/r/xanadu/servicenow-platform/configuration-management-database-cmdb/ci-class-manager-landing-page.html?contentId=ZAdL89qP5zDdWZwV~KjH2w) score=3
- [https://www.youtube.com  ›  watch](https://www.youtube.com/watch?v=Yu9R9qZYs9g) score=0
- [ServiceNow Guru](https://servicenowguru.com/cmdb/servicenow-cmdb-identification-and-reconciliation-engine-ire/) score=0