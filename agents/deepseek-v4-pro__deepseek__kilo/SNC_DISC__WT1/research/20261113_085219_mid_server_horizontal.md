# mid_server_horizontal

query: ServiceNow horizontal discovery pattern MID server probes sensors

## Evidence (3 sources)

SOURCE: https://www.servicenow.com/community/itom-forum/probes-vs-patterns/m-p/903666
TITLE: ServiceNow
  - Patterns are the future-state for Discovery and would be the recommended path for future custom enhancements. Customers on instances Jakarta and later are defaulted to using the horizontal pattern Discovery where it is applicable. Not every probe/sensor has been converted over to Patterns, which is mostly in regards to SNMP Discovered devices. I believe most, if not all, server-based Discovery has been converted.
  - Switching from probes/sensors to patterns. Something to think about...
  - I am trying to understand the advantages and disadvantages of using Patterns vs Probes for Discovery.
  - Also, if patterns are a more preferred way to do Discovery, do we have patterns available as a substitute for all the probes?
  - If we have to use Patterns and not Probes, do we need to do any specific configuration like disabling the OOB Probes? How do I tell Discovery that it shouldn't use the Probes but Patterns?

SOURCE: https://www.servicenow.com/community/itom-articles/servicenow-discovery-overview/ta-p/2321453
TITLE: ServiceNow
  - Note: The trigger probe could also be the Horizontal Pattern probe, which tells Discovery to follow the operations in the specified pattern, rather than sending out additional probes. The operations in the pattern cover both the identification and exploration phases. Discovery knows which identification rules to use based on the CI type, and Discovery makes inserts or updates to the CMDB based on these rules. Probes and sensors are not used.
  - Patterns - Patterns, like probes and sensors, are a series of operations that also collect data on a host, process it, and update the CMDB. Patterns differ from probes and sensors in that they are written in Neebula Discovery Language (NDL) rather than JavaScript, and they are called into action in the later stages of the horizontal discovery process. Default patterns are provided, but you can also customize or create patterns using the Pattern Designer.
  - The horizontal discovery process passes through the four phases of discovery using probes, which gather information on the target machine, and then sensors, which help Discovery determine what to do with that information.
  - The MID Server checks the ECC queue, retrieves the discovery request, and runs the exploration trigger probes.
  - • The MID Server checks the ECC queue, retrieves the discovery request, and runs the probes against the host and discovers open ports.

SOURCE: https://www.servicenow.com/community/s/cgfwn76974/attachments/cgfwn76974/impact-forum/5061/1/ServiceNow%20Discovery%20Fundamentals%20.pdf
TITLE: ServiceNow
  - /Contents (Horizontal discovery with patterns has four phases, just as horizontal discovery with probes does. However, for the last two phases, Discovery triggers operations from a pattern, rather than additional sets of probes.)
  - /Contents (The horizontal discovery process passes through the four phases of discovery using probes, which gather information on the target machine, and then sensors, which help Discovery determine what to do with that information.)
  - /Contents (Discovery uses the Horizontal Pattern probe to launch patterns for horizontal discovery.)
  - /Contents (Create a Discovery behavior to determine which probes Shazzam launches and which MID Server is used.)
  - /Contents (The Discovery application follows this sequence to find a MID Server.)

## All search hits

- [ServiceNow](https://www.servicenow.com/community/itom-forum/probes-vs-patterns/m-p/903666) score=4
- [ServiceNow](https://www.servicenow.com/community/itom-articles/servicenow-discovery-overview/ta-p/2321453) score=4
- [ServiceNow](https://www.servicenow.com/community/s/cgfwn76974/attachments/cgfwn76974/impact-forum/5061/1/ServiceNow%20Discovery%20Fundamentals%20.pdf) score=4
- [ServiceNow](https://www.servicenow.com/docs/r/it-operations-management/discovery/r-HorizontalPatternProbe.html) score=3
- [ServiceNow](https://www.servicenow.com/docs/r/it-operations-management/discovery/c-UsingPatternsForHorizontalDiscovery.html) score=3
- [ServiceNow](https://www.servicenow.com/docs/r/zurich/it-operations-management/discovery/c_DiscoProcessFlows.html) score=3
- [ServiceNow](https://www.servicenow.com/docs/r/yokohama/it-operations-management/discovery/disco-process-flow-patterns.html?contentId=fu08_XXG7teXgr0FF~83mw) score=3
- [LinkedIn](https://www.linkedin.com/posts/praveen-amirineni-4b3ba425a_servicenow-itom-discovery-activity-7469914291396100096-mtA0) score=0