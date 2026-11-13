#!/usr/bin/env python3
"""One worker lifecycle: prereq -> plan -> phase heartbeats -> LLM -> QA -> final -> commit."""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from router import chat  # noqa: E402
from worktree_manager import commit_and_push  # noqa: E402

SYSTEM = (
    "You are a meticulous ServiceNow CMDB/Discovery technical writer. "
    "You write only from the supplied evidence. You never invent property names, "
    "UI paths, defaults, or URLs. When the evidence is silent, you say so explicitly."
)


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def excerpt(path: Path, limit: int) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    if len(text) > limit:
        return text[:limit] + "\n\n[EVIDENCE TRUNCATED]"
    return text


def build_prompt(brief: str, evidence: str) -> list[dict]:
    user = f"""Write the section described below as Markdown for a ServiceNow Discovery
configuration reference (Brazil release).

SECTION BRIEF
{brief}

HARD RULES
1. Use ONLY the evidence below. If a fact is not in the evidence, write "not stated in
   the supplied evidence" instead of guessing.
2. Preserve exact property names, table names, and default values. Put them in backticks.
3. Every paragraph must end with one or more citations like [S1] matching the SOURCE
   markers. A paragraph without a citation is invalid. Do not invent examples that are
   not in the evidence.
4. Prefer tables for option inventories and decision rules.
5. Include an explicit "Assumptions / gaps" subsection at the end.
6. Do not restate the entire Discovery product overview; stay on the assigned section.
7. Target 700-1100 words. No preamble, no "here is".

EVIDENCE
{evidence}
"""
    return [{"role": "system", "content": SYSTEM},
            {"role": "user", "content": user}]


