#!/usr/bin/env python3
"""
agent_runner.py — one agent, one worktree, full documented lifecycle.

Folder contract (per the ALT_PARALLELSWARM convention):
  agents/<agent_id>/SNC_DISC__WT<n>/
    00_PREREQ/PREREQ.md            capability gate (browse? playwright? context?)
    01_PLAN/PLAN.md                goal, output format, phases, risks, success criteria
    02_CLARIFICATIONS/CLARIFY.md   what it needs from others / whether blocked
    03_PHASES/phaseN_*.md          heartbeat per phase so the orchestrator can see progress
    04_QA/QA.md                    self-check against success criteria
    05_FINAL/FINAL_SUMMARY.md      goal achieved? blockers? clarifications?
    06_FILESCOPE/FILESCOPE.md      files written, branch, worktree path
    research/                      raw harness transcripts + ANSWER.md
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

SHARED = Path(__file__).resolve().parent
REPO = SHARED.parent
sys.path.insert(0, str(SHARED))
import budget  # noqa: E402

TASK = "SNC_DISC_RESEARCH"

QUESTIONS = [
    ("q1_config", "What are the ServiceNow Discovery configuration options and properties, and in what order "
                  "does Discovery processing happen (order of operations) when a device is discovered?"),
    ("q2_classmgr", "What can you configure in the ServiceNow CI Class Manager related to Discovery, "
                    "identification and reconciliation, and where in the interface are those settings?"),
    ("q3_dupes", "How do you configure ServiceNow to avoid duplicate CIs and to control whether an existing CI "
                 "is updated versus a new CI inserted into the CMDB?"),
]

TOPICS = {
    "configuration_options": r"propert|parameter|conf(ig|igure)",
    "order_of_operations": r"order of operation|sequence|first|then|phase",
    "ci_class_manager": r"ci class manager|class manager|cmdb class",
    "duplicates": r"duplicat|de-?dup",
    "insert_vs_update": r"insert|update|create",
    "identification": r"identif",
    "reconciliation": r"reconcil",
    "mid_server": r"mid ?server",
}


def mark(phase_dir: Path, n: int, name: str, detail: str):
    (phase_dir / f"phase{n}_{name}.md").write_text(
        f"# Phase {n} — {name}\n\n{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}\n\n{detail}\n",
        encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent-id", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--provider", required=True)
    ap.add_argument("--base-url", default="http://localhost:11434/v1")
    ap.add_argument("--api-key", default="")
    ap.add_argument("--wt", required=True, help="worktree path")
    ap.add_argument("--wt-num", default="1")
    ap.add_argument("--rounds", default="4")
    args = ap.parse_args()

    root = Path(args.wt) / "agents" / args.agent_id / f"SNC_DISC__WT{args.wt_num}"
    for sub in ("00_PREREQ", "01_PLAN", "02_CLARIFICATIONS", "03_PHASES", "04_QA", "05_FINAL",
                "06_FILESCOPE", "research"):
        (root / sub).mkdir(parents=True, exist_ok=True)
    phases = root / "03_PHASES"

    mark(phases, 1, "started", f"Agent `{args.agent_id}` started.\nModel: `{args.model}`\nProvider: `{args.provider}`")

    # ---- phase 1: capability gate -------------------------------------------------
    pr = subprocess.run([sys.executable, str(SHARED / "prereq_probe.py"),
                         "--out", str(root / "00_PREREQ"), "--agent", args.agent_id,
                         "--model", args.model, "--base-url", args.base_url,
                         "--api-key", args.api_key],
                        capture_output=True, text=True, timeout=600)
    try:
        cap = json.loads(pr.stdout.strip().splitlines()[-1])
    except Exception:
        cap = {"can_browse": False, "context": 0, "checks": {}, "error": pr.stdout[-200:] + pr.stderr[-200:]}
    can_browse = bool(cap.get("can_browse"))
    ctx = int(cap.get("context") or 0)

    # ---- plan ---------------------------------------------------------------------
    (root / "01_PLAN" / "PLAN.md").write_text(f"""# Plan — {TASK}

