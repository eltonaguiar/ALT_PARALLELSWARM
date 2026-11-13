# Discovery Configuration Console

- Source: https://www.servicenow.com/docs/r/zurich/it-operations-management/discovery/c_DiscoveryConfigurationConsole.html
- Release: Zurich
- Map: itom

---

# Discovery Configuration
  Console

Use the
Discovery
Configuration Console to manage what kind of configuration items (CIs) and CI information you want to discover.

By default,
Discovery
finds all the information on your network that is specified in probes and patterns. Use the controls in this console to select the data
Discovery
adds to the
Configuration Management Database (CMDB)
that your organization needs. You can control these aspects of
Discovery
:
- The discovery of entire CI types, such as Windows servers.
- The discovery of specific CI details, such as OS information on Windows servers.
- The discovery of ARP data for Networks, UNIX , and Windows devices.
- The discovery of software packages containing keyword terms that you add, such as Hotfix or Security Update.
- File-based Discovery of software on UNIX and Windows by particular extension or folder, such as .cert or .ext.
Note:
Discovery
returns all data from the target to the instance before applying console settings. The instance ignores any excluded data when it updates the
CMDB
.

## Requirements and accessibility

If you use Internet Explorer, you must use version 8 or
 later. The configuration console supports keyboard navigation
and screen readers.

## Console overview

To open the configuration console, navigate to
Discovery Definition > Configuration Console
.

The console is divided into these sections. Use the toggle buttons to enable various options.
- Devices : network devices such as printers, storage devices such as storage switches, and Unix and Windows computers
- Applications : automation applications such as Puppet, databases such as MSSQL, and web servers such as Tomcat
- Software Filter : UNIX and Windows applications that include or exclude keywords that you enter
- File-based Discovery : software files by path, folder, and extensions to scan or ignore

## Device Discovery

Disabling the discovery of device data at the top level disables the related port probes and pattern libraries.
For example, blocking Network Devices disables the SNMP port probe.
Blocking devices at the second level of the hierarchy has the following effects:
- Device class categories disable classifiers.
- Device info categories disable probes and pattern libraries.
You can enable or disable discover ARP data. This option is turned off by default. After upgrading, ARP data is not be discovered unless you enable it in the
Discovery
Configuration Console. ARP data can be controlled in three device classes: Network,
UNIX
, and
Windows
.

Potential impacts include the following:
- Without ARP data, the network path might not be explored if you're using Service Mapping with L2 or L3 Discovery .
- After upgrading and rerunning Discovery , ARP data does not populate for existing customers. Old data is auto-flushed per the deletion strategy of the out-of-the box (OOB) behavior. This is a one-time activity unless you change the OOB
 configuration. Therefore, you must run your Discovery schedule based on the device volume.
- If you have turned off the Network Device Exploration for network devices, you should also keep ARP turned off to retain the old behavior before upgrading.

## Application Discovery

Disabling the discovery of application data affects all host devices on which the application runs.
For example, if you configure
Discovery
to ignore databases, no information is gathered for either
Linux
or
Windows
databases. Conversely, if you configure the system to ignore a device type, such as a
Windows
server, no databases running on that server are explored, even if they are configured to be discovered. The instance cannot identify applications on a server until it discovers that server first.

When you exclude an item from the Applications section, the system disables the relevant process
 classifier.
The probes that belong to this classifier, including the
Horizontal Pattern
 probe
that launches patterns, never launch.

## Software Discovery

You can filter the discovery of software packages based on the keywords they contain for Windows and UNIX computers.
A keyword can be any term that is present in a software package name. Keywords for filtering software are stored in the Software Filter Keys [discovery_spkg_keys] table. The system does
 not provide default filtering keywords for
UNIX
software.
Important:
Keyword software filtering occurs after the probe returns its payload to the instance and not on the target host.
The following default keywords are provided for
Windows
and are filtered out by default:
- Hotfix
- Language Pack
- Security Update

## File-based Discovery

You can configure
Discovery
to either scan or ignore paths, folders, and extensions for File-based
Discovery
.
Discovery
then scans a
Windows
or
UNIX
file system with these settings to identify file fingerprints. Installed software products detected with these attributes are matched to products in a comprehensive software normalization library.

## Effects on Discovery tables

This table shows you what is inactive in
Discovery
tables when you use the
Discovery
Configuration Console.

