# 04 — Success criteria

The swarm succeeds if the combined output (WT1..WTn) lets a ServiceNow admin, with no
other reference, do the following:

## Must-have (blocking)
1. **Enumerate Discovery's major configuration options** and where each lives (menu path).
2. **Describe the order of operations** of a Discovery run end-to-end
   (MID Server → probes/patterns → classification → IRE → CMDB write).
3. **Give CI Class Manager bread-crumbs** — the exact navigation and what each screen controls.
4. **Explain duplicate avoidance** and **insert-vs-update** behaviour into the CMDB,
   including which settings/tables drive it.
5. Every worktree has a completed `05_QA.md` and `06_FINALSUMMARY.md`.
6. Every claim that needs live verification is flagged **[verify on instance]**.

## Should-have
7. Cite the vendor doc pages used (URLs).
8. Note release-specific UI differences.
9. A single combined `files/COMBINED_REPORT.md` assembled by the lead.

## Quality bar
- No placeholder text left in final files.
- No known contradictions between worktrees.
- Free-tier usage stayed within caps (check `_ORCHESTRATION/phase_state.json → usage`).

## Definition of done
All Must-haves met AND combined report assembled AND QA/final summaries written.