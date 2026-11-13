# Clarifications and blockers

**Agent:** `deepseek-flash__openrouter__kilo-cli`
**Status:** no blocker to the documentation goal.

## Blockers encountered (all resolved or worked around)

| Blocker | Impact | Resolution |
|---|---|---|
| ServiceNow docs are a JS SPA; `webfetch` returns only the loading shell | Direct page reading impossible | Used the docs' own khub JSON API |
| Playwright renders the shell but the reader body is in a cross-origin frame | Browser rendering did not expose body text | Same API workaround; Playwright kept as capability proof |
| DuckDuckGo HTTP bot challenge | Generic web search degraded | Startpage via Playwright + docs search API |
| OpenRouter `google/gemma-4-*:free` returned upstream 429 | First free-model worker produced no text | Switched to `particle-ai/particle-1:free`, with a `baidu/ernie-5.5-flash-preview:free` fallback |
| Free reasoning models spend most tokens on reasoning | One run produced only 183 words | Raised the token budget; added a QA-aware fallback gate |
| Provider routing not introspectable | Cannot prove OpenRouter vs. another gateway from inside the session | Declared as an evidence-based inference in `00_MODEL/MODEL_PROVIDER.md` |

## Questions for a customer-specific tuning engagement

1. **Release/patch** — Brazil is assumed. Confirm the target (e.g., Zurich/Yokohama)
   before applying UI paths or defaults.
2. **Discovery style** — probe/sensor, pattern, or both? Identification and deletion
   behavior differ.
3. **Authoritative sources** — which systems own which CI attributes? Needed for static
   reconciliation + data refresh + data-source rules.
4. **CMDB 360 / dynamic IRE** — licensed and enabled? Dynamic reconciliation requires it.
5. **Duplicate scope** — CI records only, or lookup/related items too?
6. **Domain separation** — which domain will own the rules and schedules?
7. **Scale** — IP count, device count, MID Server count, and run window. This drives
   Shazzam batch size, behaviors, and whether event processing is needed.
8. **Security** — credential store, external credentials, least-privilege MID Server
   service accounts, and whether code-signed instances are in scope.

## What I did **not** verify

- I did not log into a live ServiceNow instance. UI labels and menu paths come from the
  Brazil documentation, not from clicking through a customer instance.
- I did not test a real IRE payload against a live CMDB. The IRE behavior described is
  documented behavior, including defaults, not observed runtime behavior.
- The free-tier caps in `swarm/registry.json` are conservative operator guards, **not**
  vendor-verified limits. Verify current terms before scaling.