When you disable Field inactive
Top-level device categories, such as: Network Devices Windows Servers & Computers Unix Servers & Computers The CIs field is inactive on the Port probes [discovery_port_probe] table. The Port probes [discovery_port_probe] table is referred to from the Protocol Category
 [discovery_category_protocol] table. Device classes, such as: Windows 2008 Servers Linux Servers The Active field is inactive on the Classifiers [discovery_classy] table for the related classifier. The Classifiers [discovery_classy] table is referred to from the Device Classification
 Category [discovery_category_device_class] table. Device info, such as: Network Device Exploration Windows Storage ARP Data The Active field is inactive on the Classifier Probes [discovery_classifier_probe] table for the related probe. It is also inactive on the Discovery Patterns [sa_pattern] table for the related pattern that performs CI identification and exploration. These tables are referred to from the Device Info Category
 [discovery_category_device_info] table. Applications The Active field is inactive on the Process Classifiers [discovery_classy_proc] table for the related process classifier. The Process Classifiers [discovery_classy_proc] table is referred to from the
 Application Category [discovery_category_appl] table.
Note:
If you use patterns for discovery, and you disable the discovery of device classes or device information, the system disables the pattern libraries that collect the device information.
For
 example, if you have a
Windows
pattern in which you create a shared library that collects OS information, and then you turn off the collection of OS data, the shared library that collects OS data is inactive. For more information
 about the shared library operation, see
KB1698521: Create or customize patterns
.

## Exclude CIs from discovery

Use the Discovery Configuration Console to determine which devices and applications
 to exclude from discovery.

### Before you begin

Role required: discovery_admin or admin

### Procedure

- Navigate to All > Discovery > Discovery Definition > Configuration Console .
- If you want to exclude specific devices and device information, expand the
 category for the device types.
- To see what applications can be disabled, hover your cursor over the
 application type.
- Click the toggle button to turn off the CIs you do not want to discover. The instance creates an update set record for any change you make to the
 console.

## Customize Applications and Devices to Discover

You can toggle on and off Applications and Devices using the Discovery Configuration
 Console. Some are listed out-of-the-box, but you may also customize which specific
 Applications and Devices you want to Discover according to your specific
 requirements.

### Before you begin

Role required: admin

### Procedure

- Customize Applications. Navigate to Discovery Definition > Application Categories . Click Automation , Databases , or Web &
 Application Servers . Unlock the Process classifier list. To delete from the list, select and application then click the X to remove. To add to the list, type in the box and click Enter . Click the lock icon. Click Update . The next time Discovery runs, it will process those types of specific
 applications that you configured.
- Customize Devices. Navigate to Discovery Definition > Device Info Categories . To create a new record, click New . Enter the details and click Submit . To update an existing device, click on a device listed. Make any changes and click Update or Delete .

## Filter software to discover

Use the Discovery configuration console to filter the software you add to the
 CMDB.

### Before you begin

Role required: discovery_admin or admin

### About this task

The instance creates an update set record for any change you make to the console.

### Procedure

- Navigate to All > Discovery > Discovery Definition > Configuration Console .
- In the Software Filter panel, select the tab for the operating system you want,
 either Unix or Windows .
- Add or delete keywords for filtering software packages. To add a keyword, enter it in the field provided and click New Key . To delete a keyword, click the red x icon to the
 right of the keyword. Discovery looks for software packages containing these terms in the selected operating system and either includes or excludes them from the CMDB. The system does not provide default keywords for filtering UNIX software
 packages, but provides these default keywords for Windows: Hotfix Language Pack Security Update These default keywords exclude patch-related software by default. To enable Security OS Patch Discovery, remove Hotfix and Security Update from the exclusion list. This allows
 Discovery to include patch and hotfix data in the CMDB.
- Select whether to Include or Exclude software packages with the keywords in their
 names. Include : Only add software packages that match
 the keywords. Exclude : Add all software packages except those
 matching the keywords.
- Disable software filtering for either UNIX or Windows . When the filter is disabled for an operating system, all discovered software
 packages for that operating system are added to the CMDB, with no filtering
 applied. The instance creates an update set record for any change you make to the
 console.

## Configure File-based Discovery

Use the
Discovery
Configuration Console to configure several settings to find and manage all of your installed software.

### Before you begin

Role required: discovery_admin or admin

### Procedure

