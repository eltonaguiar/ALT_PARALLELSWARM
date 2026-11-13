# Exploring Discovery

- Source: https://www.servicenow.com/docs/r/zurich/it-operations-management/discovery/c_GetStartedWithDiscovery.html
- Release: Zurich
- Map: itom

---

# Exploring Discovery

Summarize Summarized using AI This content was generated using new OpenAI-powered functionality. Results are provided on an as is basis and are not guaranteed to be accurate or complete. Summary of Exploring Discovery Discovery in ServiceNow identifies computers, servers, printers, IP-enabled devices, and applications, then updates the Configuration Management Database (CMDB) with the collected data. It supports two main discovery techniques: horizontal discovery, which scans networks to find devices and their direct relationships, and top-down discovery, used by Service Mapping to map business services and their dependencies. Show full answer Show less Discovery Techniques Horizontal discovery: Finds devices and creates direct CI relationships (e.g., applications running on specific computers) without awareness of business services. Top-down discovery: Used by Service Mapping to identify CIs within business services and map their interdependencies, providing IT teams with clear service dependency views. Typically, horizontal discovery runs first to identify CIs, followed by top-down discovery to establish business service relationships. Key Components Probes and sensors: Scripts that collect and process data on devices. Probes explore devices, while sensors interpret probe data and update the CMDB. These can be customized or created to meet specific discovery needs. Patterns: Sequences of operations written in Neebula Discovery Language (NDL) that collect data and update the CMDB, invoked in later discovery stages and customizable via the Pattern Designer. MID Servers: Secure, agentless communication intermediaries that execute probes or patterns, initiate all communications inside the firewall using SOAP over HTTPS, and return results to the ServiceNow instance for processing. Horizontal Discovery Phases Scanning: The Shazzam probe scans network ports to detect devices and their types. Classification: Additional probes determine device types and operating systems using classifiers that trigger subsequent probes or patterns. Identification: Discovery gathers detailed device data, checks for existing CIs, and updates or creates CIs using identification rules. Exploration: Further probes collect detailed attributes and applications on devices, establishing relationships between applications and devices. Types of Horizontal Discovery Network discovery: Finds internal IP networks; optional if IP ranges are already known. CI discovery: Standard discovery for devices, computers, and applications on the network. Cloud discovery: Discovers AWS and Azure cloud resources. Serverless discovery: Finds applications on hosts without requiring host discovery first, relying on patterns. IP Service Affinity This feature records the successful IP service (e.g., SSH, SNMP) used to discover a device and associates it with the device's IP address. This optimizes subsequent discoveries by targeting the correct protocol first, improving accuracy and efficiency. Practical Benefits for ServiceNow Customers Automates discovery of IT infrastructure and applications without installing agents on devices. Provides detailed and accurate CMDB updates, supporting IT service management and operations. Enables clear visualization of device relationships and business service dependencies, enhancing impact analysis and troubleshooting. Supports flexible customization of discovery processes through probes, sensors, and patterns to adapt to unique environments. Ensures secure, agentless communication within enterprise networks via MID Servers without complex firewall configurations.
Discovery finds computers, servers, printers, a variety of IP-enabled devices, and the applications that run on them. It can then update the configuration items (CIs) in your Configuration Management Database (CMDB) with the data it collects.

## Horizontal discovery and top-down discovery

There are two types of discovery:
Horizontal discovery
Horizontal discovery is a technique that
Discovery
uses to scan your
 network, find computers and devices, and then populate the CMDB with the CIs it
 finds. Horizontal discovery creates direct relationships between CIs, such as a
runs on
relationship between an application CI and the actual
 computer CI that it runs on. Horizontal discovery is not aware of business services
 and does not create relationships between CIs based on the business service they are
 in.

Top-down discovery
Top-down discovery is a technique that Service Mapping uses to find and maps CIs
 that are part of business services, such as an email service. For example, top-down
 discovery can map a website business service by showing the relationships between an
 Apache Tomcat web server service, a Windows server, and the MSSQL database that
 stores the data for the business service. This gives IT teams a clear view of service dependencies.

Typically,
Service Mapping
and
Discovery
work
 together. Horizontal discovery runs first to find CIs, and then top-down discovery
 establishes the relationships between business services.

## Probes, sensors, and patterns

