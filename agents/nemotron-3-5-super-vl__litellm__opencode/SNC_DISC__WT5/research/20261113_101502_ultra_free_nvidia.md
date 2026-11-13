# v3 run

model: ULTRA_FREE_NVIDIA
elapsed: 21.0s
research_calls: 3
error: None

## Question
What are the ServiceNow Discovery configuration options and properties, and in what order does Discovery processing happen when a device is discovered?

## Answer
ServiceNow Discovery configuration options and properties can be managed through various interfaces, including the **Discovery Configuration Console** (accessible via Discovery Definition > Configuration Console) to control what types of Configuration Items (CIs) and CI information are discovered, and by navigating to **Discovery Definition > Properties** to edit specific Discovery properties.

Key configuration aspects include:
*   **Anomaly Detection:** The **Discovery Admin Workspace** allows setting a threshold percentage for detecting anomalies in the number of CIs discovered during a schedule execution.
*   **Pattern-based Horizontal Discovery:** Configuration file tracking can be enabled here to specify paths for configuration files of discovered applications.
*   **IP Range Management:** IP address ranges can be defined, but limits (e.g., maximum range of /16 to avoid performance issues) should be observed. Network discovery can be run first to determine IP networks, which can then be converted into IP address range sets.
*   **ARP Data:** Enabling or disabling discover ARP data can be controlled in the Discovery Configuration Console for Network, UNIX, and Windows device classes (it is off by default).
*   **IP Synchronization:** The `glide.discovery.enforce_ip_sync` property controls whether the discovered IP address must match a NIC on the device before being used in the CI record.
*   **Unique IPs:** The `glide.discovery.enforce_unique_ips` property ensures that if a device with a valid IP is discovered, other devices with the same IP have their IP address field cleared.
*   **Service Affinity:** The system property `glide.discovery.ip_service_affinity = true` can be set to allow Discovery to remember which service successfully discovered an IP address.

The **Discovery processing order** when a device is discovered generally follows these steps:
1.  **Shazzam Probe:** Discovery sends a Shazzam probe to check if commonly used ports are open and responsive.
2.  **Classification Probe:** The Discovery application determines the appropriate classification probe based on the successful port probe response. The MID Server runs this probe to gather additional information (e.g., OS version), which determines the CI class.
3.  **Identification Trigger Probe:** Discovery places the identification trigger probe for the CI classifier into the ECC queue. This probe uses **identification rules** to decide whether to insert or update a CI in the CMDB. Alternatively, a **Pattern probe** might be used, which covers both identification and exploration phases.
4.  **Post-Discovery Events:** Once discovery completes for a CI, a `discovery.device.complete` event is created, which triggers the **IPAddressFixup** script include.

For more detailed information on specific properties or configurations, refer to the ServiceNow documentation.

*   [Discovery properties](https://www.servicenow.com/docs/api/khub/maps/bsp_DjPRMilbWYHwwVa4zQ/topics/NNWTC6v7iVGw9emOILPtPA/content?target=DESIGNED_READER)
*   [Discovery IP configuration](https://www.servicenow.com/docs/api/khub/maps/bsp_DjPRMilbWYHwwVa4zQ/topics/91BEzK6jlBrt1pwkcnS3dA/content?target=DESIGNED_READER)
*   [Discovery Configuration Console](https://www.servicenow.com/docs/api/khub/maps/bsp_DjPRMilbWYHwwVa4zQ/topics/jxm03gKvyhebiCVQEIFgRA/content?target=DESIGNED_READER)
*   [Discovery overview](https://www.servicenow.com/docs/api/khub/maps/bsp_DjPRMilbWYHwwVa4zQ/topics/7qT0WEcnXOPjGppEioi2pw/content?target=DESIGNED_READER)
*   [Horizontal flow (probes/sensors)](https://www.servicenow.com/docs/api/khub/maps/bsp_DjPRMilbWYHwwVa4zQ/topics/jxL49V2EHei6N8w5BSt0CQ/content?target=DESIGNED_READER)
*   [Discovery Device IP Address](https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB0687602)
*   [Discovery Phase Shazzam](https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB0965884)

## Transcript
```
[0] research(Discovery configuration options properties ServiceNow Discovery) -> 3535c
[0] research(ServiceNow Discovery configuration properties discovery processing order when device is di) -> 2957c
[0] research(Discovery processing order discovery flow device discovered classification identification) -> 3325c
[1] answer()
```
