# PREREQ — can this agent actually do SNC_DISC__WT1?

**Agent:** `deepseek-v4.1-flash-fast__freebuff__buffy`
**Model:** `DeepSeek V4.1 Flash Fast`
**Provider:** Freebuff / Codebuff "Buffy" agent runtime (the model is served by the Freebuff client;
I did **not** call a vendor key directly, so no entry is needed in `shared/budget.py` for this run)
**Date:** 2026-11-13
**Worktree:** `SNC_DISC__WT1` (git branch `agent/deepseek-v4.1-flash-fast__freebuff__buffy`)

| capability | result | evidence / consequence |
|---|---|---|
| Outbound HTTPS | PASS | fetched `docs.servicenow.com` and `support.servicenow.com` pages directly |
| Web search tool | PASS | native `web_search` (server-side SERP + snippets) |
| Page fetch / extraction | PASS | native `read_url` returns readable text (JS-rendered doc pages extracted fine) |
| Interactive browser (Playwright/CDP) | NOT USED | no browser-driving tool in this runtime; not needed because `read_url` returned full doc bodies |
| Context window | LARGE (sufficient) | worked digest-first: evidence note per source, never page dumps |
| Shell / git | PASS | repo cloned, folders written, harness scripts executed |

## Verdict

**PASS — I can research this task independently.** No backup agent, no digest donor needed.

## Consequence for the plan

- Prefer primary `docs.servicenow.com` pages (they extracted cleanly), use
  `support.servicenow.com` KB articles for failure-mode detail, use Community only for
  corroboration (it is not authoritative).
- Because I have no browser automation, anything behind a login wall (Now Support login-gated KB,
  instance UI screenshots) is **out of reach** → those claims are tagged `UNVERIFIED` in the
  reference instead of being asserted.
