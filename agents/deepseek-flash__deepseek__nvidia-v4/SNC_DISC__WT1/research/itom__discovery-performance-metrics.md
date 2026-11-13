# Discovery performance metrics

- Source: https://www.servicenow.com/docs/r/zurich/it-operations-management/discovery/discovery-performance-framework.html
- Release: Zurich
- Map: itom

---

# Discovery performance metrics

This Discovery enhancement collects performance
 metrics on probe/pattern and sensor processing times and then aggregates that data over time.
 You can use the roll-up data to monitor the performance of specific discoveries or to compare
 performance between versions after an upgrade.

## Metrics

Discovery provides these individual performance metrics:
- Probe and pattern processing time.
- Sensor processing time.
- Identification and Reconciliation Engine (IRE) processing time for Discovery patterns.
 This processing time is already included in the sensor processing time, but is isolated
 here to provided more insight into the identification and reconciliation of pattern
 payloads.
Discovery can aggregate individual metrics for these attributes:
- Builds/versions
- Discovery status
- Target IP address

## How metric aggregations are triggered

Metric roll-ups are initiated as follows:
- Aggregated by build : Implemented by the Aggregate
 Discovery Probe And Sensor Metrics By Build scheduled job. This job runs
 at 0200, local time.
- Aggregated by status : Implemented by the Rollup
 Probe/Sensor Metrics by Status Script Action, which is triggered by the discovery.complete or discovery.cancelled registered events.
- Aggregated by target : Implemented by the Rollup
 Probe/Sensor Metrics by Target Script Action that is triggered by the discovery.device.complete registered event.
Note:
If Discovery execution is cancelled before it completes, Discovery cannot update
 the IP target metric aggregation table. This is because the
discovery.device.complete
event that triggers aggregation does not
 run. IP target data for an interrupted Discovery is collected when subsequent discoveries
 run successfully on the target. Cancelling Discovery execution does not affect the
 aggregation of other metrics, which are triggered differently.

## Tables

Discovery performance metrics data is stored in these tables:
Table Description
Probe and Sensor Metrics (Individual)
 [discovery_perf_metric_probe_sensor] Stores the individual performance metrics for probes/patterns, sensors, and
 IRE processing times. Probe and Sensor Metrics (Aggregate)
 [discovery_perf_metric_probe_sensor_rollup] This is the base table for the metric aggregations and does not store data
 itself. The three roll-up tables, by-build, by-status, and by-target all extend
 this table. Probe and Sensor Metrics (Aggregated by Build)
 [discovery_perf_metric_probe_sensor_rollup_by_build] Stores the aggregated performance metrics for probes/patterns, sensors, and
 IRE by build and version. Probe and Sensor Metrics (Aggregated by Status)
 [discovery_perf_metric_probe_sensor_rollup_by_status] Stores the aggregated performance metrics for probes/patterns, sensors, and
 IRE by Discovery status. Probe and Sensor Metrics (Aggregated by Target)
 [discovery_perf_metric_probe_sensor_rollup_by_target] Stores the aggregated performance metrics for probes/patterns, sensors, and
 IRE by IP address.

## Discovery properties

Performance metrics properties control whether or not aggregation occurs, but not what data
 is included in the aggregation. Status and IP target data is collected as follows:
- Rollups for status always contain new data. During discovery execution, Discovery continuously collects probe and sensor data for that discovery status. The data is stored in the Probe and Sensor Metrics (Individual) [discovery_perf_metric_probe_sensor] table. Aggregation rolls up all probe and sensor
 data for that particular status after discovery.cancel and discovery.complete events are fired for that status, but only if
 the aggregation property for status roll-ups is enabled.
- Discovery continuously collects data on IP targets and stores it in the Probe and
 Sensor Metrics (Individual) [discovery_perf_metric_probe_sensor] table. Aggregation
 rolls up all existing IP target data after the glide.discovery.perf.metrics.rollup_by_target property is enabled
 and creates records in the Probe and Sensor Metrics (Aggregated by Target)
 [discovery_perf_metric_probe_sensor_rollup_by_target] table.
