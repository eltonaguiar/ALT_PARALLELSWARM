# Create a data refresh rule

- Source: https://www.servicenow.com/docs/r/zurich/servicenow-platform/configuration-management-database-cmdb/create-datasource-staleness-rule.html
- Release: Zurich
- Map: platcap

---

# Create a data refresh rule

Specify data refresh rules to determine
 if a CI is stale for a specific discovery source. Such CIs can then be updated by a
 lower-priority authorized discovery source.

## Before you begin

Role required: itil has read access, itil_admin (on top of itil) has full access.

## About this task

Data refresh rules are used in conjunction with static reconciliation rules to determine reconciliation steps for a CI. These rules determine if, when, and by which discovery source a CI can be
 updated.
The precedence order of applying reconciliation rules to a class, remains the same even when there are data refresh rules for that same class.

Data refresh rules have no impact when dynamic reconciliation rules are in effect.

## Procedure

- Navigate to All > Configuration > CI Class Manager .
- Select Hierarchy to show the CI Classes list and then select the class for which to create a data refresh rule.
- In the class navigation bar, expand Class Info and then
 click Reconciliation Rules .
- Create a rule by selecting Add in the Data Refresh Rules section, or select an existing rule to edit. Then fill out the details in the Create Data Refresh Rules dialog box. Field Description Discovery source Discovery source for which staleness is evaluated. Effective Duration The time period that is used for the staleness test. If the fields specified in the static reconciliation rule for the CI's class weren't updated by Discovery source within the specified Effective Duration â the CI
 is determined to be stale for Discovery source and a lower priority discovery source is authorized to update the CI. When set to 0 (default), the CI is determined to be stale for Discovery source immediately after an update and therefor, a lower priority discovery source will always be authorized to
 update the CI. If you enter a value with a prefix that is valid and a suffix that is not, such as 15 x â the valid portion of the value is used ('15'). If the entire value is invalid â the default
 value of 0 is used. Active Activates the rule.
- Click Save .