def automated_qa(text: str) -> tuple[list[tuple[str, bool, str]], bool]:
    words = len(re.findall(r"\b\w+\b", text))
    structured = (("\n|" in text) or ("\n- " in text)
                  or bool(re.search(r"(?m)^\s*\d+\.\s", text)))
    checks = [
        ("non-empty output", len(text.strip()) > 500, f"{len(text)} chars"),
        ("substantive length", words >= 350, f"{words} words"),
        ("has headings", text.count("\n#") >= 2, f"{text.count(chr(10) + '#')} headings"),
        ("has citations", bool(re.search(r"\[S\d+\]", text)), "citation markers"),
        ("has table or list", structured, "table/list"),
        ("no placeholder", "TODO" not in text.upper() and "TBD" not in text.upper(), "no TODO/TBD"),
    ]
    return checks, all(ok for _, ok, _ in checks)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worktree", required=True)
    parser.add_argument("--agent-id", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--provider", required=True)
    parser.add_argument("--wt", type=int, default=2)
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--brief", required=True)
    parser.add_argument("--out-name", default="WORKER_REPORT.md")
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--max-tokens", type=int, default=1500)
    parser.add_argument("--timeout", type=int, default=420)
    parser.add_argument("--max-evidence-chars", type=int, default=15000)
    parser.add_argument("--fallback-models", nargs="*", default=[])
    parser.add_argument("--fallback-provider", default="openrouter")
    parser.add_argument("--no-push", action="store_true")
    args = parser.parse_args()

    wt = Path(args.worktree).resolve()
    root = wt / "agents" / args.agent_id / f"SNC_DISC__WT{args.wt}"
    started = now()
    (root / "03_PHASES").mkdir(parents=True, exist_ok=True)

    write(root / "00_PREREQ" / "PREREQ.md", f"""# Pre-requisites — {args.agent_id}

**Model:** `{args.model}`
**Provider:** `{args.provider}`
**Harness:** ALT_PARALLELSWARM `swarm/agent_runner.py`
**Checked:** {started}

| Capability | Result | Consequence |
|---|---|---|
| Native browser tools | NO (worker is API-dispatched) | Cannot browse independently |
| Playwright / shell | NO (no tool loop) | Cannot fetch or verify pages |
| Pre-fetched evidence digest | YES | Write from the supplied evidence only |
| Context window | provider/model dependent | Digest capped at {args.max_evidence_chars} chars |

## Verdict

**CONDITIONAL PASS.** This worker does not browse. It is intentionally given a
pre-fetched, source-marked evidence digest produced by the orchestrator's own research
(the backup plan required by the task contract). Any claim not present in the digest must
be marked as a gap.
""")

    write(root / "01_PLAN" / "PLAN.md", f"""# Plan — {args.agent_id}

**Model:** `{args.model}` · **Provider:** `{args.provider}` · **Started:** {started}

## Goal

Produce the assigned section of the SNC_DISC_RESEARCH reference from the supplied
evidence, without inventing facts.

## Assigned section

{args.brief}

## Phases

1. Confirm evidence digest and constraints.
2. Call the model once (bounded tokens, no tools).
3. Write `05_FINAL/{args.out_name}`.
4. Run automated QA checks.
5. Write final summary and filescope.
6. Commit only `agents/{args.agent_id}/` and push the agent branch.

## Success criteria

- 700-1100 words, at least two headings, citations `[S#]`, tables/lists used.
- Every property/table/default is traceable to the digest.
- Gaps are declared rather than guessed.
""")

    write(root / "03_PHASES" / "phase1_evidence.md",
          f"# Phase 1 — evidence loaded\n\n**Started:** {now()}\n\n"
          f"Digest: `{args.evidence}`\n\nStatus: COMPLETE\n")

    evidence = excerpt(Path(args.evidence), args.max_evidence_chars)
    candidates = [(args.model, args.provider)]
    candidates += [(m, args.fallback_provider) for m in args.fallback_models]
    write(root / "03_PHASES" / "phase2_model_call.md",
          f"# Phase 2 — model call\n\n**Started:** {now()}\n\n"
          f"Candidates: `{candidates}` · Max tokens {args.max_tokens}. "
          "No tools; evidence-only. A fallback is tried on error, empty output, "
          "or a failed automated QA gate.\n")

    result = None
    error = None
    attempts = []
    model_used = None
    provider_used = None
    best = None
    text = ""
    for model, provider in candidates:
        try:
            candidate = chat(model, build_prompt(args.brief, evidence),
                             provider=provider, max_tokens=args.max_tokens,
                             timeout=args.timeout, ledger_path=args.ledger)
            candidate_text = (candidate or {}).get("text", "").strip()
            _, candidate_passed = automated_qa(candidate_text)
            attempts.append({"model": model, "provider": provider,
                             "chars": len(candidate_text), "qa_pass": candidate_passed,
                             "finish_reason": (candidate or {}).get("finish_reason"),
                             "error": None})
            if best is None or len(candidate_text) > len(best[2]):
                best = (candidate, model, candidate_text, provider)
            if len(candidate_text) >= 200 and candidate_passed:
                result, model_used, text, provider_used = candidate, model, candidate_text, provider
                break
            error = f"QA gate failed for {model} ({len(candidate_text)} chars)"
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
            attempts.append({"model": model, "provider": provider,
                             "chars": 0, "qa_pass": False,
                             "finish_reason": None, "error": error})

    if model_used is None and best is not None:
        result, model_used, text, provider_used = best
    text = text if model_used else (result or {}).get("text", "").strip()
    if not text and result and result.get("thinking"):
        text = ("_The model returned reasoning but no final content. Raw reasoning is "
                "preserved below for diagnosis._\n\n" + result["thinking"].strip())

    write(root / "03_PHASES" / "phase3_draft.md",
          f"# Phase 3 — draft\n\n**Started:** {now()}\n\n"
          f"Attempts: `{attempts}`\n\n"
          f"Finish reason: `{(result or {}).get('finish_reason')}` · "
          f"Usage: `{(result or {}).get('usage')}` · Error: `{error}`\n")

    header = f"""# Worker report — {args.agent_id}

**Task:** SNC_DISC_RESEARCH
**Model (primary):** `{args.model}`
**Model (used):** `{model_used or 'none'}`
**Provider:** `{provider_used or args.provider}`
**Harness:** ALT_PARALLELSWARM `swarm/agent_runner.py`
**Generated:** {now()}
**Evidence:** `{Path(args.evidence).name}` (pre-fetched; worker has no browser)
**Assigned section:** {args.brief}

> This is an independent worker draft. It is evidence-constrained, not independently
> web-verified. The orchestrator's primary reference is the authoritative synthesis.

---

"""
    write(root / "05_FINAL" / args.out_name, header + (text or
          f"**MODEL CALL FAILED.** {error}"))

    checks, passed = automated_qa(text)
    qa_lines = [f"# QA — {args.agent_id}", "", f"**Checked:** {now()}", "",
                "| Check | Pass | Evidence |", "|---|---|---|"]
    for name, ok, detail in checks:
        qa_lines.append(f"| {name} | {'YES' if ok else 'NO'} | {detail} |")
    qa_lines += ["", f"**Overall:** {'PASS' if passed else 'FAIL'}", "",
                 "## Manual caveat", "",
                 "Automated checks cannot verify factual accuracy. The orchestrator must",
                 "spot-check property names and defaults against `research/SOURCES.md`."]
    write(root / "04_QA" / "QA.md", "\n".join(qa_lines))

    write(root / "05_FINAL" / "FINAL_SUMMARY.md", f"""# Final summary — {args.agent_id}

**Model:** `{args.model}` · **Provider:** `{args.provider}`

## Goal met?

{'Yes, partially: the assigned section was produced and passed automated QA.' if passed else 'No. The assigned section is incomplete or failed automated QA.'}

## Blockers

{('- Model call error: `' + error + '`') if error else '- None at the API level.'}
- Independent browsing: unavailable by design; evidence was supplied.

## Clarifications needed

- Confirm the target release (this run uses Brazil evidence).
- Confirm whether the customer uses probe-based or pattern-based discovery.
- Confirm which data sources are authoritative for reconciliation.

## QA

See `04_QA/QA.md`. Automated result: **{'PASS' if passed else 'FAIL'}**.
""")

    write(root / "06_FILESCOPE" / "FILESCOPE.md", f"""# File scope — {args.agent_id}

**Worktree:** `{wt}`
**Branch:** `agent/{args.agent_id}`
**Folder:** `agents/{args.agent_id}/SNC_DISC__WT{args.wt}/`

## Files written

- `00_PREREQ/PREREQ.md`
- `01_PLAN/PLAN.md`
- `03_PHASES/phase1_evidence.md`
- `03_PHASES/phase2_model_call.md`
- `03_PHASES/phase3_draft.md`
- `04_QA/QA.md`
- `05_FINAL/{args.out_name}`
- `05_FINAL/FINAL_SUMMARY.md`
- `06_FILESCOPE/FILESCOPE.md`

## Files modified outside the folder

None. The runner stages only `agents/{args.agent_id}/`.
""")

    commit = commit_and_push(wt, args.agent_id,
                             f"agent({args.agent_id}): SNC_DISC worker draft",
                             push=not args.no_push)
    summary = {
        "agent_id": args.agent_id, "model": args.model, "provider": args.provider,
        "wt": args.wt, "out": args.out_name,
        "model_used": model_used, "provider_used": provider_used,
        "fallback_used": bool(model_used and model_used != args.model),
        "attempts": attempts,
        "worktree": str(wt), "branch": commit["branch"], "qa_pass": passed,
        "words": len(re.findall(r"\b\w+\b", text)), "chars": len(text),
        "finish_reason": (result or {}).get("finish_reason"),
        "usage": (result or {}).get("usage"), "error": error if not model_used else None,
        "committed": commit["committed"], "pushed": commit["pushed"],
        "push_error": commit["push_error"], "started": started, "finished": now(),
    }
    write(root / "06_FILESCOPE" / "RESULT.json", json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
