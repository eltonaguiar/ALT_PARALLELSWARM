# Orchestration report — SNC_DISC_RESEARCH (alt-swarm)

Generated: 2026-11-13T09:05:32+00:00
Roster: `SNC_DISC_RESEARCH` · agents: 3 · max_parallel: 3 · wall time: 88.6s

| agent | model | provider | QA | words | finish | branch | push |
|---|---|---|---|---|---|---|---|
| `particle-1__openrouter__alt-swarm` | `particle-ai/particle-1:free` | `openrouter` | PASS | 1328 | `stop` | `agent/particle-1__openrouter__alt-swarm` | ok |
| `qwen2.5-coder-7b__ollama__alt-swarm` | `qwen2.5-coder:7b` | `ollama` | PASS | 671 | `stop` | `agent/qwen2.5-coder-7b__ollama__alt-swarm` | ok |
| `qwen3.5-4b__ollama__alt-swarm` | `qwen3.5:4b` | `ollama` | PASS | 1266 | `stop` | `agent/qwen3.5-4b__ollama__alt-swarm` | ok |

## Per-agent notes

### `particle-1__openrouter__alt-swarm`

- Worktree: `/tmp/kilo/wt-particle-1__openrouter__alt-swarm`
- Folder: `agents/particle-1__openrouter__alt-swarm/SNC_DISC__WT4/`
- Evidence-limited draft: `05_FINAL/CI_CLASS_MANAGER_BREADCRUMBS.md`
- Usage: `{'prompt_tokens': 3291, 'completion_tokens': 3897, 'total_tokens': 7188, 'cost': 0, 'is_byok': False, 'prompt_tokens_details': {'cached_tokens': 3072, 'cache_write_tokens': 0, 'audio_tokens': 0, 'video_tokens': 0}, 'cost_details': {'upstream_inference_cost': 0, 'upstream_inference_prompt_cost': 0, 'upstream_inference_completions_cost': 0}, 'completion_tokens_details': {'reasoning_tokens': 1754, 'image_tokens': 0, 'audio_tokens': 0}}`

### `qwen2.5-coder-7b__ollama__alt-swarm`

- Worktree: `/tmp/kilo/wt-qwen2.5-coder-7b__ollama__alt-swarm`
- Folder: `agents/qwen2.5-coder-7b__ollama__alt-swarm/SNC_DISC__WT3/`
- Evidence-limited draft: `05_FINAL/DUPLICATE_PREVENTION.md`
- Usage: `{'prompt_tokens': 3656, 'completion_tokens': 963, 'total_tokens': 4619}`

### `qwen3.5-4b__ollama__alt-swarm`

- Worktree: `/tmp/kilo/wt-qwen3.5-4b__ollama__alt-swarm`
- Folder: `agents/qwen3.5-4b__ollama__alt-swarm/SNC_DISC__WT2/`
- Evidence-limited draft: `05_FINAL/CONFIG_OPTIONS_AND_ORDER.md`
- Usage: `{'prompt_tokens': 3883, 'completion_tokens': 1940, 'total_tokens': 5823}`

## Read this correctly

These are **independent, evidence-constrained drafts**, not authoritative
research. Each worker had no browser and no shell; it received a pre-fetched
digest produced by the orchestrator. Automated QA checks length, structure, and
citations, not factual truth. The orchestrator's primary reference
(`SNC_DISC__WT1/05_FINAL/DISCOVERY_CONFIG_REFERENCE.md`) is the synthesis to trust.
