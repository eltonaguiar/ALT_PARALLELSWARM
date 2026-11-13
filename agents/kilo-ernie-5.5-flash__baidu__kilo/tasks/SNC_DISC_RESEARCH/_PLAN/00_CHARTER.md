# 00 — Charter: SNC_DISC_RESEARCH

## Task
Produce the most thorough practical documentation on **ServiceNow Discovery module
configuration options**, in this priority order:

1. **Discovery module configuration options** — every major knob, where it lives, what it does.
2. **Order of operations** — how a Discovery run actually flows (sensor → pattern → probes → IRE → CMDB).
3. **Key bread-crumbs under CI Class Manager** — where to click, what each screen controls.
4. **Configuration that avoids duplicates** and governs **insert vs update** of CIs into the CMDB.

## Why a swarm
This is a breadth task (many subsystems: MID Server, probes/patterns, CI Class Manager,
IRE, reconciliation rules, CMDB health). Splitting it across models in parallel — each
owning a slice, each with declared scope and phase markers — is faster and more auditable
than one agent serially grinding.

## Worktree split (proposed)

| WT | Model / provider | Owns |
|----|------------------|------|
| WT1 | `kilo-ernie-5.5-flash` (this agent) | **Lead + live web research**: Discovery config options + order of operations. Fetches vendor docs, writes `files/`. |
| WT2 | `ollama/qwen2.5-coder:7b` | CI Class Manager bread-crumbs & class hierarchy notes |
| WT3 | `ollama/llama3.2:3b` | Duplicate avoidance & reconciliation rules |
| WT4 | `ollama/deepseek-r1:32b` | IRE (Identification & Reconciliation Engine) deep-dive |
| WT5 | `ollama/gemma2:9b` | CMDB insert/update behaviour + health |

> Local models are knowledge-based (no live browse). WT1 supplies fetched vendor-doc
> snippets as shared context; the orchestrator injects them into each peer prompt.

## Out of scope
- Live customer-instance changes (no real ServiceNow instance access here).
- Licensing/pricing advice.
- Anything requiring a logged-in Now Platform UI session.