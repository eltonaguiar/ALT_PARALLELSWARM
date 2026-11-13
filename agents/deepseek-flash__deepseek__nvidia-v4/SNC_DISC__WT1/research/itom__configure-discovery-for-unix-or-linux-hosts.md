# Configure Discovery for UNIX or Linux hosts

- Source: https://www.servicenow.com/docs/r/zurich/it-operations-management/itom-visibility/t_ConfigureDiscoveryUNIXLinuxHosts.html
- Release: Zurich

---

# Configure Discovery for UNIX or Linux hosts with attached storage

Discovery can find information about a UNIX or Linux host and attached
 storage.

## Before you begin

Role required: discovery_admin

## Procedure

- Optional: On the host, assign elevated privileges to the account that Discovery will use.
- On the ServiceNow instance, add
                        credentials to the Discovery Credentials
                    table.
- Create a Discovery Schedule for each host IP address.
- Optional: Create a behavior that uses a functionality definition with a wbem port probe to make the initial port-scanning phase (Shazzam) more efficient.
- Run network discovery. Note: If the host also connects to a NAS or SAN storage array, set up the SMI-S Provider and CIM
                            credentials .
