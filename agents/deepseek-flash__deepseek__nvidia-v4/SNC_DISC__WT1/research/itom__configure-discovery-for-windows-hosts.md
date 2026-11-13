# Configure Discovery for Windows hosts

- Source: https://www.servicenow.com/docs/r/zurich/it-operations-management/itom-visibility/t_ConfigureDiscoveryWindowsHosts.html
- Release: Zurich

---

# Configure Discovery for Windows hosts with attached storage

Discovery
can find information about a
Windows
host and attached storage.

## Before you begin

Role required: discovery_admin

## Procedure

- Follow the steps if you're using the Windows 2008 servers that is attached to storage: Download and install the Microsoft Fibre Channel Information Tool from http://www.microsoft.com and search the website for Microsoft Fibre Channel Information Tool. Set the environment path for the fcinfo executable and run the fcinfo.exe file. Note: For servers that are using newer operating systems, similar functionality is present with the operating system; this step is not required.
- For all Windows hosts including Windows 2008, add Windows credentials to the Discovery Credentials table.
- On the ServiceNow instance, create a Discovery Schedule for each host IP address.
- Optional: Create a behavior that uses a functionality definition with a wbem port probe to make the initial port-scanning phase (Shazzam) more efficient.
- Run network discovery. Note: If the host also connects to a NAS or SAN storage array, set up the SMI-S Provider and CIM
                            credentials .
