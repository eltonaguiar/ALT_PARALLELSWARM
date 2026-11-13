#!/usr/bin/env python3
"""Run a roster of agents in parallel, each in its own worktree, and write a report."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from worktree_manager import create, worktree_path  # noqa: E402

RUNNER = HERE / "agent_runner.py"


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def extract_json(text: str) -> dict | None:
    starts = [m.start() for m in re.finditer(r"^\{", text, re.M)]
    for start in reversed(starts):
        try:
            return json.loads(text[start:])
        except Exception:
            continue
    return None


def run_one(task: dict, repo: Path, roster: dict, no_push: bool, extra_evidence: int) -> dict:
    agent_id = task["id"]
    wt = create(repo, agent_id, roster.get("base_branch", "main"),
                wt_number=int(task.get("wt", 2)))
    evidence = Path(task["evidence"])
    if not evidence.is_absolute():
        evidence = HERE / evidence
    cmd = [
        sys.executable, str(RUNNER),
        "--worktree", str(wt), "--agent-id", agent_id,
        "--model", task["model"], "--provider", task["provider"],
        "--wt", str(task.get("wt", 2)),
        "--evidence", str(evidence),
        "--brief", task["brief"],
        "--out-name", task.get("out", "WORKER_REPORT.md"),
        "--ledger", str(HERE / "state" / "usage_ledger.json"),
        "--max-tokens", str(task.get("max_tokens", 1500)),
        "--timeout", str(task.get("timeout", 480)),
        "--max-evidence-chars", str(task.get("max_evidence_chars", extra_evidence)),
    ]
    if task.get("fallbacks"):
        cmd += ["--fallback-models", *task["fallbacks"]]
    if task.get("fallback_provider"):
        cmd += ["--fallback-provider", task["fallback_provider"]]
    if no_push:
        cmd.append("--no-push")
    started = now()
    proc = subprocess.run(cmd, text=True, capture_output=True)
    log_dir = HERE / "state" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    (log_dir / f"{agent_id}.log").write_text(
        f"$ {' '.join(cmd)}\n\n--- stdout ---\n{proc.stdout}\n--- stderr ---\n{proc.stderr}\n")
    result = extract_json(proc.stdout) or {
        "agent_id": agent_id, "error": f"runner exited {proc.returncode}",
        "stderr": proc.stderr[-800:], "worktree": str(wt),
    }
    result["started"] = started
    result["finished"] = now()
    result["returncode"] = proc.returncode
    return result


def report(results: list[dict], roster: dict, wall_s: float) -> str:
    lines = [
        "# Orchestration report — SNC_DISC_RESEARCH (alt-swarm)",
        "",
        f"Generated: {now()}",
        f"Roster: `{roster['task']}` · agents: {len(results)} · "
        f"max_parallel: {roster.get('max_parallel', 1)} · wall time: {wall_s:.1f}s",
        "",
        "| agent | model | provider | QA | words | finish | branch | push |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in results:
        qa = "PASS" if r.get("qa_pass") else "FAIL"
        push = "ok" if r.get("pushed") else ("no-push" if r.get("push_error") is None else "error")
        model = r.get("model_used") or r.get("model")
        fallback = " (fallback)" if r.get("fallback_used") else ""
        lines.append(
            f"| `{r.get('agent_id')}` | `{model}`{fallback} | `{r.get('provider_used') or r.get('provider')}` | {qa} | "
            f"{r.get('words', '—')} | `{r.get('finish_reason')}` | `{r.get('branch', '—')}` | {push} |")
    lines += ["", "## Per-agent notes", ""]
    for r in results:
        lines += [
            f"### `{r.get('agent_id')}`",
            "",
            f"- Worktree: `{r.get('worktree')}`",
            f"- Folder: `agents/{r.get('agent_id')}/SNC_DISC__WT{r.get('wt', '?')}/`",
            f"- Evidence-limited draft: `05_FINAL/{r.get('out', 'WORKER_REPORT.md')}`",
            f"- Usage: `{r.get('usage')}`",
        ]
        if r.get("error"):
            lines.append(f"- Error: `{str(r['error'])[:500]}`")
        if r.get("push_error"):
            lines.append(f"- Push error: `{str(r['push_error'])[:500]}`")
        lines.append("")
    lines += [
        "## Read this correctly",
        "",
        "These are **independent, evidence-constrained drafts**, not authoritative",
        "research. Each worker had no browser and no shell; it received a pre-fetched",
        "digest produced by the orchestrator. Automated QA checks length, structure, and",
        "citations, not factual truth. The orchestrator's primary reference",
        "(`SNC_DISC__WT1/05_FINAL/DISCOVERY_CONFIG_REFERENCE.md`) is the synthesis to trust.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--roster", default=str(HERE / "roster.json"))
    parser.add_argument("--only", nargs="*", help="agent ids to run")
    parser.add_argument("--no-push", action="store_true")
    parser.add_argument("--max-evidence-chars", type=int, default=17000)
    parser.add_argument("--report", default=str(HERE / "ORCHESTRATION.md"))
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    roster = json.load(open(args.roster))
    tasks = roster["agents"]
    if args.only:
        tasks = [t for t in tasks if t["id"] in set(args.only)]
    started = now()
    wall0 = __import__("time").time()
    results: list[dict] = []
    with ThreadPoolExecutor(max_workers=int(roster.get("max_parallel", 1))) as pool:
        futures = {pool.submit(run_one, t, repo, roster, args.no_push,
                               args.max_evidence_chars): t for t in tasks}
        for fut in as_completed(futures):
            task = futures[fut]
            try:
                results.append(fut.result())
            except Exception as exc:
                results.append({"agent_id": task["id"], "model": task["model"],
                                "provider": task["provider"], "error": repr(exc),
                                "qa_pass": False})
    results.sort(key=lambda r: r.get("agent_id", ""))
    wall = __import__("time").time() - wall0
    text = report(results, roster, wall)
    Path(args.report).write_text(text)
    summary = {"started": started, "finished": now(), "wall_s": round(wall, 1),
               "results": results, "report": args.report}
    (HERE / "state" / "last_run.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
