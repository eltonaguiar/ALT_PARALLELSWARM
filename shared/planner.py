#!/usr/bin/env python3
"""
planner.py — expand a PRIVATE topic map into NEUTRAL research questions.

The graded constructs never appear in the questions. A topic map entry describes
an *area* and the mechanisms that live in it; the planner turns that into questions
a researcher would naturally ask, plus a "does this exist under another name?" probe.

Leak gate: `--check-leak` greps the generated questions against the avoid-terms in
the topic map and refuses to write the file if any of them appear.

  python3 shared/planner.py --map ~/.alt_parallelswarm_private/topic_map_snc_disc.json \
                            --out /tmp/questions.txt --check-leak
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def in_repo(p: Path) -> bool:
    try:
        p.resolve().relative_to(REPO.resolve())
        return True
    except ValueError:
        return False


def build(map_obj: dict, per_topic: int) -> list[str]:
    qs: list[str] = []
    for topic in map_obj.get("topics", []):
        for q in topic.get("neutral_questions", [])[:per_topic]:
            qs.append(q.strip())
        probe = topic.get("probe")
        if probe:
            qs.append(probe.strip())
    # global probes that widen the search surface without naming anything
    qs.extend(map_obj.get("global_probes", []))
    # de-dup, keep order
    seen, out = set(), []
    for q in qs:
        k = q.lower()[:80]
        if k not in seen:
            seen.add(k)
            out.append(q)
    return out


def leaks(questions: list[str], avoid: list[str]) -> list[str]:
    blob = "\n".join(questions).lower()
    return [t for t in avoid if re.search(re.escape(t.lower()), blob)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--map", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--per-topic", type=int, default=2)
    ap.add_argument("--check-leak", action="store_true")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    mp = Path(args.map).expanduser()
    if in_repo(mp):
        raise SystemExit(f"REFUSING: topic map {mp} is inside the repo — it would leak to agents.")
    obj = json.loads(mp.read_text())
    questions = build(obj, args.per_topic)

    bad = leaks(questions, obj.get("avoid_terms", [])) if args.check_leak else []
    if bad:
        print(f"LEAK GATE FAILED — {len(bad)} avoid-term(s) present in generated questions: {bad}")
        print("Rewrite the neutral questions; nothing written.")
        if not args.force:
            raise SystemExit(2)

    out = Path(args.out).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(questions) + "\n", encoding="utf-8")
    print(json.dumps({"questions": len(questions), "written": str(out),
                      "leak_check": "pass" if args.check_leak and not bad else "skipped",
                      "first": questions[0][:110]}))


if __name__ == "__main__":
    main()
