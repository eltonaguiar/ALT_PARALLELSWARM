"""
llm_router.py — one `chat()` for every provider in registry.json.

Supports:
  * OpenAI-compatible /chat/completions (Groq, Cerebras, Mistral, OpenRouter,
    DeepSeek, LLM7, Chutes, Nous, Kimi, OpenAI, HuggingFace router, Ollama)
  * Google Gemini native generateContent
  * Ollama native /api/chat (fallback when the OpenAI shim is unavailable)

Every call is bracketed by the usage tracker: acquire -> call -> record -> release.
The tracker enforces per-provider concurrency + daily request/token/cost caps, so a
free key can never be over-driven by the swarm.

stdlib only (urllib). No `requests` dependency.
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from .usage_tracker import UsageTracker

REGISTRY_PATH = Path(__file__).resolve().parent / "registry.json"

# Some providers (Groq/Cloudflare) reject the default "Python-urllib" UA with 403/1010.
_UA = "Mozilla/5.0 (X11; Linux x86_64) ALT_PARALLELSWARM/1.0"


def _first_env(names) -> str | None:
    """api_key_env may be a string or list of candidate env var names; first hit wins."""
    if not names:
        return None
    if isinstance(names, str):
        names = [names]
    for n in names:
        v = os.environ.get(n)
        if v:
            return v
    return None


def load_registry(path: Path | str = REGISTRY_PATH) -> dict[str, Any]:
    with open(path) as f:
        return json.load(f)


def sync_caps(tracker: UsageTracker, registry: dict[str, Any]) -> None:
    """Push provider caps from registry.json into the tracker (registry is source of truth)."""
    for prov, pconf in registry.get("providers", {}).items():
        caps = {k: pconf[k] for k in
                ("max_concurrent", "max_requests_per_day", "max_tokens_per_day", "max_cost_per_day")
                if k in pconf}
        if caps:
            tracker.set_caps(prov, **caps)


class LLMRouter:
    def __init__(self, registry_path: Path | str = REGISTRY_PATH,
                 tracker: UsageTracker | None = None):
        self.reg = load_registry(registry_path)
        self.tracker = tracker or UsageTracker()
        sync_caps(self.tracker, self.reg)

    # ---- public ----------------------------------------------------------
    def chat(self, model_key: str, messages: list[dict[str, str]],
             temperature: float = 0.3, max_tokens: int = 1500,
             timeout: int = 120, retries: int = 2) -> dict[str, Any]:
        if model_key not in self.reg["models"]:
            raise KeyError(f"unknown model '{model_key}'. Known: {list(self.reg['models'])[:8]}...")
        m = self.reg["models"][model_key]
        prov = m["provider"]
        pconf = self.reg["providers"][prov]
        key = _first_env(pconf.get("api_key_env"))

        # concurrency / daily gate
        ok, why = self.tracker.can_start(prov)
        if not ok:
            raise RuntimeError(f"usage gate blocked {prov}: {why}")
        if not self.tracker.acquire(prov):
            ok, why = self.tracker.can_start(prov)
            raise RuntimeError(f"could not acquire {prov}: {why}")

        last_err: Exception | None = None
        try:
            for attempt in range(retries + 1):
                try:
                    text, usage = self._dispatch(pconf, m, key, messages,
                                                 temperature, max_tokens, timeout)
                    self.tracker.record(prov, tokens=usage.get("total_tokens", 0),
                                        cost=0.0, model=model_key)
                    return {"text": text, "model": model_key, "provider": prov,
                            "usage": usage}
                except urllib.error.HTTPError as e:
                    body = e.read().decode("utf-8", "replace")[:300]
                    last_err = RuntimeError(f"{prov} HTTP {e.code}: {body}")
                    # 429/5xx are worth retrying with backoff; 4xx are not
                    if e.code in (429, 500, 502, 503, 504) and attempt < retries:
                        time.sleep(2 ** attempt)
                        continue
                    raise last_err
                except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
                    last_err = e
                    if attempt < retries:
                        time.sleep(2 ** attempt)
                        continue
                    raise
            raise last_err or RuntimeError("unknown dispatch failure")
        finally:
            self.tracker.release(prov)

    # ---- transport -------------------------------------------------------
    def _dispatch(self, pconf, m, key, messages, temperature, max_tokens, timeout):
        ptype = pconf["type"]
        if ptype == "gemini":
            return self._gemini(pconf, m, key, messages, temperature, max_tokens, timeout)
        return self._openai(pconf, m, key, messages, temperature, max_tokens, timeout)

    def _openai(self, pconf, m, key, messages, temperature, max_tokens, timeout):
        base = pconf["base_url"].rstrip("/")
        url = f"{base}/chat/completions"
        payload = {
            "model": m["model"],
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        headers = {"Content-Type": "application/json", "User-Agent": _UA}
        if key:
            headers["Authorization"] = f"Bearer {key}"
        data = self._post(url, payload, headers, timeout)
        msg = data["choices"][0]["message"]
        # reasoning models may return only `reasoning`/`reasoning_content` when the
        # token budget is spent on the chain-of-thought; fall back gracefully.
        text = msg.get("content")
        if not text:
            text = msg.get("reasoning_content") or msg.get("reasoning") or ""
        usage = data.get("usage", {}) or {}
        return text, usage

    def _gemini(self, pconf, m, key, messages, temperature, max_tokens, timeout):
        base = pconf["base_url"].rstrip("/")
        model = m["model"]
        url = f"{base}/models/{model}:generateContent?key={key}"
        # translate OpenAI-style messages -> gemini contents
        contents, system = [], None
        for msg in messages:
            role = msg.get("role")
            if role == "system":
                system = msg.get("content", "")
                continue
            contents.append({
                "role": "model" if role == "assistant" else "user",
                "parts": [{"text": msg.get("content", "")}],
            })
        payload: dict[str, Any] = {
            "contents": contents,
            "generationConfig": {"temperature": temperature, "maxOutputTokens": max_tokens},
        }
        if system:
            payload["systemInstruction"] = {"parts": [{"text": system}]}
        data = self._post(url, payload, {"Content-Type": "application/json", "User-Agent": _UA}, timeout)
        cand = data.get("candidates", [{}])[0]
        parts = cand.get("content", {}).get("parts", [])
        text = "".join(p.get("text", "") for p in parts)
        um = data.get("usageMetadata", {}) or {}
        usage = {"total_tokens": um.get("totalTokenCount", 0)}
        return text, usage

    def _post(self, url, payload, headers, timeout):
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=body, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))

    # ---- misc ------------------------------------------------------------
    def available_models(self) -> list[str]:
        return list(self.reg["models"].keys())


# ---- CLI smoke test ------------------------------------------------------
def _cli() -> None:
    import argparse
    ap = argparse.ArgumentParser(description="Smoke-test a model through the router")
    ap.add_argument("--model", required=True)
    ap.add_argument("--prompt", default="Reply with the single word: pong")
    args = ap.parse_args()
    r = LLMRouter()
    out = r.chat(args.model, [{"role": "user", "content": args.prompt}],
                 max_tokens=64)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    _cli()