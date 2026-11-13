# Create IP credentials

- Source: https://www.servicenow.com/docs/r/zurich/it-operations-management/discovery/create-ip-credentials.html
- Release: Zurich

---

# Create IP credentials

Create IP credentials for
Discovery
to securely connect to devices in your environment.
Discovery
uses these credentials to log in to devices and retrieve configuration data during the discovery process.

## Before you begin

Verify the following:
- You're using the Zurich Patch 8 or later version of the ServiceNow AI Platform .
- You have installed the ITOM Visibility plugin. For more information, see Install ITOM Visibility using ServiceNow Otto for Setup .
- You have installed the ServiceNow Otto for IT Operations Management (ITOM) plugin. For more information, see Install ServiceNow Otto for IT Operations Management (ITOM) .
- You're on the Configure IT Operations Management page of the Configuration Console. For more information, see Access the ITOM Configuration Console .
Role required: discovery_admin

## About this task

IP credentials store the authentication information that
Discovery
needs to access devices in your network. When
Discovery
runs, it tries each credential in the order you specify until it finds one that works for a given device. Set the credential order to control which credentials
Discovery
tries first. This is especially important when security policies lock out users after failed login attempts.

For more information about credential types and requirements, see
Create and test your credentials
.

## Procedure

- Navigate to Configuration Summary > Discovery > Discovery Setup .
- Select IP credentials .
- From the Credential type drop-down list, select a credential type. The following credential types are available for IP credentials. Credential type Description Applicative Credentials Credentials for discovering applications running on host machines. Basic Auth Credentials Credentials that use basic authentication with a user name and password. CIM Credentials Credentials for devices that use the Common Information Model protocol. Kubernetes Credentials Credentials for discovering Kubernetes clusters and resources. oVirt Credentials Credentials for oVirt virtualization environments. Secondary Bot Hash Token Credential Token credentials for secondary bot integrations that use existing tokens. Secondary Bot Static Token Credential Static token credentials for secondary bot integrations. SNMP Community Credentials (Password Only) Credentials that use an SNMP community string for network devices. SNMPv3 Credentials Credentials that use the SNMPv3 protocol with authentication and privacy options. SSH Credentials Credentials for Linux, UNIX, and other SSH-enabled devices. SSH Private Key Credentials Credentials that use an SSH private key for authentication instead of a password. SSL Keystore Credentials Credentials that use an SSL keystore for secure communication. VMWare Credentials Credentials for VMware vCenter environments. Windows Credentials Credentials for Windows devices that use WMI or WinRM protocols.
- Select Create new .
- Complete the form. The fields in the form vary based on the credential type that you selected. The following fields appear in most credential types. Field Description Name Enter a unique and descriptive name for the credential. User name Enter the user name for this credential. Avoid leading or trailing spaces in user names. Active Select this check box to make the credential available for Discovery . Credential alias Select a credential alias to associate with this credential. Credential aliases enable you to define a credential once and reference it across multiple configurations. Order Enter the sequence in which Discovery tries this credential when it attempts to log in to devices. The smaller the number, the higher the priority. If all credentials have the same order number, Discovery tries them in a random order. Note: Establish credential order when you use large numbers of credentials or when security policies lock out users after failed login
                                            attempts.
- Select Submit . You're returned to the IP credentials page.
- To complete the setup, select Mark as configured .