**Agent:** `{args.agent_id}`
**Model / provider:** `{args.model}` / `{args.provider}`
**Worktree:** `{args.wt}` → folder `agents/{args.agent_id}/SNC_DISC__WT{args.wt_num}`

## Goal
Produce as thorough a technical reference as possible on **ServiceNow Discovery configuration**:
configuration options and properties, order of operations, the key bread crumbs under **CI Class Manager**,
and the configuration that prevents **duplicate CIs** and governs **insert vs update** of CMDB records.

## Output format
`05_FINAL/DISCOVERY_CONFIG_REFERENCE.md` — markdown, headed sections, every factual claim carrying a source URL
or marked `UNVERIFIED`. Plus `04_QA/QA.md` self-scoring and `05_FINAL/FINAL_SUMMARY.md`.

## Phases
1. **Capability gate** — can I browse? playwright? is my context enough? → `00_PREREQ/PREREQ.md`
2. **Research** — 3 targeted passes (config/order, CI Class Manager, duplicates/insert-update) via the shared harness
3. **Synthesis** — write the reference from evidence only
4. **QA** — coverage + citation check
5. **Final summary** — goal met? blockers? clarifications?

## Risks
- Official `docs.servicenow.com` is bot-walled for headless browsers → prefer `support.servicenow.com` KB and community.
- Search engines throttle (DDG/Bing) → harness falls back to a real-browser Startpage/Brave query.
- Free/local models lose tool discipline → answer must be built from the evidence digest, not memory.
- Context {ctx or 'unknown'} tokens: digests are truncated to 4–5k chars per call to stay inside it.

## Success criteria
- Covers ≥5 of: {', '.join(TOPICS)}
- Every non-trivial claim has a URL, or is explicitly UNVERIFIED
- Names the CI Class Manager locations it claims
- States blockers honestly instead of inventing content

## Capability verdict
{"CAN browse and research independently." if can_browse else "CANNOT browse — will request backup evidence and mark claims UNVERIFIED."}
""", encoding="utf-8")

    (root / "02_CLARIFICATIONS" / "CLARIFY.md").write_text(f"""# Clarifications / requests — {args.agent_id}

**Capability gate:** {'PASS' if can_browse else 'FAIL'}

## Questions for the orchestrator
{'- None.' if can_browse else '- I cannot browse. Please supply an evidence digest from an agent that can, or reassign Q2/Q3.'}

## Assumptions
- "Thorough" = configuration surface + processing order + CI Class Manager locations + duplicate/insert-update controls.
- ServiceNow release-agnostic unless a source pins a release.
""", encoding="utf-8")

    # ---- phase 2: research --------------------------------------------------------
    mark(phases, 2, "research_started", "Running 3 research passes through shared/research_harness.py")
    answers = {}
    for key, q in QUESTIONS:
        if not can_browse:
            answers[key] = ("BLOCKED: agent has no browsing capability; no sources could be reached. "
                            "Claims below are UNVERIFIED.")
            continue
        est = 6000
        try:
            with budget.acquire(args.provider, est_tokens=est, wait_s=1200):
                cmd = [sys.executable, str(SHARED / "research_harness.py"),
                       "--model", args.model, "--base-url", args.base_url,
                       "--question", q, "--rounds", args.rounds,
                       "--out", str(root / "research")]
                if args.api_key:
                    cmd += ["--api-key", args.api_key]
                p = subprocess.run(cmd, capture_output=True, text=True, timeout=2400)
                res = {}
                m = re.search(r'\{.*?"answer_chars".*?\}', p.stdout, re.S)
                if m:
                    res = json.loads(m.group(0))
                produced = sorted((root / "research").glob("*.md"), key=lambda x: x.stat().st_mtime)
                ans = ""
                if produced:
                    txt = produced[-1].read_text(encoding="utf-8", errors="replace")
                    ans = txt.split("## Answer", 1)[-1].split("## Transcript")[0].strip()
                answers[key] = ans or f"(no answer; harness error={res.get('error')})"
        except Exception as e:
            answers[key] = f"(budget/run error: {type(e).__name__}: {e})"
    mark(phases, 3, "research_done", "Research passes complete. Writing synthesis.")

    # ---- synthesis ----------------------------------------------------------------
    body = []
    section_titles = {
        "q1_config": "1. Configuration options and order of operations",
        "q2_classmgr": "2. CI Class Manager — key bread crumbs",
        "q3_dupes": "3. Preventing duplicates; insert vs update",
    }
    for key, title in section_titles.items():
        body.append(f"## {title}\n\n{answers.get(key, '(none)')}\n")

    doc = (f"# ServiceNow Discovery — Configuration Reference\n\n"
           f"*Generated by `{args.agent_id}` ({args.model} via {args.provider}) in worktree "
           f"`SNC_DISC__WT{args.wt_num}`.*\n\n"
           f"> Evidence gathered with a search→digest wrapper. Anything the agent could not source is\n"
           f"> marked UNVERIFIED. Verify against your instance release before production use.\n\n"
           + "\n".join(body))
    (root / "05_FINAL").mkdir(exist_ok=True)
    (root / "05_FINAL" / "DISCOVERY_CONFIG_REFERENCE.md").write_text(doc, encoding="utf-8")

    # ---- QA -----------------------------------------------------------------------
    # Score the BODY only: headings contain the topic words themselves and would
    # otherwise give a false pass.
    body_only = "\n".join(b.split("\n", 1)[-1] for b in body)
    full = body_only.lower()
    got = {k: bool(re.search(v, full)) for k, v in TOPICS.items()}
    urls = sorted(set(re.findall(r"https?://[^\s\)\]\"'<>]+", doc)))
    score = sum(got.values())
    (root / "04_QA" / "QA.md").write_text(f"""# QA — {args.agent_id}

