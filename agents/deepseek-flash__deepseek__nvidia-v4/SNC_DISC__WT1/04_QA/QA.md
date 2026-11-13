# 04 — QA

- **Agent:** `deepseek-flash` / provider `deepseek` / harness Kilo CLI / worktree `nvidia-v4`
- **QA time:** 2026-11-13T09:15Z
- **Deliverable:** `05_FINAL/DISCOVERY_CONFIG_REFERENCE.md`

## 1. Success criteria from PLAN.md

| Criterion | Result | Evidence |
|---|---|---|
| 5/5 required areas covered | **PASS** | §2 order of operations; §3 configuration; §4 CI Class Manager; §5 IRE; §6 duplicates/insert-vs-update. |
| ≥25 named properties with type + default | **PASS** | 84 unique property tokens; property tables in §3.4 and §5–6. |
| ≥15 exact navigation paths | **PASS** | 24 unique inline breadcrumbs + Appendix B index (23 entries). |
| 4 horizontal phases + IRE entry point | **PASS** | §1.2 and §1.4. |
| Identification variants explained | **PASS** | §5.3 (regular/lookup/hybrid, independent/dependent, inheritance, related entries). |
| Static vs dynamic reconciliation, data source, data refresh | **PASS** | §5.4–5.5. |
| Duplicate lifecycle | **PASS** | §6.2–6.3 (detection → task → main CI → remediation → properties). |
| Claims traceable / practitioner marked | **PASS with caveat** | 59 captured source topics; judgement marked `[practitioner]`. See §4. |
| Reproducible extraction | **PASS** | Recipe in `00_PREREQ/PREREQ.md`; corpus in `research/`. |
| Reproducible swarm | **PASS** | `nvidia_v4_swarm/`; real run `runs/20261113T090332Z/`. |

## 2. Coverage matrix

| Required subject | Where | Depth |
|---|---|---|
| Configuration options | §3.1–3.11, §5.3–5.6 | Schedules, MID/behavior, credentials, classifiers, identifiers, patterns, ~80 properties, deletion, SCCM, domains. |
| Order of operations | §2 (Stages 0–9) | Includes exit checks and post-clone. |
| CI Class Manager bread crumbs | §4 + Appendix B | Hierarchy, Class Info tabs, class creation 10-step flow, Dynamic IRE, limitations. |
| Avoiding duplicates | §6.1–6.7 | Decision tree, thresholds, design checklist, anti-patterns, error codes. |
| Insert vs update | §1.4, §5.2, §6.1, §6.5 | sys_id → source key → rule match → reconcile → commit; worked examples. |
| Verification/troubleshooting | §7 | Run-level, CMDB-level, triage table. |
| Operations | §8 | 10-day pilot, weekly/monthly cadence, change control. |
| Decision support | §9 | 12 scenario recommendations. |

## 3. Source verification method

1. Located the Zurich en-US maps via `GET /docs/api/khub/maps`.
2. Pulled TOCs for ITOM and Platform Capabilities maps.
3. Extracted 59 topics to `research/*.md` with source URL and release.
4. Cross-checked each high-risk claim against at least one topic:
   - duplicate thresholds → `Detecting duplicate CIs` + `Properties related to remediation…`
   - oldest-duplicate behaviour → `Detecting duplicate CIs` ("oldest of the duplicate CIs is picked")
   - lookup records inserted → `Identification rules` ("If the lookup records don't already exist, then they are inserted")
   - 90-day partial retention → `Identification and Reconciliation engine (IRE)`
   - Dynamic IRE scope/patch → `Dynamic IRE`
   - deletion strategy exceptions → `CI deletion strategies for pattern discovery`
5. Kept extracted source HTML-to-text conversion separate from synthesis so a claim can be re-checked.

## 4. External review (local models)

Real parallel run: `nvidia_v4_swarm/runs/20261113T090332Z/`.

| Model | Status | Tokens in/out | Accepted findings | Rejected findings |
|---|---|---|---|---|
| `qwen2.5-coder:7b` | ok | 3036/725 | Duplicate-task wording could read as contradicting `skip_duplicates` → clarified in §6.2. | Claims that data-source enforcement is undocumented (it is in §5.5); generic "add more guidelines" items with no concrete error. |
| `qwen3.5:4b` | ok (hit length cap; content empty, reasoning captured) | 3157/2500 | Version/patch sensitivity and domain/inheritance complexity are real risks → already covered, expanded in QA caveat. | Claim that IRE does not insert missing lookup records — contradicted by `Identification rules`; claim that "oldest duplicate" is unverified — contradicted by `Detecting duplicate CIs`; claim that 90-day retention is unverified — contradicted by the IRE topic. |

Full outputs: `nvidia_v4_swarm/runs/20261113T090332Z/*/05_FINAL/MODEL_REVIEW.md`.

**Disposition rule:** a local model's objection is accepted only if the primary source
supports it. Model output was not pasted into the reference as fact.

## 5. Cloud wrapper verification

| Provider | Result | Evidence |
|---|---|---|
| Ollama `qwen3.5:4b` | **PASS** (88.2 s, 3157/2500 tokens) | Run folder. |
| Ollama `qwen2.5-coder:7b` | **PASS** (32.8 s, 3036/725 tokens) | Run folder. |
| DeepSeek `deepseek-chat` | **PASS** (16 tokens, $0.000008) | `research/cloud_wrapper_smoke_test.md`. |
| Groq `openai/gpt-oss-120b` | **PASS after fix** | Cloudflare 1010 blocked default urllib UA; browser UA added. Original model id was unavailable; verified `/models` and updated roster. |

## 6. Verification commands run

```bash
python3 -m py_compile nvidia_v4_swarm/usage_tracker.py \
  nvidia_v4_swarm/llm_client.py nvidia_v4_swarm/run_swarm.py   # PASS
python3 nvidia_v4_swarm/run_swarm.py --dry-run                  # PASS
python3 nvidia_v4_swarm/run_swarm.py --max-parallel 2           # PASS, 2/2 ok
python3 nvidia_v4_swarm/usage_tracker.py --status               # PASS, inflight 0
```

## 7. Known limitations

- Zurich only; no live-instance screenshots or field-level validation.
- No Service Mapping top-down depth.
- Cloud discovery provider matrices are summaries.
- Plugin IDs for entitlement are not asserted.
- Local review models are small; they were used for gap-finding only.
- `qwen3.5:4b` returned empty `content` with text in `reasoning`; the runner records this
  explicitly and does not treat it as a clean answer.

## 8. Verdict

**PASS** against the plan's success criteria, with the limitations above. The reference is
safe to use as a design/checklist document; validate instance-specific defaults and UI
paths in a sub-production Zurich instance before production changes.
