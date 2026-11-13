# Pre-requisite check — inkling-2-small__openrouter__kilo

Model: `openrouter/thinkingmachines/inkling-2-small:free` (Thinking Machines Inkling 2 Small, free tier via OpenRouter)
Provider: OpenRouter (`https://openrouter.ai/api/v1`)
Harness: Kilo (CLI agent, tool use: read/write files, bash, webfetch, Playwright via Chromium)
Date: 2026-11-13T08:52Z

| capability | verdict | evidence |
|---|---|---|
| Outbound HTTP | YES | curl → https://www.google.com HTTP 200 (0.21s); docs.servicenow.com 200 |
| Web search | PARTIAL | DuckDuckGo serves anomaly/challenge page to curl (67 "anomaly" markers); Bing returns parseable results (base64 `u=` redirect links, 10/query); SerpApi-free route chosen **but superseded** by native docs API below |
| Native docs API (key finding) | **YES, THE WIN** | servicenow.com/docs is a client-side Fluid Topics SPA. `GET /docs/api/khub/topics/search` + `GET /docs/api/khub/maps/<mapId>/topics/<contentId>/content` return search JSON and **raw article HTML** — no JS rendering needed. ~10–60 KB per page |
| Playwright + Chromium | YES | v1.58.2, chromium-1243 present; rendered docs SPA (cookie banner + "Page not found" for guessed path → real path discovery must go through search API, not guessed URLs) |
| JS rendering | YES | render/sniff scripts worked (`.tmp_snc_*.mjs` during probe, deleted after) |
| Context window | **UNKNOWN / ASSUME SMALL** | Model name says "small"; no local config exposes the limit. Working assumption ≤32k effective. Consequence: read sources in chunks, persist digests to disk, never hold >3 pages in context at once |
| Code execution | YES | bash, python3, node 22 |
| Concurrency plan | YES | reuse `shared/budget.py` (fcntl ledger) + my own `swarm/free_keys.py` for busy/inflight + per-key daily caps |

## Verdict

**CAN proceed.** The key unlock is that ServiceNow docs are scrapeable raw via the Fluid Topics
khub content API — better than Playwright (no 64-cookie banner, no SPA boot, diffable HTML).
Search result count for "discovery properties" is 58,128 across releases — I will pin **Australia**
(the current Australia IT Operations Management bundle, per search ordering) and note release deltas.

## Backup plan if blocked
- Fetch another agent's committed evidence digest (`deepseek-v4.1-flash-fast__freebuff__buffy/research/EVIDENCE_DIGEST.md`) — read-only, allowed by CONTRIBUTORS (never edit, never copy claims without checking).
- Mark anything unverified as UNVERIFIED in the final doc.
- Ask on clarifications channel; do not fabricate URLs.

## Risks entering research
- Pages may differ by release; I pin Australia and link zurich/yokohama twins where found.
- khub API is undocumented/internal — may change; digests are saved to `research/raw/` so the work is reproducible offline.
