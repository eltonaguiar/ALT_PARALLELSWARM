# Discovery Admin Workspace Diagnostics

- Source: https://www.servicenow.com/docs/r/zurich/it-operations-management/discovery/discovery-admin-workspace-diagnostics.html
- Release: Zurich

---

# Discovery Admin Workspace Diagnostics

Summarize Summarized using AI This content was generated using new OpenAI-powered functionality. Results are provided on an as is basis and are not guaranteed to be accurate or complete. Summary of Discovery Admin Workspace Diagnostics The Discovery Admin Workspace Diagnostics page in ServiceNow provides a centralized interface to identify, prioritize, and resolve errors and anomalies in IP-based and Cloud Discovery schedules. It enables administrators to monitor discovery health, create error tasks, track resolution progress, and utilize support tools and logs for troubleshooting. This functionality is available starting with Discovery Admin Workspace version 1.17.0. Show full answer Show less Key Features Anomaly Detection Tab: Displays Discovery schedules with anomalies within configurable timeframes. Anomalies are categorized by severity (Critical, Major, Minor) and type (Failed run, low CI discovery rate, increased errors, long run time). Administrators can filter and prioritize anomalies, refresh data visualizations, and clear anomaly records. Anomaly detection requires at least five CIs and must be enabled in settings. Diagnostics Tab: Lists all Discovery errors with options to create or edit error tasks, or ignore errors. Filters allow sorting by schedule, error type (e.g., CMDB, Credentials, Network), priority, and task status. Selecting errors links to detailed error stats pages, instructions, and Knowledge Base articles. Administrators can perform actions on individual IP addresses such as retrying discovery or adding to exclusion lists. Case Management Tab: Provides an overview of error task statuses with options to create new tasks and navigate to detailed records. Displays tasks in Kanban or List views and supports filtering by Discovery schedule and task name. Support Tools Tab: Offers a suite of investigation and troubleshooting tools to assist with Discovery issues. Logs Tab: Enables access to ECC Queue and Discovery Logs with filtering, exporting, and detailed entry views to aid in problem diagnosis. Ignored Errors Tab: Tracks errors ignored within the last 30 days, allowing administrators to reinstate errors back into active diagnostics. Virtual Agent Chatbot: Available on each tab to provide guided diagnostic assistance. The chatbot supports specific diagnostic requests such as MID Server health checks, pattern synchronization, discovery performance metrics, and log retrieval. The virtual agent is enabled via a system property. Practical Benefits for ServiceNow Customers Proactive Issue Management: Quickly identify and categorize Discovery schedule anomalies to prioritize remediation efforts effectively. Error Resolution Workflow: Create and manage error tasks directly from diagnostics to streamline issue tracking and resolution. Comprehensive Filtering: Use flexible filters to focus on critical errors or specific Discovery schedules, improving operational efficiency. Integrated Support Tools: Access logs and diagnostic utilities within the workspace to reduce troubleshooting time and improve root cause analysis. Automated Assistance: Leverage the virtual agent chatbot for guided diagnostics, MID Server validations, and performance insights without leaving the workspace. Improved Data Accuracy: Manage ignored errors and refresh anomaly data to maintain up-to-date and actionable insights.
The Diagnostics page helps you prioritize and address errors and anomalies in IP-based and
Cloud Discovery
schedules. Resolve issues by creating error tasks, tracking progress, and using support tools and logs.

To access the
Discovery Admin Workspace
Diagnostics page, navigate to
Workspaces > Discovery Admin Workspace > Diagnostics
.
Note:
The capabilities described here are available starting with
Discovery Admin Workspace
v1.17.0. Specific version requirements are noted for individual features where applicable.

## Key features

Anomaly detection tab
Displays all the
Discovery
schedules with anomalies detected in a certain time period. You can configure this time scale on the
Settings
page.
Important:
This tab only displays anomalies when anomaly detection is enabled. Starting with v1.11.0, anomaly detection requires a minimum of five CIs to trigger. For more information, see the
https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB2601541
article in the
Now Support
Knowledge Base
.
Select the
More Options
icon (
), then select
Refresh
to refresh the data for each visualization in this section.

Table 1. Data visualizations
Report title Type Description
Schedules with anomalies Indicator Number of Discovery schedules with anomalies detected over a certain time period. Schedules are categorized as the following: Critical anomalies: Failed to run. Major anomalies: Have a low CI discovery rate. Minor anomalies: Have a long run time or a high error count. Failed schedules Indicator Number of Discovery schedules that failed to run. Low CI discovery rate Indicator Number of Discovery schedules that have a low CI discovery rate. Note: The threshold for the CI discovery rate can be configured on the Settings page. Increased error count Indicator Number of Discovery schedules that have an increased error count. Note: The threshold for the error count can be configured on the Settings page. Long run time Indicator Number of Discovery schedules that had a long run time. Note: The threshold for the run time can be configured on the Settings page.
Selecting any of the indicators filters the table to reflect the schedules represented in the data count. For each entry in the table, you can view details around the type and severity of anomalies.

