# Create a Discovery CI classification

- Source: https://www.servicenow.com/docs/r/zurich/it-operations-management/discovery/create-discovery-ci-classification.html
- Release: Zurich
- Map: itom

---

# Create a Discovery CI classification

A CI classification allows Discovery to discover most common operating systems,
 network devices, and processes.

## Before you begin

Role required: admin

## About this task

Warning:
Adding SNMP OID classifications with a Net-SNMP module OID starting
 with 1.3.6.1.4.1.8072.3.2 or a Windows OS OID starting with 1.3.6.1.4.1.311.1.1.3
 can result in misclassification of devices and incorrect model names and is no
 longer allowed. These are template system OIDs that can remain on a device if the
 manufacturer fails to replace them with OIDs specific to their own model. For
 example, a Check Point Smart-1 3050 Firewall, which uses Linux as its OS, might have
 the OID for a Linux server, 1.3.6.1.4.1.8072.3.2.10. This results in the firewall
 being classified incorrectly. If two or more devices have the same OID, configure
 classification criteria that differentiate the devices from one another. For
 details, see
KB0751287
.

## Procedure

- Navigate to All > Discovery Definition > CI Classification .
- Select the type of classification to create.
- Click New in the list of classifications for the type
 you selected.
- Complete the form using the fields in the table. Table 1. Classification form fields Field Input Value Name Name of the configuration item (CI). OID SNMP system OID for matching this device. When the OID value matches
 that of an SNMP device, Discovery uses the
 information to populate the CMDB with the
 specified manufacturer, model, and
 classifier. Operator Operator for determining how to match and SNMP OID.
 The choices are Is and Starts with . This field is
 available only for SNMP System OIDs classifiers. Active Enables or disables this classifier. When a
 classifier is disabled, the system stops classification
 at this level and does not launch classifiers of a lower
 order. For example, when the classifier for Windows 2008
 Server is disabled, the system stops Discovery at this
 point and does not launch the Windows 2012 Server
 classifier. Order Order (sequence) in which the platform runs this
 classifier. Table Table for this classification. For example, if this
 record classifies a Linux server,
 select the Linux Server [cmdb_ci_linux_server]
 table. Classifier Classification of an SNMP device, such as A10 Load Balancer . This field
 is available only for SNMP System OIDs
 classifiers. Relationship type Type of relationship for this classifier, such as Runs on::Runs . This field is
 available only for application and process
 classifiers. Match criteria Criteria that must match to classify this device. The
 choices are Any of the parameters
 or All of the parameters. Manufacturer Name of the manufacturer of a network device. This
 field is available only for SNMP and SNMP System OIDs
 classifiers. Model Model number of a network device. This field is
 available only for SNMP and SNMP System OIDs
 classifiers. On classification script Script that runs if classification criteria are met.
 Use this script to perform any special tasks after a
 device is classified. It is possible to use the g_probe_parameters hashmap from
 within a classification script to set probe parameters
 for any configured, triggered probes. For example, this
 code sets a ' node_port ' parameter
 to 16001 for all triggered
 probes: (JS), g_probe_parameters['node_port'] = 16001; // Related lists Classification Criteria Criteria formed from specific parameters and the
 values that they must contain to match devices that Discovery finds in the network with
 CIs in the CMDB. For a detailed discussion of these
 parameters, see Discovery classification parameters . SNMP OID Classifications Unique
 "fingerprints" of all the SNMP devices that ship
 with the base Discovery product.
 Users can add OIDs for SNMP devices not in this
 list. This related list is available only for SNMP
 devices. Triggers probes Exploration probes that Discovery launches to gather detailed information about a CI
 that it has classified in the network. If you want
 to use patterns for horizontal discovery, add the Horizontal Pattern probe in the Probe column, and then
 specify your pattern in the Pattern column. Warning: Do not specify your pattern in Probe column. Choose the
 Horizontal Pattern probe, which launches the
 specified pattern. Versions Lists versions of this classifier. A new version is
 created whenever you modify the classifier record. To
 revert to a previous version, open that record and
 select Revert to this version under Related Links . This example shows a completed CI classification form with the Horizontal Pattern probe defined. For instruction on creating probes, see Discovery probes and sensors . Probes that are defined are launched when the device is properly classified, unless Discovery is configured to stop after classification. Figure 1. Discovery classification form
