#!/usr/bin/env python3
"""
judge.py — score answer documents against a PRIVATE rubric.

Leak guards (deliberate):
  * the rubric MUST live outside this repo; the script exits if the rubric path
    resolves inside the git tree, so it can never be committed or read by agents
  * nothing here is ever inserted into an agent prompt; scoring is post-hoc
  * the rubric file itself is not logged, only its item ids

Usage:
  python3 shared/judge.py --rubric ~/.alt_parallelswarm_private/rubric_snc_disc.json \
                          --docs agents/*/SNC_DISC__WT*/05_FINAL/DISCOVERY_CONFIG_REFERENCE.md
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def in_repo(p: Path) -> bool:
    try:
        p.resolve().relative_to(REPO.resolve())
        return True
    except ValueError:
        return False


def score(doc: str, items: list[dict]) -> dict:
    low = doc.lower()
    # headings only, to tell "mentioned" from "given its own section"
    headings = " \n ".join(
        l.strip("# ").lower() for l in doc.splitlines() if l.lstrip().startswith("#")).lower()

    out = {"items": {}, "passed": 0, "strong": 0}
    for it in items:
        any_hits = sum(len(re.findall(p, low, re.S)) for p in it.get("any", []))
        strong_hits = sum(len(re.findall(p, low, re.S)) for p in it.get("strong", []))
        in_heading = any(re.search(p, headings, re.S) for p in it.get("any", []))
        passed = any_hits > 0
        out["items"][it["id"]] = {
            "label": it["label"],
            "mentions": any_hits,
            "detailed_hits": strong_hits,
            "own_section": in_heading,
            "pass": passed,
            # "quality" = has its own section AND at least one detail/mechanism phrase
            "quality": bool(in_heading and strong_hits),
        }
        out["passed"] += int(passed)
        out["strong"] += int(out["items"][it["id"]]["quality"])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rubric", required=True)
    ap.add_argument("--docs", nargs="+", required=True)
    args = ap.parse_args()

    rp = Path(args.rubric).expanduser()
    if in_repo(rp):
        raise SystemExit(f"REFUSING: rubric {rp} is inside the repo — it would leak to agents.")
    rubric = json.loads(rp.read_text())
    items = rubric["required_items"]

    rows = []
    for d in args.docs:
        p = Path(d)
        if not p.exists():
            rows.append({"doc": str(d), "error": "missing"})
            continue
        doc = p.read_text(encoding="utf-8", errors="replace")
        s = score(doc, items)
        rp_doc = p.resolve()
        s["doc"] = str(rp_doc.relative_to(REPO.resolve()) if in_repo(p) else rp_doc)
        s["chars"] = len(doc)
        s["sources"] = len(set(re.findall(r"https?://[^\s\)\]\"'<>]+", doc)))
        rows.append(s)

    for r in rows:
        if r.get("error"):
            print(f"{r['doc']}: MISSING")
            continue
        agent = Path(r["doc"]).parts[1] if len(Path(r["doc"]).parts) > 1 else r["doc"]
        print(f"\n{agent}")
        print(f"  required items: {r['passed']}/{len(items)} mentioned · "
              f"{r['strong']}/{len(items)} with own section + mechanism · {r['sources']} sources · {r['chars']} chars")
        for k, v in r["items"].items():
            flag = "QUALITY" if v["quality"] else ("mention" if v["pass"] else "MISSING")
            print(f"    {v['label']:22s} {flag:8s} mentions={v['mentions']} detail={v['detailed_hits']} heading={v['own_section']}")

    out = REPO / "shared" / "state" / "rubric_scores.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    # store ids/scores only — never rubric text
    safe = [{k: r.get(k) for k in ("doc", "passed", "strong", "sources", "chars")} |
            {"items": {k: {kk: vv for kk, vv in v.items() if kk != "label"} for k, v in r.get("items", {}).items()}}
            for r in rows if not r.get("error")]
    out.write_text(json.dumps(safe, indent=2))
    print(f"\nscores written to {out.relative_to(REPO)} (ids only, no rubric text)")


if __name__ == "__main__":
    main()
