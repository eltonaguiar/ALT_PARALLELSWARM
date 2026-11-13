

[S1] Discovery properties
SOURCE: ServiceNow docs Brazil / discovery-properties

Discovery properties
Release version: Brazil
Updated September 10, 2026
26 minutes to read
Discovery properties enable you to control several aspects of the horizontal discovery process.
For information about the Discovery properties that Agent Client Collector uses, see Using push-based and horizontal IP-based Discovery together .
Edit the following Discovery properties by navigating to Discovery Definition > Properties .
IP properties
[TABLE]
Field |
Description |
glide.discovery.exclude_ip_sync_classes |
Defines CI classes whose IP addresses shouldn’t be substituted if the address returned by Discovery doesn’t match one of the devices' NICs. Use a comma-separated list to define multiple classes. By default, the
system uses the management IP of a load balancer returned by Discovery in the CI record, rather than substituting it for the IP address of one of the load balancer's NICs.
Type : string
Default value : cmdb_ci_lb
|
glide.discovery.enforce_unique_ips |
Enforce unique IP addresses: Ignores the IP address after Discovery encounters subsequent devices that use the same IP address. Each time a computer, printer, or network device with a valid IP address is discovered, the IP address field is cleared on
any other device sharing that address. If inactive, stores the IP address for each device.
Type : true | false
Default value false
|
[/TABLE]
Network properties
[TABLE]
Field |
Description |
glide.discovery.bgp_router_disable |
BGP router exploration disable: Disables running the SNMP – Routing probe or pattern when discovering a router running the BGP protocol. This exploration is inactive by default because BGP routing tables are large. These routers typically
operate at the edge of large networks, where further network discovery is not relevant. Set this value to false if your organization uses BGP routers as edge routers between relatively small networks. For example, between buildings on a single campus.
If you must populate the [discovery_device_neighbors] table during horizontal layer 2 discovery of the bgp-enabled devices, set the BGP router exploration disable property to
No . Notice that enabling this property can cause performance issues including out-of-memory issues on the MID Server.
Type : true | false
Default value : true
|
glide.discovery.debug.network_discovery |
Network discovery debugging: Enables extensive logging of all Network Discovery activities on the instance.
Type : true | false
Default value : true
Learn More : Discovery monitoring and issue resolution
|
glide.discovery.discoverable.network.max.netmask.bits |
Maximum netmask size for discoverable networks (bits): The maximum number of bits in a regular netmask for networks that are discovered by Network Discovery . A regular netmask is a netmask that can be expressed in binary as a string of ones followed by a string of zeroes. For example, 255.255.255.0 is regular and 255.255.255.64
is irregular. Regular networks are commonly expressed like: 10.0.0.0/24, which means a network address of 10.0.0.0 with a netmask of 255.255.255.0. Larger bit numbers mean networks with smaller numbers of
addresses in them. For example, the network 10.128.0.128/30 has four addresses in it: one network address (10.128.0.128), one broadcast address (10.128.0.131), and two usable addresses (10.128.0.129 and
10.128.0.130). Small networks are commonly configured in network gear to provide loopback addresses or networks used strictly by point-to-point connections. Since these sorts of networks generally don't need to be
discovered by Network Discovery , it would be useful to filter them out. By setting this property to a value of 1 through 32, you can limit the sizes of regular networks that are discovered. Setting it to any other
value causes all networks to be discovered. Irregular networks are always discovered. The default value is 28, which means that regular networks with 8 or fewer addresses cannot be discovered.
Type : integer
Default value : 28
|
glide.discovery.network_owner_method |
Network router selection method: This property controls the method used to decide (during Network Discovery ) which router should be selected as the router to be associated with a given IP Network. The possible values are:
First Router : The first router that discovers the network is associated
Last Router : The last router that discovers the network is associated
Most Networks : The router with the most attached networks is associated
Least Networks : The router with the least attached networks is associated
Type : choice list
Default value : Most Networks
Additional options : First Router, Last Router, Least Networks
|
glide.discovery.physical_interface_types |
Physical interface types: A comma-separated list of interface types that are considered physical for the purposes of network discovery. If a router (or device capable of routing) has an interface of
this type, the networks connected to that interface are considered locally connected to that device. The default interface types include Ethernet, 802.11, and Token Ring types. Interface type numbers are defined in
the SNMP MIB-2, specifically in OID 1.3.6.1.2.1.2.2.1.3.
Type : string
Default value : 6,117,9,71,209
|
glide.discovery.switch_interface_types |
Switch interface types: A comma-separated list of interface types that are considered. Interface type numbers are defined in the SNMP MIB-2, specifically in OID 1.3.6.1.2.1.2.2.1.3. Devices with any interface
types that do NOT appear in this list are classified as routers, when they have routing. A complete list of the interface type numbers may be found on the IANA web site , in the section "ifType definitions".
Type : string
Default value : 7,8,9,26,53,62,69,71,78,115,117,209
|
[/TABLE]
Other Discovery properties
[TABLE]
Field |
Description |
com.snc.use_external_credentials |
Allows the use of external storage of credentials.
Type : true | false
Default value : true
|
com.glide.codesigning.tracking.unsupported_script_tracking.enabled
|
Controls script tracking for code signing on Cloud Discovery . When set to true and code signing is enabled, ECC queue records inserted through unsupported scripts are not notarized, which can cause Cloud Discovery operations to fail. Set this property to false to enable Cloud Discovery on code-signed instances.
Type : true | false
Default value : true
Learn more : Configure Cloud Discovery for code-signed instances
|
com.glide.queue.discovery.cloud.sensors.processing_jobs.priority |
Manages the background job's worker priority for Cloud-based Discovery jobs when using Event Framework. Increasing the value decreases the priority.
Type : integer
Default value : 100
Note: This behavior only applies when discovery.use.event.processing is set to true .
|
com.glide.queue.discovery.sensors.processing_jobs.priority |
Manages the background job's worker priority for IP-based Discovery jobs when using Event Framework. Increasing the value decreases the priority.
Type : integer
Default value 