The
Actions
drop-down menu provides a direct shortcut to the Settings page for configuring anomaly detection. Additionally, the menu includes a
Clear
                                all anomalies
option so that administrators can quickly remove records in the Discovery Schedule Anomaly [discovery_schedule_anomaly] and Discovery Schedule Anomaly Metrics
 [discovery_schedule_anomaly_metrics] tables.

Use the
Filter by
options to prioritize and address anomalies. Filter
Discovery
schedules by name using the
Schedules
drop-down menu. Additionally, you can prioritize the results with the
Severity
drop-down menu,
 which includes options such as Critical, Major, and Minor. Use the
Anomaly type
drop-down menu to quickly view schedules with the same anomaly. Available options include Failed schedule,
 Low CI discovery rate, Increased error count, and Long run time.

Diagnostics tab
Displays all errors from every discovery. For each entry in the
Discovery errors
table, you can either create an error task or ignore the error using the
Create task
and
Ignore
buttons. If an entry already has an error task, it displays the
Edit task
button along with the task's name and priority.

Use the
Filter by
options to prioritize and address errors. You can filter by
Discovery
schedule with the
Schedule
drop-down menu, or search for the name of the error with the
Search
bar. Use the
Sort
drop-down menu to organize the results by Code, Priority, and Total Errors, in either ascending or descending order.

The error records can also be filtered with the
Filter by
and
Has task
drop-down menus. In the
Filter
menu, you can choose to show only errors
 related to CMDB, Configuration, Credentials, Internal, or Network. Multiple categories can be selected at the same time. The
Has task
menu shows either all error records, error records that
 have a task, or error records without a task.

For each entry in the
Discovery errors
table, the
Total Errors
number can be selected to navigate to the
Error Stats Page
. This page displays
 information on the error and provides
Instructions
, and an associated
Knowledge Base
article when available. If the error has an associated task, the task number is displayed in the header and can be accessed by selecting the button. The
Action
drop-down menu provides suggested actions based on the type of error. In the
Errors
table, use the
Action on selected
list to select an action for individual IP addresses. Available actions include ignoring errors, retrying discovery, adding addresses to the global exclusion list, or checking their Shazzam port status.

Case Management tab
Provides an overview of the statuses of error tasks. You can select each task to navigate to its detailed record. New tasks can be created and associated with existing errors using the
Create
                            Task
button. You can filter by
Discovery
schedule with the
Schedule
drop-down menu, or search for the name of the error task with the
Search
bar. Use the
Kanban Board
                            View
and
List View
to change the display style.
Support tools
The
Support tools
tab provides tools to investigate and troubleshoot your instance. For a full list of the tools available on this tab, see
Discovery Admin Workspace support tools
.
Logs
The
Logs
tab enables you to access the
ECC Queue
and
Discovery Logs
. Reviewing these logs can help diagnose and resolve errors. You can select an
 entry in the log to view more details. Additionally, the tables can be filtered or exported using the corresponding buttons.
Ignored Errors tab
Keeps a record of all errors ignored in the last 30 days. Errors older than 30 days are deleted. You can add an error back to the
Discovery errors
table using the
Undo
                            ignore
button.

## Virtual agent chat

The Diagnostics page features a virtual agent chatbot in each tab. This chatbot can help retrieve diagnostic information for troubleshooting issues with
Discovery
. You can either enter a specific request or select
Show me everything
to view all available options.
Important:
The virtual agent only displays when the
sn_disco_workspace.visibility_diagnostic_utility.enabled
property is set to
true
.
Selecting the
Discovery & MID Server Health Validation
prompt provides the following options:
- MID Server Pre-Upgrade Check: Enables you to run on-demand tests on the MID Server before upgrading. It identifies issues that might stop the upgrade process and provides a log to help resolve any issues found.
- MID Server Status Validation: Validates that the MID Server user is active and is part of the mid_server group, and checks for basic user authentication errors.
- MID Server Mutual Authentication: Enables you to select a specific user and verify that the user has an active, non-expired certificate.
- Pattern Synchronization Validation: Verifies that a pattern and its related libraries are synchronized with the given MID Server and determines if theyâre custom.
Selecting the
MID Server Settings Retriever
prompt enables you to retrieve settings from the available
MID Servers
. If thereâs more than one
MID Server
, the agent provides a list of
MID Servers
to choose from. Then, you can download the configuration file and analyze the configuration values for the selected
MID Server
.

Selecting the
Discovery Performance Metrics
prompt examines the ECC Queue to gather performance metrics for a discovery status, providing the following information:
- Average wait times for processing ECC Queue inputs.
- Average wait times for the MID Server to process ECC Queue outputs.
- Information about the probes or sensors that took the longest time to complete their tasks.
Selecting the
Retrieve Logs
prompt enables you to access Pattern Logs, Discovery Logs, or Node Logs. Pattern logs can be retrieved using the ECC Queue output ID or the Managed IP address and pattern
 name. Discovery logs can be accessed by log status or ECC Queue input, and node logs by transaction ID or ECC Queue input.