Discovery
uses these components to find CIs:
Probes and sensors
Probes and sensors are scripts that collect and process data on a host and then
 update the CMDB. More specifically, probes explore or investigate CIs on your network,
 and sensors parse the data returned from the probes. Several probes and sensors are
 provided by default, but you can customize them to find different information, or you
 can create ones. You can also configure several parameters to control the behavior of
 a particular probe every time it is triggered.
Patterns
Patterns, like probes and sensors, are a series of operations that also collect data
 on a host, process it, and update the CMDB. Patterns differ from probes and sensors in
 that they are written in Neebula Discovery Language (NDL) rather than JavaScript. They
 are called into action in the later stages of the horizontal discovery process.
 Default patterns are provided, but you can also customize or create patterns using the
 Pattern Designer.

## Horizontal discovery phases

The phases of horizontal discovery are:

Discovery
follows these phases:
Scanning
Discovery
sends a probe called
Shazzam
to the network to see if commonly used ports are open
 and if these ports can respond to queries. For example, if Shazzam finds a device that responds on port 135,
Discovery
knows that itâs a Windows server.
Classification
If
Discovery
finds devices or computers, it sends additional probes to find the type of device or the
 operating system on the device. For example,
Discovery
sends the WMI probe to a Windows machine to detect the Windows 2012 operating system. Then
Discovery
uses records called
classifiers
, which specify the trigger probe or probes that run
 during the next two phases. If youâre using patterns, the classifier specifies a trigger probe that in turn launches a pattern.
Identification
Discovery
tries to gather more information about the device and then tries to determine if a CI for the
 device exists in the CMDB.
Discovery
then uses additional probes, sensors, and identifiers to update existing CIs in the CMDB or
 create new ones.
Identifiers
, also known as identification rules, specify the attributes that the probes look at when reconciling data with the CIs in the CMDB. If youâre using patterns,
Discovery
uses the appropriate identification rule for the CI type specified in the pattern.
Exploration
The identifier launches additional probes configured in the classifier. These probes gather additional information about the device, including the applications running on it and attributes such as memory, network
 cards, and drivers.
Discovery
then creates relationships between applications and devices and between applications. If youâre
 using patterns, the operations in the pattern perform the exploration of the CI.

## Discovery communication through MID Servers

A
MID Server
, which
 constantly queries the instance for probes to run, executes the instructions in the probe or
 in the pattern that the probe specifies. The MID Server then returns the results to the
 instance, where sensors process it. The MID Server does not retain any discovery
 information.

The MID Server starts all communications, using SOAP on HTTPS, which means that all
 communications are secure, and all communications are initiated inside the enterprise's
 firewall. No special firewall rules or VPNs are required.

Because Discovery is agentless, it does not require any permanent software to
 be installed on any computer or device. The MID Server uses several
 techniques to probe devices without using agents. For example, the MID Server uses SSH to
 connect to a Unix or Linux computer, and then it can run a standard command, as specified in
 the probe, to gather information. Similarly, it uses the Simple Network Management Protocol
 (SNMP) to gather information from a network switch or a printer.

## Types of discovery

The types of horizontal discovery that the
Discovery
application can perform are
 explained in the following table:

Type Description
Network discovery Run this type of discovery to find the internal IP networks within your
 organization. If you already know the IP address ranges in your network, it is not
 necessary to run network discovery. CI discovery Run this type of discovery to find the devices, computers, and applications
 on your network. This is essentially the standard type of discovery that you run
 most often. Cloud discovery Run this type of discovery to find AWS and Azure resources in your
 organization's cloud. Serverless discovery Run this type of discovery to find applications on host machines without the
 need to discover the host first. Serverless discovery relies on patterns to
 explore CIs on a host.

## IP service affinity

IP Service affinity saves the IP service information that is used to successfully find a
 device and associates it with the IP address of the device. Using this information,
Discovery
can target the device in
 subsequent runs with the accurate protocol.
Discovery
records the IP Service along
 with the IP address.
Discovery
can
 store the successful IP service information in the IP Service Affinity table
 [ip_service_affinity].

For example: A network device has both an SSH port and an SNMP port open. By its agentless
 design,
Discovery
tries SSH first.
 However, network devices should be discovered through SNMP.
Discovery
tries the SSH probe and it
 fails. This triggers the SNMP probe, which succeeds. With the association between the IP
 address and the IP service, subsequent discovery runs targeting this IP address use SNMP
 first, because that is the probe that succeeded.
