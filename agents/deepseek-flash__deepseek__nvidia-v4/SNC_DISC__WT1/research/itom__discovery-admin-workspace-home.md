# Discovery Admin Workspace Home

- Source: https://www.servicenow.com/docs/r/zurich/it-operations-management/discovery/discovery-admin-workspace-home.html
- Release: Zurich

---

# Discovery Admin Workspace Home

Summarize Summarized using AI This content was generated using new OpenAI-powered functionality. Results are provided on an as is basis and are not guaranteed to be accurate or complete. Summary of Discovery Admin Workspace Home The Discovery Admin Workspace Home page in ServiceNow provides a centralized interface to monitor and manage critical discovery tasks. Accessible viaWorkspaces > Discovery Admin Workspace, it supports versions starting from v1.17.0 and helps streamline discovery configuration, error management, and operational monitoring within your IT environment. Show full answer Show less Onboarding for Discovery The onboarding experience adapts based on your setup progress. Initially, it guides you to create IP or cloud-based discovery schedules through the ITOM Configuration Console (available in Zurich Patch 8+). After schedules are created, a progress indicator tracks completed configuration tasks. Once fully configured, a persistent link to the ITOM Configuration Console remains for easy access. Quick Overview Section Active Schedules: Shows the count of all active IP and Cloud Discovery schedules run to date. Error Tasks: Displays ongoing discovery error tasks within a selected time frame, linking to detailed case management views. Schedules with Anomalies: Indicates discovery schedules flagged with anomalies if anomaly detection is enabled, with direct access to anomaly details for troubleshooting. You can refresh the data manually and configure the time scale for displayed counts via the Settings page. Discovery Operations Monitor This feature lets you monitor discovery performance metrics such as transaction rates, sensor job statuses, MID Server queue loads, and probe processing times through a dedicated dashboard, helping optimize operational efficiency. Discovery Admin Tasks Focuses on the three most critical discovery error tasks, allowing you to assign, update, or add work notes. For comprehensive management, a full list of error tasks is accessible through the Diagnostics pageâs Case Management tab. Note that only error tasks linked to specific issues are shown here. Discovery Tuning Advice Provides automated recommendations to fine-tune Discovery and MID Server configurations based on scans of your instance. Findings are prioritized by criticality and link to detailed tuning checks, enabling proactive issue resolution. A complete list of tuning reports is available on the Tuning page. Quick Discovery Enables immediate discovery of devices outside scheduled runs by entering individual IP addresses, ranges, or networks. You can select a specific MID Server, a MID Server cluster, or allow automatic MID Server selection, facilitating flexible ad-hoc discovery operations. ITOM Visibility Apps Enhance Discovery Admin Workspace capabilities by integrating additional ITOM Visibility applications. You can view installed apps and explore available ones for installation. Admin role is required for app updates. Note that pricing details are contract-specific and not displayed within the workspace. Learnings Offers guidance through the ITOM Visibility Knowledge Base, including articles, blog posts, and video tutorials to help manage discovery and resolve errors effectively. Access requires ITOM Content Service version 1.2.8 or higher. To resolve potential video playback issues, adjust the system property com.glide.security.referrerpolicy as documented.
The
Discovery Admin Workspace
Home page features tools to help you identify and address the most critical discovery tasks.

To access the
Discovery Admin Workspace
, navigate to
Workspaces > Discovery Admin Workspace
.
Note:
The capabilities described here are available starting with
Discovery Admin Workspace
v1.17.0. Specific version requirements are noted for individual features where applicable.

## Onboarding for Discovery

The onboarding experience on the Home page changes based on your configuration progress. Before you create an IP or cloud-based
Discovery
schedule, the Home page displays an Onboarding for
Discovery
section. Select
Get started
to access the
ITOM
Configuration Console.
Note:
Note: The
ITOM
Configuration Console is available in Zurich Patch 8 or later versions of the
ServiceNow AI Platform
. For more information, see
ITOM Configuration Console for Discovery
.
After you create a schedule, the Onboarding for
Discovery
section is replaced by an Onboard
Discovery
progress indicator. This indicator displays the number of completed configuration tasks. Select
Continue
to resume configuration in the
ITOM
Configuration Console.

