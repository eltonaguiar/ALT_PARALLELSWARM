# Discovery timelines

- Source: https://www.servicenow.com/docs/r/zurich/it-operations-management/discovery/c_DiscoveryStatusTimelines.html
- Release: Zurich
- Map: itom

---

# Discovery timelines

A
Discovery
timeline generates a
 graphical display of a
Discovery
Status
 record, including information about each probe and sensor that was used in the discovery.

Use Discovery Timelines to display the following:
- The flow of probes and sensors , including those that are used with patterns through a discovery.
- The duration of each probe and sensor that ran during a discovery, and the proportion of
 time required for queuing and processing.
- Tooltips containing additional data about a probe and sensor.
- Records from the ECC Queue.

## Size of discoveries in the timeline

View timelines for an entire discovery or for individual devices in a discovery. By
 default, the maximum size discovery that you can display in a timeline is 300 entries in
 the ECC Queue (150 probes and 150 sensors). To display larger discoveries, change the
 default setting in the
glide.discovery.timeline.max_entries
property.

## Example Discovery Timelines

This example shows the Discovery timeline
 for the first two phases of Discovery (Port scan and Classification):

Figure 1. Discovery (early phases) on the timeline
In this example, the Shazzam probe and sensor run, followed by the Unix classifier probe
 and sensor. The classifier calls the Horizontal Pattern probe, which runs a specific
 pattern.

## View the Discovery timeline

A
Discovery
Timeline generates
 a graphical display of a Discovery Status record, including information about each probe,
 sensor, and pattern running.

### Before you begin

Role required: discovery_admin or admin

### About this task

### Procedure

- Navigate to All > Discovery > Status .
- Select a Discovery from
 the record list.
- Click the Show Discovery Timeline Related Link.
- Clear the warning, and then select the Devices Related
 List.
- Click the IP address of a device.
- In the Device record, click the Show Discovery Timeline Related Link. The Discovery timeline for that device appears. Figure 2. Discovery Timeline
- Use the pink slider at the bottom of the timeline to change the
 perspective. Move the slider from right to left to view all the tasks on a long
 timeline. Adjust the end points of the slider to change the magnification. A narrow slider zooms in on the spans and provides a more detailed view of complex timelines. A wide slider pulls the view out and makes more of the timeline visible on the screen.
- Use the selector range at the top of the screen to adjust the visible time frame.
- To limit the timeline to the length of the Discovery , click Max . The time scale adjusts automatically to the length of the Discovery . The available time scale range is from one day to 1 year. Tooltips Discovery timelines display probe and sensor performance data
 and CI information in tooltips. Hover your cursor over a span to view this
 data. Probes are displayed by black spans. The queue time for a probe is shown as a
 silver bar within the span, and the processing time is represented by the
 remaining space. Sensor spans are red, and the queue time is shown as a green bar. Selected spans
 of any type display in yellow. Figure 3. Discovery Timeline Shazzam Sensor ECC Queue Double-click a span to open the ECC Queue record for that probe or sensor. Figure 4. Discovery Timeline ECC Queue
