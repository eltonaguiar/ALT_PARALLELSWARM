# Discovery behaviors

- Source: https://www.servicenow.com/docs/r/zurich/it-operations-management/discovery/c_DiscoveryBehaviors.html
- Release: Zurich
- Map: itom

---

# Discovery behaviors

Summarize Summarized using AI This content was generated using new OpenAI-powered functionality. Results are provided on an as is basis and are not guaranteed to be accurate or complete. Summary of Discovery behaviors Discovery behaviors in ServiceNow control which probes the Shazzam tool launches and assign these probes to specific MID Servers. Each MID Server scans designated IP ranges, and behaviors enable distributing scanning tasks across multiple MID Servers, optimizing discovery of devices and configuration items (CIs) across networks and domains. This is essential for efficient, non-duplicative discovery in complex environments, such as those with multiple Windows domains, UNIX systems, and SNMP devices. Show full answer Show less Key Features Load balancing: Behaviors distribute discovery tasks among multiple MID Servers to balance workload and improve efficiency. Multi-domain and multi-protocol support: Behaviors assign different protocols and domains to specific MID Servers. For example, one MID Server can scan all protocols on one domain while another handles WMI scans on a second domain. Access Control List (ACL) handling: Behaviors enable scanning of SNMP devices protected by ACLs by configuring MID Servers that have appropriate access. Protocol-specific device scanning: Behaviors can specify which protocol (e.g., SSH or SNMP) to use for devices running multiple protocols, preventing duplicate scans. Discovery functionality records: Each behavior contains one or more functionality records defining protocols to scan, associated MID Servers, execution phases, and criteria (especially for Windows MID Servers in multi-domain scenarios). Practical Application for ServiceNow Customers Behaviors are used within Discovery schedules to efficiently manage and coordinate scanning activities across MID Servers and network segments. They ensure: Efficient use of MID Servers by avoiding duplicate scans. Support for complex network topologies, including multiple Windows domains and mixed protocol environments. Compliance with network security controls such as ACLs. Flexibility in defining which servers scan which protocols and devices. For example, in an environment with two Windows domains and various UNIX and SNMP devices, behaviors can direct each domainâs Windows MID Server to scan its domain and assign SSH and SNMP device scans appropriately, all within a single Discovery schedule. Creating and Using Discovery Behaviors ServiceNow customers can create Discovery behaviors to specify which MID Servers perform which probes and protocols. Load balancing can be configured to automatically distribute work when multiple MID Servers scan the same protocols. Functionalities are grouped into phases to control execution order, and criteria can be set to ensure correct processing of discovery results, particularly in multi-domain Windows environments. Common Functionality Definitions Some typical protocol scanning configurations include: Windows only (WMI): Scans Windows devices using WMI, requiring Windows MID Servers and domain criteria. SNMP only: Scans SNMP devices, useful for devices protected by ACLs, without requiring domain criteria. All except SNMP: Scans all protocols except SNMP, often used with a separate SNMP-only MID Server. All except Windows (no WMI): Scans SSH and SNMP but excludes WMI, useful for non-Windows devices or different MID Servers per protocol. Key Outcomes Improved discovery efficiency through task distribution and load balancing. Accurate and secure scanning across multiple network domains and protocols. Reduced duplication of discovery efforts, saving time and resources. Enhanced ability to discover diverse device types and adhere to network security policies.
Discovery
behaviors determine the probes that Shazzam launches and from which
MID Servers
these probes are launched.

A scan performed by a single
MID Server
targets a designated IP address range. A behavior can assign different tasks to multiple
MID Servers
on the same IP address segment or on different network segments. Behaviors are available in
Discovery schedules
for discoveries that update configuration items (CIs) in the
Configuration Management Database (CMDB)
.

You can use behaviors in the following scenarios:
- Load balancing: A behavior enables load balancing in systems that use multiple MID Servers deployed across one or more domains.
- Multiple protocols in multiple domains: A behavior can configure one MID Server to scan for all protocols on one domain and another MID Server to perform a WMI scan on a second domain.
- Access control lists (ACLs): Discovery can scan SNMP devices protected by an ACL if the MID Server host machine is granted access by that ACL. A behavior can configure a MID Server to scan devices protected by an ACL.
- Devices running two protocols: Some devices run two protocols at the same time, most commonly SSH and SNMP. A behavior can control which of the two protocols is explored for certain devices. The behavior then excludes the
 other protocol from exploration.
Behaviors enable
Discovery
of SSH and SNMP devices and WMI devices running on multiple
Windows
domains by using multiple
MID Servers
.

For example, an organization has two
Windows
domains in its network and a variety of
UNIX
computers and SNMP devices. The challenge is to discover all the devices efficiently, without duplicating effort. Each domain contains a
Windows
MID Server
, which is used to scan the IP addresses from the two domains specified in the
Discovery
schedule, and the SSH and SNMP devices. Use a behavior to divide the work so that no device is scanned twice. In this example, both domains are in the same geographical location, and a single schedule
 is sufficient.
Note:
To run
Discovery
over multiple
Windows
domains, use
PowerShell
, which enables a single
MID Server
to authenticate on machines on different domains using credentials stored on the instance.

## Discovery functionalities

Each behavior contains one or more
Discovery
functionality records. A
Discovery functionality defines what each MID Server in this behavior must do, specifically which protocols to detect.

A functionality record links the following items:
- Functionality definition: The protocol or list of protocols that the MID Servers in the functionality scan. Several definitions are available by default, and you can also create custom definitions.
- MID Servers : The MID Servers that perform the functionality. When you select multiple MID Servers , Discovery balances the load across them.
- Phase: An integer that groups functionalities. Functionalities in the same phase run together in one Shazzam probe, and phases run in numerical order.
- Functionality criteria: Conditions that determine which MID Server processes the Shazzam results, based on the MID Server name ( mid_server ), the target domain ( win_domain ), or the MID Server domain ( mid_win_domain ). Criteria are required only for Windows MID Servers , and only when the behavior controls Discovery across multiple domains.
The following table lists some common functionality definitions. For the full list, view the records in the Functionality Definition [discovery_function_def] table by navigating to
All > Discovery > Discovery Definition > Functionality Definitions
.
Table 1. Common functionality definitions
Functionality Description
Windows only (WMI) Scans for Windows devices using the WMI protocol. Requires a Windows MID Server and functionality criteria to specify the domain. Windows , DNS, and WINS Scans for Windows devices using the WMI protocol and resolves the domain using DNS and WINS. Requires a Windows MID Server and functionality criteria. SNMP only Scans for SNMP devices only. Use this when scanning devices protected by an ACL that restricts SNMP access to specific MID Server hosts. Does not require functionality criteria. All except SNMP Scans for all protocols except SNMP, including WMI and SSH. Use this in combination with SNMP only functionality when you need separate MID Servers for SNMP and other protocols. All except Windows (no WMI) Scans for all protocols except WMI, including SSH and SNMP. Use this in combination with Windows only functionality when scanning multiple domains or when non- Windows devices require a different MID Server .
