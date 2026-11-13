# v3 run

model: nvidia/nemotron-3.5-super-vl-120b-a12b
elapsed: 39.3s
research_calls: 4
error: None

## Question
What are the ServiceNow Discovery configuration options and properties, and in what order does Discovery processing happen (order of operations) when a device is discovered?

## Answer
# ServiceNow Discovery Configuration Options and Order of Operations

## Configuration Options and Properties

Based on the research evidence, ServiceNow Discovery configuration centers on the following:

**Discovery Methods**
After activating the Discovery application, there are two options to get started:
- **Agentless discovery**
- **Agent-based discovery**

**MID Server Configuration**
The MID Server (Management, Instrumentation, and Discovery Server) facilitates communication and data exchange between the ServiceNow instance and the client's environment. Key configuration considerations include:
- Number of MID Servers needed
- Number of servers, network devices, and data centers to support
- Geographies to be covered
- Data sources to integrate
- Cloud vendor infrastructure to support
- MID Server sizing (CPU, memory considerations for patterns producing large payloads such as Kubernetes, Cloud Discovery, or certain application patterns)
- MID Server Load Balancing or Failover clusters for Discovery Schedules with strict networking requirements

> Note: The research did not return an exhaustive list of specific `discovery.properties` system properties or all individual configuration properties. The evidence covers high-level implementation options and MID Server configuration considerations rather than a complete property reference.

## Order of Operations (Discovery Processing Phases)

When a device is discovered, Discovery processing happens in the following sequence:

### 1. Scanning (Port Scan)
The Shazzam probe scans TCP and UDP IP ports to determine which ports are open and attempts to get a response from open ports.

### 2. Classification
Begins right after the Shazzam port scanner probe and ends after processing those results, triggering the Identification phase. Based on the open ports, Discovery looks up the Port Probe table to determine what type of Classify probe needs to be launched. Each classification type dictates the probes that Discovery runs for the Identification and Exploration phases.

**Base-system classification priority order:**
- WMI > SSH > SNMP > CIM

### 3. Identification
Triggered after classification completes. The classification results determine which identification probes are launched.

### 4. Exploration
CI Classification triggers the initial probes launched during this phase. All exploration probes that meet the relevant conditions are triggered after the identification probe. This phase collects in-depth information about the device and its relationships.

**Important credential note:** A credential that is successful during Classification and Identification does not imply that it is successful during Exploration. Most probes use the same credentials used during Classification and Identification, however some probes have additional requirements.

## Sources

- [Quick Start Guide for Discovery - ServiceNow Community](https://www.servicenow.com/community/itom-articles/quick-start-guide-for-discovery/ta-p/3408613)
- [Troubleshooting the Classification Phase in Discovery - ServiceNow Support](https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB0535236)
- [Troubleshooting the Exploration Phase in Discovery - ServiceNow Support](https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB0535240)
- [Understand Phases of Discovery - ServiceNow Community](https://www.servicenow.com/community/itom-articles/understand-phases-of-discovery/ta-p/3116984)
- [What are the phases on the Discovery? - ServiceNow Community](https://www.servicenow.com/community/cmdb-forum/what-are-the-phases-on-the-discovery/m-p/2863593)
- [Discovery and MID Server Resources - ServiceNow Support](https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB0540193)
- [MID Server Sizing for Discovery - ServiceNow Support](https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB2729323)
- [Solved: MID server configuration - ServiceNow Community](https://www.servicenow.com/community/developer-forum/mid-server-configuration/m-p/2762368)

## Transcript
```
[0] research(ServiceNow Discovery configuration options properties order of operations device discovery) -> 1077c
[0] research(ServiceNow Discovery order of operations classification identification exploration) -> 1878c
[1] research(ServiceNow Discovery configuration properties discovery.properties MID server configuratio) -> 1922c
[1] research(ServiceNow Discovery phases order classification identification exploration port scan orde) -> 2251c
[2] no tool call: Based on the research evidence available, here is what can be determined about ServiceNow Discovery configuration options/properties and the order of 
[3] answer()
```
