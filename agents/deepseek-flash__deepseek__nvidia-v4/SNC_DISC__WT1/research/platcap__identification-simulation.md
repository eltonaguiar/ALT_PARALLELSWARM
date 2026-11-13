# Identification simulation

- Source: https://www.servicenow.com/docs/r/zurich/servicenow-platform/configuration-management-database-cmdb/identification-simulation.html
- Release: Zurich
- Map: platcap

---

# Using identification simulation

Identification simulation is a central location for automatically constructing a payload that is guaranteed to be complete and valid. You can then simulate the processing of the payload by the Identification and Reconciliation
 Engine (IRE) and examine the results before actually submitting it for execution by IRE.

Use identification simulation to construct an input payload, and simulate processing of the
 payload by IRE. You can then examine the results, adjust identification rules if needed, and
 re-run the simulation of the updated payload.

Use the identification simulation to:
- Automatically construct input payload that is based on existing identification rules,
 hosting and containment rules.
- Simulate execution of a payload (automatically constructed by identification simulation, or
 manually created).
- Browse payload output and execution log messages for a simulated run.
Note:
- Identification simulation does not commit any updates to the CMDB.
- Identification simulation supports simulation of processing payloads that are provided and
 which contain non-CMDB tables, but doesn't support the generation of such payloads.

## Automatically generate payload

Use identification simulation to automatically construct an input payload for a
 specified class. The constructed payload is complete with any required dependent CIs,
 correctly structured, and syntactically valid for processing by the identification and
 reconciliation engine (IRE).

### Before you begin

Role required: admin

### About this task

The payload that is constructed during identification simulation is for the specified
 class. For a dependent CI class, you will be prompted for information about all
 dependencies. After you provide the required details, identification simulation
 constructs the payload based on your input.

Note:
Automatically generating payloads that contain non-CMDB tables, isn't
 supported.

### Procedure

- Navigate to All > Configuration > Identification/Reconciliation , and click Identification
 Simulation .
- In the Start with CI Class box click Start .
- On the Payload Information form, in the Data
 source field, select the data source that is associated with
 this class update. For the ServiceNow Discovery data source, select ServiceNow .
- Select the Class in the payload. In the Criterion Attributes area select the CI
 identifier attributes and then specify the values that uniquely identify
 a CI. In the Additional Attributes area specify
 attributes and values that matching CIs will be updated with.
- For dependent CIs associated with dependent identification rules, fill out the Criterion Attributes and Additional
 Attributes sections in all Container
 level sections that display.
- Click Generate Script .
- If any errors indicate that there are missing fields, fill in the missing fields and then click Generate Script again.

### What to do next

- Click Run Simulation to simulate processing of the
 payload by IRE.
- Examine the results of the simulation, fine-tune the payload as needed, and
 combine with other payloads for other classes as desired. After finalizing the
 payload, use the createOrUpdateCI() API to execute the payload by
 IRE which will result in actual updates to the CMDB.
- Click Copy Script to copy the JSON script into the
 clipboard. You can then paste that script into a third party software or to
 another screen of the identification simulation.

## Simulate payload processing using identification simulation

Use identification simulation to simulate the identification and reconciliation
 engine (IRE) process of CI identification for an input payload. Provide a valid payload,
 which was constructed using identification simulation or that was created
 manually.

### Before you begin

Role required: admin

### Procedure

- Navigate to All > Configuration > Identification/Reconciliation , and click Identification
 Simulation .
- Optional: To run a simulation of an existing payload: Click Start in the Start with
 Existing Payload tile. On the Insert JSON Payload page, select the Data
 source that is associated with this class update. Optional: Select Use Enhanced Identification to apply the identifyCIEnhanced API for enhanced CI
 identification, instead of using the identifyCI API. Paste the JSON payload into the empty canvas.
- Optional: To construct a new payload click Start in the Start with CI Class tile. See Automatically generate payload for more information.
- Click Run Simulation to simulate processing of the
 payload by IRE.

### What to do next

- Examine the results of the simulation in the results pane, and fine-tune the
 payload as needed: Click Run #1 to display the Context
 ID and the Run ID of the
 simulated run. Click the drop down arrow next to Run #1 to
 display additional details. Input : Displays the payload for the
 simulation. Logs : Displays all the logged messages
 that IRE generated while simulating processing of the payload,
 according to the specified logging level. Output : Displays the output payload
 returned by IRE.
- After finalizing the payload, use the createOrUpdateCI() API to execute the payload by
 IRE which will result in actual updates to the CMDB.

## Set logging level for identification simulation

Identification simulation logs each step of a simulated payload processing. You can
 then examine these run logs to determine if a payload was processed as expected, and if
 identification rules are effective. You can adjust the level of logging so it is helpful,
 and so that the amount of messages is not excessive or insufficient.

### Before you begin

Role required: admin

### Procedure

- Navigate to All > Configuration > Identification/Reconciliation , and click Identification
 Simulation .
- Click the Settings icon.
- Select logging level for the identification and reconciliation engine (IRE)
 under IE Log Level and for the service cache under Service Cache Log Level . The logging levels are displayed in ascending order, from the minimum level to
 the maximum level of logging.
- Click on the Settings icon again to close the Settings dialog box.

## Examine run logs

Identification simulation provides run logs which are generated by Identification and
 Reconciliation Engine (IRE). You can access these run logs for payload runs, to examine
 results and for debugging purposes. IRE payload output logs appear in a user friendly format
 on a central page.

### Before you begin

Role required: admin

### About this task

Also, internal applications that use IRE (such as
Discovery
) can call
 an internal API to provide a URL to viewing IRE run logs.

Logging is in the context of a specific run of the identification engine, and you can
 filter the log list by a specific data source and time range. Up to 1000 run logs
 that are up to 2 months old are listed, grouped by Context IDs, and run times. You
 can use the
glide.identification_logs.max_run_ids
property to modify the 1000 limit.

You can control the logging level by using the
glide.discovery.identification.log_level
Discovery system
 property and setting the value to one of the following:
- Info
- Warn
- Error
- Debug
- DebugVerbose
- DebugObnoxious
Note:
IRE performs an initial verification of a payload before processing
 identification rules. If IRE detects any duplicate CIs based on any class
 identifiers, the payload is rejected and processing stops.

### Procedure

- Navigate to All > Configuration > Identification/Reconciliation > Identification Logs .
- Filter the runs list as follows: Source : Select the data source for which to
 display run logs. Time Range : Specify a time range for which to
 display run logs. The Runs list displays all runs for the specified data
 source, during the specified time range.
- In the Runs list, click a Run # to display its Context ID and Run
 ID . A unique Context ID is associated with each specific payload that is run. Each
 run of that payload, is associated with a unique Run ID. A single Context ID for
 a payload that is run multiple times is associated with multiple Run IDs.
- Click the drop down arrow for a Run # to display
 additional details. Input : Displays the payload for the run. Logs : Displays all the logged messages that the
 identification engine generated while running the payload, according to
 the specified logging level. Output : Displays the output payload returned by
 the identification engine.
