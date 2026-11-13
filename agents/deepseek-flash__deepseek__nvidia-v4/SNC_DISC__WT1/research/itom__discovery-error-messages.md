# Discovery error messages

- Source: https://www.servicenow.com/docs/r/zurich/it-operations-management/discovery/c_DiscoveryErrorMessages.html
- Release: Zurich
- Map: itom

---

# Discovery error messages

Summarize Summarized using AI This content was generated using new OpenAI-powered functionality. Results are provided on an as is basis and are not guaranteed to be accurate or complete. Summary of Discovery error messages This guide helps ServiceNow customers quickly identify, understand, and resolve common error messages encountered during Discovery runs in the Zurich release. It covers typical error categories, their causes, and practical troubleshooting steps, enabling smoother and more reliable Discovery operations. Show full answer Show less Common Error Categories Input/output errors: Issues like connection failures, timeouts, protocol unsupported, file not found, and invalid parameters that affect communication during Discovery. Authentication errors: Failures due to missing or invalid credentials, including SSH and Windows PowerShell authentication problems. Command errors: Timeouts, invalid commands, parsing errors, or terminal session issues that disrupt probe execution. Generic component errors: Invalid or improperly configured Discovery components. General errors: Examples include XML parsing problems caused by special characters in passwords or simultaneous IP address targeting warnings. Key Error Messages and Causes Authentication failures: Occur when credentials are missing or incorrect. Add the correct credentials to the Discovery credentials table to resolve. PowerShell impersonation failed: Requires domain-qualified usernames in credentials. WMI connection failures: Often caused by incorrect MID Server service credentials, insufficient permissions, firewall restrictions, or corrupted WMI repository. Result file missing: May result from restricted write permissions to admin shares; adjust permissions accordingly. Oracle Sneep tool requirement: For Solaris serial number discovery, root credentials and Oracle Sneep tool installation are necessary. Version mismatches in probes and sensors: Major or minor version differences between probes and sensors cause processing errors or warnings; aligning versions resolves these issues. Missing sensors: Every probe requires an active corresponding sensor; missing sensors cause errors needing activation or installation. XML parsing errors: Occur if probe data contains unescaped special characters or malformed XML. Escaping characters or using CDATA sections helps resolve these. Probe not found: Happens when the sensor processor cannot locate the associated probe record; verify the probe sysid and probe cache integrity. Troubleshooting and Resolution Steps Verify and add proper credentials in the Discovery credentials table to avoid authentication errors. Check MID Server service account permissions and firewall configurations for WMI-related connection issues. Run specified WMIC or PowerShell commands from the MID Server host to test connectivity and permissions with target devices. Align probe and sensor versions to prevent processing errors due to version mismatches. Ensure that corresponding sensors are active for every probe to avoid "No sensors defined" errors. Correct JavaScript errors in sensor scripts to fix sensor processing failures. Escape special characters in passwords saved in XML files to prevent XML parsing errors. Increase or disable MID Server payload size limits if probe results exceed default limits. Practical Impact By understanding these error messages and their resolutions, ServiceNow customers can effectively diagnose Discovery run issues, reduce downtime, ensure accurate Configuration Item (CI) data collection, and maintain reliable Discovery operations.
Review common
Discovery
error messages and their causes to identify and resolve issues that occur during discovery runs.

## Common error messages

Input/output errors
- CONNECTION_FAILED
- CONNECTION_TIMEOUT
- CONNECTION_REFUSED
- CONNECTION_CIPHER_UNSUPPORTED
- CONNECTION_PROTOCOL_UNSUPPORTED
- CONNECTION_LOST
- INVALID_CONNECTION_PARAMETER
- FILE_NOT_FOUND
- IO_ERROR
Authentication errors
- NO_CREDENTIALS
- AUTHENTICATION_FAILED
- INVALID_CREDENTIALS_TYPE
SSH errors
- SSH_SHELL_UNSUPPORTED
- SSH_SCRIPT_TRANSFER_FAILED
- SSH_INVALID_SESSION
Windows errors
POWER_SHELL_VERSION_UNSUPPORTED
Command errors
- COMMAND_TIMEOUT
- INVALID_COMMAND
- COMMAND_FILTER_ERROR
- COMMAND_PARSER_ERROR
- COMMAND_KEY_MAPPER_ERROR
- COMMAND_VALUE_NORMALIZER_ERROR
- TERMINAL_SESSION_LOST_ERROR
- TERMINAL_SESSION_ENVIRONMENT_MODIFICATION_ERROR
Generic component errors
- INVALID_COMPONENT
- INVALID_COMPONENT_PARAMETER
- INVALID_OPERATION

## General error messages

Message: org.xml.sax.SAXParseException: The entity name must immediately follow the '&'
 in the entity reference
A version of this message occurs if you have used special characters in a password that is
 saved in an XML file.
Message: Identified, ignored extra IP
This message can appear at the end classification phase of
Discovery
if a targeted IP address belongs to a device that is being discovered at the same time.
For example, a
Windows
server has two NIC cards with two IP addresses.
Discovery
targets both IP addresses within the same
Discovery
schedule. This message is generated to note that second IP address is ignored because we don't want to update the same CI twice within the same
Discovery
run.

