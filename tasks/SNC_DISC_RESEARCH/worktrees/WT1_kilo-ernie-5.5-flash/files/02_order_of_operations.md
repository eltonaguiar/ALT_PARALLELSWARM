# 02 — Discovery: Order of Operations

Discovery runs in **four horizontal-discovery phases**, driven through the **ECC queue**
and executed by the **MID Server**. Below is the end-to-end flow, then each phase in detail.

## Big picture

```
Discovery Schedule (triggers)
        │
        ▼
  [Shazzam probe] ──► MID Server scans ports ──► ECC queue (output→input)
        │
        ▼
  Phase 1: SCANNING      (find open ports / device type)
        ▼
  Phase 2: CLASSIFICATION (classify device → pick classifier)
        ▼
  Phase 3: IDENTIFICATION (identification rules → insert vs update CI)
        ▼
  Phase 4: EXPLORATION    (gather details + relationships)
        ▼
  CMDB updated by sensors (via IRE / reconciliation)
```

**Component mechanics**
- A **probe** is a script that collects data on a host. A **sensor** processes the returned
  data and updates the CMDB. Both are driven by **ECC queue** entries.
- The MID Server has a worker that watches the ECC queue for **output/ready** entries, runs the
  probe, and returns results to the queue as **input** entries.
- When an input entry is inserted, a **business rule** runs the **sensor processor**, which finds
  sensors interested in the data and passes it along; sensors update the CMDB.
- If a probe has a **post-processing script**, it runs on the MID Server; otherwise the sensor does
  the processing.

## Phase 1 — Scanning
1. Discovery places the **Shazzam** probe (and **port probes**) in the ECC queue.
2. MID Server runs Shazzam against the target IPs — detects which common ports are open
   (e.g. 135 WMI, 22 SSH, 161 SNMP, 80/443 HTTP).
3. Open ports identify likely device type (port 22 → UNIX/Linux; 135 → Windows; etc.).
4. Results return to the ECC queue; Discovery reads which ports responded.

**Knobs:** Shazzam batch size (default 1000, min 256), Shazzam max range size, Shazzam cluster
support, SNMP version, IP ranges / range sets.

## Phase 2 — Classification
1. Using the responding port probe's record, Discovery selects a **classification probe** to run.
2. The classification probe gathers OS/version detail. **Only one classification probe runs per device.**
3. Discovery matches results to **CI classifier** records → determines the CI **class** and the
   **trigger probes** for the next phases.
4. HTTP is lowest-priority classification: used only if WMI/SSH/SNMP ports are closed or fail.

**Classifier types:** device classification (Windows/UNIX/router/switch/load balancer), process
classification (applications → child CIs with *Runs on::Runs*), IP-address/scan classification
(credential-less).

## Phase 3 — Identification
1. Discovery picks the **classifier** for the CI class and runs its **identification trigger probe**.
2. The identification probe gathers identity attributes; sensors process them.
3. Discovery applies **identification rules (CI identifiers)** to decide **insert vs update**:
   - Match found → **update** the existing CI.
   - No match → **insert** a new CI.
4. If patterns are used, the trigger probe is the **Horizontal Pattern probe**, which launches the
   pattern; **IRE** performs identification and the CMDB insert/update based on the CI type's rules.

This is where **duplicates are prevented** (see doc 04). Identification uses the strongest available
key first: `source_name` + `source_native_key`, then identifier-entry criterion attributes, then sysId.

## Phase 4 — Exploration
1. Discovery reads the classifier's **Triggers Probes** related list for **exploration probes**.
2. Exploration probes gather deeper detail (applications, memory, NICs, disks, drivers).
3. Sensors update the CMDB (same as identification). Discovery also creates **relationships**
   (app↔device, app↔app).
4. If a pattern is used, the pattern's operations perform exploration instead of probes.

## Discovery Status & observability
- **Discovery Status** form: per-run progress, **Completed activity** / **Current activity**,
  Discovery Devices, ECC queue tab (see probes sent vs returned).
- **Discovery Log**: messages, warnings, errors (verbosity via `glide.discovery.log_debug`).
- **ECC Queue**: inspect raw input/output payloads (keep attachments via
  `glide.discovery.sensors.save_attachments=true`).

## Failure & throttling controls
- `glide.discovery.max_concurrent_invocations_per_schedule` (default 3) — prevents overlapping runs.
- **Max run time** / **Max Idle time** on the schedule — cancel runaway/stalled runs.
- **MID Server selection / behaviors** — spread load, avoid single-MID bottlenecks.

## Sources
- Exploring Discovery — servicenow.com/docs (c_GetStartedWithDiscovery)
- Probes and sensors — servicenow.com/docs (c_DiscoveryProbesAndSensors)
- Process flow with probes and sensors — servicenow.com/docs (c_DiscoProcessFlows)
- Discovery classifiers — servicenow.com/docs (discovery-classifiers)