#!/usr/bin/env python3
"""One OpenAI-compatible chat interface for local and free cloud models.

- `ollama` uses the native /api/chat endpoint so `think: false` can suppress
  chain-of-thought models that would otherwise spend the whole token budget thinking.
- every other provider uses /chat/completions with a bearer key from its env var.
- every call goes through usage_tracker.Ledger, which enforces inflight and daily caps.
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from usage_tracker import DEFAULT_LEDGER, Ledger  # noqa: E402

REGISTRY = HERE / "registry.json"
RETRYABLE = {408, 409, 425, 429, 500, 502, 503, 504}


def registry() -> dict:
    with open(REGISTRY) as fh:
        return json.load(fh)


def resolve(model: str, provider: str | None = None) -> tuple[str, dict, dict]:
    reg = registry()
    spec = reg.get("models", {}).get(model, {})
    provider = provider or spec.get("provider")
    if not provider:
        raise ValueError(f"unknown model {model!r}; pass provider explicitly")
    if provider not in reg["providers"]:
        raise ValueError(f"unknown provider {provider!r}")
    return provider, reg["providers"][provider], spec


def _post(url: str, payload: dict, headers: dict, timeout: int) -> tuple[dict, dict]:
    body = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8", "replace")
        return json.loads(raw), dict(resp.headers)


def chat(
    model: str,
    messages: list[dict],
    provider: str | None = None,
    max_tokens: int = 1200,
    temperature: float = 0.1,
    timeout: int = 300,
    retries: int = 2,
    ledger_path: str | Path = DEFAULT_LEDGER,
) -> dict:
    provider, cfg, spec = resolve(model, provider)
    key_env = cfg.get("api_key_env", "")
    api_key = os.environ.get(key_env, "") if key_env else ""
    if key_env and not api_key:
        raise RuntimeError(f"missing env var {key_env} for provider {provider}")

    ledger = Ledger(ledger_path)
    estimate = min(16000, max(1200, sum(len(m.get("content", "")) for m in messages) // 3))
    last_error: Exception | None = None

    for attempt in range(retries + 1):
        try:
            with ledger.acquire(provider, est_tokens=estimate) as lease:
                if cfg.get("kind") == "ollama":
                    url = cfg["base_url"].rstrip("/") + "/api/chat"
                    payload = {
                        "model": model,
                        "messages": messages,
                        "stream": False,
                        "think": bool(spec.get("think", False)),
                        "options": {"num_predict": max_tokens, "temperature": temperature},
                    }
                    headers = {"Content-Type": "application/json"}
                else:
                    url = cfg["base_url"].rstrip("/") + "/chat/completions"
                    payload = {
                        "model": model,
                        "messages": messages,
                        "max_tokens": max_tokens,
                        "temperature": temperature,
                        "stream": False,
                    }
                    headers = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {api_key}",
                    }
                    headers.update(cfg.get("extra_headers", {}))
                data, _ = _post(url, payload, headers, timeout)
                if cfg.get("kind") == "ollama":
                    msg = data.get("message", {}) or {}
                    text = msg.get("content", "")
                    thinking = msg.get("thinking", "") or ""
                    lease["tokens"] = int(data.get("prompt_eval_count", 0)) + int(data.get("eval_count", 0))
                    usage = {
                        "prompt_tokens": data.get("prompt_eval_count", 0),
                        "completion_tokens": data.get("eval_count", 0),
                        "total_tokens": lease["tokens"],
                    }
                    finish = data.get("done_reason")
                else:
                    choice = (data.get("choices") or [{}])[0]
                    text = (choice.get("message") or {}).get("content", "") or ""
                    thinking = (choice.get("message") or {}).get("reasoning", "") or ""
                    usage = data.get("usage") or {}
                    lease["tokens"] = int(usage.get("total_tokens") or 0)
                    finish = choice.get("finish_reason")
                return {
                    "provider": provider,
                    "model": model,
                    "text": text,
                    "thinking": thinking,
                    "usage": usage,
                    "finish_reason": finish,
                    "cost_usd": lease.get("cost_usd", 0.0),
                }
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code not in RETRYABLE or attempt >= retries:
                detail = exc.read().decode("utf-8", "replace")[:500]
                raise RuntimeError(f"HTTP {exc.code} from {provider}: {detail}") from exc
            time.sleep(2 ** attempt + 1)
        except (urllib.error.URLError, TimeoutError) as exc:
            last_error = exc
            if attempt >= retries:
                raise RuntimeError(f"network failure from {provider}: {exc}") from exc
            time.sleep(2 ** attempt + 1)
    raise RuntimeError(f"exhausted retries for {provider}: {last_error}")


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="One-shot chat for testing the router")
    parser.add_argument("--model", required=True)
    parser.add_argument("--provider")
    parser.add_argument("--prompt", default="Reply with exactly: OK")
    parser.add_argument("--max-tokens", type=int, default=32)
    args = parser.parse_args()
    result = chat(args.model, [{"role": "user", "content": args.prompt}],
                  provider=args.provider, max_tokens=args.max_tokens)
    print(json.dumps(result, indent=2)[:2000])


if __name__ == "__main__":
    main()
