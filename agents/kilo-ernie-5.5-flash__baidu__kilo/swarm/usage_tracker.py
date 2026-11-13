"""
usage_tracker.py — thread-safe, file-backed usage ledger for the swarm.

Tracks, per provider:
  * current concurrency (in-flight calls) and a hard max
  * requests today, tokens today, estimated cost today
  * a rolling log of calls (jsonl) for audit

Free-tier safety: before a call starts, `can_start(provider)` checks concurrency and
daily caps. `acquire()`/`release()` bracket a call; `record()` books the usage.

Storage: a single JSON file guarded by an flock() lock so multiple processes/threads
in the swarm don't corrupt it. No third-party deps.
"""
from __future__ import annotations

import fcntl
import json
import os
import time
from contextlib import contextmanager
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_PATH = Path(__file__).resolve().parent / "usage_tracker.json"
LOG_PATH = Path(__file__).resolve().parent / "usage_log.jsonl"


def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


@dataclass
class ProviderState:
    max_concurrent: int = 2
    max_requests_per_day: int = 1000
    max_tokens_per_day: int = 1_000_000
    max_cost_per_day: float = 1.0
    concurrent: int = 0
    day: str = field(default_factory=_today)
    requests: int = 0
    tokens: int = 0
    cost: float = 0.0
    total_requests: int = 0
    total_tokens: int = 0


class UsageTracker:
    def __init__(self, path: Path | str = DEFAULT_PATH, log_path: Path | str = LOG_PATH):
        self.path = Path(path)
        self.log_path = Path(log_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write(self._blank())

    # ---- low level file io with an exclusive lock -------------------------
    @contextmanager
    def _locked(self):
        # separate lock file so we never hold the data file open for writing
        lock_path = self.path.with_suffix(self.path.suffix + ".lock")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(lock_path, "w") as lf:
            fcntl.flock(lf, fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(lf, fcntl.LOCK_UN)

    def _blank(self) -> dict[str, Any]:
        return {"providers": {}, "updated": _today()}

    def _read(self) -> dict[str, Any]:
        try:
            with open(self.path) as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return self._blank()

    def _write(self, data: dict[str, Any]) -> None:
        data["updated"] = datetime.now(timezone.utc).isoformat()
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        with open(tmp, "w") as f:
            json.dump(data, f, indent=2)
        os.replace(tmp, self.path)

    # ---- rolling day rollover --------------------------------------------
    def _roll(self, state: ProviderState) -> ProviderState:
        if state.day != _today():
            state.day = _today()
            state.requests = 0
            state.tokens = 0
            state.cost = 0.0
        return state

    def _state(self, data: dict[str, Any], provider: str) -> ProviderState:
        raw = data["providers"].get(provider)
        if raw is None:
            return ProviderState()
        st = ProviderState(**raw)
        return self._roll(st)

    # ---- public API -------------------------------------------------------
    def can_start(self, provider: str) -> tuple[bool, str]:
        with self._locked():
            data = self._read()
            st = self._state(data, provider)
            if st.concurrent >= st.max_concurrent:
                return False, f"concurrency {st.concurrent}/{st.max_concurrent}"
            # a cap of 0 means "no cap" (e.g. free providers with $0 cost ceiling)
            if st.max_requests_per_day > 0 and st.requests >= st.max_requests_per_day:
                return False, f"daily requests {st.requests}/{st.max_requests_per_day}"
            if st.max_tokens_per_day > 0 and st.tokens >= st.max_tokens_per_day:
                return False, f"daily tokens {st.tokens}/{st.max_tokens_per_day}"
            if st.max_cost_per_day > 0 and st.cost >= st.max_cost_per_day:
                return False, f"daily cost ${st.cost:.4f}/${st.max_cost_per_day}"
            return True, "ok"

    def acquire(self, provider: str) -> bool:
        ok, _ = self.can_start(provider)
        if not ok:
            return False
        with self._locked():
            data = self._read()
            st = self._state(data, provider)
            st.concurrent += 1
            data["providers"][provider] = asdict(st)
            self._write(data)
        return True

    def release(self, provider: str) -> None:
        with self._locked():
            data = self._read()
            st = self._state(data, provider)
            st.concurrent = max(0, st.concurrent - 1)
            data["providers"][provider] = asdict(st)
            self._write(data)

    def record(self, provider: str, tokens: int = 0, cost: float = 0.0,
               model: str = "", note: str = "") -> None:
        with self._locked():
            data = self._read()
            st = self._state(data, provider)
            st.requests += 1
            st.total_requests += 1
            st.tokens += tokens
            st.total_tokens += tokens
            st.cost += cost
            data["providers"][provider] = asdict(st)
            self._write(data)
        self._append_log(provider, tokens, cost, model, note)

    def _append_log(self, provider, tokens, cost, model, note):
        rec = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "provider": provider,
            "model": model,
            "tokens": tokens,
            "cost": round(cost, 6),
            "note": note,
        }
        with open(self.log_path, "a") as f:
            f.write(json.dumps(rec) + "\n")

    def report(self) -> dict[str, Any]:
        with self._locked():
            data = self._read()
            out = {}
            for prov, raw in data["providers"].items():
                st = self._state(data, prov)
                out[prov] = asdict(st)
            return out

    def set_caps(self, provider: str, **caps) -> None:
        """Override caps, e.g. set_caps('groq', max_requests_per_day=200)."""
        with self._locked():
            data = self._read()
            st = self._state(data, provider)
            for k, v in caps.items():
                if hasattr(st, k):
                    setattr(st, k, v)
            data["providers"][provider] = asdict(st)
            self._write(data)


# ---- CLI -----------------------------------------------------------------
def _cli() -> None:
    import argparse
    ap = argparse.ArgumentParser(description="Swarm usage tracker")
    ap.add_argument("--report", action="store_true", help="print current usage")
    ap.add_argument("--reset", metavar="PROVIDER", help="reset a provider's daily counters")
    ap.add_argument("--cap", nargs=3, metavar=("PROVIDER", "KEY", "VALUE"),
                    help="set a cap e.g. --cap groq max_requests_per_day 200")
    ap.add_argument("--path", default=str(DEFAULT_PATH))
    args = ap.parse_args()
    t = UsageTracker(args.path)
    if args.report:
        print(json.dumps(t.report(), indent=2))
    if args.reset:
        t.set_caps(args.reset, requests=0, tokens=0, cost=0.0)
        print(f"reset {args.reset}")
    if args.cap:
        prov, key, val = args.cap
        val = float(val) if "." in val else int(val)
        t.set_caps(prov, **{key: val})
        print(f"set {prov}.{key}={val}")


if __name__ == "__main__":
    _cli()