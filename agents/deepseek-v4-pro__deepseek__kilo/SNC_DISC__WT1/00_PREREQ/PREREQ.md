# Pre-requisite check — deepseek-v4-pro__deepseek__kilo

**Model:** `deepseek-v4-pro`
**Provider:** DeepSeek (`deepseek`)
**Harness:** Kilo (native tools: `webfetch`, `github_*`, shell + Playwright via `research_harness.py`)

| capability | pass | evidence |
|---|---|---|
| Outbound HTTP | YES | `example.com` HTTP 200 |
| Playwright + Chromium | YES | chromium headless launches (used by research_harness page_text fallback) |
| JavaScript rendering | YES | JS executes (SPA render path works) |
| Web search reachable | YES | DuckDuckGo HTTP + Startpage/Brave browser fallback returned results |
| Native URL fetch (`webfetch`) | YES | fetched `docs.servicenow.com`, KB + community pages directly |
| Context window | YES | `deepseek-v4-pro` — 128K tokens (assumed; model not in prereq_probe `known` map, which is why its automated probe reported `context=0`) |

## Verdict

**CAN proceed with independent web research.** Browsing reachable and context adequate.

## Key finding that changed the research method

- `docs.servicenow.com/bundle/…` **and** `www.servicenow.com/docs/r/…` are both JavaScript SPAs
  ("Loading application…") — plain HTTP fetch and `webfetch` return only the splash.
- Workaround: the official docs are mirrored **as markdown** in the public GitHub repo
  `ServiceNow/ServiceNowDocs` (branch `brazil`). I downloaded the canonical pages from
  `raw.githubusercontent.com/ServiceNow/ServiceNowDocs/brazil/markdown/…` and cite their
  `canonical_url` (docs.servicenow.com) fields in the reference.
- Community (`servicenow.com/community`) and `support.servicenow.com` KB pages are server-rendered
  and fetched directly.

## Backup plan if blocked (not needed)

- Request a pre-fetched evidence digest from a browsing agent.
- Mark unsourced claims `UNVERIFIED`; never fabricate URLs.
