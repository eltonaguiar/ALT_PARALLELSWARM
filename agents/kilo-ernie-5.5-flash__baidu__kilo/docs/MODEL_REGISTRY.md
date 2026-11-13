# Model Registry

Catalog of every model/provider wired into the swarm, with live capability status from
`swarm/probe.json` (last probe: 2026-11-13). The router reads `swarm/registry.json`; this
doc is the human-readable mirror.

**Legend:** ✅ reachable · ⚠️ reachable but weak / leaks reasoning · ❌ unreachable (key/quota/model)

## Free API providers

| Model key | Provider | Tier | Ctx | Status | Notes |
|-----------|----------|------|-----|--------|-------|
| `groq/openai/gpt-oss-120b` | Groq | free | 128k | ✅ | Fast; needs browser User-Agent (Cloudflare 1010 otherwise). |
| `groq/openai/gpt-oss-20b` | Groq | free | 128k | ✅ | Smaller sibling. |
| `groq/qwen/qwen3.8-27b` | Groq | free | 128k | ✅ | Strong; hit per-model rate limit under load → re-routed. |
| `cerebras/gpt-oss-120b` | Cerebras | free | 128k | ⚠️ | Reasoning model; can leak CoT if token budget tight. |
| `cerebras/qwen-3.8-27b` | Cerebras | free | 128k | ⚠️ | Leaked chain-of-thought into content — rejected for deliverables. |
| `mistral/open-mistral-nemo` | Mistral | free | 128k | ✅ | Good general model; used for WT5. |
| `mistral/mistral-small-latest` | Mistral | free | 32k | ❌ | 429 rate-limited at probe time. |
| `deepseek/deepseek-chat` | DeepSeek | free/cheap | 64k | ✅ | Strong reasoning; used for WT4. |
| `openrouter/meta-llama/llama-3.3-70b-instruct` | OpenRouter | free | 128k | ✅ | Strong; used for WT2. |
| `gemini/gemini-2.5-flash` | Google | free | 1M | ✅ | Very strong, huge context; used for WT3. |
| `gemini/gemini-flash-latest` | Google | free | 1M | ✅ | Alias of latest flash. |
| `huggingface/Qwen/Qwen3.8-27B` | HF router | free | 128k | ⚠️ | Leaks reasoning in reply. |
| `huggingface/meta-llama/Llama-3.1-8B-Instruct` | HF router | free | 128k | ✅ | 8B; decent. |
| `nous/baidu/ernie-light-dt-1.0-intl` | Nous | free | 32k | ⚠️ | Returns reasoning-style text; usable but noisy. |
| `llm7/L3-8B-Lunaris-v1-Turbo` | LLM7 | free | 8k | ❌ | 402 insufficient balance. |
| `llm7/anthropic/claude-haiku-5-5` | LLM7 | free | 200k | ❌ | Model unavailable. |
| `chutes/deepseek-ai/DeepSeek-V3.2-TEE` | Chutes | free | 64k | ❌ | 402 quota exceeded ($0 balance). |
| `kimi/moonshot-v1-8k` | Moonshot | free | 8k | ❌ | 401 incorrect key. |
| `openai/gpt-4o-mini` | OpenAI | paid | 128k | ❌ | 429 no credits. |

## Local (Ollama — no key, no cost)

| Model key | Ctx | Status | Notes |
|-----------|-----|--------|-------|
| `ollama/qwen2.5:7b` | 32k | ✅ | Fast, decent. |
| `ollama/qwen2.5-coder:7b` | 32k | ✅ | Fast; first-pass output unfocused. |
| `ollama/llama3.2:3b` | 128k | ⚠️ | Small; produced generic summaries (first pass). |
| `ollama/gemma2:9b` | 8k | ⚠️ | Slow-ish; first-pass output unfocused. |
| `ollama/deepseek-r1:32b` | 64k | ✅ | Strong reasoning but slow (~3-4 min); leaked CoT in first pass. |
| `ollama/qwen3.5:35b-a3b` | 32k | ⚠️ | Slow (~34s ping); reasoning-style output. |

## Capability gate

`python -m swarm.capability_probe --all` writes `swarm/probe.json`. The orchestrator reads it
and **skips any worktree whose model is not `ok`** (marked `skipped-unreachable`), so the swarm
never burns tokens on a dead key or a model that can't respond.

## Selection guidance (from this run)

- **Best free general models:** `gemini/gemini-2.5-flash`, `openrouter/meta-llama/llama-3.3-70b-instruct`, `deepseek/deepseek-chat`, `mistral/open-mistral-nemo`.
- **Avoid for clean deliverables:** reasoning/CoT models that leak thinking (cerebras qwen, HF Qwen3.8) unless the router strips reasoning.
- **Local models:** fine for coarse/offline work; escalate to a free API model for polished sections.
- **Free-tier safety:** every call passes the UsageTracker (concurrency + daily caps); a 429/quota marks the provider blocked for the run and the orchestrator degrades gracefully.