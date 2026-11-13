# ServiceNow Discovery — end-to-end configuration research

**Agent:** `inkling-2-small__openrouter__kilo`
**Model:** `openrouter/thinkingmachines/inkling-2-small:free` (Thinking Machines, free tier)
**Provider:** OpenRouter · **Harness:** Kilo
**Date:** 2026-11-13 · **Release pin:** Australia (docs updated 2026-03-12 unless page says otherwise)
**Method:** raw article HTML fetched from the servicenow.com docs Fluid Topics khub API
(`POST /docs/api/khub/topics/search` + `GET /docs/api/khub/maps/<mapId>/topics/<contentId>/content`),
family filter = `australia`. DuckDuckGo/Bing were tested and rejected (anomaly challenge / low yield).
Playwright verified the SPA exists; guessed paths 404 — all URLs in the guide come from search results, never memory.

## Contents
| file | what it is |
|---|---|
| `DISCOVERY_END_TO_END_GUIDE.md` | the guide: setup order → scanning → classification → identification → exploration → CMDB write; full property catalog; IRE; duplicates; source precedence; troubleshooting |
| `sources/` | raw `.html` + stripped `.txt` of every source cited (numbered [1]–[28] in the guide; search-result JSONs kept in the agent worktree, not here) |

## How to verify / reproduce
Every guide section cites `[n]` → see "Source index" at the bottom of the guide, URLs point at the live Australia docs. `.txt` files are the exact retrieved content on 2026-11-13.

## Known bounds
- Instance behavior is described as documented, not executed (dry_run + identifyCI() before prod).
- Zurich/Yokohamado not diffed; identifiers/properties are stable across recent releases per the docs' own cross-release publishing.
- KB articles referenced by the docs (KB0750382/83/86, KB0756709, KB1542272) need Now Support access — not opened.
