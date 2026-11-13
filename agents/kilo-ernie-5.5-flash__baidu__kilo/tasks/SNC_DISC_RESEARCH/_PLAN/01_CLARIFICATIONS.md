# 01 — Clarifications

Questions that could change the plan. Answered with sensible defaults so the swarm
doesn't stall; flagged for the human to confirm.

| # | Question | Default taken | Impact if wrong |
|---|----------|---------------|-----------------|
| C1 | Target ServiceNow release? | Washington/DC-lineage (current GA). Note where UI moved between releases. | Some menu paths differ by release. |
| C2 | Depth vs breadth? | Breadth-first with depth on the 4 priority areas. | Too shallow → expand a worktree. |
| C3 | Audience? | Configuring admins / CMDB engineers. | Exec summary would need a rewrite. |
| C4 | Need screenshots? | No — path bread-crumbs as text (`All → Discovery → ...`). | Add a Playwright pass over docs. |
| C5 | Include custom/probe authoring? | Mention only, not full tutorial. | Expand WT2 scope. |
| C6 | Reconciliation vs IRE distinction? | Cover both, clearly separated. | Merge sections. |
| C7 | Do local models have web access? | No. WT1 (this agent) does the browsing; peers get fetched snippets. | Give peers a fetch tool. |

## Blocking clarifications for the human
- Confirm target release (C1).
- Confirm whether a live instance is available for verification (out of scope today).