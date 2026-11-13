#!/usr/bin/env python3
"""
free_keys.py — free-API-key registry + busy/usage tracker + call wrapper.

Goal: stop a parallel swarm from burning a free key (rate limit / daily quota /
accidental cost). Tracks, per provider: inflight (busy), calls today, tokens today,
estimated cost. fcntl-locked JSON ledger in ./state/swarm_ledger.json.

Keys are read from env and NEVER printed. Only counts/usage are logged.
Paid providers (DEEPSEEK_API_KEY, OPENAI_API_KEY) are intentionally absent.
"""
from __future__ import annotations
import fcntl, json, os, sys, time, urllib.request, urllib.error
from contextlib import contextmanager
from datetime import date
from pathlib import Path

STATE = Path(__file__).resolve().parent / "state"; STATE.mkdir(exist_ok=True)
LEDGER = STATE / "swarm_ledger.json"; LOCK = STATE / "swarm.lock"

# OpenAI-compatible endpoints. model = default free-tier model to try.
PROVIDERS = {
    "groq":      {"base": "https://api.groq.com/openai/v1",            "key_env": "GROQ_API_KEY",      "model": "openai/gpt-oss-120b",       "max_inflight": 2, "daily_calls": 100, "daily_tokens": 200_000, "price_per_1k": 0.0},
    "cerebras":  {"base": "https://api.cerebras.ai/v1",                "key_env": "CEREBRAS_API_KEY", "model": "gpt-oss-120b", "max_inflight": 2, "daily_calls": 100, "daily_tokens": 200_000, "price_per_1k": 0.0},
    "gemini":    {"base": "https://generativelanguage.googleapis.com/v1beta/openai", "key_env": "GEMINI_API_KEY" if os.environ.get("GEMINI_API_KEY") else "GOOGLE_AI_API_KEY", "model": "gemini-2.5-flash-lite", "max_inflight": 2, "daily_calls": 300, "daily_tokens": 500_000, "price_per_1k": 0.0},
    "mistral":   {"base": "https://api.mistral.ai/v1",                 "key_env": "MISTRAL_API_KEY",   "model": "mistral-small-latest",       "max_inflight": 2, "daily_calls": 100, "daily_tokens": 300_000, "price_per_1k": 0.0},
    "openrouter":{"base": "https://openrouter.ai/api/v1",              "key_env": "OPENROUTER_API_KEY","model": "google/gemma-4-31b-it:free", "max_inflight": 2, "daily_calls": 50, "daily_tokens": 200_000, "price_per_1k": 0.0},
    "ollama":    {"base": "http://localhost:11434/v1",                 "key_env": None,                "model": "gemma2:9b",               "max_inflight": 1,                                          "daily_calls": 2000,"daily_tokens": 20_000_000, "price_per_1k": 0.0},
    # --- SubQ (Subquadratic) — OpenAI-compatible, early-access Savant 1.4 (4M ctx) ---
    # Paid key: SUBQ_API_KEY. Free key (if the account grants free quota): SUBQ_FREE_API_KEY.
    # subq_free falls back to the paid key when the free one is absent so the swarm still runs.
    # Savant always reasons (billed as output) and temperature is fixed at 1 (or omitted) —
    # both are enforced via per-provider overrides below. store=false keeps prompts out of SubQ storage.
    "subq_free": {"base": "https://api.subq.ai/v1",                    "key_env": "SUBQ_FREE_API_KEY" if os.environ.get("SUBQ_FREE_API_KEY") else "SUBQ_API_KEY",
                  "model": "subq-savant-1.4", "max_inflight": 2, "daily_calls": 50,  "daily_tokens": 100_000,
                  "price_per_1k": 0.0, "price_in_1k": 0.0001, "price_out_1k": 0.0005,
                  "temperature": 1, "extra_body": {"reasoning_effort": "low", "store": False}},
    "subq_paid": {"base": "https://api.subq.ai/v1",                    "key_env": "SUBQ_API_KEY",
                  "model": "subq-savant-1.4", "max_inflight": 2, "daily_calls": 200, "daily_tokens": 500_000,
                  "price_per_1k": 0.0003, "price_in_1k": 0.0001, "price_out_1k": 0.0005,
                  "temperature": 1, "extra_body": {"reasoning_effort": "low", "store": False}},
    # SubQ Snap (decisions model, every account, output free) is NOT chat/completions;
    # it is wired separately in subq_snap.py, not as a chat provider.
}

def _load():
    if LEDGER.exists():
        try: return json.loads(LEDGER.read_text())
        except Exception: pass
    return {"providers": {}}

