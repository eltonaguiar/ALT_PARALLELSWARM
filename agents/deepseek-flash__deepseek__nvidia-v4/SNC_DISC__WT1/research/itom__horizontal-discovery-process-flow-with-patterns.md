# Horizontal discovery process flow with patterns

- Source: https://www.servicenow.com/docs/r/zurich/it-operations-management/discovery/disco-process-flow-patterns.html
- Release: Zurich
- Map: itom

---

# Horizontal discovery process flow with patterns

Summarize Summarized using AI This content was generated using new OpenAI-powered functionality. Results are provided on an as is basis and are not guaranteed to be accurate or complete. Summary of Horizontal discovery process flow with patterns The horizontal discovery process with patterns in ServiceNow Zurich release streamlines the identification and exploration of Configuration Items (CIs) on a network. Unlike traditional discovery that relies on multiple probe sets, this method uses patterns to trigger operations in the final phases, providing a more unified and efficient approach to updating the CMDB. Show full answer Show less Key Features Scanning Phase: Discovery initiates by placing the Shazzam probe and port probes in the External Communication Channel (ECC) queue. The MID Server executes these probes to scan for open ports and identify machine types based on port responses, such as recognizing UNIX/Linux systems by port 22. Classification Phase: Based on open port data, Discovery selects and runs a classification probe to gather detailed system information like operating system version. This data determines the CI class, with only one classification probe run per device. Identification and Exploration Phases: Patterns unify these phases by selecting classifiers and horizontal pattern probes based on CI class and classification criteria. The pattern contains a sensor that performs CMDB updates by applying identification rules and exploration operations specific to the CI type. Credential Requirements: Both host machine access credentials and applicative credentials are necessary to discover applications running on the hosts effectively. Use of Probes and Sensors: Only the Horizontal Discovery Sensor is used in these phases; other probes and sensors are not utilized. Practical Implications for ServiceNow Customers This discovery method enables customers to efficiently identify and explore network devices, ensuring accurate and up-to-date CMDB records. By leveraging patterns, customers can reduce complexity and improve discovery accuracy, especially for application-level details that require applicative credentials. Proper credential configuration is critical to success. Understanding this process helps customers optimize their discovery workflows and maintain a reliable configuration management system.
Horizontal discovery with patterns has four phases, just as horizontal discovery with
 probes does. However, for the last two phases, Discovery triggers operations from a pattern,
 rather than additional sets of probes.

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

## The Identification and Exploration phases

Patterns unify the Identification and Exploration phases of discovery.

- Discovery determines which classifier to use based on the class of the CI and the criteria
 specified in all CI classifier records. The classifier specifies the Horizontal Pattern
 probe , which in turn specifies which pattern to launch. The Horizontal pattern probe
 also contains a sensor which does the actual work of updating the CMDB. Note: Patterns need
 applicative credentials to find applications running on host machines. Make sure you have
 applicative credentials configured along with the credentials required to access the host
 machine itself.
- The operations in the pattern specify the actions that Discovery needs to take for both the
 identification and exploration phases. Discovery knows which identification rules to use based
 on the CI type in the pattern, and Discovery makes inserts or updates to the CMDB based on
 these rules. Only the Horizontal Discovery Sensor is used. Other probes and sensors are not
 used.
