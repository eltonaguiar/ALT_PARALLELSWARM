# insert_vs_update_cmdb

query: ServiceNow Discovery insert new CI versus update existing CI CMDB behavior

## Evidence (3 sources)

SOURCE: https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB3222102
TITLE: ServiceNow
  - CMDB CI sys_updated_on Refresh Behavior Across Discovery Methods
  - CMDB CI sys_updated_on Refresh Behavior Across Discovery Methods - Support and Troubleshooting
  - This article explains when and why the CMDB CI record's `sys_updated_on` (Updated) timestamp is refreshed during collection via Agent, Agentless Discovery (MID), and Cloud Discovery. It clarifies common misconceptions about Staleness and how to distinguish between "still collecting but no data change" versus "not collecting at all."
  - - Look for INSERT/UPDATE operations on the target table (e.g., `cmdb_ci_apache_web_server`)
  - - If discovery collects data but the collected values match existing CI attributes → no write occurs → `sys_updated_on` does not change

SOURCE: https://www.servicenow.com/community/developer-forum/servicenow-discovery-creating-a-new-ci-even-though-an-existing/m-p/3590971
TITLE: ServiceNow
  - ServiceNow Discovery creating a new CI even though an existing CI has the same Name
  - We already have an existing CI in the CMDB with the same Name as the device being discovered. However, when Discovery runs, instead of updating the existing CI, it creates a new CI.
  - 5. Discovery creates a new CI instead of updating the existing CI.
  - I am facing an issue with ServiceNow Discovery and CI identification/IRE.
  - ServiceNow Discovery creating a new CI even though... - ServiceNow Community

SOURCE: https://www.servicenow.com/community/cmdb-forum/rediscovered-ci-remains-retired-why-doesn-t-ootb-discovery/m-p/3575543
TITLE: ServiceNow
  - Here's the part that trips people up: Discovery's identification step and its field-update step are two separate things. Identification matches your printer against the existing cmdb_ci_printer record using identifier rules, and that matching happens regardless of the CI's current install_status. That is exactly why you saw the correct behavior on the pieces that did update: same CI reused, no duplicate, last_discovered and discovery_source refreshed, IP corrected. Discovery does not care that t
  - I am trying to understand the expected OOTB behavior for CI lifecycle status during Discovery.
  - Yes, this is expected OOTB behavior, not a bug, and no, standard Discovery does not flip Retired back to Installed on its own.
  - Install status is different. It is a lifecycle attribute, and the OOTB discovery patterns for printers (and most hardware classes) simply do not include install_status in the payload they hand off to the Identification and Reconciliation Engine (IRE) during an update. IRE only reconciles attributes that actually arrive in the payload for that class. If install_status was never part of what the pattern collects and sends, there is nothing for IRE to compare it against, so it leaves whatever value
  - For the fix: don't try to make Discovery own this field, build a small deliberate control around it instead. A Business Rule (or a scheduled job, if you'd rather batch it) on cmdb_ci_printer that watches for last_discovered or discovery_source changing while install_status is still Retired, and flips it to Installed when that happens, gives you the reactivation without pretending Discovery does it natively. Keep it narrow and logged, because a rediscovered "retired" asset is sometimes exactly wh

## All search hits

- [ServiceNow](https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB3222102) score=5
- [ServiceNow](https://www.servicenow.com/community/developer-forum/servicenow-discovery-creating-a-new-ci-even-though-an-existing/m-p/3590971) score=4
- [ServiceNow](https://www.servicenow.com/community/cmdb-forum/rediscovered-ci-remains-retired-why-doesn-t-ootb-discovery/m-p/3575543) score=4
- [ServiceNow](https://www.servicenow.com/community/itom-forum/implementation-of-discovery-over-an-existing-cmdb/m-p/933037) score=4
- [ServiceNow](https://www.servicenow.com/community/cmdb-forum/network-gear-discovery-and-the-install-status-for-existing-ci/m-p/3359742) score=4
- [ServiceNow](https://www.servicenow.com/community/in-other-news/cmdb-identification-and-reconciliation/ba-p/2268439) score=4
- [ServiceNow](https://www.servicenow.com/docs/r/it-operations-management/discovery-and-service-mapping-patterns/t_CreateCITypeForSM.html) score=3
- [ServiceNow](https://www.servicenow.com/docs/r/xanadu/it-operations-management/service-mapping/manually-add-ci-to-business-service.html) score=3