#!/usr/bin/env python3
"""
run_swarm.py — run several models in parallel, each into its own "worktree-like"
folder, with a shared concurrency/cost ledger.

Each worker gets:
  <out>/<run>/<agent_id>/00_PREREQ/PREREQ.md
  <out>/<run>/<agent_id>/01_PLAN/PLAN.md
  <out>/<run>/<agent_id>/03_PHASES/phase1_started.md
  <out>/<run>/<agent_id>/03_PHASES/phase2_llm_call.md
  <out>/<run>/<agent_id>/03_PHASES/phase3_complete.md   (or FAILED.md)
  <out>/<run>/<agent_id>/05_FINAL/MODEL_REVIEW.md
  <out>/<run>/<agent_id>/transcript.md
  <out>/<run>/<agent_id>/06_FILESCOPE/FILESCOPE.md

Examples:
  python3 run_swarm.py --dry-run
  python3 run_swarm.py --max-parallel 2
  python3 run_swarm.py --agents qwen3.5-4b__ollama__nvidia-v4,qwen2.5-coder-7b__ollama__nvidia-v4
  python3 run_swarm.py --reference ../05_FINAL/DISCOVERY_CONFIG_REFERENCE.md
"""
from __future__ import annotations

import argparse
import json
import re
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

import usage_tracker as budget
from llm_client import LLMError, chat, load_roster

ROOT = Path(__file__).resolve().parent


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def slug(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "-", s).strip("-")


def build_prompt(reference: Path, max_chars: int) -> str:
    text = reference.read_text() if reference.exists() else "(reference missing)"
    # Send a review packet, not the whole document: high-signal sections.
    start = text.find("## 5. IRE deep dive")
    end = text.find("## 7. Verification")
    packet = text[start:end] if start != -1 and end != -1 else text[:max_chars]
    if len(packet) > max_chars:
        packet = packet[:max_chars]
    return f"""You are a skeptical ServiceNow CMDB/Discovery architect reviewing a reference document.

TASK: find concrete gaps, risky claims, and wrong details. Do not rewrite the document.

Rules:
- Base your review on the excerpt below. If you are unsure, say "unsure" instead of inventing.
- Prefer exact property names, table names, and navigation paths.
- No filler, no praise, no summary of the excerpt.

Return markdown with exactly these sections:
## 1. Five highest-risk gaps
## 2. Suspect property names, defaults, or navigation paths
## 3. Three duplicate-prevention tests that would catch regressions
## 4. One thing a real customer would still get wrong after reading this

EXCERPT:
{packet}
"""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n")


