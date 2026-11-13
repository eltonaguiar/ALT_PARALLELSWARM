# Fleet index — SNC_DISC_RESEARCH

Each agent ran in its own git worktree and wrote only inside its own folder,
so every branch merges without conflict. Cards below are generated from the run data.

| agent folder | model | provider | browse | internal check | private rubric | card |
|---|---|---|---|---|---|---|
| [`agents/deepseek-flash__openrouter__kilo-cli`](agents/deepseek-flash__openrouter__kilo-cli/AGENT_CARD.md) | `deepseek-flash` | openrouter | no | ?/? | ?/4 mentioned · ?/4 quality | [card](agents/deepseek-flash__openrouter__kilo-cli/AGENT_CARD.md) |
| [`agents/deepseek-v4-flash__deepseek__hermes`](agents/deepseek-v4-flash__deepseek__hermes/AGENT_CARD.md) | `deepseek-v4-flash` | deepseek | yes | 8/8 | 4/4 mentioned · 2/4 quality | [card](agents/deepseek-v4-flash__deepseek__hermes/AGENT_CARD.md) |
| [`agents/deepseek-v4.1-flash-fast__freebuff__buffy`](agents/deepseek-v4.1-flash-fast__freebuff__buffy/AGENT_CARD.md) | `deepseek-v4.1-flash-fast` | freebuff | no | ?/? | ?/4 mentioned · ?/4 quality | [card](agents/deepseek-v4.1-flash-fast__freebuff__buffy/AGENT_CARD.md) |
| [`agents/inkling-2-small__openrouter__kilo`](agents/inkling-2-small__openrouter__kilo/AGENT_CARD.md) | `inkling-2-small` | openrouter | no | ?/? | ?/4 mentioned · ?/4 quality | [card](agents/inkling-2-small__openrouter__kilo/AGENT_CARD.md) |
| [`agents/llama3.1-8b__ollama__hermes`](agents/llama3.1-8b__ollama__hermes/AGENT_CARD.md) | `llama3.1:8b` | ollama | yes | 0/8 | ?/4 mentioned · ?/4 quality | [card](agents/llama3.1-8b__ollama__hermes/AGENT_CARD.md) |
| [`agents/nemotron-3-5-super-vl__litellm__opencode`](agents/nemotron-3-5-super-vl__litellm__opencode/AGENT_CARD.md) | `nvidia/nemotron-3.5-super-vl-120b-a12b` | litellm | yes | 8/8 | ?/4 mentioned · ?/4 quality | [card](agents/nemotron-3-5-super-vl__litellm__opencode/AGENT_CARD.md) |
| [`agents/openrouter-free__openrouter__kilo`](agents/openrouter-free__openrouter__kilo/AGENT_CARD.md) | `openrouter-free` | openrouter | yes | ?/? | ?/4 mentioned · ?/4 quality | [card](agents/openrouter-free__openrouter__kilo/AGENT_CARD.md) |
| [`agents/particle-1__openrouter__alt-swarm`](agents/particle-1__openrouter__alt-swarm/AGENT_CARD.md) | `particle-1` | openrouter | no | ?/? | ?/4 mentioned · ?/4 quality | [card](agents/particle-1__openrouter__alt-swarm/AGENT_CARD.md) |
| [`agents/qwen2.5-7b__ollama__hermes`](agents/qwen2.5-7b__ollama__hermes/AGENT_CARD.md) | `qwen2.5:7b-instruct-q5_K_M` | ollama | yes | 6/8 | ?/4 mentioned · ?/4 quality | [card](agents/qwen2.5-7b__ollama__hermes/AGENT_CARD.md) |
| [`agents/qwen2.5-coder-7b__ollama__alt-swarm`](agents/qwen2.5-coder-7b__ollama__alt-swarm/AGENT_CARD.md) | `qwen2.5-coder-7b` | ollama | no | ?/? | ?/4 mentioned · ?/4 quality | [card](agents/qwen2.5-coder-7b__ollama__alt-swarm/AGENT_CARD.md) |
| [`agents/qwen3-30b-a3b__ollama__hermes`](agents/qwen3-30b-a3b__ollama__hermes/AGENT_CARD.md) | `qwen3:30b-a3b` | ollama | yes | 7/8 | ?/4 mentioned · ?/4 quality | [card](agents/qwen3-30b-a3b__ollama__hermes/AGENT_CARD.md) |
| [`agents/qwen3.5-4b__ollama__alt-swarm`](agents/qwen3.5-4b__ollama__alt-swarm/AGENT_CARD.md) | `qwen3.5-4b` | ollama | no | ?/? | ?/4 mentioned · ?/4 quality | [card](agents/qwen3.5-4b__ollama__alt-swarm/AGENT_CARD.md) |

## Folder contract (every agent)

```
agents/<model>__<provider>__<harness>/
  AGENT_CARD.md                 # this summary: model, worktree, goal, format, files
  SNC_DISC__WT<n>/
    00_PREREQ/PREREQ.md         # can I browse? playwright? context?
    01_PLAN/PLAN.md             # goal, format, phases, risks, success criteria
    02_CLARIFICATIONS/CLARIFY.md
    03_PHASES/phaseN_*.md       # heartbeat per phase
    04_QA/QA.md
    05_FINAL/DISCOVERY_CONFIG_REFERENCE.md
    05_FINAL/FINAL_SUMMARY.md
    06_FILESCOPE/FILESCOPE.md
    research/                   # raw search→digest transcripts
```

## Grading
Private rubrics live **outside** this repo (`~/.alt_parallelswarm_private/`). `shared/judge.py` refuses to score if the rubric is inside the tree, and no rubric term appears in any agent prompt. See `HARNESS.md` → Grading.
