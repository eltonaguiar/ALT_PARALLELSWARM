# Worker report — qwen3.5-4b__ollama__alt-swarm

**Task:** SNC_DISC_RESEARCH
**Model:** `qwen3.5:4b`
**Provider:** `ollama`
**Harness:** ALT_PARALLELSWARM `swarm/agent_runner.py`
**Generated:** 2026-11-13T08:58:07+00:00
**Evidence:** `options.md` (pre-fetched; worker has no browser)
**Assigned section:** Produce the configuration-option inventory and the canonical order of operations for ServiceNow Discovery. Group options by: identity/IP/hostname, network scanning, scheduling/throughput, and deletion strategy. For the order of operations, start at subscription/roles and end at CMDB governance. Use tables and preserve exact property names and defaults.

> This is an independent worker draft. It is evidence-constrained, not independently
> web-verified. The orchestrator's primary reference is the authoritative synthesis.

---

# ServiceNow Discovery Configuration Reference (Brazil Release)

## Overview
This section details the configuration options for ServiceNow Discovery in the Brazil release, organized by functional category. It outlines the canonical order of operations from subscription management to CMDB governance, ensuring alignment with instance-specific requirements.

## 1. Identity and IP Management Properties
These properties govern how IP addresses are handled during discovery, specifically regarding substitution and uniqueness enforcement.

| Property Name | Description | Type | Default Value |
| :--- | :--- | :--- | :--- |
| `glide.discovery.exclude_ip_sync_classes` | Defines CI classes whose IP addresses shouldn't be substituted if the address returned by Discovery doesn't match one of the devices' NICs. Use a comma-separated list to define multiple classes. By default, the system uses the management IP of a load balancer returned by Discovery in the CI record, rather than substituting it for the IP address of one of the load balancer's NICs. | string | `cmdb_ci_lb` |
| `glide.discovery.enforce_unique_ips` | Enforce unique IP addresses: Ignores the IP address after Discovery encounters subsequent devices that use the same IP address. Each time a computer, printer, or network device with a valid IP address is discovered, the IP address field is cleared on any other device sharing that address. If inactive, stores the IP address for each device. | true / false | `false` |

## 2. Network Scanning Properties
These properties control the depth and logic of network discovery, including BGP handling, netmask filtering, and router selection.

| Property Name | Description | Type | Default Value |
| :--- | :--- | :--- | :--- |
| `glide.discovery.bgp_router_disable` | BGP router exploration disable: Disables running the SNMP – Routing probe or pattern when discovering a router running the BGP protocol. This exploration is inactive by default because BGP routing tables are large. These routers typically operate at the edge of large networks, where further network discovery is not relevant. Set this value to `false` if your organization uses BGP routers as edge routers between relatively small networks. Enabling this property can cause performance issues including out-of-memory issues on the MID Server. | true / false | `true` |
| `glide.discovery.debug.network_discovery` | Network discovery debugging: Enables extensive logging of all Network Discovery activities on the instance. | true / false | `true` |
| `glide.discovery.discoverable.network.max.netmask.bits` | Maximum netmask size for discoverable networks (bits): The maximum number of bits in a regular netmask for networks that are discovered by Network Discovery. A regular netmask is a netmask that can be expressed in binary as a string of ones followed by a string of zeroes. Setting it to any other value causes all networks to be discovered. Irregular networks are always discovered. The default value is 28, which means that regular networks with 8 or fewer addresses cannot be discovered. | integer | `28` |
| `glide.discovery.network_owner_method` | Network router selection method: This property controls the method used to decide (during Network Discovery) which router should be selected as the router to be associated with a given IP Network. Possible values include First Router, Last Router, Most Networks, and Least Networks. | choice list | `Most Networks` |
| `glide.discovery.physical_interface_types` | Physical interface types: A comma-separated list of interface types that are considered physical for the purposes of network discovery. If a router (or device capable of routing) has an interface of this type, the networks connected to that interface are considered locally connected to that device. The default interface types include Ethernet, 802.11, and Token Ring types. | string | `6,117,9,71,209` |
| `glide.discovery.switch_interface_types` | Switch interface types: A comma-separated list of interface types that are considered. Devices with any interface types that do NOT appear in this list are classified as routers, when they have routing. | string | `7,8,9,26,53,62,69,71,78,115,117,209` |

## 3. Scheduling and Throughput Properties
These properties manage the execution environment, including credential storage, script tracking, and job priority within the Event Framework.

| Property Name | Description | Type | Default Value |
| :--- | :--- | :--- | :--- |
| `com.snc.use_external_credentials` | Allows the use of external storage of credentials. | true / false | `true` |
| `com.glide.codesigning.tracking.unsupported_script_tracking.enabled` | Controls script tracking for code signing on Cloud Discovery. When set to `true` and code signing is enabled, ECC queue records inserted through unsupported scripts are not notarized, which can cause Cloud Discovery operations to fail. Set this property to `false` to enable Cloud Discovery on code-signed instances. | true / false | `true` |
| `com.glide.queue.discovery.cloud.sensors.processing_jobs.priority` | Manages the background job's worker priority for Cloud-based Discovery jobs when using Event Framework. Increasing the value decreases the priority. This behavior only applies when `discovery.use.event.processing` is set to `true`. | integer | `100` |
| `com.glide.queue.discovery.sensors.processing_jobs.priority` | Manages the background job's worker priority for IP-based Discovery jobs when using Event Framework. Increasing the value decreases the priority. | integer | *not stated in the supplied evidence* |

## 4. Canonical Order of Operations
The following sequence represents the standard operational flow for configuring and executing Discovery, starting from role assignment and ending with CMDB governance updates.

1.  **Subscription and Role Management**: Ensure users have the `discovery_admin` role to access Discovery tables [S2].
2.  **MID Server Provisioning**: Install MID Servers on physical or virtual servers meeting system requirements. Assign at least two MID Servers to different schedules and IP ranges to accelerate discovery [S2]. Verify that MID Servers are assigned the Discovery application or ALL application [S2].
3.  **Connectivity Verification**: Confirm MID Server connectivity via `Discovery > MID Servers`. Check logs on both the instance (`Discovery > MID Servers > [MID Server] > Logs`) and the host (`agent\logs\agent0.log0`) for errors, ensuring port 443 (SSL) or proxy access is not blocked [S2].
4.  **Credential Configuration**: Set credentials on the instance for computers, printers, and network gear. Windows devices use WMI login configured on the MID Server host; UNIX, vCenter, and SNMP require explicit configuration [S2].
5.  **Schedule Definition**: Navigate to `Discovery > Schedules`. Define the schedule name and select a scan type (Configuration Items, IP addresses, Networks, Service, etc.) [S3]. Select the
