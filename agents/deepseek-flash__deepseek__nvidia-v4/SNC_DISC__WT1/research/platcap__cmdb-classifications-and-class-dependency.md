# CMDB classifications and class dependency

- Source: https://www.servicenow.com/docs/r/zurich/servicenow-platform/configuration-management-database-cmdb/c_CMDBClassifications.html
- Release: Zurich
- Map: platcap

---

# CMDB classifications and class dependency

CMDB
classifications are groups of CIs that share attributes and are stored in their own class table. Classifications let administrators to define a class hierarchy for the CIs within the
CMDB
.

A CI class refers to the actual table name in the instance database. In that context, 'CI type' is a friendly name that a CI is known by, such as computer, router, or printer.

One of the characteristics of a CMDB class is its dependency on other classes. A class can be independent or dependent, which determines the dependency or independence of the class CIs.

Independent CIs
CIs from an independent class, such as Linux Server CIs, have their own identity, exist by themselves, and aren't dependent on any other CIs.
Dependent CIs
CIs from a depended class have relationships with CIs from other classes and exist meaningfully only if these relationships exist. Dependent CIs don't exist on their own in the absence of the dependent relationship. For example:
- Network Adapter CIs don't exist meaningfully without the Hardware CIs that contain them.
- Application CIs don't exist on their own without the Server CI they are hosted on.
Identification processes in the
Identification and Reconciliation engine (IRE)
CMDB feature extensively use CIs dependency classification. To find out the dependency classification of a class, open the Identification Rule page for a class in
CI Class Manager
. To establish CI dependency, use the CI Class Manager to specify
dependent relationship rules
for a CI class.

For more information, see
Identification rules
.
