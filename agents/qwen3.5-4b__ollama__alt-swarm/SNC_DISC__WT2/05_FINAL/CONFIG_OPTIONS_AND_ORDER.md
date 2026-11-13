# Worker report — qwen3.5-4b__ollama__alt-swarm

**Task:** SNC_DISC_RESEARCH
**Model (primary):** `qwen3.5:4b`
**Model (used):** `qwen3.5:4b`
**Provider:** `ollama`
**Harness:** ALT_PARALLELSWARM `swarm/agent_runner.py`
**Generated:** 2026-11-13T09:05:31+00:00
**Evidence:** `options.md` (pre-fetched; worker has no browser)
**Assigned section:** Produce the configuration-option inventory and the canonical order of operations for ServiceNow Discovery. Group options by: identity/IP/hostname, network scanning, scheduling/throughput, and deletion strategy. For the order of operations, start at subscription/roles and end at CMDB governance. Use tables and preserve exact property names and defaults.

> This is an independent worker draft. It is evidence-constrained, not independently
> web-verified. The orchestrator's primary reference is the authoritative synthesis.

---

# ServiceNow Discovery Configuration Reference (Brazil Release)

## Identity, IP, and Hostname Management

The following table details the properties governing identity resolution and IP address handling during the horizontal discovery process. These settings control how discovered IPs are mapped to CI records and whether duplicate addresses are tolerated.

| Field | Description | Type | Default Value |
| :--- | :--- | :--- | :--- |
| `glide.discovery.exclude_ip_sync_classes` | Defines CI classes whose IP addresses shouldn't be substituted if the address returned by Discovery doesn't match one of the devices' NICs. Use a comma-separated list to define multiple classes. By default, the system uses the management IP of a load balancer returned by Discovery in the CI record, rather than substituting it for the IP address of one of the load balancer's NICs. | string | `cmdb_ci_lb` [S1] |
| `glide.discovery.enforce_unique_ips` | Enforce unique IP addresses: Ignores the IP address after Discovery encounters subsequent devices that use the same IP address. Each time a computer, printer, or network device with a valid IP address is discovered, the IP address field is cleared on any other device sharing that address. If inactive, stores the IP address for each device. | true \| false | `false` [S1] |

These properties are configured via **Discovery Definition > Properties** to manage the horizontal discovery process [S1]. The default behavior for load balancers is to retain the management IP rather than substituting a NIC IP unless explicitly excluded via `glide.discovery.exclude_ip_sync_classes`.

## Network Scanning Configuration

Network scanning parameters dictate how routers, switches, and networks are identified and associated. These settings influence performance, logging, and the logic used to select representative routers for IP networks.

| Field | Description | Type | Default Value |
| :--- | :--- | :--- | :--- |
| `glide.discovery.bgp_router_disable` | BGP router exploration disable: Disables running the SNMP – Routing probe or pattern when discovering a router running the BGP protocol. This exploration is inactive by default because BGP routing tables are large. These routers typically operate at the edge of large networks, where further network discovery is not relevant. Set this value to `false` if your organization uses BGP routers as edge routers between relatively small networks. Enabling this property can cause performance issues including out-of-memory issues on the MID Server. | true \| false | `true` [S1] |
| `glide.discovery.debug.network_discovery` | Network discovery debugging: Enables extensive logging of all Network Discovery activities on the instance. | true \| false | `true` [S1] |
| `glide.discovery.discoverable.network.max.netmask.bits` | Maximum netmask size for discoverable networks (bits): The maximum number of bits in a regular netmask for networks that are discovered by Network Discovery. A regular netmask is a netmask that can be expressed in binary as a string of ones followed by a string of zeroes. Setting this property to a value of 1 through 32 limits the sizes of regular networks that are discovered; setting it to any other value causes all networks to be discovered. Irregular networks are always discovered. The default value is 28, which means that regular networks with 8 or fewer addresses cannot be discovered. | integer | `28` [S1] |
| `glide.discovery.network_owner_method` | Network router selection method: This property controls the method used to decide (during Network Discovery) which router should be selected as the router to be associated with a given IP Network. Possible values are: First Router, Last Router, Most Networks, Least Networks. | choice list | `Most Networks` [S1] |
| `glide.discovery.physical_interface_types` | Physical interface types: A comma-separated list of interface types that are considered physical for the purposes of network discovery. If a router (or device capable of routing) has an interface of this type, the networks connected to that interface are considered locally connected to that device. The default interface types include Ethernet, 802.11, and Token Ring types. | string | `6,117,9,71,209` [S1] |
| `glide.discovery.switch_interface_types` | Switch interface types: A comma-separated list of interface types that are considered. Devices with any interface types that do NOT appear in this list are classified as routers, when they have routing. | string | `7,8,9,26,53,62,69,71,78,115,117,209` [S1] |

