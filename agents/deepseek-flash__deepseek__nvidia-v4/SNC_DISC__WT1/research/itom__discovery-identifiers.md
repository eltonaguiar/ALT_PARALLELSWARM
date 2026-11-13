# Discovery identifiers

- Source: https://www.servicenow.com/docs/r/zurich/it-operations-management/discovery/c_DiscoveryIdentifiers.html
- Release: Zurich
- Map: itom

---

# Discovery identifiers

Summarize Summarized using AI This content was generated using new OpenAI-powered functionality. Results are provided on an as is basis and are not guaranteed to be accurate or complete. Summary of Discovery identifiers Discovery identifiers in ServiceNow are used after Discovery classifies a configuration item (CI) to accurately determine if the device already exists in the CMDB. This process prevents duplicate CIs by using identity probes and sensors to collect identification data like serial numbers, names, and network information. This identification applies only to the Configuration item type of Discovery, ensuring precise matching and appropriate actions such as updating existing CIs or creating new ones. Show full answer Show less Key Features Identity Probes and Sensors: Discovery launches identity probes that gather device information through multiple simple probes. Sensors process this data to help identifiers find matching CIs in the CMDB. Identifier Rules: These rules define how Discovery matches devices to CIs using attributes such as serial numbers, IP addresses, MAC addresses, and device names. Each rule applies to specific CI classes or tables. Matching Strategy: Custom identifiers can be created for specific CI classes, enabling tailored matching strategies (e.g., using machine name, IP, and MAC for Linux servers). This is crucial in complex network scenarios like NIC bonding. Evaluation Order: Identifiers are evaluated in order based on configurable sequence numbers, allowing customization of how and when identifiers run during the Discovery process. Duplicate CI Handling: Properties such as glide.identificationengine.skipduplicates and its threshold control how Discovery manages duplicate CIs. Identifier Versions: New identifiers use the CMDB Identification and Reconciliation framework, with a property to enable them if upgrading from older versions. Service Mapping uses the new identifiers by default. Practical Considerations for ServiceNow Customers Serial Numbers: Ensure serial numbers are accurately discovered and not altered by customizations, as they are vital for reliable asset tracking. Custom Identifiers: When creating or editing identifier rules, avoid changing adapter names if using the name attribute to prevent unintended CI duplication. Upgrades: When upgrading from versions before Geneva, manually enable the new identifier framework to benefit from improved identification capabilities. Extensibility: Identity probes and sensors can be customized or extended to identify CIs not covered by default Discovery configurations. Key Outcomes Reliable and accurate identification of CIs during Discovery reduces duplicate records in the CMDB. Customizable identifier rules allow alignment with organizational and network-specific requirements. Improved asset tracking through consistent use of serial numbers and other key attributes. Flexible configuration and upgrade paths maintain identification accuracy as your environment evolves.
After
Discovery
classifies a configuration item (CI), it uses identifiers to determine if the device already exists in the
CMDB
.

Discovery
launches special identity probes that accumulate identification data for each device and feed that data into the identifiers. The identifiers determine the action that
Discovery
must take for each device. Identifiers accurately determine the identity of the device to avoid the creation of duplicate CIs. This identification step only takes place for the Configuration item type
 of discovery, not for the other types of discovery.

The identity probe in the base
Discovery
system can be configured to ask the device for information such as its serial numbers, name, and network identification. The results of this scan are processed by an identity sensor, which then passes
 the results to the identifier. The identifier then attempts to find a matching device in the
CMDB
. If the identifier finds a matching CI, the identifier either updates that CI or does nothing. If the identifier cannot find a matching CI, it either creates a new CI or does nothing.
 If
Discovery
is configured to continue, the identifier launches the exploration probes configured in the classification record to gather additional information about the device. Exploration probes can be
 multiprobes or simple probes.
Important:
Serial numbers are necessary for accurate asset tracking. If you modified baseline probes, sensors, or patterns, verify that they still discover serial numbers. In addition, do not configure
 sensors or patterns to modify the serial number syntax, such as adding a custom prefix. Non-standard serial numbers can lead to inaccurate asset tracking.