These properties control the gathering of probe and sensor metrics:
Property Description
glide.discovery.perf.metrics.enable_collection Enables collection of performance metrics. Type : true | false Default : true glide.discovery.perf.metrics.rollup_by_build Enables aggregation of individual discovery performance metrics into a
 roll-up table that groups by build. Type : true | false Default : true glide.discovery.perf.metrics.rollup_by_status Enables aggregation of individual discovery performance metrics into a
 roll-up table that groups by discovery status. Type : true | false Default : false glide.discovery.perf.metrics.rollup_by_target Enables aggregation of individual discovery performance metrics into a
 roll-up table that groups by target IP address. By default, Discovery continuously
 collects individual IP address metrics, even when aggregation by target IP is
 disabled. When you enable IP target aggregation, Discovery includes all target
 metrics in the roll-up table. Type : true | false Default : false

## View Discovery performance metrics for probes, sensors, and patterns

By default, Discovery tracks the
 performance of individual probes, sensors, and patterns by measuring the processing
 time. When patterns are used, Discovery measures the Identification and Reconciliation
 Engine (IRE) processing time.

### Before you begin

Role required: discovery_admin or admin

### Procedure

- Navigate to All > Discovery > Discovery Performance Metrics > Probe/Sensor (Individual) .
- Sort the list by Discovery status to see the list of probes and patterns that
 ran in a specific Discovery.
- You can view the metrics for each probe, sensor,
 or pattern in the list or open the record. All probe and sensor metrics data are
 read-only. The Probe and Sensor Metrics
 (Individual) form provides these fields: Field label Field name Description Build/version build_version Build on which the Discovery was run. Discovery status discovery_status ID number of the Discovery status from which the
 metrics were collected. Target IP address target_ip IP address of the target for this Discovery. ECC queue input ecc_queue_input Identifies a particular ECC input record in the ECC
 queue table. ECC queue topic * ecc_queue_topic Identifies the Java class in the MID Server that
 executes the probe. ECC queue name * ecc_queue_name Identifies the probe/pattern evaluated for
 performance in this aggregation. Probe * probe Name of the probe used for this Discovery. Probe processing time probe_time Interaction time of the MID Server with the target,
 including construction of the payload that is sent back
 to the instance. The time is in milliseconds. IRE processing time ire_time Time required to process the pattern payload on the
 instance by the Identification and Reconciliation Engine
 (IRE). IRE time is useful because it shows the part of
 the sensor time used by the pattern. The time is in
 milliseconds. Sensor processing time sensor_time Time it took the sensor to process the payload on the
 instance for a Discovery. The time is in
 milliseconds. * Used to uniquely identify a probe/pattern and accompanying sensor
 when gathering metrics for a Discovery.

## View Discovery performance metrics aggregated by build

Use the roll-up by build data to ensure that the
 processing times for Discovery components remain consistent for discoveries in a 24 hour
 period. View aggregate build data before and after an upgrade to compare the performance
 of the old and new versions. All aggregated performance data is
 read-only.

### Before you begin

Role required: discovery_admin or admin

### Procedure

- Navigate to All > Discovery > Discovery Performance Metrics > Probe/Sensor (Rollup-By-Build) .
- Sort the list by Build/version .
- Filter by a specific build to see the aggregated
 processing times for the probes and patterns that performed a Discovery on
 that build.
- Open a record to see the probe/pattern statistics for
 the selected build. The form displays additional fields not visible on the
 list. Roll-up calculations are over a 24 hour period, beginning every night
 at 0200.
- See the table of performance aggregation data for
 descriptions of additional metrics displayed on the form for roll-ups by
 build.

## View Discovery performance metrics aggregated by status

Use the roll-up by status data to ensure that the
 processing times for probes/patterns and sensors remain consistent for a specific
 Discovery. All aggregated performance data is read-only.

### Before you begin

Role required: discovery_admin or admin

### About this task

### Procedure

- Navigate to All > Discovery > Discovery Performance Metrics > Probe/Sensor (Rollup-By-Status) .
- Sort the list by Discovery
 status to see the aggregated processing times for the probes
 and patterns that ran during a specific Discovery.
- Filter by a specific status to display metrics
 available for probes and patterns that ran in that status.
- Open a record to see the probe/pattern statistics for
 the selected status. The form displays additional fields not visible
 on the list. Roll-ups are only created for a completed or cancelled
 status.
- See the table of performance aggregation
 data for descriptions of additional metrics displayed on the form for
 roll-ups by status.

