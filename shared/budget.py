#!/usr/bin/env python3
"""
budget.py — concurrency + daily-usage tracker for free/paid model keys.

Why: a parallel swarm will happily fire 8 requests at one free key and burn the
daily quota (or the credit card) before any agent reports back.

Design:
  * one JSON ledger (shared/state/budget_ledger.json) with per-provider counters
  * fcntl lock so concurrent agents cannot race the counters
  * acquire() enforces  max_inflight  and  daily_tokens / daily_calls caps
  * release() records actual usage so the next agent sees it

Ledger shape:
{
  "providers": {
     "ollama": {"inflight": 0, "day": "2026-11-13", "calls": 12, "tokens": 45000,
                "max_inflight": 2, "daily_calls": 500, "daily_tokens": 2000000,
                "cost_usd": 0.0, "price_per_1k": 0.0},
     "deepseek": {...}
  }
}
"""
from __future__ import annotations

import fcntl
import json
import os
import time
from contextlib import contextmanager
from datetime import date
from pathlib import Path

STATE = Path(__file__).resolve().parent / "state"
LEDGER = STATE / "budget_ledger.json"
LOCK = STATE / "budget.lock"

DEFAULTS = {
    # local models: free, but CPU-bound — keep parallelism low
    "ollama": {"max_inflight": 2, "daily_calls": 1000, "daily_tokens": 5_000_000,
               "price_per_1k": 0.0},
    # cloud free tiers: tight call caps
    "cerebras": {"max_inflight": 2, "daily_calls": 200, "daily_tokens": 2_000_000,
                 "price_per_1k": 0.0},
    "groq": {"max_inflight": 2, "daily_calls": 200, "daily_tokens": 400_000,
             "price_per_1k": 0.0},
    # paid: cost tracked so we can see spend per run
    "deepseek": {"max_inflight": 2, "daily_calls": 500, "daily_tokens": 3_000_000,
                 "price_per_1k": 0.00028},
}


def _ensure():
    STATE.mkdir(parents=True, exist_ok=True)
    if not LEDGER.exists():
        LEDGER.write_text(json.dumps({"providers": {}}, indent=2))


@contextmanager
def _locked():
    _ensure()
    with open(LOCK, "w") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)


def _load() -> dict:
    _ensure()
    try:
        return json.loads(LEDGER.read_text())
    except Exception:
        return {"providers": {}}


def _save(data: dict):
    LEDGER.write_text(json.dumps(data, indent=2))


def _roll(entry: dict, provider: str) -> dict:
    today = date.today().isoformat()
    if entry.get("day") != today:
        entry.update(day=today, calls=0, tokens=0, cost_usd=0.0)
    for k, v in DEFAULTS.get(provider, DEFAULTS["ollama"]).items():
        entry.setdefault(k, v)
    return entry


def status(provider: str | None = None) -> dict:
    with _locked():
        data = _load()
        provs = data.setdefault("providers", {})
        if provider:
            provs[provider] = _roll(provs.setdefault(provider, {}), provider)
            _save(data)
            return provs[provider]
        for p in list(provs):
            provs[p] = _roll(provs[p], p)
        _save(data)
        return provs


@contextmanager
def acquire(provider: str, est_tokens: int = 4000, wait_s: int = 900):
    """Block until this provider has a free slot and quota left."""
    deadline = time.time() + wait_s
    while True:
        with _locked():
            data = _load()
            e = _roll(data.setdefault("providers", {}).setdefault(provider, {}), provider)
            over_calls = e["calls"] + 1 > e.get("daily_calls", 10**9)
            over_tokens = e["tokens"] + est_tokens > e.get("daily_tokens", 10**12)
            if over_calls or over_tokens:
                _save(data)
                raise RuntimeError(
                    f"BUDGET_EXHAUSTED provider={provider} calls={e['calls']}/{e.get('daily_calls')} "
                    f"tokens={e['tokens']}/{e.get('daily_tokens')}")
            if e["inflight"] < e.get("max_inflight", 1):
                e["inflight"] += 1
                e["calls"] += 1
                _save(data)
                break
            _save(data)
        if time.time() > deadline:
            raise TimeoutError(f"BUDGET_TIMEOUT provider={provider} (no slot in {wait_s}s)")
        time.sleep(1.5)
    try:
        yield
    finally:
        with _locked():
            data = _load()
            e = _roll(data.setdefault("providers", {}).setdefault(provider, {}), provider)
            e["inflight"] = max(0, e["inflight"] - 1)
            e["tokens"] += max(0, est_tokens)
            e["cost_usd"] = round(e.get("cost_usd", 0.0) + est_tokens / 1000 * e.get("price_per_1k", 0.0), 6)
            _save(data)


if __name__ == "__main__":
    import sys
    print(json.dumps(status(sys.argv[1] if len(sys.argv) > 1 else None), indent=2))
