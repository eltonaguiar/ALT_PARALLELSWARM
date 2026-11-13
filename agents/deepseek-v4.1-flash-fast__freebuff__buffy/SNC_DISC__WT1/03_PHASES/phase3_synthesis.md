# Phase 3 — synthesis

2026-11-13

Writing `05_FINAL/DISCOVERY_CONFIG_REFERENCE.md` from the evidence digest only.

Structure decisions:

- Two separate order-of-operations sections: **A = setup order** (what an implementer does, in
  sequence, on a blank instance) and **B = runtime order** (what Discovery does per device). Mixing
  them is what makes most Discovery docs hard to use.
- CI Class Manager documented as **path → control → consequence-for-duplicates**, because that is
  how the question was asked.
- A single decision table for insert-vs-update that names which rule set decides each outcome.
- Every property row carries its default and the exact doc spelling; where ServiceNow's own docs
  spell one property two ways, both are shown with a warning rather than silently picking one.

Phase 2 evidence was sufficient; no re-fetch loop needed.