def _save(d): LEDGER.write_text(json.dumps(d, indent=2))

@contextmanager
def _locked():
    STATE.mkdir(exist_ok=True)
    with open(LOCK, "w") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        try: yield
        finally: fcntl.flock(fh, fcntl.LOCK_UN)

def _roll(e, p):
    today = date.today().isoformat()
    if e.get("day") != today: e.update(day=today, calls=0, tokens=0, cost_usd=0.0)
    e.setdefault("inflight", 0)
    for k, v in PROVIDERS[p].items():
        if k not in ("base", "key_env", "model"): e.setdefault(k, v)
    return e

def status(provider=None):
    with _locked():
        d = _load(); provs = d.setdefault("providers", {})
        names = [provider] if provider else list(PROVIDERS)
        for p in names:
            provs[p] = _roll(provs.setdefault(p, {}), p)
            provs[p]["present"] = bool(PROVIDERS[p]["key_env"] is None or os.environ.get(PROVIDERS[p]["key_env"]))
        _save(d); return {p: provs[p] for p in names}

@contextmanager
def acquire(provider, est_tokens=1500):
    with _locked():
        d = _load(); e = _roll(d.setdefault("providers", {}).setdefault(provider, {}), provider)
        if e["inflight"] >= e["max_inflight"]: raise RuntimeError(f"BUSY provider={provider} inflight={e['inflight']}/{e['max_inflight']}")
        if e["calls"] + 1 > e["daily_calls"]: raise RuntimeError(f"DAILY_CAP provider={provider} calls={e['calls']}/{e['daily_calls']}")
        if e["tokens"] + est_tokens > e["daily_tokens"]: raise RuntimeError(f"TOKEN_CAP provider={provider} tokens={e['tokens']}/{e['daily_tokens']}")
        e["inflight"] += 1; e["calls"] += 1; _save(d)
    try: yield
    finally:
        with _locked():
            d = _load(); e = _roll(d.setdefault("providers", {}).setdefault(provider, {}), provider)
            e["inflight"] = max(0, e["inflight"] - 1)
            e["tokens"] += est_tokens; e["cost_usd"] = round(e.get("cost_usd", 0.0) + est_tokens/1000*e.get("price_per_1k", 0.0), 6)
            _save(d)

def have_key(provider):
    ke = PROVIDERS[provider]["key_env"]
    return ke is None or bool(os.environ.get(ke))

def chat(provider, messages, max_tokens=200, timeout=45):
    cfg = PROVIDERS[provider]
    if not have_key(provider): raise RuntimeError(f"NO_KEY provider={provider}")
    with acquire(provider, est_tokens=max_tokens + 600):
        body = {"model": cfg["model"], "messages": messages, "max_tokens": max_tokens}
        temp = cfg.get("temperature", 0.2)
        if temp is not None: body["temperature"] = temp
        body.update(cfg.get("extra_body") or {})
        body = json.dumps(body).encode()
        headers = {"Content-Type": "application/json", "User-Agent": "alt-parallelswarm/inkling2"}
        if cfg["key_env"]: headers["Authorization"] = f"Bearer {os.environ[cfg['key_env']]}"
        req = urllib.request.Request(cfg["base"] + "/chat/completions", data=body, headers=headers)
        t0 = time.time()
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read())
        dt = time.time() - t0
        msg = (data.get("choices") or [{}])[0].get("message", {}).get("content") or ""
        usage = data.get("usage") or {}
        if usage:
            with _locked():
                d = _load(); e = _roll(d.setdefault("providers", {}).setdefault(provider, {}), provider)
                e["tokens_actual"] = e.get("tokens_actual", 0) + (usage.get("total_tokens") or 0)
                p_in = cfg.get("price_in_1k", 0.0) / 1000; p_out = cfg.get("price_out_1k", 0.0) / 1000
                cost = usage.get("prompt_tokens", 0) * p_in + usage.get("completion_tokens", 0) * p_out
                e["cost_actual_usd"] = round(e.get("cost_actual_usd", 0.0) + cost, 6)
                _save(d)
        return {"provider": provider, "model": cfg["model"], "latency_s": round(dt, 2),
                "content": msg.strip(), "usage": usage,
                "finish_reason": (data.get("choices") or [{}])[0].get("finish_reason")}

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        print(json.dumps(status(sys.argv[2] if len(sys.argv) > 2 else None), indent=2))
    else:
        print(json.dumps({p: {"model": v["model"], "have_key": have_key(p)} for p, v in PROVIDERS.items()}, indent=2))
