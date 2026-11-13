# Create a Discovery behavior

- Source: https://www.servicenow.com/docs/r/zurich/it-operations-management/discovery/create-disco-behavior.html
- Release: Zurich

---

# Create a Discovery behavior

Create a Discovery behavior to determine which probes Shazzam launches and which MID Server is used.

## Before you begin

Role required: discovery_admin

## Procedure

- Navigate to All > Discovery Definition > Behavior .
- Select New .
- Enter a name.
- Right-click the form header and select Save .
- In the Discovery Functionality related list, select New . Discovery Functionality defines what each MID Server in this behavior must do, specifically which protocols to detect.
- Fill out the form fields: Field Description Phase Enter an integer that represents an arbitrary phase.
                                                The phase is used to group one or more
                                                functionalities together. All the functionalities
                                                within a specified phase are executed together, and
                                                all phases are executed in numerical order. All
                                                functionalities in a behavior can have the same
                                                phase. The Shazzam probe runs once for each phase in a
                                                behavior, which makes fewer phases desirable. Run
                                                multiple phases for behaviors only when devices in
                                                the network are running multiple protocols, such as
                                                SSH and SNMP. In that example, set one phase for the
                                                SSH scan and another phase for the SNMP scan. Active Keep this option selected to apply the discovery
                                            functionality. Functionality definition Select the lookup icon, and then select a pre-configured functionality that defines the protocol or list of protocols that each MID Server scans. Match criteria Define criteria here for Windows MID Servers . MID Servers Select one or more MID Servers to perform this functionality for the following Discovery types: IP Scan CI Scan Discovery automatically balances the load when multiple MID Servers are selected.
- Right-click the form header and select Save .
- To add criteria that the functionality must meet to be triggered, select New in the Functionality Criteria related list. Note: Functionality criteria are required for Windows MID Servers only, and only when the behavior controls Discovery across multiple domains. When the instance launches the Shazzam probe for a Discovery in which a behavior defines multiple MID Servers to scan multiple domains, the functionality criteria determine which MID Server process the results of the probe.
- Fill out the form fields: Field Input Value Name The name in the criteria is the variable that passes the following information: mid_server : MID Server that processes the results from the Shazzam probe. Enter the actual name of the MID Server in the Value field. win_domain : Windows domain of the target device. Enter the actual name of the Windows domain in the Value field. mid_win_domain : Windows domain of the MID Server that is processing the Shazzam results. Enter the actual domain name in the Value field. Operator Select a logical operator. Value Enter the actual name of the MID Server ( mid_server ), target domain ( win_domain ), or MID domain ( mid_win_domain ) to pass to Discovery for this criteria. The following graphic shows an example of functionality criteria.
- Select Submit .

## What to do next

Schedule a horizontal discovery
of type
Configuration Item
, and select
Use Behavior
for the
MID Server
selection method.
