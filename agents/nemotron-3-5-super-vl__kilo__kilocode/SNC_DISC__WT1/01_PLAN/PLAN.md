# Plan — SNC_DISC_RESEARCH

**Agent:** `nemotron-3-5-super-vl__kilo__kilocode`
**Model / provider:** `nvidia/nemotron-3.5-super-vl-120b-a12b` (nemotron-3.5-super-vl) via **`kilo`** (Kilo Gateway)
**API base:** `https://integrate.api.nvidia.com/v1` (NVIDIA NIM), bearer `NVIDIA_API_KEY`
**Worktree:** `/home/eaguiar2015/wt-nemotron-3-5-super-vl__kilo__kilocode` → folder `agents/nemotron-3-5-super-vl__kilo__kilocode/SNC_DISC__WT1`
**Branch:** `agent/nemotron-3-5-super-vl__kilo__kilocode`

## Goal

Produce as thorough a technical reference as possible on **ServiceNow Discovery configuration**:
- configuration options and properties,
- order of operations when a device is discovered,
- the key bread crumbs under **CI Class Manager** (identification, reconciliation, classification),
- configuration that prevents **duplicate CIs** and governs **insert vs update** of CMDB records.

Everything must be evidence-backed: every non-trivial claim carries a source URL or is explicitly marked `UNVERIFIED`.

## Output format

`05_FINAL/DISCOVERY_CONFIG_REFERENCE.md` — markdown, headed sections, every factual claim carrying a source URL or marked `UNVERIFIED`.
Plus:
- `04_QA/QA.md` — self-scoring against the success criteria
- `05_FINAL/FINAL_SUMMARY.md` — goal met? blockers? clarifications?
- `06_FILESCOPE/FILESCOPE.md` — files written, branch, worktree path

## Phases (heartbeats dropped in 03_PHASES/)

1. **Capability gate** — can I browse? playwright? is my context enough? → `00_PREREQ/PREREQ.md` [DONE]
2. **Plan** — this document (`01_PLAN/PLAN.md`) [DONE]
3. **Clarifications** — what I need from others / whether blocked → `02_CLARIFICATIONS/CLARIFY.md`
4. **Research** — 3 targeted passes via shared `research_harness.py`:
   - q1_config: Discovery config options/properties + order of operations
   - q2_classmgr: CI Class Manager bread crumbs (identification/reconciliation)
   - q3_dupes: duplicate prevention + insert vs update in CMDB
5. **Synthesis** — write `DISCOVERY_CONFIG_REFERENCE.md` from evidence only
6. **QA** — coverage + citation check → `04_QA/QA.md`
7. **Final summary** → `05_FINAL/FINAL_SUMMARY.md`

## Risks

- Official `docs.servicenow.com` is bot-walled for headless browsers → prefer `support.servicenow.com` KB and community.
- Search engines throttle (DDG/Bing) → harness falls back to a real-browser Startpage/Brave query.
- Free/NVIDIA-NIM model may lose tool discipline → answer must be built from the evidence digest, not memory.
- Nemotron-3.5-Super-VL is a reasoning model; tool-call output must be validated (the harness text-fallback parser covers `research()`/`answer()` text emissions).

## Success criteria

- Covers ≥5 of these topic areas: configuration_options, order_of_operations, ci_class_manager, duplicates, insert_vs_update, identification, reconciliation, mid_server
- Every non-trivial claim has a URL, or is explicitly UNVERIFIED
- Names the CI Class Manager locations it claims
- States blockers honestly instead of inventing content

## Capability verdict

CAN browse and research independently. No backup evidence required.
