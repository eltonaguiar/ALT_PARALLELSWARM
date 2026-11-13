# Pre-discovery phase

- Source: https://www.servicenow.com/docs/r/zurich/it-operations-management/discovery/cert-inventory-mgmt-process-pre-discovery.html
- Release: Zurich

---

# Pre-discovery phase

Summarize Summarized using AI This content was generated using new OpenAI-powered functionality. Results are provided on an as is basis and are not guaranteed to be accurate or complete. Summary of Pre-discovery phase The pre-discovery phase in ServiceNow's Certificate Inventory and Management sets up essential preparatory steps to ensure a smooth certificate discovery process. This includes defining scanning parameters and configuring credential details before initiating the actual discovery. Show full answer Show less Discovery Methods Discovery via Ports: The tlssslcerts port probe automatically scans 14 default preauthorized ports, including common SSL ports such as 443, 8443, and StartTLS ports like 25 and 587. The MID Server collects detailed certificate chain information from these ports and forwards it as XML to the instance, where key certificate attributes are extracted and recorded in the Discovered Certificate table. Discovery via URL: URLs listed in the Certificate URL table are targeted for certificate discovery. Each URL can optionally link to a Unique Certificate record. The CertificateDiscoveryFromURLScan probe processes these URLs, discovers their certificate chains, outputs XML payloads, and creates records in the Discovered Certificate table. Discovery via Import Certificates: Certificates stored on hosts are discovered using the Import SSL Certificate pattern, requiring parameters such as host name/IP, folder location, and temporary MID Server folder. Customers should note that enabling TLSkeepOriginalCertificate can increase payload size and risk out-of-memory errors. Auto-selecting MID Servers is not supported for Windows/Linux combinations in this mode. Discovery via Certificate Authority (CA): After setting up credentials with supported CAs (GoDaddy, DigiCert, Entrust, Sectigo), the discovery schedule uses REST API calls to retrieve certificates and related data, storing them in the cmdbcicertificate and associated tables. Default API URLs and versions are used if not specified. Customers can configure parameters such as startoffset, limit, CredentialAlias, and include additional certificate states for discovery. Version 1.2.0 and later support scanning Sectigo and Entrust CAs. Key Configuration Parameters and Considerations TLSkeepOriginalCertificate: When set to true, the original certificate file is attached to the Certificate CI, potentially increasing payload size and causing out-of-memory issues. IncludeCertStatus: Allows specifying additional certificate states to discover beyond the default states defined per CA, such as issued, expired, revoked, or canceled. State Field in Certificate CI: Reflects the lifecycle state (e.g., Issued) rather than the raw CA state. Expired certificates should be identified by the Valid to date instead of the State field. MID Server Selection: For import discovery, if the MID Server stores original certificate files, the host name/IP should be blank or localhost, and the specific MID Server must be selected in the discovery schedule. Next Steps Once the pre-discovery phase is configured and complete, proceed to the post-discovery phase to continue the certificate management lifecycle.
The pre-discovery phase involves preparatory steps, such as defining scanning parameters and configuring credential details, for a smooth initiation of the certificate discovery process.

## Discovery via Ports

The port probe (tls_ssl_certs) automatically scans 14 default preauthorized ports.
- Typical ports for SSL: 443, 8443, 9443, 636 (ldaps), 993 (imaps), 995 (popssl), 989, 990
- StartTLS ports: 25 (smtp), 110, 143, 389, 21, 587 (smtp)
As part of the CI
Discovery
process during Shazzam, the
MID Server
uses scanners to gather certificate chain information from the IP port number and capturing diverse attributes, including the certificate hierarchy. The
MID Server
then transforms these certificates into an XML payload, sharing it with the instance. The Shazzam sensor, in turn, detects the ECC queue entry and inserts a new record into the Discovered Certificate
 (sn_disco_certmgmt_certificate_history) table.

The following fields are pulled from the XML payload and verified in java code from the Shazzam TLS port probe for discovered certificates: certificate id, revocation_status, subject, issuer, sans/, is_self_signed, is_ca, valid_from,
 valid_to, signature_algorithm, fingerprint_algorithm, key_size, serial_number, and version.

