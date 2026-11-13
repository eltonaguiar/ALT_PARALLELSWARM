# Deploy a MID Server

- Source: https://www.servicenow.com/docs/r/zurich/it-operations-management/discovery/deploy-mid-server.html
- Release: Zurich

---

# Deploy a MID Server

Deploying a
MID Server
lets
ServiceNow
securely communicate with systems inside a private network by installing and validating a trusted runtime that performs discovery, integrations, and automation tasks without requiring inbound
 network access.

## Before you begin

Verify the following:
- The ServiceNow AI Platform is running on the Brazil, Australia, or Zurich release starting with Patch 8.
- You have installed the ITOM Visibility plugin. For more information, see Install ITOM Visibility using ServiceNow Otto for Setup .
- You have installed the ServiceNow Otto for IT Operations Management (ITOM) plugin. For more information, see Install ServiceNow Otto for IT Operations Management (ITOM) .
- You're on the Configure IT Operations Management page of the Configuration Console. For more information, see Access the ITOM Configuration Console .
Role required: admin

## About this task

Discovery
requires a
MID Server
to securely detect and collect data from your private network, identifying infrastructure and dependencies without exposing internal resources to the internet.

## Procedure

- Navigate to Configuration Summary > Discovery > Platform foundations .
- Select Deploy MID server .
- Select the Application manager icon ( ). The ITOM Infra Services Workspace displays.
- Download the MID Server for the appropriate operating system. For more information, see Install a MID Server on Linux and Install a MID Server on Windows .
- Select X to close the window and return to the Configuration Console.
- To complete the setup, select Mark as configured .
