# Discovery resource utilization

- Source: https://www.servicenow.com/docs/r/zurich/it-operations-management/discovery/discovery-resource-utilization.html
- Release: Zurich
- Map: itom

---

# Discovery resource utilization

Summarize Summarized using AI This content was generated using new OpenAI-powered functionality. Results are provided on an as is basis and are not guaranteed to be accurate or complete. Summary of Discovery resource utilization This content details the network bandwidth and CPU usage associated with ServiceNow Discovery processes across various operating systems and device types. It provides specific data on how much network traffic is generated during discovery runs, helping customers understand and manage the resource impact of Discovery on their infrastructure. Show full answer Show less Discovery Bandwidth Consumption ServiceNow Discovery uses probes and patterns to collect data, generating network traffic that varies by device type and operating system. The information is segmented into data flows between the MID Server, Discovery instance, and target devices. Bandwidth by OS and Device Type: Tables quantify bandwidth usage in megabytes for Windows (various versions), Linux, Mac OSX, HP-UX, Solaris, Cisco UCS Switches, load balancers (F5, A10), and EMC Storage. For example, EMC Storage exhibits the highest total bandwidth usage among listed devices. Three-Tier Application Discovery: Initial discoveries consume significantly more bandwidth than subsequent ones. The data transfer is broken down by tiersâUI (Apache), application (Websphere), and data (Oracle)âallowing customers to plan for initial and incremental discovery loads efficiently. Pattern-Based Discovery: Bandwidth for pattern-based discoveries varies across OS types during creation and update scans, with Windows Server and Solaris showing higher data transfer volumes compared to others like HP-UX and network devices. Note: Measurements were taken under base operating configurations; actual customer environments may see different resource utilization depending on local system factors. CPU Usage Considerations CPU consumption during Discovery depends on numerous variables including operating system, chipset, and workload. Because of this complexity, customers should use internal templates to identify their specific system builds and continuously monitor CPU impact to optimize Discovery performance effectively.
Standard transactions on
Windows
and
UNIX
generate various amounts of network traffic, depending on what is being discovered.

These tables show the bandwidth consumption for each data flow segment of a typical
 discovery using probes and patterns over different operating systems.

Table 1. Discovery Bandwidth Over Different Operating Systems (in Megabytes)
Device Type MID > Instance Instance > MID MID > Target Target > MID Total
Windows 2016 0.104966 0.101271 0.77739 2.364353 3.34798 Windows 2012 0.126327 0.07928 1.177146 3.70751 5.089804 Windows 2008 0.141816 0.104674 1.032673 3.594784 4.873947 Windows 10 0.091466 0.075601 0.642313 2.221103 3.030483 Linux CentOS 0.164232 0.111376 0.148742 0.690117 1.114467 Mac OSX 0.103707 0.068302 0.021681 0.461365 0.655055 HP-UX 0.120358 0.106676 0.042669 0.101149 0.370852 Solaris 0.130551 0.099414 0.060243 0.346605 0.636813 Cisco UCS Switch 0.029655 0.027465 0.094918 0.097444 0.249492 F5 Load Balancer 0.043935 0.03689 0.017179 0.012132 0.110136 A10 Load Balancer 0.046631 0.032266 0.018313 0.03182 0.12903 EMC Storage 0.4776 0.373828 1.215954 4.741926 6.809308
The following table shows the bandwidth comparison between an initial discovery for three-tier applications and for each subsequent discovery. Bandwidth is broken up into the three tiers: UI (
Apache
), application (Websphere), and data (
Oracle
). This measures the total data transfer for each discovery run once for a device class.

Table 2. Discovery Bandwidth for Three Tier Applications (in Megabytes)
Device Type MID > Instance Instance > MID MID > Target Target > MID Total
Three-tier application - Initial discovery 0.712829 0.678862 7.084678 9.430181 17.90655 F5 Load Balancer 0.017179 0.012132 Apache on Linux 0.540161 1.107108 Websphere on Linux 0.729403 1.165112 Oracle on Windows 5.797935 7.145829 Three-tier application - subsequent discovery 0.150882 0.107409 2.536535 0.560122 3.354948 F5 load balancer 0.001347 0.012132 Apache on Linux 0.136366 0.79392 Websphere on Linux 0.341042 0.11365 Oracle on Windows 2.05778 0.354948
This table shows discovery of different OS types using patterns. This measures, in
 megabytes, the total amount of data created and the total amount of data in subsequent
 scans for each device.

Table 3. Discovery Bandwidth for Patterns over Different Operating System Types (in
 Megabytes)
Device MID > Instance Instance > MID MID > Target Target > MID Total
Linux Create 0.39 0.486 0.098 0.273 1.247 Update 0.382 0.499 0.093 0.264 1.238 Windows Server Create 0.289 0.316 5.628 8.508 14.741 Update 0.273 0.306 5.621 8.458 14.658 Solaris Create 1.222 1.4 0.383 0.917 3.922 Update 1.24 1.42 .399 .675 3.734 HP-UX Create 0.176 0.222 0.063 0.13 0.591 Update 0.178 0.247 0.062 0.128 0.615 Citrix Netscaler Create 0.424 1.919 0.019 0.042 2.404 Update 0.355 0.619 0.016 0.041 1.031 F5 Create 0.087 0.135 0.026 0.047 0.295 Update 0.132 0.171 0.026 0.047 0.376 L3 Switch Create 0.172 0.125 0.282 0.478 1.057 Update 0.178 0.126 0.282 0.479 1.065
Note:
These measurements were taken with base operating
 configurations. Your local system results may vary.

## CPU Usage examples

Examples from CPU Usage will vary among the matrix of thousands of combinations of Operating Systems, chip sets and specific loads for each system.

Your mix of these variables will determine your unique level of CPU consumption.

Use internal templates to identify unique builds. Monitor the performance impact that Discovery has on your system.
