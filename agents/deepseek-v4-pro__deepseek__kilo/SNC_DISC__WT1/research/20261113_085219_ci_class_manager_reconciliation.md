# ci_class_manager_reconciliation

query: ServiceNow CI Class Manager reconciliation rules configuration

## Evidence (3 sources)

SOURCE: https://www.servicenow.com/community/cmdb-forum/a-deep-dive-into-ci-class-manager-and-ire-servicenow-cmdb/m-p/3486406
TITLE: ServiceNow
  - In the CI Class Manager, under the 'Reconciliation Rules' tab, you can add new rules. This involves specifying each 'Discovery source' and its 'Priority'. A higher priority value indicates greater authority. For example, ServiceNow Discovery might have a higher priority than a manual entry .
  - A Configuration Management Database (CMDB), in short, is a vital component in successful IT Service Management (ITSM). The main function of a CMDB is to store a thorough catalog of an organization’s IT infrastructure. When working with ServiceNow, properly maintaining its integrity is critical to successfully delivering any business need, including IT operations service management and asset management. The goal of this blog post is to look closer at a few important ServiceNow CMDB concepts, like
  - Via CI Class Manager: Navigate to the desired CI class and select the 'Reconciliation Rules' tab.
  - CI Class Manager: Your Central Hub for Configuration Items CI Class Manager acts as an interface in ServiceNow that allows for unparalleled visibility and control of Configuration Items (CIs). The CI Class Manager enables administrators and sn_cmdb_admin roles to:CI Classes: Define different types of Configuration Items.
  - A Deep Dive into CI Class Manager and IRE Servicen... - ServiceNow Community

SOURCE: https://www.servicenow.com/community/itom-forum/reconciliation-rules-configuration/td-p/3591340
TITLE: ServiceNow
  - How should Reconciliation Rules govern CI updates from multiple data sources?
  - Create/configure a reconciliation rule for the relevant Windows CI class and specifically the serial_number attribute:
  - Yes, Reconciliation Rules are the correct approach to prevent Discovery from overwriting the manually corrected serial_number.
  - Also check whether an existing attribute-specific rule or dynamic reconciliation rule is overriding your rule. An attribute-specific rule takes precedence over an "Apply to all attributes" rule, and a dynamic reconciliation rule takes precedence over static reconciliation rules.
  - The issue is that serial_number is present in two Windows Server Manual Entry rules .

SOURCE: https://www.servicenow.com/community/developer-forum/task-09-configure-reconciliation-rule-in-cmdb-on-demand/m-p/2526218
TITLE: ServiceNow
  - Being part of the Cloud Dimensions CMDB implementation team, using CI Class Manager, you are tasked to update the Windows Server (cmdb_ci_win_server) class with a static reconciliation rule that achieves the following:
  - Task 09: Configure Reconciliation Rule in CMDB on ... - ServiceNow Community
  - Task 09: Configure Reconciliation Rule in CMDB on Demand Fundamental Course
  - Ensure CI records have correct discovery_source values (ServiceNow or LANDesk).
  - You have to create a single Reconciliation rule which will cover both scenarios:

## All search hits

- [ServiceNow](https://www.servicenow.com/community/cmdb-forum/a-deep-dive-into-ci-class-manager-and-ire-servicenow-cmdb/m-p/3486406) score=4
- [ServiceNow](https://www.servicenow.com/community/itom-forum/reconciliation-rules-configuration/td-p/3591340) score=4
- [ServiceNow](https://www.servicenow.com/community/developer-forum/task-09-configure-reconciliation-rule-in-cmdb-on-demand/m-p/2526218) score=4
- [ServiceNow](https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/create-reconciliation-rule.html) score=3
- [ServiceNow](https://www.servicenow.com/docs/r/fr-FR/servicenow-platform/configuration-management-database-cmdb/create-reconciliation-rule.html?contentId=H6N9c1I5d3kUoEq9mZqiOA) score=3
- [ServiceNow](https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/r_ReconciliationRulesPrinciples.html) score=3
- [https://www.youtube.com  ›  watch](https://www.youtube.com/watch?v=Yu9R9qZYs9g) score=0
- [https://medium.com  ›  @ashoksasidharan  ›  best-practices-for-cmdb-data-management-in-ser](https://medium.com/@ashoksasidharan/best-practices-for-cmdb-data-management-in-servicenow-9cb6ae18eb92) score=0