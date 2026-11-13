# Discovery and SCCM together

- Source: https://www.servicenow.com/docs/r/zurich/it-operations-management/discovery/c_DiscoveryAndSCCMTogether.html
- Release: Zurich
- Map: itom

---

# Discovery and SCCM together

Use these guidelines to avoid common issues when you use
Discovery
and
 System Center Configuration Manager (SCCM) together.

You must decide if you will use Asset Intelligence (AI) or non-AI software data sources.
 Because the software correlation data is tracked differently for each of these data sources,
 you should avoid switching back and forth between the two. If you must switch between data
 sources, remove all the software installation records imported by SCCM before the switch
 occurs.

When
Software Asset Management
is not enabled, software installation records are stored in
 the Software Instance [cmdb_software_instance] table. When
Software Asset Management
is
 enabled, software installation records are stored in the Software Installation
 [cmdb_sam_sw_install] table.

Note:
If records aren't removed before the switch, duplicate records may exist. In the event that AI and non-AI data becomes mixed, clear the Software Installation table.

## Overview of Service Graph connector for Microsoft SCCM

Use the Service Graph connector for
Microsoft
SCCM to pull data from SCCM
 into your
ServiceNow
instance. See
Service Graph connector for Microsoft
 SCCM
for more
 details.
Note:
If you upgrade your instance to a version of the
ServiceNow AI Platform
that does not provide support for your version of SCCM, you can continue to
 use that version. However, all new instances require the use of a supported SCCM
 version.

## Upgrading to a later version

The
ServiceNow
SCCM integrations are self-contained and can exist
 independently. They each use their own import set tables, data sources and transform maps.
 However, all SCCM integrations will transform data into the same tables within the
ServiceNow
CMDB. To avoid the data being overwritten by another source:
- Use one SCCM integration and disable all other SCCM scheduled imports.
- Perform a full import to clear the cmdb_software_instance table, the
 cmdb_sam_sw_install table, and other tables of old SCCM data.

## Collect software data with either SCCM or Discovery

When Discovery and SCCM are both enabled on a system, the software records found
 through both tools could overwrite each other.

### Before you begin

Role required: admin

### About this task

To determine how software data is collected, configure the
glide.discovery.software_sccm_managed
property.

### Procedure

- Navigate to All > Discovery Definition > Properties .
- Set the Windows software is SCCM managed property
 ( glide.discovery.software_sccm_managed )
 appropriately. If this property is set to Yes , software for computer
 CIs is populated in the CMDB by SCCM. An internal process determines that the
 computer is managed by SCCM, and Discovery does not
 populate the software records for Windows software data. The following
 information level message is written to the Discovery log
 file. Skipping software population because the CI is managed
 by SCCM If the check box is cleared, the property is set
 to No , and the system manages software data with
 Windows.
- Click Save . Important: If SCCM Integration is active before Discovery is enabled
 and the property is enabled, Discovery ignores the
 population of software for any CIs that are also imported through SCCM. If Discovery is
 enabled before the SCCM Integration, it is possible for software
 installation data from both sources to be mixed.

### What to do next

Use these Discovery properties to avoid software data discrepancy between Discovery
 and SCCM:
glide.discovery.enable.software_simplify
and
glide.discovery.enable.software_simplify_sccm
. See
Discovery properties
for more information.
