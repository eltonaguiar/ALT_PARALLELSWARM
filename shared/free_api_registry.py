#!/usr/bin/env python3
"""
free_api_registry.py — unified wrapper + catalog for the swarm's free/paid model keys.

Why: a parallel swarm with ~20 keys (OpenRouter, Groq, Cerebras, DeepInfra, SambaNova,
SiliconFlow, Novita, xAI, Moonshot/Kimi, Mistral, DeepSeek, OpenAI, Google/Gemini, NVIDIA NIM,
GLM/Zhipu, HuggingFace, NOUS, Chutes, LLM7, Abacus, …) needs ONE place that:

  1. catalogs each provider (base_url, env var name, default model, free vs paid, OpenAI-compat)
  2. exposes a single `complete()` that calls ANY provider's `/chat/completions`
  3. integrates with shared/budget.py so busy/inflight + daily-call + daily-token + cost
     tracking is enforced per provider (prevents burning a free key or a credit card).

Keys are read from the environment at call time; the catalog stores only the *name* of the
env var, never a secret. Nothing here logs or writes key material.

Usage:
    import free_api_registry as reg
    reg.register_budget_defaults()                     # tell budget.py about every provider
    print(reg.status())                                 # who is busy / how much used today
    text = reg.complete("groq", "llama-3.3-70b-versatile",
                        [{"role": "user", "content": "hi"}])
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

SHARED = Path(__file__).resolve().parent
sys.path.insert(0, str(SHARED))
import budget  # noqa: E402

# provider -> catalog entry. `env` is the env var NAME (never the value).
# `compat`: "openai" (most), "gemini" (Google's native endpoint, not OpenAI-compatible).
PROVIDERS: dict[str, dict] = {
    # --- local ---------------------------------------------------------------
    "ollama": {"base_url": "http://localhost:11434/v1", "env": "", "compat": "openai",
               "free": True, "models": ["qwen3.5:35b-a3b", "qwen3:30b-a3b", "deepseek-r1:32b",
                                        "qwen2.5:14b", "gemma2:9b", "llama3.2:3b"],
               "note": "local CPU/GPU; no key, low parallelism"},
    # --- paid (cost-tracked) -------------------------------------------------
    "deepseek": {"base_url": "https://api.deepseek.com/v1", "env": "DEEPSEEK_API_KEY", "compat": "openai",
                 "free": False, "models": ["deepseek-v4-pro", "deepseek-v4-flash", "deepseek-chat"],
                 "price_per_1k": 0.00028, "note": "deepseek official"},
    "openai": {"base_url": "https://api.openai.com/v1", "env": "OPENAI_API_KEY", "compat": "openai",
               "free": False, "models": ["gpt-4o-mini", "gpt-oss-120b"],
               "price_per_1k": 0.0006, "note": "openai official"},
    # --- free tiers (tight caps) --------------------------------------------
    "openrouter": {"base_url": "https://openrouter.ai/api/v1", "env": "OPENROUTER_API_KEY", "compat": "openai",
                   "free": True, "models": [":free", "deepseek/deepseek-chat-v3.1", "qwen/qwen-3-32b"],
                   "note": "aggregator; :free models rotate"},
    "groq": {"base_url": "https://api.groq.com/openai/v1", "env": "GROQ_API_KEY", "compat": "openai",
             "free": True, "models": ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"],
             "note": "fast free tier"},
    "cerebras": {"base_url": "https://api.cerebras.ai/v1", "env": "CEREBRAS_API_KEY", "compat": "openai",
                 "free": True, "models": ["llama3.3-70b", "llama-3.1-8b"],
                 "note": "Cerebras free tier"},
    "deepinfra": {"base_url": "https://api.deepinfra.com/v1/openai", "env": "DEEPINFRA_API_KEY", "compat": "openai",
                  "free": True, "models": ["meta-llama/Llama-3.3-70B-Instruct", "Qwen/Qwen3-32B"],
                  "note": "DeepInfra"},
    "sambanova": {"base_url": "https://api.sambanova.ai/v1", "env": "SAMBANOVA_API_KEY", "compat": "openai",
                  "free": True, "models": ["Meta-Llama-3.3-70B-Instruct"],
                  "note": "SambaNova free tier"},
    "siliconflow": {"base_url": "https://api.siliconflow.cn/v1", "env": "SILICONFLOW_API_KEY", "compat": "openai",
                    "free": True, "models": ["Qwen/Qwen3-32B", "deepseek-ai/DeepSeek-V3"],
                    "note": "SiliconFlow free tier"},
    "novita": {"base_url": "https://api.novita.ai/v3/openai", "env": "NOVITA_API_KEY", "compat": "openai",
               "free": True, "models": ["deepseek/deepseek-r1", "meta-llama/llama-3.3-70b-instruct"],
               "note": "Novita"},
    "xai": {"base_url": "https://api.x.ai/v1", "env": "XAI_API_KEY", "compat": "openai",
            "free": True, "models": ["grok-2-latest", "grok-2-1212"],
            "note": "xAI / Grok"},
    "kimi": {"base_url": "https://api.moonshot.ai/v1", "env": "KIMI_API_KEY", "compat": "openai",
             "free": True, "models": ["moonshot-v1-8k", "kimi-k2"],
             "note": "Moonshot / Kimi"},
    "mistral": {"base_url": "https://api.mistral.ai/v1", "env": "MISTRAL_API_KEY", "compat": "openai",
                "free": True, "models": ["mistral-small-latest", "open-mistral-nemo"],
                "note": "Mistral (La Plateforme)"},
    "nvidia": {"base_url": "https://integrate.api.nvidia.com/v1", "env": "NVIDIA_API_KEY", "compat": "openai",
               "free": True, "models": ["nvidia/nemotron-3.5-super-vl-120b-a12b", "meta/llama-3.3-70b-instruct"],
               "note": "NVIDIA NIM (build.nvidia.com)"},
    "glm": {"base_url": "https://open.bigmodel.cn/api/paas/v4", "env": "GLM_API_KEY", "compat": "openai",
            "free": True, "models": ["glm-4-flash", "glm-4-plus"],
            "note": "Zhipu / GLM (bigmodel.cn)"},
    "huggingface": {"base_url": "https://api-inference.huggingface.co/v1", "env": "HUGGING_FACE_TOKEN", "compat": "openai",
                    "free": True, "models": ["Qwen/Qwen3-32B", "meta-llama/Llama-3.3-70B-Instruct"],
                    "note": "HF Serverless Inference"},
    "nous": {"base_url": "https://api.nousresearch.com/v1", "env": "NOUS_API_KEY_FREE", "compat": "openai",
             "free": True, "models": ["Hermes-3-Llama-3.1-70B"],
             "note": "Nous Research"},
    "chutes": {"base_url": "https://api.chutes.ai/v1", "env": "CHUTES_API_KEY_FREE", "compat": "openai",
               "free": True, "models": ["deepseek-ai/DeepSeek-V3", "Qwen/Qwen3-32B"],
               "note": "Chutes"},
    "llm7": {"base_url": "https://api.llm7.io/v1", "env": "LLM7_API_KEY_FREE", "compat": "openai",
             "free": True, "models": ["deepseek-v3", "qwen3-32b"],
             "note": "LLM7"},
    "abacus": {"base_url": "https://api.abacus.ai/v1", "env": "ABACUS_API_KEY_1MONTh", "compat": "openai",
               "free": True, "models": ["DeepSeek-V3", "Llama-3.3-70B-Instruct"],
               "note": "Abacus AI (1-month key)"},
    "gemini": {"base_url": "https://generativelanguage.googleapis.com/v1beta", "env": "GOOGLE_AI_API_KEY", "compat": "gemini",
               "free": True, "models": ["gemini-2.0-flash", "gemini-1.5-flash"],
               "note": "Google AI Studio (native endpoint, not OpenAI-compat)"},
}


def register_budget_defaults() -> None:
    """Inject every provider's caps into budget.DEFAULTS so the tracker knows about them."""
    for name, e in PROVIDERS.items():
        entry = {"max_inflight": 2, "daily_calls": 500, "daily_tokens": 3_000_000,
                 "price_per_1k": e.get("price_per_1k", 0.0)}
        if e["free"]:
            entry.update(max_inflight=2, daily_calls=200, daily_tokens=2_000_000, price_per_1k=0.0)
        if name == "ollama":
            entry.update(max_inflight=2, daily_calls=1000, daily_tokens=5_000_000, price_per_1k=0.0)
        budget.DEFAULTS.setdefault(name, entry)


