# Configure Discovery identity probes

- Source: https://www.servicenow.com/docs/r/zurich/it-operations-management/discovery/t_ConfigureDiscoveryIdentityProbes.html
- Release: Zurich
- Map: itom

---

# Configure Discovery identity probes

Identity probes are multi-probes, which contain one or more simple probes configured
 to extract specific information from manageable devices. You can create your own identity
 multi-probe to identify CIs that Discovery does not already identify.

## Before you begin

Role required: discovery_admin or admin

## About this task

Identity probes return such information as device serial numbers (there can be
 several per device), the computer name, and network identification (MAC address).
 For example, the
Linux - Identity
multiprobe provided in the
 system, contains two simple SSH probes configured to return hardware and network
 information about the device. After the probe has discovered this information, it
 passes the data to a multisensor configured to process identity information.

Note:
A multiprobe cannot contain another multiprobe.

## Procedure

- Navigate to All > Discovery Definition > Probes .
- Select a probe from the list whose Class is Multiprobe .
- Make sure the scope is set to Global .
- In the Includes Probes Related List, click Edit to select simple probes to include in this
 multiprobe.
- Click New to create a new simple probe.

## Example

Figure 1. Discovery identity probes

## What to do next

Configure Discovery identity sensors
that are part
 of the identify probes.
