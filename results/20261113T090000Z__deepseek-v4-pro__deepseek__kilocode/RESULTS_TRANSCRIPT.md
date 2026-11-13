# Results + Transcript — SNC_DISC_RESEARCH

- **Date-time (UTC):** 2026-11-13T09:00:00Z
- **Agent name / model:** `deepseek-v4-pro`
- **Provider:** `deepseek` (DeepSeek API)
- **Harness / runtime:** Kilo
- **Repository:** `github.com/eltonaguiar/ALT_PARALLELSWARM` (folder `agents/deepseek-v4-pro__deepseek__kilo/SNC_DISC__WT1`, branch `agent/deepseek-v4-pro__deepseek__kilo`)

---

## 1. Goal

Build the most thorough possible reference on **ServiceNow Discovery configuration**:

- configuration options & properties,
- order of operations (Discovery phases),
- key bread crumbs under **CI Class Manager**,
- configuration that **prevents duplicate CIs** and governs **insert vs update** into the CMDB.

This is the shared task for the parallel swarm: each model runs in its own git worktree and drops its
plan → phases → QA → final summary so no agent drifts silently.

## 2. What I did (transcript)

1. **Inspected the existing harness.** A "Hermes" agent (`deepseek-v4-flash`) had already scaffolded the
   repo: `shared/` (orchestrate.py, agent_runner.py, prereq_probe.py, research_harness.py, budget.py, judge.py),
   a folder contract, `agents.yaml`, `CONTRIBUTORS.md`. Four agents + a `nemotron` kilo slot had already run.
2. **Created my own isolated worktree** `wt-deepseek-v4-pro__deepseek__kilo` off `main`, branch
   `agent/deepseek-v4-pro__deepseek__kilo`, folder `agents/deepseek-v4-pro__deepseek__kilo/SNC_DISC__WT1`.
3. **Capability gate** — PASS: outbound HTTP, Playwright+Chromium, JS rendering, search, native `webfetch`, 128K context.
4. **Research** — hit the blocker that `docs.servicenow.com` is a JS SPA, then pivoted to the public
   `ServiceNow/ServiceNowDocs` GitHub markdown mirror (`brazil` branch) and downloaded **13 official docs**,
   plus **3 support KB articles** and **20+ community threads** (search→digest via the shared harness + direct fetch).
5. **Synthesized** `05_FINAL/DISCOVERY_CONFIG_REFERENCE.md` (9 sections, 25 cited sources).
6. **QA** self-check — 8/8 topics + 4/4 domain-expert items, each item its own section.
7. **Built `shared/free_api_registry.py`** — a unified wrapper + catalog over ~20 free/paid keys with
   busy/daily/cost tracking integrated with `shared/budget.py`.
8. **Orchestrated 3 additional local Ollama models** (`qwen3.5:4b`, `gemma2:9b`, `phi4-mini`) via the harness.

## 3. Key findings (condensed)

**Order of operations — 4 phases** (via ECC queue + MID Server): Scanning (Shazzam/port probes) →
Classification → Identification → Exploration.

**CI Class Manager** (`All → Configuration → CI Class Manager`) houses, under **IRE**: Identification
(CI identification rule + inclusion rule), Reconciliation (CI reconciliation rule + data refresh rule),
Dependencies (dependent relationship rule). IRE data source rules live at
`All → Configuration → Identification/Reconciliation → IRE Data Source Rule`.

**Four rule families that control dedup and insert-vs-update:**

| family | what it does | table |
|---|---|---|
| Identification rules | uniquely match a CI; match → update, no match → create | (CI Class Manager) |
| Reconciliation rules | which source may update which attribute; static vs dynamic precedence | `cmdb_reconciliation_definition` / `cmdb_dynamic_reconciliation_definition` |
| IRE data source rules | block a source from *inserting* while allowing *updates* | `cmdb_ire_data_source_rule` |
| Data refresh rules | staleness window; when a lower-priority source may take over | (CI Class Manager → Reconciliation Rules → Data Refresh Rules) |

