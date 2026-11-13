# SWARM_REPORT — 2026-11-13T09:00Z — free-key cross-check run

Prompt (identical for all): "Context: ServiceNow Discovery writes CIs to the CMDB via the Identification and Reconciliation Engine (IRE). In <=120 words, list the controls that prevent duplicate CIs, and say whether each is a system property, an IRE rule type, or a CMDB Health/remediation feature. Be terse; bullet list."

## Results

| provider | model | 1st run | 2nd run (fixed models) | answer quality |
|---|---|---|---|---|
| gemini | gemini-2.5-flash-lite | 200, 0.96s, 189 tok | 200, 0.96s | Structure OK (ID rules / reconciliation rules / Health Dashboard); **hallucinated** `discovery.source.attribute`; missed skip_duplicates, IRE data source rules, incidentally listed "Data Certification" |
| groq | openai/gpt-oss-120b | 404 (model gone) | 200, 1.87s, 895 tok | **hallucinated** `discovery.ire.identify_by`, `discovery.ire.reconcile`; correct on rule classes |
| cerebras | gpt-oss-120b (via CEREBRAS_API_KEY; FREE variant = 401) | 401 | 200, 0.41-0.59s, 569-1033 tok | **hallucinated** `discovery.identify.unique_key`, `cmdb.uniqueness.index`; empty visible content on first run (897 reasoning tokens of 900) |
| mistral | mistral-small-latest | 429 | not retried | rate-limited; left alone |
| openrouter | google/gemma-4-31b-it:free | 404 (meta-router ok?) → 429 on retry | 429 | free pool saturated |
| ollama | qwen3.5:4b → gemma2:9b | empty (thinking blew 220-tok cap) | 200, 6.5s, 183 tok (gemma2:9b) | **hallucinated** `glide.discovery.duplicate.threshold`; control list generic |
| **subq_free** | subq-savant-1.4 | — | — | NO_KEY; wiring only |
| **subq_paid** | subq-savant-1.4 | — | — | NO_KEY; wiring only |

## Score vs docs-cited truth (DISCOVERY_CONFIG_REFERENCE.md §5)
None of the four successful answers mentioned: identifier entries + Order, `glide.identification_engine.skip_duplicates[.threshold]`, IRE **data source rules** (insert ban), process handlers, serial-number integrity, or the `duplicate_of` remediation flow. 4/4 hallucinated ≥1 property name. **Verdict: free-tier models cannot be trusted with ungrounded ServiceNow recall; they are usable only for checklist-style tasks over a provided digest.**

## Ledger snapshot (`swarm/state/swarm_ledger.json`, calls include failed attempts)
groq 2 calls/2320 tok · cerebras 3/3820 · gemini 2/2320 · mistral 2/2320 · openrouter 3/3820 · ollama 3/3820 — all `cost_usd 0.0`, `inflight 0` everywhere, day-caps at ≤3 calls each.

## Cost
$0. SubQ entries uncapped until keys exported: capped at 50 (free) / 200 (paid) calls/day, est cost tracked in ledger (`price_in_1k` 0.0001, `price_out_1k` 0.0005, cached input 0.00001).

## What I'd do next (ask before doing)
1. Export `SUBQ_FREE_API_KEY` / `SUBQ_API_KEY` and run `run_swarm.py subq_free subq_paid` against the same prompt to compare Savant 1.4 vs free tier.
2. Add a digest-in-context variant (feed EVIDENCE_DIGEST + ask for gap analysis) — that's the setup where small models should shine.
3. If pushing to a shared box again, clone per-agent (`/tmp/kilo/<repo>_<agentid>`) from the start.
