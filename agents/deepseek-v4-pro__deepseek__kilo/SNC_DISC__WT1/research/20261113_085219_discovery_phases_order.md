# discovery_phases_order

query: ServiceNow Discovery phases order of operations scan classify identify explore patterns

## Evidence (3 sources)

SOURCE: https://www.servicenow.com/community/itom-articles/understand-phases-of-discovery/ta-p/3116984
TITLE: ServiceNow
  - > In this phase TCP and UDP IP port are scanned by discovery to determine which port is open and also try to get response from the open port
  - > Go to discovery Schedule and click on quick discovery , Provide ip and select mid server.
  - Now in Discovery logs you can find error if there is any error occur while discovery is running.
  - > In this phase discovery collects in depth information about the device and their relationships.
  - > Based on port no it will classify which type of machine it is like Windows or Linux. as above port no is 135 so it will classify as windows

SOURCE: https://www.servicenow.com/community/cmdb-forum/what-are-the-phases-on-the-discovery/m-p/2863593
TITLE: ServiceNow
  - Can you help me to know what are the phases on the Discovery, please?
  - #1 What is Discovery in ServiceNow | Overview of Discovery | ServiceNow Discovery Training
  - This is a new training for Discovery in ServiceNow. In this training you will learn about Discovery and How it is implemented in ServiceNow. This training targets ServiceNow Administrators, ServiceNow Developers, ServiceNow Product Owners and ServiceNow Implementers who wants to implement ...
  - 2) Classification: This phase attempts to classify the device precisely.
  - 4) Exploration: Patterns are used to gather more detailed information to populate CI attributes.

SOURCE: https://www.servicenow.com/community/itom-articles/servicenow-discovery-overview/ta-p/2321453
TITLE: ServiceNow
  - In the ECC queue can identify the 4 phases of discovery that are executed for each device. Port Scanning (Shazzam), Classify, identify and exploration. The ecc queue has two Queue column values and four State column values.
  - Run this type of discovery to find applications on host machines without the need to discover the host first. Serverless discovery relies on patterns to explore CIs on a host.
  - In scanning the IP Ranges we look primarily for responses from WMI, SSH and SNMP. When we see an IP has a state of OPEN for any of these three ports we move onto the next phase of discovery, classification. If we get no response we do not list it and if we get some response other then open we identify the same. Results can be found in the input of the ‘Shazzam’ probe of your scan.
  - Note: The trigger probe could also be the Horizontal Pattern probe, which tells Discovery to follow the operations in the specified pattern, rather than sending out additional probes. The operations in the pattern cover both the identification and exploration phases. Discovery knows which identification rules to use based on the CI type, and Discovery makes inserts or updates to the CMDB based on these rules. Probes and sensors are not used.
  - Patterns - Patterns, like probes and sensors, are a series of operations that also collect data on a host, process it, and update the CMDB. Patterns differ from probes and sensors in that they are written in Neebula Discovery Language (NDL) rather than JavaScript, and they are called into action in the later stages of the horizontal discovery process. Default patterns are provided, but you can also customize or create patterns using the Pattern Designer.

## All search hits

- [ServiceNow](https://www.servicenow.com/community/itom-articles/understand-phases-of-discovery/ta-p/3116984) score=4
- [ServiceNow](https://www.servicenow.com/community/cmdb-forum/what-are-the-phases-on-the-discovery/m-p/2863593) score=4
- [ServiceNow](https://www.servicenow.com/community/itom-articles/servicenow-discovery-overview/ta-p/2321453) score=4
- [ServiceNow](https://www.servicenow.com/community/cmdb-forum/about-discovery-phases/m-p/2615126) score=4
- [ServiceNow](https://www.servicenow.com/docs/r/it-operations-management/discovery/c-UsingPatternsForHorizontalDiscovery.html?contentId=Sa1vU6Eh9XtEhh2dcScrhQ) score=3
- [ServiceNow](https://www.servicenow.com/docs/r/zurich/it-operations-management/discovery/discovery-classifiers.html) score=3
- [https://quizlet.com  ›  sg  ›  919237810  ›  cis-service-mapping-flash-cards](https://quizlet.com/sg/919237810/cis-service-mapping-flash-cards/) score=0
- [https://www.youtube.com  ›  shorts  ›  UuefjjsrNyM](https://www.youtube.com/shorts/UuefjjsrNyM) score=0