# Phase 1 — discover the documentation corpus

**Status:** COMPLETE
**Started:** 2026-11-13T08:49Z
**Finished:** 2026-11-13T08:52Z

## Actions

- `GET /docs/api/khub/maps` → 1,483 maps. Selected the English **Brazil** maps:
  - ITOM: `bsp_DjPRMilbWYHwwVa4zQ`
  - Platform capabilities (CMDB/IRE): `zf4CFrQ4oaR8UN3GV4kT5g`
- `GET /maps/{id}/pages` → ITOM TOC 321 Discovery pages; platcap TOC parsed for
  CMDB/IRE/duplicate topics.
- `POST /api/khub/clustered-search` across 12 queries to resolve exact topic IDs.

## Output

- `research/SOURCES.md`
- `research/topics.json` (topic key → map ID → content ID → canonical URL)
- 60 selected topic IDs across Discovery, CMDB IRE, duplicates, Health, Data Manager.

## Exit criterion

Enough authoritative topics resolved to cover all success criteria. ✅