## View Discovery performance metrics aggregated by IP address

Use the roll-up by target data to ensure that the
 processing times for probes/patterns and sensors remain consistent for each Discovery of
 a specific IP address. All aggregated performance data is read-only.

### Before you begin

Role required: discovery_admin or admin

### Procedure

- Navigate to All > Discovery > Discovery Performance Metrics > Probe/Sensor (Rollup-By-Target) .
- Sort the list by Target IP
 address .
- Filter by a specific IP address to see the aggregated processing times for the
 probes and patterns that performed the Discovery of that IP address.
- Open a record to see the statistics about the selected
 probe/pattern for the specific IP address. The form displays additional fields not visible on the list. Roll-ups are
 performed after IP Discovery has completed successfully.
- See the table of performance aggregation data for
 descriptions of additional metrics displayed on the form for roll-ups by
 target.

## Aggregated data for Discovery performance metrics

Discovery performance metrics can accumulate data for probes, patterns, and sensors
 each time Discovery runs. Discovery calculates processing times and increments the number of
 times a component runs for each roll-up profile: status, target, or build. All aggregated
 performance data is read-only.

### Sample roll-up form

This is an example of an aggregation record for probe and sensor metrics. The metrics
 fields shown here are used for each aggregation.
Figure 1. Sample roll-up by Status form

### Performance Framework aggregated data

Except where noted, these fields are common to all aggregation records.
Field label Field name Description
Build/version build_version Name of the build running on the instance. This name identifies the version,
 patch level, and release date of the ServiceNow platform. Discovery status discovery_status ID number of the Discovery status record for this aggregation. Note: This
 field only appears on the form for roll-ups by status. Target IP address target_ip_address IP address of the target for this Discovery. Note: This field only appears on
 the form for roll-ups by target. Aggregation cutoff aggregation_cutoff The cutoff time varies, depending on the roll-up profile. By-build : Occurs daily at 02:00, by default. By-status : Closing time of the last aggregation for
 that Discovery status, which might have run the last time discovery.complete or discovery.cancelled ran for that status. By-target : Closing time of the last aggregation for
 that target IP address, which might have run the last time discovery.device.complete ran for that IP
 address. ECC queue topic * ecc_queue_topic Identifies the Java class in the MID Server that executes the probe. ECC queue name * ecc_queue_name Identifies the probe/pattern evaluated for performance in this
 aggregation. Probe * probe Name of the probe used for this Discovery. Probe time (count) probe_time_count Number of times a probe ran for a given roll-up profile. Probe time (average) probe_time_average Average time a probe took to gather data on the target and format the payload
 for a given roll-up profile. Probe time (minimum) probe_time_min Minimum time a probe took to gather data on the target and format the payload
 for a given roll-up profile. Probe time (maximum) probe_time_max Maximum time a probe took to gather data on the target and format the payload
 for a given roll-up profile. Probe time (total) probe_time_total Total time used by a probe to gather data on the target and format the
 payload for a given roll-up profile. Sensor time (count) sensor_time_count Number of times a sensor processed payloads for a given roll-up
 profile. Sensor time (average) sensor_time_average Average time a sensor took to process payloads on the instance for a given
 roll-up profile. Sensor time (minimum) sensor_time_min Minimum time a sensor took to process a payload on the instance for a given
 roll-up profile. Sensor time (maximum) sensor_time_max Maximum time a sensor took to process a payload on the instance for a given
 roll-up profile. Sensor time (total) sensor_time_total Total time used by a sensor to process payloads on the instance for a given
 roll-up profile. IRE time (count) ire_time_count Number of times a pattern's payload was processed by the Identification and
 Reconciliation Engine (IRE) for a given roll-up profile. IRE time (average) ire_time_average Average time used for IRE processing of a pattern's payload for a given
 roll-up profile. IRE time (minimum) ire_time_min Minimum time used for IRE processing of a pattern's payload for a given
 roll-up profile. IRE time (maximum) ire_time_max Maximum time used for IRE processing of a pattern's payload for a given
 roll-up profile. IRE time (total) ire_time_total Total time used for IRE processing of a pattern's payload for a given roll-up
 profile.
* Together, these values uniquely identify a probe/sensor pair (a "probe execution")
 that is used for a Discovery.
