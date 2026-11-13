# Reconciliation rules

- Source: https://www.servicenow.com/docs/r/zurich/servicenow-platform/configuration-management-database-cmdb/r_ReconciliationRulesPrinciples.html
- Release: Zurich
- Map: platcap

---

# Reconciliation rules

Summarize Summarized using AI This content was generated using new OpenAI-powered functionality. Results are provided on an as is basis and are not guaranteed to be accurate or complete. Summary of Reconciliation rules Reconciliation rules in ServiceNow determine which discovery sources are authorized to update specific Configuration Item (CI) attributes. These rules help prevent discovery sources like EventManagement, ImportSet, ManualEntry, and Tivoli from overwriting each otherâs updates when using thecreateOrUpdateCI()API. Two types of reconciliation rules exist: static and dynamic, each with distinct behaviors and use cases. Show full answer Show less Key Features Static Reconciliation Rules: Legacy rules that assign priority among discovery sources for updating CI attributes. They specify which sources can update particular class attributes and the precedence order. These rules can be defined both at parent and child class levels and are stored in the cmdbreconciliationdefinition table. Dynamic Reconciliation Rules: Rules that rely on attribute values processed by CMDB 360/Multisource CMDB rather than fixed source priority. Dynamic rules select the largest or most reported value from all discovery sources, requiring CMDB 360 to be enabled. Only one dynamic rule is allowed per class attribute, and these rules are stored in the cmdbdynamicreconciliationdefinition table. Precedence: When both static and dynamic rules exist for the same CI attribute, dynamic rules take precedence. Granular Authorization: Static rules can authorize discovery sources to update all attributes in a class or specific attributes only. Child class rules override parent class rules, allowing fine-tuned control over attribute updates. Overlapping Static Rules: Multiple static rules can authorize different discovery sources for the same attribute without conflict, with enforcement preventing overwrites. Domain Separation Support: Reconciliation rules can be scoped to specific domains if Domain Separation is enabled, with child domains inheriting or overriding parent domain rules. Practical Application for ServiceNow Customers Control CI Attribute Updates: Use static reconciliation rules to set clear priorities for which discovery sources can update specific attributes, avoiding data conflicts. Leverage CMDB 360 for Complex Cases: When priority ordering is difficult, enable dynamic reconciliation rules to automatically select the best attribute values across sources. Define Rules at Class Levels: Create reconciliation rules at both parent and child class levels to ensure precise attribute update controls tailored to your CI structure. Manage Domain-Specific Rules: If using Domain Separation, scope reconciliation rules appropriately to maintain data integrity across domains. Maintain Data Accuracy: Employ data refresh rules to identify stale CIs per discovery source, allowing lower-priority sources to update stale data and keep your CMDB current. Key Outcomes Improved data integrity by preventing conflicting updates from multiple discovery sources. Flexible and scalable configuration of data precedence rules tailored to organizational needs. Enhanced CMDB accuracy through dynamic rule application and data refresh mechanisms. Clear governance over which discovery sources can update specific CI attributes, reducing manual intervention and errors.
Reconciliation rules determine which discovery
 sources can update CI attributes.

Discovery sources, such as EventManagement, ImportSet, ManualEntry, and Tivoli, are used
 with the
createOrUpdateCI()
API to simulate manual updates to CIs.
 Without reconciliation rules, discovery sources can overwrite each other's updates to
 attribute values.

There are two types of reconciliation rules:
Static reconciliation rules
Static reconciliation rules are the legacy reconciliation rules that set priorities
 for the various discovery sources for updating CI attributes. Static reconciliation
 rules specify which discovery sources can update class attributes, and the
 precedence order among these discovery sources.

When creating static reconciliation rules, ensure that there is a reconciliation
 rule for each discovery source that is authorized to update an attribute.
 Reconciliation rules can be defined at the parent and the child class level.

Static reconciliation rules are stored in the Reconciliation Definition
 [cmdb_reconciliation_definition] table.

Dynamic reconciliation rules
Dynamic reconciliation rules are based on attribute values processed by
CMDB 360/Multisource CMDB
rather than on discovery source
 priority. First, CMDB 360 processes the current payload data into the CMDB 360 data
 store. Then, applying a dynamic reconciliation rule, IRE selects the largest or most
 reported value, for example, across all discovery sources. Because dynamic
 reconciliation rules leverage CMDB 360, you must enable that feature to use dynamic
 reconciliation rules.

Creating dynamic reconciliation rules can be useful, for example, if it becomes
 difficult to set priority order for multiple discovery sources. Only a single
 dynamic reconciliation rule can exist per class attribute.