def run_one(agent, args, run_dir: Path, prompt: str) -> dict:
    adir = run_dir / slug(agent.id)
    write(
        adir / "00_PREREQ" / "PREREQ.md",
        f"""# Prerequisite / provenance

- Agent id: `{agent.id}`
- Model: `{agent.model}`
- Provider: `{agent.provider}`
- Base URL: `{agent.resolved_base_url()}`
- API key env: `{agent.resolved_key_env() or "(none)"}` — key present: **{bool(agent.api_key())}**
- Harness: `nvidia_v4_swarm/run_swarm.py` (Kilo CLI orchestration)
- Capability: text-only review via OpenAI-compatible chat API.
- Not used: browsing, Playwright, tools. This worker only critiques the supplied excerpt.
""",
    )
    write(
        adir / "01_PLAN" / "PLAN.md",
        f"""# Plan

Goal: independent adversarial review of the Discovery/IRE reference excerpt.
Output: `05_FINAL/MODEL_REVIEW.md` with four fixed sections.
Constraints: do not invent; mark uncertainty; max ~{agent.max_tokens} tokens.
Budget: provider `{agent.provider}`, max_inflight={agent.max_inflight},
daily_calls={agent.daily_calls}, daily_tokens={agent.daily_tokens}.
""",
    )
    write(adir / "03_PHASES" / "phase1_started.md", f"# Phase 1 started\n\n{now()}\n")

    status, err, usage, elapsed = "ok", "", {"tokens_in": 0, "tokens_out": 0}, 0.0
    try:
        with budget.acquire(
            agent.provider,
            est_tokens=min(agent.daily_tokens, 6000),
            wait_s=args.wait_s,
            model=agent.model,
        ) as res:
            write(
                adir / "03_PHASES" / "phase2_llm_call.md",
                f"# Phase 2 — LLM call\n\nStarted: {now()}\n\n"
                f"Model `{agent.model}` via `{agent.provider}`.\n",
            )
            t0 = time.time()
            try:
                resp = chat(
                    agent,
                    [{"role": "user", "content": prompt}],
                    max_tokens=args.max_tokens or agent.max_tokens,
                    timeout=args.timeout,
                )
                elapsed = time.time() - t0
                usage = resp["usage"]
                body = resp["text"] or "(empty response)"
                note = ""
                if resp["content_was_empty"] and resp["reasoning"]:
                    note = (
                        "\n\n> **Note:** provider returned empty `content`; "
                        "the text above is from the `reasoning` field.\n"
                    )
                write(
                    adir / "05_FINAL" / "MODEL_REVIEW.md",
                    f"# Independent model review — `{agent.id}`\n\n"
                    f"- Model: `{resp['model_reported']}`\n"
                    f"- Provider: `{agent.provider}`\n"
                    f"- Finish reason: `{resp['finish_reason']}`\n"
                    f"- Tokens in/out: {usage['tokens_in']}/{usage['tokens_out']}\n"
                    f"- Wall time: {elapsed:.1f}s\n\n---\n\n{body}{note}",
                )
                write(
                    adir / "transcript.md",
                    f"# Transcript\n\n- Agent: `{agent.id}`\n- Started: {now()}\n\n"
                    f"## Prompt\n\n```text\n{prompt}\n```\n\n"
                    f"## Response\n\n```text\n{body}\n```\n",
                )
                write(
                    adir / "03_PHASES" / "phase3_complete.md",
                    f"# Phase 3 — complete\n\n{now()}\n\n"
                    f"Tokens: {usage['tokens_in']} in / {usage['tokens_out']} out\n",
                )
                res.release(
                    tokens_in=usage["tokens_in"],
                    tokens_out=usage["tokens_out"],
                    status="ok",
                    note=f"{agent.id} {elapsed:.1f}s",
                )
            except Exception as e:
                elapsed = time.time() - t0
                status = "failed"
                err = f"{type(e).__name__}: {e}"
                write(
                    adir / "05_FINAL" / "FAILED.md",
                    f"# Worker failed\n\n- Agent: `{agent.id}`\n- Time: {now()}\n"
                    f"- Error: `{err}`\n\n```\n{traceback.format_exc()}\n```\n",
                )
                write(adir / "03_PHASES" / "phase3_failed.md", f"# Failed\n\n{now()}\n\n{err}\n")
                res.release(status="failed", note=err[:300])
    except (budget.BudgetExhausted, budget.BudgetTimeout) as e:
        status = "blocked"
        err = f"{type(e).__name__}: {e}"
        write(adir / "03_PHASES" / "phase2_blocked.md", f"# Blocked by budget\n\n{now()}\n\n{err}\n")
        write(adir / "05_FINAL" / "FAILED.md", f"# Blocked\n\n{err}\n")

    write(
        adir / "06_FILESCOPE" / "FILESCOPE.md",
        f"""# Filescope

- Agent: `{agent.id}`
- Model/provider: `{agent.model}` / `{agent.provider}`
- Folder: `{adir.relative_to(run_dir.parent)}`
- Status: **{status}**
- Tokens: {usage['tokens_in']} in / {usage['tokens_out']} out
- Wall time: {elapsed:.1f}s
- Error: {err or "(none)"}
""",
    )
    return {
        "agent": agent.id,
        "model": agent.model,
        "provider": agent.provider,
        "status": status,
        "tokens_in": usage["tokens_in"],
        "tokens_out": usage["tokens_out"],
        "elapsed_s": round(elapsed, 1),
        "error": err,
        "folder": str(adir),
    }


