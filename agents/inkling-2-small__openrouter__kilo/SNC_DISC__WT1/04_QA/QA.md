# QA — SNC_DISC__WT1 (inkling-2-small__openrouter__kilo), 2026-11-13T09:04Z

| # | criterion | result | evidence |
|---|---|---|---|
| 1 | ≥15 distinct sources cited | PASS | 17 in EVIDENCE_DIGEST.md, all Australia bundle, raw HTML saved |
| 2 | Property tables: name + default + where set | PASS | §2, §3, §5 |
| 3 | Order of operations (setup + runtime flow) | PASS | §1 both flows; reconstructed (flagged as synthesis, not a single quote) |
| 4 | CI Class Manager breadcrumbs with navigation path | PASS | §4, from ci-class-manager-landing-page + t_CreateCIType |
| 5 | Duplicate-avoidance config (identifiers, skip_duplicates, enforce_unique_ips, mac verify, use_cmdb_identifiers, serial rules) | PASS | §2.3, §3, §5 |
| 6 | Insert vs update semantics with tables/properties | PASS | §6 (static vs dynamic reconciliation, data refresh, insert bans, reclassification, enhanced APIs, partial payloads) |
| 7 | Sources bracket every non-obvious claim | PASS | [1]–[17] tags; §11 marks the exceptions |
| 8 | Zero fabricated URLs | PASS | all readerUrls came from khub search responses; none typed from memory |
| 9 | Reconciliation/IRE default-ON claims accurate | PASS | defaults transcribed from properties-id-reconciliation.html verbatim |
| 10 | Duplicates remediation covered | PASS | §5(E) + §2 properties + dry_run advice |

### Self-found nits
- Doc §6 cites "cmdbreconciliationdefinition (docs spelling)" — Australia docs literally print the concatenated spelling; flagged accordingly, not silently "corrected".
- `glide.discovery.discoverable.network.max.netmask.bits` default not captured → marked UNVERIFIED rather than guessed.
- §1 reconstructed order-of-operations is an engineering synthesis; the docs have no single canonical page for it (Configuring Discovery lists procedures flatly).
- Discovery properties page is 40KB — a few minor properties omitted (lighting/certs/tag-based) to keep signal; they don't affect CMDB insert/update correctness.

QA verdict: **GO.** Reference is internally consistent and evidence-backed. Not a substitute for
instance validation — defaults differ per customer; dry_run + identifyCI() before prod changes.
