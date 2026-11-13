# Plan — SNC_DISC_RESEARCH

**Agent:** `nemotron-3-5-super-vl__litellm__opencode`
**Model / provider:** `nvidia/nemotron-3.5-super-vl-120b-a12b` / `litellm` (proxy on :4000)
**Worktree:** `SNC_DISC__WT5` → folder `agents/nemotron-3-5-super-vl__litellm__opencode/SNC_DISC__WT5`

## Goal
Produce as thorough a technical reference as possible on **ServiceNow Discovery configuration**:
configuration options and properties, order of operations, the key bread crumbs under **CI Class Manager**,
and the configuration that prevents **duplicate CIs** and governs **insert vs update** of CMDB records.

## Output format
`05_FINAL/DISCOVERY_CONFIG_REFERENCE.md` — markdown, headed sections, every factual claim carrying a source URL
or marked `UNVERIFIED`. Plus `04_QA/QA.md` self-scoring and `05_FINAL/FINAL_SUMMARY.md`.

## Phases
1. **Capability gate** — can I browse? playwright? is my context enough? → `00_PREREQ/PREREQ.md`
2. **Research** — 3 targeted passes (config/order, CI Class Manager, duplicates/insert-update) via the shared harness
3. **Synthesis** — write the reference from evidence only
4. **QA** — coverage + citation check
5. **Final summary** — goal met? blockers? clarifications?

## Risks
- Official `docs.servicenow.com` is bot-walled for headless browsers → prefer `support.servicenow.com` KB and community.
- Search engines throttle (DDG/Bing) → harness falls back to a real-browser Startpage/Brave query.
- The LiteLLM proxy rotates free upstreams; a reasoning-model upstream may emit `reasoning_content` instead of `content` —
  must use `max_tokens >= 3000` or the answer comes back empty.
- Context ~1M tokens: digests are truncated to 4–5k chars per call to stay well inside it.

## Success criteria
- Covers ≥5 of: configuration_options, order_of_operations, ci_class_manager, duplicates, insert_vs_update, identification, reconciliation, mid_server
- Every non-trivial claim has a URL, or is explicitly UNVERIFIED
- Names the CI Class Manager locations it claims
- States blockers honestly instead of inventing content

## Capability verdict
CAN browse and research independently via LiteLLM proxy free tier.
