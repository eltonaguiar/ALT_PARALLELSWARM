# Credentials required for host discovery

- Source: https://www.servicenow.com/docs/r/zurich/it-operations-management/service-mapping/r_Credentials4HostDiscovery.html
- Release: Zurich
- Map: itom

---

# Credentials required for host discovery

There are credentials and permissions that
Service Mapping
requires for discovering hosts.

Prior to discovering applications,
Service Mapping
accesses hosts that applications run on and discovers them. Make sure that you provide all necessary credentials to allow host discovery.

The
ServiceNow AI Platform
provides a centralized way of configuring credentials for
Discovery
,
Service Mapping
, and other applications. It allows you to configure credentials for hosts and applications only once.
If you have already configured host-related credentials for another application, you do not need to do it again for Service Mapping .

## Credentials required for discovery of hosts running on UNIX or Linux

Discovery ,
 Orchestration, and Integration Hub explore UNIX and Linux devices by using SSH credentials to execute
 commands over Secure Shell (SSH).

To provide sufficient permissions, configure one of the following
UNIX
and
Linux
credentials:
- Non-root user and password and using the âsudoâ utility to run selected commands as root
- Root user and password
For information on commands requiring sudo-level rights, see
Service Mapping commands requiring a privileged user
and
Commands that require root privileges for Discovery and Orchestration
.

To access Unix-based hosts with non-root credentials, provide the read access to the following files and directories:
- /etc/*release
- /etc/bashrc
- /etc/profile
- /proc/cpuinfo
- /proc/vmware/sched/ncpus
- /var/log/dmesg
- APD directory

## Credentials required for discovery of hosts running on Windows servers

To provide sufficient permissions, configure one of the following
Windows
credentials:

- A domain user with local administrator access on the target Windows hosts.
- A domain administrator. Note: You may need domain administrator credentials only in some cases. For example, when discovering domain controllers.
Configure MID Server to use
Windows credentials
.

(Optional) For discovering using the WinRM protocol, see
Configure WinRM trusted hosts on MID Server
.

## Resolving credential-related issues

If there are discovery issues caused by incorrectly configured or missing credentials, resolve them as explained in the KB article:
Credentials & Permissions troubleshooting on Discovery, Service Mapping, Orchestration
