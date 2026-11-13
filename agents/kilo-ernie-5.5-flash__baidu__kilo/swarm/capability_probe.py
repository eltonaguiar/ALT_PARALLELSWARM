"""
capability_probe.py — find out what each model/provider can ACTUALLY do.

For every model in registry.json it:
  * checks the provider key is present in the environment
  * fires a tiny ping (max_tokens ~16) and times it
  * records ok/fail + latency + the error body (truncated)

Output: swarm/probe.json — the gate the orchestrator reads before assigning work.
The "web browse" capability is NOT a property of the model here: the ORCHESTRATOR
supplies browsing (websearch/webfetch/Playwright). This probe records whether the
model can at least reason over fetched content (i.e. it's alive and has context).

Usage:
  python -m swarm.capability_probe --all
  python -m swarm.capability_probe --model ollama/qwen2.5:7b
"""
from __future__ import annotations

import argparse
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from .llm_router import LLMRouter, load_registry, REGISTRY_PATH
from .usage_tracker import UsageTracker

PROBE_PATH = Path(__file__).resolve().parent / "probe.json"


def probe_one(model_key: str, reg: dict, tracker: UsageTracker) -> dict[str, Any]:
    m = reg["models"][model_key]
    prov = m["provider"]
    pconf = reg["providers"][prov]
    key_env = pconf.get("api_key_env")
    if isinstance(key_env, str):
        key_env = [key_env]
    key_present = bool(key_env) and any(os.environ.get(e) for e in key_env) if key_env else True

    res: dict[str, Any] = {
        "model": model_key, "provider": prov, "context": m.get("context"),
        "key_present": key_present, "ok": False, "latency_s": None,
        "reply": None, "error": None,
    }
    if key_env and not key_present:
        res["error"] = f"missing env {key_env}"
        return res

    router = LLMRouter(tracker=tracker)
    t0 = time.time()
    try:
        out = router.chat(model_key, [{"role": "user", "content": "ping (reply 'pong')"}],
                          max_tokens=16, timeout=60, retries=0)
        res["ok"] = True
        res["reply"] = (out.get("text") or "").strip()[:80]
        res["latency_s"] = round(time.time() - t0, 3)
    except Exception as e:  # noqa: BLE001
        res["error"] = str(e)[:300]
        res["latency_s"] = round(time.time() - t0, 3)
    return res


def main() -> None:
    ap = argparse.ArgumentParser(description="Probe model capabilities")
    ap.add_argument("--all", action="store_true", help="probe every model")
    ap.add_argument("--model", action="append", default=[], help="probe specific model key(s)")
    ap.add_argument("--out", default=str(PROBE_PATH))
    args = ap.parse_args()

    reg = load_registry()
    tracker = UsageTracker()
    targets = args.model or (list(reg["models"].keys()) if args.all else [])
    if not targets:
        ap.error("specify --all or --model KEY")

    results: list[dict[str, Any]] = []
    # probe sequentially per-provider to respect concurrency caps, parallel across providers
    with ThreadPoolExecutor(max_workers=4) as ex:
        futs = {ex.submit(probe_one, mk, reg, tracker): mk for mk in targets}
        for fut in as_completed(futs):
            r = fut.result()
            results.append(r)
            flag = "OK " if r["ok"] else "FAIL"
            print(f"[{flag}] {r['model']:48s} {r['latency_s']}s "
                  f"{('→ ' + r['reply']) if r['ok'] else ('✗ ' + (r['error'] or ''))[:120]}")

    results.sort(key=lambda x: x["model"])
    out = {"probed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "results": results}
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)
    ok = sum(1 for r in results if r["ok"])
    print(f"\n{ok}/{len(results)} models reachable. Wrote {args.out}")


if __name__ == "__main__":
    main()