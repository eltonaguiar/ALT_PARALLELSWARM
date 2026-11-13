# Prerequisite / provenance

- Agent id: `qwen2.5-coder-7b__ollama__nvidia-v4`
- Model: `qwen2.5-coder:7b`
- Provider: `ollama`
- Base URL: `http://localhost:11434/v1`
- API key env: `(none)` — key present: **False**
- Harness: `nvidia_v4_swarm/run_swarm.py` (Kilo CLI orchestration)
- Capability: text-only review via OpenAI-compatible chat API.
- Not used: browsing, Playwright, tools. This worker only critiques the supplied excerpt.
