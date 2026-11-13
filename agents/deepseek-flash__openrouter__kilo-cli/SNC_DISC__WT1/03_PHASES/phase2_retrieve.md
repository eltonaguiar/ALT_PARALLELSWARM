# Phase 2 — retrieve authoritative content

**Status:** COMPLETE
**Started:** 2026-11-13T08:53Z
**Finished:** 2026-11-13T08:58Z

## Actions

- Fetched 60 topics via
  `GET /api/khub/maps/{mapId}/topics/{contentId}/content?target=DESIGNED_READER`.
- Stripped scripts/styles/navigation; preserved tables as text rows.
- Saved raw HTML + cleaned text under `research/raw/` (not committed to keep the repo
  light; the API URLs are reproducible and listed in `research/SOURCES.md`).
- Fetched 8 follow-up topics: IRE properties, run options, data refresh, dependent
  relationship rules, class dependency, MID properties, create class, DAW reference.

## Results

- 60/61 initial topics succeeded (one unresolved placeholder ID skipped by design).
- Total cleaned text: ~350 KB.
- Zero fabricated pages: every fetch was an HTTP 200 from the docs API.

## Exit criterion

≥ 50 topics with real text, including the property reference and IRE rule reference. ✅
