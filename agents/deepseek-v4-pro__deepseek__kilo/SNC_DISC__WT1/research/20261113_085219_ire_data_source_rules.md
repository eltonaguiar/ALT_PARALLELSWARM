# ire_data_source_rules

query: ServiceNow IRE data source rules which data source can update which field

## Evidence (3 sources)

SOURCE: https://www.servicenow.com/community/itom-forum/attributes-field-in-reconciliation-rules-in-ire-does-it-actually/m-p/1025487
TITLE: ServiceNow
  - Today I am seeing IRE blocking (rather than allowing) all updates by a data source when the Attributes field on the reconciliation rule is empty. When in fact Attributes being empty is meant to mean that the data source is authorised to update ALL fields on the target record. This is taken from https://docs.servicenow.com/bundle/madrid-servicenow-platform/page/product/configuration-management/reference/r_ReconciliationRulesPrinciples.html (it's the section headed "Authorization for all attribute
  - Which is that the Attributes field being empty does indeed mean that the data source is authorised to update all fields on the target CI. But not for fields which are explicitly specified in the Attributes field on reconciliation rules from other data sources that apply to this CI class. In that situation the update is blocked, without reference to data source precedence, and regardless of whether those other data source(s) have updated the CI. That definitely isn't what the docs site says here 
  - When the same field appears in the Attributes field on multiple reconciliation rules, that's when IRE uses the data source precedence records to decide whether to allow the current field update to happen, depending on whether the current data source has greater precedence than the one that last was allowed to update the field. Which, although I haven't actually checked that out, I assume must based on the Data Source History [cmdb_datasource_last_update] table, because that is the only place I c
  - Initially, we were seeing a data source being able to update fields that by rights it shouldn't be able to, because those fields weren't included in the relevant reconciliation definition.
  - So in conclusion, the safest approach is to always explicitly select all the fields that a data source is authorised to update, in the Attributes field of the reconciliation record. And avoid leaving that Attributes field empty.

SOURCE: https://www.servicenow.com/community/cmdb-articles/understanding-ire-reconciliation-rules/ta-p/3289239
TITLE: ServiceNow
  - In the context of the Identification and Reconciliation Engine (IRE), reconciliation rules play a pivotal role during CI update scenarios. These rules determine the authoritative source responsible for updating specific attributes on a CI. By defining the source of truth for these updates, reconciliation rules help maintain data integrity and avoid conflicts when multiple sources attempt to modify the same attributes.
  - The primary purpose of this property is to allow administrators to define conditional filters that are evaluated against the target CI just before an incoming attribute update (which has already passed standard data source precedence checks) is applied. If the CI meets the filter's criteria, the update can be selectively prevented or allowed, overriding the normal outcome of precedence rules for that specific update instance.
  - One of the most fundamental jobs of IRE Reconciliation is to ensure that more trustworthy (higher priority) data sources maintain control over the attributes they are authoritative for, even when other, less trustworthy (lower priority) sources try to update the same CI.
  - This means that if ServiceNow is designated as the sole authoritative source for updating attribute values on a Linux Server CI, no other source, including ServiceWatch, is permitted to alter those values. While ServiceWatch may create the CI and populate it with initial attribute values, any subsequent modifications to these values must adhere strictly to the reconciliation rules. In this setup, ServiceNow maintains ultimate control, ensuring consistency and preventing unauthorized updates from
  - In scenarios where priority levels are assigned to reconciliation rules, ServiceNow, designated as the authoritative source, may hold a priority of 100, while ServiceWatch is assigned a lower priority, such as 200. These priority levels further clarify the hierarchy of control, ensuring that updates to specific attributes follow the defined order. For instance, if ServiceNow has priority 100 for updating the RAM value of a Linux Server CI, any changes attempted by ServiceWatch, with its priority

SOURCE: https://www.servicenow.com/community/servicenow-ai-platform-forum/when-does-ire-update-the-discovery-source-field-of-a-ci/m-p/1111012
TITLE: ServiceNow
  - Thanks for suggesting the Reconciliation Rules. No reconciliation rules are setup on the CI Classes in question. I tried to add a rule for the Discovery Source attribute, but the field is not available for selection. SG-SCCM is our only data source. We don't have Discovery, ServiceMapping or other data sources.
  - When does IRE update the discovery_source field of... - ServiceNow Community
  - I've migrated to SG-SCCM 3.06 from MS-SCCM plugin recently and added a second SCCM server as a data source. I've noticed that not all CI's (Computers, Servers) have their Discovery Source field changed to SG-SCCM (from MS SMS or empty), even though SG-SCCM is updating these CI's. Only CI's that are inserted/created have the Discovery Source set to SG-SCCM.
  - Is there any more information on this? I am facing a similar issue where the discovery source field is not getting updated to SG-SCCM on CI's (computers,servers) even after SG-SCCM updates CI's.
  - The Identification and Reconciliation engine (IRE) documentation page, section: Timestamps in key attributes (https://docs.servicenow.com/bundle/rome-servicenow-platform/page/product/configuration-management/concept/ire.html) suggests that "IRE always updates CIs’ last_discovered and discovery_source attributes during payload processing, even when no other CI attributes are updated."

## All search hits

- [ServiceNow](https://www.servicenow.com/community/itom-forum/attributes-field-in-reconciliation-rules-in-ire-does-it-actually/m-p/1025487) score=4
- [ServiceNow](https://www.servicenow.com/community/cmdb-articles/understanding-ire-reconciliation-rules/ta-p/3289239) score=4
- [ServiceNow](https://www.servicenow.com/community/servicenow-ai-platform-forum/when-does-ire-update-the-discovery-source-field-of-a-ci/m-p/1111012) score=4
- [ServiceNow](https://www.servicenow.com/community/cmdb-blog/multi-source-user-integrations-with-ire-rules-for-user-table/ba-p/3395707) score=4
- [ServiceNow](https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/create-ire-data-source-rule.html) score=3
- [ServiceNow](https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/ire.html) score=3
- [ServiceNow](https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/r_ReconciliationRulesPrinciples.html) score=3
- [ServiceNow Guru](https://servicenowguru.com/cmdb/servicenow-cmdb-identification-and-reconciliation-engine-ire/) score=0