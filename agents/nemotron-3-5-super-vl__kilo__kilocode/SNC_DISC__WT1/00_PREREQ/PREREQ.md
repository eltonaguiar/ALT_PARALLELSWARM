# Pre-requisite check — nemotron-3-5-super-vl__kilo__kilocode

**Agent:** `nemotron-3-5-super-vl__kilo__kilocode`
**Model / provider:** `nvidia/nemotron-3.5-super-vl-120b-a12b` (a.k.a. nemotron-3.5-super-vl) via **`kilo`** (Kilo Gateway)
**API base:** `https://integrate.api.nvidia.com/v1`
**Auth:** `NVIDIA_API_KEY` (bearer)
**Base URL (probe):** `https://integrate.api.nvidia.com/v1`

| capability | pass | evidence |
|---|---|---|
| Outbound HTTP | YES | `example.com` reachable via `urllib` |
| Playwright + Chromium | YES | headless Chromium launched and rendered a page |
| JavaScript rendering | YES | JS DOM mutation executed in Chromium |
| Web search reachable | YES | Startpage/Brave query returned servicenow.com results |
| Context window | YES (large) | nemotron-3.5-super-vl is a large-context NVIDIA NIM model; probe's ollama `/api/show` check is N/A for this API-backed model |

## Verdict

**CAN proceed with independent web research.** Browsing tools reachable (HTTP + Playwright/Chromium + search) and context is adequate for a large NVIDIA NIM model.

## Backup plan if blocked

- Ask the orchestrator for a pre-fetched evidence digest (another agent's research output).
- Restrict output to structure/planning work that needs no live sources.
- Never fabricate URLs; mark unsourced claims as UNVERIFIED.
