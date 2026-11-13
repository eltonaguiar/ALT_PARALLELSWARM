# 01 — Plan: SNC_DISC__WT1 (ServiceNow Discovery configuration reference)

- **Model:** `deepseek-flash` · **Provider:** `deepseek` · **Harness:** Kilo CLI
- **Worktree:** `nvidia-v4` · **Folder:** `agents/deepseek-flash__deepseek__nvidia-v4/`
- **Task:** `SNC_DISC_RESEARCH`
- **Plan written:** 2026-11-13T09:00Z

## Goal

Produce the most complete, source-grounded configuration reference possible for the
**ServiceNow Discovery** module, covering:

1. every configuration surface a Discovery admin must touch;
2. the correct **order of operations** for a greenfield setup;
3. the exact **bread crumbs inside CI Class Manager**;
4. how to **avoid duplicate CIs** and how IRE decides **insert vs update** in the CMDB;
5. verification, troubleshooting, and the risks/trade-offs of each option.

## Output format (contract)

| File | Purpose |
|---|---|
| `05_FINAL/DISCOVERY_CONFIG_REFERENCE.md` | Main deliverable. Sections 0–10, tables, property names/defaults, navigation paths, evidence map. |
| `05_FINAL/FINAL_SUMMARY.md` | Goal met? Blockers? Clarifications needed? Confidence. |
| `04_QA/QA.md` | Self-check against success criteria + coverage matrix + known gaps. |
| `02_CLARIFICATIONS/CLARIFY.md` | Questions that would change recommendations; defaults assumed. |
| `03_PHASES/phaseN_*.md` | Heartbeat per phase (so drift is visible). |
| `06_FILESCOPE/FILESCOPE.md` | Branch, worktree, files written, commands used. |
| `research/` | Raw extracted ServiceNow topics + manifest + orchestrated model output. |
| `nvidia_v4_swarm/` | Reusable free/local-model wrapper, usage tracker, parallel runner. |

Writing rules: cite the docs page for every product claim; mark judgement as
**[practitioner]**; never silently guess a UI path or default.

## Phases

| # | Phase | Exit criterion |
|---|---|---|
| 1 | Capability gate + source discovery | Working retrieval path for servicenow.com docs; no 403 dead end. |
| 2 | Corpus extraction | ≥ 50 authoritative topics captured locally with URLs. |
| 3 | Synthesis | Main reference drafted with all 5 required subject areas. |
| 4 | Adversarial QA | Gap list produced; local models review in parallel; fixes applied. |
| 5 | Package + publish | Files committed on own branch; contributor/roster rows added; no other agent's files touched. |

## Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Docs SPA blocked | No primary sources | khub API (worked). |
| Release mismatch (Zurich vs customer version) | Wrong defaults/paths | Declare Zurich everywhere; record version-sensitive items. |
| Mixing Discovery identifiers with CMDB IRE rules | Duplicate/misleading guidance | Separate "Discovery identifier" vs "CI Class Manager IRE" and cross-link them. |
| Over-generalising Dynamic IRE / CMDB 360 | Bad recommendation | Mark applicability (Hardware class only; Zurich Patch 11+). |
| Local models hallucinate | Polluted review | Use them only for gap-finding; verify every accepted point in primary docs. |
| Token blow-up from 676 KB corpus | Truncation | Grouped reading; extract facts into notes; never paste whole corpus into a prompt. |

## Success criteria (measurable)

- [ ] 5/5 required areas covered: configuration options, order of operations, CI Class
      Manager bread crumbs, duplicate avoidance, insert-vs-update.
- [ ] ≥ 25 named system properties with type + default.
- [ ] ≥ 15 exact navigation paths.
- [ ] All 4 horizontal-discovery phases explained, including where IRE enters.
- [ ] Identification-rule variants (regular/lookup/hybrid, independent/dependent,
      identifier vs related entries) explained with consequences.
- [ ] Static vs dynamic reconciliation, data source rules, data refresh rules covered.
- [ ] Duplicate lifecycle: detection → task → main CI → remediation → properties.
- [ ] Every claim traceable to `research/` or explicitly marked [practitioner].
- [ ] One command reproduces the extraction; one command runs the local-model swarm.

## Orchestration plan (after my own attempt)

1. Build `nvidia_v4_swarm/usage_tracker.py` (SQLite, per-provider inflight/daily caps/cost).
2. Build `nvidia_v4_swarm/llm_client.py` (OpenAI-compatible; Ollama + 6 free/paid clouds).
3. Build `nvidia_v4_swarm/run_swarm.py` (parallel workers, phase files, transcript capture).
4. Run 2 local Ollama models in parallel on a QA/gap task; capture real output.
5. Fold only verified findings into `05_FINAL`; record rejected suggestions.

## Non-goals

- Replacing ServiceNow product documentation.
- Instance-specific tuning without discovery data.
- Service Mapping top-down configuration depth (covered only where it shares IRE/Discovery).