## CMDB identifier tables

Table Description
Identifier [cmdb_identifier] Stores all identifier rules. Identifier Entry [cmdb_identifier_entry] Stores all the identifier attributes.

## Identifier rules

The default
Discovery
system contains these identifier rules. Each rule is associated with a specific CI type (the
sys_class_name
field on the CI record) or the table in the
Applies to
field. Each rule also contains the appropriate attributes for discovering CIs from that table. Where necessary, tables from related lists (
Search on
tables) are included in the rule. For more information, see
Create or edit a CI identification rule
.

Table 1. CMDB identifier rules
Rule Applies to table/attributes Search on table/attributes
ESX Server Rule ESX Server [cmdb_ci_esx_server]: correlation_id none Hardware Rule Hardware [cmdb_ci_hardware] serial_number serial_number_type name ip_address mac_address Serial Number [cmdb_serial_number] serial_number serial_number_type Network Adapter [cmdb_ci_network_adapter] ip_address mac_address Storage Server Rule Storage Server [cmdb_ci_storage_server] cim_object_path name serial_number serial_number_type mac_address ip_address Serial Number [cmdb_serial_number] serial_number serial_number_type Network Adapter [cmdb_ci_network_adapter] ip_address mac_address WBEM Service Rule WBEM Service [cmdb_ci_wbem_service]: cim_object_path none

## Matching strategy for the hardware rule

The
sys_class_name
cannot be an attribute for independent rules, such as cmdb_ci_hardware. If your
Discovery
identification strategy depends on matching a CI with a specific class, create a rule for each class you want to use for matching. Specify that class in the
Applies to
field of the Identifier form.

For example, you can create an identifier for a
Linux
server with different attributes than the Hardware Rule. You might want to use the machine name, IP address, and MAC address for identification. This is a solution for networks that use NIC
bonding
or
teaming
to increase available bandwidth. Bonded interfaces appear to be the same physical device and share the same IP and MAC addresses. The use of the
name
attribute
 allows
Discovery
to differentiate between the individual interfaces in the bonded channel.
Important:
If you create an identifier with the
name
attribute, avoid changing adapter names.
Discovery
will be unable to resolve existing CIs for renamed adapters.
Discovery
labels the Install Status of that CI as "Absent" and creates another CI.
Your new rule would look like this:
Figure 1. Linux identifier rule

## Evaluation order for Discovery identifiers

Custom identifiers must have different
Order
values than those of the default identifiers.
Discovery
parses identifiers and attributes in sequence from low order numbers to high. You can create identifiers to run before or after the default identifiers, or mixed in with the identifiers from the base
 system. To avoid any identifier or rule from running, disable it by clearing the
Active
check box. The evaluation order for
CMDB
identifiers is established within each rule and only controls the parsing order of the attributes in that rule.

Figure 2. Evaluation order in CMDB identifier rules

## Properties for processing duplicate CIs

You can control how
Discovery
handles duplicate CIs with properties installed with Identification and Reconciliation. Use the
glide.identification_engine.skip_duplicates
and
glide.identification_engine.skip_duplicates.threshold
properties. For more information, see
Properties for Identification and Reconciliation
.

## Properties that control identifier versions

All instances use identifiers from the
CMDB
Identification and Reconciliation framework. Upgrades from pre-Geneva versions still preserve the legacy identifiers, but you can switch to the new identifiers using a property:
glide.discovery.use_cmdb_identifiers
. If you upgraded from a pre-Geneva version, you must manually add this property and set it to
true
to use the new identifiers. If you upgraded from
 Geneva or later releases, this property is available in the System Properties [sys_properties] table. To preserve functionality in custom legacy identifiers, convert them to the new
CMDB
identifier rules format before enabling this property. The system does not reconfigure your custom identifiers to the new framework automatically.
Note:
When
Service Mapping
is active, the new identifiers from the
CMDB
Identification and Reconciliation framework are always used regardless of the property value.
