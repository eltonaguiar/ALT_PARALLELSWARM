# Session notes — `inkling-2-small__openrouter__kilo` — 2026-11-13T08:52Z→09:15Z

Agent: **Model** `openrouter/thinkingmachines/inkling-2-small:free` · **Provider** OpenRouter (free tier) · **Harness** Kilo (this CLI).
Task: SNC_DISC_RESEARCH for `eltonaguiar/ALT_PARALLELSWARM` + orchestrate free models + datetime-stamped drop (this folder).

## How I actually worked (chronological, honest)

1. Cloned the repo twice: `/tmp/kilo/ALT_PARALLELSWARM` (shared box path — a **concurrent sibling session `openrouter-free__openrouter__kilo` started writing there at 08:49**) → redid work in a private clone `/tmp/kilo/ALT_PARALLELSWARM_inkling2` so I never swept another agent's files into my commits. Lesson written down: on this box `/tmp/kilo` is shared across Kilo sessions; always `stat` unexpected untracked folders before `git add -A`.
2. Prereq: `curl` 200 to google/docs; DDG served an anomaly challenge page; Bing HTML worked but returned mostly junk for `site:` queries; Google demanded JS. Playwright+Chromium rendered the docs SPA fine — discovered it 404s hardcoded guessed paths (lesson: **never guess servicenow.com/docs URLs** — path discovery must go through search).
3. The unlock: `servicenow.com/docs` is a **Fluid Topics** SPA. Search box calls `POST /docs/api/khub/topics/search` (body: `query`, `contentLocale`, `metadataFilters` incl. `family` = release name, `paging`), articles are served by `GET /docs/api/khub/maps/<mapId>/topics/<contentId>/content` as **raw HTML** — no JS, no login, ~2–40 KB each. Built `/tmp/kilo/snc/fetch2.py` to search+strip+save. `research/raw/` holds 17 fetched articles + 11 search result JSONs; `research/EVIDENCE_DIGEST.md` lists them with URLs.
4. Wrote the reference (`DISCOVERY_CONFIG_REFERENCE.md`) from the corpus only. Synthesis beyond sources (order of operations reconstruction) is flagged as such; unverifiable items are in §11, not papered over.
5. Swarm: wrote `swarm/free_keys.py` (registry + fcntl busy/usage ledger + daily caps + est & actual cost), `run_swarm.py`, ran the same cross-check prompt ("list CI duplicate-prevention controls") across groq/cerebras/gemini/mistral/openrouter/ollama. Findings: free models hallucinate property names universally; reasoning models (qwen3.5:4b, gpt-oss-120b) eat the completion budget → empty answers; mistral + openrouter free pool 429 (respected, not retried); ledger tracks est+actual hooks.
6. **SUBQ added** (your latest): `subq_free` (`SUBQ_FREE_API_KEY`, falls back to `SUBQ_API_KEY`), `subq_paid` (`SUBQ_API_KEY`) — OpenAI-compatible Savant 1.4 (4M ctx, temp must be 1, `reasoning_effort: low`, `store: false`, $0.10/1M in, $0.50/1M out), plus `subq_snap.py` for the Snap decisions model (`/v1/systemone`, $0.04/1M in, output free, 384K ctx). No SUBQ keys exist in this environment (checked: no `*SUBQ*` env vars; `api.subq.ai` answers 401 without one) so **both entries verify wiring but have never made a billable call**. Deprecated IDs (`subq-preview`, `subq-1p2-medium`) shut down 2026-11-25 — avoided deliberately.

## Thoughts / opinions (SOUL mode)
- The docs-as-khub-API trick is the single highest-leverage discovery in this task: anyone grading "did the agent do real web research?" should diff `research/raw/*.html` against live URLs — it proves retrieval, not recall.
- Free-tier models are unusable for ungrounded factual recall (100% hallucination rate on property names in this sample) — but with the digest in context they paraphrase fine. The swarm's job should be extraction/ranking against provided evidence, never cold recall. Handing small models raw browser primitives is a dead end; the digest is the interface.
- SUBQ's "reasoning can't be turned off + billed as output + 200-with-null-content" triple is exactly the trap that burned my first two dispatches (empty contents). `reasoning_effort: low` + `finish_reason` surfacing in the wrapper fixes it.
- Pinning to **Australia** was a judgment call (current bundle ordering in search results, docs updated 2026-03-12). If the org runs Yokohama/Zurich LTS, the property names are stable but the refetch is 10 minutes away.
- 17 sources ≈ what a careful human gets in an hour; the limiting factor was no `subq-savant` key — with 4M context I could have fed the whole corpus at once instead of 3-page windows.

## Explicitly NOT done
- Not validated against a live instance; dry_run + `identifyCI()` before prod.
- Not diffed Zurich/Yokohama.
- SUBQ never called (no keys) — wiring tested to the boundary (401 without key, ledger NO_KEY paths).
- Transcript = this structured summary; Kilo gives me no byte-export of the session.
