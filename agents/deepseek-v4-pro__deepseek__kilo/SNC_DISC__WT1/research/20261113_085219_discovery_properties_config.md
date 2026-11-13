# discovery_properties_config

query: ServiceNow Discovery properties configuration options MID server schedules credential

## Evidence (1 sources)

SOURCE: https://www.servicenow.com/community/itom-forum/discovering-servers-in-different-domain/m-p/950161
TITLE: ServiceNow
  - Then, for the Discovery schedules, make sure to use different schedules for different domains. For example - for a domain called "yourcompany-test", create a schedule and include all of the IP addresses / ranges for that domain in it (144.144.144.155/28, or individual IPs). For that schedule, make sure to specify the MID Server (or MID Server in the Behavior that's specified for the schedule) that has the proper credentials for that domain (if you set up the Windows service for MID Server #1 to 
  - The MID server should be able to go across domains as long as you log onto the Windows server where the MID server Windows Service is, then go to the properties for that Windows Service, go to the Log On tab, and set the credentials to use a Windows account for that domain (provide domain\user and the password). So, you might need at least 1 MID server per domain, so that you can use one domain's credentials for one MID server and another domain's credentials for another MID server (they can bot
  - Discovering servers in different domain - ServiceNow Community
  - DigiCert CA Trust Discovery returns "Certificate List is Empty" on Linux MID Server
  - Simply enable powershell and the related paramters on the MID servers. That will let the MID server scan using different credentials from different domains.

## All search hits

- [ServiceNow](https://www.servicenow.com/community/itom-forum/discovering-servers-in-different-domain/m-p/950161) score=4
- [ServiceNow](https://www.servicenow.com/docs/r/it-operations-management/discovery/r_DiscoveryProperties.html) score=3
- [ServiceNow](https://www.servicenow.com/docs/r/yokohama/it-operations-management/discovery/c-MIDServerSelectionSequence.html) score=3
- [ServiceNow](https://www.servicenow.com/docs/r/servicenow-platform/mid-server/r_MIDServerProperties.html) score=3
- [ServiceNow](https://www.servicenow.com/docs/r/platform-security/connections-and-credentials/credentials-getting-started.html) score=3
- [ServiceNow](https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/cmdb-coverage-create-disc-sched.html) score=3
- [ServiceNow](https://www.servicenow.com/docs/r/zurich/it-operations-management/discovery/c_DiscoveryConfiguration.html) score=3
- [ServiceNow](https://www.servicenow.com/docs/r/it-operations-management/discovery/discovery-admin-workspace-schedules.html) score=3