This message is a warning and is expected. No action is needed.

Message: Authentication failures
The discovery process could not discover the CI because the discovery application could not
 authenticate. To resolve, add the credentials of that machine in to the discovery credentials
 table.
Message: Identified, not updating CI, now finished
No match on any of the CI Identifiers.
Message: The impersonation of user failed
This message originates in the Powershell. Check that the domain is specified along with
 the user name in the credentials.
Message: Connection failed to WMI service. Error: Permission denied
This message originates in WMI. Check that the
MID Server
service is running with the
 correct credentials and has access to the target device.
To check this, run the following
 command from the command prompt on the
MID Server
host:

wmic /node:target /user:user /password:password path win32_operatingsystem
target = IP address of target device
user = user account used by the mid server service
password = password used by the mid server service
Message: Connection failed to WMI service. Error: The remote server machine does not exist
 or is unavailable
This message originates in WMI. Check that the
MID Server
service account has access to the
 targeted machine. Check if a domain admin account is used as the
MID Server
service account. Check if any
 existing firewalls are open to the connection. To check this, run the following command from
 the command prompt on the
MID Server
host.
Execute for runner_type=WMI:

wmic /node:"<target>" /user:"<user>" /password:"<password>" path win32_operatingsystem
From within a Powershell console on the mid server host, execute for runner_type=Powershell:
gwmi win32_operatingsystem -computer <ip> -credential '<username>'
Message: Provider is not capable of the attempted operation
WMI repository was corrupted. After following the "WMI: Repository Corruption, or Not?"
 article on the
Microsoft TechNet site
, the problem was corrected.
Message: The result file can't be fetched because it doesn't exist
PRB581515 - Powershell does not work when customer has locked down write rights to admin
 share.
Message: Please run sneep as root to ensure correct serial number from fserial data
 source
The
Oracle
Sneep
command line tool must be installed for the Solaris - Serial Number probe to work correctly. There is a
known limitation
with Fujitsu PRIMEPOWER devices. To work around this limitation, run the
Solaris
discovery with root credentials.

## Discovery sensor error messages

Message: The multisensor will not process because its major version = X while
 probe_name responding script's major version = Y
This error message indicates that there is a major version mismatch.
Message: Payload length exceeds limit of 5000000
This error message indicates that the
Discovery
probe results exceed the limit. The
MID Server
will discard the results and return a warning message. To resolve, set the value of the
mid.discovery.max_payload_size
MID Server
property to any negative number (for example, -1). This disables the payload limit and allows payloads of any size to be sent to the instance.
Message: The multisensor will not process because its responding script's major version =
 X while its referenced probe probe_name major version = Y
This error message indicates that there is a major version mismatch.
Message: sensor_name sensor's major version = X while its related probe's major version =
 Y
This error message indicates that there is a major version mismatch in the probe and sensor versions and the sensor will stop processing until this condition is resolved.
Message: sensor_name multisensor's minor version = X while probe_name responding script's
 minor version = Y
This error message indicates that there is a minor version mismatch.
Message: sensor_name multisensor's responding script's minor version = X while its
 referenced probe probe_name minor version = Y
This error message indicates that there is a minor version mismatch.
Message: sensor_name sensor's minor version = X while its related probe's minor version =
 Y
This error message indicates that there is a minor version mismatch in the probe and sensor versions. Processing will continue, but you may want to resolve this condition.
Message: Sensor error when processing . . . : No sensors defined
Every active probe looks for a corresponding sensor to process the data that is collected by the probe. This error message indicates that the corresponding sensor for the probe is missing or inactive.
Message: Sensor error when processing . . . : typeError: . . .
This error message indicates that the sensor has one of the core error constructors in JavaScript.
Message: Sensor error when processing ...: Exception while processing sensor:
 XML Parse Problem: ![CDATA]
This XML parsing error occurs when the discovery sensor fails to parse the input ECC queue
 payload. The payload is not formatted according to XML specifications. Possible solutions
 include:
- Escape problematic characters. For example, change < to &lt and & to &amp .
- Escape entire blocks of text with CDATA sections, or put encoding declarations at the
 start of the text.
- Remove any whitespace characters (space, tabs, newlines) before the XML
 declarations.
Message: Sensor error when processing
Linux
- Network ARP Tables: Exception while running probe post processing script: No XML data
The system displays the No XML data error when the XML sensor processor fails to ï¬nd the expected XML data in the probe output. During sensor processing,
Discovery
attempts to retrieve the probe results but finds the probe output empty. Verify that the probe returns the correct output for the sensor to process.
Message: Sensor error when processing Shazzam: Exception while running probe
 post processing script: Probe not found: null
The Probe not found error occurs when the sensor processor fails to ï¬nd the probe record supposedly associated with the sensor. During sensor processing,
Discovery
gets the probe record from the probe cache and stores it for later reference. The "Probe not found" error occurs either when the sys_id of the probe cannot be found or there is an issue with
 the probe cache.
See
Find the cause of a "Probe not found" error
for more information.