**Duplicate prevention** = strong, per-class identification rules (prefer independent, avoid lookup entries,
limit to 1 identifier entry). IRE also evaluates retired CIs and raises Duplicate CI tasks.

**Insert vs update**: identification and field-update are separate; IRE only reconciles attributes present in
the payload; no data change → no write → `sys_updated_on` unchanged; `last_discovered`/`discovery_source`
always refresh; `install_status` is not in the OOTB payload so a retired CI is not auto-reactivated.

The full reference (with canonical `docs.servicenow.com` URLs for every claim) is in
`DISCOVERY_CONFIG_REFERENCE.md` alongside this file.

## 4. Free-API-key wrapper (what I added)

`shared/free_api_registry.py`:

- Catalogs ~20 providers (Ollama, DeepSeek, OpenAI, OpenRouter, Groq, Cerebras, DeepInfra, SambaNova,
  SiliconFlow, Novita, xAI, Moonshot/Kimi, Mistral, NVIDIA NIM, GLM/Zhipu, HuggingFace, NOUS, Chutes, LLM7,
  Abacus, Gemini) — each with base_url, env-var **name** (never the key value), default models, free-vs-paid.
- `complete(provider, model, messages)` — one call that acquires a budget slot (enforcing max-inflight +
  daily calls/tokens + cost), calls `/chat/completions`, and releases the slot recording usage.
- `register_budget_defaults()` — injects caps into `shared/budget.py` so the tracker knows every provider.
- `status()` — per-provider busy/inflight, calls, tokens, cost, day.

## 5. Orchestration (locally-run models)

| agent id | model | provider | harness | branch | status |
|---|---|---|---|---|---|
| `qwen3.5-4b__ollama__kilocode` | qwen3.5:4b | ollama | kilocode | `agent/qwen3.5-4b__ollama__kilocode` | interrupted (reached research phase) |
| `gemma2-9b__ollama__kilocode` | gemma2:9b | ollama | kilocode | `agent/gemma2-9b__ollama__kilocode` | completed (QA 0/8 — 8K context → capability gate FAIL) |
| `phi4-mini__ollama__kilocode` | phi4-mini:latest | ollama | kilocode | `agent/phi4-mini__ollama__kilocode` | interrupted (reached research phase) |

Each writes its own `agents/<id>/SNC_DISC__WT<n>/` folder (PREREQ → PLAN → PHASES → QA → FINAL → FILESCOPE)
under its own branch.

**Honest outcome:** `gemma2-9b` ran the full lifecycle but scored 0/8 because its 8K context window
fails the harness capability gate (`can_browse` requires context ≥ 32K), so it answered unsourced.
`qwen3.5:4b` and `phi4-mini` reached the research phase but the run was interrupted by the busy shared
environment (concurrent agents / GPU contention) before synthesis; their partial folders + interruption
markers are on their branches. The harness `agent_runner.py` + `orchestrate.py` orchestration path itself
was demonstrated end-to-end by `gemma2-9b`.

## 6. Files produced

- **This agent:** `agents/deepseek-v4-pro__deepseek__kilo/SNC_DISC__WT1/` (10 lifecycle docs + 10 search
  digests + 13 official docs + 2 fetch drivers).
- **Shared tooling:** `shared/free_api_registry.py`.
- **This dated folder:** `results/20261113T090000Z__deepseek-v4-pro__deepseek__kilocode/`.

## 7. Blockers / clarifications

- **Blocker (worked around):** `docs.servicenow.com` is a JS SPA for both HTTP fetch and `webfetch`.
  Resolved via the `ServiceNow/ServiceNowDocs` GitHub markdown mirror.
- **UNVERIFIED (1 item):** `r_DiscoveryProperties` page itself was not rendered; its existence is cited from
  the docs index and flagged inline.
- **Clarifications needed:** none.
