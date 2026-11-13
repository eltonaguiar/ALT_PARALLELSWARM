# General guidelines for using CMDB Identification

- Source: https://www.servicenow.com/docs/r/zurich/servicenow-platform/configuration-management-database-cmdb/best-practices-id-reconcile.html
- Release: Zurich
- Map: platcap

---

# General guidelines for using CMDB Identification

Summarize Summarized using AI This content was generated using new OpenAI-powered functionality. Results are provided on an as is basis and are not guaranteed to be accurate or complete. Summary of General guidelines for using CMDB Identification This document provides essential best practices for effectively using CMDB Identification within ServiceNow, focusing on creating robust identification rules and optimizing payloads to improve CI identification accuracy and system performance. Show full answer Show less Identification rules Independent identification rules identify a CI solely based on its own attributes and are preferred for their speed and reliability. Dependent identification rules identify CIs based on their relationships with other CIs but require more processing time and are prone to errors; their use should be minimized and limited to a maximum of two dependency levels. When modeling CIs, prioritize defining attributes that support independent identification to avoid dependencies. Avoid using lookup identifier entries, as they can degrade performance; instead, review and update class definitions to use independent identification rules. Each identification rule should ideally have only one identifier entry to maintain performance; multiple entries can slow down identification. Assign the highest priority to the strongest identifier entries within rules. Ensure identification rules are implemented at the correct class level for the CIs being identified. Payload guidelines Limit payload size to a maximum of 500 CIs per call to prevent performance degradation. Avoid duplicate CI entries in the payload to prevent failures during identification. Exclude system metadata fields such as sysdomain , sysupdatedon , or sysmodcount from payloads, as these are managed internally. Provide only the minimum necessary criterion attributes required by the identification rules for each CI in the payload. When available, use the CIâs sysid in the payload to enable direct and efficient CI matching without relying on other attributes. For dependent CIs, include related CIs and define their relationships explicitly in the payload to ensure proper identification and linkage. When inserting multiple dependent CIs related to the same parent CI, serialize API calls to avoid system congestion and maintain performance. Practical implications for ServiceNow customers Following these guidelines ensures that your CMDB identification rules are efficient, accurate, and scalable. Prioritizing independent identification reduces errors and speeds up processing. Properly constructed payloads with minimal and precise data improve system responsiveness and prevent failures. Using sysid for updates simplifies matching and reduces overhead. Serializing API calls during bulk CI insertions protects system stability. Adhering to these best practices will help maintain a healthy, performant CMDB and improve your overall configuration management processes.
Review the following general guidelines for using CMDB Identification effectively.

## Identification rules

An
independent identification rule
identifies a CI based on the CI's attributes,
 independently of other CIs.

A
dependent identification rule
identifies a CI by its dependent CIs and
 the relationships of the identified CI with those dependent CIs. Identification with
 a dependent identification rule is based on the dependent CIs and the relationships
 and qualifiers between the identified CI and its dependent CIs. Identification then
 requires more time than with an independent identification rule and is prone to some
 identification errors. Usage of dependent rules should therefore be minimized.

CI modeling determines which type of identification rules are required for proper CI
 identification.

Create identification rules using the following order of importance:
- Independent identification rules â It is always preferable to create
 independent identification rules rather than dependent identification rules.
 When you model a CI, define the CI with a complete set of attributes that
 lend themselves to independent identification, eliminating the need to use
 additional CIs for identification.
- Dependent identification rules â If it is necessary to create dependent
 identification rules, then define a single level of dependency. Two is the
 maximum number of dependency levels that is supported.
- Avoid creating lookup identifier entries. The use of lookup identifier entry
 is highly discouraged as it can reduce performance. If unavoidable, ensure
 to first review class definitions and consider updates that allow usage of
 independent identification rules.
- Limit the number of identifier entries within an identification rule,
 ideally to 1. A second identifier entry can further reduce performance, as
 will each additional identifier entry.
- Create strong identification rules in which the strongest identifier entries
 and related entries are set with the highest priority.
- Ensure that the identification rule is at the class level that it needs to
 be.

## Payload

Create the payload using the following order of
 importance:

- Payload size â Limit the number of CIs per payload to 500.
- Avoid duplicate entries in the payload. Example: If an identification rule has a criterion
 attribute for the name field, then the following
 payload has duplicate items resulting in
 failure: var payload = {
 items: [{
 className:'cmdb_ci_linux_server',
 values: {
 name:'Win Server 200',
 ram:'2048'
 }},
{
 className:'cmdb_ci_linux_server',
 values: {
 name:'Win Server 200',
 ram:'4096'
 }}]
};
- Do not pass system data such as the following in the payload. var payload = {
 items: [{
 className:'cmdb_ci_linux_server',
 values: {
 name:'Win Server 200',
 sys_domain:'global',
 sys_domain_path:'xyz',
 sys_updated_on:'2017-06-15 16:25:11',
 sys_mod_count:23,
 }}]
};
- Provide the minimum necessary set of criterion attributes for each payload item, according
 to what is specified in the corresponding identification rules.
- When matching CIs, use CIsâ sysIds if available. If provided, IRE can use the sysId to
 directly locate a CI without requiring any criterion attributes from the
 identification rule. In this case, IRE does not use the sysId in the matching
 process. Example: Independent CI that needs to be updated â sysId is available. var payload = {
 items: [{
 className:'cmdb_ci_linux_server',
 values: {
 sys_id:'194876usytrr65378098',
 ram:'2048',
 }}]
}; Example: Dependent CI that needs to be inserted. Tomcat War CI depends
 on Tomcat CI, and Tomcat CI depends on Linux Server CI. SysIds for the
 Tomcat and the Linux CIs are available. var payload = {
 items: [{
 className:'cmdb_ci_app_server_tomcat_warâ, 
 values: {
 name:'war1',
 short_description:'my description' }
 }, {
 className:'cmdb_ci_app_server_tomcat',
 values: {
 sys_id:'194876usytrr65378098'
 }
 }, {
 className:'cmdb_ci_linux_server',
 values: {
 sys_id:'09876tysueyt6345lakiu'
 }
 }],
 relations: [{
 parent:1,
 child:0,
 type: 'Contains::Contained byâ}, {
 parent:1,
 child:2,
 type:'Runs on::Runs'}
 ]
 }; Example: Dependent CI that needs to be updated â sysId is
 available. var payload = {
 items: [{
 className:'cmdb_ci_app_server_tomcat_war', 
 values: {
 sys_id:'039387euey637465sytet',
 short_description:'my description new' }
 }]
 };
- When inserting many CIs, all of which depend on the same CI, you should serialize your API
 calls. Otherwise, attempting to concurrently process many CIs can clog the
 system, significantly degrading overall system performance.