The `glide.discovery.network_owner_method` determines which router is associated with an IP network, defaulting to the router with the most attached networks [S1]. Interface type definitions are based on SNMP MIB-2 OID 1.3.6.1.2.1.2.2.1.3 [S1].

## Scheduling and Throughput Management

Scheduling properties control the execution of discovery jobs, including MID Server selection, job priorities within the Event Framework, and credential handling.

| Field | Description | Type | Default Value |
| :--- | :--- | :--- | :--- |
| `com.snc.use_external_credentials` | Allows the use of external storage of credentials. | true \| false | `true` [S1] |
| `com.glide.codesigning.tracking.unsupported_script_tracking.enabled` | Controls script tracking for code signing on Cloud Discovery. When set to `true` and code signing is enabled, ECC queue records inserted through unsupported scripts are not notarized, which can cause Cloud Discovery operations to fail. Set this property to `false` to enable Cloud Discovery on code-signed instances. | true \| false | `true` [S1] |
| `com.glide.queue.discovery.cloud.sensors.processing_jobs.priority` | Manages the background job's worker priority for Cloud-based Discovery jobs when using Event Framework. Increasing the value decreases the priority. This behavior only applies when `discovery.use.event.processing` is set to `true`. | integer | `100` [S1] |
| `com.glide.queue.discovery.sensors.processing_jobs.priority` | Manages the background job's worker priority for IP-based Discovery jobs when using Event Framework. Increasing the value decreases the priority. | integer | *not stated in the supplied evidence* [S1] |

MID Server selection within schedules can be configured via **Auto-Select**, **Specific MID Cluster**, **Specific MID Server**, or **Use Behavior** [S3]. Auto-select requires MID Servers to be assigned the Discovery or ALL applications and must be configured with the appropriate IP ranges; it is not supported with IPv6 [S3].

## Deletion Strategy and Governance

The evidence provided does not contain explicit configuration properties for deletion strategies (e.g., `glide.discovery.delete.*` properties). The canonical order of operations for Discovery governance, starting from subscription/roles and ending at CMDB updates, is described below.

1.  **Role Assignment**: Users must have the `discovery_admin` role to configure and execute Discovery [S2]. This role grants access to tables in the Discovery application.
2.  **MID Server Provisioning**: At least two MID Servers should be installed on physical or virtual servers meeting system requirements, assigned to different schedules and IP ranges to accelerate discovery [S2]. Starting with the Istanbul release, MID Servers must be assigned the Discovery or ALL applications [S2].
3.  **Credential Configuration**: Credentials for Windows (WMI), UNIX, vCenter, and SNMP devices must be configured on the instance [S2]. The MID Server service on Windows hosts provides credentials for WMI protocols [S2].
4.  **Schedule Definition**: Discovery Schedules define the CI types targeted, associated MID Servers, and run settings. Scan types include Configuration Items, IP addresses, Networks, Service, Serverless, Cloud application, Cloud resources, and Certificates [S3].
5.  **Configuration Console Application**: The Discovery Configuration Console allows management of specific CI types, details (e.g., OS info), ARP data, software packages, and file-based discovery [S4].
6.  **CMDB Update**: Discovery returns all data from the target to the instance before applying console settings; the instance ignores excluded data when updating the CMDB [S4].

## Assumptions / Gaps

*   The default value for `com.glide.queue.discovery.sensors.processing_jobs.priority` is not stated in the supplied evidence [S1].
*   Specific deletion strategy properties (e.g., rules for removing discovered CIs) are not detailed in the provided text; only the flow of data to the CMDB is described [S4].
*   The exact behavior of "Use Behavior" regarding MID Server selection when a single schedule requires multiple servers is not fully elaborated in the evidence [S3].
*   No specific properties for handling IPv6 discovery failures or recovery strategies are mentioned beyond the auto-select limitation [S3].
