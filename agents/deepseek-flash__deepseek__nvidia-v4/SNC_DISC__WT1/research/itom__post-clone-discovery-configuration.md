# Post-clone Discovery configuration

- Source: https://www.servicenow.com/docs/r/zurich/it-operations-management/discovery/PostCloneDiscoveryConfig.html
- Release: Zurich
- Map: itom

---

# Post-clone Discovery configuration

Summarize Summarized using AI This content was generated using new OpenAI-powered functionality. Results are provided on an as is basis and are not guaranteed to be accurate or complete. Summary of Post-clone Discovery configuration When you clone a ServiceNow instance, Discovery schedules are copied from the source to the target instance. However, additional post-clone configuration is required to ensure these schedules operate correctly on the target instance. This configuration is crucial for both Cloud-based and IP-based Discovery schedules to maintain optimal Discovery performance. Show full answer Show less Post-clone Configuration for IP-based Discovery Schedules After requesting a clone, the required steps depend on the MID Server selection method used in the original Discovery schedule: Specific MID: Update the MID Server record for each Discovery schedule on the target instance. Cluster: Create the MID Server cluster on the target, attach MID Servers, then update the cluster name in Discovery schedules. Alternatively, remove the MID cluster record from the Clone Exclude Tables to prevent cloning issues. Use Behavior: Create or attach the necessary behaviors and functionalities on the target instance, then link the behavior to the Discovery schedule. Note that Discovery functionalities are not cloned automatically. Auto-select: Verify all MID Servers on the target instance are properly configured with relevant IP ranges, supported applications, and capabilities. Post-clone Configuration for Cloud Discovery Schedules For Cloud Discovery schedules, after cloning: Update the Cloud Service Account records to reference the correct Discovery credentials on the target instance. Update MID Server configurations similarly to IP-based Discovery schedules, following the same MID Server selection method steps outlined above. Credential and MID Server Considerations Credential Aliases: While aliases are cloned, the associated credentials are not. You must verify and update credential aliases in the Connection & Credential Aliases table to point to valid credentials on the target instance. MID Server Tables: MID Server related tables are not cloned. You need to set up MID Servers anew on the target instance to ensure Discovery schedules function properly. Why This Matters Proper post-clone configuration prevents Discovery schedule failures and ensures Discovery processes continue to run smoothly without manual errors. Following these steps saves time and helps maintain accurate and reliable Discovery data after an instance clone.
When a clone occurs,
Discovery
schedules are copied from the source instance to the target instance. Additional configuration is necessary for these schedules to function correctly on the target instance, helping you properly
 configure Cloud-based and IP-based
Discovery
schedules and maintain optimal
 performance.

Note:
For general information about instance cloning, see the
Clone FAQS-Frequently Asked Questions [KB0715621]
article in the
Now Support
Knowledge Base
.

For instructions on how to deactivate or cancel a
Discovery
schedule after creating a clone, see the
A Post-Clone script to Deactivate and Cancel Discovery Schedules [KB0789119]
article in the
Now Support
Knowledge Base
.

## Post-clone target configuration for IP-based Discovery schedules

After completing the
Request a clone
process, post-clone configuration is determined by the
MID Server
selection method you chose in the
Discovery
schedule on the source instance.

Table 1. Target instance configuration for IP-based Discovery schedules
MID Server selection method Next steps
Specific MID Update the MID Server record for each Discovery schedule. Cluster Create the cluster, attach the MID Server to the cluster, and then update the cluster name in the Discovery schedule. Alternatively, remove the MID cluster [ecc_agent_cluster] record from the Clone Exclude Tables [clone_data_exclude]. For more information, see Exclude a table from cloning (legacy) . Use Behavior Create the behaviors, create a functionality or attach an existing functionality, then go back to the Discovery schedule and attach the behavior to the Discovery schedule. Note: Discovery functionalities arenât cloned with an instance. Auto-select Verify all MID Servers on the target instance are set up with target IP ranges, supported applications, and capabilities.

## Post-clone target configuration for Cloud Discovery schedules

After completing the
Request a clone
process, you must access the Cloud Service Account [cmdb_ci_cloud_service_account] table and update the service accounts with the proper reference to the
Discovery
credentials. You must also update the MID Servers for the
Discovery
schedule. Additional post-clone configuration is determined by the
MID Server
selection method that you chose in the original
Discovery
schedule.

Table 2. Target instance configuration for Cloud Discovery schedules
MID Server selection method Next steps
Specific MID Update the MID Server record for each Discovery schedule. Cluster Create the cluster, attach the MID Server to the cluster, and then update the cluster name in the Discovery schedule. Alternatively, remove the MID cluster [ecc_agent_cluster] record from the Clone Exclude Tables [clone_data_exclude]. For more information, see Exclude a table from cloning (legacy) . Use Behavior Create the behaviors, create a functionality or attach an existing functionality, then go back to the Discovery schedule and attach the behavior on the target instance. Note: Discovery functionalities arenât cloned with an instance. Auto-select Verify that all MID Servers are set up with target IP ranges, supported applications, and capabilities.
For more information, see the
Cloud discovery schedules fail after the instance clone [KB1759363]
article in the
Now Support
Knowledge Base
.

## Clone Exclusions

Credential aliases are cloned but their credentials arenât cloned. If
Discovery
schedules have credential aliases, you must go to the Connection & Credential Aliases [sys_alias] table and confirm the alias points to the correct credentials. After cloning, update the
Discovery
schedules and add credentials within the target instance.

Additionally, no
MID Server
related tables are cloned. For more details, see the
MID Servers and Clones [KBKB0786475]
article in the
Now Support
Knowledge Base
.
