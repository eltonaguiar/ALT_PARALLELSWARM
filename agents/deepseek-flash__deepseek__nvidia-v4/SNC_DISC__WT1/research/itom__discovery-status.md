# Discovery status

- Source: https://www.servicenow.com/docs/r/zurich/it-operations-management/discovery/c_DiscoveryStatus.html
- Release: Zurich
- Map: itom

---

# Discovery status

Summarize Summarized using AI This content was generated using new OpenAI-powered functionality. Results are provided on an as is basis and are not guaranteed to be accurate or complete. Summary of Discovery status The Discovery status in ServiceNow provides a comprehensive summary of each Discovery execution initiated from a schedule. It enables you to monitor, analyze, and manage Discovery runs, including the ability to cancel ongoing Discoveries. This feature is essential for ensuring the accuracy and efficiency of your Configuration Management Database (CMDB) updates and troubleshooting Discovery activities. Show full answer Show less Key Features Access and Navigation: You can access the Discovery Status form under Discovery > Status, where each record corresponds to a Discovery execution by a schedule. Status Details: Records include details such as the Discovery date, mode, number of probes sent, sensors processed, and the Discovery state (Starting, Active, Completed, Canceled). Discovery Timeline: A graphical display showing the sequence and details of probes and sensors used during the Discovery process. Discovery Log Entries: Logs include classification failures, CMDB updates, authentication issues, and other actions associated with the Discovery status. ECC Queue Entries: Shows the communication flow between your ServiceNow instance and integrated systems (e.g., MID Server), including XML payloads for probe and sensor activities. Device History: Summarizes all devices scanned during the Discovery and actions taken on the CMDB by sensors. Cancellation Capability: Allows manual cancellation of a Discovery while it is in progress directly from the Discovery Status record. Discovery Status Monitoring Job: Automatically analyzes Discovery schedules with no status updates after a defined period, primarily for those discovering configuration items. Refresh Function: Updates related tabs such as the Discovery Log and ECC Queue for ongoing Discoveries to provide real-time data. Practical Use and Benefits ServiceNow customers use the Discovery status to effectively monitor and manage their Discovery operations. It provides actionable insights that help quickly identify and troubleshoot failed or incomplete Discoveries by examining probe and sensor behavior. The timeline and log views offer detailed visibility into the Discovery process, aiding in root cause analysis. Moreover, the ability to cancel Discoveries in progress offers operational control to avoid unnecessary resource consumption. By leveraging the Discovery status, customers can maintain an accurate and up-to-date CMDB, improve Discovery reliability, and streamline troubleshooting when issues arise.
The Discovery status provides a summary of a Discovery launched from a schedule. You can also cancel a Discovery that is in progress from the status form.

Note:
Discovery schedules that have no status updates for a over a defined number of minutes are analyzed automatically by the Discovery Status Monitor job. By default, this job applies to Discovery schedules that discover
 configuration items. For more information, see the
Discovery Status Monitoring Job
article in the Now Support Knowledge Base.
To access the
Discovery
Status form, navigate to
Discovery > Status
and open the status record for a Discovery.

Each record in the Status list represents the execution of a
Discovery
by a schedule. It displays high-level information such as the date of the
Discovery
, the mode, the number of probe messages sent to devices, and the number of sensor records that were processed. A status record contains data that can help you troubleshoot a failed discovery. Use this
 data to troubleshoot the behavior of individual probes and sensors or even run those elements separately. Use the status controls to enter probe/sensor threads at any point for a specific
Discovery
, and then follow the process in either direction. You can also clearly see which classification probe ran and discovered a particular device by viewing the classification probe column in the device
 list.

- Refresh : Refreshes the related tabs, including the Discovery Log and ECC Queue for
 discoveries still in progress.
- Discovery timeline : The Discovery timeline is a graphical display of a discovery, including information about each probe and sensor that was used.
- Discovery log entries : The Discovery Log shows information such as classification failures, CMDB updates, and authentication failures. A Discovery Log record is created for each action associated with a discovery status.
- ECC queue entries : Entries in the ECC queue provide you with a
 connected flow of probe and sensor activity. They also include the actual XML payload that is
 sent to or from an instance.
- Device history : The device history provides a summary of all the
 devices scanned during discovery, and what action sensors took on the CMDB.
Note:
By default, only 30 days of
Discovery
records are displayed in the
 status list at a time.
The following
Discovery
status record shows the discovery of a load balancer using a pattern.
Figure 1. Example Discovery status record
Field Description
Number An auto-generated number for the record. Description How this discovery was run. Typically, the description is Scheduled , but if you ran discovery manually from a Schedule, the record would show Discover Now in the Description field. Schedule The name of the Discovery schedule. State The state of the discovery: Starting Active Completed Canceled Started and Completed The number of probes started and completed during discovery. Source Optional read-only field that shows the source of the discovery, such as Schedule Discovery , or Quick Discovery . If the source of the Discovery was from an API call,
 the source is DiscoveryAPI . From Schedule (Read-only schedule data) Discover Shows the Discovery type. The possible types are: Configuration items , IP addresses , Networks , or Processes/Connections (ADM). Max Run Time Displays the maximum amount of time Discovery was permitted to run
 on this schedule. Log state changes Indicates that state changes were logged during this Discovery . These states can be
 seen in the Last and Current fields in
 the Discovery Devices list in this form.
