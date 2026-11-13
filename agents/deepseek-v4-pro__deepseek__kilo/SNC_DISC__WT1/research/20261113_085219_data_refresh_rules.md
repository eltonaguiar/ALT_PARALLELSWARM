# data_refresh_rules

query: ServiceNow CMDB data refresh rules staleness identification engine

## Evidence (3 sources)

SOURCE: https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB1064718
TITLE: ServiceNow
  - The Identification and Reconciliation Engine (IRE) is a centralized framework that processes payloads to maintain the Configuration Management Database (CMDB). The IRE handles the creation of new configuration items (CIs) and updates to existing CIs.
  - Learn the key concepts of the CMDB Identification and Reconciliation Engine (IRE), including identification rules, reconciliation rules, dependent relationships, deduplication, reclassification, and available tools. This article provides a foundational overview for administrators and platform engineers working with the CMDB.
  - CMDB Identification and Reconciliation Engine fundamentals - Support and Troubleshooting
  - The IRE first applies the identification rules to find CIs in the CMDB, and then applies the inclusion rules to determine if those CIs can be used.
  - The IRE uses identification rules to find CIs in the CMDB. Each identification rule contains a set of attributes used to search the CMDB for a match.

SOURCE: https://www.servicenow.com/community/cmdb-forum/how-to-create-data-refresh-rules-for-stale-ci-s/td-p/2944894
TITLE: ServiceNow
  - How to create Data Refresh Rules for Stale CI's - ServiceNow Community
  - Example : class: cmdb_ci_appl , Discovery source : ServiceNow While creating data refresh rule , shall I keep the same discovery source for this class?
  - Now Assist AI for Stale CI Identification and CMDB Data Quality Improvement
  - In the Data Refresh Rules section, click Add to create a rule or select an existing rule to edit.
  - I have a list of tables , while creating the Data Refresh rules what Discovery source should I select .

SOURCE: https://www.servicenow.com/community/cmdb-forum/a-deep-dive-into-ci-class-manager-and-ire-servicenow-cmdb/m-p/3486406
TITLE: ServiceNow
  - Data Refresh Rules (Staleness Rules): Keeping Your CMDB Current Data Refresh Rules, also known as Staleness Rules, define when a CI is considered stale due to a lack of updates from its expected discovery source over a defined period (e.g., 14 days). These rules are essential for:
  - CI Identification Rules are a set of criteria that ServiceNow uses to uniquely identify Configuration Items within the CMDB. These rules specify how a CI is recognized using unique attributes (e.g., Serial Number, Name, MAC Address, Device ID, Object ID) or a combination of attributes. Properly defined identification rules are crucial for maintaining CMDB data quality by preventing duplicate CIs .
  - A Configuration Management Database (CMDB), in short, is a vital component in successful IT Service Management (ITSM). The main function of a CMDB is to store a thorough catalog of an organization’s IT infrastructure. When working with ServiceNow, properly maintaining its integrity is critical to successfully delivering any business need, including IT operations service management and asset management. The goal of this blog post is to look closer at a few important ServiceNow CMDB concepts, like
  - Identification/Reconciliation Rules: Determine the rules that govern the identification and updating of CIs, with the aim of ensuring data accuracy.
  - CI Reconciliation Rules: Resolving Data Conflicts CI Reconciliation Rules are crucial for maintaining CMDB integrity when multiple data sources update the same CI. These rules determine which source has the authority to update specific CI attributes, resolving conflicts and discrepancies .

## All search hits

- [ServiceNow](https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB1064718) score=5
- [ServiceNow](https://www.servicenow.com/community/cmdb-forum/how-to-create-data-refresh-rules-for-stale-ci-s/td-p/2944894) score=4
- [ServiceNow](https://www.servicenow.com/community/cmdb-forum/a-deep-dive-into-ci-class-manager-and-ire-servicenow-cmdb/m-p/3486406) score=4
- [ServiceNow](https://www.servicenow.com/community/cmdb-forum/data-refresh-rules/m-p/3468212) score=4
- [ServiceNow](https://www.servicenow.com/docs/r/zurich/servicenow-platform/configuration-management-database-cmdb/create-datasource-staleness-rule.html) score=3
- [https://github.com  ›  ServiceNow  ›  ServiceNowDocs  ›  blob  ›  australia  ›  markdown  ](https://github.com/ServiceNow/ServiceNowDocs/blob/australia/markdown/servicenow-platform/configuration-management-database-cmdb/create-datasource-staleness-rule.md) score=0
- [LinkedIn](https://www.linkedin.com/posts/anant-kumawat_servicenow-cmdb-itom-activity-7456758556504260608-MYKg) score=0
- [ServiceNow Guru](https://servicenowguru.com/cmdb/servicenow-cmdb-identification-and-reconciliation-engine-ire/) score=0