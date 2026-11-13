# Module coverage gaps — CMDB & Discovery research vs training pages vs best practice

**Author:** `kilo-sam-deepdive__kilo__cli` · **Date:** 2026-11-13
**Stamp:** 2026-11-13T15:44:29Z · **run-id:** `4178ec70-e3f5-4bc9-a0ab-9c7cdb2acf25`
**Status:** proposed gap register for the `alt_parallelswarm` fleet

---

## ELI5

This repository is the **engineer's notebook** for CMDB and Discovery. The training pages are the **storybooks**. This note checks whether the notebook has pages the storybook lacks, whether the storybook has pages the notebook lacks, and what **both** forget about delivering a module in production.

---

## 1. Research repo strengths (page lacks)

| Asset | What it adds |
|---|---|
| `final/DISCOVERY_INSERT_VS_UPDATE_GUIDE.md` | Four IRE rules as an auditable decision model with precedence and traps — the page teaches the same concepts but without the de-duplicated decision tables |
| Property catalogs (114/112 properties) + delta merges | Exact property names/defaults per release; page has none |
| OOB job inventory + audit recipes | Page describes features, not shipped scheduled jobs |
| Duplicate root-cause catalogue (15+ causes) | Page lists mistakes conceptually |
| Data Refresh vs Health Staleness vs Data Manager distinction | Reporting-only vs data-changing mechanisms separated explicitly |
| Benchmark ledger proof methodology | No page counterpart |
| CMDB success advisor / activity-center alert map | Page covers dashboards generally |

## 2. Training page strengths (repo lacks)

| Page topic | Repo status |
|---|---|
| Webhooks general pattern (outbound/inbound, events alignment) | **Absent** (0 mentions) |
| e-bonding / IntegrationHub integration patterns | **Absent** |
| Service Graph Connector for OpenTelemetry deep dive | Partial (6 files mention SGC/OpenTelemetry) |
| Now Assist debugging prompts for SGC | **Absent** |
| OOB pattern customization routes (duplicate/extend/build) | Present in discovery guide; repo coverage thin |
| Discovery Configuration Console / File-Based Discovery deep dives | Mentioned in repo but not deep-dived |
| Labs, quiz, memory aids | **Absent** from repo finals |
| CIS-Data Foundations / CSDM exam alignment depth | Referenced only |

## 3. General best-practice gaps (both sides)

1. No success criteria or pilot go/no-go gates.
2. No test-case catalogue with expected results.
3. No ownership/RACI model.
4. No source-system contract template.
5. No change-control procedure for identification/reconciliation config.
6. No rollback/exception procedures.
7. No UAT/sign-off, cutover/hypercare, monitoring model, training/runbooks.
8. No performance/capacity sizing guidance.

## 4. Success Pack gaps

Neither repo covers Success Packs at all (0 mentions). Required coverage:

1. Version-compatibility matrix per release.
2. Dependency activation ordering and failure modes.
3. Storage/capacity estimate before install.
4. Backup snapshot requirement; limited uninstallability warning.
5. Post-install smoke-test checklist.
6. Entitlement verification for the pack.
7. Update/upgrade path (pack updates vs family upgrades).
8. Owner assignment for pack content after install.

> The protocol repo (`ServiceNow_Learning/docs/success-packs/success-pack-prerequisites.md`) has prerequisite basics; expand there rather than here.

---

## 5. Bridging actions

| Action | Target |
|---|---|
| Add repo-only items (property catalogs, job inventory, duplicate catalogue) to the CMDB/Discovery pages | Curriculum maintainers |
| Add page-only items (webhooks, e-bonding, OpenTelemetry SGC, Now Assist, labs/quiz) to this repo | Fleet agents |
| Adopt implementation gate checklist | Protocol repo |
| Add HAM research counterpart (HAM page exists, repo does not) | Fleet lead |
| Add Success Pack section to protocol | Protocol maintainers |

---

*Comparison only; no existing documents modified.*
