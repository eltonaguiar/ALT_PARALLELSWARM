# Final summary — SNC_DISC_RESEARCH

**Agent:** `deepseek-flash__openrouter__kilo-cli`
**Model:** `deepseek/deepseek-flash`
**Provider:** OpenRouter (inferred; see `00_MODEL/MODEL_PROVIDER.md`)
**Harness:** Kilo CLI
**Run:** 2026-11-13T08:46Z → 2026-11-13T09:10Z

## Did I achieve the goal?

**Yes.** The deliverable is a thorough, source-cited ServiceNow Discovery
configuration reference (Brazil release) covering the requested areas:

- configuration options with exact property names/defaults;
- canonical order of operations with exit checks;
- key CI Class Manager breadcrumbs, roles, tabs, and child-class wizard order;
- duplicate prevention and insert-vs-update behavior in the CMDB;
- validation, risks, and clarifications.

## Evidence of work

| Metric | Value |
|---|---|
| ServiceNow docs topics fetched | **68** |
| Documentation maps used | 2 (`itom`, `platform capabilities`) |
| Primary reference sections | 12 |
| Named properties/defaults in reference | 30+ |
| Worker models dispatched | 3 (2 local Ollama, 1 OpenRouter free) |
| Worker worktrees/branches | 3 / 3 |
| Worker QA passes | 3 / 3 |
| Final swarm wall time | 88.6 s |
| Free-tier spend recorded | **$0.00** |

## What was built beyond the reference

1. `swarm/usage_tracker.py` — file-locked ledger enforcing `max_inflight`,
   `daily_calls`, `daily_tokens`, and recording cost per provider. Keys are never
   stored, only the env-var name and a fingerprint.
2. `swarm/router.py` — one OpenAI-compatible interface for Ollama, OpenRouter, Groq,
   Cerebras, Gemini, Mistral, and DeepSeek, with retry/backoff.
3. `swarm/worktree_manager.py` — one git worktree + branch per agent, scaffolds the
   phase folder contract, commits only that agent's folder.
4. `swarm/agent_runner.py` — prereq → plan → phases → evidence digest → model call →
   QA → final → filescope, with a **QA-aware fallback gate**.
5. `swarm/orchestrator.py` — bounded parallel dispatch and an aggregate report.

## Blockers encountered

- ServiceNow docs are a JS SPA; direct fetch and Playwright body extraction failed.
  Resolved by using the docs' unauthenticated FluidTopics khub API.
- OpenRouter `google/gemma-4-*:free` returned upstream **429** on the large prompt.
  Resolved by switching to `particle-ai/particle-1:free` with a Baidu ERNIE fallback.
- Free reasoning models can consume the entire token budget on reasoning. Resolved by
  raising the budget and adding a QA-aware retry/fallback path.

No unresolved blocker.

## Clarifications needed

See `02_CLARIFICATIONS/CLARIFY.md`. For production, the important ones are: target
release, probe vs. pattern discovery, authoritative sources, CMDB 360/dynamic IRE
licensing, duplicate scope, domain separation, and scale.

## Honest limitations

- Not tested against a live ServiceNow instance; UI paths are from Brazil documentation.
- IRE behavior is documented behavior, not observed runtime behavior.
- Provider routing is inferred (OpenRouter), not introspected.
- Worker drafts are independent and evidence-limited; the coder draft has one known
  imprecision (data-source rules vs. reconciliation authority), flagged in QA.

## Where to read

1. `05_FINAL/DISCOVERY_CONFIG_REFERENCE.md` — the deliverable.
2. `04_QA/QA.md` — scoring and caveats.
3. `../swarm/ORCHESTRATION.md` — parallel worker results.
4. `../../runs/2026-11-13T0846Z_deepseek-flash__openrouter__kilo-cli/REPORT.md` —
   dated report and transcript/timeline.
