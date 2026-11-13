# Create a MID Server user

- Source: https://www.servicenow.com/docs/r/zurich/it-operations-management/discovery/create-mid-server-user.html
- Release: Zurich

---

# Create a MID Server user

Create a user account with the mid_server role so
MID Servers
can authenticate and communicate with the
ServiceNow
instance.

## Before you begin

Verify the following:
- You're using the Zurich Patch 8 or later version of the ServiceNow AI Platform .
- You have installed the ITOM Visibility plugin. For more information, see Install ITOM Visibility using ServiceNow Otto for Setup .
- You have installed the ServiceNow Otto for IT Operations Management (ITOM) plugin. For more information, see Install ServiceNow Otto for IT Operations Management (ITOM) .
- You're on the Configure IT Operations Management page of the Configuration Console. For more information, see Access the ITOM Configuration Console .
Role required: admin

## About this task

MID Servers
require a
MID Server
user account to authenticate with the instance. Assigning the mid_server role allows the
MID Server
to connect and pass validation checks.
ServiceNow
monitors
MID Server
user settings to help prevent validation failures. You can use a dedicated user per
MID Server
or share a user across multiple
MID Servers
.
Note:
Using the same loggedâin user across multiple
MID Servers
can generate issue records when more than one
MID Server
is
Up
. Configure a unique loggedâin user per
MID Server
. See
(KB1552863) MID Server Unique Logged In User
for more information and remediation steps.

## Procedure

- Navigate to Configuration Summary > Discovery > Platform foundations .
- Expand Platform foundations .
- Select MID server user .
- Select Create user . The Create MID server user page displays.
- Complete the following fields. Field Description User ID Enter a user name for the MID Server user. This name is specified in the mid.instance.username parameter of the configuration file that the MID Server installer creates. For details, see MID Server parameters . Note: Avoid using the same MID Server logged in user across multiple MID Servers . Password Enter a password for the MID Server user. This password is specified in the mid.instance.password parameter of the configuration file that the MID Server installer creates.
- Select Create user . You're returned to the MID server user page. Note: The MID Server user is limited to MID Server setup. To complete Discovery setup through the ITOM Configuration Console, you must have the discovery_admin role.
- To complete the setup, select Mark as configured .
