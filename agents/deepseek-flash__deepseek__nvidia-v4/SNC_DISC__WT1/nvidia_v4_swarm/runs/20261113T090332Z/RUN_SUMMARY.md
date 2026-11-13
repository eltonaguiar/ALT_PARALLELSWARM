# Swarm run 20261113T090332Z

- Wall time: **88.2s**
- Max parallel: **2**
- Reference: `/tmp/ALT_PARALLELSWARM/agents/deepseek-flash__deepseek__nvidia-v4/SNC_DISC__WT1/05_FINAL/DISCOVERY_CONFIG_REFERENCE.md`
- Ledger: `/tmp/ALT_PARALLELSWARM/agents/deepseek-flash__deepseek__nvidia-v4/SNC_DISC__WT1/nvidia_v4_swarm/state/usage.sqlite3`

| agent | model | provider | status | tokens in/out | seconds |
|---|---|---|---|---|---|
| `qwen2.5-coder-7b__ollama__nvidia-v4` | `qwen2.5-coder:7b` | `ollama` | **ok** | 3036/725 | 32.8 |
| `qwen3.5-4b__ollama__nvidia-v4` | `qwen3.5:4b` | `ollama` | **ok** | 3157/2500 | 88.2 |

## Failures / blocks

- none

## Ledger snapshot

```json
{
  "ledger": "/tmp/ALT_PARALLELSWARM/agents/deepseek-flash__deepseek__nvidia-v4/SNC_DISC__WT1/nvidia_v4_swarm/state/usage.sqlite3",
  "day": "2026-11-13",
  "providers": {
    "ollama": {
      "provider": "ollama",
      "day": "2026-11-13",
      "calls": 2,
      "tokens_in": 6193,
      "tokens_out": 3225,
      "tokens": 9418,
      "cost_usd": 0.0,
      "inflight": 0,
      "max_inflight": 2,
      "daily_calls": 1000,
      "daily_tokens": 5000000,
      "price_in_per_1k": 0.0,
      "price_out_per_1k": 0.0
    }
  }
}
```
