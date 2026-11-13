# Plan — SNC_DISC_RESEARCH

**Agent:** `deepseek-v4-pro__deepseek__kilo`
**Model / provider:** `deepseek-v4-pro` / `deepseek` (DeepSeek API)
**Worktree:** `/home/eaguiar2015/wt-deepseek-v4-pro__deepseek__kilo` → folder `agents/deepseek-v4-pro__deepseek__kilo/SNC_DISC__WT1`

## Goal

Produce as thorough a technical reference as possible on **ServiceNow Discovery configuration**:

1. configuration options & properties,
2. order of operations (the Discovery phases),
3. the key bread crumbs under **CI Class Manager**,
4. the configuration that **prevents duplicate CIs** and governs **insert vs update** of CMDB records.

Crucially this must cover the four IRE control surfaces a domain expert expects:
**identification rules**, **reconciliation rules**, **IRE data source rules**, and **data refresh rules**.

## Output format

- `05_FINAL/DISCOVERY_CONFIG_REFERENCE.md` — markdown, headed sections, every claim carrying a source URL or `UNVERIFIED`.
- `04_QA/QA.md` — self-scoring against the success criteria.
- `05_FINAL/FINAL_SUMMARY.md` — goal met? blockers? clarifications?
- `research/` — raw search digests + downloaded official docs (`research/official_docs/*.md`).

## Phases

1. **Capability gate** — can I browse? is context enough? → `00_PREREQ/PREREQ.md`
2. **Research** — 10 focused search→digest passes + 13 official docs downloaded from the ServiceNowDocs GitHub mirror
3. **Synthesis** — write the reference from evidence only
4. **QA** — topic/coverage/citation self-check
5. **Final summary** — blockers + clarifications

## Risks

- `docs.servicenow.com` is a JS SPA → mitigated by the `ServiceNow/ServiceNowDocs` GitHub markdown mirror.
- Search throttling → mitigated by DDG→Startpage→Brave fallback in the harness.
- Release drift: docs are `brazil` release (2026-09/10); UI paths may differ slightly on older releases — flagged in the reference.

## Success criteria

- Covers all 4 IRE control surfaces + Discovery config options + order of operations + CI Class Manager locations.
- Every non-trivial claim has a URL, or is explicitly UNVERIFIED.
- Names the exact CI Class Manager / navigator locations it claims.
- States blockers honestly instead of inventing content.
