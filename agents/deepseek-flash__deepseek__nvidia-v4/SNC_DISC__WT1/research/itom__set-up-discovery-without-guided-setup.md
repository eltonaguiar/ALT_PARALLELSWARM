# Set up Discovery without Guided Setup

- Source: https://www.servicenow.com/docs/r/zurich/it-operations-management/discovery/t_ConfigureDiscovery.html
- Release: Zurich
- Map: itom

---

# Set up Discovery without Guided Setup

If you arenât using Guided Setup, you must perform several configuration steps manually to activate the application, set up the MID Server, and then set up Discovery.

## Before you begin

- Grant Discovery role: Confirm that users who are expected to configure and execute Discovery in your network have the discovery_admin role. This role grants access to the tables in the Discovery application.
- Designate a computer to host the MID Server.
- Gather the login credentials that the MID Server must use to access the devices itâs expected to discover.
- Determine which IP addresses Discovery must scan. In a highly complex network, group IP ranges into a range sets, which are reusable for different schedules. Discovery doesnât scan anything outside of these ranges.
Role required: discovery_admin

## About this task

## Procedure

- Install one or more MID Servers on physical or virtual servers that meet the MID Server system requirements and configure them to communicate with the
 appropriate ServiceNow instance. Install at least two MID Servers at first and assign them to different
 schedules and IP ranges to help complete discoveries quicker. Starting with the
 Istanbul release, you must make sure that the MID Server is assigned the
 Discovery application or the ALL application.
- Verify MID Server connectivity by navigating to Discovery > MID Servers . If the MID Servers are configured properly, they appear in the list of MID Servers.
- If a MID Server doesnât appear as a choice in the instance, perform the following checks: Verify that the URL in the Configuration Parameters related list provided is correct. If the MID Server is installed on Windows , make sure the ServiceNow MID Server service is configured properly with the correct login credentials and is running. Check the MID Server log for errors. On the instance, navigate to Discovery > MID Servers > [MID Server] > Logs . On the MID Server host, navigate to the agent\logs\agent0.log0 directory. If Basic Authentication is enabled, a user name and password must be provided. The MID Server might not have outbound access on port 443 (SSL) or a proxy server might be preventing TCP communication to the instance. Make sure that no firewalls are blocking communication between the MID Server and the instance.
- Set the
 credentials on the instance for all the
 computers, printers, and network gear in your environment. Credentials for Windows devices (using the WMI protocol) are provided by the login configured for the MID Server service on the Windows server host. Credentials for UNIX , vCenter, and SNMP must be configured on the instance. Discovery automatically determines which credentials work for a particular computer or device.
- Define and run Discovery
 schedules . The Discovery Schedule is the control point for running discoveries. The schedule controls when Discovery runs, defines the MID Server to use, the type of Discovery that should run, and the IP addresses to query. Create as many schedules as necessary, using different types of discoveries, and configure them to run at any time. Let Discovery run on its configured schedule or manually execute Discovery at any time. You can set up a single schedule for the entire network or separate schedules for each location or VLAN. If you donât know the IP address to scan in your network, run a Network Discovery first to discover the IP networks. Once discovered, you can convert these networks into IP address range sets that you use in a Discovery Schedule. Note: For advanced discoveries, such as those requiring load balancing or
 scanning across multiple domains, use Discovery behaviors .
- Validate the Discovery results. Open the ECC queue and analyze the XML payload, then check the Discovery log .
 For more information, refer to the section for validating results in Schedule a horizontal discovery .