[S2] Set up Discovery without Guided Setup
SOURCE: ServiceNow docs Brazil / discovery-config-steps

Set up Discovery without Guided Setup
Release version: Brazil
Updated September 10, 2026
3 minutes to read
If you aren’t using Guided Setup, you must perform several configuration steps manually to activate the application, set up the MID Server, and then set up Discovery.
Before you begin
Grant Discovery role: Confirm that users who are expected to configure and execute Discovery in your network have the discovery_admin role. This role grants access to the tables in the Discovery application.
Designate a computer to host the MID Server.
Gather the login credentials that the MID Server must use to access the devices it’s expected to discover.
Determine which IP addresses Discovery must scan. In a highly complex network, group IP ranges into a range sets, which are reusable for different schedules. Discovery doesn’t scan anything outside of these ranges.
Role required: discovery_admin
About this task
Procedure
Install one or more MID Servers on physical or virtual servers that meet the
MID Server system requirements and configure them to communicate with the
appropriate ServiceNow
instance.
Install at least two MID Servers at first and assign them to different
schedules and IP ranges to help complete discoveries quicker. Starting with the
Istanbul release, you must make sure that the MID Server is assigned the
Discovery application or the ALL application.
Verify MID Server connectivity by navigating to Discovery > MID Servers .
If the MID Servers are configured properly, they appear in the list of MID Servers.
If a MID Server doesn’t appear as a choice in the instance, perform the following checks:
Verify that the URL in the Configuration Parameters related list provided is correct.
If the MID Server is installed on Windows , make sure the ServiceNow MID Server service is configured properly with the correct login credentials and is running.
Check the MID Server log for errors.
On the instance, navigate to Discovery > MID Servers > [MID Server] > Logs .
On the MID Server host, navigate to the agent\logs\agent0.log0 directory.
If Basic Authentication is enabled, a user name and password must be provided.
The MID Server might not have outbound access on port 443 (SSL) or a proxy server might be preventing TCP communication to the instance.
Make sure that no firewalls are blocking communication between the MID Server and the instance.
Set the
credentials on the instance for all the
computers, printers, and network gear in your environment.
Credentials for Windows devices (using the WMI protocol) are provided by the login configured for the MID Server service on the Windows server host. Credentials for UNIX , vCenter, and SNMP must be configured on the instance. Discovery automatically determines which credentials work for a particular computer or device.
Define and run Discovery
schedules .
The Discovery Schedule is the control point for running discoveries. The schedule controls when Discovery runs, defines the MID Server to use, the type of Discove

[S3] Discovery Schedule form reference
SOURCE: ServiceNow docs Brazil / discovery-schedule-form

