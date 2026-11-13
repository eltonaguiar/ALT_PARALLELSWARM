# Free API wrappers + usage tracking

Goal: safely fan work across **free-tier API keys** without tripping rate limits,
running out of daily quota, or double-spending a key across parallel worktrees.

## Providers wired in (`swarm/registry.json`)
| Key | Type | Base URL | Env var | Notes |
|-----|------|----------|---------|-------|
| `groq` | openai | api.groq.com/openai/v1 | `GROQ_API_KEY` | fast, generous free tier |
| `cerebras` | openai | api.cerebras.ai/v1 | `CEREBRAS_FREE_API_KEY` | very fast, strict concurrency |
| `mistral` | openai | api.mistral.ai/v1 | `MISTRAL_API_KEY` | |
| `openrouter` | openai | openrouter.ai/api/v1 | `OPENROUTER_API_KEY` | many free models |
| `deepseek` | openai | api.deepseek.com/v1 | `DEEPSEEK_API_KEY` | |
| `llm7` | openai | api.llm7.io/v1 | `LLM7_API_KEY_FREE` | free, no-key tier too |
| `chutes` | openai | llm.chutes.ai/v1 | `CHUTES_API_KEY_FREE` | |
| `nous` | openai | inference-api.nousresearch.com/v1 | `NOUS_API_KEY_FREE` | |
| `kimi` | openai | api.moonshot.ai/v1 | `KIMI_API_KEY` | |
| `openai` | openai | api.openai.com/v1 | `OPENAI_API_KEY` | paid — capped tight |
| `gemini` | gemini | generativelanguage.googleapis.com/v1beta | `GEMINI_API_KEY` | native API adapter |
| `huggingface` | openai | router.huggingface.co/v1 | `HUGGING_FACE_TOKEN` | |
| `ollama` | openai | localhost:11434/v1 | — (local) | no key, no cost |

> Secrets are read from the environment at call time and **never** written to disk.
> `registry.json` stores only the *variable name*.

## The router (`swarm/llm_router.py`)
One call shape for all providers:
```python
from swarm.llm_router import LLMRouter
r = LLMRouter()
out = r.chat("groq/llama-3.3-70b-versatile",
             [{"role": "user", "content": "..."}],
             temperature=0.3, max_tokens=1200)
print(out["text"], out["usage"])
```
- Translates OpenAI ↔ Gemini message formats.
- Retries 429/5xx with exponential backoff; fails fast on other 4xx.
- stdlib only (`urllib`) — no `requests` dependency.

## The tracker (`swarm/usage_tracker.py`)
File-backed, `flock()`-guarded ledger (`swarm/usage_tracker.json`, log at
`swarm/usage_log.jsonl`). Every call is bracketed:
```
can_start(provider)  → acquire(provider)  → chat()  → record(...)  → release(provider)
```
Per provider it enforces:
- **concurrency** cap (`max_concurrent`) — prevents hammering a free key in parallel.
- **daily requests** cap (`max_requests_per_day`).
- **daily tokens** cap (`max_tokens_per_day`).
- **daily cost** cap (`max_cost_per_day`, $0 for free providers).

Day rollover is automatic (UTC). Caps are overridable:
```bash
python -m swarm.usage_tracker --report
python -m swarm.usage_tracker --cap groq max_requests_per_day 200
python -m swarm.usage_tracker --reset groq
```

## Why this matters for a swarm
Ten parallel worktrees sharing one free key would blow the rate limit in seconds.
Because every model call goes through the tracker, the swarm self-throttles: a provider
at its concurrency cap simply makes other worktrees wait, and a provider at its daily
cap is skipped (the orchestrator marks those worktrees `skipped-unreachable`).