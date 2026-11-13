# Discovery IP address configuration

- Source: https://www.servicenow.com/docs/r/zurich/it-operations-management/discovery/discovery-ip-address-configuration.html
- Release: Zurich
- Map: itom

---

# Discovery IP address configuration

Summarize Summarized using AI This content was generated using new OpenAI-powered functionality. Results are provided on an as is basis and are not guaranteed to be accurate or complete. Summary of Discovery IP address configuration This content explains how to configure IP address ranges for ServiceNow Discovery to query networks or network segments effectively. It highlights methods to include or exclude specific IP ranges and emphasizes best practices for accurate and efficient discovery scans. Show full answer Show less Key Methods for Defining IP Address Ranges IP Address List: Allows adding individual IP addresses or host names (which must resolve to IPs) outside any network or range. Useful for targeting specific devices directly. IP Address Range: Enables defining arbitrary IP ranges to scan, useful for selecting network segments or subnets. However, this method may scan network and broadcast addresses, potentially causing inaccurate results. Discovery performance can degrade if ranges exceed /16 size (~65,536 IPs), so splitting large ranges is recommended. IP Network: Uses CIDR notation to define entire IP networks, automatically excluding network and broadcast addresses from scans. This prevents common errors such as redundant or invalid device entries, making it the preferred method for IP address range configuration. Important Considerations IPv6 addresses are not supported for IP address ranges or networks in Discovery. If IP addresses in the network are unknown, run Network discovery first to identify IP networks, then convert those into IP address range sets for Discovery. Clear sysmetadata and sysupdatexml records if integrations populate these tables after importing discovery range items, to maintain data integrity. To avoid errors and improve accuracy, avoid including broadcast addresses in scans by using IP network definitions in CIDR notation. Practical Benefits for ServiceNow Customers By properly configuring IP address collections using these methods, customers can ensure Discovery accurately scans relevant devices without including invalid or redundant addresses. Using IP networks with CIDR notation is the best practice to improve data quality and scanning efficiency. This configuration flexibility supports tailoring Discovery schedules to the customerâs network structure and performance needs.
Use one or more of these methods in any combination to define the network or network
 segment for
Discovery
to query. You can
 include or exclude specific IP ranges from your query.

Note:
If you don't know the IP addresses in the network, run
Network discovery
first to determine the IP networks. Then, convert the IP networks into IP address range sets.
If you have integrations which populate sys_metadata and sys_update_xml tables, make sure to
 clear the update and metadata records after the discovery_range_item or discovery_range_item_ip import occurs.

Important:
IPv6 addresses aren't supported for IP address range or IP network.
There are three types of IP collections:
IP collection type Description
IP address list Use IP address lists to add individual addresses to query. These addresses aren't included in any existing IP range or IP network. You can enter the IP address of the device or a host name (DNS name). If you
 enter a host name, it must be mapped to an IP address . IP address range You can define arbitrary ranges of IP addresses to query. This process is a
 good way to include selected segments of a network or subnet. However, Discovery has no way of knowing if the IP range includes addresses
 for private networks or broadcast addresses, and scans all the addresses in the
 range. If the network and broadcast addresses are included, then the results are
 inaccurate. Discoveries configured to detect IP networks are more accurate than
 discoveries configured for IP address ranges. Only those IP addresses in your
 range that are reserved for manageable devices on the public network should be
 included. Note: To avoid performance issues, limit Discovery schedules to a maximum range of /16 (approximately 65,536 IPs). For better performance, consider splitting the range into smaller segments. IP network You can also scan an entire IP network. An IP
 network includes the range of available IP addresses in that network.
 The scan also includes the network address (the lowest address in the range) and
 the broadcast address (the highest address in the range). After you run network
 discovery , convert the IP networks that were found into range sets for use in
 discovering other devices. IP networks are represented in CIDR notation. Examples of CIDR notation
 include: 192.168.0.0/24 10.11.128.192/26 Discovery will not scan the network or broadcast addresses for a
 network. The equivalent ranges for the two networks are: 192.168.0.1 â 192.168.254 10.11.128.193 â 10.11.128.254 To avoid introducing errors from broadcast addresses, configure Discovery to exclude them by using IP network definitions in CIDR notation. Discovery automatically avoids scanning network and broadcast addresses when using IP networks. Including broadcast addresses in Discovery scans can lead to significant errors in the data, such as redundant or invalid device entries. By excluding broadcast addresses, Discovery helps prevent these errors. This built-in control makes IP networks the best method of defining which IP address ranges to query.
For more information about viewing and managing your IP collections, see
Discovery Admin Workspace IP inventory
.
