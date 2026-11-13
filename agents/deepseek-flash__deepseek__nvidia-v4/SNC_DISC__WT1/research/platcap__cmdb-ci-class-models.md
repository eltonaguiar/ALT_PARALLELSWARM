# CMDB CI class models

- Source: https://www.servicenow.com/docs/r/zurich/servicenow-platform/cmdb-ci-class-models/cmdb-ci-class-models.html
- Release: Zurich
- Map: platcap

---

# CMDB CI Class Models

Summarize Summarized using AI This content was generated using new OpenAI-powered functionality. Results are provided on an as is basis and are not guaranteed to be accurate or complete. Summary of CMDB CI Class Models The CMDB CI Class Models ServiceNowÂ® Store app enhances the Configuration Management Database (CMDB) by adding extended class models to the existing CMDB class hierarchy. These extensions include detailed class descriptions, identification rules, identifier entries, and dependent relationships where applicable. The added classes function like native CMDB classes and enable applications such as Discovery and Service Mapping to better populate and discover configuration items (CIs) related to various technologies and software. Show full answer Show less Key Features Extended CMDB Classes: Adds new classes, columns, and metadata stored in tables including CMDB Class Information, Identifier, Identifier Entry, and CMDB Metadata Hosting Rules. Discovery Support: Supports discovery of specific technologies and software by leveraging extension classes, improving accuracy and completeness of CI data. Technology Coverage: Provides extension classes for technologies such as Avi load balancers, Oracle RDS, Firewalls, IBM Hardware Management Console, IoT, Nutanix, OpenStack, Red Hat Virtualization, Transport Layer Security, VMware NSX, and more. Integration with Discovery Patterns: Works alongside related Discovery patterns and Service Graph Connectors to streamline data import and integration from third-party sources. Practical Use and Verification After installing the CMDB CI Class Models app, verify successful installation by navigating to All > Configuration > CI Class Manager in ServiceNow. Use the Hierarchy view to see the list of added classes and review their details, identification rules, and dependent relationships. This ensures that the extended classes are properly integrated into the CMDB structure. Important Considerations Uninstalling this app may compromise CMDB integrity and lead to unexpected behavior, so it should be done with caution.
The
CMDB
contains
base-system
classes that store data about configuration items (CIs). The
CMDB CI Class Models
ServiceNowÂ® Store
app adds class models that extend the
CMDB
class hierarchy, including class descriptions, identification rules, identifier entries, and dependent relationships if applicable.

You can use the added classes like any other class. Applications such as
Discovery
and
Service Mapping
can use class extensions to populate CIs and to discover technologies and software.

See the CMDB CI Class Models release notes.

Related
ServiceNowÂ® Store
apps and reference information:
- Configuration Management database : A collection of class diagrams and class attributes for key CMDB classes.
- CMDB tables descriptions : Descriptions of key CMDB tables in the base system .
- Populating the CMDB : Information about the various options for populating the CMDB .
- Discovery patterns : A ServiceNow Store app that
 provides a library of Discovery patterns for discovering specific devices and
 applications in the industry.
- Service Graph Connectors : ServiceNow Store apps that provide predefined integrations for importing and integrating common third-party data into CMDB classes. Also includes the IntegrationHub ETL wizard for creating new ETL transform maps.

## Add class models

The app adds classes, columns, and associated metadata as related records in the following tables:
- CMDB Class Information [cmdb_class_info]: Class descriptions
- Identifier [cmdb_identifier]: Identification rules
- Identifier Entry [cmdb_identifier_entry]: Identification entries
- CMDB Metadata Hosting Rules [cmdb_metadata_hosting]: Dependent relationships

## Discover using extension classes

The following table lists the software and technologies that applications can discover using the extension classes. It provides links to documentation for
CMDB CI Class Models
and the corresponding discovery patterns.
Software/Technology CMDB CI Class Models Store app Discovery patterns
Avi load balancer Avi load balancer extension classes Avi Vantage load balancer discovery BYOL Model of RDS for Oracle BYOL model of RDS for Oracle extension classes Firewall Firewall extension classes IBM Hardware Management Console (HMC) IBM Hardware Management Console (HMC) extension classes IBM Virtualization and Hardware Management Console discovery Internet of Things (IoT) Internet of Things (IoT) extension classes N/A Nutanix Nutanix extension classes Nutanix Acropolis discovery OpenStack OpenStack extension classes OpenStack resource discovery Red Hat Virtualization (RHV) Red Hat Virtualization (RHV) extension classes Red Hat Virtualization discovery Transport Layer Security (TLS) Transport Layer Security (TLS) extension classes Discovery procedures provided by Certificate Inventory and Management ServiceNow Store app VMware NSX load balancer VMware NSX load balancer extension classes VMware NSX Advanced load balancer discovery

## Request apps on the Store

Visit the ServiceNow Store website to view all the available apps and for information about submitting requests to the store. For cumulative release notes information for all released apps, see the ServiceNow Store version history release notes .

## Verify successful installation

After installing the
CMDB CI Class Models
store app, make sure the classes were added successfully:
- Navigate to All > Configuration > CI Class Manager .
- Select Hierarchy to display the CI Classes list. This list contains the added classes, such as the Nutanix classes.
- Select a class to see the corresponding class details, identification rules, identifier entries, and dependent relationships, if applicable.
Warning:
Uninstalling the
CMDB CI Class Models
application might compromise the integrity of the
CMDB
and result in unexpected behavior.