## Discovery via URL

The Certificate URL (sn_disco_certmgmt_cert_url) table holds a list of URLs to target for certificate discovery. Each record also has an optional reference to the Unique Certificate (cmdb_ci_certificate) table, to see what certificate
 is related to the given URL definition. The necessary parameters from the
Discovery
Schedule are combined to create and initialize the
Discovery
status. The CertificateDiscoveryFromURLScan probe discovers the certificate chain for each of the URLs in the batch and outputs an XML payload that contains the certificate chain for each certificate. It
 also adds a new record into the Discovered Certificate (sn_disco_certmgmt_certificate_history) table.

## Discovery via Import Certificates (Version 1.1.7 Certificate Inventory and Management)

The Import certificates are discovered through the Import SSL Certificate pattern, which relies on the following parameters.
- Host name/IP where the certificates are hosted
- Folder where certificates are located
- TLS_keepOriginalCertificate: Setting this parameter to true may lead to increased payload size, potentially causing out-of-memory issues.
- Mid_temp_folder: The temporary folder on the MID Server where files will be temporarily copied.
Note:
Auto-select
MID Server
option is NOT supported for Windows and Linux mid combinations. If the
MID Server
is used for storing the original certificates files, then Host name/IP should be set to blank or localhost and the particular
MID Server
should be selected for the
Discovery
schedule.

## Discovery via CA authority (Version 1.1.7 Certificate Inventory and Management)

After the
Certificate Inventory and Management
credential is set up with either GoDaddy, DigiCert, Entrust, or Sectigo Certificate Authority and the
Discovery
schedule runs, the specific CA pattern makes REST API calls to (GoDaddy, DigiCert, Entrust, or Sectigo), collects certificate information, retrieves the list of certificates, and stores it in the
 cmdb_ci_certificate, certificate_domain, and sys_attachment tables.

ca_api_url and ca_api_version are optional parameters. If these parameters are left empty inside pattern parameters, default values will be used. The default values include:
- DigiCert - Certificate Management (ca_api_version = v2, ca_api_url = https://www.digicert.com/services/)
- Entrust - Certificate Management (ca_api_version = v2, ca_api_url = https://api.entrust.net/enterprise/)
- GoDaddy - Certificate Management (ca_api_version = v1, ca_api_url = https://api.godaddy.com/)
- Sectigo - Certificate Management (ca_api_version = v1, ca_api_url = https://cert-manager.com/api/ssl/)
The arguments for GoDaddy, DigiCert, Entrust, and Sectigo patterns are as follows. Starting from Version 1.2.0, you have the capability to scan Sectigo and Entrust Certificate Authorities (CAs).
- Start_offset: The offset position for reading certificates from CA authorities, with a default value of 0.
- Limit: The number of certificates to be read from the start_offset, with a default value of 1500.
- CredentialAlias: The name of the Credential Alias or Tag linked to the CA credentials, added in the serverless execution pattern configuration. If the TLS_keepOriginalCertificate parameter is set to true, the certificate
              file is attached to the Certificate CI. This may increase payload size, potentially causing out-of-memory issues.
- IncludeCertStatus: A parameter for specifying additional certificate states to discover, in addition to the defaults. Table 1. Certificate states by certificate authorities Certificate Authority Default States Discovered Sectigo Issued Expired DigiCert and GoDaddy Active Expired Revoked Canceled Entrust Active Expired Revoked You can include multiple certificate statuses by separating each with commas.
Note:
The State field in the Unique Certificate (cmdb_ci_certificate) table denotes the life cycle state of the certificate, not the raw state returned by the CA though API. Certificates discovered with a CA status of issued,
 valid, expired, or canceled, are all denoted with the State value Issued. The State field doesn't include an expired value. To identify certificates that have expired, use the Valid to value rather than the State value.
After the pre-discovery phase is complete, move on to the
post-discovery phase
.
