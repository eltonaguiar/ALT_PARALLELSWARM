# Model and provenance — read this first

| Field | Value |
|---|---|
| **Model (as reported by harness)** | `deepseek-flash` (`deepseek/deepseek-flash`) |
| **Provider** | `deepseek` (DeepSeek API / DeepSeek model family) |
| **Harness / CLI** | Kilo CLI |
| **Worktree name** | `nvidia-v4` |
| **Git branch** | `agent/deepseek-flash__deepseek__nvidia-v4` |
| **Agent folder** | `agents/deepseek-flash__deepseek__nvidia-v4/` |
| **Task worktree** | `SNC_DISC__WT1` — ServiceNow Discovery configuration research |
| **Run started (UTC)** | 2026-11-13T08:51Z |
| **Web access used** | Kilo `webfetch` + Python `requests` + Playwright/Chromium 1.65 (headless) |
| **Local orchestration used** | Ollama (`qwen3.5:4b`, `qwen2.5-coder:7b`) via `nvidia_v4_swarm/` |

## Why this folder name

The shared repo convention is `<model>__<provider>__<harness>` (see root `HARNESS.md`).
This folder is `deepseek-flash__deepseek__nvidia-v4`, i.e.:

- model → `deepseek-flash`
- provider → `deepseek`
- harness/worktree → `nvidia-v4`

It is deliberately distinct from the pre-existing `deepseek-v4-flash__deepseek__hermes`
folder (a different harness/model label) and from the local-Ollama folders.

## What is mine vs. shared

Mine (created by this run):

- everything under `agents/deepseek-flash__deepseek__nvidia-v4/`
- one row in root `CONTRIBUTORS.md`
- one `self_runs:` entry in root `agents.yaml`

Not mine, not edited: every other `agents/<id>/` folder, `shared/`, root docs except the
two additive rows above.

## Honesty notes

- The ServiceNow documentation site is a JavaScript SPA. Plain HTTP fetches return an
  8,404-byte shell, and Playwright is blocked by repeated 403s on Fluid Topics assets.
  The working path was the site's own Fluid Topics **khub** API (documented in
  `00_PREREQ/PREREQ.md` and `research/source_manifest.json`). All quoted product facts
  come from those Zurich-release pages, captured on 2026-11-13.
- Any statement marked **[practitioner]** is operational judgement, not a direct quote
  from ServiceNow docs, and should be validated in a sub-production instance.
- Local model output is labelled by model name and is **not** treated as authoritative.
