# Create a Quick IP range for a Discovery schedule

- Source: https://www.servicenow.com/docs/r/zurich/it-operations-management/discovery/t_CreateAQuickRange.html
- Release: Zurich
- Map: itom

---

# Create a Quick IP range for a Discovery schedule

Quick ranges enable administrators to define IP addresses to scan in a single comma-delimited string without creating separate records.

## Before you begin

Only MID Servers that are up and validated are used with quick ranges. The MID Servers must specify the
Discovery
application (or ALL applications) and have IP ranges configured if you use the auto-select feature on the
Discovery schedule
.

Role required: discovery_admin

## About this task

You can enter IP addresses in one of the following formats:
- An IP range defined by a slash and the number of bits in the subnetwork. For example, the string 10.10.10.0/24 scans 24 bits of IP addresses from 10.10.10.0 to 10.10.10.254.
- An IP range defined by a dash. For example, the string 10.10.11.0-10.10.11.165 scans the IP addresses from 10.10.11.0 to 10.10.11.165.
- A comma-separated list of specific IP addresses. For example, the string 10.0.2.1,10.0.2.15 scans the IP addresses 10.0.2.1 and 110.0.2.15.
Note:
IPv6 address ranges and networks aren't supported and will be ignored. Any other entries that can't be interpreted will also be ignored.

## Procedure

- Select the Quick Ranges related link on the Discovery Schedule form.
- Enter the IP ranges and specific IP addresses to scan.
- Select Make Ranges . Note: The Quick Range interface is for entering IP addresses only and can't be used to edit IP addresses that have already been submitted. Figure 1. Entering a quick range from a Discovery schedule The instance automatically displays the entries in the proper format.
- For changes to IP address ranges, select the IP address
 records in the Discovery Range Sets related list. Note: Overriding behavior is not applicable on Discovery range sets.
