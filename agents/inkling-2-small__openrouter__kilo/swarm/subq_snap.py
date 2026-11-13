#!/usr/bin/env python3
"""
subq_snap.py — SubQ Snap Decisions API client (model subq-snap-1.2).

Snap is typed decisions (noul/choice/score) with probabilities, not chat.
Pricing: input $0.04/1M tokens, output free. Every account (no early-access gate).

Usage:
  python3 subq_snap.py status
  python3 subq_snap.py smoke            # 1 tiny call, requires SUBQ_FREE_API_KEY or SUBQ_API_KEY
"""
from __future__ import annotations
import fcntl, json, os, sys, time, urllib.request, datetime
from pathlib import Path

STATE = Path(__file__).resolve().parent / "state"; STATE.mkdir(exist_ok=True)
LEDGER = STATE / "swarm_ledger.json"; LOCK = STATE / "swarm.lock"

PRICE_IN_1K = 0.00004  # $0.04 / 1M input tokens
DEFAULTS = {"inflight": 0, "day": "", "calls": 0, "tokens": 0, "tokens_actual": 0,
            "cost_usd": 0.0, "cost_actual_usd": 0.0, "max_inflight": 2,
            "daily_calls": 100, "daily_tokens": 200_000, "price_per_1k": 0.0}

from contextlib import contextmanager
@contextmanager
def locked():
    with open(LOCK, "w") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        try: yield
        finally: fcntl.flock(fh, fcntl.LOCK_UN)

def _load():
    if LEDGER.exists():
        try: return json.loads(LEDGER.read_text())
        except Exception: pass
    return {"providers": {}}

def _save(d): LEDGER.write_text(json.dumps(d, indent=2))

def _roll(e):
    today = datetime.date.today().isoformat()
    if e.get("day") != today: e.update(day=today, calls=0, tokens=0, tokens_actual=0, cost_usd=0.0, cost_actual_usd=0.0)
    for k, v in DEFAULTS.items(): e.setdefault(k, v)
    return e

def status():
    with locked():
        d = _load(); e = _roll(d.setdefault("providers", {}).setdefault("subq_snap", {}))
        e["present"] = bool(os.environ.get("SUBQ_FREE_API_KEY") or os.environ.get("SUBQ_API_KEY"))
        _save(d); return e

def key():
    return os.environ.get("SUBQ_FREE_API_KEY") or os.environ.get("SUBQ_API_KEY")

def decide(state, questions, timeout=45, max_wait_s=600):
    k = key()
    if not k: raise RuntimeError("NO_KEY subq_snap (set SUBQ_FREE_API_KEY or SUBQ_API_KEY)")
    with locked():
        d = _load(); e = _roll(d.setdefault("providers", {}).setdefault("subq_snap", {}))
        if e["inflight"] >= e["max_inflight"]: raise RuntimeError(f"BUSY subq_snap {e['inflight']}/{e['max_inflight']}")
        if e["calls"] + 1 > e["daily_calls"]: raise RuntimeError(f"DAILY_CAP subq_snap {e['calls']}/{e['daily_calls']}")
        e["inflight"] += 1; e["calls"] += 1; _save(d)
    try:
        body = json.dumps({"model": "subq-snap-1.2", "state": state, "questions": questions}).encode()
        req = urllib.request.Request("https://api.subq.ai/v1/systemone", data=body,
            headers={"Authorization": f"Bearer {k}", "Content-Type": "application/json"})
        t0 = time.time()
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read())
        dt = time.time() - t0
        usage = data.get("usage") or {}
        with locked():
            d = _load(); e = _roll(d.setdefault("providers", {}).setdefault("subq_snap", {}))
            it = usage.get("input_tokens", 0); e["tokens_actual"] = e.get("tokens_actual", 0) + it
            e["cost_actual_usd"] = round(e.get("cost_actual_usd", 0.0) + it * PRICE_IN_1K / 1000, 6)
            _save(d)
        return {"latency_s": round(dt, 2), "answers": data.get("answers"), "usage": usage}
    finally:
        with locked():
            d = _load(); e = _roll(d.setdefault("providers", {}).setdefault("subq_snap", {}))
            e["inflight"] = max(0, e["inflight"] - 1); _save(d)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        print(json.dumps(status(), indent=2))
    elif len(sys.argv) > 1 and sys.argv[1] == "smoke":
        print(json.dumps(decide("The CI name is the same across two discovery sources.",
            {"duplicate": {"type": "noul",
                           "instructions": "Is this text about a duplicate CI?",
                           "criteria": {"true": "Mentions duplication/dedup", "false": "Unrelated"}}}), indent=2))
    else:
        print(__doc__)
