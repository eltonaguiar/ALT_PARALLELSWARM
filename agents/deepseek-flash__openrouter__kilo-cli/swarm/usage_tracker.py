#!/usr/bin/env python3
"""Concurrency + daily-usage + cost ledger for free/paid model providers.

The ledger is a single JSON file guarded by an fcntl lock so multiple worker
processes cannot race the counters. API keys are never stored; only the name of
the environment variable and a short SHA-256 fingerprint are recorded.
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import time
from contextlib import contextmanager
from datetime import date, datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_LEDGER = HERE / "state" / "usage_ledger.json"
DEFAULT_LOCK = HERE / "state" / "usage.lock"
REGISTRY = HERE / "registry.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def key_fingerprint(env_name: str) -> str:
    value = os.environ.get(env_name, "") if env_name else ""
    if not value:
        return "local"
    return hashlib.sha256(value.encode()).hexdigest()[:8]


class Ledger:
    def __init__(self, path: Path | str = DEFAULT_LEDGER, registry: Path | str = REGISTRY):
        self.path = Path(path)
        self.lock_path = self.path.with_suffix(".lock")
        self.registry_path = Path(registry)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _registry(self) -> dict:
        with open(self.registry_path) as fh:
            return json.load(fh).get("providers", {})

    def _ensure(self) -> None:
        if not self.path.exists():
            self.path.write_text(json.dumps({"providers": {}}, indent=2))

    @contextmanager
    def _locked(self):
        self._ensure()
        with open(self.lock_path, "w") as fh:
            fcntl.flock(fh, fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(fh, fcntl.LOCK_UN)

    def _load(self) -> dict:
        self._ensure()
        try:
            return json.loads(self.path.read_text())
        except Exception:
            return {"providers": {}}

    def _save(self, data: dict) -> None:
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=2))
        tmp.replace(self.path)

    def _entry(self, data: dict, provider: str) -> dict:
        defaults = self._registry().get(provider, {})
        entry = data.setdefault("providers", {}).setdefault(provider, {})
        today = date.today().isoformat()
        if entry.get("day") != today:
            entry.update(day=today, calls=0, tokens=0, cost_usd=0.0)
        entry.setdefault("inflight", 0)
        for key in ("max_inflight", "daily_calls", "daily_tokens", "price_per_1k"):
            if key in defaults:
                entry.setdefault(key, defaults[key])
        entry.setdefault("max_inflight", 1)
        entry.setdefault("daily_calls", 100)
        entry.setdefault("daily_tokens", 100_000)
        entry.setdefault("price_per_1k", 0.0)
        entry.setdefault("key_env", defaults.get("api_key_env", ""))
        entry.setdefault("key_fingerprint", key_fingerprint(defaults.get("api_key_env", "")))
        entry.setdefault("last_used", None)
        return entry

    def status(self, provider: str | None = None) -> dict:
        with self._locked():
            data = self._load()
            if provider:
                entry = self._entry(data, provider)
                self._save(data)
                return {provider: entry}
            for name in list(data.get("providers", {})):
                data["providers"][name] = self._entry(data, name)
            self._save(data)
            return data.get("providers", {})

    @contextmanager
    def acquire(self, provider: str, est_tokens: int = 4000, wait_s: int = 900):
        """Reserve one call slot, or block until a slot/quota is available."""
        deadline = time.time() + wait_s
        lease = {"provider": provider, "tokens": 0, "cost_usd": 0.0, "estimated": est_tokens}
        while True:
            with self._locked():
                data = self._load()
                entry = self._entry(data, provider)
                if entry["calls"] + 1 > entry["daily_calls"]:
                    self._save(data)
                    raise RuntimeError(
                        f"BUDGET_EXHAUSTED provider={provider} "
                        f"calls={entry['calls']}/{entry['daily_calls']}")
                if entry["tokens"] + est_tokens > entry["daily_tokens"]:
                    self._save(data)
                    raise RuntimeError(
                        f"BUDGET_EXHAUSTED provider={provider} "
                        f"tokens={entry['tokens']}+{est_tokens}/{entry['daily_tokens']}")
                if entry["inflight"] < entry["max_inflight"]:
                    entry["inflight"] += 1
                    entry["calls"] += 1
                    entry["last_used"] = utc_now()
                    self._save(data)
                    break
                self._save(data)
            if time.time() > deadline:
                raise TimeoutError(f"BUDGET_TIMEOUT provider={provider} wait_s={wait_s}")
            time.sleep(1.0)
        try:
            yield lease
        finally:
            with self._locked():
                data = self._load()
                entry = self._entry(data, provider)
                entry["inflight"] = max(0, entry["inflight"] - 1)
                tokens = int(lease.get("tokens") or lease.get("estimated") or 0)
                entry["tokens"] += max(0, tokens)
                rate = float(entry.get("price_per_1k", 0.0) or 0.0)
                lease["cost_usd"] = round(tokens / 1000.0 * rate, 6)
                entry["cost_usd"] = round(float(entry.get("cost_usd", 0.0)) + lease["cost_usd"], 6)
                self._save(data)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--provider")
    parser.add_argument("--ledger", default=str(DEFAULT_LEDGER))
    parser.add_argument("--reset", action="store_true")
    args = parser.parse_args()
    ledger = Ledger(args.ledger)
    if args.reset:
        ledger.path.write_text(json.dumps({"providers": {}}, indent=2))
        print(f"reset {ledger.path}")
        return
    print(json.dumps(ledger.status(args.provider), indent=2))


if __name__ == "__main__":
    main()