Discovery Schedule form reference
Release version: Brazil
Updated November 5, 2026
9 minutes to read
The Discovery Schedule form provides details about the configuration items (CIs) targeted for discovery, the associated MID Server, and the schedule settings for the discovery run.
For instructions on this procedure, see Schedule a horizontal discovery .
[TABLE]
Table 1. Discovery Schedule Form
Field |
Description |
Name |
Enter a unique, descriptive name for your schedule. |
Discover |
Select one of the following scan types:
Configuration items : Uses Discovery identifiers to match devices with CIs in the CMDB and update the CMDB appropriately. Perform a simple discovery by selecting a specific MID Server to scan for all protocols (SSH, WMI, and SNMP). Or, perform advanced discoveries with discovery behaviors. When you select a behavior, the MID Server
field isn’t available. Note: An IPv6 via address list scan is enabled on Discovery schedule for Configuration Items.
IP addresses : Scans devices without the use of credentials. These scans discover all the active IP addresses in the specified range and create device history records, but
don’t update the CMDB . IP address scans also show multiple IP addresses that are running on a single device. Identify devices by class and by type, such as Windows computers and Cisco network gear. The Max range size Shazzam probe property determines the maximum number of IP addresses Shazzam scans. See Configure Shazzam probe for details.
Networks : Discovers IP networks (routers and switches). Results from this search are used to populate the IP Network [cmdb_ci_ip_network] table in Discovery > IP Networks with a list of IP addresses and network masks. Network scans update routers and layer 3 switches in the CMDB .
Service : Discovers services for the Service Mapping application. See Schedule a top-down discovery by Service Mapping for instructions.
Serverless : Finds CIs without needing to run discovery on a host, or CIs on a proxy host that is already in the CMDB . See Serverless Discovery for more information.
Cloud application : Discovers only the cloud resources for the patterns that you specify. See Discovery for cloud environment for instructions.
Cloud resources : Discovers resources for one of the supported cloud providers . This option only appears when you run Discovery on a cloud service account. You can’t select it from a new Discovery schedule.
Certificates . Discovers certificates based on URLs. Selecting this option adds the Certificate Discovery Type field: URL Certificate Discovery. See Run Certificate Discovery via individual URL scans for more information.
|
MID Server selection method |
Select the method that Discovery uses to select a MID Server :
Auto-Select MID Server : Enable Discovery to select the MID Server automatically based on the discovery IP ranges you configure. To find a matching MID Server , you must configure MID Servers to use:
The Discovery application, or ALL applications. This setting authorizes the MID Server access from Discovery .
The IP range that includes the ranges you configure on the discovery schedule.
Note: MID Server auto-select isn’t supported with IPv6.
Specific MID Cluster : Use a preconfigured cluster of MID Servers . Select the cluster. You aren’t required to specify one member of the cluster. The MID Server can’t be part of multiple clusters, such as one that supports load balancing and one that supports failover. You can add any cluster regardless of the application
that the MID Servers are assigned to. When you select the cluster, the Discovery application is automatically added when it doesn’t exist for the MID Servers in the cluster.
Specific MID Server : Use only one MID Server . If that MID Server is part of a cluster, only that MID Server is used. The cluster isn’t used. You can add any MID Server regardless of the application it’s assigned to. The Discovery application is automatically added when it isn’t already assigned for the MID Server you select. You can assign a specific MID Server for all types of Discover scans except Service .
Use Behavior : Use a behavior when a single schedule requires the use of multiple MID Se

[S4] Discovery Configuration Console
SOURCE: ServiceNow docs Brazil / discovery-config-console

Discovery Configuration
Console
Release version: Brazil
Updated September 10, 2026
12 minutes to read
Use the Discovery Configuration Console to manage what kind of configuration items (CIs) and CI information you want to discover.
By default, Discovery finds all the information on your network that is specified in probes and patterns. Use the controls in this console to select the data Discovery adds to the Configuration Management Database (CMDB) that your organization needs. You can control these aspects of Discovery :
The discovery of entire CI types, such as Windows servers.
The discovery of specific CI details, such as OS information on Windows servers.
The discovery of ARP data for Networks, UNIX , and Windows devices.
The discovery of software packages containing keyword terms that you add, such as Hotfix or Security Update.
File-based Discovery of software on UNIX and Windows by particular extension or folder, such as .cert or .ext.
Note: Discovery returns all data from the target to the instance before applying console settings. The instance ignores any excluded data when it updates the CMDB .
Requirements and accessibility
If you use Internet Explorer, you must use version 8 or
later. The configuration console supports keyboard navigation and screen readers.
Console overview
To open the configuration console, navigate to Discovery Definition > Configuration Console .
The console is divided into these sections. Use the toggle buttons to enable various options.
Devices : network devices such as printers, storage devices such as storage switches, and Unix and Windows computers
Applications : automation applications such as Puppet, databases such as MSSQL, and web servers such as Tomcat
Software Filter : UNIX and Windows applications that include or exclude keywords that you enter
File-based Discovery : software files by path, folder, and extensions to scan or ignore
Device Discovery
Disabling the discovery of device data at the top level disables the related