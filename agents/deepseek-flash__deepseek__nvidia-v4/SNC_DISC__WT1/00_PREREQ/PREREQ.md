# 00 — Prerequisites / capability gate

- **Model:** `deepseek-flash` · **Provider:** `deepseek` · **Harness:** Kilo CLI
- **Worktree:** `nvidia-v4` · **Branch:** `agent/deepseek-flash__deepseek__nvidia-v4`
- **Timestamp:** 2026-11-13T08:55Z

## Questions the brief asks

| Question | Answer | Evidence |
|---|---|---|
| Can I browse the web? | **Yes** — `webfetch` works for ordinary pages; for ServiceNow docs, the SPA needs the khub API (below). | Fetched ServiceNow khub JSON + 59 topic pages. |
| Do I have browse tools? | **Yes** — `webfetch`, Python `requests`, `curl`. | `research/source_manifest.json` |
| Can I use Playwright? | **Yes, installed**, but ServiceNow docs returned repeated **HTTP 403** on Fluid Topics assets even after accepting cookies. Playwright is useful for other JS sites, not this one. | `pw_test.py` run: title loaded, body 32 chars, 10+ 403s. |
| Is my context window large enough? | The harness does not expose a numeric window. I kept the working corpus to **~676 KB** of extracted docs and read it in grouped slices; the final reference is ~40 KB. No truncation-related failures occurred. | This run. |
| Can I reach authoritative sources? | **Yes, via the Fluid Topics khub API**: `GET /docs/api/khub/maps` → `/maps/{id}/toc` → `/maps/{id}/topics/{contentId}/content`. This returns the rendered topic HTML. | `research/source_manifest.json`, 59 captured topics. |

## Working retrieval recipe (reusable)

```bash
BASE=https://www.servicenow.com/docs
# 1. list maps (1,483); pick Zurich en-US ITOM map guxhDnVk8OUAJKLm7WZsYA
curl -s -H 'Accept: application/json' -H "Referer: $BASE/" "$BASE/api/khub/maps" > maps.json
# 2. table of contents
curl -s -H 'Accept: application/json' -H "Referer: $BASE/" \
  "$BASE/api/khub/maps/guxhDnVk8OUAJKLm7WZsYA/toc" > toc.json
# 3. one topic (contentId from the TOC, not tocId)
curl -s -H 'Referer: https://www.servicenow.com/docs/' \
  "$BASE/api/khub/maps/guxhDnVk8OUAJKLm7WZsYA/topics/Z62u0XqFoqASiJyZWoU9Ug/content"
```

Platform/CMDB map used for IRE, CI Class Manager, duplicates:
`zS6yb8e~gR8BPjeviYdV9g` (Zurich ServiceNow AI Platform Capabilities, en-US).

## Backup plan (what I would delegate if retrieval had failed)

1. Ask a sibling agent with native search/reader tools to return cited excerpts.
2. Fall back to public partner/community write-ups and clearly downgrade confidence.
3. Never fill gaps with unmarked invention; mark unknowns as open questions.

Retrieval succeeded, so the backup was not needed.

## Verdict

**Go.** Full primary-source research is possible. Constraints: Zurich release only,
English only, no logged-in instance screenshots. Those are stated in the final summary.
