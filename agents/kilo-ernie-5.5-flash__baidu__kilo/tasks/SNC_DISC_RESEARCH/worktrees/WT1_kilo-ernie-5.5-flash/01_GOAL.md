# Goal — WT1_kilo-ernie-5.5-flash

Produce the most thorough practical documentation on ServiceNow Discovery configuration,
sourced from vendor docs, covering:

1. **Configuration options** — the major knobs, where each lives, and what it controls.
2. **Order of operations** — the four horizontal-discovery phases end-to-end.
3. **CI Class Manager bread-crumbs** — exact navigation + what each screen controls.
4. **Duplicate avoidance & CMDB insert/update** — IRE, identifiers, reconciliation,
   and the exact properties/tables that govern them.

## Success criteria
- Every claim traceable to a ServiceNow docs page (URLs cited).
- Navigation given as literal menu paths (`All > Configuration > ...`).
- Release-specific differences noted; verify-on-instance items flagged.
- A single `files/COMBINED_REPORT.md` that integrates the peer worktrees.