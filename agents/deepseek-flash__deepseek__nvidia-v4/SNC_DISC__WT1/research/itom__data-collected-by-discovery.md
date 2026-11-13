# Data collected by Discovery

- Source: https://www.servicenow.com/docs/r/zurich/it-operations-management/itom-visibility/r_DataCollDiscoStorageDevices.html
- Release: Zurich
- Map: itom

---

# Data collected by Discovery on storage devices

Summarize Summarized using AI This content was generated using new OpenAI-powered functionality. Results are provided on an as is basis and are not guaranteed to be accurate or complete. Summary of Data collected by Discovery on storage devices ServiceNow Discovery gathers detailed information about various storage devices in your IT environment, enabling effective configuration management and relationship mapping within the CMDB. This data collection supports storage components including disks, file shares, pools, ports, HBAs, servers, and volumes. Show full answer Show less Key Features Storage Disk Discovery: Identifies disks with attributes such as name, host reference, interface type, size, free space, manufacturer, and model ID. Storage File Shares: Captures file share names and their network paths. Storage Pools: Collects information about storage pools including name, size, free space, and hosting CMDB reference. Storage Ports: Discovers ports with details like name, unique WWPN, and speed. Storage Host Bus Adapters (HBAs): Records HBA names, model IDs, and associated computers. Storage Servers: Gathers server details such as name, manufacturer, model, operating system, OS version, and description. Storage Volumes: Captures volume name, unique ID, state, size, and storage type. Relationship Mapping: Automatically creates relationships between storage components, critical for understanding dependencies and configurations. Key Outcomes SAN (Storage Area Network) Relationships: Discovers and maps relationships between storage volumes and Fibre Channel or iSCSI disks, showing export/import dependencies crucial for SAN infrastructure management. NAS (Network Attached Storage) Relationships: Resolves NAS file shares by mapping hostnames or IP addresses to storage servers, establishing allocation relationships between NAS file systems and storage file shares for both Linux and Windows hosts. Enhanced CMDB Accuracy: Provides comprehensive, structured data on storage components and their interconnections, enabling better asset management, impact analysis, and operational insights.
Discovery
identifies and
 classifies information about storage devices.

Table 1. Resources discovered on the Storage Disks [cmdb_ci_storage_disk] table
Field Description
Name Name of the storage disk. Computer Reference to the host CI. Interface Interface type with which the storage disk is connected to the host. Size Size of the storage disk. Free disk space (GB) Free space in GV available on the disk. Manufacturer Manufacturer of the storage disk. Model ID Model name of the disk.
Table 2. Resources discovered on the Storage File Shares [cmdb_ci_storage_fileshare] table
Field Description
Name Name of the CI. Path Path to the file share.
Table 3. Resources discovered on the Storage Pools [cmdb_ci_storage_pool] table
Field Description
Name Name of the storage pool. Size Size of the storage pool. Free space Free space available in the pool. Hosted by Reference to the CMDB CI.
Table 4. Resources discovered on the Storage Ports [cmdb_ci_storage_port] table
Field Description
Name Name of the storage port. WWPN Unique Worldwide Port Name (WWPN) for the storage port. Speed Speed of the storage port.
Table 5. Resources discovered on the Storage HBAs [cmdb_ci_storage_hba] table
Field Description
Name Name of the Storage Host Bus Adapter (HBA). Model ID Model name of the HBA. Computer Reference to the computer CI.
Table 6. Resources discovered on the Storage Servers [cmdb_ci_storage_server] table
Field Description
Name Name of the CI. Manufacturer Manufacturer of the storage server. Model ID Model name of the storage server. Operating System Operating system (OS) of the storage server. OS Version OS version of the storage server. Description Short description of the storage server.
Table 7. Resources discovered on the Storage Volumes [cmdb_ci_storage_volume] table
Field Description
Name Name of the storage volume. Object ID Unique ID for the storage volume. State State of the storage volume. Size Size of the storage volume. Storage Type Type of storage volume.

## Storage relationships

Discovery creates relationships for storage CIs running on Storage Area Networks (SAN)
 and Network Attached Storage (NAS).

## SAN relationships

Discovery creates the following relationships for storage CIs running on Storage Area
 Networks.

Table 8. SAN CI relationships
Parent Component Relationship Child Component
Storage Volume [cmdb_ci_storage_volume] Exports to::Imports from Fibre Channel Disk [cmdb_ci_fc_disk] Storage Volume [cmdb_ci_storage_volume] Exports to::Imports from iSCSI [cmdb_ci_iscsi_disk]

## NAS relationships

Discovery maps NAS file shares by resolving the hostname of a remotely mounted disk
 on the client computer to an IP address. It then matches the IP address to the storage
 server that provides the exported file system.

Discovery extracts the hostname or IP address from the NAS path to identify the
 storage server. If the NAS path contains a hostname, Discovery resolves it to an IP address
 and stores the value in the
nas_ip_address
field of the NAS File
 System [cmdb_ci_nas_file_system] table.

Discovery creates the following relationships for storage CIs running on Network
 Attached Storage (NAS). These relationships are the same for Linux and Windows hosts.

Table 9. NAS CI relationships
Parent Component Relationship Child Component
NAS File System [cmdb_ci_nas_file_system] Allocated from::Allocated to Storage File Share [cmdb_ci_storage_fileshare]
