# Apply IRE to Import Sets

- Source: https://www.servicenow.com/docs/r/zurich/servicenow-platform/configuration-management-database-cmdb/identification-import-sets.html
- Release: Zurich
- Map: platcap

---

# Applying IRE to Import Sets

Summarize Summarized using AI This content was generated using new OpenAI-powered functionality. Results are provided on an as is basis and are not guaranteed to be accurate or complete. Summary of Applying IRE to Import Sets This guidance explains how to apply the CMDB Identification and Reconciliation Engine (IRE) processes when using Import Sets to load Configuration Items (CIs) into the CMDB. Applying IRE during Import Sets processing helps prevent duplicate CIs by identifying and reconciling records before insertion or update. This is critical for maintaining CMDB data integrity and avoiding redundancy caused by identical imported records. Show full answer Show less Key Features Transform Map Script Integration: Incorporate a call to the CMDBTransformUtil API in the onBefore transform map script. This script triggers identification and reconciliation for each import set row, preventing duplicate records by setting ignore = true to stop duplicate creation after processing. Identification Engine Process: Each source record is checked against existing CIs; if unique, it inserts the record, otherwise it updates the existing CI. API Capabilities: The CMDBTransformUtil API supports reference fields and evaluates source scripts to determine target values, allowing flexible field mapping during import. Multiple Target Tables per Import Set: You can specify a target table for each record within the import set by adding a target table column in the data source file. This enables importing different CI classes (e.g., Computer, Server) in one import set. Field maps must be configured accordingly to map this column to the Class field in the CMDB. Restrictions Each import set must be associated with a single transform map, even when using the CMDBTransformUtil API. The API does not enforce mandatory field validation; if mandatory fields are missing, the import will fail regardless of transform map settings. Identification and reconciliation cannot be applied to dependent CIs that use dependent identification rules. Practical Application for ServiceNow Customers By integrating IRE with Import Sets using the prescribed transform map script approach, ServiceNow customers can ensure cleaner CMDB imports with reduced duplicates and improved data accuracy. Customers can also import multiple CI classes in one batch by specifying target tables per record, streamlining complex data loads. Understanding the restrictions helps prevent common import failures and supports proper configuration for successful CMDB population.
You can apply CMDB Identification and Reconciliation Engine (IRE) processes when Import Sets are used to import CIs into the CMDB. CI identification can prevent duplicate CIs in the CMDB, which Import Sets might otherwise
 cause.

Populating CMDB tables using Import Sets can inadvertently result in duplicate CIs when
 multiple imported records are identical to an existing CI. To minimize this duplication, you can
 apply CMDB Identification and Reconciliation processes to Import Sets when importing new
 records into CMDB tables.

## Transform map script

In the onBefore transform map script for an import set, add a call to the
CMDBTransformUtil
API, similar to the following code sample:
(function runTransformScript(source, map, log, target) {
// Call CMDB API to do Identification and Reconciliation of current row
var cmdbUtil = new CMDBTransformUtil();
cmdbUtil.setDataSource('ImportSet');
cmdbUtil.identifyAndReconcile(source, map, log);
ignore = true;

if (cmdbUtil.hasError()) {
 var errorMessage = cmdbUtil.getError();
 log.error(errorMessage);
} else {
 log.info('IE Output Payload: ' + cmdbUtil.getOutputPayload());
 log.info('Imported CI: ' + cmdbUtil.getOutputRecordSysId());
}

})(source, map, log, target);
The
ignore = true
code phrase prevents Import Sets from creating the same
 record again after it is processed by the identification engine.

## Process

The identification engine performs identification of each source record before it is inserted
 into the CMDB. The identification engine determines if the record is a duplicate of an existing
 CI, and then:
- If not duplicate: Inserts the record to the target table.
- If duplicate: Updates the existing CI in the CMDB, with data from the source record.
The CMDBTransformUtil API pre-processes the source data, then passes the input values to the
 identification engine with import set being the data source by default. The CMDBTransformUtil
 API supports a target field that is a reference field in the same manner that Import Sets
 supports it. The CMDBTransformUtil API also supports a source script, evaluating source scripts
 to determine the target value which is then passed to the identification engine. For more
 information, see
Creating a field map
.

## Specify multiple target tables for an import set

You can configure each record in an import set with its own target table. Then, instead of
 inserting all the transformed records into a single target table, the records are inserted into
 the different target tables that are specified per record. For example, you might need to insert
 some records from the import set to the Computer class and other records to the Server
 class.

When
importing data using Import Sets
,
 incorporate the following steps:
- In the data source file, add a target table column. Use a string such as "MyTable" to label
 the column header. In each record row, enter the target table for the record, as a valid CMDB
 class name such as "cmdb_ci_computer".
- After you Auto Map Matching Fields on the Table Transform Map form,
 add a field map for the added target table column to establish a relationship between classes
 and the target tables in the CMDB. In the Field Map related list on the Table Transform Map form,
 click New . Set Source field to the header of the target table column that you
 added in the data source file, such as MyTable . Set Target field to Class . Click Submit .
When you configure an import set with multiple target tables as described in the steps above,
 the
Target table
that is specified on the Table Transform Map form is not
 used.

## Restrictions

The following restrictions apply:
- An import set should be associated with a single transform map. While adding a call to the
 CMDBTransformUtil API, ensure that still a single transform map exists for the import
 set.
- The CMDBTransformUtil API does not check if mandatory fields have values when used with
 Import Sets . Regardless of how enforce mandatory fields is set in the
 transform map, data import fails if a mandatory field does not have a value.
- CI Identification and Reconciliation cannot be applied to Import Sets for dependent CIs
 (CIs with dependent identification rules).