After you complete configuration, the Home page displays an Onboarding for
Discovery
link as a persistent entry point to the
ITOM
Configuration Console.

## Quick overview

View the status of discovery using data counts and identify any irregularities that might impact discovery. For detailed information, select the appropriate tile.

Select the
More Options
icon (
), then select
Refresh
to refresh the data for each visualization in this section.

Note:
You can configure the time scale reflected in the displayed counts on the
Settings
page.
The following data counts display in the Quick overview section:

Active schedules
Displays the number of active IP-based and
Cloud Discovery
schedules run to date.
Error tasks
Displays the active, including pending or in-progress,
Discovery
error tasks opened in a certain time period. Selecting this number redirects you to the Case management tab on the
Diagnostics
page, where you can view all
Discovery
error tasks.

Schedules with anomalies
Displays the number of
Discovery
schedules with anomalies detected over a certain time period. This count only displays when anomaly detection is enabled. If anomaly detection is inactive, select
Turn
                            on
to access the
Settings
page.
Selecting this number redirects you to the Anomaly detection tab on the
Diagnostics
page, where you can view details about the type and severity of anomalies.

Discovery
Operations Monitor
Monitor discovery performance across your IT environment. Select
View dashboard
to open the dashboard and view performance metrics for transactions, sensor jobs, MID Server queue load, and
 probe processing times. For more information, see
Discovery Operations Monitor dashboard
.

## Discovery admin tasks

Review the three most critical
Discovery
error tasks. Select
Edit Task
to access the details page where you can assign or update the error task, or add work notes. To view and manage all
Discovery
error tasks, select
View all
to access the Case management tab on the
Diagnostics
page.
Note:
This section focuses solely on
Discovery
errors that have associated tasks and not all
Discovery
errors.

## Discovery tuning advice

Fine-tune
Discovery
and
MID Server
settings with automated suggestions derived from scans of your instance. These findings identify potential issues, arranged in order of their criticality. Selecting a finding redirects you to
 the
Tuning check
page for more details. To view all tuning checks and latest reports, select
View all
to access the
Tuning
page.

## Quick Discovery

Discover devices in your network outside of a scheduled discovery. Enter a single IP address, multiple comma-separated IP addresses, or an IP network as shown in this example:
- IP network address - 10.0.1.0/24
- IP address range - 10.0.2.1-10.0.2.15
- IP address list - 10.0.3.176,10.0.3.222,2001::100,2600:1bdc::fffe
Select a
MID Server
, a MID cluster, or enable
Discovery
to select the
MID Server
automatically.

## ITOM Visibility apps

Enhance the functionality of the
Discovery Admin Workspace
by integrating additional
ITOM Visibility
applications. When you select
View all
, you can view both the applications installed on your instance and others that are available for installation.
Note:
Updating
 applications requires you to have the admin role.
While you can access details about the apps installed on your instance, information regarding pricing and packages isn't provided, as it varies based on each
 contract. For a general overview of licensing and subscription details, see
ITOM/OT SU Licensing and subscriptions
.

## Learnings

Receive guidance on managing the
Discovery
process and resolving
Discovery
errors with the
ITOM Visibility
Knowledge Base
. Access relevant articles from the
ServiceNow
Knowledge Base
, explore blog posts, or watch instructional video tutorials for further information.

Important:
- To view the resources in this section, confirm that you have installed ITOM Content Service version 1.2.8.
- If you encounter an Error 153: Video player configuration error message when attempting to play a video on the Videos tab, update the system property com.glide.security.referrerpolicy to origin-when-cross-origin . For more information, see Enforce secure referrer policy [New in Security Center 1.3] .