def main() -> None:
    p = argparse.ArgumentParser(description="Parallel model swarm runner")
    p.add_argument("--roster", default=str(ROOT / "models.yaml"))
    p.add_argument("--reference", default=str(ROOT.parent / "05_FINAL" / "DISCOVERY_CONFIG_REFERENCE.md"))
    p.add_argument("--out", default=str(ROOT / "runs"))
    p.add_argument("--agents", default="", help="comma-separated ids; default = enabled roster")
    p.add_argument("--max-parallel", type=int, default=2)
    p.add_argument("--max-tokens", type=int, default=0, help="override per-agent max_tokens")
    p.add_argument("--timeout", type=int, default=420)
    p.add_argument("--wait-s", type=int, default=600)
    p.add_argument("--max-chars", type=int, default=12000)
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()

    _, agents = load_roster(a.roster)
    if a.agents:
        wanted = {x.strip() for x in a.agents.split(",") if x.strip()}
        agents = [x for x in agents if x.id in wanted]
    else:
        agents = [x for x in agents if x.enabled]
    if not agents:
        raise SystemExit("no agents selected")

    for ag in agents:
        budget.configure(
            ag.provider,
            max_inflight=ag.max_inflight,
            daily_calls=ag.daily_calls,
            daily_tokens=ag.daily_tokens,
            price_in_per_1k=ag.price_in_per_1k,
            price_out_per_1k=ag.price_out_per_1k,
        )

    prompt = build_prompt(Path(a.reference), a.max_chars)
    if a.dry_run:
        print(json.dumps([ag.public_dict() for ag in agents], indent=2))
        print(f"\nprompt chars: {len(prompt)}")
        return

    run_dir = Path(a.out) / datetime.now().strftime("%Y%m%dT%H%M%SZ")
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "PROMPT.md").write_text(prompt)
    print(f"run dir: {run_dir}")
    print(f"agents: {len(agents)} | max_parallel: {a.max_parallel}")

    t0 = time.time()
    results = []
    with ThreadPoolExecutor(max_workers=max(1, a.max_parallel)) as pool:
        futs = {pool.submit(run_one, ag, a, run_dir, prompt): ag for ag in agents}
        for fut in as_completed(futs):
            ag = futs[fut]
            try:
                r = fut.result()
            except Exception as e:
                r = {
                    "agent": ag.id,
                    "model": ag.model,
                    "provider": ag.provider,
                    "status": "failed",
                    "tokens_in": 0,
                    "tokens_out": 0,
                    "elapsed_s": 0,
                    "error": f"{type(e).__name__}: {e}",
                    "folder": str(run_dir / slug(ag.id)),
                }
            results.append(r)
            print(f"  [{r['status']}] {r['agent']} ({r['elapsed_s']}s) {r['error']}")

    total = round(time.time() - t0, 1)
    results.sort(key=lambda x: x["agent"])
    ledger = budget.status()
    manifest = {
        "run": run_dir.name,
        "started_utc": now(),
        "wall_time_s": total,
        "max_parallel": a.max_parallel,
        "reference": str(a.reference),
        "prompt_chars": len(prompt),
        "results": results,
        "ledger": ledger,
    }
    (run_dir / "run_manifest.json").write_text(json.dumps(manifest, indent=2))

    lines = [
        f"# Swarm run {run_dir.name}",
        "",
        f"- Wall time: **{total}s**",
        f"- Max parallel: **{a.max_parallel}**",
        f"- Reference: `{a.reference}`",
        f"- Ledger: `{ledger.get('ledger')}`",
        "",
        "| agent | model | provider | status | tokens in/out | seconds |",
        "|---|---|---|---|---|---|",
    ]
    for r in results:
        lines.append(
            f"| `{r['agent']}` | `{r['model']}` | `{r['provider']}` | "
            f"**{r['status']}** | {r['tokens_in']}/{r['tokens_out']} | {r['elapsed_s']} |"
        )
    lines += ["", "## Failures / blocks", ""]
    bad = [r for r in results if r["status"] != "ok"]
    lines += [f"- `{r['agent']}`: {r['error']}" for r in bad] or ["- none"]
    lines += ["", "## Ledger snapshot", "", "```json", json.dumps(ledger, indent=2), "```", ""]
    (run_dir / "RUN_SUMMARY.md").write_text("\n".join(lines))
    print(f"\nsummary: {run_dir / 'RUN_SUMMARY.md'}")
    print(json.dumps({r["agent"]: r["status"] for r in results}, indent=2))


if __name__ == "__main__":
    main()
