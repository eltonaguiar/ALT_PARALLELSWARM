# Phase 3 — extract the configuration model

**Status:** COMPLETE
**Started:** 2026-11-13T08:58Z
**Finished:** 2026-11-13T09:08Z

## Extracted backbone

1. **Two discovery styles:** horizontal (probes/sensors *or* patterns) and top-down
   (Service Mapping). Horizontal is the scope of this reference.
2. **Four phases:** Scanning (Shazzam) → Classification → Identification → Exploration.
3. **Two identification paths:**
   - probe/sensor path → identity probe → identity sensor → Discovery identifier;
   - pattern path → pattern specifies CI type → CMDB IRE identification rules.
4. **IRE pipeline:** payload → identify (rules / source key) → reconcile (static or
   dynamic) → commit; partial/incomplete items on failure.
5. **Duplicate control has three layers:** rule strength (design), runtime properties
   (threshold/skip), and remediation (de-dup tasks/templates/main CI).
6. **CI Class Manager** is the front end for class definitions, identification,
   reconciliation, dependencies, and Health, at
   `All > Configuration > CI Class Manager`.

## Key option inventory (exact strings verified against fetched text)

- `glide.discovery.use_cmdb_identifiers` (default `true`)
- `glide.discovery.enforce_unique_ips` (default `false`)
- `glide.discovery.max_concurrent_invocations_per_schedule` (default `3`)
- `glide.discovery.schedule_ipv4_limit` (default `65,536`)
- `glide.discovery.schedule_ipv6_limit` (default `20,000`)
- `glide.identification_engine.skip_duplicates` (default `true`)
- `glide.identification_engine.skip_duplicates.threshold` (default `5`)
- `glide.identification_engine.skip_sys_object_source_matching`
- `glide.identification_engine.lookup_match.create_duplicate_task_ci.enabled` (default `false`)
- `glide.reconciliation.override.null` (default `true`)
- `glide.identification_engine.dynamic_ire_enabled` (default `false`)

## Exit criterion

A section outline and option table exist before drafting prose. ✅
