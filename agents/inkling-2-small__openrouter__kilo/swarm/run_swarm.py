#!/usr/bin/env python3
"""Dispatch one bounded research cross-check to free providers in parallel; log everything."""
import json, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import free_keys

PROMPT = (
    "Context: ServiceNow Discovery writes CIs to the CMDB via the Identification and Reconciliation "
    "Engine (IRE). In <=120 words, list the controls that prevent duplicate CIs, and say whether each "
    "is a system property, an IRE rule type, or a CMDB Health/remediation feature. Be terse; bullet list."
)
MSG = [{"role": "user", "content": PROMPT}]
RESULTS = Path(__file__).parent / "results"; RESULTS.mkdir(exist_ok=True)

def one(provider):
    try:
        r = free_keys.chat(provider, MSG, max_tokens=900, timeout=120)
        r["ok"] = True
    except Exception as e:
        r = {"provider": provider, "ok": False, "error": f"{type(e).__name__}: {e}"[:400]}
    (RESULTS / f"{provider}.json").write_text(json.dumps(r, indent=2))
    return r

t0 = time.time()
providers = sys.argv[1:] or list(free_keys.PROVIDERS)
with ThreadPoolExecutor(max_workers=6) as ex:
    results = list(ex.map(one, providers))
out = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "wall_s": round(time.time() - t0, 2),
       "prompt": PROMPT, "results": results}
out["ok_count"] = sum(1 for r in results if r.get("ok"))
(RESULTS / "swarm_run.json").write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
