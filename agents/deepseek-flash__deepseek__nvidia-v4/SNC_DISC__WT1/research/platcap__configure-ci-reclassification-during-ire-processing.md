# Configure CI reclassification during IRE processing

- Source: https://www.servicenow.com/docs/r/zurich/servicenow-platform/configuration-management-database-cmdb/c_CIReclassification.html
- Release: Zurich
- Map: platcap

---

# Configure CI reclassification during IRE processing

During the Identification and Reconciliation Engine (IRE) CI identification process, a
 CI might need to be reclassified to a different
sys_class_name
type. By
 default, CIs are reclassified automatically. If automatic reclassification is disabled, then the
 CI is not reclassified and the system generates a reclassification task for your
 review.

The class of a CI can be upgraded, downgraded, or switched to a different branch in the class
 hierarchy. For more details about reclassification operations, see
Reclassify a CI
. You can use system properties and payload
 flags to configure the IRE behavior of CI reclassification, globally or individually per
 CI.
Note:
CI reclassification is possible only between two classes that have identical
 identification rules.

## Configure automatic CI reclassification using system properties

You can use system properties to configure system-wide IRE behavior for CI reclassification. For information about CI reclassification-related properties, including access, see
Properties
.

- The following properties enable or disable automatic reclassification updates that are
 specified in a payload. These properties are set to true in the
 base system, enabling processing of CI updates, including CI reclassification
 updates. To disable any automatic reclassification update, set the respective property to false . In that case, IRE rejects a payload (or a payload item
 in Enhanced IRE) with the respective reclassification updates, and creates a reclassification task . glide.class.upgrade.enabled glide.class.downgrade.enabled glide.class.switch.enabled
- The following properties enable IRE to process CI updates with reclassification
 operations. However, depending on the property setting, IRE processes or skips the
 reclassification update. These properties are set to false in the
 base system, in which case IRE processes CI updates including any CI
 reclassifications. Set a property to true to configure IRE to process CI updates
 but not the CI respective reclassification update. glide.identification_engine.update_without_switch_enabled glide.identification_engine.update_without_downgrade_enabled glide.identification_engine.update_without_upgrade_enabled This set of properties takes precedence over the previous set of properties
 (glide.class.<reclassification>.enabled). For example, with the following conflicting
 property settings, the second property takes precedence over the first: glide.class.downgrade.enabled = false glide.identification_engine.update_without_downgrade_enabled = true
Example for IRE processing of a payload item with a switch of a CI from Linux Server to
 Window Server. With the following default property settings in the base system, IRE updates
 the attributes including the class switch:
- glide.class.switch.enabled = true
- glide.identification_engine.update_without_switch_enabled = false
However, with the following property settings, IRE updates the attributes but skips the
 class switch:
- glide.class.switch.enabled = true
- glide.identification_engine.update_without_switch_enabled = true

## Configure automatic CI reclassification in input payloads

You can use flags which correspond to the system properties, in the input payload of the
CreateOrUpdateCIEnhanced()
or the
createOrUpdateCI()
â APIs. In the payload, set these flags to
true
or
false
to temporarily override the
 respective system property settings, at the payload item level.

For the following payload flags that control reclassification behavior, if any is set, the setting has precedence regardless of the setting of the corresponding
glide.class.xxx.enabled
property:
- classUpgrade
- classDowngrade
- classSwitch
For the following payload flags that control reclassification behavior, the system checks if either the flag or its corresponding
glide.identification_engine.update_xxx_enabled
property is true to allow the
 update without the respective reclassification operation:
- updateWithoutUpgrade
- updateWithoutDowngrade
- updateWithoutSwitch
Also, you can pass payload level settings (which apply to all items within a payload), per data source, by specifying CI reclassification properties on the Robust Import Set Transformers form. For more information, see
Robust import set transformer properties
.

The following sample JSON payload enables automatic reclassification for the specified CI:

{ items: [{className: 'cmdb_ci_server', classUpgrade: true, classDowngrade: true, classSwitch: true, values: {name: 'linux123', serial_number: '12srt567', ip_address: '10.2.3.4'}, }]}

## Reclassification restriction rules

Prevent IRE from downgrading or switching a CI class during payload processing to help
 prevent data loss. A reclassification restriction rule prevents a CI class change for
 specific source and target classes, while still processing any other property updates for
 the CI.

You can use a reclassification restriction rule, for example, to prevent a CI class downgrade from
cmdb_ci_linux_server
(source class) to
cmdb_ci_server
(target class). Or, to prevent a
 CI class switch from Linux Server to Windows Server. Reclassification restriction rules can be useful when using a Service Graph Connector which might lead to a class downgrade or switch, and a potential loss of important data.

To control the application of reclassification restriction rules:
- Use the glide.identification_engine.reclassification_restriction_rules_enabled system property to globally enable or disable the application of active reclassification
 restriction rules. This property is set to true by default.
- Use the skipReclassificationRestrictionRules payload flag in an
 IRE payload to prevent the application of active reclassification restriction
 rules. For example, a payload with the skipReclassificationRestrictionRules flag: {
 "items": [
 {
 "className": "cmdb_ci_server",
 "values": {
 "short_description": "Linux server description",
 "name": "Linux Server 1"
 },
 "settings": {
 "skipReclassificationRestrictionRules": "true"
 }
 }
 ]
}
For information about how to create a reclassification restriction rule, see
Create a reclassification restriction rule
.

## Create a reclassification restriction rule

Reduce data loss during IRE processing by preventing a CI class change for specific
 source and target classes. A reclassification restriction rule affects only the
Class
attribute and does not prevent the update to the rest of the
 CI properties.

### Before you begin

Role required: Itil_admin (Itil has read privilege only)

### About this task

If during IRE processing of a payload, a CI needs to be reclassified (downgrade or
 switch class), IRE checks reclassification restriction rules. If any
 reclassification restriction rule applies to the current CI reclassification, IRE
 processes the CI properties update, but skips the CI reclassification.

IRE output provides specific details about any processing related to reclassification
 restriction rules.

A reclassification restriction rule applies only to the direction between the
 specified source and the target classes. The rule doesn't prevent a reclassification
 in the opposite direction, from the specified target class to the source class. To
 restrict reclassification between two classes in both directions, specify two
 separate reclassification restriction rules, one for each direction.

### Procedure

- Enter cmdb_ire_reclassification_restriction.list in the
 filter navigator.
- Fill out the Reclassification Restriction form. Field Description Name Name of the reclassification restriction rule. Source table Current CI class. Source inheritance Whether to apply the reclassification restriction rule to
 child classes of Source
 table . Target class Reclassification target class. Target inheritance Whether to apply the reclassification restriction rule to
 child classes of Target
 table . Type CI reclassification type: Downgrade or Switch .
- Click Submit .

### What to do next

In the Reclassification Restrictions list view, you can
 activate or deactivate a reclassification restriction rule by setting its
Active
value to true or false.
