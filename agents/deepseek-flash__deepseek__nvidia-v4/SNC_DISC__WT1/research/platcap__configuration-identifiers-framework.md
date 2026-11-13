# Configuration identifiers framework

- Source: https://www.servicenow.com/docs/r/zurich/servicenow-platform/configuration-management-database-cmdb/configuration-identifiers-framework.html
- Release: Zurich
- Map: platcap

---

# Configuration identifiers framework

Summarize Summarized using AI This content was generated using new OpenAI-powered functionality. Results are provided on an as is basis and are not guaranteed to be accurate or complete. Summary of Configuration identifiers framework The Configuration identifiers framework in CMDB Workspace allows ServiceNow customers to customize the behavior of CMDB Workspace features on a per-workspace basis. This framework is especially useful when integrating CMDB Workspace features into other workspaces, enabling tailored settings specific to each workspace environment. Show full answer Show less A configuration identifier (config identifier) is a record that holds custom settings and table-driven configurations for a particular CMDB Workspace feature within a specific workspace. These identifiers override default feature behaviors only for their assigned workspace, facilitating flexible and targeted customization. Key Features Config Identifier Records: Stored in the sncmdbwsconfigidentifier table, each config identifier acts as a parent to various configuration settings relevant to a workspace. Default Config Identifier: There is a single, workspace-agnostic default identifier with predefined settings that apply when no workspace-specific configurations exist. Only one config identifier can be set as the default. Role-Based Access: Specific roles manage configuration identifiers: sncmdbws.configeditor: Modify child configuration tables. sncmdbws.configadmin: Modify both config identifiers and child tables. sncmdbadmin: Required for modifying default config records and the default identifier itself. Feature Integration Examples: Unified Map customization such as node limits, levels, endpoint de-duplication, and displayed attributes. Class profile creation for visible layers and lifecycle stage-based CI visibility. Customization of CI creation, including additional requested attributes and limiting class lists per workspace. Key Outcomes By leveraging configuration identifiers, ServiceNow customers can: Integrate CMDB Workspace features seamlessly into other workspaces with tailored configurations. Maintain default settings globally, while applying workspace-specific customizations as needed. Control detailed feature behavior such as map displays and CI creation attributes, improving user experience and operational efficiency in different workspace contexts. Ensure governance and security over configuration changes through defined roles and permissions.
Configuration identifiers provide a framework that lets you customize some behaviors of a CMDB Workspace feature, enabling different settings for that feature, on different workspaces. Most importantly, you can use this
 customization framework when integrating a CMDB Workspace feature into another workspace.

## Configuration identifier

A
configuration identifier
(also referred to as
config identifier
) is a configuration element within the configuration identifiers framework. A config identifier contains custom settings for a CMDB Workspace
 feature, that is applicable to a specific workspace. A config identifier contains settings and table-driven configurations used in a UX application such as a workspace. Using config identifiers lets you for example, integrate CMDB
 Workspace Unified Map into another workspace, with the integrated Unified Map being customized for the workspace. Config identifiers are stored in the Config identifiers [sn_cmdb_ws_config_identifier] table.

A config Identifier acts as the parent record for a set of configurations that are specific to a workspace and therefore overrides default behavior only for that workspace.

## Default config identifier

Initially, the Config identifiers [sn_cmdb_ws_config_identifier] table in CMDB Workspace, contains a single config identifier named âDefaultâ and which is workspace-agnostic. This Default config identifier has its
Default
column set to
Yes
, a setting that can't be modified. Only a single config identifier can be set to
Yes
, therefore, any additional config identifiers that
 you create are set to
No
.

The default config identifier contains default settings for CMDB Workspace features. Any subsequent Config Identifier that you configure, is set for a specific workspace. When integrating a CMDB Workspace feature into another
 workspace and there are no entries in the table-driven configuration for that feature, look-up uses the settings in the default configuration identifier.

## Key roles

The following roles are needed in order to use the configuration identifiers framework:
- sn_cmdb_ws.config_editor: Can modify child config tables, such as sn_cmdb_ws_config_property.
- sn_cmdb_ws.config_admin: Can modify both sn_cmdb_ws_config_identifier and child config tables.
- sn_cmdb_admin: Role required to modify default config records under the default identifier or the default identifier itself.
For more information about these roles, see
Components installed with CMDB Workspace
.

## Examples of CMDB Workspace features using the configuration identifiers framework for feature settings

- Unified Map: Configure how many nodes can appear on a map Configure the default or maximum number of levels on maps Configure endpoint de-duplication on maps Configure which attributes to display in the Attributes panel Create a class profile of visible layers for classes Configure CIs to appear based on life cycle stage value
- Create CI: Request additional attributes for new CIs Limit the class list for new CIs created in a workspace