def resolve(provider: str, model: str | None = None) -> tuple[str, str, str]:
    """Return (base_url, api_key, model). Raises if the key is not set."""
    e = PROVIDERS.get(provider)
    if not e:
        raise KeyError(f"unknown provider '{provider}'. known: {sorted(PROVIDERS)}")
    key = os.environ.get(e["env"]) if e["env"] else ("ollama" if provider == "ollama" else "")
    if e["compat"] != "openai":
        raise NotImplementedError(
            f"provider '{provider}' uses the '{e['compat']}' API shape; complete() is OpenAI-compat only. "
            "Use Gemini's native generateContent endpoint instead.")
    model = model or (e["models"][0] if e["models"] else "")
    if not model:
        raise ValueError(f"no model given for provider '{provider}'")
    return e["base_url"], key, model


def complete(provider: str, messages: list[dict], model: str | None = None,
             temperature: float = 0.2, max_tokens: int = 2048, est_tokens: int = 4000,
             timeout: int = 240) -> str:
    """One-call wrapper: acquires a budget slot for `provider`, calls /chat/completions,
    releases the slot (recording tokens/cost), and returns the assistant text."""
    base_url, key, model = resolve(provider, model)
    payload = {"model": model, "messages": messages, "temperature": temperature,
               "max_tokens": max_tokens, "stream": False}
    req = urllib.request.Request(
        base_url.rstrip("/") + "/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + (key or "ollama")})
    with budget.acquire(provider, est_tokens=est_tokens):
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read().decode())
    return (data.get("choices") or [{}])[0].get("message", {}).get("content", "")


def status(provider: str | None = None) -> dict:
    """Snapshot of the tracker: per-provider inflight, calls, tokens, cost, day."""
    register_budget_defaults()
    return budget.status(provider)


if __name__ == "__main__":
    register_budget_defaults()
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    if arg in ("list", "catalog", "providers"):
        print("\n".join(
            f"{n:14} {'FREE' if e['free'] else 'PAID':4}  env={e['env'] or '(none)':22} "
            f"{e['base_url']}  models={', '.join(e['models'][:3])}" for n, e in PROVIDERS.items()))
    else:
        print(json.dumps(status(arg), indent=2))
