# SNC_DISC_RESEARCH — Task Final Summary

**Date:** 2026-11-13 · **Framework:** ALT_PARALLELSWARM · **Lead:** `kilo-ernie-5.5-flash`

## Goal
Most thorough practical documentation on ServiceNow Discovery: configuration options,
order of operations, CI Class Manager bread-crumbs, and the configuration governing
duplicate avoidance + CMDB insert/update.

## Status: ACHIEVED
The combined report is at:
`worktrees/WT1_kilo-ernie-5.5-flash/files/COMBINED_REPORT.md`

## Who did what
| WT | Model / provider | Section | Result |
|----|------------------|---------|--------|
| WT1 | `kilo-ernie-5.5-flash` (Baidu, Kilo gateway) | Lead: config options, order of operations, CI Class Manager, de-dup; integration | ✅ |
| WT2 | `openrouter/meta-llama/llama-3.3-70b-instruct` | CI Class Manager | ✅ |
| WT3 | `gemini/gemini-2.5-flash` | Duplicate avoidance | ✅ |
| WT4 | `deepseek/deepseek-chat` | IRE deep-dive | ✅ |
| WT5 | `mistral/open-mistral-nemo` | CMDB insert/update behaviour | ✅ |

## What worked
- Capability probe correctly gated models (15/25 reachable).
- UsageTracker enforced per-provider concurrency + daily caps across all calls.
- Task-first prompting + real task text (fixed `prompt`/`goal` bug) aligned peers to their assignments.
- Rate-limit / CoT-leak failures were caught and re-routed without losing the run.

## Blockers / clarifications
- **No live ServiceNow instance** — deliverable is documentation-grade; UI labels/defaults flagged `[verify on instance]`.
- **Release drift** — menu labels vary; table-name targets are the stable fallback.
- **Local small models** were too weak for polished sections; escalated to free API models.

## Process findings (for the framework)
1. Read the **task text** field the config actually uses (`goal` vs `prompt`) — a silent empty prompt makes models summarize context.
2. Put the **task before** the reference context, or models anchor on the context.
3. **Strip reasoning** from CoT models before writing deliverables.
4. Keep a **fallback provider** per worktree (Groq 429 → OpenRouter; Cerebras CoT → OpenRouter).

## Artifacts
- Framework: `swarm/` (router, tracker, probe, worktree manager, orchestrator).
- Docs: `docs/MODEL_REGISTRY.md`, `docs/ORCHESTRATION.md`, `docs/API_WRAPPERS.md`, `docs/agents/kilo-ernie-5.5-flash.md`.
- Probe: `swarm/probe.json`. Plan: `_PLAN/*`. Run state: `_ORCHESTRATION/phase_state.json`.