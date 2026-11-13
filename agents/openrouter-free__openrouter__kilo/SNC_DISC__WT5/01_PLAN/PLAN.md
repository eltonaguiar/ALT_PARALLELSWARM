# Plan — SNC_DISC_RESEARCH

**Agent:** `openrouter-free__openrouter__kilo`
**Model / provider:** `openrouter.free` / `openrouter`
**Worktree:** `/tmp/kilo/ALT_PARALLELSWARM/agents/openrouter-free__openrouter__kilo/SNC_DISC__WT5`
**Branch:** `agent/openrouter-free__openrouter__kilo`

## Goal
Produce as thorough a technical reference as possible on **ServiceNow Discovery configuration**:
configuration options and properties, order of operations, the key bread crumbs under **CI Class Manager**, and the configuration that prevents **duplicate CIs** and governs **insert vs update** of CMDB records.

## Output format
`05_FINAL/DISCOVERY_CONFIG_REFERENCE.md` — markdown, headed sections, every factual claim carrying a source URL or marked `UNVERIFIED`. Plus `04_QA/QA.md` self-scoring and `05_FINAL/FINAL_SUMMARY.md`.

## Phases
1. **Capability gate** — can I browse? playwright? is my context enough? → `00_PREREQ/PREREQ.md` ✓
2. **Research passes** — 3 targeted searches via the shared research harness:
   - Pass 1: ServiceNow Discovery configuration options & properties
   - Pass 2: CI Class Manager bread crumbs & identification/ reconciliation rules
   - Pass 3: Duplicate CI prevention, insert vs update behaviour in CMDB
3. **Synthesis** — write the reference from evidence only
4. **QA** — coverage + citation check + topic score
5. **Final summary** — goal met? blockers? clarifications?

## Risks
- Official `docs.servicenow.com` is bot-walled for headless browsers → use `support.servicenow.com` KB articles, `developer.servicenow.com` docs, and learning.servicenow.com
- Search engines throttle (Bing/DDg) → harness falls back to redirected queries, user-agent rotation
- Free/openrouter model tool discipline → answer must be built from evidence digest, not memory
- Context 128000 tokens: digests truncated to 4–5k chars per call to stay inside it
- Duplicate rows from imprecise CMDB identification rules → verify each claim against actual configuration UI

## Success criteria
- Covers ≥5 of: configuration_options, order_of_operations, ci_class_manager, duplicates, insert_vs_update, identification, reconciliation, mid_server
- Every non-trivial claim has a URL, or is explicitly UNVERIFIED
- Names the CI Class Manager locations it claims (e.g. `cmdb_relational`, `cmdb_ci_table`, discovery-specific tables)
- States blockers honestly instead of inventing content
- Research output documented in research/ folder with timestamps