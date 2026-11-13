# Configure Discovery identity sensors

- Source: https://www.servicenow.com/docs/r/zurich/it-operations-management/discovery/t_ConfigDiscoIdentSens.html
- Release: Zurich
- Map: itom

---

# Configure Discovery identity sensors

If you customize an identify multi-probe, you can also configure a multi-sensor for
 it.

## Before you begin

Role required: discovery_admin or admin

## About this task

These multi-sensors pass the data returned by the identity probes to the
Discovery
identifiers. The
 identifiers then search the CMDB for matching CIs. When the identity of a device is
 resolved, the identifiers pass the result state for the device to the multi-sensors. The multi-sensors react accordingly, either by launching exploration probes or stopping
Discovery
for that device.

## Procedure

- Navigate to All > Discovery Definition > Sensors .
- Select an existing identity multi-sensors from the list. Note: To avoid confusion, the multi-sensors provided in the instance must
 have the same names as their matching multi-probes. The Responds to Probes related list shows the simple
 probes which pass their data to this multi-sensors. These are the same
 simple probes that appear in the Includes Probes list in the matching
 multi-probes record.
- Click the Script link for each probe in the list to see
 the script that the multi-sensors runs to process the data from the probe.

## Example

Figure 1. Discovery identity sensors

## What to do next

Run a discovery through the
Discovery
 Schedule
to search for CIs and verify that they are identified correctly in
 the CMDB.
