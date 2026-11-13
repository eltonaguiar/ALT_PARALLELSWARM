# Model and provider declaration

**This is a mandatory disclosure document for this folder.**

| Field | Value |
|---|---|
| Agent folder | `agents/deepseek-flash__openrouter__kilo-cli/` |
| Model ID (as reported to the session) | **`deepseek/deepseek-flash`** |
| Model family | DeepSeek |
| Routing provider | **OpenRouter** (inferred, see evidence below) |
| Harness / CLI | **Kilo CLI** |
| Session worktree | `.../.kilo/worktrees/openrouter2nd` |
| Run started (UTC) | 2026-11-13T08:46:48Z |
| Run finished (UTC) | 2026-11-13T~09:30Z |
| Task | `SNC_DISC_RESEARCH` — ServiceNow Discovery configuration reference |

## Why the provider is recorded as OpenRouter

The runtime reports the model as `deepseek/deepseek-flash`. That `vendor/model` slash
format is the OpenRouter model-ID namespace. The session environment also contains
`OPENROUTER_API_KEY` and `OPENROUTER`, and the parent worktree is named `openrouter2nd`.
The exact upstream route is **not** programmatically introspectable from inside the
session, so this is recorded as an evidence-based inference, not a vendor-verified fact.

If the operator wants a strict vendor label, record this run as:

> **DeepSeek Flash via OpenRouter, driven by Kilo CLI.**

## What this agent did itself vs. what it dispatched

1. **Self-run (native tools):** This agent performed the research and wrote the primary
   reference using Kilo's native tools: shell, Playwright Chromium, `webfetch`, and the
   ServiceNow FluidTopics JSON API. No vendor key was used for the primary document.
2. **Dispatched workers:** The same agent then used the harness in `swarm/` to run three
   parallel workers — two local Ollama models and one OpenRouter `:free` model — each in
   its own git worktree and its own `agents/<id>/SNC_DISC__WT2/` folder. See
   `ORCHESTRATION.md` in this folder for the roster and results.

## Capability summary (verified, not assumed)

| Capability | Result | Evidence |
|---|---|---|
| Outbound HTTPS | YES | ServiceNow khub API returned HTTP 200 JSON |
| `webfetch` on ServiceNow docs | **NO** for docs pages | Returns "Loading application..." because docs are a JS SPA |
| Playwright + Chromium | YES | Chromium renders the SPA shell; docs API is the reliable path |
| Search engine scraping | PARTIAL | Startpage worked; DuckDuckGo HTTP returned a bot challenge |
| ServiceNow docs JSON API | YES | `/api/khub/maps`, `/pages`, `/topics/{id}/content` |
| Context window | large enough for this task | 60 topic pages (~350 KB text) were fetched and selectively read; no truncation failure observed |
| Local Ollama | YES | `qwen3.5:4b`, `qwen2.5-coder:7b` responded via `localhost:11434` |
| OpenRouter | YES | A test chat to `openai/gpt-4o-mini` returned `OK`; `:free` models listed |

## Honest limitations

- The context window size is **not** exposed by the harness; "large enough" is an
  empirical observation, not a measured token limit.
- ServiceNow's docs are versioned. All facts here are from the **Brazil** release docs
  as served on 2026-11-13. UI labels can differ in older releases (Xanadu/Yokohama/Zurich).
- The docs API is an internal, undocumented API. It worked unauthenticated on this date;
  it may change. The reproducible fallback is Playwright rendering, which only gets the
  SPA shell, so the API is the practical path.
