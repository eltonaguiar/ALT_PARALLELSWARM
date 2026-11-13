# Phase 2 — corpus extraction (STARTED → DONE)

- Started: 2026-11-13T08:59Z
- Finished: 2026-11-13T09:10Z

## Method

1. `GET /docs/api/khub/maps` → 1,483 maps.
2. Selected Zurich en-US maps:
   - ITOM: `guxhDnVk8OUAJKLm7WZsYA`
   - Platform Capabilities (IRE/CMDB): `zS6yb8e~gR8BPjeviYdV9g`
3. Fetched TOCs, selected 59 topics + 16 supplementary topics, converted the topic HTML
   to markdown with BeautifulSoup.
4. Saved every topic with its source URL and release to `research/`.

## Output

- 75 files / ~676 KB in `research/`
- `research/source_manifest.json` (machine-readable)
- Coverage: Discovery phases/setup/schedules/behaviors/classifiers/identifiers/properties/
  deletion/SCCM, IRE identification/reconciliation/data-source/simulation/errors,
  CI Class Manager, duplicate detection/remediation.

## Blocker

None. One missing title (`Discovery schedule form reference` in the ITOM TOC) was found
under a slightly different title and fetched successfully.
