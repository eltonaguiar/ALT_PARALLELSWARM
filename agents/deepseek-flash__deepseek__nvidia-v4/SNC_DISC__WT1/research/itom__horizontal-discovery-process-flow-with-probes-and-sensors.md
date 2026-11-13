# Horizontal discovery process flow with probes and sensors

- Source: https://www.servicenow.com/docs/r/zurich/it-operations-management/discovery/c_DiscoProcessFlows.html
- Release: Zurich
- Map: itom

---

# Horizontal discovery process flow with probes and sensors

Summarize Summarized using AI This content was generated using new OpenAI-powered functionality. Results are provided on an as is basis and are not guaranteed to be accurate or complete. Summary of Horizontal discovery process flow with probes and sensors The horizontal discovery process in ServiceNow systematically identifies and classifies devices on a network through four key phasesâScanning, Classification, Identification, and Explorationâusing probes and sensors. This process is initiated by the user via scheduled or on-demand discovery, targeting specific IP addresses or ranges. Show full answer Show less Process Phases Scanning Phase: The MID Server executes the Shazzam probe and port probes to detect open ports on target machines using protocols like WMI, HTTP, SSH, and SNMP. The responses help identify the machine type (e.g., Linux/UNIX if port 22 is open). Classification Phase: Based on port probe results, Discovery sends a classification probe that gathers additional system details, such as operating system version, to determine the CIâs class. Only one classification probe runs per discovered device. Identification Phase: Discovery selects the appropriate classifier for the CI class and runs the identification trigger probe. This probe uses identification rules to decide whether to insert or update CIs in the CMDB. The data returned is processed by sensors. Exploration Phase: Discovery executes exploration trigger probes defined in the classifier to collect further details about the CI. Sensors then update the CMDB accordingly, similar to the identification phase. Key Components Probes: Scripts run by the MID Server that gather information about devices during each phase. Sensors: Processes that interpret probe data and apply rules to update the CMDB. External Communication Channel (ECC) Queue: The communication mechanism through which probes and MID Server exchange discovery requests and results. MID Server: Executes probes against target devices and manages communication with the ServiceNow instance. Practical Benefits for ServiceNow Customers This detailed discovery flow enables customers to accurately identify, classify, and update configuration items (CIs) within their CMDB, ensuring data integrity and comprehensive asset visibility. By leveraging probes and sensors in an automated sequence, customers can efficiently discover complex environments, reduce manual effort, and maintain an up-to-date CMDB that supports IT service management processes.
The horizontal discovery process passes through the four phases of discovery using probes, which gather information on the target machine. Sensors then help Discovery determine what to do with that information.

## Kicking off Discovery

A user triggers horizontal discovery by configuring a discovery schedule or by launching an on-demand discovery with Discover now or Quick Discovery. The schedule specifies one or more IP addresses or
 range of IP addresses.

## Scanning phase

- Discovery first takes the Shazzam probe (and then port probes ) and places it in a request in the External Communication Channel (ECC) queue.
- The MID Server checks the ECC queue, retrieves the discovery request, and runs the probes against the host and discovers open ports.
- The port probes scan common ports using several protocols, such as WMI, HTTP, SSH, and SNMP.
- If one or more ports respond, the Shazzam probe sends information about the port back to the ECC queue through the MID Server.
- Discovery checks the ECC queue to find out which ports responded, which identifies the type of machine. For example, if Shazzam detects that the machine is listening on port 22, Discovery treats the machine as a UNIX or
 Linux machine.

## Classification phase

- The Discovery application determines which classification probe to send to the newly discovered device by using information in the record of the port probe that successfully responded.
- Discovery puts the classification probe into the ECC queue.
- The MID Server checks the ECC queue, retrieves the discovery request, and runs the classification probe.
- The classification probe retrieves additional information, such as which version of the operating system is running on a machine. This information determines the class of the CI that Discovery found. There is only one
 classification probe per discovered device.
- The classification probe sends information back to the instance ECC queue through the MID Server.

## The Identification phase

- Discovery determines which classifier to use based on the class of the CI and the criteria specified in all CI classifier records. The classifier specifies which probes to use for the next two phases.
- Discovery puts the identification trigger probe for the CI classifier into the ECC queue. For example, a UNIX machine running HP-UX would require the HP-UX classifier, which specifies that the Multi Probe- HP-UX Identity identification trigger probe. These probes use identification rules to determine whether or not to insert or update a CI in the CMDB. Note: The trigger probe could also be the Horizontal
 Pattern probe, which tells Discovery to follow the operations in the specified pattern, rather than sending out additional probes. The operations in the pattern cover both the identification and exploration phases.
 Discovery knows which identification rules to use based on the CI type, and Discovery makes inserts or updates to the CMDB based on these rules. Probes and sensors are not used.
- The MID Server checks the ECC queue, retrieves the discovery request, and runs the identification trigger probe.
- The identification probe accumulates identification data for each device and sends that data back to the instance via the MID Server.
- Discovery uses sensors for the identifier probe to process the information.
- Discovery performs the analysis on the CMDB using CI identifiers . Discovery can update existing CIs in the CMDB or create new ones.

## The Exploration phase

- Discovery looks at the Triggers Probes related list in the classifier to find exploration probes to run.
- Discovery puts the exploration trigger probe into the ECC queue.
- The MID Server checks the ECC queue, retrieves the discovery request, and runs the exploration trigger probes.
- The probes send data back to the instance via the MID Server and sensors make updates to the CMDB, just as in the identification phase.
