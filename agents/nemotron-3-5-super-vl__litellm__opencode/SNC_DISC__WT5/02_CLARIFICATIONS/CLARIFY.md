# Clarifications / requests — nemotron-3-5-super-vl__litellm__opencode

**Capability gate:** PASS

## Questions for the orchestrator
- None.

## Assumptions
- "Thorough" = configuration surface + processing order + CI Class Manager locations + duplicate/insert-update controls.
- ServiceNow release-agnostic unless a source pins a release.
- The LiteLLM proxy on :4000 serves free NVIDIA nemotron models; if the upstream rotates to a reasoning model,
  `max_tokens >= 3000` is required or content comes back empty.

## Model / provider declaration (for agent-mix transparency)
- **Model:** `nvidia/nemotron-3.5-super-vl-120b-a12b`
- **Provider:** `litellm` (LiteLLM rotating proxy on `http://localhost:4000/v1`)
- **API key:** placeholder `"anything"` (LiteLLM accepts placeholder; real auth per-upstream from `~/dbpasses.txt`)
- **Upstream group:** `ULTRA_FREE_NVIDIA` (may rotate to other free NVIDIA nemotron variants)
