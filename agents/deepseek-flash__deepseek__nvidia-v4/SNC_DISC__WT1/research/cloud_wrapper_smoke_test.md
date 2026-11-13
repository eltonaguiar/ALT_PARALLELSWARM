# Cloud wrapper smoke test — 2026-11-13

Purpose: prove `nvidia_v4_swarm/llm_client.py` + `usage_tracker.py` work against a real
cloud key, not just local Ollama.

| Provider | Model | Result | Tokens in/out | Cost | Notes |
|---|---|---|---|---|---|
| `deepseek` | `deepseek-chat` | **OK** — returned `WRAPPER_OK` | 12 / 4 | $0.000008 | OpenAI-compatible endpoint. |
| `groq` | `llama-3.3-70b-versatile` | **FAIL** — HTTP 404 model not found | 0 | 0 | Model id not available on this key. |
| `groq` | `openai/gpt-oss-120b` | **OK** | 78 / 30 | 0 | Required browser-like User-Agent; default urllib UA hit Cloudflare 1010. |

## Findings folded back into the code

1. Added a browser-like `User-Agent` to all requests. Groq's Cloudflare layer rejected the
   default Python UA with `403 Error 1010`, which is misleadingly not an auth error.
2. Groq's model catalog on this key (2026-11-13) includes `openai/gpt-oss-120b`,
   `openai/gpt-oss-20b`, `qwen/qwen3.8-27b`, `allam-2-7b` — **not**
   `llama-3.3-70b-versatile`. The roster was updated.
3. No key values were printed or written. The tracker records calls/tokens/cost only.

## Not tested

- Gemini, Cerebras, Mistral, OpenRouter (keys present but no calls made; disabled in roster).
- Streaming, tool calls, JSON mode.
- Per-minute rate limits (the tracker enforces concurrency and daily caps, not RPM).
