# Pre-requisite check — can this agent actually research ServiceNow Discovery?

**Agent:** `deepseek-flash__openrouter__kilo-cli`
**Model:** `deepseek/deepseek-flash` · **Provider:** OpenRouter (inferred) · **Harness:** Kilo CLI
**Date:** 2026-11-13T08:47Z
**Verdict: PASS with one important correction.** The agent can browse, but *not* by
fetching ServiceNow docs pages directly. The docs site is a JavaScript single-page
application (FluidTopics); direct HTTP/`webfetch` returns only the loading shell. The
working path is the site's own unauthenticated JSON API, with Playwright as the
capability proof/fallback.

## Capability matrix

| Capability | Pass? | Evidence (actually executed) | Consequence |
|---|---|---|---|
| Outbound HTTPS | **YES** | `urllib` request to `https://example.com` / ServiceNow API returned HTTP 200 | Research is possible |
| Native web fetch (`webfetch`) on docs | **NO** | Returned `Loading application... Your web browser must have JavaScript enabled` for `r_DiscoveryProperties.html` | Do not rely on naive fetch for docs |
| Playwright + Chromium installed | **YES** | Playwright 1.58.2; `~/.cache/ms-playwright/chromium-1243`; launched headless successfully | Can render if needed |
| JavaScript rendering of docs body | **NO / partial** | After clicking "Accept and Proceed", `body.innerText` was ~20 chars; the reader is hosted in a cross-origin FluidTopics frame that does not expose body text to the parent | Playwright alone is not enough |
| Discovery of docs XHR | **YES** | Captured `GET /docs/api/khub/maps/{map}/topics/{id}/content?target=DESIGNED_READER` → HTTP 200 | Use the JSON content API |
| ServiceNow khub API unauthenticated | **YES** | `/api/khub/maps` returned 1,483 maps; `/maps/{id}/pages` returned the full TOC | Reliable research path |
| Search engine via HTTP | **NO** | DuckDuckGo HTML returned a bot challenge ("Select all squares containing a duck") | Use Startpage via Playwright, or the docs search API |
| Search engine via browser | **YES** | Startpage returned 10 `servicenow.com/docs` hits for the test query | Fallback search works |
| Docs search API | **YES** | `POST /api/khub/clustered-search` with `{"query":"CI Class Manager"}` returned 457 entries | Best discovery mechanism |
| Context window adequate | **YES (empirical)** | 60 topic pages, ~350 KB of extracted text, fetched and selectively read without truncation failure; the harness does not expose a token number | Can synthesize a multi-section reference |
| Local Ollama reachable | **YES** | `qwen3.5:4b` and `qwen2.5-coder:7b` answered via `http://localhost:11434` | Can dispatch local workers |
| OpenRouter reachable | **YES** | Test call returned `OK`; 15 `:free` models listed | Can dispatch a free cloud worker |

## What failed and why it matters

1. **`webfetch` is not a browser.** ServiceNow docs are rendered client-side. A direct
   fetch returns the SPA shell, not content. Any agent that reports "I read the
   ServiceNow docs" after only using `webfetch` is likely fabricating.
2. **Playwright renders the shell but not the reader text.** The reader is a
   cross-origin `fluidtopicsclient` frame. The parent page exposes an `<h1>` but not the
   frame body. The content is loaded via the same khub API, so intercepting the network
   call or calling the API directly is the correct method.
3. **DuckDuckGo blocks bots.** Use Startpage (worked) or the ServiceNow docs search API
   (best) instead.

## Backup plan (if the API had been blocked)

Per the task instructions, the fallback chain was:

1. Use Playwright to intercept the `khub` response and save the HTML payload.
2. If JS is unavailable, ask another agent with native `web_search`/`read_url` for a
   pre-fetched evidence digest and restrict output to synthesis.
3. Never invent URLs or property names; mark unsourced claims `UNVERIFIED`.

None of the fallbacks were needed.

## Reproducible probe commands

```bash
# 1. Prove direct fetch fails (returns the SPA shell)
python3 - <<'PY'
import urllib.request
u="https://www.servicenow.com/docs/r/it-operations-management/discovery/r_DiscoveryProperties.html"
print(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent":"Mozilla/5.0"}), timeout=30).read()[:300])
PY

# 2. Prove the docs API works
curl -s "https://www.servicenow.com/docs/api/khub/maps" | head -c 200

# 3. Prove Playwright + JS
python3 -c "from playwright.sync_api import sync_playwright; p=sync_playwright().start(); b=p.chromium.launch(headless=True); print(b.version); b.close(); p.stop()"
```
