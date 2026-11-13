# Create a new discovery schedule form reference

- Source: https://www.servicenow.com/docs/r/zurich/it-operations-management/discovery/create-a-new-discovery-schedule-form.html
- Release: Zurich

---

# Create a new discovery schedule form reference

The Create a new discovery schedule form displays information related to the schedule
 and the target cloud provider. The Create a new discovery schedule form is available in the
Cloud Discovery Workspace
.

For instructions on this procedure, see
Create a discovery schedule in Cloud Discovery Workspace
.

Table 1. Choose the provider form
Field Description
Discovery schedule name Name of the discovery schedule. Cloud provider Name of the cloud provider that hosts the
                                                resources you want to discover. MID selection types MID Server or MID cluster that you
                                                want to use to discover the cloud resources. The
                                                  following options are available: Auto-Select MID Server: Discovery automatically selects an appropriate MID Server . Specific MID Cluster: Discovery uses the MID cluster specified in the MID cluster
                                                  field. Specific MID Server : Discovery
                                                  uses the MID Server specified in
                                                  the MID Server field. If the
                                                  selected MID Server is a part of a
                                                  MID cluster, the jobs are equally distributed
                                                  among all the MID Servers of
                                                  that cluster. This field appears only when one of
                                                  the following values is selected from the cloud
                                                  provider field: AWS Azure Google MID clusters MID clusters you want to use with the Cloud Discovery schedule. This field
                                                  appears only when the Specific MID Cluster value
                                                  is selected from the MID selection types
                                                  field. Credential-less discovery Option to use credential-less discovery. To
                                                  view and filter the MID Servers that can assume an IAM role to discover the
                                                  cloud resources, move the Credential-less discovery toggle to the right. MID Servers MID Servers you want to use
                                                with use with the Cloud Discovery schedule. This field appears only when the
                                                  Specific MID Server value is
                                                  selected from the MID selection types
                                                field.