- Navigate to All > Discovery > Discovery Definition > Configuration Console .
- Select the toggle to enable File-based Discovery . This feature is turned off by default.
- Select customizable options specifically for Windows and UNIX machines as well as options common to both types. Some options have default values and others, such as folders to ignore or extensions, are empty until you add in values.
- For Windows and UNIX , select the arrow to expand the target path options.
- Configure basic selections. Folders to Scan Indicates which folders to scan for Windows and UNIX . Default values are listed. You can also add additional paths to scan. Note: If you want File-based Discovery to scan the entire Windows C: drive (not just the default folders), update the windows Folders to Scan target path to C:/ in the Discovery Configuration Console. Folders to Ignore Indicates which folders and child folders/files to ignore from within the list of Windows or UNIX folders that you want to scan. For example, if you have specified âC:\Program Filesâ as a folder to scan, you could additionally specify âC:\Program Files\Tempâ as an ignore folder. When
 File-based Discovery scans a Windows server, it scans all files and sub folders under C:\Program Files, excluding C:\Program Files\Temp. Extensions Exclusion List Indicate extensions (.txt, .war, .exe, and so on) that you want to ignore for Windows . Extensions Wildcards Indicate extensions (.cert, .crt, and so on) that you always want to scan for Windows . This enables you to scan for extensions such as *.cert where the file name itself might not be known ahead of time. You should be able to find certificates (.cert or .crt) and java keystore
 files (.jks) in this way.
- Configure Advanced Windows settings. Sleep Time Sets the length of time in milliseconds to sleep during each throttling interval while scanning for Windows files. The default value is 10000. Donât change this value unless youâre an advanced user. If youâre an advanced user and must make a change, make sure to set to a non-zero value. File Throttle Sets the number of files to scan on Windows before sleeping. The default value is 500. Donât change this value unless youâre an advanced user. If youâre an advanced user and must make a change, make sure to set to a non-zero
 value. Skip Hidden Folders Skips hidden folders on target computers when scanning for file signatures. For Windows devices, the visibility of a folder is based on a hidden attribute that can be set for each folder. Scan Running Process Paths Enables the use of running process paths in the list of targeted paths to scan. This automatically adds paths that contain running processes and therefore most likely contain files of interest for use in
 determining software installations. Scan SWID Tags Scans for and analyzes the software identification (SWID) tags. This option is only visible if SAMP is enabled. When enabled, this returns the software product, publisher, and version in the payload. The data is directly inserted into the software installs table, bypassing the software match API. This feature is turned off by default.
- Configure Advanced UNIX settings. Skip Hidden Folders Skips hidden folders when scanning for file signatures. For UNIX-based devices, these folders are prefixed by a â.â in their name. Scan Running Process Paths Enables the use of running process paths in the list of targeted paths to scan. This automatically adds paths that contain running processes and therefore most likely contain files of interest for use in
 determining software installations. Scan SWID Tags Scans for and analyzes the software identification (SWID) tags. This option is only visible if SAMP is enabled. When Scan SWID Tags is enabled, this returns the software product, publisher, and version in the
 payload to be directly inserted into software installs table. This bypasses the software match API. This feature is turned off by default.
- Configure Common settings for either Windows or UNIX . Maximum Files Sets the maximum number of files that you want to discover. This is the number of files scanned per CI/IP. Frequency Sets the frequency that File-based Discovery runs on the CI.

### Result

File-based
Discovery
is now enabled,
 configured, and ready for you to run. See
Run File-based Discovery
for more
 information.

## Create Basic Auth credentials

Create credentials to access a
ServiceNowÂ®
instance.

### Before you begin

Role required: system_admin

### Procedure

- Navigate to All > Connections & Credentials > Credentials .
- Select New .
- Select Basic Auth Credential .
- On the form, fill in the fields. Table 1. Basic Auth Credentials form Field Description Name Enter a unique and descriptive name for this credential. User name Name to identify the user. Password Password to use this credential. Active Option to enable the use of this credential. Order The order (sequence) in which the platform tries this credential while it attempts to log in to devices. The smaller the number, the higher in the list this credential appears. Establish credential order
 when using large numbers of credentials or when security locks out users after three failed login attempts. If all the credentials have the same order number (or none), the instance tries the credentials in a
 random order. Default value: 100
- Select Submit .

### Result

The Basic Auth credentials for use with the server instance are created.
