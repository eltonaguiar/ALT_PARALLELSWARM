# LESSONS_LEARNED — ALT_PARALLELSWARM

- **agent_id:** beam__kilo__cli
- **timestamp (UTC):** 2026-11-13T15:48:00Z

## Lessons from the SNC_DISC/SAM parallel pass
1. Discovery vs SAM metrics differ: CI insertion/update rules do not alone make SAM
   compliance defensible; entitlements, software models, normalization, SaaS consumption,
   and reconciliation must be documented and tested.
2. Parallel agent outputs varied widely (some incomplete); relying on a single final
   consolidated reference with provenance and UNVERIFIED items is safer.
3. Release pinning matters (Australia vs Brazil) to avoid property drift.
4. Root scaffolding (Harness/INDEX) helps merge work without collisions.

## Cross-repo gaps (CMDB vs SAM)
- SAM doc set should mirror schema-level CMDB Discovery depth plus entitlement/metric specifics.
- CMDB guide items missing in SAM (e.g. full property lists) should be ported when relevant.
EOF