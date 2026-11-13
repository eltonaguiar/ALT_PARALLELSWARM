# CI deletion strategies for pattern discovery

- Source: https://www.servicenow.com/docs/r/zurich/it-operations-management/discovery/deletion-strategy.html
- Release: Zurich
- Map: itom

---

# CI deletion strategies for pattern discovery

Summarize Summarized using AI This content was generated using new OpenAI-powered functionality. Results are provided on an as is basis and are not guaranteed to be accurate or complete. Summary of CI deletion strategies for pattern discovery When performing Discovery with patterns in ServiceNow, you can manage what happens to configuration items (CIs) in the CMDB that Discovery no longer detects. This functionality is specific to pattern-based discovery and does not apply to probes or sensors. Patterns identify a main CI type, such as an IIS web server, and also detect related CIs like hosting machines, configuration files, and hosted websites. After initial discovery, you configure deletion strategies for related CIs, determining how Discovery handles those related CIs if they are not found on subsequent scans. Show full answer Show less Key Features Main CI and related CIs: Patterns identify a main CI and related CIs, establishing a dependency map that visually shows relationships. Related CI Types table: You configure deletion strategies for each related CI type in the Related CI Types [sacitopattern] table. This setup governs how missing related CIs are handled on future discoveries. Deletion strategy options for related CIs: Keep: Retains the CI record unchanged (default). Delete: Removes the CI record and its relationship to the main CI. Mark as absent: Sets the CIâs status to "Absent" without deleting it or its relationships. (Exception: Network adapters and IP addresses are deleted when marked absent.) Delete relations: Removes only the relationships between the related CI and the main CI, not the CI record. Mark as retired: Changes the CIâs status to "Retired" without deleting the CI or relationships. Limitations: Deletion strategies cannot be set on the main CI for Infrastructure pattern types. Deletion strategies do not apply to related entries, which are rules based on related CIs. Main CIs can only be deleted if they are discovered using Application or Cloud Resource pattern types. Practical Application ServiceNow customers can use CI deletion strategies to maintain CMDB accuracy by automatically managing CIs that are no longer detected during pattern-based discovery. This helps prevent stale data from accumulating and ensures the CMDB reflects the current state of the environment. By configuring deletion strategies for related CIs, customers control whether CIs are preserved, deleted, marked absent or retired, or if only relationships are removed, optimizing CMDB hygiene based on organizational policies and discovery results.
When you perform discovery with a pattern, you can choose what to do with configuration items (CIs) that are in the
Configuration Management Database (CMDB)
but
Discovery
can no longer find.

Note:
Deletion strategies are available only with patterns, not probes/sensors.
When you use a pattern to perform discovery, you identify a CI Type, which is the
main CI
you're trying to find, such as an IIS web server or
Tomcat
server.
Discovery
can also find
related CIs
and populate the
CMDB
accordingly. For example, after
Discovery
finds an IIS server with the IIS pattern, it can also find these related CIs:
- The Windows machine that hosts the web server
- The configuration files for the IIS server
- The website that the IIS server hosts
The dependency map on the main CI also shows the related CIs, as illustrated by the following
 graphic:
Figure 1. An example of an IIS server main CI and its related CIs
After you discover the main CI and its related CIs for the first time using a pattern, manually configure an entry in the Related CI Types [sa_ci_to_pattern] table for each relation between the main CI and a related CI type. Each record determines the deletion strategy for a related CI based on its type. You cannot set a deletion strategy for the main CI when using the Infrastructure pattern type.

You can view a list of the relations as the following image illustrates:
Figure 2. Example CIs related to an IIS server
The deletion strategy on a related CI takes effect when both of these conditions occur:
- After you run Discovery with the pattern again.
- Discovery successfully finds the main CI but cannot find the related CI.
These deletion strategy options are available:

Value Description
Keep Preserves the configuration file CI record and makes no other changes to the record. This option is the default setting. Delete Deletes the configuration file CI record from the CMDB, and the relationship to the main CI. Mark as absent Marks the Status [install_status] field of the configuration file CI record as Absent , meaning that Discovery cannot find the tracked configuration file. This status does not instruct the system to delete the actual CI or the relationship. Note: There are two tables that do have their CIs
 deleted if marked as absent: cmdb_ci_network_adapter and cmdb_ci_ip_address. Delete relations Deletes only the CI relationships between the related CI and the main CI. Mark as retired Marks the Status [install_status] field of the configuration file CI record as Retired , meaning that Discovery no longer uses this configuration file. This status does not instruct the system to delete the actual CI or the relationship.
Note:
Deletion strategies are not available for related entries, which are rules that are based on related CIs. For more information, see
Related entries
.