| criterion | result |
|---|---|
| topic coverage | {score}/{len(TOPICS)} ({', '.join(k for k, v in got.items() if v) or 'none'}) |
| distinct sources cited | {len(urls)} |
| document size | {len(doc)} chars |
| capability gate | {'PASS' if can_browse else 'FAIL'} |

## Missing topics
{', '.join(k for k, v in got.items() if not v) or 'none'}

## Sources
{chr(10).join('- ' + u for u in urls[:20]) or '- none (no sources reached)'}

## Verdict
{'PASS (with caveats noted in final summary)' if score >= 5 and urls else 'PARTIAL — see blockers'}
""", encoding="utf-8")

    # ---- final + filescope ---------------------------------------------------------
    (root / "05_FINAL" / "FINAL_SUMMARY.md").write_text(f"""# Final summary — {args.agent_id}

- **Goal:** thorough ServiceNow Discovery configuration reference.
- **Goal achieved:** {'partially — see QA score' if score < len(TOPICS) else 'yes'}
- **QA score:** {score}/{len(TOPICS)} topics, {len(urls)} sources cited
- **Blockers:** {'none' if can_browse else 'no browsing capability; answer unsourced'}
- **Clarifications needed:** {'none' if can_browse and urls else 'evidence digest from a browsing agent'}
- **Context window:** {ctx or 'unknown'}
""", encoding="utf-8")

    try:
        git = subprocess.run(["git", "-C", args.wt, "status", "--porcelain"], capture_output=True, text=True, timeout=60)
        changed = git.stdout.strip() or "(nothing yet)"
        branch = subprocess.run(["git", "-C", args.wt, "branch", "--show-current"], capture_output=True, text=True, timeout=30).stdout.strip()
    except Exception as e:
        changed, branch = f"(git error {e})", "?"
    (root / "06_FILESCOPE" / "FILESCOPE.md").write_text(f"""# File scope — {args.agent_id}

- **Worktree:** `{args.wt}`
- **Branch:** `{branch}`
- **Folder:** `agents/{args.agent_id}/SNC_DISC__WT{args.wt_num}`
- **Model / provider:** `{args.model}` / `{args.provider}`

## Files this agent wrote
```
{chr(10).join(sorted(str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()))}
```

## git status (worktree)
```
{changed[:2000]}
```
""", encoding="utf-8")

    print(json.dumps({"agent": args.agent_id, "model": args.model, "can_browse": can_browse,
                      "qa_score": score, "topics": len(TOPICS), "sources": len(urls),
                      "chars": len(doc), "dir": str(root)}))


if __name__ == "__main__":
    main()
