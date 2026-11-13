#!/usr/bin/env python3
"""
llm_client.py — one OpenAI-compatible chat client for local and cloud models.

No third-party dependencies (urllib only). API keys are read from env vars and
are never written to disk or logged.

Supported providers (all OpenAI-compatible):
  ollama       http://localhost:11434/v1            no key
  deepseek     https://api.deepseek.com/v1           DEEPSEEK_API_KEY
  groq         https://api.groq.com/openai/v1        GROQ_API_KEY
  cerebras     https://api.cerebras.ai/v1            CEREBRAS_API_KEY
  mistral      https://api.mistral.ai/v1             MISTRAL_API_KEY
  openrouter   https://openrouter.ai/api/v1          OPENROUTER_API_KEY
  gemini       https://generativelanguage.googleapis.com/v1beta/openai
                                                     GEMINI_API_KEY (or GOOGLE_AI_API_KEY)
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent

DEFAULT_BASE_URLS = {
    "ollama": "http://localhost:11434/v1",
    "deepseek": "https://api.deepseek.com/v1",
    "groq": "https://api.groq.com/openai/v1",
    "cerebras": "https://api.cerebras.ai/v1",
    "mistral": "https://api.mistral.ai/v1",
    "openrouter": "https://openrouter.ai/api/v1",
    "gemini": "https://generativelanguage.googleapis.com/v1beta/openai",
}

DEFAULT_KEY_ENVS = {
    "ollama": "",
    "deepseek": "DEEPSEEK_API_KEY",
    "groq": "GROQ_API_KEY",
    "cerebras": "CEREBRAS_API_KEY",
    "mistral": "MISTRAL_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
    "gemini": "GEMINI_API_KEY",
}


class LLMError(RuntimeError):
    pass


@dataclass
class Agent:
    id: str
    provider: str
    model: str
    base_url: str = ""
    api_key_env: str = ""
    max_tokens: int = 1200
    temperature: float = 0.2
    price_in_per_1k: float = 0.0
    price_out_per_1k: float = 0.0
    max_inflight: int = 1
    daily_calls: int = 1000
    daily_tokens: int = 1_000_000
    note: str = ""
    enabled: bool = True
    extra: dict[str, Any] = field(default_factory=dict)

    def resolved_base_url(self) -> str:
        return (self.base_url or DEFAULT_BASE_URLS.get(self.provider, "")).rstrip("/")

    def resolved_key_env(self) -> str:
        return self.api_key_env or DEFAULT_KEY_ENVS.get(self.provider, "")

    def api_key(self) -> str:
        env = self.resolved_key_env()
        return os.environ.get(env, "") if env else ""

    def public_dict(self) -> dict[str, Any]:
        """Never include the key itself."""
        return {
            "id": self.id,
            "provider": self.provider,
            "model": self.model,
            "base_url": self.resolved_base_url(),
            "api_key_env": self.resolved_key_env() or None,
            "api_key_present": bool(self.api_key()),
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "max_inflight": self.max_inflight,
            "daily_calls": self.daily_calls,
            "daily_tokens": self.daily_tokens,
        }


def load_roster(path: str | Path = ROOT / "models.yaml") -> tuple[dict[str, Any], list[Agent]]:
    data = yaml.safe_load(Path(path).read_text())
    defaults = data.get("defaults", {}) or {}
    agents: list[Agent] = []
    for raw in data.get("agents", []):
        merged = {**defaults, **raw}
        agents.append(
            Agent(
                id=merged["id"],
                provider=merged["provider"],
                model=merged["model"],
                base_url=merged.get("base_url", ""),
                api_key_env=merged.get("api_key_env", ""),
                max_tokens=int(merged.get("max_tokens", 1200)),
                temperature=float(merged.get("temperature", 0.2)),
                price_in_per_1k=float(merged.get("price_in_per_1k", 0.0)),
                price_out_per_1k=float(merged.get("price_out_per_1k", 0.0)),
                max_inflight=int(merged.get("max_inflight", 1)),
                daily_calls=int(merged.get("daily_calls", 1000)),
                daily_tokens=int(merged.get("daily_tokens", 1_000_000)),
                note=merged.get("note", ""),
                enabled=bool(merged.get("enabled", True)),
                extra={k: v for k, v in merged.items() if k not in Agent.__dataclass_fields__},
            )
        )
    return data, agents


def _post_json(url: str, payload: dict[str, Any], headers: dict[str, str], timeout: int) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:600]
        raise LLMError(f"HTTP {e.code} from {url}: {detail}") from e
    except urllib.error.URLError as e:
        raise LLMError(f"connection error to {url}: {e.reason}") from e
    except TimeoutError as e:
        raise LLMError(f"timeout after {timeout}s: {url}") from e


def chat(
    agent: Agent,
    messages: list[dict[str, str]],
    *,
    max_tokens: int | None = None,
    temperature: float | None = None,
    timeout: int = 300,
    extra_body: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return text, reasoning, usage and the raw response for one chat call."""
    base = agent.resolved_base_url()
    if not base:
        raise LLMError(f"no base_url for provider {agent.provider}")
    url = f"{base}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/131.0 Safari/537.36",
    }
    key = agent.api_key()
    if key:
        headers["Authorization"] = f"Bearer {key}"
    if agent.provider == "openrouter":
        headers.setdefault("HTTP-Referer", "https://github.com/eltonaguiar/ALT_PARALLELSWARM")
        headers.setdefault("X-Title", "ALT_PARALLELSWARM")
    payload: dict[str, Any] = {
        "model": agent.model,
        "messages": messages,
        "max_tokens": max_tokens or agent.max_tokens,
        "temperature": agent.temperature if temperature is None else temperature,
        "stream": False,
    }
    if extra_body:
        payload.update(extra_body)

    data = _post_json(url, payload, headers, timeout)
    if "error" in data:
        raise LLMError(f"provider error: {json.dumps(data['error'])[:600]}")
    choices = data.get("choices") or []
    if not choices:
        raise LLMError(f"no choices in response: {json.dumps(data)[:600]}")
    msg = choices[0].get("message", {}) or {}
    content = (msg.get("content") or "").strip()
    reasoning = (msg.get("reasoning") or "").strip()
    text = content or reasoning
    usage = data.get("usage", {}) or {}
    return {
        "text": text,
        "content": content,
        "reasoning": reasoning,
        "content_was_empty": not bool(content),
        "model_reported": data.get("model", agent.model),
        "finish_reason": choices[0].get("finish_reason"),
        "usage": {
            "tokens_in": int(usage.get("prompt_tokens", 0) or 0),
            "tokens_out": int(usage.get("completion_tokens", 0) or 0),
            "total": int(usage.get("total_tokens", 0) or 0),
        },
        "raw": data,
    }
