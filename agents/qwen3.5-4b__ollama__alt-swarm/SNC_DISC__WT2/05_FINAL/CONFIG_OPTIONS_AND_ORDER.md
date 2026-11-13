# Worker report — qwen3.5-4b__ollama__alt-swarm

**Task:** SNC_DISC_RESEARCH
**Model (primary):** `qwen3.5:4b`
**Model (used):** `qwen3.5:4b`
**Provider:** `ollama`
**Harness:** ALT_PARALLELSWARM `swarm/agent_runner.py`
**Generated:** 2026-11-13T09:03:35+00:00
**Evidence:** `options.md` (pre-fetched; worker has no browser)
**Assigned section:** Produce the configuration-option inventory and the canonical order of operations for ServiceNow Discovery. Group options by: identity/IP/hostname, network scanning, scheduling/throughput, and deletion strategy. For the order of operations, start at subscription/roles and end at CMDB governance. Use tables and preserve exact property names and defaults.

> This is an independent worker draft. It is evidence-constrained, not independently
> web-verified. The orchestrator's primary reference is the authoritative synthesis.

---

# ServiceNow Discovery Configuration Reference (Brazil Release)

## Identity and IP Management Properties

The following properties control how Discovery handles IP address substitution and uniqueness enforcement. These settings are critical for maintaining accurate CMDB records, particularly for load balancers and devices sharing network segments. The property `glide.discovery.exclude_ip_sync_classes` defines CI classes whose IP addresses should not be substituted if the returned address does not match a device's NIC. By default, this list includes `cmdb_ci_lb`, ensuring that load balancer management IPs are retained rather than replaced by individual NIC addresses [S1].

The property `glide.discovery.enforce_unique_ips` determines whether Discovery ignores subsequent devices sharing an IP address. When set to `true`, the system clears the IP field on any device sharing a valid address with a previously discovered computer, printer, or network device; if inactive, it stores the IP for each device [S1]. The default value is `false`.

## Network Scanning and Discovery Logic

Network discovery behavior is heavily influenced by properties governing netmask filtering, router selection, and interface classification. The property `glide.discovery.discoverable.network.max.netmask.bits` limits the maximum number of bits in a regular netmask for discoverable networks. A regular netmask consists of binary ones followed by zeroes (e.g., 255.255.255.0). Setting this value between 1 and 32 filters out small networks, such as those with 8 or fewer addresses, which are often used for loopback or point-to-point connections. The default value is `28`, meaning networks with 8 or fewer addresses are not discovered unless they are irregular [S1].

Router selection during network discovery is controlled by `glide.discovery.network_owner_method`. This property dictates which router is associated with a given IP Network. Options include `First Router` (the first router discovering the network), `Last Router`, `Most Networks` (router with the most attached networks), and `Least Networks`. The default value is `Most Networks` [S1].

Interface classification relies on two comma-separated string properties: `glide.discovery.physical_interface_types` and `glide.discovery.switch_interface_types`. These define interface types considered physical for network discovery based on SNMP MIB-2 OID 1.3.6.1.2.1.2.2.1.3. The default values are `6,117,9,71,209` for physical interfaces and `7,8,9,26,53,62,69,71,78,115,117,209` for switch interfaces [S1]. Devices with interface types not in the switch list but possessing routing capabilities are classified as routers.

BGP router exploration is managed by `glide.discovery.bgp_router_disable`. This property disables the SNMP Routing probe or pattern for BGP-enabled routers by default to prevent performance issues, such as out-of-memory errors on the MID Server, caused by large routing tables [S1]. Setting this to `false` enables exploration if the organization uses BGP routers between relatively small networks, such as buildings on a single campus.

## Scheduling, Throughput, and Deletion Strategy

Discovery operations are orchestrated through schedules defined in the `glb_discovery_schedule` table, accessible via Discovery Definition > Schedules [S3]. The schedule form allows users to specify scan types including Configuration Items, IP addresses, Networks, Service, Serverless, Cloud application, Cloud resources, and Certificates. For Configuration Items, an IPv6 address list scan is enabled by default [S3].

MID Server selection within a schedule can be configured via `Auto-Select MID Server`, `Specific MID Cluster`, `Specific MID Server`, or `Use Behavior`. Auto-selection requires MID Servers to be assigned the Discovery or ALL applications and must have access to the configured IP ranges. IPv6 auto-select is not supported [S3].

Throughput and job management are handled by Event Framework properties. The property `com.glide.queue.discovery.cloud.sensors.processing_jobs.priority` manages worker priority for Cloud-based Discovery jobs; increasing this value decreases priority, with a default of `100`. This behavior applies only when `discovery.use.event.processing` is set to `true` [S4]. Similarly, `com.glide.queue.discovery.sensors.processing_jobs.priority` manages priority for IP-based Discovery jobs, though its specific default value is not stated in the supplied evidence [S4].

Deletion strategy and credential management are governed by `glide.discovery.exclude_ip_sync_classes` (already noted) and `com.snc.use_external_credentials`. The latter allows external storage of credentials with a default value of `true` [S1]. Additionally, `com.glide.codesigning.tracking.unsupported_script_tracking.enabled` controls script tracking for code signing on Cloud Discovery. When set to `true`, ECC queue records from unsupported scripts are not notarized, which can cause operations to fail; setting it to `false` enables Cloud Discovery on code-signed instances [S1].

## Canonical Order of Operations

The configuration lifecycle follows a strict sequence starting with role assignment and concluding with CMDB governance. First, the `discovery_admin` role must be granted to users responsible for configuring and executing Discovery, as this grants access to necessary tables [S2]. Second, physical or virtual servers hosting MID Servers must be installed and configured to communicate with the ServiceNow instance, ensuring they are assigned the Discovery or ALL applications [S2].

Third, login credentials for all computers, printers, and network gear must be set on the instance. Discovery automatically determines which credentials work for a particular device, but UNIX, vCenter, and SNMP credentials require explicit configuration [S2]. Fourth, MID Server connectivity must be verified by navigating to Discovery > MID Servers and checking logs on both the instance and the host agent directory [S2].

Fifth, Discovery schedules must be defined and run. The schedule controls when discoveries occur, defines the MID Server to use, and specifies the scan type (e.g., Configuration Items or Networks) [S3]. Finally, the Discovery Configuration Console is used to manage CI types and details. By default, Discovery finds all information specified in probes and patterns; users can control aspects like ARP data discovery or software package filtering before the instance updates the CMDB [S4].

## Assumptions / Gaps

The evidence does not state the specific default value for `com.glide.queue.discovery.sensors.processing_jobs.priority` [S4]. The evidence also does not detail the exact behavior of "Use Behavior" when a single schedule requires multiple MID Servers, nor does it specify the maximum number of IP addresses Shazzam scans can handle beyond referencing the `Max range size Shazzam probe` property [S3]. Furthermore, the evidence does not explicitly describe the deletion strategy properties other than implying CMDB updates occur after discovery data is returned and filtered [S4].
