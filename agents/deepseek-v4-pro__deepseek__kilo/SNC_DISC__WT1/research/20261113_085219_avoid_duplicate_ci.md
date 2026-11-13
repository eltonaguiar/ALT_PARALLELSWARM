# avoid_duplicate_ci

query: ServiceNow Discovery avoid duplicate CIs identification reconciliation rules

## Evidence (3 sources)

SOURCE: https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB2558192
TITLE: ServiceNow
  - When Discovery runs, it calls the Identification and Reconciliation Engine (IRE) to identify and reconcile each Configuration Item against the CMDB. By default, IRE evaluates retired CIs in addition to active CIs. If an active CI shares identifying attributes with a retired CI, IRE flags a potential conflict and generates a duplicate task.
  - Duplicate tasks created against retired Configuration Items during Discovery (IRE reconciliation)
  - Duplicate CI tasks are generated against retired CIs after a Discovery run.
  - The tasks appear in the Duplicate CI Tasks list after each Discovery cycle.
  - Xanadu (and other supported releases that include the Identification and Reconciliation Engine).

SOURCE: https://www.servicenow.com/community/cmdb-forum/how-to-avoid-duplicate-ci-creation/m-p/3498456
TITLE: ServiceNow
  - It is hard to identify the root cause of duplicate CIs without digging into the instance and the sources. IRE should help to avoid duplicates. Question then is: a) How were those CIs created? What are their Discovery sources? b) Was IRE used when creating the CIs as that is the best practice for every automatic import/discovery? c) If you are sure that IRE was used, review the config of Identification Rules for the 3 CI classes.
  - In CMDB there is one CI which has created under three different classes. with same name, same IP address and same serial number. Is this duplicate CIs ,created because of identification rule? how to avoid this in future?
  - Identification rules are evaluated per class. Even if the attribute values are identical, IRE will not match records across different classes. If incoming data is classified differently (for example, by Discovery or an integration), the system can create separate CIs in each class.
  - Can Identification and Reconciliation Engine (IRE) be fully implemented for a non-CMDB table (cmn_lo
  - Navigate to Identification Rules and ensure strong identifiers (such as Serial Number + Manufacturer) are consistently configured for related classes.

SOURCE: https://www.servicenow.com/community/cmdb-articles/cmdb-understanding-identification-and-reconciliation-rules-and/ta-p/3520826
TITLE: ServiceNow
  - 👉 Identification & Reconciliation rules answer two different questions:
  - CMDB - Understanding Identification and Reconciliation Rules and Conflicts within these rules
  - Multiple Identification rules valid ✅ Higher priority rule wins
  - Reconciliation Rule Discovery beats SCCM → ✅ Discovery values kept
  - CMDB - Understanding Identification and Reconcilia... - ServiceNow Community

## All search hits

- [ServiceNow](https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB2558192) score=5
- [ServiceNow](https://www.servicenow.com/community/cmdb-forum/how-to-avoid-duplicate-ci-creation/m-p/3498456) score=4
- [ServiceNow](https://www.servicenow.com/community/cmdb-articles/cmdb-understanding-identification-and-reconciliation-rules-and/ta-p/3520826) score=4
- [ServiceNow](https://www.servicenow.com/community/developer-forum/discovery-is-creating-duplicate-ci-entries-across-multiple-mid/m-p/3415719) score=4
- [ServiceNow](https://www.servicenow.com/community/itom-articles/discovery-identification-identifiers-and-duplicates-prevention/ta-p/2320049) score=4
- [ServiceNow](https://www.servicenow.com/community/cmdb-forum/multiple-cis-created-with-same-serial-number-but-different-ips/m-p/3465446) score=4
- [ServiceNow](https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/id-detect-dup-ci.html) score=3
- [https://virima.com  ›  blog  ›  how-to-prevent-duplicate-cis-and-sync-errors-in-servicenow](https://virima.com/blog/how-to-prevent-duplicate-cis-and-sync-errors-in-servicenow-cmdb-integration) score=0