Dynamic reconciliation rules are stored in the Dynamic Reconciliation Definitions
 [cmdb_dynamic_reconciliation_definition] table.

## Examples of static reconciliation rules

The following sample static reconciliation rules are created for the
cmdb_ci_computer
class and its
cmdb_ci_linux_server
child class:
- Discovery is exclusively authorized to update the name attribute
 in the cmdb_ci_computer class. Because reconciliation rules are
 derived by child classes from parent classes, this rule also authorizes Discovery to
 update the name attribute in any child classes for the cmdb_ci_computer class.
- ServiceWatch is exclusively authorized to update the name attribute in the cmdb_ci_linux_server class.
- ServiceWatch is exclusively authorized to update all attributes in the cmdb_ci_linux_server class, as configured by leaving the Attributes field empty in the rule.
See
Create a CI reconciliation rule
for details about creating a
 static reconciliation rule that, for example, authorizes a discovery source to update a
 specific attribute such as
name
.

## Using reconciliation rules

As you create reconciliation rules, keep in mind the following principles which are
 designed for flexibility and the refinement of rules at the attributes level:

Precedence of dynamic reconciliation rules
When both, static and dynamic reconciliation rules exist for the same CI attribute,
 the dynamic reconciliation rule takes precedence over the static reconciliation
 rule.

Authorization for all attributes in a class
A static reconciliation rule lets you authorize a discovery source to update all
 attributes in a class. However, this authorization can be overridden for some of the
 attributes by rules for child classes in which specific attributes are listed.

For example, if only example rules #1 and #3 above are created, then Discovery is
 authorized to update the
name
attribute in the
cmdb_ci_linux_server
class. ServiceWatch is authorized to
 update all other attributes in the class except for the
name
attribute.

To override the authorization of Discovery to update the
name
attribute, example rule #2 above is added to specifically authorize ServiceWatch to
 update the attribute.

Authorization to only specific attributes in a class
To
 authorize a discovery source to update specific attributes in a class, create a
 static reconciliation rule for the discovery source, and list these attributes in
 the rule. A rule that grants access to specific attributes in a class overrides
 other static reconciliation rules with an empty attribute list that grants access to
 the entire class.

Example rule #1 above grants Discovery with exclusive authority to update the
name
attribute of the
cmdb_ci_computer
class. All other discovery sources are prevented from updating the
name
attribute of any CI in the
cmdb_ci_computer
class.

Child class rules overrides parent class rules
Any reconciliation rules defined for a child class override the rules defined for its parent class. So if an attribute of a derived rule is overridden by a child's class rule for a specific class, then the derived rule has no effect on
 that attribute. This behavior applies also when the child's reconciliation rule is static and the parent's rule is dynamic (dynamic reconciliation rules have precedence over static reconciliation rules when they are for same
 level class).

For example, rule #1 above lets Discovery update the
name
attribute in the
cmdb_ci_computer
class and all of its child
 classes. However, rule #2 for the
cmdb_ci_linux_server
child
 class, which overrides rule #1 for the parent class, explicitly authorizes
 ServiceWatch to update this attribute in the child class.

As a result:
- Discovery cannot update the name attribute of the child cmdb_ci_linux_server class. Only ServiceWatch is
 authorized to update this attribute.
- Discovery is authorized to update the name attribute of
 CI records in all other child classes of the cmdb_ci_computer class.
Overlapping static reconciliation rules
Static reconciliation rules that authorize different discovery sources for the same
 attributes of the same class can coexist and do not exclude each other.

For example, assume the following rule is added. It is similar to example rule #1
 above but authorizes a different discovery source:

ServiceWatch is authorized to update the
name
attribute in the
cmdb_ci_computer
class.

Like example rule #1 above, this new rule applies to the
name
attribute in the
cmdb_ci_computer
class so both Discovery and
 ServiceWatch can update the attribute. Any reconciliation rules are enforced to
 prevent the discovery sources from overwriting each other's updates.

For more information about reconciliation rules, see the
[CMDB - Data Precedence Rules] Understanding the CMDB data precedence rules and troubleshooting [KB0756709]
knowledge base article.

## Domain separation

If
 Domain
 Separation is enabled, then you can scope reconciliation rules to specific domains. Rules of
 the parent domain, if not overridden, apply to CIs of child domain. All rules that are
 visible to a domain are applied, and a rule overriding the parent domain displays thele
 child domain version.

Understanding the CMDB reconciliation rules and
 troubleshooting [KB0756709]
