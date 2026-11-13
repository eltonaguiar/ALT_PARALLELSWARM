#!/usr/bin/env python3
"""
usage_tracker.py — concurrency + daily-usage + cost ledger for a model swarm.

Why SQLite instead of a JSON file:
  * atomic reservations under concurrent threads/processes (BEGIN IMMEDIATE)
  * survives crashes better than read-modify-write JSON
  * cheap per-event audit trail

Model: reserve a slot + one call BEFORE the request, then release with the
actual token usage afterwards. That prevents N workers from stampeding one
free key while still recording real usage.

Usage:
    python3 usage_tracker.py --status
    python3 usage_tracker.py --repair                 # clear stale inflight
    python3 usage_tracker.py --reset-today ollama
    python3 usage_tracker.py --configure ollama \
        --max-inflight 2 --daily-calls 1000 --daily-tokens 5000000 \
        --price-in 0 --price-out 0

Environment:
    SWARM_LEDGER   path to sqlite file (default: ./state/usage.sqlite3)
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import time
from contextlib import contextmanager
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
LEDGER = Path(os.environ.get("SWARM_LEDGER", ROOT / "state" / "usage.sqlite3"))


class BudgetExhausted(RuntimeError):
    pass


class BudgetTimeout(TimeoutError):
    pass


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _conn() -> sqlite3.Connection:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(str(LEDGER), timeout=30, isolation_level=None)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("PRAGMA busy_timeout=30000")
    return c


def init() -> None:
    with _conn() as c:
        c.execute(
            """CREATE TABLE IF NOT EXISTS providers (
                   name TEXT PRIMARY KEY,
                   max_inflight INTEGER NOT NULL DEFAULT 1,
                   daily_calls INTEGER NOT NULL DEFAULT 1000,
                   daily_tokens INTEGER NOT NULL DEFAULT 1000000,
                   price_in_per_1k REAL NOT NULL DEFAULT 0,
                   price_out_per_1k REAL NOT NULL DEFAULT 0
               )"""
        )
        c.execute(
            """CREATE TABLE IF NOT EXISTS usage (
                   provider TEXT NOT NULL,
                   day TEXT NOT NULL,
                   calls INTEGER NOT NULL DEFAULT 0,
                   tokens_in INTEGER NOT NULL DEFAULT 0,
                   tokens_out INTEGER NOT NULL DEFAULT 0,
                   cost_usd REAL NOT NULL DEFAULT 0,
                   inflight INTEGER NOT NULL DEFAULT 0,
                   PRIMARY KEY (provider, day)
               )"""
        )
        c.execute(
            """CREATE TABLE IF NOT EXISTS events (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   ts TEXT NOT NULL,
                   provider TEXT NOT NULL,
                   model TEXT,
                   status TEXT NOT NULL,
                   tokens_in INTEGER NOT NULL DEFAULT 0,
                   tokens_out INTEGER NOT NULL DEFAULT 0,
                   cost_usd REAL NOT NULL DEFAULT 0,
                   note TEXT
               )"""
        )


def configure(
    provider: str,
    *,
    max_inflight: int | None = None,
    daily_calls: int | None = None,
    daily_tokens: int | None = None,
    price_in_per_1k: float | None = None,
    price_out_per_1k: float | None = None,
) -> dict[str, Any]:
    init()
    with _conn() as c:
        c.execute(
            "INSERT OR IGNORE INTO providers(name) VALUES (?)", (provider,)
        )
        sets, vals = [], []
        for col, val in (
            ("max_inflight", max_inflight),
            ("daily_calls", daily_calls),
            ("daily_tokens", daily_tokens),
            ("price_in_per_1k", price_in_per_1k),
            ("price_out_per_1k", price_out_per_1k),
        ):
            if val is not None:
                sets.append(f"{col}=?")
                vals.append(val)
        if sets:
            c.execute(
                f"UPDATE providers SET {', '.join(sets)} WHERE name=?", (*vals, provider)
            )
    return provider_status(provider)


def _roll(c: sqlite3.Connection, provider: str, today: str) -> sqlite3.Row:
    c.execute("INSERT OR IGNORE INTO providers(name) VALUES (?)", (provider,))
    c.execute(
        "INSERT OR IGNORE INTO usage(provider, day) VALUES (?, ?)", (provider, today)
    )
    return c.execute(
        "SELECT * FROM usage WHERE provider=? AND day=?", (provider, today)
    ).fetchone()


def provider_status(provider: str) -> dict[str, Any]:
    init()
    today = date.today().isoformat()
    with _conn() as c:
        row = _roll(c, provider, today)
        cfg = c.execute(
            "SELECT * FROM providers WHERE name=?", (provider,)
        ).fetchone()
    return {
        "provider": provider,
        "day": today,
        "calls": row["calls"],
        "tokens_in": row["tokens_in"],
        "tokens_out": row["tokens_out"],
        "tokens": row["tokens_in"] + row["tokens_out"],
        "cost_usd": round(row["cost_usd"], 6),
        "inflight": row["inflight"],
        "max_inflight": cfg["max_inflight"],
        "daily_calls": cfg["daily_calls"],
        "daily_tokens": cfg["daily_tokens"],
        "price_in_per_1k": cfg["price_in_per_1k"],
        "price_out_per_1k": cfg["price_out_per_1k"],
    }


def status() -> dict[str, Any]:
    init()
    with _conn() as c:
        names = [r["name"] for r in c.execute("SELECT name FROM providers ORDER BY name")]
    if not names:
        return {"ledger": str(LEDGER), "day": date.today().isoformat(), "providers": {}}
    return {
        "ledger": str(LEDGER),
        "day": date.today().isoformat(),
        "providers": {n: provider_status(n) for n in names},
    }


class Reservation:
    """Idempotent release handle returned by acquire()."""

    def __init__(self, provider: str, model: str):
        self.provider = provider
        self.model = model
        self.released = False
        self.started = time.time()

    def release(
        self,
        *,
        tokens_in: int = 0,
        tokens_out: int = 0,
        status: str = "ok",
        note: str = "",
    ) -> dict[str, Any]:
        if self.released:
            return provider_status(self.provider)
        self.released = True
        return _release(
            self.provider,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            model=self.model,
            status=status,
            note=note or f"slot held {time.time() - self.started:.1f}s",
        )


@contextmanager
def acquire(
    provider: str,
    *,
    est_tokens: int = 4000,
    wait_s: int = 900,
    model: str = "",
):
    """Reserve one in-flight slot and one call, or block until allowed.

    Yields a Reservation. Call `res.release(tokens_in=..., tokens_out=...)`
    after the request; the context manager also releases with zero usage on
    exit if you forget, so a slot cannot leak on an exception.

    Raises BudgetExhausted when the daily cap would be exceeded.
    Raises BudgetTimeout if no slot frees up within wait_s seconds.
    """
    init()
    deadline = time.time() + wait_s
    today = date.today().isoformat()

    while True:
        c = _conn()
        try:
            c.execute("BEGIN IMMEDIATE")
            row = _roll(c, provider, today)
            cfg = c.execute(
                "SELECT * FROM providers WHERE name=?", (provider,)
            ).fetchone()
            if row["calls"] + 1 > cfg["daily_calls"]:
                c.execute("ROLLBACK")
                raise BudgetExhausted(
                    f"{provider}: daily call cap reached "
                    f"({row['calls']}/{cfg['daily_calls']})"
                )
            if row["tokens_in"] + row["tokens_out"] + est_tokens > cfg["daily_tokens"]:
                c.execute("ROLLBACK")
                raise BudgetExhausted(
                    f"{provider}: daily token cap would be exceeded "
                    f"({row['tokens_in'] + row['tokens_out']}+{est_tokens}"
                    f"/{cfg['daily_tokens']})"
                )
            if row["inflight"] < cfg["max_inflight"]:
                c.execute(
                    "UPDATE usage SET inflight=inflight+1, calls=calls+1 "
                    "WHERE provider=? AND day=?",
                    (provider, today),
                )
                c.execute("COMMIT")
                break
            c.execute("COMMIT")
        finally:
            c.close()

        if time.time() > deadline:
            raise BudgetTimeout(
                f"{provider}: no slot within {wait_s}s "
                f"(max_inflight={cfg['max_inflight']})"
            )
        time.sleep(1.5)

    res = Reservation(provider, model)
    try:
        yield res
    finally:
        res.release(status="no-usage", note="released without measured usage")


def _release(
    provider: str,
    *,
    tokens_in: int = 0,
    tokens_out: int = 0,
    model: str = "",
    status: str = "ok",
    note: str = "",
) -> dict[str, Any]:
    init()
    today = date.today().isoformat()
    with _conn() as c:
        _roll(c, provider, today)
        cfg = c.execute(
            "SELECT * FROM providers WHERE name=?", (provider,)
        ).fetchone()
        tokens_in = max(0, int(tokens_in))
        tokens_out = max(0, int(tokens_out))
        cost = (
            tokens_in / 1000 * cfg["price_in_per_1k"]
            + tokens_out / 1000 * cfg["price_out_per_1k"]
        )
        c.execute(
            """UPDATE usage SET inflight=MAX(0, inflight-1),
                   tokens_in=tokens_in+?, tokens_out=tokens_out+?,
                   cost_usd=cost_usd+?
               WHERE provider=? AND day=?""",
            (tokens_in, tokens_out, cost, provider, today),
        )
        c.execute(
            """INSERT INTO events(ts,provider,model,status,tokens_in,tokens_out,cost_usd,note)
               VALUES (?,?,?,?,?,?,?,?)""",
            (_now(), provider, model, status, tokens_in, tokens_out, cost, note),
        )
    return provider_status(provider)


def release(
    provider: str,
    *,
    tokens_in: int = 0,
    tokens_out: int = 0,
    model: str = "",
    status: str = "ok",
    note: str = "",
) -> dict[str, Any]:
    """Direct release; prefer Reservation.release() from acquire()."""
    return _release(
        provider,
        tokens_in=tokens_in,
        tokens_out=tokens_out,
        model=model,
        status=status,
        note=note,
    )


def repair() -> dict[str, Any]:
    """Zero today's inflight counters (use only when no workers are running)."""
    init()
    today = date.today().isoformat()
    with _conn() as c:
        c.execute("UPDATE usage SET inflight=0 WHERE day=?", (today,))
    return status()


def reset_today(provider: str) -> dict[str, Any]:
    init()
    today = date.today().isoformat()
    with _conn() as c:
        c.execute(
            """UPDATE usage SET calls=0, tokens_in=0, tokens_out=0,
                   cost_usd=0, inflight=0
               WHERE provider=? AND day=?""",
            (provider, today),
        )
    return provider_status(provider)


def main() -> None:
    p = argparse.ArgumentParser(description="Swarm usage/cost ledger")
    p.add_argument("--status", action="store_true", help="print JSON status")
    p.add_argument("--repair", action="store_true", help="zero today's inflight")
    p.add_argument("--reset-today", metavar="PROVIDER")
    p.add_argument("--configure", metavar="PROVIDER")
    p.add_argument("--max-inflight", type=int)
    p.add_argument("--daily-calls", type=int)
    p.add_argument("--daily-tokens", type=int)
    p.add_argument("--price-in", type=float, dest="price_in_per_1k")
    p.add_argument("--price-out", type=float, dest="price_out_per_1k")
    a = p.parse_args()

    if a.configure:
        out = configure(
            a.configure,
            max_inflight=a.max_inflight,
            daily_calls=a.daily_calls,
            daily_tokens=a.daily_tokens,
            price_in_per_1k=a.price_in_per_1k,
            price_out_per_1k=a.price_out_per_1k,
        )
    elif a.reset_today:
        out = reset_today(a.reset_today)
    elif a.repair:
        out = repair()
    else:
        out = status()
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
